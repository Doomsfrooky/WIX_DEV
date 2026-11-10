#!/usr/bin/env python3
"""Photos kept in the repository (site/media/), optimised for the web.

Decision 2026-11-09 (the client: "관리가 쉬운 쪽으로"): people portraits and new gallery photos live in the
repository as web-ready copies; originals never go in. Every copy is auto-rotated from EXIF, stripped of all
metadata (camera, GPS location), resized and saved as progressive JPEG. Videos stay on Wix media, and photos
that are already on Wix or Imgur keep their URLs.

    python3 tools/media.py people  <image> --name 김강현 --slug kim-ganghyun [--crop x,y,w,h]
        4:5 portrait (centre crop unless --crop), at most 640x800 -> site/media/people/<slug>.jpg,
        and data/people.json gets photo = "media/people/<slug>.jpg" for that name.
    python3 tools/media.py gallery <zip or folder> [--sheet captions.xlsx]
        every image (jpg, png, webp, heic) -> site/media/gallery/<year>/<year>-<nn>-<w>.jpg in widths
        480 / 1024 / 1600 (never upscaled: a smaller source adds its own width, e.g. 480 / 599), appended to
        data/gallery.json (newest first) as
        {src: "media/gallery/<year>/<year>-<nn>", widths: [...], width, height, year, caption_ko, caption_en}.
        Captions and years come from the sheet (columns: 파일명, 연도, 설명(한국어), 설명(영어)); a missing year
        falls back to the photo's EXIF date, and a photo with neither is skipped. Write '-' (or 연도 없음, 미상) as
        the year of a photo whose year nobody knows: it goes to site/media/gallery/undated/ with year "" (shown under
        '전체' only, with no year label) at the end of data/gallery.json. Within a year, photos keep the sheet's file
        order (name the files so they sort newest first); existing entries keep their order.
    python3 tools/media.py template <out.xlsx>
        the caption sheet to fill in.
    python3 tools/media.py figure  <image> --slug <name> [--crop x,y,w,h]
        a diagram or figure, never cropped unless --crop -> site/media/figures/<slug>-<w>.jpg in widths 800 / 1600
        (never upscaled; the source width is used when it is smaller), quality 88 so lettering stays clean.
        Prints the {src, widths, width, height} to put in the page.

Paths in data are relative to site/ (the pages live there). Pages one level deeper resolve them through the
page shell's prefix.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif')
GALLERY_WIDTHS = (480, 1024, 1600)
UNDATED = 'undated'                       # the sheet said the year is unknown
Image.MAX_IMAGE_PIXELS = 80_000_000          # refuse absurd images (decompression bombs)


def load_image(path):
    """Open any supported image (HEIC through ImageMagick), apply the EXIF rotation, return (RGB image, exif year)."""
    if path.lower().endswith(('.heic', '.heif')):
        tmp = tempfile.mkdtemp(prefix='media-')
        out = os.path.join(tmp, 'x.jpg')
        subprocess.run(['convert', path, out], check=True, capture_output=True)
        path = out
    im = Image.open(path)
    year = None
    try:
        dt = im.getexif().get_ifd(0x8769).get(0x9003) or im.getexif().get(0x0132)   # DateTimeOriginal / DateTime
        if dt:
            year = int(str(dt)[:4])
    except Exception:
        pass
    im = ImageOps.exif_transpose(im)
    if im.mode not in ('RGB', 'L'):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.convert('RGBA').split()[-1])
        im = bg
    return im.convert('RGB'), year


def save_jpeg(im, path, q=82):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, 'JPEG', quality=q, optimize=True, progressive=True)   # no exif/icc passed: metadata is dropped
    return os.path.getsize(path)


def people(args):
    im, _ = load_image(args.image)
    if args.crop:
        x, y, w, h = (int(v) for v in args.crop.split(','))
        im = im.crop((x, y, x + w, y + h))
    else:                                    # centre crop to 4:5, keeping the upper part (faces sit high)
        W, H = im.size
        if W / H > 0.8:
            w = round(H * 0.8); x = (W - w) // 2; im = im.crop((x, 0, x + w, H))
        else:
            h = round(W / 0.8); im = im.crop((0, 0, W, h))
    tw = min(640, im.size[0])
    im = im.resize((tw, round(tw / 0.8)), Image.LANCZOS)
    rel = f'media/people/{args.slug}.jpg'
    size = save_jpeg(im, os.path.join(SITE, rel))
    pj = os.path.join(ROOT, 'data', 'people.json')
    data = json.load(open(pj, encoding='utf-8'))
    hits = [m for tm in data for m in tm['members'] if m['name'] == args.name]
    if len(hits) != 1:
        sys.exit(f'{args.name}: {len(hits)} matches in data/people.json (need exactly 1)')
    hits[0]['photo'] = rel
    json.dump(data, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{args.name}: site/{rel} {im.size[0]}x{im.size[1]} {size // 1024} KB')


def read_sheet(path):
    import openpyxl
    rows = {}
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if not r or not r[0]:
            continue
        name = os.path.basename(str(r[0]).strip())
        y = str(r[1]).strip() if r[1] is not None else ''
        year = UNDATED if y in ('-', '연도 없음', '미상') else (int(float(y)) if y else None)
        rows[name.lower()] = dict(year=year, ko=(r[2] or '').strip() if len(r) > 2 else '',
                                  en=(r[3] or '').strip() if len(r) > 3 else '')
    return rows


def safe_extract(zpath, dest):
    """Extract only image files, flattening paths (no zip-slip, no executables)."""
    out = []
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = os.path.basename(info.filename)
            if info.is_dir() or not name.lower().endswith(IMG_EXT + ('.xlsx',)) or name.startswith('.'):
                continue
            target = os.path.join(dest, name)
            with z.open(info) as src, open(target, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            out.append(target)
    return out


def gallery(args):
    src = os.path.abspath(args.source)
    work = tempfile.mkdtemp(prefix='gallery-')       # a new, empty folder for untrusted input
    files = safe_extract(src, work) if zipfile.is_zipfile(src) else [os.path.join(src, f) for f in sorted(os.listdir(src))]
    sheet_path = args.sheet or next((f for f in files if f.lower().endswith('.xlsx')), None)
    sheet = read_sheet(sheet_path) if sheet_path else {}
    images = sorted(f for f in files if f.lower().endswith(IMG_EXT))
    gj = os.path.join(ROOT, 'data', 'gallery.json')
    data = json.load(open(gj, encoding='utf-8'))
    added = []
    for f in images:
        meta = sheet.get(os.path.basename(f).lower(), {})
        im, exif_year = load_image(f)
        year = meta.get('year') or exif_year
        if not year:
            print(f'skip {os.path.basename(f)}: no year in the sheet or EXIF'); continue
        folder = UNDATED if year == UNDATED else str(year)
        n = 1 + sum(1 for d in data + added if str(d.get('src', '')).startswith(f'media/gallery/{folder}/'))
        stem = f'media/gallery/{folder}/{folder}-{n:02d}'
        widths = []
        for w in GALLERY_WIDTHS:
            tw = min(w, im.size[0])
            if widths and tw - widths[-1] < 64:      # a source a little wider than the last width adds nothing
                break
            save_jpeg(im.resize((tw, round(im.size[1] * tw / im.size[0])), Image.LANCZOS) if tw != im.size[0] else im,
                      os.path.join(SITE, f'{stem}-{tw}.jpg'), q=80)
            widths.append(tw)
            if tw < w:                               # a smaller source: its own width is the last one (never upscaled)
                break
        added.append(dict(src=stem, widths=widths, width=im.size[0], height=im.size[1], year='' if year == UNDATED else str(year),
                          caption_ko=meta.get('ko', ''), caption_en=meta.get('en', ''), file=os.path.basename(f)))
        print(f'{os.path.basename(f)} -> site/{stem}-{{{",".join(map(str, widths))}}}.jpg ({im.size[0]}x{im.size[1]}, {year})')
    dated = sorted((d for d in added if d['year']), key=lambda d: d['year'], reverse=True)   # stable: sheet order within a year
    undated = [d for d in added if not d['year']]
    json.dump(dated + data + undated, open(gj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    missing = [d['file'] for d in added if not d['caption_ko']]
    print(f'{len(added)} photos added to data/gallery.json' + (f'; no caption yet: {", ".join(missing)}' if missing else ''))
    shutil.rmtree(work, ignore_errors=True)


FIGURE_WIDTHS = (800, 1600)


def figure(args):
    im, _ = load_image(args.image)
    if args.crop:
        x, y, w, h = (int(v) for v in args.crop.split(','))
        im = im.crop((x, y, x + w, y + h))
    stem = f'media/figures/{args.slug}'
    widths = []
    for w in FIGURE_WIDTHS:
        tw = min(w, im.size[0])
        if tw in widths:
            break
        size = save_jpeg(im.resize((tw, round(im.size[1] * tw / im.size[0])), Image.LANCZOS) if tw != im.size[0] else im,
                         os.path.join(SITE, f'{stem}-{tw}.jpg'), q=88)
        widths.append(tw)
        print(f'site/{stem}-{tw}.jpg {size // 1024} KB')
    print(json.dumps(dict(src=stem, widths=widths, width=im.size[0], height=im.size[1])))


def template(args):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = '갤러리 사진'
    ws.append(['파일명', '연도', '설명(한국어)', '설명(영어, 없어도 됨)'])
    ws.append(['IMG_0001.jpg', 2026, '2026 대한이비인후과학회 춘계학술대회 발표', 'Talk at the 2026 spring meeting of the Korean Society of Otorhinolaryngology'])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, w in zip('ABCD', (22, 8, 48, 60)):
        ws.column_dimensions[col].width = w
    wb.save(args.out)
    print('wrote', args.out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('people'); p.add_argument('image'); p.add_argument('--name', required=True); p.add_argument('--slug', required=True); p.add_argument('--crop')
    g = sub.add_parser('gallery'); g.add_argument('source'); g.add_argument('--sheet')
    t = sub.add_parser('template'); t.add_argument('out')
    f = sub.add_parser('figure'); f.add_argument('image'); f.add_argument('--slug', required=True); f.add_argument('--crop')
    a = ap.parse_args()
    {'people': people, 'gallery': gallery, 'template': template, 'figure': figure}[a.cmd](a)


if __name__ == '__main__':
    main()
