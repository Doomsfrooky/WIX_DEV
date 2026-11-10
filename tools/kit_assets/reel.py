#!/usr/bin/env python3
"""Direction C2 (a copy of direction C's tool) · the hero reel's data budget (CLAUDE.md: video data).

The promo footage (Hearing Big-data Center promo, 480p only) is one 21.2 MB MP4. The hero shows four short shots from it
(about 7.3 s in all). A plain <video> that seeks to each shot makes Chrome read about 3 MB ahead of every seek point,
so the first pass of the reel would cost about 10 MB. This script precomputes, from a local copy of the file, everything
the page needs to fetch only the bytes of the shots it uses:

  ranges   one HTTP byte range per shot: from the keyframe at or before the in point (the promo has a closed GOP and a
           keyframe every 2.000 s) to a little past the out point
  pieces   where the video samples sit inside each fetched range (audio is interleaved; it is dropped)
  head     ftyp + a rebuilt moov (video track only, the four windows laid end to end at SPACING s intervals, sample
           tables rewritten) + the mdat header, base64
  shots    in/out times inside the assembled clip (t0, t1), plus the crop and speed of each shot

The page fetches the ranges (Range is CORS-safelisted; video.wixstatic.com answers 206 with ACAO *), concatenates
head + pieces into a Blob and plays that in one <video>: about 1.3 MB for the whole reel, nothing more after that.

    python3 -I tools/kits/cw/reel.py PROMO.mp4 [--clip out.mp4]    # writes tools/kits/cw/reel.json
    (--clip also writes the assembled clip for checking with ffprobe/ffmpeg)

The file is not stored in the repository (CLAUDE.md decision 2); fetch it with curl to a scratch folder first.
"""
import base64
import json
import os
import struct
import sys

SRC = 'https://video.wixstatic.com/video/b8629b_b4d81b25a9d641439ec983afe489fd43/480p/mp4/file.mp4'
SPACING = 5.0      # s between window starts in the assembled clip (every window is shorter than 4 s)
TAIL = 0.25        # s of frames kept past each out point (B-frame reorder depth is 3 frames = 0.125 s)

# shot list: in/out (s) in the promo, kept >= .1 s inside the promo's own cuts (112.0/114.3, 84.0, 177.75, 184.5, 186.0,
# 188.4); y0/y1 the usable band (burned-in subtitles and the chair's fall-caution sign excluded); fx/fy the subject;
# ax where it sits across the frame (the title covers the left edge); r playback rate. Crops are from the /67 final.
SHOTS = [
    # (otology clinic, ear examination, 174.06-177.35: removed 2026-11-10 at the client's request, a patient is shown)
    dict(a=112.1, b=114.15, y0=0, y1=.78, fx=.7, fy=.58, ax=.62, r=.8, near=0),     # audiometer, hands on the keys
    dict(a=82.1, b=83.88, y0=0, y1=.84, fx=.8, fy=.3, ax=.7, r=.8, near=0),         # researcher at the code screens
    dict(a=182.98, b=184.38, y0=0, y1=.84, fx=.46, fy=.56, ax=.56, r=.8, near=1),   # team meeting
    dict(a=186.12, b=188.25, y0=0, y1=.84, fx=.5, fy=.5, ax=.58, r=.78, near=1),    # earbud fitting, close-up
]
# near=1: the two shots inside one 15 s stretch of the file. If the page cannot assemble the clip (a browser that
# preflights Range, a changed file), it falls back to one player seeking the original URL and plays only these two,
# so Chrome's read-ahead stays near 3 MB.


def boxes(d, start, end):
    o = start
    while o < end:
        sz, typ = struct.unpack('>I4s', d[o:o + 8])
        h = 8
        if sz == 1:
            sz = struct.unpack('>Q', d[o + 8:o + 16])[0]
            h = 16
        elif sz == 0:
            sz = end - o
        yield typ.decode('latin-1'), o, o + h, o + sz
        o += sz


def child(d, parent, name):
    for t, o, b, e in boxes(d, parent[2], parent[3]):
        if t == name:
            return (t, o, b, e)
    return None


def full(d, bx):            # payload after version/flags
    return bx[2] + 4


def u32(d, o):
    return struct.unpack('>I', d[o:o + 4])[0]


def box(name, payload):
    return struct.pack('>I4s', 8 + len(payload), name.encode()) + payload


def fbox(name, payload, version=0, flags=0):
    return box(name, struct.pack('>I', (version << 24) | flags) + payload)


def video_track(d):
    moov = next(x for x in boxes(d, 0, len(d)) if x[0] == 'moov')
    ftyp = next(x for x in boxes(d, 0, len(d)) if x[0] == 'ftyp')
    for trak in (x for x in boxes(d, moov[2], moov[3]) if x[0] == 'trak'):
        mdia = child(d, trak, 'mdia')
        hdlr = child(d, mdia, 'hdlr')
        if d[hdlr[2] + 8:hdlr[2] + 12] != b'vide':
            continue
        return dict(ftyp=ftyp, moov=moov, trak=trak, mdia=mdia, hdlr=hdlr, mvhd=child(d, moov, 'mvhd'),
                    tkhd=child(d, trak, 'tkhd'), edts=child(d, trak, 'edts'), mdhd=child(d, mdia, 'mdhd'),
                    minf=child(d, mdia, 'minf'))
    raise SystemExit('no video track')


