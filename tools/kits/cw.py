#!/usr/bin/env python3
"""Direction C2 · editorial cinematic on white (에디토리얼 시네마틱 · 흰 지면). Direction C (tools/kits/c.py) re-designed
for one white sheet: the live site's Wix header, ground and footer are #ffffff, so the page is white from top to bottom.
People and the field first: big photographs and footage, the asymmetric 34/66 axis, blunt display type, the boldest motion.

One system on white paper; the cinema comes from the editing, not from a dark ground (tools/kits/cw/):
  hero     a bounded footage frame on the sheet; an ink cut line is drawn, holds a beat, splits, and the frame opens from
           it; the title crosses the frame's edge as a knockout (ink on the paper, paper white over the photograph); the
           line's lower half stays under the picture as the reel's umber clock; rack focus, hard cuts, counter wheels
  reading  the Research list and People on the same white: the same axis (the frame's left edge at 34% of the width), an
           ink rule that is drawn to open each block, every portrait cut open from an ink line through its middle, a reel
           of 120 frames (one per publication) that shows where the filter and the page sit in the whole record
Design document: site/_directions/cw.design.md.   Build: python3 tools/directions.py cw
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import core  # noqa: E402
from core import t, e, img, imgur, name_pair, member_role, initials, lang_attr  # noqa: E402

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cw')


def rd(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


ARROW_R = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>'
ARROW_L = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>'


def nw_paren(s):
    """Keep a parenthetical with the word before it: '특허 (출원·등록)' never breaks inside the brackets."""
    return re.sub(r' (\([^)]*\))', r' <span class="nw">\1</span>', s)


# ================================================================== hero (the /67 final, filled from core)
def hero():
    h = re.sub(r'^\s*<!--.*?-->\s*', '', rd('hero.html'), count=1, flags=re.S)
    inst_en = core.INST[1].replace(' · ', ' · <span class="nw">', 1) + '</span>'
    lead = t(core.HOME_LEAD[0], core.HOME_LEAD[1], 'p', 'cx-lead', 'data-a')
    nums = '\n      '.join(
        f'<li data-ai><b><span class="cx-n" data-n="{n}" aria-hidden="true">{n}</span><span class="sr">{n}</span></b>'
        f'{t(nw_paren(ko), en)}</li>' for n, (ko, en) in core.OUTCOMES)
    more = core.link('research', t('논문·학회 발표·특허 보기', 'Publications, reports and patents')
                     + '<svg viewBox="0 0 20 10" aria-hidden="true"><path d="M0 5h18M14 1l4 4-4 4"/></svg>', 'cx-more', 'data-a')
    out = (h.replace('{{inst}}', t(core.INST[0], inst_en)).replace('{{lead}}', lead)
           .replace('{{nums}}', nums).replace('{{more}}', more))
    assert '{{' not in out
    return out


# ================================================================== shared pieces
def h2(lines_ko, lines_en, hid, one_line_desktop=False):
    """Display heading with authored lines (the title of the section, split at word boundaries only).
    Each line rides in a mask of a fixed height, the same in both languages, so KO and EN headings are equally tall."""
    m = lambda ls: ' '.join(f'<span class="m"><span class="l">{x}</span></span>' for x in ls)
    cls = 'c-h2' + (' c-h2--one' if one_line_desktop else '')
    return (f'<h2 class="{cls}" id="{hid}" data-a><span class="c-h2-ko" data-l="ko">{m(lines_ko)}</span>'
            f'<span class="c-h2-en" data-l="en" lang="en">{m(lines_en)}</span></h2>')


def lead(pair):
    return f'<div class="c-leadw" data-a data-lk>{t(pair[0], pair[1], "p", "c-lead")}</div>'


def split_title(pair, ko_at, en_at):
    """Split a (ko, en) title into authored lines at the given word counts, checking that no copy changes."""
    ko, en = pair
    kw, ew = ko.split(' '), en.split(' ')
    lines = ([' '.join(kw[:ko_at]), ' '.join(kw[ko_at:])], [' '.join(ew[:en_at]), ' '.join(ew[en_at:])])
    assert ' '.join(lines[0]) == ko and ' '.join(lines[1]) == en
    return lines


# ================================================================== Research: the publication list
TEAM_KEYS = core.pub_teams(core.PUBS)
YEARS = core.pub_years(core.PUBS)
ITEMS = [dict(i=i, year=d['year'], team=d.get('team', ''), title=d['title'], authors=d['authors'], journal=d['journal'])
         for i, d in enumerate(core.PUBS)]


def pub_row(d):
    tm = core.TEAM_LABEL.get(d['team'], ('', ''))
    return (f'<li class="c-row" data-i="{d["i"]}"><span class="c-yr">{d["year"]}</span><div class="c-tx">'
            f'<p class="c-ti"{lang_attr(d["title"])}>{e(d["title"])}</p>'
            f'<p class="c-au"{lang_attr(d["authors"])}>{e(d["authors"])}</p>'
            f'<p class="c-jn"{lang_attr(d["journal"])}>{e(d["journal"])}</p></div>'
            f'<span class="c-tm">{t(tm[0], tm[1])}</span></li>')


EMPTY = f'<li class="c-row c-row--e">{t(*core.UI["none"])}</li>'


def n_match(team='all', year='all'):
    """How many publications a filter state shows (the engine's rule: '~YYYY' is that year and earlier)."""
    def ok(d):
        if team != 'all' and d['team'] != team:
            return False
        if year == 'all':
            return True
        return int(d['year']) <= int(year[1:]) if year.startswith('~') else str(d['year']) == year
    return sum(1 for d in ITEMS if ok(d))


def filt(key, label, values):
    """One filter group. The pressed button is marked by a 2 px umber bar that slides to it (script), or by a static
    underline when there is no script. Every option carries its count under the other filter (data, no words): a
    combination with nothing in it reads 0 before it is pressed. The script keeps the counts current."""
    btns = ''.join(f'<button type="button" data-k="{key}" data-v="{v}" aria-pressed="{"true" if v == "all" else "false"}">'
                   f'<span class="c-bl">{lab}</span> <span class="c-bc">{n}</span></button>' for v, lab, n in values)
    return (f'<div class="c-f c-f--{key}" role="group" aria-label="{label[0]}" data-aria-en="{label[1]}">'
            f'<p class="c-fl" aria-hidden="true">{t(*label)}</p><div class="c-fb">{btns}<i class="c-ind" aria-hidden="true"></i></div></div>')


def research():
    teams = [('all', t(*core.UI['all']), len(ITEMS))] + [(k, t(*core.TEAM_LABEL[k]), n_match(team=k)) for k in TEAM_KEYS]
    years = [('all', t(*core.UI['all']), len(ITEMS))] + [(y, f'<span class="c-num">{y}</span>', n_match(year=y)) for y in YEARS]
    first = ''.join(pub_row(d) for d in ITEMS[:10])
    pages = -(-len(ITEMS) // 10)
    reel = ''.join(f'<i class="on" style="--d:{i * 2}"></i>' for i in range(len(ITEMS)))
    y_hi, y_lo = ITEMS[0]['year'], ITEMS[-1]['year']
    lines = split_title(core.RESEARCH_TITLE, 1, 2)
    return f"""<section class="c-sec c-res" id="research" aria-labelledby="c-res-h">
<div class="c-in">
{h2(lines[0], lines[1], 'c-res-h')}
{lead(core.RESEARCH_LEAD)}
<div class="c-pubs" data-a data-list>
  <i class="c-ln" aria-hidden="true"></i>
  <div class="c-ctl" data-lk>
    {filt('team', core.UI['team'], teams)}
    {filt('year', core.UI['year'], years)}
    <p class="c-tally"><span data-n>{t(f'<b class="c-cn">{len(ITEMS)}</b>건', f'<b class="c-cn">{len(ITEMS)}</b> items')}</span></p>
    <div class="c-reel" data-ticks aria-hidden="true">{reel}</div>
    <p class="c-reel-y" aria-hidden="true"><span>{y_hi}</span><span>{y_lo}</span></p>
  </div>
  <div class="c-lw"><i class="c-top" aria-hidden="true"></i>
    <ol class="c-list" data-items>{first}</ol>
    <div class="c-pg">
      <button type="button" data-p="-1" aria-label="{core.UI['prev'][0]}" data-aria-en="{core.UI['prev'][1]}" disabled>{ARROW_L}</button>
      <span class="c-pi"><span data-pi>1 / {pages}</span></span>
      <button type="button" data-p="1" aria-label="{core.UI['next'][0]}" data-aria-en="{core.UI['next'][1]}">{ARROW_R}</button>
    </div>
  </div>
</div>
</div>
</section>"""


# ================================================================== People: faculty + HeAD Lab
def member(m):
    ko, en = name_pair(m['name'])
    if m.get('photo'):
        im = img(imgur(m['photo'], 'l'), (ko, en), 640, 800, cls='c-im', attrs='decoding="async"')
        ph = f'<div class="c-pp">{im}</div>'
    else:
        ik, ie = initials(m['name'])
        ph = f'<span class="c-ini" aria-hidden="true">{t(ik, ie) if ik != ie else ik}</span>'
    rk, re_ = member_role(m)
    nm = t(ko, en) if ko != en else f'<span lang="ko">{ko}</span>'
    return (f'<li class="c-mem"><div class="c-ph">{ph}<i class="c-cut" aria-hidden="true"></i></div><div class="c-mt">'
            f'<p class="c-nm">{nm}</p><p class="c-rl">{t(rk, re_)}</p></div></li>')


def team(key, cls):
    tm = core.TEAMS[key]
    _, ko, en = core.TEAM_META[key]
    ko = re.sub(r'(HeAD Lab|Basic Lab|Hearing Lab)', r'<span class="nw">\1</span>', ko)
    return (f'<div class="c-team {cls}" data-a><i class="c-ln" aria-hidden="true"></i>'
            f'<h3 class="c-h3"><span class="c-h3-ko" data-l="ko">{ko}</span><span class="c-h3-en" data-l="en" lang="en">{en}</span></h3>'
            f'<ul class="c-mems" data-lk>{"".join(member(m) for m in tm["members"])}</ul></div>')


def people():
    lines = split_title(core.PEOPLE_TITLE, 2, 2)
    return f"""<section class="c-sec c-ppl" id="people" aria-labelledby="c-ppl-h">
<div class="c-in">
{h2(lines[0], lines[1], 'c-ppl-h', one_line_desktop=True)}
{lead(core.PEOPLE_LEAD)}
{team('faculty', 'c-team--fac')}
{team('head', 'c-team--lab')}
</div>
</section>"""


# ================================================================== CSS
CSS = r"""
/* ---------------------------------------------------------------- tokens (one system: the hero and the reading zones)
   One white sheet: the Wix header, ground and footer measure #ffffff, so does every zone here. Contrast on white:
   ink 19.3, ink-2 8.7, ink-3 5.7, umber 5.9 (text accents), amber 2.1 (never text: only the selection highlight). */
:root {
  --paper: #ffffff;                                   /* the sheet; also the knockout title's white (the paper through the picture) */
  --ink: #0f0e0c; --ink-2: #4e4b47; --ink-3: #696660;
  --ink-r: rgba(15, 14, 12, .12); --ink-r2: rgba(15, 14, 12, .28);   /* row rules / button and record hairlines */
  --tint: #f1f1ef;                                    /* an empty frame before its picture (never seen once it opens) */
  --umber: #8a5a0e; --amber: #e3a640;
  --W: min(100vw, 1640px); --ox: max(0px, calc((100vw - 1640px) / 2)); --m: clamp(28px, 3.75vw, 72px);
  --fx: calc(var(--ox) + var(--W) * .34); --tx: calc(var(--ox) + var(--m)); --gut: clamp(20px, 2.4vw, 40px);
  --ko: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --lat: 'Archivo', 'Helvetica Neue', Arial, sans-serif;
  --dsp: 'Black Han Sans', var(--ko);
  --out: cubic-bezier(.16, 1, .3, 1);
}
@media (max-width: 760px) { :root { --m: 16px; } }
html { background: var(--paper); }
body { margin: 0; background: var(--paper); color: var(--ink); }
::selection { background: var(--amber); color: var(--ink); }
.nw { white-space: nowrap; }

/* ---------------------------------------------------------------- paper: the reading zones */
.c-sec { position: relative; background: var(--paper); color: var(--ink); font-family: var(--ko); padding: clamp(64px, 6.6vw, 112px) 0 clamp(88px, 8.4vw, 140px);
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
.c-sec *, .c-sec *::before, .c-sec *::after { box-sizing: border-box; }
.c-sec [lang="en"] { font-family: var(--lat); }
.c-sec [lang="ko"] { font-family: var(--ko); }
/* the hero's axis: the left column ends one gutter before the frame's left edge (34% of the width) */
.c-in { position: relative; max-width: 1640px; margin: 0 auto; padding: 0 var(--m); display: grid;
  grid-template-columns: calc(var(--W) * .34 - var(--m) - var(--gut)) minmax(0, 1fr); column-gap: var(--gut); }

.c-h2 { grid-column: 1 / -1; margin: 0; font-weight: 400; color: var(--ink); --hs: clamp(50px, 6.3vw, 104px); font-size: var(--hs); }
.c-h2 .m { display: block; height: calc(var(--hs) * 1.04); overflow: hidden; padding: .06em .05em 0; margin: -.06em -.05em 0; }
.c-h2 .l { display: block; white-space: nowrap; line-height: calc(var(--hs) * 1.04); }
.c-h2-ko .l { font-family: var(--dsp); font-size: var(--hs); letter-spacing: -.012em; margin-left: -.045em; }   /* the face's side bearing: the stems sit on the column edge */
.c-h2-en .l { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: calc(var(--hs) * 1.08); text-transform: uppercase; letter-spacing: -.004em;
  word-spacing: .07em; margin-left: -.03em; }   /* the condensed space alone reads OF RIHE as one word; the gap between masks is wider */
/* one line on desktop: the masks set the height (a normal line box would add 37 px under the heading) */
@media (min-width: 761px) { .c-h2--one { line-height: 0; } .c-h2--one .m { display: inline-block; vertical-align: top; } }

.c-leadw { grid-column: 2; margin-top: clamp(24px, 2.6vw, 40px); }
.c-lead { margin: 0; max-width: 35em; font-size: clamp(16.5px, 1.22vw, 18px); line-height: 1.78; color: var(--ink-2); word-break: keep-all; overflow-wrap: break-word; text-wrap: pretty; }
.c-lead[lang="en"] { line-height: 1.62; max-width: 37em; }

/* the cut line: a 1 px ink rule that opens each block (drawn in by the script) */
.c-ln { grid-column: 1 / -1; display: block; height: 1px; background: var(--ink); transform-origin: 0 50%; }

/* ---------------------------------------------------------------- the publication list */
.c-pubs { position: relative; grid-column: 1 / -1; display: grid; grid-template-columns: subgrid; margin-top: clamp(52px, 5.4vw, 88px); }
.c-top { position: absolute; left: 0; top: -150px; width: 1px; height: 1px; pointer-events: none; }
.c-ctl { grid-column: 1; align-self: start; padding-top: 18px; }   /* 18: the first label starts on the first title's line (optical) */
.c-f + .c-f { margin-top: 24px; }
.c-fl { margin: 0 0 4px; font-size: 12px; line-height: 1.4; letter-spacing: .02em; color: var(--ink-3); }
.c-fb { position: relative; display: grid; justify-content: start; justify-items: start; column-gap: 24px; }
.c-f--year .c-fb { grid-template-columns: repeat(4, minmax(0, 1fr)); max-width: 288px; column-gap: 16px; }   /* one pitch for every year */
.c-fb button { appearance: none; -webkit-appearance: none; margin: 0; padding: 8px 0; border: 0; border-radius: 0; background: none; cursor: pointer;
  font: 500 15px/1.3 var(--ko); color: var(--ink-3); text-align: left; white-space: nowrap; transition: color .2s ease; }
.c-fb button [lang="en"] { font-family: var(--lat); font-weight: 500; }
.c-fb .c-num { font-family: var(--lat); font-stretch: 62%; font-weight: 640; font-size: 18px; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; }
.c-fb button:hover, .c-fb button[aria-pressed="true"] { color: var(--ink); }
.c-fb button:focus-visible { outline: 2px solid var(--umber); outline-offset: 2px; }
.c-fb:not(.has-ind) button[aria-pressed="true"] .c-bl { box-shadow: 0 2px 0 var(--umber); }
.c-ind { position: absolute; left: 0; top: 0; width: 0; height: 2px; background: var(--umber); pointer-events: none; }
.c-fb:not(.has-ind) .c-ind { display: none; }
/* an option's count under the other filter, set like an index's superscript; it turns over when the other filter changes */
.c-bc { display: inline-block; vertical-align: top; font: 640 11px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em;
  font-variant-numeric: tabular-nums lining-nums; color: var(--ink-3); }
.c-fb button[aria-pressed="true"] .c-bc { color: var(--ink-2); }
.c-tally { margin: 32px 0 8px; overflow: hidden; font-size: 13.5px; line-height: 1.4; color: var(--ink-2); }
.c-tally [data-n] { display: inline-block; }
/* the result count speaks with the pager's counter numerals */
.c-cn { font: 640 18px/1 var(--lat); font-stretch: 62%; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink); }
/* the reel: one frame per publication, newest first; the filter lights its frames, the page on screen is umber */
.c-reel { display: flex; align-items: flex-end; gap: 1px; height: 30px; }
.c-reel i { flex: 1 1 0; min-width: 0; height: 100%; background: var(--ink); opacity: .13; transform-origin: 50% 100%; transform: scaleY(.42); }
.c-reel i.on { opacity: .6; transform: none; }
.c-reel i.cur { opacity: 1; background: var(--umber); }
.c-reel.live i { transition: opacity .3s ease, transform .45s var(--out), background-color .3s ease; transition-delay: calc(var(--d, 0) * 1ms); }
.c-reel-y { display: flex; justify-content: space-between; margin: 8px 0 0; font: 640 12px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); font-variant-numeric: tabular-nums; }

.c-lw { position: relative; grid-column: 2; min-width: 0; }
.c-list { list-style: none; margin: 0; padding: 0; }
/* year, title and team share the title's first baseline (no nudges); 16 above and below balances the line boxes */
.c-row { display: grid; grid-template-columns: 58px minmax(0, 1fr) 128px; grid-template-areas: "yr tx tm"; align-items: baseline; column-gap: 24px; padding: 16px 0; border-bottom: 1px solid var(--ink-r); }
.c-yr { grid-area: yr; font: 640 18px/1.4 var(--lat); font-stretch: 62%; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink); }
.c-tx { grid-area: tx; min-width: 0; max-width: 680px; }
.c-ti { margin: 0; font-size: 16.5px; line-height: 1.46; font-weight: 500; color: var(--ink); word-break: keep-all; overflow-wrap: anywhere; }
.c-ti[lang="en"] { letter-spacing: -.004em; }
.c-au { margin: 6px 0 0; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); overflow-wrap: anywhere; }
.c-jn { margin: 2px 0 0; font-size: 13.5px; line-height: 1.5; font-weight: 500; color: var(--ink); }
.c-tm { grid-area: tm; font-size: 12px; line-height: 1.45; color: var(--ink-3); text-align: right; white-space: nowrap; }
.c-row--e { display: block; padding: 24px 0 28px; font-size: 18px; line-height: 1.45; font-weight: 500; color: var(--ink); word-break: keep-all; }
.c-row--e [lang="en"] { letter-spacing: -.006em; }
.c-pg { display: flex; align-items: center; gap: 12px; margin-top: 24px; }
.c-pg button { appearance: none; -webkit-appearance: none; width: 44px; height: 44px; margin: 0; padding: 0; display: grid; place-items: center; border: 1px solid var(--ink-r2); border-radius: 0;
  background: transparent; color: var(--ink); cursor: pointer; transition: background-color .2s ease, color .2s ease, border-color .2s ease, transform .12s ease; }
.c-pg svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.6; transition: transform .3s var(--out); }
.c-pg button:hover:not(:disabled) { background: var(--ink); border-color: var(--ink); color: var(--paper); }
.c-pg button[data-p="1"]:hover:not(:disabled) svg { transform: translateX(2px); }
.c-pg button[data-p="-1"]:hover:not(:disabled) svg { transform: translateX(-2px); }
.c-pg button:active:not(:disabled) { transform: scale(.94); }
.c-pg button:disabled { opacity: .3; cursor: default; }
.c-pg button:focus-visible { outline: 2px solid var(--umber); outline-offset: 3px; }
.c-pi { display: inline-block; overflow: hidden; min-width: 4.6em; text-align: center; font: 640 18px/44px var(--lat); font-stretch: 62%; letter-spacing: .02em; font-variant-numeric: tabular-nums lining-nums; }
.c-pi > span { display: inline-block; }

/* ---------------------------------------------------------------- people */
.c-team { grid-column: 1 / -1; display: grid; grid-template-columns: subgrid; margin-top: clamp(56px, 5.8vw, 96px); }
.c-team + .c-team { margin-top: clamp(60px, 6vw, 100px); }
.c-team > .c-ln { margin-bottom: clamp(16px, 1.6vw, 24px); }
.c-h3 { grid-column: 1; margin: 0; font-weight: 400; align-self: start; color: var(--ink); }
.c-h3-ko, .c-h3-en { display: block; }
.c-h3-ko { font: 400 clamp(28px, 2.5vw, 40px)/1.12 var(--dsp); letter-spacing: -.01em; }
.c-h3-en { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: clamp(30px, 2.7vw, 43px); line-height: 1.04; letter-spacing: -.004em; }
/* the grid holds the taller of its two languages (data-lk), the spare stays at its foot */
.c-mems { grid-column: 2; list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); align-content: start; gap: 40px clamp(16px, 1.7vw, 28px); }
/* the lab: each member takes three rows of the grid (portrait, name, role), so a name that wraps keeps every role of its
   row on one line; the row gap becomes the member's bottom padding, and the last row gives it back */
.c-team--lab .c-mems { --rg: 32px; grid-template-columns: repeat(6, minmax(0, 1fr)); column-gap: clamp(12px, 1.2vw, 20px); row-gap: 0; margin-bottom: calc(-1 * var(--rg)); }
.c-team--lab .c-mem { display: grid; grid-row: span 3; grid-template-rows: subgrid; row-gap: 0; padding-bottom: var(--rg); }
.c-team--lab .c-mt { display: grid; grid-row: span 2; grid-template-rows: subgrid; row-gap: 0; }
.c-mem { margin: 0; min-width: 0; }
.c-ph { position: relative; aspect-ratio: 4 / 5; overflow: hidden; }
.c-pp { position: absolute; left: 0; right: 0; top: -5%; height: 110%; background: var(--tint); }
/* a hairline edge, so a portrait shot on a white wall still reads as a frame on the white sheet (hidden while cut open) */
.c-ph::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 0 1px var(--ink-r); pointer-events: none; transition: opacity .6s ease; }
.c-team.is-cut .c-ph::after { opacity: 0; transition: none; }   /* gone at once while cut open; only the return fades */
/* the cut line through a portrait's middle: drawn by the script, the picture opens from it, then it is gone */
.c-cut { position: absolute; left: 0; right: 0; top: 50%; height: 1px; margin-top: -.5px; background: var(--ink); transform: scaleX(0); transform-origin: 0 50%; pointer-events: none; }
.c-im { display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 26%; filter: saturate(.88) contrast(.98);
  transition: filter .7s var(--out), transform .9s var(--out); }
.c-mem:hover .c-im { filter: saturate(1) contrast(1); transform: scale(1.035); }
.c-ini { position: absolute; inset: 0; display: grid; place-items: center; font: 400 clamp(40px, 4vw, 64px)/1 var(--dsp); color: var(--umber); background: var(--tint); }
.c-ini [lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 860; }
.c-mem .c-mt { margin-top: 12px; }
.c-nm { margin: 0; font-size: 18px; line-height: 1.35; font-weight: 500; color: var(--ink); }
.c-nm [lang="en"] { font-weight: 640; letter-spacing: -.006em; }
.c-rl { margin: 4px 0 0; font-size: 13.5px; line-height: 1.46; color: var(--ink-2); word-break: keep-all; }
.c-team--lab .c-nm { font-size: 16.5px; }
.c-team--lab .c-rl { font-size: 12px; }

/* ---------------------------------------------------------------- reveal states: hidden only when motion will run */
html.js:not(.rm) .c-sec [data-a]:not(.on) { opacity: 0; }

/* ---------------------------------------------------------------- tablet widths (Wix shows 980+ and 320; kept sound between) */
@media (max-width: 1199px) {
  .c-row { grid-template-columns: 52px minmax(0, 1fr) 112px; column-gap: 20px; }
  .c-team--lab .c-nm { font-size: 15px; }
}
/* the lab stays one row of six on every desktop width, half the faculty's size (the hierarchy holds at 980); below 900
   (not a Wix width) the left column is too narrow for four years with their counts */
@media (max-width: 899px) {
  .c-team--lab .c-mems { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .c-f--year .c-fb { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

/* ---------------------------------------------------------------- 320 (Wix mobile): one column, the same parts */
@media (max-width: 760px) {
  .c-sec { padding: 56px 0 72px; }
  .c-in { grid-template-columns: minmax(0, 1fr); column-gap: 0; }
  .c-h2, .c-leadw, .c-pubs, .c-team, .c-ln, .c-ctl, .c-lw, .c-h3, .c-mems { grid-column: 1; }
  .c-pubs, .c-team { grid-template-columns: minmax(0, 1fr); }
  .c-h2 { --hs: 34px; }
  .c-h2-en .l { font-size: calc(var(--hs) * 1.06); }
  .c-leadw { margin-top: 16px; }
  .c-lead { font-size: 15px; line-height: 1.72; }
  .c-lead[lang="en"] { font-size: 15px; line-height: 1.58; }
  .c-pubs { margin-top: 40px; }
  .c-ctl { padding-top: 16px; margin-bottom: 24px; }
  .c-fb { column-gap: 16px; }
  .c-f--team .c-fb { grid-template-columns: repeat(2, minmax(0, 1fr)); width: 100%; }
  .c-f--year .c-fb { grid-template-columns: repeat(4, minmax(0, 1fr)); width: 100%; max-width: none; }
  .c-fb button { padding: 12px 0; }
  .c-f + .c-f { margin-top: 16px; }
  .c-tally { margin: 24px 0 8px; }
  .c-reel { height: 24px; }
  .c-row { grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "yr tm" "tx tx"; row-gap: 4px; padding: 16px 0; }
  .c-yr { font-size: 15px; }
  .c-ti { font-size: 15px; line-height: 1.48; }
  .c-au, .c-jn { font-size: 12px; }
  .c-team { margin-top: 48px; }
  .c-team + .c-team { margin-top: 56px; }
  .c-h3 { margin-bottom: 16px; }
  .c-h3-ko { font-size: 26px; }
  .c-h3-en { font-size: 28px; }
  .c-team--fac .c-mems { grid-template-columns: minmax(0, 1fr); gap: 16px; }
  .c-team--fac .c-mem { display: grid; grid-template-columns: 112px minmax(0, 1fr); column-gap: 16px; align-items: end; }
  .c-team--fac .c-mem .c-mt { margin: 0 0 2px; }
  .c-team--lab .c-mems { --rg: 24px; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 8px; }
  .c-team--lab .c-mem .c-mt { margin-top: 8px; }
  .c-team--lab .c-nm { font-size: 15px; }
  .c-team--lab .c-rl { font-size: 12px; line-height: 1.4; }
}

/* reduced motion: nothing moves, not even the hover transitions */
html.rm .c-sec *, html.rm .c-sec *::before, html.rm .c-sec *::after { transition: none !important; }
"""

# ================================================================== JS (runs after the hero's script; GSAP is optional)
JS = r"""
(function () {
  'use strict';
  var R = window.RIHE, doc = document, root = doc.documentElement;
  if (!R) return;
  var g = window.gsap, ST = window.SplitText, CE = window.CustomEase, reduce = !!R.reduce;
  var $$ = function (s, c) { return [].slice.call((c || doc).querySelectorAll(s)); };
  var phone = function () { return !!(window.matchMedia && matchMedia('(max-width: 760px)').matches); };
  // the hero's script has made the projector curves already; make them only if it could not
  if (g && CE && !CE.get('cxGate')) { g.registerPlugin(CE); CE.create('cxGate', 'M0,0 C0.5,0 0.14,1 1,1'); CE.create('cxDraw', 'M0,0 C0.65,0 0.35,1 1,1'); }
  var EGATE = g && CE ? 'cxGate' : 'expo.inOut', EDRAW = g && CE ? 'cxDraw' : 'power2.inOut';

  /* ---------------------------------------------------------------- one height for both languages
     The Wix element has one fixed height for KO and EN. Each [data-lk] block reserves the taller of its two languages
     (both measured in one synchronous pass, never painted), so switching the language never moves anything below it. */
  function lock() {
    var els = $$('[data-lk]');
    els.forEach(function (el) { el.style.minHeight = ''; });
    var cur = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko';
    var a = els.map(function (el) { return el.getBoundingClientRect().height; });
    root.setAttribute('data-lang', cur === 'en' ? 'ko' : 'en');
    var b = els.map(function (el) { return el.getBoundingClientRect().height; });
    root.setAttribute('data-lang', cur);
    els.forEach(function (el, i) { el.style.minHeight = Math.ceil(Math.max(a[i], b[i])) + 'px'; });
  }
  lock();
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(lock);
  var lw = root.clientWidth, lz = 0;
  window.addEventListener('resize', function () { clearTimeout(lz); lz = setTimeout(function () { if (root.clientWidth !== lw) { lw = root.clientWidth; lock(); } }, 180); });

  /* ---------------------------------------------------------------- the publication list (works without GSAP) */
  var box = doc.querySelector('[data-list]');
  var D = JSON.parse(doc.getElementById('c-pubs-data').textContent);
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;'); }
  function la(s) { return /[가-힣]/.test(s) ? ' lang="ko"' : ' lang="en"'; }
  function row(d) {
    var tm = D.teams[d.team] || ['', ''];
    return '<li class="c-row" data-i="' + d.i + '"><span class="c-yr">' + d.year + '</span><div class="c-tx">' +
      '<p class="c-ti"' + la(d.title) + '>' + esc(d.title) + '</p>' +
      '<p class="c-au"' + la(d.authors) + '>' + esc(d.authors) + '</p>' +
      '<p class="c-jn"' + la(d.journal) + '>' + esc(d.journal) + '</p></div>' +
      '<span class="c-tm"><span data-l="ko">' + tm[0] + '</span><span data-l="en" lang="en">' + tm[1] + '</span></span></li>';
  }
  var ticks = box.querySelector('[data-ticks]'), pi = box.querySelector('[data-pi]'), tally = box.querySelector('[data-n]');
  var dir = 1, listShown = false, pressed = null;
  box.addEventListener('click', function (ev) { var p = ev.target.closest && ev.target.closest('button[data-p]'); if (p) { dir = +p.getAttribute('data-p'); pressed = p; } }, true);
  // the engine reserves the tallest page on the list itself; hold that height on the list's wrapper instead, so the pager
  // always follows the rows and a short page (or an empty result) leaves its spare height after the pager, at the end of
  // the section, never as a hole between the rows and the pager. The total height is the same, so nothing below moves.
  var lwrap = box.querySelector('.c-lw'), pgr = box.querySelector('.c-pg');
  function reserve(ul) {
    var mh = parseFloat(ul.style.minHeight) || 0;
    if (!mh || !lwrap || !pgr) return;
    ul.style.minHeight = '';
    lwrap.style.minHeight = Math.ceil(mh + pgr.offsetHeight + (parseFloat(getComputedStyle(pgr).marginTop) || 0)) + 'px';
  }
  // the first or last page disables the button that was pressed: keep the keyboard on the pager (the other button)
  function keepFocus() {
    if (!pressed || !pressed.disabled) return;
    var a = doc.activeElement;
    if (a && a !== doc.body && a !== pressed) return;
    var other = box.querySelector('button[data-p="' + (-dir) + '"]');
    if (other && !other.disabled) { try { other.focus({ preventScroll: true }); } catch (e) {} }
  }
  // the pressed filter: a 2 px umber bar slides under it (continuity: where the selection went)
  function indicators(anim) {
    $$('.c-fb', box).forEach(function (fb) {
      var ind = fb.querySelector('.c-ind'), b = fb.querySelector('button[aria-pressed="true"]');
      if (!ind || !b) return;
      var lab = b.querySelector('.c-bl') || b;
      var x = lab.offsetLeft, y = lab.offsetTop + lab.offsetHeight + 1, w = lab.offsetWidth;
      fb.classList.add('has-ind');
      if (g && anim) g.to(ind, { x: x, y: y, width: w, duration: .5, ease: 'expo.out', overwrite: true });
      else if (g) g.set(ind, { x: x, y: y, width: w });
      else { ind.style.transform = 'translate(' + x + 'px,' + y + 'px)'; ind.style.width = w + 'px'; }
    });
  }
  // a number that changes turns over like the hero's counters
  function turn(el, d) {
    if (!el || !g || reduce) return;
    g.fromTo(el, { yPercent: 85 * d, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: .5, ease: 'expo.out', overwrite: true, clearProps: 'transform,opacity,visibility' });
  }
  // every option carries its count under the other filter (data, no words): a combination with nothing in it reads 0
  // before it is pressed, and the numbers turn over like the hero's counters when the other filter changes
  var opts = $$('button[data-k]', box);
  function hit(d, f) {
    for (var k in f) {
      var v = f[k];
      if (v === 'all') continue;
      if (v.charAt(0) === '~') { if (!(+d[k] <= +v.slice(1))) return false; }
      else if (String(d[k]) !== v) return false;
    }
    return true;
  }
  function counts(anim) {
    var f = {};
    opts.forEach(function (b) { if (b.getAttribute('aria-pressed') === 'true') f[b.getAttribute('data-k')] = b.getAttribute('data-v'); });
    opts.forEach(function (b) {
      var c = b.querySelector('.c-bc'), x = {}, n = 0, y;
      if (!c) return;
      for (y in f) x[y] = f[y];
      x[b.getAttribute('data-k')] = b.getAttribute('data-v');
      D.items.forEach(function (d) { if (hit(d, x)) n++; });
      if (c.textContent !== String(n)) { c.textContent = n; if (anim) turn(c, 1); }
    });
  }
  // the engine writes the count as plain text; give its number the counter numerals again
  function tallyNum() {
    $$('[data-l]', tally).forEach(function (s) { if (!s.querySelector('.c-cn')) s.innerHTML = s.textContent.replace(/^(\d+)/, '<b class="c-cn">$1</b>'); });
  }
  // paging from the pager under the list: bring the list's top back on screen (the outer Wix page scrolls; the anchor sits
  // 150 px above the list so the phone's sticky Wix header does not cover the first row)
  var anchor = box.querySelector('.c-top');
  function toTop() {
    var lw = box.querySelector('.c-lw'), b = R.band, top = R.rect(lw).top;
    var above = b && b.ok ? top < b.top + 40 : lw.getBoundingClientRect().top < 0;
    if (above && anchor && anchor.scrollIntoView) anchor.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }
  function after(ul, reason) {
    if (reason === 'measure') reserve(ul);
    var cur = {};
    [].forEach.call(ul.children, function (li) { var i = li.getAttribute('data-i'); if (i !== null) cur[i] = 1; });
    for (var i = 0; i < ticks.children.length; i++) ticks.children[i].classList.toggle('cur', !!cur[i]);
    tallyNum();
    if (reason !== 'page') counts(reason !== 'measure' && !reduce && listShown);
    indicators(reason !== 'measure' && !reduce);
    if (reason === 'page') { keepFocus(); toTop(); }
    if (reason === 'measure' || reduce || !g || !listShown) return;
    // the next page is a cut, not a crossfade: the rows come up in about 300 ms, top first
    g.fromTo(ul.children, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: .4, stagger: .018, ease: 'expo.out', overwrite: true, clearProps: 'transform,opacity,visibility' });
    if (reason === 'page') turn(pi, dir); else { turn(tally, 1); turn(pi, 1); }
  }
  R.list(box, { data: D.items, size: 10, render: row, empty: D.empty, after: after });
  // the count and the page number speak when the visitor changes them, not while the page loads (the engine redraws on
  // fonts.ready): the live regions are attached after that last redraw
  (doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve()).then(function () {
    setTimeout(function () { [box.querySelector('.c-tally'), box.querySelector('.c-pi')].forEach(function (el) { if (el) el.setAttribute('aria-live', 'polite'); }); }, 0);
  });

  /* ---------------------------------------------------------------- motion (none under reduced motion or without GSAP) */
  if (!g || reduce) { listShown = true; return; }
  var tls = [];
  function keep(tl) { tls.push(tl); return tl; }
  function finishAll() { tls.forEach(function (tl) { try { tl.progress(1); } catch (e) {} }); }
  R.showHooks.push(finishAll);
  R.onLang(finishAll);
  var fontsIn = (doc.fonts && doc.fonts.ready) ? Promise.race([doc.fonts.ready, new Promise(function (r) { setTimeout(r, 1500); })]) : Promise.resolve();
  function safe(fn) { return function (el) { try { fn(el); } catch (err) { if (window.console) console.error(err); R.showAll(); } }; }

  // headings: the authored lines rise through their masks (the hero's title, one step quieter: by line, not by syllable)
  function heading(h) {
    var ls = $$('[data-l="' + R.lang + '"] .l', h);
    g.set(ls, { yPercent: 108 });
    h.classList.add('on');
    keep(g.to(ls, { yPercent: 0, duration: 1.05, stagger: .1, ease: 'expo.out', clearProps: 'transform' }));
  }
  // leads: lines rise into focus (the hero's statement and its rack focus)
  function leadIn(w) {
    fontsIn.then(safe(function () {
      var p = w.querySelector('[data-l="' + R.lang + '"]') || w.firstElementChild;
      var sp = ST ? new ST(p, { type: 'lines', mask: 'lines', linesClass: 'c-ll' }) : null;
      var tg = sp ? sp.lines : [p];
      g.set(tg, sp ? { yPercent: 135, filter: 'blur(6px)' } : { autoAlpha: 0, y: 14, filter: 'blur(6px)' });   // 135%: the halo waits outside the mask
      w.classList.add('on');
      keep(g.to(tg, { yPercent: 0, y: 0, autoAlpha: 1, filter: 'blur(0px)', duration: 1, stagger: .08, ease: 'expo.out',
        onComplete: function () { if (sp) sp.revert(); else g.set(tg, { clearProps: 'all' }); } }));
    }));
  }
  // the list: the slit opens the block, the controls settle, the reel runs through its 120 frames, the first page comes up
  function listIn(el) {
    var ln = el.querySelector('.c-ln'), ctl = el.querySelector('.c-ctl'), rows = $$('.c-row', el), tk = $$('.c-reel i', el), pg = el.querySelector('.c-pg');
    g.set(ln, { scaleX: 0 }); g.set([ctl, pg], { autoAlpha: 0, y: 10 }); g.set(rows, { autoAlpha: 0, y: 12 }); g.set(tk, { scaleY: 0 });
    el.classList.add('on');
    keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: function () {
      g.set([ln, ctl, pg].concat(rows, tk), { clearProps: 'transform,opacity,visibility' });
      ticks.classList.add('live'); listShown = true;
    } })
      .to(ln, { scaleX: 1, duration: .8, ease: EDRAW }, 0)
      .to(ctl, { autoAlpha: 1, y: 0, duration: .7 }, .12)
      .to(tk, { scaleY: function (i) { return tk[i].classList.contains('on') ? 1 : .42; }, duration: .5, stagger: .003 }, .16)
      .to(rows, { autoAlpha: 1, y: 0, duration: .7, stagger: .03 }, .15)
      .to(pg, { autoAlpha: 1, y: 0, duration: .6 }, .45));
  }
  // people: every portrait is cut open like the hero: an ink line through its middle, a beat, the picture opens from it
  // with its rack focus; names follow
  function decoded(ims, cap) {
    return Promise.race([Promise.all(ims.map(function (im) {
      if (!im || !im.decode) return null;
      return im.decode().catch(function () {});
    })), new Promise(function (r) { setTimeout(r, cap); })]);
  }
  function teamIn(el) {
    var ln = el.querySelector('.c-ln'), h3 = el.querySelector('.c-h3'), mems = $$('.c-mem', el);
    var phs = mems.map(function (m) { return m.querySelector('.c-pp, .c-ini'); });
    var cuts = mems.map(function (m) { return m.querySelector('.c-cut'); });
    var ims = mems.map(function (m) { return m.querySelector('.c-im, .c-ini'); });
    var txs = mems.map(function (m) { return m.querySelector('.c-mt'); });
    var all = [ln, h3].concat(phs, cuts, ims, txs), gate = null, over = false;
    var clear = function () { g.set(all, { clearProps: 'transform,opacity,visibility,clipPath,filter' }); el.classList.remove('is-cut'); };
    ims.forEach(function (im) { if (im && im.loading === 'lazy') im.loading = 'eager'; });
    // the block's frame (its rule and the team's name) comes at once; the portraits wait for their pictures (600 ms at most)
    g.set(ln, { scaleX: 0 }); g.set(h3, { autoAlpha: 0, y: 12 }); g.set(txs, { autoAlpha: 0, y: 10 });
    g.set(phs, { clipPath: 'inset(50% 0% 50% 0%)' }); g.set(ims, { scale: 1.08, filter: 'blur(9px)' }); el.classList.add('is-cut');
    el.classList.add('on');
    keep(g.timeline({ defaults: { ease: 'expo.out' } }).to(ln, { scaleX: 1, duration: .8, ease: EDRAW }, 0).to(h3, { autoAlpha: 1, y: 0, duration: .7 }, .1));
    keep({ progress: function () { over = true; if (gate) gate.progress(1); else clear(); } });   // finished early (language switch, show all)
    decoded(ims.filter(function (im) { return im && im.tagName === 'IMG'; }), 600).then(function () {
      if (over) return;
      gate = g.timeline({ defaults: { ease: 'expo.out' }, onComplete: clear })
        .to(cuts, { scaleX: 1, duration: .4, stagger: .08, ease: EDRAW }, 0)
        // explicit four-value strings: read back from the computed style the start is 'inset(50% 0%)', and the bottom edge
        // would snap open at once instead of moving with the top (the picture opens from its line, both ways)
        .fromTo(phs, { clipPath: 'inset(50% 0% 50% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, stagger: .08, ease: EGATE }, .55)
        .to(cuts, { autoAlpha: 0, duration: .3, stagger: .08, ease: 'power1.in' }, .8)
        .to(ims, { scale: 1, filter: 'blur(0px)', duration: 1.4, stagger: .08, ease: 'power2.out' }, .59)
        .to(txs, { autoAlpha: 1, y: 0, duration: .6, stagger: .08 }, .95);
    }, clear);
  }
  $$('.c-h2').forEach(function (h) { R.inview(h, safe(heading), { threshold: .35, px: 60 }); });
  $$('.c-leadw').forEach(function (w) { R.inview(w, leadIn, { threshold: .4, px: 50 }); });
  $$('.c-pubs').forEach(function (el) { R.inview(el, safe(listIn), { threshold: .08, px: 160 }); });
  $$('.c-team').forEach(function (el) { R.inview(el, teamIn, { threshold: .2, px: 180 }); });

  // portraits start loading before they reach the screen (rootMargin is ignored in the Wix iframe: the sentinel band
  // tells how far the visible part of the page is from the People section)
  var pplTop = null, eager = false;
  function bands() {
    R.onBand(function (b) {
      if (eager || !b.ok) return;
      if (pplTop === null) { var s = doc.querySelector('.c-ppl'); pplTop = s ? R.rect(s).top : 0; }
      if (b.bottom > pplTop - 1400) { eager = true; $$('.c-ppl img[loading="lazy"]').forEach(function (im) { im.loading = 'eager'; }); }
    });
    // faculty portraits drift a little against the page (desktop): the camera moves past the people, the frames stay put
    if (phone()) return;
    var pps = $$('.c-team--fac .c-pp').map(function (el) { return { el: el, to: g.quickTo(el, 'yPercent', { duration: .8, ease: 'power3.out' }) }; });
    R.onBand(function (b) {
      if (!b.ok) return;
      pps.forEach(function (o) { var p = R.progress(R.rect(o.el.parentNode)); if (p !== null) o.to((.5 - p) * 7); });
    });
  }
  // start after fonts, the language locks and the list's reserved height have settled (the sentinels tile the document)
  fontsIn.then(function () { requestAnimationFrame(function () { requestAnimationFrame(bands); }); });
})();
"""


# ================================================================== fonts (Korean faces: only the glyphs on the page)
def fonts(body):
    pub_text = ''.join(d['title'] + d['authors'] + d['journal'] for d in core.PUBS)
    ko_text = core.chars_in(body, tags=('section', 'div'), extra=pub_text + core.UI['none'][0] + '건')
    dsp_text = core.chars_in(body, classes=('cx-h-ko', 'c-h2-ko', 'c-h3-ko', 'c-ini'))
    return [core.gfont('Black+Han+Sans', dsp_text),
            'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..100,400..900&display=swap',
            core.gfont('Noto+Sans+KR:wght@400;500', ko_text)]


def render():
    reel = json.loads(rd('reel.json'))
    hero_js = rd('hero.js')
    assert '/*@REEL@*/null' in hero_js
    hero_js = hero_js.replace('/*@REEL@*/null', json.dumps(reel, separators=(',', ':')))
    data = dict(items=ITEMS, teams={k: list(v) for k, v in core.TEAM_LABEL.items()}, empty=EMPTY)
    body = (hero() + '\n' + core.sample_mark('Research 페이지 일부', 'Part of the Research page') + '\n' + research() + '\n'
            + core.sample_mark('People 페이지 일부', 'Part of the People page') + '\n' + people() + '\n'
            + core.json_script(data, 'c-pubs-data'))
    return core.page_shell('C2 · 에디토리얼 시네마틱 · 흰 지면 · RIHE', body, css=CSS + rd('hero.css'), js=hero_js + '\n' + JS,
                           fonts=fonts(body), vendor=('gsap', 'split', 'ease'), prefix='../', robots='noindex', lang_toggle=True,
                           comment='방향 C2 (에디토리얼 시네마틱 · 흰 지면) 시안. 설계: site/_directions/cw.design.md, 영상 데이터: tools/kits/cw/reel.py')
