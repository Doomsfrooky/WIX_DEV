#!/usr/bin/env python3
"""Direction A · 아카데믹 클래식 (academic classic): the canonical university research institute.

The /67 hero (tools/kits/a/: hero.html, hero.css, hero.js) is the navy masthead, the title page. Everything below it is
set like a page from a university press, derived from that masthead: paper ground, navy ink in one hue family,
Source Serif 4 with Noto Serif KR, hairline rules and the Oxford rule (a heavy line over a hairline) closing every
heading, small capitals for labels, lining tabular figures. Side headings in a left rail, the reading matter in the
main column. Motion is the masthead's own language, used sparingly: line masks, the ruling-pen draw, prints that
develop out of the navy ground. The design document is site/_directions/a.design.md.

Content follows tools/kits/README.md exactly: hero, outcomes (count-up), Research (publication list), People
(faculty + HeAD Lab). The four figures appear once per width: on desktop the hero's own ledger is the outcomes band
(its figures count up as they rise), at 320 (where the hero has no room for the ledger) a navy band directly below it.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import core  # noqa: E402
from core import t, tt, e, img, imgur, name_pair, member_role, initials, lang_attr, json_script, gfont, sample_mark  # noqa: E402

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'a')


def asset(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


# ================================================================== hero (the /67 final, copied verbatim; the ledger
# figures are filled from core.OUTCOMES so they always follow the data)
def num(n, cls):
    """A figure that may count up: the visible digits are aria-hidden (they change while counting), the final value
    is in a visually hidden twin, so a screen reader never meets an intermediate number."""
    return f'<span class="{cls}" aria-hidden="true">{n}</span><span class="sr">{n}</span>'


def hero():
    h = asset('hero.html')
    items = ''.join(f'\n        <li data-ai>{num(n, "hx-num")}<span class="hx-lab">{tt(lab)}</span></li>' for n, lab in core.OUTCOMES)
    h, k = re.subn(r'(<ul class="hx-ledger" data-a>).*?(\n      </ul>)', lambda m: m.group(1) + items + m.group(2), h, flags=re.S)
    assert k == 1, 'hero.html: ledger not found'
    for s in (core.NAME[0], core.INST[0], core.HOME_LEAD[0], core.HOME_LEAD[1]):
        assert s in h, 'hero.html copy differs from core: ' + s[:30]
    return h


# ================================================================== shared pieces
ARROW = ('<svg class="a-arr" viewBox="0 0 22 10" width="22" height="10" aria-hidden="true" focusable="false">'
         '<path d="M0 5h20.5M16.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.25"/></svg>')


def head(hid, title, lead, tag=''):
    """Section head in the rail: the title rises line by line, the Oxford rule closes it (carrying a tag at its right
    end, as the masthead's rule carries RIHE), the lead follows."""
    tg = f'<span class="a-tag">{tag}</span>' if tag else ''
    return (f'<h2 class="a-h2" id="{hid}" data-a>{tt(title)}</h2>'
            f'<div class="a-rule" data-a><i aria-hidden="true"></i>{tg}</div>'
            f'<p class="a-lead" data-a>{tt(lead)}</p>')


def same_or_pair(ko, en, tag='span', cls=''):
    """A name written the same way in both languages is one element (lang="ko" when Hangul), not two copies."""
    if ko == en:
        c = f' class="{cls}"' if cls else ''
        return f'<{tag}{c}{lang_attr(ko)}>{ko}</{tag}>'
    return t(ko, en, tag, cls)


# ================================================================== outcomes (320 only; desktop: the hero's ledger)
def outcomes():
    items = ''.join(f'<li>{num(n, "ao-num")}<span class="ao-lab">{tt(lab)}</span></li>' for n, lab in core.OUTCOMES)
    return f'<section class="ao" aria-labelledby="hx-title"><ul class="ao-l" data-a>{items}</ul></section>'


# ================================================================== Research: the publication list
TEAM_KEYS = core.pub_teams(core.PUBS)
YEARS = core.pub_years(core.PUBS)
SIZE = 10
TICK_LABELS = {2026: 'a', 2020: 'b', 2015: 'c', 2008: 'z'}    # years printed under the tick strip (z: right-aligned)


def team_label(k):
    ko, en = core.TEAM_LABEL[k]
    return ko if ko == en else t(ko, en)


def caps(s):
    """class="cap" for a journal written in capitals in the data: shown in small capitals instead of shouting italic
    capitals (the text is not changed; tools/kits/a.py and the JS caps() must agree)."""
    return ' class="cap"' if re.search('[A-Z]', s) and not re.search('[a-z]', s) else ''


def pub_item(d, i):
    """One entry. tools/kits/a.py and the JS render() below must produce the same markup."""
    return (f'<li class="pl-it" data-i="{i}"><span class="pl-y">{d["year"]}</span>'
            f'<div class="pl-b"><p class="pl-ti"{lang_attr(d["title"])}>{e(d["title"])}</p>'
            f'<p class="pl-au"{lang_attr(d["authors"])}>{e(d["authors"])}</p>'
            f'<p class="pl-j"><cite{lang_attr(d["journal"])}{caps(d["journal"])}>{e(d["journal"])}</cite></p></div>'
            f'<span class="pl-tm">{team_label(d["team"])}</span></li>')


def filt(key, label, values):
    """A facet in the margin: a small-caps label over a column of values; the pressed one is ruled underneath."""
    def btn(v, inner, on=False):
        return f'<button type="button" data-k="{key}" data-v="{v}" aria-pressed="{"true" if on else "false"}">{inner}</button>'
    bs = btn('all', tt(core.UI['all']), True) + ''.join(btn(v, lab) for v, lab in values)
    return (f'<div class="pl-g pl-g-{key}" role="group" aria-label="{e(label[0])}" data-aria-en="{e(label[1])}">'
            f'<span class="pl-k" aria-hidden="true">{tt(label)}</span>{bs}</div>')


def research():
    pubs = core.PUBS
    n = len(pubs)
    first = ''.join(pub_item(d, i) for i, d in enumerate(pubs[:SIZE]))
    ticks, prev = [], None
    for i, d in enumerate(pubs):
        cls = ['on'] + (['cur'] if i < SIZE else []) + (['y0'] if prev is not None and d['year'] != prev else [])
        lab = f' data-y="{d["year"]}" data-yl="{TICK_LABELS[d["year"]]}"' if d['year'] != prev and d['year'] in TICK_LABELS else ''
        ticks.append(f'<i class="{" ".join(cls)}"{lab}></i>')
        prev = d['year']
    data = {
        'items': [{'i': i, 'year': d['year'], 'team': d['team'], 'ti': d['title'], 'au': d['authors'], 'j': d['journal']} for i, d in enumerate(pubs)],
        'team': {k: list(core.TEAM_LABEL[k]) for k in TEAM_KEYS},
        'empty': f'<li class="pl-empty">{tt(core.UI["none"])}</li>',
    }
    teams = [(k, team_label(k)) for k in TEAM_KEYS]
    years = [(y, y) for y in YEARS]
    pages = -(-n // SIZE)
    count = t(f'{n}건', f'{n} items')
    return f"""<section class="a-s a-res" id="research" aria-labelledby="research-h">
  <div class="a-wrap">
    <div class="a-rail">
      {head('research-h', core.RESEARCH_TITLE, core.RESEARCH_LEAD, f'<span data-n aria-live="polite">{count}</span>')}
      <div class="pl-f" data-a>{filt('team', core.UI['team'], teams)}{filt('year', core.UI['year'], years)}</div>
    </div>
    <div class="a-main pl-main" data-a>
      <div class="pl-tk" data-ticks aria-hidden="true">{''.join(ticks)}</div>
      <ol class="pl-items" data-items>{first}</ol>
      <div class="pl-pg">
        <button type="button" class="pl-prev" data-p="-1" aria-label="{e(core.UI['prev'][0])}" data-aria-en="{e(core.UI['prev'][1])}" disabled>{ARROW}</button>
        <span class="pl-pi" data-pi>1 / {pages}</span>
        <button type="button" class="pl-next" data-p="1" aria-label="{e(core.UI['next'][0])}" data-aria-en="{e(core.UI['next'][1])}">{ARROW}</button>
      </div>
    </div>
  </div>
  {json_script(data, 'pl-data')}
</section>"""


# ================================================================== People: faculty + HeAD Lab
def member(m, big):
    ko, en = name_pair(m['name'])
    if m.get('photo'):
        src = m['photo']
        ph = img(imgur(src, 'l'), alt=(ko, en), w=640, h=800, cls='pp-img',
                 srcset=f'{imgur(src, "m")} 320w, {imgur(src, "l")} 640w',
                 sizes='(max-width: 760px) 140px, 30vw' if big else '(max-width: 760px) 140px, 20vw',
                 attrs='decoding="async"')
        frame = f'<div class="pp-ph">{ph}</div>'
    else:
        ik, ie = initials(m['name'])
        frame = f'<div class="pp-ph pp-ini" aria-hidden="true">{same_or_pair(ik, ie)}</div>'
    return (f'<li class="pp-m" data-ai>{frame}'
            f'<p class="pp-nm">{same_or_pair(ko, en)}</p>'
            f'<p class="pp-rl">{tt(member_role(m))}</p></li>')


def group(key, big):
    _, ko, en = core.TEAM_META[key]
    ms = ''.join(member(m, big) for m in core.TEAMS[key]['members'])
    return (f'<div class="pp-g pp-{key}"><h3 class="pp-h" data-a>{t(ko, en)}</h3>'
            f'<ul class="pp-l{" pp-big" if big else ""}" data-a>{ms}</ul></div>')


def people():
    return f"""<section class="a-s a-ppl" id="people" aria-labelledby="people-h">
  <div class="a-wrap">
    <div class="a-rail">{head('people-h', core.PEOPLE_TITLE, core.PEOPLE_LEAD)}</div>
  </div>
  {group('faculty', True)}
  {group('head', False)}
</section>"""


# ================================================================== fonts: one serif voice, Korean as text= subsets
SERIF = 'https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400..600&display=swap'
HANGUL = re.compile('[가-힣]')


def fonts(body):
    """Source Serif 4 (roman and italic, optical sizes) and Noto Serif KR 400 / 600, each Korean weight a text= subset
    of exactly the Hangul set in it (the publication data included, since the list renders every entry)."""
    text = re.sub(r'<(script|style)\b.*?</\1>', ' ', body, flags=re.S)
    data = ' '.join(d['title'] + d['authors'] + d['journal'] for d in core.PUBS) + core.UI['none'][0] + '건'
    bold = ''.join(re.findall(r'<(?:h1|h2|h3)\b.*?</(?:h1|h2|h3)>|<p class="pp-nm">.*?</p>', text, flags=re.S))
    k400 = ''.join(sorted(set(HANGUL.findall(text + data))))
    k600 = ''.join(sorted(set(HANGUL.findall(bold))))
    return [SERIF, gfont('Noto+Serif+KR:wght@400', k400), gfont('Noto+Serif+KR:wght@600', k600)]


# ================================================================== CSS
CSS = r"""
/* ================================================================ direction A · the page below the masthead */
:root {
  --a-n950: #050e21; --a-n900: #081a38; --a-n800: #0d2650; --a-n700: #163469; --a-n500: #2c5596;
  --a-n300: #8aa2c9; --a-n200: #bccae2; --a-n100: #e0e7f2; --a-paper: #f6f4ef;
  --a-ink: #081a38; --a-ink-2: #3a4d72; --a-ink-3: #5b6c8e;
  --a-line: rgba(8, 26, 56, .13); --a-line-2: rgba(8, 26, 56, .3);
  --a-serif: "Source Serif 4", "Noto Serif KR", "Nanum Myeongjo", Georgia, serif;
  --a-pad: clamp(24px, 5vw, 96px);
  --a-gap: clamp(20px, 2.3vw, 40px);
  --a-sec: clamp(72px, 8vw, 132px);
  --a-out: cubic-bezier(.16, .84, .3, 1);
  --a-draw: cubic-bezier(.56, 0, .24, 1);
}
html { background: var(--a-paper); }
body { margin: 0; background: var(--a-paper); color: var(--a-ink); font-family: var(--a-serif); font-optical-sizing: auto; font-kerning: normal; }
::selection { background: var(--a-n900); color: var(--a-paper); }
.a-s, .ao { font-family: var(--a-serif); }
.a-s *, .a-s *::before, .a-s *::after, .ao *, .ao *::before, .ao *::after { box-sizing: border-box; }
.a-s { position: relative; padding: var(--a-sec) var(--a-pad); }
.a-s a, .a-s button { -webkit-tap-highlight-color: transparent; }
.a-s :focus-visible { outline: 2px solid var(--a-n500); outline-offset: 3px; }

/* grid: twelve columns inside the masthead's own side margins; side headings take four, the reading matter eight */
.a-wrap { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--a-gap); align-items: start; }
.a-rail { grid-column: 1 / span 4; }
.a-main { grid-column: 5 / -1; }

/* ---------------------------------------------------------------- section head: title, Oxford rule, lead */
.a-h2 { margin: 0; font-size: clamp(32px, 3.05vw, 46px); font-weight: 600; color: var(--a-ink); }
.a-h2 > span { display: block; text-wrap: balance; }
.a-h2 [data-l="ko"] { font-size: clamp(32px, 3.05vw, 46px); line-height: 1.26; letter-spacing: -.026em; word-break: keep-all; margin-left: -.03em; }
.a-h2 [data-l="en"] { font-size: clamp(31px, 2.95vw, 44px); line-height: 1.12; letter-spacing: -.014em; font-weight: 500; margin-left: -.03em; }
.a-h2 .a-ml-mask { padding-bottom: .16em; margin-bottom: -.16em; }
.a-rule { display: flex; align-items: center; gap: 14px; margin: clamp(18px, 1.7vw, 24px) 0 clamp(18px, 1.7vw, 24px); }
.a-rule i { flex: 1 1 auto; height: 5px; border-top: 2px solid var(--a-ink); border-bottom: 1px solid rgba(8, 26, 56, .5); transform-origin: 0 50%; }
.a-tag { flex: none; font-size: 13px; font-weight: 600; line-height: 1; letter-spacing: .12em; margin-right: -.12em; color: var(--a-ink-2); font-variant-numeric: lining-nums tabular-nums; }
.a-lead { margin: 0; color: var(--a-ink-2); word-break: keep-all; text-wrap: pretty; max-width: 34em; }
.a-lead [data-l="ko"] { font-size: 17px; line-height: 1.86; }
.a-lead [data-l="en"] { font-size: 18px; line-height: 1.6; }

/* ---------------------------------------------------------------- facets: an index in the margin */
.pl-f { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 var(--a-gap); margin-top: clamp(36px, 3.6vw, 56px); padding-top: 18px; border-top: 1px solid var(--a-line-2); }
.pl-g { display: flex; flex-direction: column; align-items: flex-start; }
.pl-k { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 600; line-height: 1.6; letter-spacing: .1em; color: var(--a-ink-3); }
.pl-k [data-l="en"] { font-variant-caps: all-small-caps; font-size: 15px; letter-spacing: .09em; }
.pl-g button {
  position: relative; appearance: none; -webkit-appearance: none; margin: 0; border: 0; border-radius: 0; background: none;
  padding: 7px 0 8px; font: inherit; font-size: 16px; line-height: 1.45; color: var(--a-ink-2); text-align: left; cursor: pointer;
  font-variant-numeric: lining-nums tabular-nums; transition: color .2s ease;
}
.pl-g button::after { content: ""; position: absolute; left: 0; right: 0; bottom: 5px; height: 1.5px; background: currentColor; transform: scaleX(0); transform-origin: 0 50%; transition: transform .38s var(--a-draw), opacity .2s ease; }
.pl-g button:hover { color: var(--a-ink); }
.pl-g button:hover::after { transform: scaleX(1); opacity: .28; }
.pl-g button[aria-pressed="true"] { color: var(--a-ink); }
.pl-g button[aria-pressed="true"]::after { transform: scaleX(1); opacity: 1; }
.pl-g button:active { transform: translateY(1px); }

/* ---------------------------------------------------------------- tick strip: one mark per paper, newest on the left */
.pl-tk { position: relative; display: flex; align-items: flex-end; height: 30px; margin: 4px 0 34px; }
.pl-tk i { position: relative; flex: 1 1 0; min-width: 0; height: 100%; }
.pl-tk i::before { content: ""; position: absolute; left: 50%; bottom: 0; width: 1px; height: 100%; margin-left: -.5px; background: var(--a-ink); opacity: .17; transform: scaleY(.3); transform-origin: 50% 100%; transition: transform .42s var(--a-out), opacity .3s ease, background-color .2s ease; }
.pl-tk i.on::before { opacity: .55; transform: scaleY(.52); }
.pl-tk i.on.cur::before { opacity: 1; transform: scaleY(1); }
.pl-tk i.hov::before { opacity: 1; background: var(--a-n500); transform: scaleY(1.22); transition-duration: .18s; }
.pl-tk i.y0 { margin-left: 2px; }
.pl-tk i[data-y]::after { content: attr(data-y); position: absolute; top: 100%; left: 50%; margin: 8px 0 0 -.5px; padding-left: 6px; border-left: 1px solid var(--a-line-2); font-size: 12px; line-height: 1; letter-spacing: .02em; color: var(--a-ink-3); font-variant-numeric: lining-nums tabular-nums; white-space: nowrap; }
.pl-tk i[data-yl="z"]::after { left: auto; right: 50%; margin: 8px -.5px 0 0; padding: 0 6px 0 0; border-left: 0; border-right: 1px solid var(--a-line-2); }

/* ---------------------------------------------------------------- the list: year | entry | team, ruled like a ledger */
.pl-items { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--a-ink); }
.pl-it { display: grid; grid-template-columns: 3.6em minmax(0, 1fr) 8.6em; column-gap: clamp(16px, 1.6vw, 26px); padding: 17px 0 18px; border-bottom: 1px solid var(--a-line); }
.pl-b { max-width: 42em; }
.pl-y { font-size: 15px; font-weight: 600; line-height: 1.6; color: var(--a-ink); font-variant-numeric: lining-nums tabular-nums; transition: opacity .2s ease; }
.pl-same .pl-y { opacity: 0; }
.pl-ti { margin: 0; font-size: 17px; line-height: 1.5; color: var(--a-ink); text-wrap: pretty; overflow-wrap: anywhere; }
.pl-ti[lang="ko"] { font-size: 16px; line-height: 1.72; word-break: keep-all; overflow-wrap: break-word; }
.pl-au { margin: 5px 0 0; font-size: 14px; line-height: 1.55; color: var(--a-ink-2); overflow-wrap: anywhere; }
.pl-j { margin: 1px 0 0; font-size: 14px; line-height: 1.55; color: var(--a-ink-2); }
.pl-j cite { font-style: italic; }
.pl-j cite[lang="ko"] { font-style: normal; }
.pl-j cite.cap { font-variant-caps: all-small-caps; font-size: 15.5px; letter-spacing: .045em; }
.pl-tm { padding-top: 2px; font-size: 13px; line-height: 22px; height: 24px; color: var(--a-ink-3); text-align: right; letter-spacing: .02em; white-space: nowrap; }
.pl-tm, .pl-tm [data-l="en"] { font-variant-caps: all-small-caps; font-size: 15px; letter-spacing: .07em; }
.pl-tm [data-l="ko"] { font-variant-caps: normal; font-size: 13px; letter-spacing: 0; }
.pl-empty { padding: 28px 0; font-size: 16px; line-height: 24px; color: var(--a-ink-2); border-bottom: 1px solid var(--a-line); }

/* ---------------------------------------------------------------- pager */
.pl-pg { display: flex; align-items: center; justify-content: flex-end; gap: 6px; padding-top: 14px; border-top: 1px solid var(--a-ink); }
.pl-main { scroll-margin-top: 24px; }
.pl-pi { min-width: 5.2em; text-align: center; font-size: 15px; color: var(--a-ink-2); font-variant-numeric: lining-nums tabular-nums; }
.pl-pg button {
  width: 44px; height: 44px; display: grid; place-items: center; margin: 0; padding: 0; border: 1px solid var(--a-line-2); border-radius: 0;
  background: transparent; color: var(--a-ink); cursor: pointer; transition: border-color .2s ease, background-color .2s ease, opacity .2s ease;
}
.pl-pg .a-arr { transition: transform .32s var(--a-out); }
.pl-prev .a-arr { transform: scaleX(-1); }
.pl-pg button:hover:not(:disabled) { border-color: var(--a-ink); background: rgba(8, 26, 56, .04); }
.pl-next:hover:not(:disabled) .a-arr { transform: translateX(3px); }
.pl-prev:hover:not(:disabled) .a-arr { transform: scaleX(-1) translateX(3px); }
.pl-pg button:active:not(:disabled) { background: rgba(8, 26, 56, .08); }
.pl-pg button:disabled { opacity: .32; cursor: default; }

/* ---------------------------------------------------------------- people: prints in a navy duotone, mounted on paper */
.pp-g { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--a-gap); align-items: start; margin-top: clamp(40px, 4vw, 64px); padding-top: clamp(22px, 2vw, 30px); border-top: 1px solid var(--a-line-2); }
.pp-h { grid-column: 1 / span 4; margin: 0; font-size: 19px; font-weight: 600; line-height: 1.4; color: var(--a-ink); letter-spacing: -.005em; }
.pp-h [data-l="en"] { font-variant-caps: all-small-caps; font-size: 21px; letter-spacing: .08em; }
.pp-l { grid-column: 5 / -1; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(30px, 3vw, 44px) var(--a-gap); max-width: 960px; margin: 0; padding: 0; list-style: none; }
.pp-m { min-width: 0; }
/* the frame's ground is black: through the duotone it becomes exactly the prints' darkest navy, so a print develops
   out of its own deepest tone (as the masthead footage develops out of the navy ground) */
.pp-ph { position: relative; aspect-ratio: 4 / 5; overflow: hidden; background: #000; isolation: isolate; }
.pp-img { position: absolute; left: 0; top: -14px; width: 100%; height: calc(100% + 28px); object-fit: cover; object-position: 50% 28%; filter: grayscale(1) contrast(1.08) brightness(1.04); }
.pp-ph::before, .pp-ph::after { content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none; transition: opacity .7s var(--a-out); }
.pp-ph::before { background: #ebe6dc; mix-blend-mode: multiply; }
.pp-ph::after { background: var(--a-n800); mix-blend-mode: screen; }
.pp-ini { display: grid; place-items: center; background: var(--a-n800); color: var(--a-n100); font-size: clamp(40px, 4vw, 64px); font-weight: 600; }
.pp-ini::before, .pp-ini::after { display: none; }
.pp-nm { margin: 15px 0 0; font-size: 18px; font-weight: 600; line-height: 1.35; color: var(--a-ink); }
.pp-nm [data-l="en"], .pp-nm[lang="en"] { font-size: 18.5px; letter-spacing: -.005em; }
.pp-rl { margin: 4px 0 0; font-size: 14px; line-height: 1.55; color: var(--a-ink-2); word-break: keep-all; }

/* ---------------------------------------------------------------- outcomes band (320: under the masthead) */
.ao { display: none; }

/* ---------------------------------------------------------------- reveal (hidden only while motion runs) */
html.js:not(.rm) .a-s [data-a]:not(.on), html.js:not(.rm) .ao [data-a]:not(.on) { opacity: 0; }
html.js:not(.rm) .a-s [data-ai]:not(.on) { opacity: 0; }

/* ---------------------------------------------------------------- from 1600: the wide column reads from further away */
@media (min-width: 1600px) {
  .pl-b { max-width: 44em; }
  .pl-y { font-size: 16px; }
  .pl-ti { font-size: 18px; }
  .pl-ti[lang="ko"] { font-size: 17px; }
  .pl-au, .pl-j { font-size: 15px; }
  .pl-j cite.cap { font-size: 16.5px; }
  .pl-it { padding: 19px 0 20px; }
}

/* ---------------------------------------------------------------- up to 1200: the team label joins the entry, the entry gets the width */
@media (max-width: 1200px) {
  .pl-it { grid-template-columns: 3.6em minmax(0, 1fr); grid-template-areas: "y b" "y tm"; }
  .pl-y { grid-area: y; } .pl-b { grid-area: b; }
  .pl-tm { grid-area: tm; padding-top: 3px; text-align: left; }
}
@media (max-width: 1100px) {
  .pl-tk i[data-yl="c"]::after { display: none; }
}

/* ---------------------------------------------------------------- 980 and below: one column, the facets as rows */
@media (max-width: 960px) {
  .a-rail, .a-main, .pp-h, .pp-l { grid-column: 1 / -1; }
  .a-lead { max-width: 38em; }
  .pl-f { grid-template-columns: 1fr; gap: 4px; margin: 30px 0 30px; padding-top: 14px; }
  .pl-g { flex-direction: row; flex-wrap: wrap; align-items: baseline; column-gap: 18px; }
  .pl-k { width: 3.4em; margin: 0; }
  .pp-l { margin-top: 22px; }
}

/* ---------------------------------------------------------------- phone (Wix mobile renders this file at 320) */
@media (max-width: 760px) {
  :root { --a-pad: 16px; --a-sec: 56px; }
  .a-h2 [data-l="ko"] { font-size: 28px; line-height: 1.3; }
  .a-h2 [data-l="en"] { font-size: 27px; line-height: 1.15; }
  .a-rule { margin: 14px 0 14px; gap: 10px; }
  .a-rule i { height: 4px; border-top-width: 1.5px; }
  .a-tag { font-size: 12px; }
  .a-lead [data-l="ko"] { font-size: 15.5px; line-height: 1.8; }
  .a-lead [data-l="en"] { font-size: 16px; line-height: 1.58; }
  .pl-f { margin: 24px 0 22px; }
  .pl-g { column-gap: 14px; }
  .pl-k { width: 100%; margin: 4px 0 -2px; }
  .pl-g-year { display: grid; grid-template-columns: repeat(4, max-content); column-gap: 22px; }
  .pl-g-year .pl-k { grid-column: 1 / -1; }
  .pl-g button { font-size: 15px; padding: 9px 0 10px; }
  .pl-g button::after { bottom: 7px; }
  .pl-tk { height: 26px; margin-bottom: 30px; }
  .pl-tk i.y0 { margin-left: 1px; }
  .pl-it { grid-template-columns: auto minmax(0, 1fr); grid-template-areas: "y tm" "b b"; row-gap: 5px; padding: 15px 0 16px; }
  .pl-y { grid-area: y; font-size: 14px; line-height: 22px; }
  .pl-same .pl-y { opacity: 1; }
  .pl-tm { grid-area: tm; padding-top: 0; height: 22px; text-align: right; }
  .pl-tm, .pl-tm [data-l="en"] { font-size: 14px; }
  .pl-tm [data-l="ko"] { font-size: 12.5px; }
  .pl-b { grid-area: b; }
  .pl-ti { font-size: 15.5px; line-height: 1.48; }
  .pl-ti[lang="ko"] { font-size: 15px; line-height: 1.68; }
  .pl-au, .pl-j { font-size: 13.5px; }
  .pl-pg { justify-content: space-between; padding-top: 12px; }
  .pl-main { scroll-margin-top: 156px; }   /* the Wix mobile header (140 px) is sticky */
  .pp-g { margin-top: 36px; padding-top: 18px; }
  .pp-h { font-size: 17.5px; }
  .pp-h [data-l="en"] { font-size: 19px; }
  /* faculty: a directory row each (print on the left, name and role beside it) */
  .pp-big { grid-template-columns: 1fr; gap: 18px; margin-top: 18px; }
  .pp-big .pp-m { display: grid; grid-template-columns: 112px minmax(0, 1fr); column-gap: 16px; align-items: end; }
  .pp-big .pp-ph { grid-row: 1 / span 2; }
  .pp-big .pp-nm { margin: 0; align-self: end; }
  .pp-big .pp-rl { align-self: start; padding-bottom: 2px; }
  .pp-head .pp-l { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px 16px; margin-top: 18px; }
  .pp-nm { margin-top: 11px; font-size: 16.5px; }
  .pp-rl { font-size: 13px; }

  .ao { display: block; padding: 0 16px 28px; background: var(--a-n900); color: var(--a-paper); -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  .ao-l { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); margin: 0; padding: 0; list-style: none; border-bottom: 1px solid rgba(224, 231, 242, .24); }
  .ao-l li { padding: 16px 12px 15px 0; border-top: 1px solid rgba(224, 231, 242, .24); }
  .ao-l li:nth-child(2n) { padding-left: 16px; border-left: 1px solid rgba(224, 231, 242, .24); }
  .ao-num { display: block; font-size: 38px; line-height: 1; font-weight: 400; letter-spacing: -.01em; font-variant-numeric: lining-nums tabular-nums; }
  .ao-lab { display: block; margin-top: 8px; font-size: 13.5px; line-height: 1.4; color: var(--a-n200); word-break: keep-all; }
}

@media (prefers-contrast: more) {
  :root { --a-ink-2: #22355a; --a-ink-3: #3a4d72; --a-line: rgba(8, 26, 56, .3); }
}
@media (forced-colors: active) {
  .pp-ph::before, .pp-ph::after, .pl-tk { display: none; }
  .pl-g button[aria-pressed="true"] { outline: 2px solid ButtonText; }
}
@media print {
  .pl-tk, .pl-pg, .pl-f { display: none; }
  .a-s [data-a], .a-s [data-ai] { opacity: 1 !important; transform: none !important; }
}
"""

# ================================================================== JS (runs after the hero's script)
JS = r"""
/* Direction A · page motion and the publication list. The list works without GSAP; motion needs it. */
var R = window.RIHE || {}, G = window.gsap, ST = window.SplitText, CE = window.CustomEase;
var doc = document;
var $ = function (s, c) { return (c || doc).querySelector(s); };
var $$ = function (s, c) { return [].slice.call((c || doc).querySelectorAll(s)); };
var reduce = !!R.reduce, motion = !!G && !reduce;
var phone = !!(window.matchMedia && matchMedia('(max-width: 760px)').matches);
var OUT = 'expo.out', DRAW = 'power2.inOut';
if (G && CE) { try { CE.create('aOut', 'M0,0 C0.16,0.84 0.3,1 1,1'); CE.create('aDraw', 'M0,0 C0.56,0 0.24,1 1,1'); OUT = 'aOut'; DRAW = 'aDraw'; } catch (e) {} }
if (G && ST) { try { G.registerPlugin(ST); } catch (e) {} }
if (!G && R.showAll) R.showAll();
function on(el) { if (el) el.classList.add('on'); }
function lang() { return R.lang === 'en' ? 'en' : 'ko'; }
function fontsThen(cb) {
  var done = false, go = function () { if (!done) { done = true; cb(); } };
  setTimeout(go, 900);
  try { doc.fonts.ready.then(go, go); } catch (e) { go(); }
}

/* =============================================================== 1. publication list (RIHE.list: fixed height) */
var res = $('#research'), tk = $('.pl-tk'), ticks = tk ? [].slice.call(tk.children) : [], dir = 1, listShown = false, turnedAtFoot = false;
var PL = JSON.parse($('#pl-data').textContent);
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;'); }
function la(s) { return /[가-힣]/.test(s) ? ' lang="ko"' : ' lang="en"'; }
function caps(s) { return /[A-Z]/.test(s) && !/[a-z]/.test(s) ? ' class="cap"' : ''; }
function team(k) { var p = PL.team[k]; return p[0] === p[1] ? p[0] : '<span data-l="ko">' + p[0] + '</span><span data-l="en" lang="en">' + p[1] + '</span>'; }
function render(d) {
  return '<li class="pl-it" data-i="' + d.i + '"><span class="pl-y">' + d.year + '</span>' +
    '<div class="pl-b"><p class="pl-ti"' + la(d.ti) + '>' + esc(d.ti) + '</p>' +
    '<p class="pl-au"' + la(d.au) + '>' + esc(d.au) + '</p>' +
    '<p class="pl-j"><cite' + la(d.j) + caps(d.j) + '>' + esc(d.j) + '</cite></p></div>' +
    '<span class="pl-tm">' + team(d.team) + '</span></li>';
}
// after every draw: the year is printed once per run of the same year (a ledger's ditto), the current page's marks
// stand up in the strip, and a page change slides in from the side it was turned to
function after(ul, why) {
  var items = $$('.pl-it', ul), cur = {}, prev = null;
  items.forEach(function (li) {
    var y = li.querySelector('.pl-y').textContent;
    li.classList.toggle('pl-same', y === prev); prev = y;
    cur[li.getAttribute('data-i')] = 1;
  });
  ticks.forEach(function (x, i) { x.classList.toggle('cur', !!cur[i]); x.classList.remove('hov'); });
  if (why === 'page' && turnedAtFoot) {
    turnedAtFoot = false;
    var mainEl = $('.pl-main'), b = R.band, r = R.rect ? R.rect(mainEl) : null;
    if (r && b && b.ok && r.top < b.top) { try { mainEl.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); } catch (e) { mainEl.scrollIntoView(true); } }
  }
  if (!motion || !listShown || (why !== 'page' && why !== 'filter')) return;
  var rows = $$('.pl-it, .pl-empty', ul);
  G.killTweensOf(rows);
  if (why === 'page') G.fromTo(rows, { x: 14 * dir, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.42, ease: OUT, stagger: 0.022, clearProps: 'transform,opacity,visibility' });
  else G.fromTo(rows, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.32, ease: 'power1.out', stagger: 0.012, clearProps: 'opacity,visibility' });
}
if (res && R.list) {
  // which way the page was turned (capture: before the engine redraws)
  res.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('button[data-p]'); if (b && !b.disabled) { dir = +b.getAttribute('data-p') < 0 ? -1 : 1; turnedAtFoot = true; } }, true);
  R.list(res, { data: PL.items, size: 10, render: render, empty: PL.empty, after: after });
  // pointing at an entry marks its paper in the strip: where it sits in the whole record
  var ul = $('.pl-items');
  ul.addEventListener('mouseover', function (e) { var li = e.target.closest && e.target.closest('.pl-it'); var x = li && ticks[+li.getAttribute('data-i')]; if (x) x.classList.add('hov'); });
  ul.addEventListener('mouseout', function (e) { var li = e.target.closest && e.target.closest('.pl-it'); var x = li && ticks[+li.getAttribute('data-i')]; if (x && !(e.relatedTarget && li.contains(e.relatedTarget))) x.classList.remove('hov'); });
}

/* =============================================================== 1b. one height for both languages
   The Wix element has one fixed height for KO and EN (the language changes inside it), so every block whose two
   versions differ reserves the taller one. The other language is swapped in on the root for one synchronous layout
   (nothing paints, no language hooks run), measured, and swapped back. Re-run when fonts or the width change. */
var EQ = '.a-rail, .pp-h, .pp-m, .ao-l li', geo = 0;     // geo: bumped whenever block heights (so positions) change
function equalize() {
  var root = doc.documentElement, cur = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko', els = $$(EQ);
  els.forEach(function (el) { el.style.minHeight = ''; });
  var a = els.map(function (el) { return el.getBoundingClientRect().height; });
  root.setAttribute('data-lang', cur === 'en' ? 'ko' : 'en');
  var b = els.map(function (el) { return el.getBoundingClientRect().height; });
  root.setAttribute('data-lang', cur);
  els.forEach(function (el, i) { el.style.minHeight = Math.ceil(Math.max(a[i], b[i])) + 'px'; });
  geo++;
  // the sentinel band tiles the document as it was when fonts arrived; if the list or this pass changed the height
  // afterwards, let the runtime's own resize path re-tile it (it rebuilds only when the height really changed)
  var H = Math.max(root.scrollHeight, doc.body.scrollHeight);
  if (R.band && R.band.docH && Math.abs(H - R.band.docH) > 1) { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }
}
equalize();
try { doc.fonts.ready.then(equalize); doc.fonts.addEventListener('loadingdone', function () { requestAnimationFrame(equalize); }); } catch (e) {}
(function () {
  var w = window.innerWidth, rz = 0;
  window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (window.innerWidth !== w) { w = window.innerWidth; equalize(); } }, 180); });
})();

if (!motion) { listShown = true; return; }

/* =============================================================== 2. section heads: lines rise, the rule is drawn */
function headIn(sec) {
  var h2 = $('.a-h2', sec), rule = $('.a-rule', sec), bar = $('.a-rule i', sec), tag = $('.a-tag', sec), lead = $('.a-lead', sec);
  if (!h2) return;
  R.inview(h2, function () {
    fontsThen(function () {
      var span = $('[data-l="' + lang() + '"]', h2), sp = null;
      try { if (ST) sp = new ST(span, { type: 'lines', mask: 'lines', linesClass: 'a-ml' }); } catch (e) { sp = null; }
      var lines = sp ? sp.lines : [span];
      G.set(lines, { yPercent: 115 });
      G.set(bar, { scaleX: 0, transformOrigin: '0% 50%' });
      if (tag) G.set(tag, { autoAlpha: 0 });
      G.set(lead, { autoAlpha: 0, y: 12 });
      [h2, rule, lead].forEach(on);
      var tl = G.timeline({ defaults: { ease: OUT }, onComplete: function () {
        if (sp) { try { sp.revert(); } catch (e) {} }
        G.set([bar, lead].concat(tag ? [tag] : []), { clearProps: 'transform,opacity,visibility' });
      } });
      tl.to(lines, { yPercent: 0, duration: 1.1, stagger: 0.09 }, 0)
        .to(bar, { scaleX: 1, duration: 1.15, ease: DRAW }, 0.3)
        .to(lead, { autoAlpha: 1, y: 0, duration: 0.95 }, 0.5);
      if (tag) tl.to(tag, { autoAlpha: 1, duration: 0.6, ease: 'power1.out' }, 1.1);
    });
  }, { threshold: 0.5, px: 50 });
}
$$('.a-s').forEach(headIn);

/* =============================================================== 3. research body: facets, the strip is written, the list settles */
(function () {
  var fac = $('.pl-f'), main = $('.pl-main');
  if (fac) R.inview(fac, function () {
    G.set(fac, { autoAlpha: 0, y: 10 }); on(fac);
    G.to(fac, { autoAlpha: 1, y: 0, duration: 0.9, ease: OUT, delay: 0.15, clearProps: 'transform,opacity,visibility' });
  }, { threshold: 0.3, px: 80 });
  if (main) R.inview(main, function () {
    var list = $('.pl-items', main), pg = $('.pl-pg', main);
    G.set(tk, { clipPath: 'inset(0% 100% -60% 0%)' });
    G.set([list, pg], { autoAlpha: 0, y: 12 });
    on(main);
    G.timeline({ defaults: { ease: OUT }, onComplete: function () { listShown = true; G.set([tk, list, pg], { clearProps: 'clipPath,transform,opacity,visibility' }); } })
      .to(tk, { clipPath: 'inset(0% 0% -60% 0%)', duration: 1.25, ease: DRAW }, 0)
      .to(list, { autoAlpha: 1, y: 0, duration: 0.9 }, 0.25)
      .to(pg, { autoAlpha: 1, y: 0, duration: 0.8 }, 0.45);
  }, { threshold: 0.12, px: 160 });
})();

/* =============================================================== 4. people: the prints develop out of the navy ground */
$$('.pp-g').forEach(function (g) {
  var h = $('.pp-h', g), l = $('.pp-l', g);
  R.inview(g, function () {
    var ms = $$('.pp-m', l), ims = $$('.pp-img', l), tx = $$('.pp-nm, .pp-rl', l), t0 = Date.now();
    // the heading, the plates and the names come in at once; a plate shows the prints' deepest navy (the unexposed
    // print) and each print develops out of it as soon as its own image is decoded, in reading order
    G.set(h, { autoAlpha: 0, y: 8 }); G.set(ims, { autoAlpha: 0, scale: 1.07 }); G.set(tx, { autoAlpha: 0, y: 8 });
    on(h); on(l); ms.forEach(on);
    G.to(h, { autoAlpha: 1, y: 0, duration: 0.8, ease: OUT, clearProps: 'transform,opacity,visibility' });
    G.to(tx, { autoAlpha: 1, y: 0, duration: 0.8, ease: OUT, stagger: 0.045, delay: 0.3, clearProps: 'transform,opacity,visibility' });
    ims.forEach(function (im, i) {
      var done = false, go = function () {
        if (done) return; done = true;
        var wait = Math.max(0, 0.1 + i * 0.09 - (Date.now() - t0) / 1000);
        G.to(im, { autoAlpha: 1, scale: 1, duration: 1.7, ease: OUT, delay: wait, clearProps: 'opacity,visibility' });   // the transform stays: the band drift owns y
      };
      setTimeout(go, 900);
      if (im.decode) im.decode().then(go, go); else go();
    });
  }, { threshold: 0.18, px: 160 });
});

/* =============================================================== 5. outcomes band (320): the figures count up */
(function () {
  var band = $('.ao'), list = band && $('.ao-l', band);
  if (!list || getComputedStyle(band).display === 'none') return;
  R.inview(list, function () {
    var nums = $$('.ao-num', list), labs = $$('.ao-lab', list), vals = nums.map(function (n) { return parseInt(n.textContent, 10) || 0; });
    nums.forEach(function (n) { n.textContent = '0'; });
    G.set(labs, { autoAlpha: 0, y: 6 });
    on(list);
    nums.forEach(function (n, i) {
      var o = { v: 0 };
      G.to(o, { v: vals[i], duration: 1.35, ease: 'power3.out', delay: 0.1 + i * 0.09, onUpdate: function () { n.textContent = String(Math.round(o.v)); }, onComplete: function () { n.textContent = String(vals[i]); } });
    });
    G.to(labs, { autoAlpha: 1, y: 0, duration: 0.8, ease: OUT, stagger: 0.09, delay: 0.45, clearProps: 'transform,opacity,visibility' });
  }, { threshold: 0.5, px: 100 });
})();

/* =============================================================== 6. faculty prints behind a mat window (band-driven, desktop) */
if (!phone && R.onBand && R.rect && R.progress) {
  var mats = $$('.pp-faculty .pp-ph'), imgs = mats.map(function (m) { return m.querySelector('.pp-img'); }), lastP = [], rects = null, rg = -1;
  window.addEventListener('resize', function () { rects = null; });
  R.onBand(function (b) {
    if (!b.ok) return;
    if (!rects || rg !== geo) { rects = mats.map(R.rect); rg = geo; }     // document px: stable until layout changes
    mats.forEach(function (m, i) {
      var p = R.progress(rects[i]), im = imgs[i];
      if (p == null || !im || Math.abs(p - (lastP[i] == null ? -1 : lastP[i])) < 0.004) return;
      lastP[i] = p;
      G.set(im, { y: (0.5 - p) * 24 });
    });
  });
}
"""


def render():
    body = '\n'.join([
        hero(),
        outcomes(),
        sample_mark('Research 페이지 일부', 'Part of the Research page'),
        research(),
        sample_mark('People 페이지 일부', 'Part of the People page'),
        people(),
    ])
    js = ('try { (function () {\n' + asset('hero.js') + '\n})(); } catch (err) { if (window.console) console.error(err); window.RIHE && RIHE.showAll(); }\n'
          '(function () {\n' + JS + '\n})();')
    return core.page_shell('A · 아카데믹 클래식 · RIHE', body, css=asset('hero.css') + CSS, js=js, fonts=fonts(body),
                           vendor=('gsap', 'split', 'ease'), prefix='../', robots='noindex', lang_toggle=True,
                           comment='방향 A 시안: tools/kits/a.py + tools/kits/a/ (hero). 설계: site/_directions/a.design.md')