def tables(d, v):
    minf = v['minf']
    stbl = child(d, minf, 'stbl')
    get = lambda n: child(d, stbl, n)
    ts = u32(d, v['mdhd'][2] + 12)                                      # mdhd v0: timescale after creation/modification
    elst = child(d, v['edts'], 'elst')
    assert d[elst[2]] == 0 and u32(d, elst[2] + 4) == 1, 'expects one v0 edit-list entry'
    shift = struct.unpack('>i', d[elst[2] + 12:elst[2] + 16])[0]
    # stts -> dts per sample
    p = full(d, get('stts'))
    dts, t = [], 0
    for i in range(u32(d, p)):
        n, delta = struct.unpack('>II', d[p + 4 + 8 * i:p + 12 + 8 * i])
        for _ in range(n):
            dts.append(t)
            t += delta
    end = t
    N = len(dts)
    # ctts (v0, unsigned)
    ct = [0] * N
    c = get('ctts')
    if c:
        assert d[c[2]] == 0, 'expects ctts v0'
        p, k = full(d, c), 0
        for i in range(u32(d, p)):
            n, off = struct.unpack('>II', d[p + 4 + 8 * i:p + 12 + 8 * i])
            for _ in range(n):
                ct[k] = off
                k += 1
    p = full(d, get('stss'))
    sync = {u32(d, p + 4 + 4 * i) - 1 for i in range(u32(d, p))}
    p = full(d, get('stsz'))
    fixed, cnt = u32(d, p), u32(d, p + 4)
    sizes = [fixed] * cnt if fixed else [u32(d, p + 8 + 4 * i) for i in range(cnt)]
    co = get('stco') or get('co64')
    p = full(d, co)
    wide = co[0] == 'co64'
    chunks = [struct.unpack('>Q', d[p + 4 + 8 * i:p + 12 + 8 * i])[0] if wide else u32(d, p + 4 + 4 * i) for i in range(u32(d, p))]
    p = full(d, get('stsc'))
    stsc = [struct.unpack('>III', d[p + 4 + 12 * i:p + 16 + 12 * i]) for i in range(u32(d, p))]
    offs, s = [], 0
    for j, (first, per, _) in enumerate(stsc):
        last = stsc[j + 1][0] - 1 if j + 1 < len(stsc) else len(chunks)
        for ch in range(first - 1, last):
            o = chunks[ch]
            for _ in range(per):
                offs.append(o)
                o += sizes[s]
                s += 1
    assert len(offs) == N == len(sizes)
    return dict(ts=ts, shift=shift, dts=dts, end=end, ct=ct, sync=sync, sizes=sizes, offs=offs, stbl=stbl,
                stsd=d[get('stsd')[1]:get('stsd')[3]])


def rle(vals):
    out = []
    for x in vals:
        if out and out[-1][1] == x:
            out[-1][0] += 1
        else:
            out.append([1, x])
    return out


