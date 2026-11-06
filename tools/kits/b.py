#!/usr/bin/env python3
"""Direction B · 클리니컬 모던 (Clinical modern). python3 tools/directions.py b -> site/_directions/b.html

One system, taken from the /67 first screen (tools/kits/b/: hero.html, hero.css, hero.js, fonts.txt, copied unchanged from
site/_directions/_67/b/final/):
  - the grid is the audiogram's frequency axis: six octave columns (125 Hz to 8 kHz) in min(1320px, 100% - 2 x pad), no
    gap at section level, so every block starts on an octave line;
  - white ground, one teal (#0a7671) and greys; Hanken Grotesk for Latin and numerals, Noto Sans KR for Korean
    (600 only as a text= subset for titles and names);
  - one motion: a teal cursor that measures. The hero sweeps the frequency axis; the outcomes band sweeps the years and its
    numbers are the running totals at the cursor; section names rise out of their axis; the list is scanned in.
Design document: site/_directions/b.design.md. Only tools/core.py is shared with other directions.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import core  # noqa: E402
from core import e  # noqa: E402

ASSETS = os.path.join(HERE, 'b')
SIZE = 10                      # publications per page


def _rd(name):
    with open(os.path.join(ASSETS, name), encoding='utf-8') as f:
        return f.read()


# ================================================================== KO/EN helpers
def d(ko, en=None, tag='span', cls='', attrs=''):
    """KO/EN pair stacked in ONE grid cell (.b-d): the box is the larger of the two in both languages, so a language
    switch never changes a wrap or a height (the Wix element height is fixed, and interact.js clicks the KO/EN toggle).
    Same text in both languages: one element, lang="ko" when it is Hangul."""
    a = f' {attrs}' if attrs else ''
    if en is None or en == ko:
        c = f' class="{cls}"' if cls else ''
        lg = ' lang="ko"' if re.search('[가-힣]', ko) else ''
        return f'<{tag}{c}{lg}{a}>{ko}</{tag}>'
    c = 'b-d' + (' ' + cls if cls else '')
    return f'<{tag} class="{c}"{a}><span data-l="ko">{ko}</span><span data-l="en" lang="en">{en}</span></{tag}>'


def dp(pair, tag='span', cls='', attrs=''):
    return d(pair[0], pair[1], tag, cls, attrs)


ARROW_L = '<svg viewBox="0 0 14 10" width="14" height="10" aria-hidden="true" focusable="false"><path d="M13 5H1.5M5.5 1 1.5 5l4 4"/></svg>'
ARROW_R = '<svg viewBox="0 0 14 10" width="14" height="10" aria-hidden="true" focusable="false"><path d="M1 5h11.5M8.5 1l4 4-4 4"/></svg>'


def section_head(hid, pair):
    """A section's name stands on its own axis line, as the institute's name stands on the frequency axis."""
    return (f'<header class="b-sh">{dp(pair, "h2", "b-h2 b-end", f"id={chr(34)}{hid}{chr(34)} data-a")}'
            f'<div class="b-ax" aria-hidden="true"><i class="b-ax-d" data-a></i></div></header>')


# ================================================================== outcomes: the record, by year
def outcomes():
    """core.OUTCOMES as four readouts on the hero's octave lines (cols 3-6). Each readout carries the record behind its
    number: publications and presentations per year (one shared year axis and scale), patents as granted (solid) and
    filed (hollow) units, technology transfers as units. All counts come from data/*.json (transfers: core.TECH_TRANSFERS)."""
    pubs, reps, pats = core.PUBS, core.REPORTS, core.PATENTS
    assert [n for n, _ in core.OUTCOMES] == [len(pubs), len(reps), len(pats), core.TECH_TRANSFERS], 'OUTCOMES order changed'
    y_pub = collections.Counter(p['year'] for p in pubs)
    y_rep = collections.Counter(r['year'] for r in reps)
    y0, y1 = min(min(y_pub), min(y_rep)), max(max(y_pub), max(y_rep))
    years = list(range(y0, y1 + 1))
    vmax = max(max(y_pub.values()), max(y_rep.values()))
    since = int(re.search(r'(\d{4})', core.SINCE[0]).group(1))       # '2015년부터 ...' (director's greeting)

    def chart(cnt):
        n = len(years)
        bars = ''.join(f'<i style="--v:{cnt.get(y, 0) / vmax:.4f}" data-n="{cnt.get(y, 0)}"></i>' for y in years)
        lab = [(y0, 's'), (since, 'k'), (y1, 'e')] if y0 < since < y1 else [(y0, 's'), (y1, 'e')]
        labels = ''.join(f'<span class="b-yl {c}" style="--x:{(years.index(y) + .5) / n:.4f}">{y}</span>' for y, c in lab)
        return (f'<div class="b-yr" data-y0="{y0}" aria-hidden="true"><div class="b-bars">{bars}</div><span class="b-yb"></span>'
                f'{labels}<span class="b-cur"></span><span class="b-rd"></span></div>')

    def units(solid, hollow=0):
        return f'<div class="b-un" aria-hidden="true">{"<i></i>" * solid}{"<i class=o></i>" * hollow}</div>'

    granted = sum(1 for p in pats if p.get('status') == '등록')
    filed = sum(1 for p in pats if p.get('status') == '출원')
    key = (f'<span class="b-key"><i></i><b>{granted}</b>{dp(core.UI["등록"])}</span>'
           f'<span class="b-key"><i class="o"></i><b>{filed}</b>{dp(core.UI["출원"])}</span>')
    viz = [(chart(y_pub), ''), (chart(y_rep), ''), (units(granted, filed), key), (units(core.TECH_TRANSFERS), '')]
    cells = ''.join(
        f'<div class="b-cell" data-ai><dt class="b-cl">{dp(pair, "span", "b-end")}</dt>'
        f'<dd class="b-cn"><span class="b-c" data-count="{n}">{n}</span></dd>'
        f'<dd class="b-cv">{v}</dd><dd class="b-ft">{foot}</dd></div>'
        for (n, pair), (v, foot) in zip(core.OUTCOMES, viz))
    # the year in the sentence takes the teal of the same year on the chart axes (presentation only; the copy is unchanged)
    yr = lambda s: re.sub(r'(\d{4})', r'<span class="b-k">\1</span>', s, count=1)
    return (f'<div class="b-rec" id="b-rec"><div class="b-in b-rec-in">{d(yr(core.SINCE[0]), yr(core.SINCE[1]), "p", "b-rec-lead", "data-a")}'
            f'<dl class="b-rec-g">{cells}</dl></div></div>')


# ================================================================== research: the publication list
def pub_row(p, i):
    tm = core.TEAM_LABEL.get(p.get('team'), ('', ''))
    team = dp(tm, 'span', 'b-pub-tm') if tm[0] else ''
    return (f'<li class="b-pub" data-i="{i}"><p class="b-pub-m"><span class="b-pub-y">{p["year"]}</span>{team}</p>'
            f'<div class="b-pub-b"><p class="b-pub-t"{core.lang_attr(p["title"])}>{e(p["title"])}</p>'
            f'<p class="b-pub-a"{core.lang_attr(p["authors"])}>{e(p["authors"])}</p>'
            f'<p class="b-pub-j"{core.lang_attr(p["journal"])}>{e(p["journal"])}</p></div></li>')


def _year_ok(p, v):
    return p['year'] <= int(v[1:]) if v.startswith('~') else str(p['year']) == v


def opt(k, v, label, n, pressed=False):
    return (f'<button type="button" class="b-opt" data-k="{k}" data-v="{v}" aria-pressed="{"true" if pressed else "false"}">'
            f'<span class="b-opt-l">{label}</span><span class="b-opt-n">{n}</span></button>')


def pager(cls, pages):
    return (f'<div class="b-pg {cls}"><button type="button" class="b-pb" data-p="-1" aria-label="{core.UI["prev"][0]}" '
            f'data-aria-en="{core.UI["prev"][1]}" disabled>{ARROW_L}</button><span class="b-pi" data-pi>1 / {pages}</span>'
            f'<button type="button" class="b-pb" data-p="1" aria-label="{core.UI["next"][0]}" data-aria-en="{core.UI["next"][1]}"'
            f'{" disabled" if pages < 2 else ""}>{ARROW_R}</button></div>')


def research():
    items = core.PUBS
    teams, years = core.pub_teams(items), core.pub_years(items)
    pages = max(1, -(-len(items) // SIZE))
    rows = [pub_row(p, i) for i, p in enumerate(items)]
    empty = f'<li class="b-pub-x">{dp(core.UI["none"], "p")}</li>'
    data = {'items': [{'year': p['year'], 'team': p.get('team', ''), 'h': rows[i]} for i, p in enumerate(items)], 'empty': empty}

    t_opts = opt('team', 'all', dp(core.UI['all']), len(items), True) + ''.join(
        opt('team', k, dp(core.TEAM_LABEL[k]), sum(1 for p in items if p.get('team') == k)) for k in teams)
    y_opts = opt('year', 'all', dp(core.UI['all']), len(items), True) + ''.join(
        opt('year', v, v, sum(1 for p in items if _year_ok(p, v))) for v in years)
    filters = (f'<div class="b-fls" data-a>'
               f'<div class="b-flt" role="group" aria-labelledby="b-f-team">{dp(core.UI["team"], "p", "b-fl", "id=b-f-team")}'
               f'<div class="b-opts">{t_opts}</div></div>'
               f'<div class="b-flt b-flt-y" role="group" aria-labelledby="b-f-year">{dp(core.UI["year"], "p", "b-fl", "id=b-f-year")}'
               f'<div class="b-opts">{y_opts}</div></div></div>')

    # the record map: one mark per publication, in list order (newest first). The list engine lights the filtered marks
    # ([data-ticks] children get .on); the page's ten stand taller (.cur, set by the kit).
    ticks = ''.join('<i class="on cur"></i>' if i < SIZE else '<i class="on"></i>' for i in range(len(items)))
    first = {}
    for i, p in enumerate(items):
        first.setdefault(p['year'], i)
    top = max(first)
    # a label near the right end hangs to the left of its boundary tick, so it never leaves the column
    marks = ''.join(f'<span{" class=r" if first[y] / len(items) > .8 else ""} style="--x:{first[y] / len(items):.4f}">{y}</span>'
                    for y in range(top - top % 5, min(first), -5) if y in first and first[y] / len(items) <= .92)
    n0 = len(items)
    head = (f'<div class="b-mh" data-a><div class="b-tb"><p class="b-n" data-n aria-live="polite"><span data-l="ko">{n0}건</span>'
            f'<span data-l="en" lang="en">{n0} items</span></p>{pager("b-pg-t", pages)}</div>'
            f'<div class="b-map" aria-hidden="true"><div class="b-tk" data-ticks>{ticks}</div><div class="b-my">{marks}</div></div></div>')
    lst = f'<ul class="b-pubs" data-items data-a>{"".join(rows[:SIZE])}</ul>'
    return (f'<section class="b-sec b-res" id="research" aria-labelledby="b-res-h"><div class="b-in">'
            f'{section_head("b-res-h", core.RESEARCH_TITLE)}'
            f'<div class="b-sb b-grid" id="b-pubs"><div class="b-side">{dp(core.RESEARCH_LEAD, "p", "b-lead", "data-a")}{filters}</div>'
            f'<div class="b-main">{head}<div class="b-lw">{lst}<div class="b-foot" data-a>{pager("b-pg-b", pages)}</div></div></div></div>'
            f'</div>{core.json_script(data, "b-pubs-data")}</section>')


# ================================================================== people
# Art direction only (no data): where the face sits in a 4:5 frame, and a crop for the two full-length snapshots.
FOCUS = {'vIAp69Y': ('36% 30%', '36% 30%', 1.0), 'yCSCJNd': ('57% 45%', '57% 64%', 2.0), 'F9YowOS': ('51% 40%', '51% 46%', 1.5)}


def photo(src):
    pid = os.path.splitext(os.path.basename(src))[0]
    pos, org, z = FOCUS.get(pid, ('50% 26%', '50% 26%', 1.0))
    style = f'object-position:{pos};--o:{org}' + (f';--z:{z}' if z > 1 else '')
    if z > 1:       # a tight crop of a full-length snapshot needs the original pixels
        return f'<img src="{src}" alt="" width="480" height="600" loading="lazy" decoding="async" style="{style}">'
    return (f'<img src="{core.imgur(src, "l")}" srcset="{core.imgur(src, "m")} 240w, {core.imgur(src, "l")} 480w" '
            f'sizes="(max-width: 760px) 92px, (max-width: 1320px) 15vw, 200px" alt="" width="480" height="600" '
            f'loading="lazy" decoding="async" style="{style}">')


def member(m):
    ko, en = core.name_pair(m['name'])
    if m.get('photo'):
        inner = photo(m['photo'])
    else:
        ik, ie = core.initials(m['name'])
        inner = f'<span class="b-ini">{d(ik, ie)}</span>'
    rko, ren = core.member_role(m)
    lg = lambda s: ' lang="ko"' if re.search('[가-힣]', s) else ''
    if (ko, rko) == (en, ren):
        text = f'<div class="b-pp-t" data-ai><p class="b-pp-n"{lg(ko)}>{ko}</p><p class="b-pp-r"{lg(rko)}>{rko}</p></div>'
    else:           # name and role stacked per language: the block, not each line, takes the larger of the two
        text = (f'<div class="b-pp-t b-d" data-ai><div data-l="ko"><p class="b-pp-n">{ko}</p><p class="b-pp-r">{rko}</p></div>'
                f'<div data-l="en" lang="en"><p class="b-pp-n"{lg(en)}>{en}</p><p class="b-pp-r">{ren}</p></div></div>')
    return f'<li class="b-pp"><div class="b-pp-f" data-ai><div class="b-pp-d">{inner}</div></div>{text}</li>'


def group(key, cls):
    _, ko, en = core.TEAM_META[key]
    ms = core.TEAMS[key]['members']
    return (f'<div class="b-grp {cls}"><div class="b-gh">{d(ko, en, "h3", "b-h3")}<span class="b-gn">{len(ms)}</span></div>'
            f'<ul class="b-pp-g" data-a>{"".join(member(m) for m in ms)}</ul></div>')


def people():
    return (f'<section class="b-sec b-ppl" id="people" aria-labelledby="b-ppl-h"><div class="b-in">'
            f'{section_head("b-ppl-h", core.PEOPLE_TITLE)}'
            f'<div class="b-sb b-grid">{dp(core.PEOPLE_LEAD, "p", "b-lead", "data-a")}</div>'
            f'{group("faculty", "b-fac")}{group("head", "b-lab")}</div></section>')


# ================================================================== page CSS (the hero keeps its own .fp CSS)
CSS = r"""
/* ======== B · the page after the first screen. Same tokens, type and octave grid as the hero (.fp) ======== */
.b {
  --paper: #ffffff;
  --ink: #0c1e21;
  --ink-2: #33474b;
  --mute: #5a6d71;
  --mute-2: #7d8f92;
  --rule: #d2dddd;
  --rule-2: #e3eaea;
  --teal: #0a7671;
  --teal-2: #065a56;
  --tint: #edf3f2;
  --wash: #f5f8f8;
  --lat: "Hanken Grotesk", "Noto Sans KR", system-ui, -apple-system, "Segoe UI", sans-serif;
  --kor: "Noto Sans KR", "Hanken Grotesk", system-ui, -apple-system, sans-serif;
  --ease: cubic-bezier(.2, .8, .2, 1);

  --pad: clamp(16px, 4.4vw, 64px);
  --wmax: 1320px;
  --gut: clamp(22px, 2.5vw, 36px);
  --gap1: clamp(16px, 1.8vw, 26px);
  --gap2: clamp(32px, 3.3vw, 48px);
  --sec: clamp(72px, 7.4vw, 112px);
  --h2: clamp(30px, 3.1vw, 44px);
  --h3: clamp(15px, 1.25vw, 18px);
  --lead: clamp(15px, 1.24vw, 18px);
  --dt: clamp(12.5px, 1.04vw, 14.5px);
  --num: clamp(40px, 4.1vw, 60px);
  --body: clamp(15px, 1.18vw, 17px);
  --small: clamp(13px, 1vw, 14px);
  --micro: 12px;

  background: var(--paper);
  color: var(--ink);
  font-family: var(--lat);
  font-kerning: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.b *, .b *::before, .b *::after { box-sizing: border-box; }
.b ::selection { background: #cfe5e2; color: var(--ink); }
.b [data-l="ko"], .b [lang="ko"] { font-family: var(--kor); }
.b-in { width: min(var(--wmax), 100% - 2 * var(--pad)); margin: 0 auto; }
.b-grid { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); }

/* KO/EN in one cell: the box takes the larger of the two in both languages */
.b-d { display: grid; }
.b-d > [data-l] { grid-area: 1 / 1; min-width: 0; }
.b-end > [data-l] { align-self: end; }
[data-lang] .b-d > [data-l] { display: block !important; }
[data-lang="ko"] .b-d > [data-l="en"], [data-lang="en"] .b-d > [data-l="ko"] { visibility: hidden; }

/* ---------- outcomes: four readouts on the hero's octave lines ---------- */
.b-rec-in {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  border-top: 1px solid var(--rule-2);
  padding: clamp(30px, 3.2vw, 46px) 0 clamp(56px, 5.6vw, 84px);
}
.b-rec-lead {
  grid-column: 1 / 3;
  margin: 0;
  padding-right: var(--gut);
  font-size: var(--lead);
  line-height: 1.6;
  color: var(--ink-2);
  text-wrap: pretty;
}
.b-rec-lead [data-l="ko"] { word-break: keep-all; line-height: 1.7; }
.b-k { color: var(--teal); font-weight: 500; font-variant-numeric: tabular-nums; }
.b-rec-g {
  grid-column: 3 / 7;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.b-cell {
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-left: 1px solid var(--rule-2);
  padding-left: clamp(14px, 1.5vw, 22px);
}
.b-cl {
  display: flex;
  align-items: flex-end;
  min-height: 2.7em;                     /* two lines kept for every label: the numbers sit on one line across the band */
  margin: 0;
  font-size: var(--dt);
  line-height: 1.35;
  font-weight: 500;
  color: var(--mute);
}
.b-cl [data-l="ko"] { word-break: keep-all; }
.b-cn {
  margin: clamp(6px, .7vw, 10px) 0 0;
  font-size: var(--num);
  line-height: 1;
  font-weight: 400;
  letter-spacing: -0.035em;
  color: var(--ink);
  font-variant-numeric: tabular-nums lining-nums;
}
.b-cv { position: relative; margin: clamp(18px, 1.9vw, 26px) 0 0; height: 44px; }
.b-ft {
  margin: 0;
  min-height: 34px;
  padding-top: 9px;
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  column-gap: 12px;
  row-gap: 5px;
  font-size: var(--micro);
  line-height: 1;
  color: var(--mute);
  font-variant-numeric: tabular-nums;
}
/* year bars: one per year on a shared axis and scale (publications 2008-2026, presentations on the same years) */
.b-yr { position: absolute; inset: 0; }
.b-bars { position: absolute; inset: 0; display: flex; align-items: flex-end; gap: 2px; }
.b-bars i { flex: 1 1 0; height: calc(var(--v) * 100%); background: var(--teal); transform-origin: 50% 100%; transition: background-color .15s ease; }
.b-bars i.hi { background: var(--teal-2); }
.b-yb { position: absolute; left: 0; right: 0; bottom: 0; height: 1px; background: var(--rule); }
@media (hover: hover) and (pointer: fine) { .b-yr { cursor: crosshair; } }     /* the chart can be read with the pointer */
.b-yl {
  position: absolute;
  top: calc(100% + 9px);
  left: calc(var(--x) * 100%);
  transform: translateX(-50%);
  font-size: var(--micro);
  line-height: 1;
  font-weight: 500;
  letter-spacing: .02em;
  color: var(--mute);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.b-yl.s { left: 0; transform: none; }
.b-yl.e { left: auto; right: 0; transform: none; }
.b-yl.k { color: var(--teal); }
/* the cursor and its readout (the hero's, on the time axis): the sweep, then the pointer */
.b-cur { position: absolute; left: 0; top: -7px; bottom: 0; width: 1px; background: var(--teal); opacity: 0; pointer-events: none; transform-origin: 50% 100%; }
.b-rd {
  position: absolute;
  left: 0;
  top: calc(100% + 9px);
  padding: 0 5px;
  background: var(--paper);
  color: var(--teal);
  font-size: var(--micro);
  line-height: 1;
  font-weight: 600;
  letter-spacing: .02em;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  opacity: 0;
  pointer-events: none;
  z-index: 2;
}
/* units: one square per patent (solid granted, hollow filed) or per transfer */
.b-un {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(20, minmax(0, 1fr));
  gap: 2px;
  align-content: end;
}
.b-un i { aspect-ratio: 1; background: var(--teal); }
.b-un i.o { background: transparent; box-shadow: inset 0 0 0 1px var(--teal); }
.b-un i.off { background: var(--rule-2); box-shadow: none; }
.b-key { display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; }
.b-key i { flex: none; width: 7px; height: 7px; background: var(--teal); }
.b-key i.o { background: transparent; box-shadow: inset 0 0 0 1px var(--teal); }
.b-key b { font-weight: 500; color: var(--ink-2); margin-right: 1px; }

/* ---------- sections: a name on its axis, then the body on the octave grid ---------- */
.b-sec { padding: var(--sec) 0; }
.b-h2 {
  margin: 0;
  font-size: var(--h2);
  line-height: 1.16;
  font-weight: 600;
  letter-spacing: -0.022em;
  color: var(--ink);
}
.b-h2 [data-l="ko"] { letter-spacing: -0.032em; word-break: keep-all; }
.b-ax { position: relative; height: 1px; margin-top: var(--gap1); background: var(--rule); }
.b-ax-d { position: absolute; inset: 0; background: var(--teal); transform-origin: 0 50%; }
.b-sb { margin-top: var(--gap2); }
.b-side { grid-column: 1 / 3; padding-right: var(--gut); }
.b-main { grid-column: 3 / 7; min-width: 0; }
.b-lead {
  margin: 0;
  font-size: var(--lead);
  line-height: 1.66;
  color: var(--ink-2);
  text-wrap: pretty;
}
.b-lead [data-l="ko"] { line-height: 1.76; word-break: keep-all; }

/* ---------- research: filters | the record map and the list ---------- */
.b-fls { margin-top: clamp(28px, 2.8vw, 40px); }
.b-flt + .b-flt { margin-top: 26px; }
.b-fl {
  margin: 0 0 9px;
  font-size: var(--micro);
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--mute);
}
.b-opts { display: flex; flex-direction: column; border-top: 1px solid var(--rule-2); }
.b-opt {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  min-height: 38px;
  margin: 0;
  padding: 8px 10px 8px 14px;
  border: 0;
  border-bottom: 1px solid var(--rule-2);
  border-radius: 0;
  background: none;
  font: 500 14px/1.3 var(--lat);
  color: var(--ink-2);
  text-align: left;
  cursor: pointer;
  transition: background-color .15s ease, color .15s ease;
}
.b-opt::before {
  content: "";
  position: absolute;
  left: 0;
  top: 9px;
  bottom: 9px;
  width: 2px;
  background: var(--teal);
  transform: scaleY(0);
  transition: transform .25s var(--ease);
}
.b-opt-l { min-width: 0; }
.b-opt-n { flex: none; min-width: 3ch; text-align: right; font-size: var(--micro); color: var(--mute); font-variant-numeric: tabular-nums; transition: color .15s ease; }
.b-opt:hover { background: var(--wash); color: var(--ink); }
.b-opt:active { background: #e6efee; transition-duration: .06s; }
.b-opt[aria-pressed="true"] { color: var(--ink); background: var(--tint); }
.b-opt[aria-pressed="true"]::before { transform: scaleY(1); }
.b-opt[aria-pressed="true"] .b-opt-n { color: var(--teal); }
.b-opt.zero { color: var(--mute); }
.b-opt:focus-visible { outline: 2px solid var(--teal); outline-offset: -2px; }

.b-tb { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 38px; scroll-margin-top: 24px; }
.b-n { margin: 0; font-size: var(--small); font-weight: 500; color: var(--ink-2); white-space: nowrap; font-variant-numeric: tabular-nums; }
.b-pg { display: flex; align-items: center; gap: 2px; }
.b-pb {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  padding: 0;
  border: 1px solid var(--rule);
  border-radius: 2px;
  background: var(--paper);
  color: var(--ink);
  cursor: pointer;
  transition: border-color .15s ease, color .15s ease, background-color .15s ease;
}
.b-pb svg { display: block; fill: none; stroke: currentColor; stroke-width: 1.5; transition: transform .35s var(--ease); }
.b-pb:hover:not(:disabled) { border-color: var(--teal); color: var(--teal-2); }
.b-pb[data-p="1"]:hover:not(:disabled) svg { transform: translateX(2px); }
.b-pb[data-p="-1"]:hover:not(:disabled) svg { transform: translateX(-2px); }
.b-pb:active:not(:disabled) { background: var(--tint); transition-duration: .06s; }
.b-pb:disabled { color: var(--mute-2); border-color: var(--rule-2); cursor: default; }
.b-pb:focus-visible { outline: 2px solid var(--teal); outline-offset: 2px; }
.b-pi { min-width: 66px; text-align: center; font-size: var(--small); color: var(--ink-2); white-space: nowrap; font-variant-numeric: tabular-nums; }

.b-map { margin-top: 16px; }
.b-tk { display: flex; align-items: flex-end; height: 16px; }
.b-tk i { position: relative; flex: 1 1 0; height: 100%; transform-origin: 50% 100%; }
.b-tk i::before {
  content: "";
  position: absolute;
  left: calc(50% - .5px);
  bottom: 0;
  width: 1px;
  height: 8px;
  background: var(--rule);
  transform-origin: 50% 100%;
  transition: background-color .2s ease, transform .25s var(--ease);
}
.b-tk i.on::before { background: var(--teal); }
.b-tk i.cur::before { transform: scaleY(2); background: var(--teal-2); }
.b-my { position: relative; height: 15px; margin-top: 4px; border-top: 1px solid var(--rule-2); }
.b-my span {
  position: absolute;
  top: -1px;
  left: calc(var(--x) * 100%);
  padding: 4px 0 0 5px;
  border-left: 1px solid var(--rule);
  font-size: 11px;
  line-height: 1;
  font-weight: 500;
  letter-spacing: .02em;
  color: var(--mute);
  font-variant-numeric: tabular-nums;
}

.b-my span.r { transform: translateX(-100%); padding: 4px 5px 0 0; border-left: 0; border-right: 1px solid var(--rule); }
.b-pubs { list-style: none; margin: 14px 0 0; padding: 0; border-top: 1px solid var(--rule); }
.b-pub {
  display: grid;
  grid-template-columns: clamp(92px, 8.6vw, 128px) minmax(0, 1fr);
  padding: 17px 0 18px;
  border-bottom: 1px solid var(--rule-2);
}
.b-pub-m { margin: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 3px; padding-right: 12px; }
.b-pub-y { font-size: var(--body); line-height: 1.45; font-weight: 500; color: var(--ink); font-variant-numeric: tabular-nums; }
.b-pub-tm { font-size: 12.5px; line-height: 1.35; color: var(--mute); }
.b-pub-b { min-width: 0; }
.b-pub-t { margin: 0; font-size: var(--body); line-height: 1.45; font-weight: 500; color: var(--ink); text-wrap: pretty; overflow-wrap: anywhere; }
.b-pub-t[lang="ko"] { word-break: keep-all; }
.b-pub-a { margin: 6px 0 0; font-size: var(--small); line-height: 1.5; color: var(--mute); overflow-wrap: anywhere; }
.b-pub-j { margin: 1px 0 0; font-size: var(--small); line-height: 1.5; font-weight: 500; color: var(--ink-2); }
.b-pub-x { padding: 32px 0; font-size: var(--body); color: var(--mute); }
.b-pub-x p { margin: 0; }
.b-foot { display: flex; justify-content: flex-end; margin-top: 18px; }
.b-lw { display: flex; flex-direction: column; }

/* ---------- people: portraits on the octave columns ---------- */
.b-ppl .b-lead { grid-column: 1 / 4; padding-right: var(--gut); }
.b-grp { margin-top: clamp(44px, 4.6vw, 68px); }
.b-gh { display: flex; align-items: baseline; gap: 10px; padding-bottom: 12px; border-bottom: 1px solid var(--rule-2); }
.b-h3 { margin: 0; font-size: var(--h3); line-height: 1.3; font-weight: 600; color: var(--ink); }
.b-gn { font-size: var(--micro); line-height: 1; font-weight: 500; color: var(--mute); font-variant-numeric: tabular-nums; }
.b-pp-g {
  list-style: none;
  margin: clamp(20px, 2vw, 28px) 0 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  column-gap: var(--gut);
  row-gap: 32px;
}
.b-pp { min-width: 0; }
.b-fac .b-pp { grid-column: span 2; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: var(--gut); }
.b-pp-f { position: relative; aspect-ratio: 4 / 5; overflow: hidden; border-radius: 2px; background: var(--tint); isolation: isolate; }
.b-pp-f::after { content: ""; position: absolute; inset: 0; border-radius: inherit; box-shadow: inset 0 0 0 1px rgba(12, 30, 33, .06); pointer-events: none; }
.b-pp-d { position: absolute; left: 0; right: 0; top: -3%; bottom: -3%; }   /* 6 % taller than the frame: room for the depth drift */
.b-pp-d img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transform: scale(var(--z, 1));
  transform-origin: var(--o, 50% 30%);
  filter: saturate(.8) contrast(1.03);
}
.b-ini { position: absolute; inset: 0; display: grid; place-items: center; font: 600 clamp(28px, 3vw, 44px)/1 var(--kor); color: var(--teal-2); background: var(--tint); }
.b-pp-t { padding-top: 12px; min-width: 0; }
.b-fac .b-pp-t { align-self: end; padding: 0 0 2px; }
.b-fac .b-pp-t > [data-l] { align-self: end; }
.b-pp-n { margin: 0; font-size: var(--h3); line-height: 1.3; font-weight: 600; color: var(--ink); }
.b-fac .b-pp-n { font-size: clamp(17px, 1.5vw, 21px); }
.b-pp-r { margin: 4px 0 0; font-size: var(--small); line-height: 1.45; color: var(--mute); }
.b-pp-r [data-l="ko"] { word-break: keep-all; }

/* ---------- runtime housekeeping (kit side) ----------
   core builds its sentinel box (#rihe-band) once, at the document's height before the web fonts arrive, and only rebuilds
   it when the document grows. Clipped to the body, it can never hold the document taller than its content (otherwise the
   fixed-height Wix element would get an inner scroll of ~50 px). The scaffolding sample marks get one height in both
   languages (their Korean glyphs fall back to a taller CJK face inside the mono stack). */
body { position: relative; }
#rihe-band { max-height: 100%; overflow: hidden; }
.b .rihe-sample { box-sizing: border-box; height: 60px; }

/* ---------- reveal states: hidden only while the script can show them ---------- */
html.js:not(.rm) .b [data-a]:not(.on),
html.js:not(.rm) .b [data-ai]:not(.on) { opacity: 0; }
html.rm .b *, html.rm .b *::before, html.rm .b *::after { transition: none !important; animation: none !important; }

/* narrower desktop */
@media (max-width: 1180px) and (min-width: 761px) {
  .b-pub { grid-template-columns: 88px minmax(0, 1fr); }
}

/* ---------- phone: Wix shows this file at 320 px ---------- */
@media (max-width: 760px) {
  .b {
    --pad: 16px;
    --gut: 12px;
    --gap1: 12px;
    --gap2: 22px;
    --sec: 52px;
    --h2: 24px;
    --h3: 15px;
    --lead: 14px;
    --dt: 11px;
    --num: 32px;
    --body: 14.5px;
    --small: 12px;
    --micro: 11px;
  }
  .b-rec-in { padding: 24px 0 44px; }
  .b-rec-lead, .b-rec-g, .b-side, .b-main, .b-ppl .b-lead { grid-column: 1 / -1; padding-right: 0; }
  .b-rec-g { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 20px; border-top: 1px solid var(--rule-2); }
  .b-cell { border-left: 0; padding: 12px 12px 0 0; }
  .b-cell:nth-child(even) { border-left: 1px solid var(--rule-2); padding-left: 12px; padding-right: 0; }
  .b-cell:nth-child(n+3) { border-top: 1px solid var(--rule-2); }
  .b-cn { margin-top: 4px; letter-spacing: -0.03em; }
  .b-cv { margin-top: 14px; height: 34px; }
  .b-ft { min-height: 30px; padding-top: 7px; column-gap: 8px; row-gap: 4px; }
  .b-bars { gap: 1px; }
  .b-yl, .b-rd { top: calc(100% + 7px); }
  .b-un { gap: 1.5px; }
  .b-key i { width: 6px; height: 6px; }

  .b-h2 { line-height: 1.22; }
  .b-fls { margin-top: 22px; }
  .b-flt + .b-flt { margin-top: 16px; }
  .b-fl { margin-bottom: 7px; }
  .b-opts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px; border-top: 0; }
  .b-flt-y .b-opts { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .b-opt:first-child { grid-column: 1 / -1; }
  .b-opt { min-height: 34px; padding: 6px 8px 6px 10px; border: 1px solid var(--rule); border-radius: 2px; font-size: 12.5px; gap: 6px; }
  .b-opt::before { top: 7px; bottom: 7px; }
  .b-main { margin-top: 26px; }
  .b-tb { scroll-margin-top: 156px; }       /* clear of the Wix sticky header (140 px) on phones */
  .b-pb { width: 40px; height: 40px; }
  .b-pi { min-width: 54px; }
  .b-map { margin-top: 12px; }
  .b-tk { height: 14px; }
  .b-tk i::before { height: 7px; }
  .b-pub { grid-template-columns: minmax(0, 1fr); padding: 14px 0 15px; }
  .b-pub-m { flex-direction: row; align-items: baseline; gap: 8px; padding: 0 0 4px; }
  .b-pub-y { font-size: 13px; }
  .b-pub-tm { font-size: 11.5px; }
  .b-pub-t { line-height: 1.42; }
  .b-pub-a { margin-top: 5px; }
  .b-foot { margin-top: 14px; }

  .b-grp { margin-top: 38px; }
  .b-gh { padding-bottom: 10px; }
  .b-pp-g { grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 10px; row-gap: 18px; margin-top: 16px; }
  .b-fac .b-pp-g { grid-template-columns: minmax(0, 1fr); row-gap: 12px; }
  .b-fac .b-pp { grid-column: auto; grid-template-columns: 92px minmax(0, 1fr); column-gap: 14px; }
  .b-fac .b-pp-t, .b-fac .b-pp-t > [data-l] { align-self: center; }
  .b-pp-t { padding-top: 8px; }
  .b-pp-n { font-size: 13.5px; }
  .b-fac .b-pp-n { font-size: 16px; }
  .b-pp-r { margin-top: 2px; font-size: 11px; line-height: 1.4; }
  .b-fac .b-pp-r { font-size: 12px; }
}
"""

# ================================================================== page motion (runs after hero.js, same DOMContentLoaded try block)
JS = r"""
/* B · clinical modern · the page after the first screen.
   One motion language with the hero: a teal cursor that measures. The outcomes band repeats the hero's sweep on the time
   axis (2008 to 2026) and its numbers are the running totals at the cursor; section names rise out of their axis line;
   the publication list is scanned in behind a soft edge and its record map shows where the page sits among all papers;
   portraits open from their baseline like the hero's window. Scroll position comes only from RIHE.onBand (the visible
   band of this document inside the non-scrolling Wix iframe); reveals from RIHE.inview (thresholds only). */
(function () {
  'use strict';
  var R = window.RIHE, doc = document;
  var root = doc.querySelector('.b');
  if (!R || !root) return;
  R.motionReady();

  var G = window.gsap;
  var mq = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
  var mobile = mq('(max-width: 760px)');
  var fine = mq('(hover: hover) and (pointer: fine)');
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || doc).querySelectorAll(s)); };
  var on = function (els) { [].concat(els).forEach(function (el) { if (el) el.classList.add('on'); }); };
  var masked = [];

  // a soft-edged scan from left to right (the hero's text scan): node.style.mask follows p.x, cleared at the end
  function maskAt(node, x, soft) {
    var m = x === null ? '' : 'linear-gradient(90deg, #000 ' + (x - soft).toFixed(1) + 'px, rgba(0,0,0,0) ' + x.toFixed(1) + 'px)';
    node.style.webkitMaskImage = m; node.style.maskImage = m;
  }
  function scanTween(node, dur, ease, soft) {
    soft = soft || 80;
    var w = Math.max(1, node.getBoundingClientRect().width), p = { x: 0 };
    if (node._scan) node._scan.kill();
    if (masked.indexOf(node) < 0) masked.push(node);
    maskAt(node, 0, soft);
    node._scan = window.gsap.to(p, { x: 1, duration: dur, ease: ease || 'power2.out',
      onUpdate: function () { maskAt(node, p.x * (w + soft), soft); },
      onComplete: function () { maskAt(node, null); node._scan = null; } });
    return node._scan;
  }

  /* ---------- the publication list: works with or without motion ---------- */
  pubs();
  function pubs() {
    var el = doc.getElementById('b-pubs'), src = doc.getElementById('b-pubs-data');
    if (!el || !src || !R.list) return;
    var data;
    try { data = JSON.parse(src.textContent); } catch (err) { return; }
    var ticks = $$('[data-ticks] > i', el), head = $('.b-tb', el), bottom = $('.b-pg-b', el);
    var lw = $('.b-lw', el), foot = $('.b-foot', el), fromBottom = false, headSeen = true;
    // the engine reserves the tallest page on the list itself; the reserve moves to the wrapper, so the foot pager follows
    // the last row (no gap above it) while the block, and the page, keep one height
    function hold(ul) {
      var mh = parseFloat(ul.style.minHeight);
      if (!mh || !lw || !foot) return;
      lw.style.minHeight = Math.ceil(mh + foot.offsetHeight + (parseFloat(getComputedStyle(foot).marginTop) || 0)) + 'px';
      ul.style.minHeight = '';
    }
    el.addEventListener('click', function (ev) {      // capture: runs before the list engine's own click handler
      var b = ev.target.closest && ev.target.closest('button[data-p]');
      fromBottom = !!(b && bottom && bottom.contains(b));
    }, true);
    if (head) R.visible(head, function (v) { headSeen = v; });
    function ok(it, k, v) {
      if (v === 'all') return true;
      if (v.charAt(0) === '~') return +it[k] <= +v.slice(1);
      return String(it[k]) === v;
    }
    // every option shows how many papers it would leave, given the other filter (no dead ends)
    function counts() {
      var f = {};
      $$('button[data-k][aria-pressed="true"]', el).forEach(function (b) { f[b.getAttribute('data-k')] = b.getAttribute('data-v'); });
      $$('button[data-k]', el).forEach(function (b) {
        var k = b.getAttribute('data-k'), v = b.getAttribute('data-v'), n = 0;
        data.items.forEach(function (it) {
          if (!ok(it, k, v)) return;
          for (var o in f) if (o !== k && !ok(it, o, f[o])) return;
          n++;
        });
        var c = $('.b-opt-n', b);
        if (c) c.textContent = String(n);
        b.classList.toggle('zero', !n);
      });
    }
    function after(ul, reason) {
      hold(ul);
      var cur = {};
      $$('li[data-i]', ul).forEach(function (li) { cur[li.getAttribute('data-i')] = 1; });
      for (var i = 0; i < ticks.length; i++) ticks[i].classList.toggle('cur', !!cur[i]);
      counts();
      if ((reason === 'page' || reason === 'filter') && window.gsap && !R.reduce) scanTween(ul, 0.42, 'power2.out', 90);
      // paging from the foot of the list while its head is off screen: bring the head (and the new page) into view
      if (reason === 'page' && fromBottom && !headSeen && head) head.scrollIntoView({ behavior: R.reduce ? 'auto' : 'smooth', block: 'start' });
      fromBottom = false;
    }
    R.list(el, { data: data.items, size: 10, render: function (it) { return it.h; }, empty: data.empty, after: after });
  }

  if (R.reduce || !G) { R.showAll(); return; }       // reduced motion: the final state at once, nothing moves

  var SplitText = window.SplitText, CustomEase = window.CustomEase;
  try { G.registerPlugin.apply(G, [SplitText, CustomEase].filter(Boolean)); } catch (err) {}
  var SWEEP = 'power2.inOut', OUT = 'expo.out';
  if (CustomEase) {
    SWEEP = CustomEase.create('bSweep', 'M0,0 C0.24,0 0.2,1 1,1');   // the hero's calibrated sweep
    OUT = CustomEase.create('bOut', 'M0,0 C0.12,0.82 0.24,1 1,1');
  }
  var css = getComputedStyle(root);
  var TEAL = (css.getPropertyValue('--teal') || '#0a7671').trim(), MUTE = (css.getPropertyValue('--mute') || '#5a6d71').trim();

  // every timeline can be finished at once: a language switch, an error (showAll) or a new width ends in the final state
  var live = [], splits = [];
  function timeline(done) {
    var tl = G.timeline({ onComplete: function () { var i = live.indexOf(tl); if (i >= 0) live.splice(i, 1); if (done) done(); } });
    live.push(tl);
    return tl;
  }
  function finishAll() {
    live.slice().forEach(function (tl) { try { tl.progress(1); } catch (err) {} });
    live = [];
    splits.forEach(function (s) { try { s.revert(); } catch (err) {} });
    splits = [];
    masked.forEach(function (n) { if (n._scan) { n._scan.kill(); n._scan = null; } maskAt(n, null); });
  }
  R.onLang(finishAll);
  R.showHooks.push(finishAll);
  var w0 = window.innerWidth;
  window.addEventListener('resize', function () { if (Math.abs(window.innerWidth - w0) > 2) { w0 = window.innerWidth; finishAll(); } });

  var fontsP = Promise.race([doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve(), new Promise(function (r) { setTimeout(r, 900); })]);
  // the first screen's measurement has the stage: the outcomes sweep waits for it (tall screens see both at once)
  var heroDone = new Promise(function (res) {
    var h = doc.getElementById('fp-hero');
    if (!h || h.classList.contains('fp-done')) return res();
    var t = setTimeout(res, 3400);
    try {
      new MutationObserver(function (_, mo) { if (h.classList.contains('fp-done')) { mo.disconnect(); clearTimeout(t); res(); } })
        .observe(h, { attributes: true, attributeFilter: ['class'] });
    } catch (err) { res(); }
  });

  heads();
  record();
  listIn();
  people();
  depth();
  scrub();

  /* ---------- section names rise out of their axis; the axis is drawn; the lead is scanned in ---------- */
  function heads() {
    $$('.b-sh', root).forEach(function (sh) {
      var h2 = $('.b-h2', sh), draw = $('.b-ax-d', sh);
      var lead = $('.b-lead', sh.parentNode);
      R.inview(sh, function () {
        fontsP.then(function () {
          var span = $('[data-l="' + R.lang + '"]', h2) || h2, st = null;
          if (SplitText) { st = SplitText.create(span, { type: 'lines', mask: 'lines', linesClass: 'b-sl' }); splits.push(st); }
          var lines = st ? st.lines : [span];
          G.set(lines, { yPercent: 106 });
          G.set(draw, { scaleX: 0 });
          on([h2, draw]);
          var tl = timeline(function () {
            if (st) { try { st.revert(); } catch (err) {} var i = splits.indexOf(st); if (i >= 0) splits.splice(i, 1); }
          });
          tl.to(draw, { scaleX: 1, duration: 1.05, ease: SWEEP }, 0);
          tl.to(lines, { yPercent: 0, duration: 0.95, ease: OUT, stagger: 0.09 }, 0.14);
          if (lead && !lead.classList.contains('on')) {
            tl.add(function () { on(lead); scanTween(lead, 1.0, 'power1.inOut', 90); }, 0.42);
            maskAt(lead, 0, 90);
            if (masked.indexOf(lead) < 0) masked.push(lead);
          }
        });
      }, { threshold: 0.85, px: 120 });
    });
  }

  /* ---------- outcomes: the cursor sweeps the years; each number is the running total at the cursor ---------- */
  function record() {
    var band = $('.b-rec', root);
    if (!band) return;
    var lead = $('.b-rec-lead', band), cells = $$('.b-cell', band);
    R.inview(band, function () { Promise.all([heroDone, fontsP]).then(go); }, { threshold: 0.6, px: 190 });

    function go() {
      var D = mobile ? 1.35 : 1.65, T0 = 0.32;
      var ease = G.parseEase(SWEEP);
      var tAt = function (x) {                      // time at which the eased cursor reaches x (0..1)
        var lo = 0, hi = 1;
        for (var i = 0; i < 22; i++) { var m = (lo + hi) / 2; if (ease(m) < x) lo = m; else hi = m; }
        return T0 + D * (lo + hi) / 2;
      };
      var charts = $$('.b-yr', band).map(function (c) {
        var bars = $$('.b-bars i', c);
        return { el: c, bars: bars, n: bars.map(function (b) { return +b.getAttribute('data-n'); }), cur: $('.b-cur', c), rd: $('.b-rd', c),
          labels: $$('.b-yl', c), num: $('.b-c', c.closest('.b-cell')), y0: +c.getAttribute('data-y0'), last: '' };
      });
      var units = $$('.b-un', band).map(function (u) { return { el: u, sq: $$('i', u), num: $('.b-c', u.closest('.b-cell')), lit: -1 }; });
      var totals = $$('.b-c', band).map(function (n) { return { el: n, n: +n.getAttribute('data-count') }; });

      charts.forEach(function (c) {
        c.el.classList.add('b-busy');
        G.set(c.bars, { scaleY: 0 });
        G.set(c.cur, { opacity: 0, scaleY: 0, x: 0 });
        G.set(c.rd, { opacity: 0, x: 0 });
        G.set(c.labels, { opacity: 0 });
        c.num.textContent = '0';
      });
      units.forEach(function (u) { u.sq.forEach(function (s) { s.classList.add('off'); }); u.num.textContent = '0'; });
      G.set(cells, { autoAlpha: 0, y: 10 });
      on(cells);
      if (lead && !lead.classList.contains('on')) { maskAt(lead, 0, 90); if (masked.indexOf(lead) < 0) masked.push(lead); }

      var tl = timeline(done);
      if (lead && !lead.classList.contains('on')) tl.add(function () { on(lead); scanTween(lead, 1.1, 'power1.inOut', 90); }, 0);
      tl.to(cells, { autoAlpha: 1, y: 0, duration: 0.6, ease: OUT, stagger: 0.06 }, 0.04);
      charts.forEach(function (c) {
        tl.to(c.cur, { opacity: 1, scaleY: 1, duration: 0.35, ease: 'power3.out' }, T0 - 0.22);
        tl.to(c.rd, { opacity: 1, duration: 0.2, ease: 'none' }, T0 - 0.1);
        var n = c.bars.length;
        c.bars.forEach(function (b, i) { tl.to(b, { scaleY: 1, duration: 0.6, ease: OUT }, tAt((i + 0.5) / n) - 0.02); });
        // a year label is printed where the cursor has passed (the readout covers it until then)
        c.labels.forEach(function (lb) {
          var x = parseFloat(lb.style.getPropertyValue('--x')) || 0, t = tAt(Math.min(1, x + 0.04));
          var key = lb.classList.contains('k');
          tl.set(lb, { opacity: 1, color: TEAL }, t);
          if (!key) tl.to(lb, { color: MUTE, duration: 0.8, ease: 'power1.inOut' }, t + 0.3);
        });
        tl.to([c.cur, c.rd], { opacity: 0, duration: 0.34, ease: 'power1.in' }, T0 + D - 0.06);
      });
      var sweep = { p: 0 };
      tl.to(sweep, { p: 1, duration: D, ease: 'none', onUpdate: paint }, T0);

      function paint() {
        var p = ease(sweep.p);                       // the cursor position (eased), 0..1
        charts.forEach(function (c) {
          var W = c.el.offsetWidth, n = c.bars.length, x = p * W;
          var k = Math.min(n - 1, Math.floor(p * n)), s = 0;
          for (var i = 0; i < k; i++) s += c.n[i];
          s += c.n[k] * Math.min(1, p * n - k);
          c.num.textContent = String(Math.round(s));
          G.set(c.cur, { x: Math.round(x) - (x >= W - 0.5 ? 1 : 0) });
          var txt = String(c.y0 + k);
          if (txt !== c.last) { c.rd.textContent = txt; c.last = txt; c.rdW = c.rd.offsetWidth; }
          G.set(c.rd, { x: Math.max(0, Math.min(W - (c.rdW || 34), x - (c.rdW || 34) / 2)) });
        });
        units.forEach(function (u) {
          var N = u.sq.length, lit = Math.round(N * p);
          if (lit === u.lit) return;
          for (var i = 0; i < N; i++) u.sq[i].classList.toggle('off', i >= lit);
          u.lit = lit;
          u.num.textContent = String(lit);
        });
      }
      function done() {
        totals.forEach(function (o) { o.el.textContent = String(o.n); });
        charts.forEach(function (c) {
          G.set(c.bars, { clearProps: 'transform' });
          G.set(c.labels, { clearProps: 'opacity,color' });
          G.set([c.cur, c.rd], { opacity: 0 });
          c.el.classList.remove('b-busy');
        });
        units.forEach(function (u) { u.sq.forEach(function (s) { s.classList.remove('off'); }); });
        G.set(cells, { clearProps: 'opacity,visibility,transform' });
      }
    }
  }

  /* ---------- the list block: the record map registers, the first page is scanned in ---------- */
  function listIn() {
    var el = doc.getElementById('b-pubs');
    if (!el) return;
    var ul = $('[data-items]', el), mh = $('.b-mh', el), foot = $('.b-foot', el), fls = $('.b-fls', el);
    var ticks = $$('[data-ticks] > i', el);
    R.inview(ul, function () {
      G.set(ticks, { scaleY: 0 });
      if (fls) G.set(fls.querySelectorAll('.b-flt'), { autoAlpha: 0, y: 8 });
      on([mh, fls, foot]);
      maskAt(ul, 0, 110);
      if (masked.indexOf(ul) < 0) masked.push(ul);
      on(ul);
      var tl = timeline(function () { G.set(ticks, { clearProps: 'transform' }); });
      tl.to(ticks, { scaleY: 1, duration: 0.45, ease: OUT, stagger: { each: 0.0042 } }, 0);
      tl.add(function () { scanTween(ul, 0.95, 'power1.inOut', 110); }, 0.12);
      if (fls) tl.to(fls.querySelectorAll('.b-flt'), { autoAlpha: 1, y: 0, duration: 0.6, ease: OUT, stagger: 0.08, clearProps: 'opacity,visibility,transform' }, 0.05);
    }, { threshold: 0.12, px: 200 });
  }

  /* ---------- portraits open from their baseline and settle into focus (the hero window's material) ---------- */
  function people() {
    $$('.b-pp-g', root).forEach(function (g) {
      var frames = $$('.b-pp-f', g), layers = $$('.b-pp-d', g), texts = $$('.b-pp-t', g);
      R.inview(g, function () {
        G.set(frames, { clipPath: 'inset(100% 0% 0% 0%)' });
        G.set(layers, { scale: 1.08, transformOrigin: '50% 70%' });
        G.set(texts, { autoAlpha: 0, y: 8 });
        on(g); on(frames); on(texts);
        var tl = timeline(function () {
          G.set(frames, { clearProps: 'clipPath' });
          G.set(layers, { scale: 1 });
          G.set(texts, { clearProps: 'opacity,visibility,transform' });
        });
        tl.to(frames, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.95, ease: OUT, stagger: 0.08 }, 0);
        tl.to(layers, { scale: 1, duration: 1.5, ease: 'power2.out', stagger: 0.08 }, 0);
        tl.to(texts, { autoAlpha: 1, y: 0, duration: 0.55, ease: OUT, stagger: 0.08 }, 0.3);
      }, { threshold: 0.3, px: 220 });
    });
  }

  /* ---------- depth: on wide screens a portrait sits a little deeper than its frame while the outer page scrolls ---------- */
  function depth() {
    if (mobile || !G.quickTo) return;
    var items = $$('.b-pp-d', root).map(function (l) { return { l: l, f: l.parentNode, y: G.quickTo(l, 'y', { duration: 0.8, ease: 'power3.out' }) }; });
    if (!items.length) return;
    R.onBand(function (b) {
      items.forEach(function (o) {
        var r = R.rect(o.f);
        if (r.bottom < b.top - 120 || r.top > b.bottom + 120) return;     // off screen: leave it
        var p = R.progress(r);
        if (p != null) o.y((p - 0.5) * 2 * r.h * 0.025);
      });
    });
  }

  /* ---------- the year charts answer the pointer with the hero's cursor and readout (year · count) ---------- */
  function scrub() {
    if (!fine) return;
    $$('.b-yr', root).forEach(function (c) {
      var bars = $$('.b-bars i', c), cur = $('.b-cur', c), rd = $('.b-rd', c), y0 = +c.getAttribute('data-y0'), k0 = -1;
      c.style.pointerEvents = 'auto';
      c.addEventListener('pointermove', function (ev) {
        if (c.classList.contains('b-busy')) return;
        var r = c.getBoundingClientRect(), n = bars.length;
        var k = Math.max(0, Math.min(n - 1, Math.floor((ev.clientX - r.left) / r.width * n)));
        if (k === k0) return;
        k0 = k;
        bars.forEach(function (b, i) { b.classList.toggle('hi', i === k); });
        var x = (k + 0.5) / n * r.width;
        rd.textContent = (y0 + k) + ' · ' + bars[k].getAttribute('data-n');
        var w = rd.offsetWidth;
        G.to(cur, { x: Math.round(x), opacity: 1, scaleY: 1, duration: 0.18, ease: 'power2.out', overwrite: true });
        G.to(rd, { x: Math.max(0, Math.min(r.width - w, x - w / 2)), opacity: 1, duration: 0.18, ease: 'power2.out', overwrite: true });
      });
      c.addEventListener('pointerleave', function () {
        k0 = -1;
        bars.forEach(function (b) { b.classList.remove('hi'); });
        G.to([cur, rd], { opacity: 0, duration: 0.2, ease: 'power1.out', overwrite: true });
      });
    });
  }
})();
"""


# ================================================================== the page
def render():
    hero_html, hero_css, hero_js = _rd('hero.html'), _rd('hero.css'), _rd('hero.js')
    body = (f'<main id="b-main">{hero_html}<div class="b">{outcomes()}'
            f'{core.sample_mark("Research 페이지 일부", "Part of the Research page")}{research()}'
            f'{core.sample_mark("People 페이지 일부", "Part of the People page")}{people()}</div></main>')
    # Noto Sans KR 600 is only a text= subset (titles and names); 400/500 load as Google's unicode-range slices; Hanken
    # Grotesk for Latin and numerals. One stylesheet per weight, so the subset never shadows another face.
    sub600 = core.chars_in(body, classes=('fp-title', 'b-h2', 'b-h3', 'b-pp-n'))
    fonts = []
    for line in _rd('fonts.txt').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        fonts.append(core.gfont('Noto+Sans+KR:wght@600', sub600) if 'Noto+Sans+KR:wght@600' in line else line)
    return core.page_shell('B · 클리니컬 모던 · RIHE', body, css=hero_css + CSS, js=hero_js + '\n' + JS, fonts=fonts,
                           vendor=('gsap', 'split', 'ease', 'draw'), prefix='../', robots='noindex', lang_toggle=True,
                           comment='방향 B · 클리니컬 모던. 원본: tools/kits/b.py, tools/kits/b/ (첫 화면). 설계: site/_directions/b.design.md')


if __name__ == '__main__':
    sys.stdout.write(render())