def build(d):
    v = video_track(d)
    T = tables(d, v)
    ts, shift, dts, ct = T['ts'], T['shift'], T['dts'], T['ct']
    N = len(dts)
    pts = lambda i: (dts[i] + ct[i] - shift) / ts
    wins = []
    for sh in SHOTS:
        s = max(i for i in T['sync'] if pts(i) <= sh['a'] + 1e-6)
        e = max(j for j in range(s, N) if pts(j) <= sh['b'] + TAIL)
        wins.append((s, e))
    # new decode timeline: window i's keyframe is presented at exactly i * SPACING
    ndts, ndur, order = [], [], []
    for wi, (s, e) in enumerate(wins):
        start = round(wi * SPACING * ts) + shift - ct[s]
        if ndts:
            gap = start - ndts[-1]
            assert gap > 0, 'windows overlap: raise SPACING'
            ndur[-1] = gap
        for j in range(s, e + 1):
            ndts.append(start + (dts[j] - dts[s]))
            ndur.append(dts[j + 1] - dts[j] if j + 1 < N else T['end'] - dts[j])
            order.append(j)
    media_dur = ndts[-1] + ndur[-1]
    # byte ranges (one per window) and the video pieces inside each
    ranges, pieces, payload = [], [], 0
    for s, e in wins:
        lo = min(T['offs'][j] for j in range(s, e + 1))
        hi = max(T['offs'][j] + T['sizes'][j] for j in range(s, e + 1))
        ranges.append([lo, hi - 1])
        pc = []
        for j in range(s, e + 1):
            o, l = T['offs'][j] - lo, T['sizes'][j]
            if pc and pc[-2] + pc[-1] == o:
                pc[-1] += l
            else:
                pc += [o, l]
            payload += l
        pieces.append(pc)
    # rebuilt moov (video track only)
    n_per = [e - s + 1 for s, e in wins]
    stts = fbox('stts', struct.pack('>I', len(rle(ndur))) + b''.join(struct.pack('>II', n, x) for n, x in rle(ndur)))
    cts = rle([ct[j] for j in order])
    ctts = fbox('ctts', struct.pack('>I', len(cts)) + b''.join(struct.pack('>II', n, x) for n, x in cts))
    syn = [k + 1 for k, j in enumerate(order) if j in T['sync']]
    stss = fbox('stss', struct.pack('>I', len(syn)) + b''.join(struct.pack('>I', x) for x in syn))
    stsc = fbox('stsc', struct.pack('>I', len(wins)) + b''.join(struct.pack('>III', i + 1, n, 1) for i, n in enumerate(n_per)))
    stsz = fbox('stsz', struct.pack('>II', 0, len(order)) + b''.join(struct.pack('>I', T['sizes'][j]) for j in order))

    def assemble(chunk_offsets):
        stco = fbox('stco', struct.pack('>I', len(chunk_offsets)) + b''.join(struct.pack('>I', x) for x in chunk_offsets))
        stbl = box('stbl', T['stsd'] + stts + ctts + stss + stsc + stsz + stco)
        raw = lambda bx: bytearray(d[bx[1]:bx[3]])
        minf = v['minf']
        parts = [raw(x) for x in (child(d, minf, 'vmhd'), child(d, minf, 'dinf'))]
        minf_b = box('minf', b''.join(bytes(p) for p in parts) + stbl)
        mdhd = raw(v['mdhd'])
        struct.pack_into('>I', mdhd, 24, media_dur)
        movie_ms = round(media_dur / ts * 1000)
        mdia = box('mdia', bytes(mdhd) + bytes(raw(v['hdlr'])) + minf_b)
        tkhd = raw(v['tkhd'])
        assert tkhd[8] == 0, 'expects tkhd v0'
        struct.pack_into('>I', tkhd, 28, movie_ms)
        elst = fbox('elst', struct.pack('>I', 1) + struct.pack('>IiHH', movie_ms, shift, 1, 0))
        trak = box('trak', bytes(tkhd) + box('edts', elst) + mdia)
        mvhd = raw(v['mvhd'])
        assert mvhd[8] == 0 and u32(d, v['mvhd'][1] + 20) == 1000, 'expects mvhd v0 with timescale 1000'
        struct.pack_into('>I', mvhd, 24, movie_ms)
        ftyp = d[v['ftyp'][1]:v['ftyp'][3]]
        return ftyp + box('moov', bytes(mvhd) + trak)

    # chunk offsets depend on the head length, which does not depend on their values: build twice
    head0 = assemble([0] * len(wins)) + struct.pack('>I4s', 8 + payload, b'mdat')
    co, at = [], len(head0)
    for n, (s, e) in zip(n_per, wins):
        co.append(at)
        at += sum(T['sizes'][j] for j in range(s, e + 1))
    head = assemble(co) + struct.pack('>I4s', 8 + payload, b'mdat')
    assert len(head) == len(head0)
    shots = []
    for wi, ((s, e), sh) in enumerate(zip(wins, SHOTS)):
        k = pts(s)
        x = {key: sh[key] for key in ('y0', 'y1', 'fx', 'fy', 'ax', 'r', 'near')}
        x.update(a=sh['a'], b=sh['b'], t0=round(wi * SPACING + sh['a'] - k, 4), t1=round(wi * SPACING + sh['b'] - k, 4))
        shots.append(x)
    fp = [d[T['offs'][s]:T['offs'][s] + 8].hex() for s, e in wins]
    data = dict(src=SRC, size=len(d), w=854, h=480, head=base64.b64encode(head).decode(), ranges=ranges, pieces=pieces,
                fp=fp, bytes=sum(r[1] - r[0] + 1 for r in ranges), clip=len(head) + payload, shots=shots)
    clip = head + b''.join(d[T['offs'][j]:T['offs'][j] + T['sizes'][j]] for j in order)
    assert len(clip) == data['clip']
    return data, clip


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    d = open(args[0], 'rb').read()
    data, clip = build(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reel.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
        f.write('\n')
    if '--clip' in args:
        with open(args[args.index('--clip') + 1], 'wb') as f:
            f.write(clip)
    print(f'{out}: {len(data["ranges"])} ranges, {data["bytes"] / 1e6:.2f} MB fetched, clip {data["clip"] / 1e6:.2f} MB, '
          f'head {len(base64.b64decode(data["head"]))} B')
    for s in data['shots']:
        print(f'  {s["a"]:7.2f}-{s["b"]:7.2f}  ->  clip {s["t0"]:6.3f}-{s["t1"]:6.3f}')


if __name__ == '__main__':
    main()
