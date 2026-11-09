#!/usr/bin/env python3
"""RIHE design system, stage 2: direction C2 "에디토리얼 시네마틱 · 흰 지면" (confirmed by the client, 2026-11-08).

Read tools/KIT.md first (every component with its signature and an example) and DESIGN.md (tokens, type, motion).
One white sheet (#ffffff, the Wix chrome is #ffffff), ink type, umber #8a5a0e as the only text accent, amber only for
the selection, warm photography, heavy display type (Black Han Sans KO / Archivo EN), Noto Sans KR for reading.
The cinema comes from the editing: an ink cut line is drawn, holds a beat, splits and the frame opens from it; titles
cross the frame's edge as a knockout; hard cuts, rack focus, counter wheels. Lab identity: soft pastel tints for
surfaces, deeper accessible tones for text and lines (TONES).

    import kit
    from kit import t, sec, more

    def render():
        body = (kit.page_hero(('연락처', 'Contact'), alt=('청각재활연구소에 문의하기', 'Get in touch'), image=kit.gallery_photo(5))
                + '<main>' + sec(('연구소 안내', 'Visit us'), kit.kv([...]), 'visit') + '</main>')
        return kit.page('Contact', body)

Every function returns an HTML string. Every visible string is a KO/EN pair (t(), tt() or a (ko, en) tuple).
The design-free runtime (language, safe reveals, the sentinel band, the list engine, the page shell) is tools/core.py.
The Home hero's assets (hero.html, hero.css, hero.js, reel.json) are in tools/kit_assets/.
"""
import json
import math
import os
import re

import core
from core import *  # noqa: F401,F403  (copy, data, helpers)
from core import e, t, tt, link, ext, img, imgur, wix, wix_poster, name_pair, initials, lang_attr, json_script  # noqa: F401

PREVIEW = False          # tools/build.py sets this; True adds the small KO/EN toggle (site-preview/)
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'kit_assets')
_HANGUL = re.compile('[가-힣]')


def rd(name):
    with open(os.path.join(ASSETS, name), encoding='utf-8') as f:
        return f.read()


# ================================================================== tokens
# Lab identity (2026-11-09): (pastel tint for surfaces, deep tone for text and lines). Every deep tone is AA (>= 4.5:1)
# on white and on its own tint; ink on every tint >= 15.8:1. Audiso's deep tone is the site's umber (its logo's gold).
TONES = {
    'inst': ('#e8ebf2', '#2d3f66'),      # the institute (faculty, Research, About, Contact, Gallery heroes)
    'basic': ('#e5efe8', '#2c6447'),     # Basic Lab
    'hearing': ('#e3edf4', '#2c5a77'),   # Hearing Lab
    'head': ('#e9e8f5', '#45458a'),      # HeAD Lab
    'audiso': ('#f6e6dc', '#8a5a0e'),    # Audiso
    'collab': ('#ecebe8', '#5b5852'),    # 협력·임상 (publications)
    'admin': ('#ecebe8', '#4e4b47'),     # administration
}
TEAM_TONE = {'faculty': 'inst', 'basic': 'basic', 'hearing': 'hearing', 'head': 'head', 'admin': 'admin',
             'audiso': 'audiso', 'collab': 'collab'}


def tone_style(key):
    """Inline style that sets a component's lab tone: --tt (tint) and --td (deep)."""
    key = TEAM_TONE.get(key, key)
    if key not in TONES:
        raise KeyError(f'unknown tone {key!r}; tones: {", ".join(TONES)}')
    return f'--tt:var(--t-{key});--td:var(--d-{key})'


# ================================================================== small helpers
AR = '<svg class="k-ar" viewBox="0 0 20 10" aria-hidden="true"><path d="M0 5h18M14 1l4 4-4 4"/></svg>'
AR_X = '<svg class="k-ar k-ar--x" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 9.5l7-7M4 2.5h5.5V8"/></svg>'
CH_L = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>'
CH_R = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>'


def _h(x):
    """A heading or label: (ko, en) tuple -> pair; a plain Latin string (a lab name) -> <span lang="en">; html as is."""
    if isinstance(x, tuple):
        return tt(x)
    if isinstance(x, str) and x and '<' not in x and not _HANGUL.search(x):
        return f'<span lang="en">{x}</span>'
    return x or ''


def _plain(x):
    return re.sub(r'<[^>]+>', '', x or '').replace('&amp;', '&').replace('&nbsp;', ' ')


def nw(s):
    return f'<span class="nw">{s}</span>'


def nw_paren(s):
    """Keep a parenthetical with the word before it: '특허 (출원·등록)' never breaks inside the brackets."""
    return re.sub(r' (\([^)]*\))', r' <span class="nw">\1</span>', s)


def more(path, ko, en=None, cls='', external=False):
    """Text link with C2's umber arrow (underline thickens on hover). path: page name, site path or (external) URL."""
    inner = f'<span class="k-mt">{t(ko, en)}</span>' + (AR_X if external else AR)
    c = 'k-more' + (' ' + cls if cls else '')
    return ext(path, inner, c) if external else link(path, inner, c)


def btn(href, ko, en=None, external=True):
    """Outlined button link (44 px, square); fills with ink on hover. Wrap several in <p class="k-btns">."""
    inner = f'<span class="k-mt">{t(ko, en)}</span>' + (AR_X if external else AR)
    return ext(href, inner, 'k-btn') if external else link(href, inner, 'k-btn')


def mail(addr):
    return f'<a class="k-mail" href="mailto:{addr}">{addr}</a>'


def mark(key):
    """Small square in a lab's deep tone (lists, jump links)."""
    return f'<i class="k-mk" style="{tone_style(key)}" aria-hidden="true"></i>'


# ================================================================== sections
def sec(h, body, sid='', note='', aside='', cls='', wide=False, tone=None, link_html='', level=2, lk=True):
    """The standard section on C2's 34% axis: an ink cut line across, the heading column (h2 in the display face, an
    optional note and aside) and the body column. h, note: (ko, en) tuples or html. wide=True: the heading row (with
    link_html at its right) and the body below it across both columns. tone: a TONES key; puts a short tab in the lab's
    deep tone on the cut line. If body has no reveal block ([data-a]) of its own, the body column reveals as one block.
    lk: the section reserves the taller of its two languages (KO = EN height)."""
    if not sid:
        raise ValueError('sec() needs a sid (section id)')
    hid = f'{sid}-h'
    n = f'<p class="k-note">{_h(note)}</p>' if note else ''
    a = f'<div class="k-aside">{aside}</div>' if aside else ''
    head = (f'<div class="k-sh" data-a data-m="head"><h{level} class="k-h" id="{hid}"><span class="k-hm"><span class="k-hl">{_h(h)}</span></span>'
            f'</h{level}>{n}{a}</div>')
    lnk = f'<div class="k-swl" data-a>{link_html}</div>' if link_html else ''
    ba = '' if 'data-a' in body else ' data-a'
    c = 'k-sec' + (' k-sec--wide' if wide else '') + (' k-sec--tone' if tone else '') + (' ' + cls if cls else '')
    ts = f' style="{tone_style(tone)}"' if tone else ''
    return (f'<section class="{c}" id="{sid}" aria-labelledby="{hid}"{ts}><div class="k-in"{" data-lk" if lk else ""}>'
            f'<i class="k-ln" aria-hidden="true" data-a data-m="ln"></i>{head}{lnk}<div class="k-sb"{ba}>{body}</div></div></section>')


def sec_wide(h, body, sid='', note='', link_html='', cls='', tone=None):
    """sec(..., wide=True): heading row with a link at its right, body across both columns (gallery pattern)."""
    return sec(h, body, sid, note=note, cls=cls, wide=True, tone=tone, link_html=link_html)


def _lines(x):
    return [x] if isinstance(x, str) else list(x)


def chapter(ko, en, sid='', lead_pair=None, one_line=False):
    """C2's chapter heading: display type across both columns (KO Black Han Sans, EN Archivo condensed caps) in
    authored lines; each line rises through a mask of a fixed height, the same in both languages. ko, en: a string
    (one line) or a list of lines. lead_pair: optional (ko, en) lead in the body column. Use it to open a big part of a
    page (Research: '청각재활연구소의 / 연구 성과'); the sections that follow can use sec(level=3)."""
    if not sid:
        raise ValueError('chapter() needs a sid')
    m = lambda ls: ' '.join(f'<span class="m"><span class="l">{x}</span></span>' for x in _lines(ls))
    cls = 'k-ch' + (' k-ch--one' if one_line else '')
    h = (f'<h2 class="{cls}" id="{sid}-h" data-a data-m="chap"><span class="k-ch-ko" data-l="ko">{m(ko)}</span>'
         f'<span class="k-ch-en" data-l="en" lang="en">{m(en)}</span></h2>')
    ld = lead(lead_pair) if lead_pair else ''
    return f'<section class="k-sec k-chs" id="{sid}" aria-labelledby="{sid}-h"><div class="k-in" data-lk>{h}{ld}</div></section>'


def lead(pair):
    """Lead paragraph in the body column (lines rise into focus). pair: (ko, en)."""
    return f'<div class="k-leadw" data-a data-m="lead">{t(pair[0], pair[1], "p", "k-lead")}</div>'


def prose(paras, cls=''):
    """Reading paragraphs (Noto Sans KR 16.5 / Archivo 16, 36em). paras: [(ko, en), ...]."""
    return f'<div class="k-prose{" " + cls if cls else ""}" data-a>' + ''.join(t(k, en, 'p') for k, en in paras) + '</div>'


def bullets(ko_list, en_list):
    """List with short marks in the page's (or the parent's) deep tone."""
    return (f'<ul class="k-bul" data-l="ko">{"".join(f"<li>{x}</li>" for x in ko_list)}</ul>'
            f'<ul class="k-bul" data-l="en" lang="en">{"".join(f"<li>{x}</li>" for x in en_list)}</ul>')


def kv(rows):
    """Definition rows on hairlines (address, email, affiliation). rows: [(label html or (ko, en), value html), ...]."""
    return '<dl class="k-kv" data-a>' + ''.join(f'<dt>{_h(a)}</dt><dd>{b}</dd>' for a, b in rows) + '</dl>'


def ruled(items, cols=2, m2=False):
    """Ruled columns: each opened by a hairline that is drawn in, an h3 in the display face, the text.
    items: [(h3 html or (ko, en), body html), ...]. cols 1-4 (one column at 320; m2=True keeps two at 320)."""
    out = f'<div class="k-cols k-c{cols}{" k-m2" if m2 else ""}" data-a>'
    for h, b in items:
        out += (f'<div class="k-col"><i class="k-rule" aria-hidden="true"></i><h3 class="k-h3" data-ai>{_h(h)}</h3>'
                f'<div class="k-d" data-ai>{b}</div></div>')
    return out + '</div>'


def areas(items=AREAS):
    """The four research areas as ruled columns (2 x 2)."""
    return ruled([((a['ko'], a['en']), t(a['d_ko'], a['d_en'], 'p')) for a in items], 2)


def plate(src, alt=('', ''), w=1600, h=1000, href='', srcset='', sizes='(max-width: 760px) 100vw, 480px', ratio=1.6, inset=.06):
    """A figure or diagram as a sheet in a hairline frame of fixed ratio (16:10): the image keeps its own ratio w/h,
    fitted inside with a 6% margin, never cropped. It is cut open like a portrait when its block appears.
    href: the full-size original (new tab, zoom cursor)."""
    r = w / h
    iw = min(1 - 2 * inset, (1 - 2 * inset) / ratio * r)
    ih = iw / r * ratio
    st = f'left:{(1 - iw) / 2 * 100:.2f}%;top:{(1 - ih) / 2 * 100:.2f}%;width:{iw * 100:.2f}%;height:{ih * 100:.2f}%'
    im = img(src, alt, w, h, 'k-im', srcset=srcset, sizes=sizes, attrs=f'style="{st}" decoding="async"')
    pa = f' style="--pr:{ratio}"' if ratio != 1.6 else ''
    inner = f'<span class="k-pp">{im}</span><i class="k-cut" aria-hidden="true"></i>'
    if href:
        alt = (alt, alt) if isinstance(alt, str) else alt
        return (f'<a class="k-plate k-ph" href="{href}" target="_blank" rel="noopener"{pa} aria-label="{e(alt[0])}: 원본 크기로 보기 (새 창)" '
                f'data-aria-en="{e(alt[1])}: full size (new tab)">{inner}</a>')
    return f'<span class="k-plate k-ph"{pa}>{inner}</span>'


def fig_cols(items, cols=2, m2=False):
    """ruled() with a figure: hairline, plate, h3, text. items: [(plate html, h3 html or (ko, en), body html), ...]."""
    out = f'<div class="k-cols k-figs k-c{cols}{" k-m2" if m2 else ""}" data-a>'
    for fg, h, b in items:
        out += (f'<div class="k-col"><i class="k-rule" aria-hidden="true"></i><div class="k-fg">{fg}</div>'
                f'<h3 class="k-h3" data-ai>{_h(h)}</h3><div class="k-d" data-ai>{b}</div></div>')
    return out + '</div>'


def record(items, links=None):
    """The record on counter wheels (the Home hero's numbers, for inner pages): figures with labels on a hairline.
    items: [(n, (ko, en)), ...] (core.OUTCOMES has the four totals); links: optional list of targets per item
    ('#publication' jumps inside the page, a page name links to it, None = no link)."""
    out = '<ul class="k-rec" data-a data-m="rec">'
    for i, (n, lab) in enumerate(items):
        to = links[i] if links and i < len(links) else None
        inner = (f'<b class="k-rec-n"><span class="k-dgw" data-n="{n}" aria-hidden="true">{n}</span><span class="sr">{n}</span></b>'
                 f'<span class="k-rec-l">{t(nw_paren(lab[0]), lab[1])}</span>')
        if to and to.startswith('#'):
            inner = f'<a href="{to}">{inner}</a>'
        elif to:
            inner = link(to, inner)
        out += f'<li data-ai>{inner}</li>'
    return out + '</ul>'


# ================================================================== labs, data centers
def faces(members, limit=6):
    """A strip of small greyscale faces (people.json order) and '+N'; members without a photo get an initial tile."""
    out = '<span class="k-faces" aria-hidden="true">'
    for m in members[:limit]:
        if m.get('photo'):
            out += img(imgur(m['photo'], 'm'), '', 32, 32)
        else:
            ko, en = initials(m['name'])
            out += f'<span class="k-fi">{t(ko, en) if en != ko else ko}</span>'
    if len(members) > limit:
        out += f'<span class="k-fx">+{len(members) - limit}</span>'
    return out + '</span>'


def lab_rows(labs=LABS, with_faces=True, current=None):
    """Linked lab rows: lab name (display), team and member count, description, face strip, arrow. Each row opens with
    a hairline that carries a tab in the lab's tone; hover fills the row with the lab's tint and colours the faces.
    current: a lab key, marked with aria-current and the tint."""
    out = '<ul class="k-labs" data-a>'
    for lb in labs:
        mem = TEAMS.get(lb['key'], {}).get('members', [])
        n = len(mem)
        cnt = t(f'{lb["team_ko"]} · {nw(f"{n}명")}', f'{lb["team_en"]} · {nw(f"{n} members")}') if mem else t(lb['team_ko'], lb['team_en'])
        fc = faces(mem) if (with_faces and mem) else ''
        cur = ' aria-current="page"' if lb['key'] == current else ''
        inner = (f'<i class="k-rule" aria-hidden="true"></i><span class="k-lab-h"><b class="k-lab-n" lang="en">{lb["name"]}</b>'
                 f'<span class="k-lab-t">{cnt}</span></span><span class="k-lab-b"><span class="k-lab-d">{t(lb["d_ko"], lb["d_en"])}</span>{fc}</span>'
                 f'<span class="k-lab-go">{AR}</span>')
        out += f'<li class="k-lab{" is-cur" if cur else ""}" data-ai style="{tone_style(lb["key"])}">' + link(lb['page'], inner, '', cur.strip()) + '</li>'
    return out + '</ul>'


def _dc_logo(dc):
    return img(dc['logo'], (dc['ko'], dc['en']), dc['logo_w'], dc['logo_h'], dc['logo_cls'])


def data_centers(items=DATA_CENTERS, links=True):
    """The two national data centers: the logo is the heading (it carries both names; alt per language), a line of
    text, and a link to the lab that runs it."""
    out = '<div class="k-cols k-c2 k-dcs" data-a>'
    for dc in items:
        lb = LAB[dc['key']]
        out += (f'<div class="k-col k-dc"><i class="k-rule" aria-hidden="true"></i><h3 class="k-dc-h" data-ai><span class="k-dc-logo">{_dc_logo(dc)}</span></h3>'
                f'<p class="k-d" data-ai>{t(dc["d_ko"], dc["d_en"])}</p>'
                + (f'<p class="k-dc-l" data-ai>{more(lb["page"], lb["name"])}</p>' if links else '') + '</div>')
    return out + '</div>'


def dc_box(key, body='', since=None, tone=None):
    """Data-center panel for a lab page, on the lab's tint: the center's logo as the heading, an optional line
    (since=(ko, en)), then body html (prose + bullets)."""
    dc = next(d for d in DATA_CENTERS if d['key'] == key)
    s = f'<p class="k-dcb-s">{tt(since)}</p>' if since else ''
    return (f'<div class="k-dcb" data-a style="{tone_style(tone or key)}"><h3 class="k-dcb-h" data-ai><span class="k-dc-logo">{_dc_logo(dc)}</span></h3>'
            f'{s}<div class="k-dcb-b" data-ai>{body}</div></div>')


def org_chart(current=None, labs=LABS):
    """Organisation chart: the institute and its director at the root, the units (LABS) hanging from one hairline
    that is drawn in. current: a lab key, shown on its tint with '현재 페이지' and not linked. 320: a vertical tree."""
    D = DIRECTOR
    root = (f'<div class="k-org-root" data-ai><p class="k-org-nm">{t(NAME[0] + " · RIHE", NAME[1])}</p>'
            f'<p class="k-org-dr">{t("연구소장 " + D["name_ko"], "Director · " + D["name_en"])}</p></div>')
    out = f'<div class="k-org" data-a>{root}<div class="k-org-b" style="--n:{len(labs)}"><i class="k-rule" aria-hidden="true"></i><ul class="k-org-u">'
    for lb in labs:
        cur = lb['key'] == current
        inner = (f'<span class="k-org-l"><b lang="en">{lb["name"]}</b>{"" if cur else AR}</span>'
                 f'<span class="k-org-tm">{t(lb["team_ko"], lb["team_en"])}</span>'
                 + (f'<span class="k-org-here">{t("현재 페이지", "This page")}</span>' if cur else ''))
        body = f'<span class="k-org-x" aria-current="page">{inner}</span>' if cur else link(lb['page'], inner, 'k-org-x')
        out += f'<li class="k-org-it{" is-cur" if cur else ""}" data-ai style="{tone_style(lb["key"])}">{body}</li>'
    return out + '</ul></div></div>'


# ================================================================== people
def _role_en_part(x):
    en = ROLE_EN.get(x.strip(), x.strip())
    return en.replace(' ', '&nbsp;') if len(en) <= 14 else en


def role_lines(m):
    """(ko, en) role lines for a member card: role parts joined by ' / ', the department on its own line.
    A dict may set role_ko / role_en directly (alumni: '박사 · 2022년 졸업' / 'Ph.D. · 2022')."""
    if m.get('role_ko') or m.get('role_en'):
        return m.get('role_ko', ''), m.get('role_en') or m.get('role_ko', '')
    role, dept = m.get('role', ''), m.get('dept', '')
    ko = ' / '.join(x.strip() for x in role.split('/')) if role else ''
    en = ' / '.join(_role_en_part(x) for x in role.split('/')) if role else ''
    if dept:
        ko = ko + '<br>' + dept if ko else dept
        en = en + '<br>' + role_en(dept) if en else role_en(dept)
    return ko, en


def _name(name):
    ko, en = name_pair(name)
    return t(ko, en) if en != ko else f'<span{lang_attr(ko)}>{ko}</span>'


def _portrait(src, w=640, h=800, alt=''):
    return (f'<div class="k-ph"><div class="k-pp">{img(src, alt, w, h, "k-im", attrs="decoding=\"async\"")}</div>'
            f'<i class="k-cut" aria-hidden="true"></i></div>')


def member(m, size='m'):
    """One portrait card: 4:5 portrait cut open from an ink line through its middle (or an initial tile on the
    team's tint), name, role lines. size 'l' | 'm' | 's' (see people_grid)."""
    if m.get('photo'):
        ph = _portrait(imgur(m['photo'], 'm' if size == 's' else 'l'), 640 if size != 's' else 320, 800 if size != 's' else 400)
    else:
        ko, en = initials(m['name'])
        ph = (f'<div class="k-ph k-ph--ini"><span class="k-ini" aria-hidden="true">{t(ko, en) if en != ko else ko}</span>'
              f'<i class="k-cut" aria-hidden="true"></i></div>')
    rk, re_ = role_lines(m)
    rl = f'<p class="k-role">{t(rk, re_)}</p>' if rk else ''
    return f'<li class="k-mem">{ph}<div class="k-mt" data-ai><p class="k-nm">{_name(m["name"])}</p>{rl}</div></li>'


def people_grid(members, size='m', tone=None):
    """Portrait grid. size 'l': 3 columns (faculty; at 320 a list with 112 px portraits; the portraits drift a little
    against the page on desktop); 'm': 6 columns on desktop, 3 at 320 (teams); 's': 6 columns of small cards, at 320 a
    list with 64 px portraits (alumni). members: people.json dicts (name, role, dept, photo) or dicts with role_ko /
    role_en. tone: a TONES key for the initial tiles (default: the page's tone)."""
    ts = f' style="{tone_style(tone)}"' if tone else ''
    return f'<ul class="k-ppl k-ppl--{size}" data-a{ts}>' + ''.join(member(m, size) for m in members) + '</ul>'


def team_heading(key):
    """(heading html, note html) for a people.json team: a lab's name (Latin, both languages) with its team name and
    count under it, or the team's KO/EN name with its count."""
    _, ko, en = TEAM_META[key]
    n = len(TEAMS[key]['members'])
    lb = LAB.get(key)
    if lb:
        return _h(lb['name']), t(f'{lb["team_ko"]} · {nw(f"{n}명")}', f'{lb["team_en"]} · {nw(f"{n} members")}')
    return t(ko, en), t(f'{n}명', f'{n} members')


def team_sec(key, members=None, size=None, link_lab=True):
    """A People-page team section: the team heading (lab tone tab, count note, a link to the lab page for the four
    labs) and its portrait grid. size: 'l' for the faculty by default, else 'm'."""
    members = TEAMS[key]['members'] if members is None else members
    h, note = team_heading(key)
    lb = LAB.get(key)
    aside = more(lb['page'], lb['name'] + ' 소개', 'About ' + lb['name']) if (lb and link_lab) else ''
    size = size or ('l' if key == 'faculty' else 'm')
    return sec(h, people_grid(members, size, TEAM_TONE.get(key)), key, note=note, aside=aside, tone=TEAM_TONE.get(key), cls='k-team')


def jump_nav(items, label=('이 페이지의 구성', 'On this page')):
    """In-page jump links (page_hero(extra=...)). items: [(section id, label html or (ko, en), tone key or None,
    count or None), ...]. A plain #fragment does not scroll the Wix page; the runtime scrolls with scrollIntoView."""
    out = f'<nav class="k-jump" aria-label="{e(label[0])}" data-aria-en="{e(label[1])}"><ul>'
    for sid, lab, tone, n in items:
        mk = mark(tone) if tone else ''
        cnt = f'<span class="k-jn-c">{n}<span class="sr">{t("명", " members")}</span></span>' if n is not None else ''
        out += f'<li><a href="#{sid}">{mk}<span class="k-jn-l">{_h(lab)}</span>{cnt}</a></li>'
    return out + '</ul></nav>'


def feature(photo, name, role, lines=None, quote=None, email=None, alt=None):
    """A person: 4:5 portrait cut open, an optional quote, the name and role, credentials, email.
    name, role, quote: (ko, en); lines: (ko_list, en_list). At 320 the portrait (112 px) sits beside the name."""
    alt = alt or (f'{name[0]} {role[0]} 사진', f'Portrait of {role[1]} {name[1]}')
    if photo:
        pic = _portrait(photo, 640, 800, alt)
    else:
        pic = f'<div class="k-ph k-ph--ini"><span class="k-ini" role="img" aria-label="{e(name[0])}">{tt(initials(name[0]))}</span><i class="k-cut" aria-hidden="true"></i></div>'
    q = f'<blockquote class="k-ft-q" data-ai>{t(quote[0], quote[1], "p")}</blockquote>' if quote else ''
    cv = ''
    if lines:
        cv += (f'<ul data-l="ko">{"".join(f"<li>{x}</li>" for x in lines[0])}</ul>'
               f'<ul data-l="en" lang="en">{"".join(f"<li>{x}</li>" for x in lines[1])}</ul>')
    if email:
        cv += mail(email)
    nm = t(name[0], name[1]) if name[1] != name[0] else f'<span{lang_attr(name[0])}>{name[0]}</span>'
    who = f'<p class="k-ft-nm">{nm}<span class="k-ft-rl">{t(role[0], role[1])}</span></p>'
    return (f'<div class="k-ft{" has-q" if quote else ""}" data-a><div class="k-ft-pic">{pic}</div>{q}'
            f'<div class="k-ft-who" data-ai>{who}</div><div class="k-ft-cv" data-ai>{cv}</div></div>')


def director(short_en=True, quote=True):
    """The director (DIRECTOR). Home: short EN credentials and the greeting; About: short_en=False, quote=False."""
    D = DIRECTOR
    return feature(imgur(D['photo'], 'l'), (D['name_ko'], D['name_en']), (D['role_ko'], D['role_en']),
                   (D['lines_ko'], D['lines_en_short'] if short_en else D['lines_en']),
                   (D['greeting_ko'], D['greeting_en']) if quote else None, D['email'])


def quote(text, cite=None, photo=None):
    """Pull quote at reading size (Noto Sans KR 500, the opening mark hung in the margin) with a cite line led by a
    short umber mark; photo: a small face beside the cite. text, cite: (ko, en)."""
    fc = img(imgur(photo, 'm'), '', 36, 36, 'k-pq-face') if photo else ''
    c = f'<figcaption class="k-pq-by" data-ai>{fc}<span>{tt(cite)}</span></figcaption>' if cite else ''
    return f'<figure class="k-pq" data-a><blockquote data-ai>{tt(text, "p")}</blockquote>{c}</figure>'


def box(body, media='', cls='', tone=None):
    """A panel: on a lab's tint (tone) or in a hairline frame. media: a badge or logo at the left (multiplied into the
    tint), body at the right; at 320 the media sits above, smaller."""
    ts = f' style="{tone_style(tone)}"' if tone else ''
    c = 'k-box' + (' k-box--tone' if tone else '') + (' k-bx' if media else '') + (' ' + cls if cls else '')
    if not media:
        return f'<div class="{c}" data-a{ts}>{body}</div>'
    return f'<div class="{c}" data-a{ts}><div class="k-bx-m">{media}</div><div class="k-bx-b">{body}</div></div>'


LOGO_AREA = 5600     # px²: the visual area every partner logo gets (logos() with sizes)


def _logo(s, a, o):
    w, h = o['w'], o['h']
    ct, cr, cb, cl = o.get('crop', (0, 0, 0, 0))
    fw, fh = 1 - cl - cr, 1 - ct - cb
    r = (w * fw) / (h * fh)
    H = max(20, min(o.get('max_h', 58), math.sqrt(o.get('area', LOGO_AREA) / r)))
    st = (f'left:{-cl / fw * 100:.2f}%;top:{-ct / fh * 100:.2f}%;width:{100 / fw:.2f}%;height:{100 / fh:.2f}%'
          + (';' + o['style'] if o.get('style') else ''))
    im = img(s, a, w, h, attrs='style="' + st + '"')
    return f'<span class="k-lg" style="--lw:{H * r:.1f};aspect-ratio:{r:.4f}">{im}</span>'


def logos(items):
    """Partner logos on a hairline grid, 4 columns (2 at 320). items: [(src, alt), ...] or (src, alt, opts) with
    opts = dict(w, h: the file's pixel size; crop=(top, right, bottom, left) fractions of built-in whitespace;
    style: extra css for the img). With opts every logo gets the same visual area (LOGO_AREA)."""
    out = '<ul class="k-logos" data-a>'
    for it in items:
        s, a = it[0], it[1]
        inner = _logo(s, a, it[2]) if len(it) > 2 and it[2] else img(s, a)
        out += f'<li data-ai>{inner}</li>'
    return out + '</ul>'


def map_embed(src, title, link_href='', link_label=('지도에서 크게 보기', 'Open in Google Maps')):
    """Google Maps (output=embed) in a 2:1 hairline frame (4:3 at 320), lazy, a KO/EN accessible name; link_href:
    an external link under it. The frame keeps its height whether or not the map loads."""
    title = (title, title) if isinstance(title, str) else title
    fr = (f'<div class="k-map" data-a><span class="k-map-ph" aria-hidden="true">Google Maps</span><iframe src="{src}" title="{e(title[0])}" '
          f'aria-label="{e(title[0])}" data-aria-en="{e(title[1])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')
    lk = f'<p class="k-map-l" data-a>{more(link_href, link_label[0], link_label[1], external=True)}</p>' if link_href else ''
    return fr + lk


def contact_rows(items):
    """Team contacts as mailto rows on the lab-row pattern: lab name and team, the contact person with a small face,
    the email; tab and hover tint in the lab's tone.
    items: [dict(key=lab key, name='Basic Lab', team=(ko, en), person=(ko, en), email='...', photo=''), ...]."""
    out = '<ul class="k-labs k-ct" data-a>'
    for it in items:
        fc = img(imgur(it['photo'], 'm'), '', 40, 40) if it.get('photo') else ''
        inner = (f'<i class="k-rule" aria-hidden="true"></i><span class="k-lab-h"><b class="k-lab-n" lang="en">{it["name"]}</b>'
                 f'<span class="k-lab-t">{tt(it["team"])}</span></span><span class="k-lab-b k-ct-who">{fc}<span><span class="k-ct-p">{tt(it["person"])}</span>'
                 f'<span class="k-ct-e">{it["email"]}</span></span></span><span class="k-lab-go">{AR}</span>')
        out += f'<li class="k-lab" data-ai style="{tone_style(it["key"])}"><a href="mailto:{it["email"]}">{inner}</a></li>'
    return out + '</ul>'


# ================================================================== lists (publications, reports, patents)
EMPTY = t(*UI['none'])
LIST_KINDS = ('pub', 'report', 'patent')
DEFAULT_FILTERS = {'pub': ('team', 'year'), 'report': ('year',), 'patent': ('status',)}
REEL_NOTE = {'pub': ('눈금 하나가 논문 한 편입니다.', 'One tick is one article.'),           # round-2 copy (tools/pages_v2/research.py)
             'report': ('눈금 하나가 발표 한 건입니다.', 'One tick is one presentation.'),
             'patent': ('출원·등록 건을 모두 포함합니다.', 'Includes filed and granted patents. Titles are listed in Korean.')}
COUNTRIES = ('대한민국', '미국', '중국', '유럽')


def _list_items(kind, items):
    out = []
    for i, d in enumerate(items):
        r = {'i': i}
        if kind == 'patent':
            r.update(status=d['status'], country=d.get('country', ''), title=d['title'])
        else:
            r.update(year=d['year'], title=d['title'], authors=d['authors'])
            if kind == 'pub':
                r.update(team=d.get('team', ''), journal=d['journal'])
            else:
                r.update(event=d['event'])
        out.append(r)
    return out


def _list_row(kind, d, show_team):
    if kind == 'patent':
        st = tt(UI.get(d['status'], (d['status'], d['status'])))
        co = tt(UI.get(d['country'], (d['country'], d['country']))) if d.get('country') else ''
        return (f'<li class="k-row k-row--pt" data-i="{d["i"]}"><span class="k-yr k-st">{st}</span><div class="k-tx">'
                f'<p class="k-ti" lang="ko">{e(d["title"])}</p></div><span class="k-tm">{co}</span></li>')
    s = d['event'] if kind == 'report' else d['journal']
    tm = ''
    if kind == 'pub' and show_team and d.get('team') in TEAM_LABEL:
        tm = mark(d['team']) + tt(TEAM_LABEL[d['team']])
    return (f'<li class="k-row" data-i="{d["i"]}"><span class="k-yr">{d["year"]}</span><div class="k-tx">'
            f'<p class="k-ti"{lang_attr(d["title"])}>{e(d["title"])}</p><p class="k-au"{lang_attr(d["authors"])}>{e(d["authors"])}</p>'
            f'<p class="k-jn"{lang_attr(s)}>{e(s)}</p></div><span class="k-tm">{tm}</span></li>')


def _hit(d, f):
    for k, v in f.items():
        if v == 'all':
            continue
        if v.startswith('~'):
            if not int(d[k]) <= int(v[1:]):
                return False
        elif str(d[k]) != v:
            return False
    return True


def _filter_opts(kind, key, items):
    if key == 'team':
        return [(k, tt(TEAM_LABEL[k])) for k in TEAM_LABEL if any(d.get('team') == k for d in items)]
    if key == 'year':
        return [(y, f'<span class="k-num">{y}</span>') for y in core.pub_years(items)]
    if key == 'status':
        return [(s, tt(UI[s])) for s in ('등록', '출원') if any(d.get('status') == s for d in items)]
    if key == 'country':
        cs = [c for c in COUNTRIES if any(d.get('country') == c for d in items)]
        cs += sorted({d.get('country') for d in items if d.get('country') and d.get('country') not in cs})
        return [(c, tt(UI.get(c, (c, c)))) for c in cs]
    raise ValueError(f'unknown list filter {key!r}')


def _list_parts(kind, items, filters, per_page, sid):
    if kind not in LIST_KINDS:
        raise ValueError(f'kind must be one of {LIST_KINDS}')
    filters = DEFAULT_FILTERS[kind] if filters is None else tuple(filters)
    data = _list_items(kind, items)
    groups, keys = [], []
    for k in filters:
        opts = _filter_opts(kind, k, data)
        if len(opts) >= 2:
            groups.append((k, opts))
            keys.append(k)
    show_team = 'team' in keys
    ctl = ''
    for k, opts in groups:
        vals = [('all', tt(UI['all']))] + opts
        btns = ''.join(f'<button type="button" data-k="{k}" data-v="{v}" aria-pressed="{"true" if v == "all" else "false"}">'
                       f'<span class="k-bl">{lab}</span> <span class="k-bc">{sum(1 for d in data if _hit(d, {k: v}))}</span></button>' for v, lab in vals)
        ctl += (f'<div class="k-f k-f--{k}" role="group" aria-label="{UI[k][0]}" data-aria-en="{UI[k][1]}">'
                f'<p class="k-fl" aria-hidden="true">{tt(UI[k])}</p><div class="k-fb">{btns}<i class="k-ind" aria-hidden="true"></i></div></div>')
    n = len(data)
    pages = max(1, -(-n // per_page))
    reel = ''.join(f'<i class="on" style="--d:{i * 2}"></i>' for i in range(n))
    ys = sorted({d['year'] for d in data if d.get('year')}, reverse=True)
    ylab = f'<p class="k-reel-y" aria-hidden="true"><span>{ys[0]}</span><span>{ys[-1]}</span></p>' if len(ys) > 1 else ''
    ctl += (f'<p class="k-tally"><span data-n>{t(f"<b class=\"k-cn\">{n}</b>건", f"<b class=\"k-cn\">{n}</b> items")}</span></p>'
            f'<div class="k-reel" data-ticks aria-hidden="true">{reel}</div>{ylab}')
    first = ''.join(_list_row(kind, d, show_team) for d in data[:per_page])
    pager = (f'<div class="k-pg"><button type="button" data-p="-1" aria-label="{UI["prev"][0]}" data-aria-en="{UI["prev"][1]}" disabled>{CH_L}</button>'
             f'<span class="k-pi"><span data-pi>1 / {pages}</span></span>'
             f'<button type="button" data-p="1" aria-label="{UI["next"][0]}" data-aria-en="{UI["next"][1]}"{" disabled" if pages < 2 else ""}>{CH_R}</button></div>')
    payload = dict(kind=kind, size=per_page, team=show_team, items=data,
                   teams={k: list(v) for k, v in TEAM_LABEL.items()}, tones={k: TEAM_TONE.get(k, 'collab') for k in TEAM_LABEL},
                   status={k: list(UI[k]) for k in ('등록', '출원')}, country={c: list(UI.get(c, (c, c))) for c in COUNTRIES},
                   empty=f'<li class="k-row k-row--e">{EMPTY}</li>')
    js = json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')
    return ctl, first, pager, f'<script type="application/json" class="k-ls-data">{js}</script>'


def list_sec(h, kind, items, sid, note='', filters=None, per_page=10, aside='', foot='', tone=None):
    """A whole list section (C2's publication list, generalised): heading, note and the controls in the heading column
    (filters with a count on every option, the result count, the reel: one frame per item, newest first, the matching
    ones lit and the page on screen in umber), the rows and the pager that follows them in the body column. Paging and
    filtering never change the page height (RIHE.list reserves the tallest page; the spare height sits after the pager).
    kind: 'pub' | 'report' | 'patent'. items: from data/*.json (filter them first for a lab page).
    filters: default pub ('team', 'year'), report ('year',), patent ('status',); patents can add 'country'. A filter
    with fewer than two options is left out. aside: html under the controls; foot: html under the pager."""
    ctl, first, pager, data = _list_parts(kind, items, filters, per_page, sid)
    hid = f'{sid}-h'
    n = f'<p class="k-note">{_h(note)}</p>' if note else ''
    a = f'<div class="k-aside">{aside}</div>' if aside else ''
    ft = f'<div class="k-ls-foot">{foot}</div>' if foot else ''
    c = 'k-sec k-lsec' + (' k-sec--tone' if tone else '')
    ts = f' style="{tone_style(tone)}"' if tone else ''
    return (f'<section class="{c}" id="{sid}" aria-labelledby="{hid}" data-list{ts}><div class="k-in" data-lk>'
            f'<i class="k-ln" aria-hidden="true" data-a data-m="ln"></i>'
            f'<div class="k-sh" data-a data-m="head"><h2 class="k-h" id="{hid}"><span class="k-hm"><span class="k-hl">{_h(h)}</span></span></h2>{n}'
            f'<div class="k-ctl" data-a data-m="ctl" data-lk>{ctl}</div>{a}</div>'
            f'<div class="k-lw" data-a data-m="list"><i class="k-top" aria-hidden="true"></i><ol class="k-list" data-items>{first}</ol>{pager}{ft}</div>'
            f'{data}</div></section>')


def listing(kind, items, filters=None, per_page=10, sid=''):
    """The same list stacked in one column (controls above the rows), for a body column of any section."""
    ctl, first, pager, data = _list_parts(kind, items, filters, per_page, sid)
    i = f' id="{sid}"' if sid else ''
    return (f'<div class="k-ls"{i} data-list><div class="k-ctl" data-a data-m="ctl" data-lk>{ctl}</div>'
            f'<div class="k-lw" data-a data-m="list"><i class="k-top" aria-hidden="true"></i><ol class="k-list" data-items>{first}</ol>{pager}</div>{data}</div>')


# ================================================================== video
def _vid_items(videos):
    out = '<ol class="k-plist">'
    for i, v in enumerate(videos):
        meta = v['duration'] + (f' · {v["date"]}' if v.get('date') else '')
        out += (f'<li><button type="button" aria-current="{"true" if i == 0 else "false"}" data-src="{v["src"]}" data-poster="{wix_poster(v["poster"])}">'
                f'{img(wix_poster(v["thumb"], 320, 180), "", 96, 54)}'
                f'<span><span class="k-pt">{t(v["title_ko"], v["title_en"])}</span><span class="k-pm">{meta}</span></span></button></li>')
    return out + '</ol>'


def _vid_screen(videos):
    v = videos[0]
    meta = v['duration'] + (f' · {v["date"]}' if v.get('date') else '')
    return (f'<div class="k-scr">{img(wix_poster(v["poster"]), "", 1280, 720, "k-poster")}'
            f'<button type="button" class="k-play" aria-label="재생: {e(v["title_ko"])}" data-aria-en="Play: {e(v["title_en"])}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z"/></svg></button></div>'
            f'<p class="k-now"><span class="k-now-t">{t(v["title_ko"], v["title_en"])}</span><span class="k-now-m">{meta}</span></p>')


def videos_sec(h=None, videos=None, sid='videos', note=''):
    """Video section: heading and playlist in the heading column, the 16:9 player in the body column (320: heading,
    player, playlist). From data/videos.json. Plays only on click (preload metadata, native controls); the box height
    never changes."""
    videos = videos or VIDEOS
    h = h or ('영상', 'Videos')
    hid = f'{sid}-h'
    n = f'<p class="k-note">{_h(note)}</p>' if note else ''
    return (f'<!-- 영상: data/videos.json에서 만들어집니다. -->'
            f'<section class="k-sec k-vid" id="{sid}" aria-labelledby="{hid}" data-player><div class="k-in" data-lk>'
            f'<i class="k-ln" aria-hidden="true" data-a data-m="ln"></i>'
            f'<div class="k-sh" data-a data-m="head"><h2 class="k-h" id="{hid}"><span class="k-hm"><span class="k-hl">{_h(h)}</span></span></h2>{n}</div>'
            f'<div class="k-vl" data-a>{_vid_items(videos)}</div><div class="k-sb k-vs" data-a>{_vid_screen(videos)}</div></div></section>')


def video_player(videos=None):
    """The player and its playlist stacked, for any body column."""
    videos = videos or VIDEOS
    return f'<div class="k-vstack" data-player data-a>{_vid_screen(videos)}{_vid_items(videos)}</div>'


# ================================================================== gallery
def _photo_alt(p):
    return (p.get('alt_ko') or p['caption_ko'], p.get('alt_en') or p['caption_en'])


def _cap_year(p):
    """Year after a caption, left out when both captions already contain it."""
    y = str(p.get('year', '') or '')
    if not y or (y in p.get('caption_ko', '') and y in p.get('caption_en', '')):
        return ''
    return f'<span class="k-cy">{y}</span>'


def _photo_frame(p, cls='', sizes='(max-width: 760px) 50vw, 420px'):
    r = p['width'] / p['height']
    src = wix(p['media'], p['file'], 600, 600, 'fit', 80)
    mid = wix(p['media'], p['file'], 1200, 1200, 'fit', 85)
    im = img(src, '', 600, round(600 / r), 'k-im', srcset=f'{src} 600w, {mid} 1200w', sizes=sizes, attrs='decoding="async"')
    return f'<span class="k-pp">{im}</span><i class="k-cut" aria-hidden="true"></i>', r


def gallery_teaser(photos=None, h=None, note=None, sid='gallery', rows=(2, 3)):
    """Home / About gallery teaser: a wide section, photos in justified rows (equal heights per row) linking to
    /gallery, each cut open; at 320 the first photo spans the width (3:2), the others sit in pairs (4:3).
    photos: default the first five entries of data/gallery.json."""
    photos = photos or GALLERY[:sum(rows)]
    h = h or ('갤러리', 'Gallery')
    note = note or ('학회와 수상, 그리고 연구소 사람들의 사진을 모았습니다.', 'Conferences, awards and the people of the institute.')
    body, k = '', 0
    for cnt in rows:
        body += '<div class="k-gt-row">'
        for p in photos[k:k + cnt]:
            fr, r = _photo_frame(p, sizes='(max-width: 760px) 50vw, 620px' if k == 0 else '(max-width: 760px) 50vw, 400px')
            body += (f'<figure class="k-gt" style="--r:{r:.4f}">'
                     + link('gallery', f'<span class="k-ph">{fr}</span><figcaption><span class="k-cp">{t(p["caption_ko"], p["caption_en"])}</span>{_cap_year(p)}</figcaption>')
                     + '</figure>')
            k += 1
        body += '</div>'
    body = f'<div class="k-gteaser" data-a>{body}</div>'
    return ('<!-- 사진: data/gallery.json의 앞 다섯 장이 여기에 나옵니다. -->'
            + sec_wide(h, body, sid, note, more('gallery', '갤러리 전체 보기', 'Open the gallery')))


def gallery_grid(photos=None, per_page=12, years=True, live=False):
    """The full gallery (/gallery): year filters (with counts), justified rows (no crop on desktop; two columns at 4:3
    at 320), 12 per page, the pager, and a viewer that opens in place over the grid (absolute, centred in the visible
    band of the tall Wix iframe, never position: fixed). The grid reserves its tallest page, so nothing moves.
    live=True: the baked list can be replaced from Wix page code ({type:'gallery', items:[...]}, handshake
    {type:'ready'}; the Velo code is in tools/pages_v2/gallery.md). Put it in sec_wide()."""
    photos = photos or GALLERY
    ys = sorted({str(p['year']) for p in photos if p.get('year')}, reverse=True)
    tg = ''
    if years and (len(ys) > 1 or live):
        btns = (f'<button type="button" data-k="year" data-v="all" aria-pressed="true"><span class="k-bl">{tt(UI["all"])}</span> <span class="k-bc">{len(photos)}</span></button>'
                + ''.join(f'<button type="button" data-k="year" data-v="{y}" aria-pressed="false"><span class="k-bl"><span class="k-num">{y}</span></span> '
                          f'<span class="k-bc">{sum(1 for p in photos if str(p.get("year")) == y)}</span></button>' for y in ys))
        tg = (f'<div class="k-f k-f--year k-gl-f" role="group" aria-label="{UI["year"][0]}" data-aria-en="{UI["year"][1]}"{"" if len(ys) > 1 else " hidden"}>'
              f'<p class="k-fl" aria-hidden="true">{tt(UI["year"])}</p><div class="k-fb">{btns}<i class="k-ind" aria-hidden="true"></i></div></div>')
    figs = ''
    for i, p in enumerate(photos):
        fr, r = _photo_frame(p)
        full = wix(p['media'], p['file'], 1600, 1600, 'fit', 85)
        alt = _photo_alt(p)
        fr = fr.replace('alt=""', f'alt="{e(alt[0])}"' + (f' data-alt-en="{e(alt[1])}"' if alt[1] != alt[0] else ''), 1)
        hid = ' hidden' if i >= per_page else ''
        figs += (f'<figure class="k-gl-it" style="--r:{r:.4f}" data-year="{p.get("year", "")}" data-full="{full}"{hid}>'
                 f'<button type="button" class="k-gl-open k-ph" aria-label="크게 보기: {e(p["caption_ko"])}" data-aria-en="View larger: {e(p["caption_en"])}">{fr}</button>'
                 f'<figcaption><span class="k-cp">{t(p["caption_ko"], p["caption_en"])}</span>{_cap_year(p)}</figcaption></figure>')
    pages = max(1, math.ceil(len(photos) / per_page))
    pager = (f'<div class="k-pg"{" hidden" if pages < 2 else ""}><button type="button" data-p="-1" aria-label="{UI["prev"][0]}" data-aria-en="{UI["prev"][1]}" disabled>{CH_L}</button>'
             f'<span class="k-pi"><span data-pi>1 / {pages}</span></span>'
             f'<button type="button" data-p="1" aria-label="{UI["next"][0]}" data-aria-en="{UI["next"][1]}"{" disabled" if pages < 2 else ""}>{CH_R}</button></div>')
    viewer = ('<div class="k-gl-view" hidden role="dialog" aria-modal="true" tabindex="-1" aria-label="사진 보기" data-aria-en="Photo viewer">'
              '<div class="k-gl-vbox"><div class="k-gl-vimg"></div><div class="k-gl-vbar"><p class="k-gl-vcap" aria-live="polite"></p><span class="k-gl-vn"></span>'
              f'<button type="button" class="k-gl-prev" aria-label="이전 사진" data-aria-en="Previous photo">{CH_L}</button>'
              f'<button type="button" class="k-gl-next" aria-label="다음 사진" data-aria-en="Next photo">{CH_R}</button>'
              f'<button type="button" class="k-gl-close">{t("닫기", "Close")}</button></div></div></div>')
    return (f'<!-- 사진: data/gallery.json에서 만들어집니다. -->'
            f'<div class="k-gl" data-gallery data-size="{per_page}"{" data-live" if live else ""} data-a>{tg}<div class="k-gl-grid">{figs}</div>{pager}{viewer}</div>')


def gallery_photo(i, pos='50% 40%', pos_m=None):
    """Hero image from data/gallery.json entry i (Wix media, fitted 640/1280 px, never upscaled). pos: the
    object-position on desktop (the frame is wide), pos_m: at 320 (default: pos)."""
    p = GALLERY[i]
    w0, h0 = p['width'], p['height']
    k = min(1, 1280 / max(w0, h0))
    w, h = round(w0 * k), round(h0 * k)
    src = wix(p['media'], p['file'], 1280, 1280, 'fit', 85)
    small = wix(p['media'], p['file'], 640, 640, 'fit', 80)
    return dict(src=src, srcset=f'{small} 640w, {src} 1280w', w=w, h=h, alt=_photo_alt(p), pos=pos, pos_m=pos_m or pos)


# ================================================================== heroes
def home_hero():
    """The Home hero (C2, tools/kit_assets/hero.*): the reel frame on the white sheet, the knockout title, the record
    (core.OUTCOMES on counter wheels), the lead and the link to the lists. Desktop: the frame's left edge cuts the
    title; 320: the photograph full width on top and its bottom edge crosses the title's first line."""
    h = re.sub(r'^\s*<!--.*?-->\s*', '', rd('hero.html'), count=1, flags=re.S)
    inst_en = INST[1].replace(' · ', ' · <span class="nw">', 1) + '</span>'
    ld = t(core.HOME_LEAD[0], core.HOME_LEAD[1], 'p', 'cx-lead', 'data-a')
    nums = '\n      '.join(
        f'<li data-ai><b><span class="cx-n" data-n="{n}" aria-hidden="true">{n}</span><span class="sr">{n}</span></b>'
        f'{t(nw_paren(ko), en)}</li>' for n, (ko, en) in core.OUTCOMES)
    mo = link('research', t('논문·학회 발표·특허 보기', 'Publications, reports and patents')
              + '<svg viewBox="0 0 20 10" aria-hidden="true"><path d="M0 5h18M14 1l4 4-4 4"/></svg>', 'cx-more', 'data-a')
    out = (h.replace('{{inst}}', t(INST[0], inst_en)).replace('{{lead}}', ld).replace('{{nums}}', nums).replace('{{more}}', mo))
    assert '{{' not in out
    return out


# measured 2026-11-09 (tools/KIT.md "metrics"): Archivo 62% 860 caps advance in em (letter-spacing -.004em included);
# Black Han Sans: a syllable .827 em, a space .284 em (letter-spacing -.012em included)
_ADV = {'A': .514, 'B': .488, 'C': .506, 'D': .503, 'E': .454, 'F': .395, 'G': .535, 'H': .506, 'I': .251, 'J': .438, 'K': .503,
        'L': .42, 'M': .69, 'N': .51, 'O': .546, 'P': .476, 'Q': .546, 'R': .5, 'S': .459, 'T': .464, 'U': .496, 'V': .479,
        'W': .715, 'X': .491, 'Y': .476, 'Z': .466, ' ': .109, '&': .549, '·': .2}


def _em_en(s):
    return sum(_ADV.get(c, .5) for c in _plain(s).upper()) or 1


def _em_ko(s):
    s = _plain(s)
    return sum(.827 if _HANGUL.match(c) else .284 if c == ' ' else _ADV.get(c.upper(), .5) for c in s) or 1


def page_hero(title, alt='', lead='', *, image=None, tone='inst', logo=None, inst=INST, extra='', cls=''):
    """The inner-page hero: a frame on the white sheet from the 34% axis to the right margin, opened from an ink cut
    line (drawn, held for a beat, split). The title stands at the frame's left edge and the frame's bottom edge crosses
    its first line: over a photograph (image) the part inside the frame is paper white (a knockout), over a lab tint
    (no image) it is the tone's deep colour; below the edge it is ink. 320: the frame spans the width.
    title: (ko, en) or a Latin string (a lab name). alt, lead: (ko, en) or html. image: gallery_photo(i) or a dict
    (src, w, h, alt=(ko, en), pos, pos_m, srcset). tone: TONES key of the frame (and the knockout) when there is no
    image. logo: dict(src, w, h) or (src, w, h): the lab's logo inside the tint frame instead of a visible title (the
    h1 stays as screen-reader text). inst: the small line under the frame (default the hospital and university).
    extra: html under the lead (buttons, jump_nav(), record())."""
    if isinstance(title, tuple):
        ko_t, en_t = title
        txt = (f'<span class="k-ht" data-l="ko"{lang_attr(ko_t)}>{ko_t}</span><span class="k-ht" data-l="en" lang="en">{en_t}</span>')
        em_ko, em_en = (_em_ko(ko_t) if _HANGUL.search(ko_t) else _em_en(ko_t)), _em_en(en_t)
    else:
        txt = f'<span class="k-ht"{lang_attr(title)}>{title}</span>'
        em_ko = em_en = _em_ko(title) if _HANGUL.search(title) else _em_en(title)
    if isinstance(logo, tuple):
        logo = dict(src=logo[0], w=logo[1], h=logo[2])
    kind = 'photo' if image else 'logo' if logo else 'tone'
    st = f'{tone_style(tone)};--em-ko:{em_ko:.3f};--em-en:{em_en:.3f}'
    if image:
        st += f';--fp:{image.get("pos", "50% 40%")};--fpm:{image.get("pos_m", image.get("pos", "50% 40%"))}'
        im = img(image['src'], image.get('alt', ('', '')), image.get('w'), image.get('h'), 'k-himg', lazy=False,
                 srcset=image.get('srcset', ''), sizes='(max-width: 760px) 100vw, 66vw', attrs='fetchpriority="high" decoding="async"')
        media = f'<div class="k-hpar"><div class="k-hmed">{im}</div></div><div class="k-hsh" aria-hidden="true"></div>'
    elif logo:
        lg = img(logo['src'], '', logo['w'], logo['h'], 'k-hlogo', lazy=False, attrs='decoding="async"')
        media = f'<div class="k-hlg">{lg}</div>'
    else:
        media = ''
    sr = ' sr' if logo else ''
    copy = '' if logo else f'<p class="k-hw" aria-hidden="true" data-a data-m="hp">{txt}</p>'
    low = ''
    if alt:
        low += f'<p class="k-halt">{_h(alt)}</p>'
    if lead:
        low += f'<div class="k-hlead">{t(lead[0], lead[1], "p") if isinstance(lead, tuple) else lead}</div>'
    if extra:
        low += f'<div class="k-hx">{extra}</div>'
    return (f'<header class="k-hero k-hero--{kind}{" " + cls if cls else ""}" style="{st}">'
            f'<div class="k-hf k-hf--{kind}" data-a data-m="hp">{media}{copy}</div>'
            f'<i class="k-he k-he-t" aria-hidden="true"></i><i class="k-he k-he-b" aria-hidden="true"></i>'
            f'<div class="k-in k-hin" data-lk><h1 class="k-hk{sr}" data-a data-m="hp">{txt}</h1>'
            f'<p class="k-hinst" data-a data-m="hp">{_h(inst)}</p>'
            + (f'<div class="k-hlow" data-a data-m="hp">{low}</div>' if low else '') + '</div></header>')


# ================================================================== lab page (Basic Lab, Hearing Lab, HeAD Lab)
def _members_link(key):
    n = len(TEAMS.get(key, {}).get('members', []))
    if not n:
        return ''
    name = LAB[key]['name']
    return more('people', f'{name} 구성원 {n}명', f'{name}: {n} members')


def lab_page(key, *, tagline, intro, mission, subjects, manager, alt=None, logo=None, image=None, dc=None, alumni=(),
             comment=''):
    """A whole lab page (round 2's tools/pages_v2/_lab.py, in C2). key: 'basic' | 'hearing' | 'head'.
    tagline, intro: (ko, en). alt: (ko, en) under the title (default the team name). mission: [((ko, en) h3, ko, en)];
    subjects: [(title_ko, title_en, ko, en)]; manager: dict(photo, name=(ko, en), lines=(ko_list, en_list)).
    logo: (src, w, h) shown in the hero instead of the title (HeAD Lab). image: a hero photo (gallery_photo(i)).
    dc: dc_box() html. alumni: [(name, photo, role_ko, role_en)], newest first (section left out when empty).
    Order: hero > About > Data center > Mission & Vision > Research subjects > Organization > Director & Manager >
    Publication (the lab's list, year filter, link to the conference reports on /project) > Alumni.
    Every section carries the lab's tone."""
    lb = LAB[key]
    name = lb['name']
    hero = page_hero(name, alt or (lb['team_ko'], lb['team_en']), tagline, image=image, tone=key, logo=logo)
    body = hero + '<main>'
    body += sec(('연구실 소개', 'About the lab'), prose([intro]), 'about', tone=key)
    if dc:
        body += sec(('데이터센터', 'Data center'), dc, 'data-center', tone=key)
    body += sec(('미션 · 비전', 'Mission &amp; Vision'), ruled([(h, t(ko, en, 'p')) for h, ko, en in mission], len(mission)), 'mission', tone=key)
    body += sec(('연구 주제', 'Research subjects'), ruled([((a, b) if a != b else a, t(c, d, 'p')) for a, b, c, d in subjects], 2), 'subjects', tone=key)
    body += sec(('조직', 'Organization'), org_chart(current=key), 'organization', tone=key)
    people = (director(short_en=False, quote=False)
              + feature(imgur(manager['photo'], 'l'), manager['name'], ('매니저', 'Manager'), manager['lines'],
                        alt=(f'{manager["name"][0]} 사진', f'Portrait of {manager["name"][1]}')))
    body += sec(('연구소장 · 매니저', 'Director &amp; Manager'), people, 'people', aside=_members_link(key), tone=key)
    pubs = [p for p in PUBS if p.get('team') == key]
    if pubs:
        body += ('<!-- 논문 목록: data/publications.json에서 team 값이 이 연구실인 논문만 보여 줍니다. -->'
                 + list_sec(('논문', 'Publication'), 'pub', pubs, 'publication', filters=('year',),
                            note=(f'{name}의 논문 {len(pubs)}편입니다. 눈금 하나가 논문 한 편입니다.', f'{len(pubs)} articles from {name}. One tick is one article.'),
                            foot=more('/project#report', '학회 발표 목록은 연구 페이지에서 보기', 'Conference reports: Research page'), tone=key))
    if alumni:
        grid = people_grid([{'name': n, 'photo': ph, 'role_ko': '<br>'.join(rk.rsplit(' · ', 1)), 'role_en': re_}
                            for n, ph, rk, re_ in alumni], 's', key)
        body += sec(('졸업생', 'Alumni'), grid, 'alumni', tone=key)
    body += '</main>'
    return page(name, body, tone=key, comment=comment)


# ================================================================== the document
DK_CLASSES = ('k-h', 'k-ch', 'k-h3', 'k-hk', 'k-hw', 'cx-h', 'k-ini', 'k-fi', 'k-org-nm', 'k-dk')   # elements set in Black Han Sans (KO)
ARCHIVO = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..100,400..900&display=swap'
NOTO_FULL = 'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500&display=swap'


def fonts_for(body, full_ko=False):
    """Google Fonts for a page: Black Han Sans with only the glyphs set in the display face (DK_CLASSES), Archivo
    (variable width and weight), Noto Sans KR with only the characters the page contains (text, data, runtime words).
    full_ko=True (a live CMS gallery: captions arrive at runtime): Noto Sans KR by unicode-range slices instead."""
    dsp = core.chars_in(body, classes=DK_CLASSES)
    txt = re.sub(r'<style\b.*?</style>', ' ', body, flags=re.S)
    txt = re.sub(r'<script\b(?![^>]*application/json)[^>]*>.*?</script>', ' ', txt, flags=re.S)
    chars = {c for c in txt if ord(c) > 127 and not c.isspace()} | {chr(i) for i in range(33, 127)} | set('·‘’“”…–건명')
    ko = NOTO_FULL if full_ko else core.gfont('Noto+Sans+KR:wght@400;500', ''.join(sorted(chars)))
    return [core.gfont('Black+Han+Sans', dsp), ARCHIVO, ko]


def page(title, body, tone='inst', comment='', full_ko=None):
    """The whole document (core.page_shell): fonts, the kit's CSS (plus the Home hero's when the body has it), the
    runtime, GSAP from site/vendor, the kit's motion and list scripts. title: plain text for <title> (' · RIHE' is
    added). tone: the page's lab tone (bullets, initial tiles and other marks without their own tone).
    comment: a Korean note for the client in the head comment."""
    home = 'class="cx"' in body
    css = CSS + f'\n:root {{ {tone_style(tone).replace(";", "; ")}; }}\n'
    js = KIT_JS
    if home:
        reel = json.loads(rd('reel.json'))
        hero_js = rd('hero.js')
        assert '/*@REEL@*/null' in hero_js
        css += rd('hero.css')
        js = hero_js.replace('/*@REEL@*/null', json.dumps(reel, separators=(',', ':'))) + '\n' + js
    full = ('data-live' in body) if full_ko is None else full_ko
    note = '이 페이지는 tools/pages/<이름>.py 와 tools/kit.py 로 만듭니다: python3 tools/build.py' + (' · ' + comment if comment else '')
    return core.page_shell(f'{title} · RIHE', body, css=css, js=js, fonts=fonts_for(body, full), vendor=('gsap', 'split', 'ease'),
                           prefix='', robots=core.ROBOTS, lang_toggle=PREVIEW, comment=note)


# ================================================================== CSS
CSS = r"""
/* ================================================================ tokens (DESIGN.md) ================================
   One white sheet: the Wix header, ground and footer are #ffffff, so is every part of the page. Contrast on white:
   ink 19.3, ink-2 8.7, ink-3 5.7, umber 5.9 (the only text accent), amber 2.1 (never text: the selection only).
   Lab tones: --t-* pastel tints for surfaces, --d-* deep tones for text and lines (AA on white and on the tint). */
:root {
  --paper: #ffffff; --ink: #0f0e0c; --ink-2: #4e4b47; --ink-3: #696660;
  --ink-r: rgba(15, 14, 12, .12); --ink-r2: rgba(15, 14, 12, .28);
  --tint: #f1f1ef; --umber: #8a5a0e; --amber: #e3a640;
  --t-inst: #e8ebf2; --d-inst: #2d3f66; --t-basic: #e5efe8; --d-basic: #2c6447; --t-hearing: #e3edf4; --d-hearing: #2c5a77;
  --t-head: #e9e8f5; --d-head: #45458a; --t-audiso: #f6e6dc; --d-audiso: #8a5a0e; --t-collab: #ecebe8; --d-collab: #5b5852;
  --t-admin: #ecebe8; --d-admin: #4e4b47;
  --W: min(100vw, 1640px); --ox: max(0px, calc((100vw - 1640px) / 2)); --m: clamp(28px, 3.75vw, 72px);
  --fx: calc(var(--ox) + var(--W) * .34); --tx: calc(var(--ox) + var(--m)); --gut: clamp(20px, 2.4vw, 40px);
  --c1: calc(var(--W) * .34 - var(--m) - var(--gut));
  --sp: clamp(64px, 6.6vw, 112px);
  --ko: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --lat: 'Archivo', 'Noto Sans KR', 'Helvetica Neue', Arial, sans-serif;
  --dsp: 'Black Han Sans', 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
  --out: cubic-bezier(.16, 1, .3, 1);
}
@media (max-width: 760px) { :root { --m: 16px; --sp: 56px; } }
*, *::before, *::after { box-sizing: border-box; }
html { background: var(--paper); -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--ko); font-size: 16.5px; line-height: 1.8;
  word-break: keep-all; overflow-wrap: break-word; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; overflow-x: hidden; }
[lang="en"] { font-family: var(--lat); }
[lang="ko"] { font-family: var(--ko); }
img { display: block; max-width: 100%; }
a { color: inherit; }
button { font: inherit; color: inherit; }
p, h1, h2, h3, ul, ol, dl, dd, figure, blockquote { margin: 0; }
ul, ol { padding: 0; list-style: none; }
::selection { background: var(--amber); color: var(--ink); }
.nw { white-space: nowrap; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--umber); outline-offset: 3px; }
main { display: block; padding-bottom: clamp(88px, 8.4vw, 140px); }

/* ================================================================ the grid: C2's 34% axis =========================
   The left column ends one gutter before the axis (the Home frame's left edge, 34% of the width); the body column
   starts on it. 320: one column. */
.k-in { position: relative; max-width: 1640px; margin: 0 auto; padding: 0 var(--m); display: grid;
  grid-template-columns: var(--c1) minmax(0, 1fr); column-gap: var(--gut); align-items: start; }
.k-sec { position: relative; padding-top: var(--sp); }
/* the cut line: a 1 px ink rule across the grid that opens every section (drawn in by the script) */
.k-ln { grid-column: 1 / -1; position: relative; display: block; height: 1px; background: var(--ink); transform-origin: 0 50%;
  margin-bottom: clamp(18px, 1.8vw, 28px); }
.k-sec--tone .k-ln::before { content: ""; position: absolute; left: 0; top: -1px; width: 56px; height: 3px; background: var(--td); }
.k-sh { grid-column: 1; min-width: 0; }
.k-sb { grid-column: 2; min-width: 0; }
.k-h { font-weight: 400; color: var(--ink); font-family: var(--dsp); font-size: clamp(28px, 2.5vw, 40px); line-height: 1.12; letter-spacing: -.01em; }
.k-hm { display: block; overflow: hidden; padding: .1em .08em .08em; margin: -.1em -.08em -.08em; }
.k-hl { display: block; margin-left: -.045em; }
.k-hl > span { display: block; }
.k-h [lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: 1.075em; line-height: 1.04; letter-spacing: -.004em; }
.k-hl > [lang="en"] { margin-left: .015em; }
.k-note { margin-top: 14px; max-width: 22em; font-size: 13.5px; line-height: 1.6; color: var(--ink-3); }
.k-note [lang="en"] { line-height: 1.5; }
.k-aside { margin-top: 20px; }
/* wide: heading row (link at its right), the body across both columns */
.k-sec--wide .k-swl { grid-column: 2; grid-row: 2; justify-self: end; align-self: end; }
.k-sec--wide .k-sb { grid-column: 1 / -1; margin-top: clamp(28px, 2.8vw, 44px); }

/* chapter heading (C2 .c-h2): authored lines in masks of one height for both languages */
.k-chs { padding-top: calc(var(--sp) * .9); }
.k-ch { grid-column: 1 / -1; font-weight: 400; color: var(--ink); --hs: clamp(50px, 6.3vw, 104px); font-size: var(--hs); }
.k-ch .m { display: block; height: calc(var(--hs) * 1.04); overflow: hidden; padding: .06em .05em 0; margin: -.06em -.05em 0; }
.k-ch .l { display: block; white-space: nowrap; line-height: calc(var(--hs) * 1.04); }
.k-ch-ko .l { font-family: var(--dsp); font-size: var(--hs); letter-spacing: -.012em; margin-left: -.045em; }
.k-ch-en .l { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: calc(var(--hs) * 1.08); text-transform: uppercase;
  letter-spacing: -.004em; word-spacing: .07em; margin-left: -.03em; }
@media (min-width: 761px) { .k-ch--one { line-height: 0; } .k-ch--one .m { display: inline-block; vertical-align: top; } }
.k-chs .k-leadw { grid-column: 2; margin-top: clamp(24px, 2.6vw, 40px); }
.k-lead { max-width: 35em; font-size: clamp(16.5px, 1.22vw, 18px); line-height: 1.78; color: var(--ink-2); text-wrap: pretty; }
.k-lead[lang="en"] { line-height: 1.62; max-width: 37em; }
.k-sb > .k-leadw + * { margin-top: clamp(28px, 2.6vw, 40px); }

/* ================================================================ text ================================================ */
.k-prose p { max-width: 36em; font-size: 16.5px; line-height: 1.85; color: var(--ink); text-wrap: pretty; }
.k-prose p[lang="en"] { font-size: 16px; line-height: 1.66; max-width: 38em; }
.k-prose p + p { margin-top: 1em; }
.k-bul { display: grid; gap: 8px; margin-top: 20px; }
.k-bul li { position: relative; padding-left: 24px; font-size: 15px; line-height: 1.7; color: var(--ink-2); }
.k-bul[lang="en"] li { line-height: 1.6; }
.k-bul li::before { content: ""; position: absolute; left: 0; top: .8em; width: 12px; height: 2px; background: var(--td, var(--umber)); }
.k-kv { display: grid; grid-template-columns: minmax(88px, 9em) minmax(0, 1fr); column-gap: 24px; }
.k-kv dt, .k-kv dd { padding: 16px 0 17px; border-top: 1px solid var(--ink-r); }
.k-kv dt { font-size: 12.5px; line-height: 1.75; letter-spacing: .02em; color: var(--ink-3); padding-top: 19px; }
.k-kv dd { font-size: 16.5px; line-height: 1.7; color: var(--ink); }
.k-kv dd [lang="en"] { line-height: 1.6; }
.k-kv dd .k-d, .k-kv dd p.k-d { margin-top: 4px; font-size: 13.5px; color: var(--ink-2); }
.k-kv dt:last-of-type, .k-kv dd:last-of-type { border-bottom: 1px solid var(--ink-r); }

/* links */
.k-more { display: inline-flex; align-items: center; gap: 12px; padding: 8px 0; color: var(--ink); text-decoration: none;
  font-size: 15px; line-height: 1.3; font-weight: 500; letter-spacing: .005em; }
.k-mt { padding-bottom: 4px; background: linear-gradient(currentColor, currentColor) 0 100% / 100% 1px no-repeat; transition: background-size .35s var(--out); }
.k-ar { width: 20px; height: 10px; flex: none; fill: none; stroke: var(--umber); stroke-width: 1.5; transition: transform .35s var(--out); }
.k-ar--x { width: 12px; height: 12px; }
.k-more:hover .k-ar, .k-btn:hover .k-ar { transform: translateX(5px); }
.k-more:hover .k-ar--x, .k-btn:hover .k-ar--x { transform: translate(3px, -3px); }
.k-more:hover .k-mt { background-size: 100% 2px; }
.k-btns { display: flex; flex-wrap: wrap; gap: 12px; }
.k-btn { display: inline-flex; align-items: center; gap: 12px; height: 44px; padding: 0 18px; border: 1px solid var(--ink-r2); color: var(--ink);
  text-decoration: none; font-size: 15px; font-weight: 500; transition: background-color .2s ease, color .2s ease, border-color .2s ease, transform .12s ease; }
.k-btn .k-mt { background: none; padding: 0; }
.k-btn:hover { background: var(--ink); border-color: var(--ink); color: var(--paper); }
.k-btn:hover .k-ar { stroke: var(--paper); }
.k-btn:active { transform: scale(.97); }
.k-mail { font-family: var(--lat); font-size: 15px; color: var(--ink); text-decoration: none; background: linear-gradient(var(--umber), var(--umber)) 0 100% / 100% 1px no-repeat; padding-bottom: 2px; }
.k-mail:hover { background-size: 100% 2px; }
.k-mk { display: inline-block; flex: none; width: 8px; height: 8px; background: var(--td); }

/* ================================================================ ruled columns, figures ============================ */
.k-cols { display: grid; grid-template-columns: repeat(var(--c, 2), minmax(0, 1fr)); gap: clamp(40px, 3.6vw, 56px) clamp(24px, 2.4vw, 40px); }
.k-c1 { --c: 1; } .k-c3 { --c: 3; } .k-c4 { --c: 4; }
.k-col { min-width: 0; }
.k-rule { display: block; height: 1px; background: var(--ink-r2); transform-origin: 0 50%; }
.k-h3 { margin-top: 18px; font: 400 clamp(21px, 1.7vw, 26px)/1.25 var(--dsp); letter-spacing: -.008em; color: var(--ink); }
.k-h3 > [lang="en"], .k-h3[lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 820; font-size: 1.1em; line-height: 1.12; letter-spacing: -.002em; }
.k-d { margin-top: 10px; max-width: 32em; font-size: 15px; line-height: 1.75; color: var(--ink-2); }
.k-d [lang="en"], .k-d[lang="en"] { line-height: 1.62; }
.k-figs .k-fg { margin-top: 20px; }
.k-plate { display: block; position: relative; aspect-ratio: var(--pr, 1.6); overflow: hidden; background: var(--paper); }
.k-plate .k-pp { position: absolute; inset: 0; background: var(--paper); }
.k-plate .k-im { position: absolute; max-width: none; object-fit: contain; filter: none; }
a.k-plate { cursor: zoom-in; }
a.k-plate::after { transition: box-shadow .3s ease, opacity .6s ease; }
a.k-plate:hover::after { box-shadow: inset 0 0 0 1px var(--ink); }

/* frames (portraits, plates, photos): a hairline edge, so a picture with a white ground still reads as a frame; the
   cut line through the middle is drawn by the script, the picture opens from it and the line is gone */
.k-ph { position: relative; display: block; overflow: hidden; }
.k-ph::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 0 1px var(--ink-r); pointer-events: none; transition: opacity .6s ease; }
.is-cut .k-ph::after { opacity: 0; transition: none; }
.k-pp { position: absolute; inset: 0; background: var(--tint); }
.k-cut { position: absolute; left: 0; right: 0; top: 50%; height: 1px; margin-top: -.5px; background: var(--ink); transform: scaleX(0); transform-origin: 0 50%; pointer-events: none; }
.k-im { display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 26%; filter: saturate(.88) contrast(.98); transition: filter .7s var(--out), transform .9s var(--out); }

/* ================================================================ the record (counter wheels) ======================== */
.k-rec { display: grid; grid-template-columns: repeat(auto-fit, minmax(96px, 1fr)); column-gap: clamp(12px, 1.4vw, 24px); row-gap: 20px; padding-top: 16px;
  background: linear-gradient(var(--ink-r2), var(--ink-r2)) no-repeat 0 0 / var(--rs, 100%) 1px; max-width: 640px; }
.k-rec a { display: block; text-decoration: none; color: inherit; }
.k-rec-n { display: block; font: 640 clamp(34px, 3vw, 48px)/1 var(--lat); font-stretch: 62%; letter-spacing: -.01em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink); }
.k-dgw { display: block; white-space: nowrap; }
.k-dg { display: inline-block; vertical-align: top; height: 1em; overflow: hidden; }
.k-strip { display: block; }
.k-strip > span { display: block; height: 1em; }
.k-rec-l { display: block; margin-top: 8px; font-size: 12.5px; line-height: 1.4; color: var(--ink-3); }
.k-rec-l [lang="en"] { font-size: 12px; font-stretch: 90%; }
.k-rec a .k-rec-l > span { background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat; transition: background-size .35s var(--out); }
.k-rec a:hover .k-rec-l > span { background-size: 100% 1px; color: var(--ink); }

/* ================================================================ labs, contact rows ================================= */
.k-labs { border-bottom: 1px solid var(--ink-r2); }
.k-lab { position: relative; }
.k-lab > a { position: relative; isolation: isolate; display: grid; grid-template-columns: minmax(0, .82fr) minmax(0, 1fr) 24px; column-gap: clamp(16px, 2vw, 32px);
  align-items: start; padding: 24px 0 26px; text-decoration: none; color: inherit; }
.k-lab .k-rule { position: absolute; left: 0; right: 0; top: 0; }
.k-lab .k-rule::before { content: ""; position: absolute; left: 0; top: -1px; width: 56px; height: 3px; background: var(--td); }
.k-lab > a::before { content: ""; position: absolute; z-index: -1; inset: 1px -16px 0; background: var(--tt); opacity: 0; transition: opacity .35s ease; }
.k-lab > a:hover::before, .k-lab > a:focus-visible::before, .k-lab.is-cur > a::before { opacity: 1; }
.k-lab-n { display: block; font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: clamp(28px, 2.3vw, 38px); line-height: 1.04; letter-spacing: -.004em; color: var(--ink); }
.k-lab-t { display: block; margin-top: 8px; font-size: 13.5px; line-height: 1.5; color: var(--ink-3); }
.k-lab-d { display: block; font-size: 16px; line-height: 1.7; color: var(--ink); }
.k-lab-d [lang="en"] { line-height: 1.58; }
.k-lab-go { justify-self: end; padding-top: 10px; }
.k-lab > a:hover .k-ar { transform: translateX(5px); }
.k-faces { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; margin-top: 14px; }
.k-faces img, .k-fi { width: 32px; height: 32px; object-fit: cover; object-position: 50% 22%; filter: grayscale(1) contrast(1.04); background: var(--tint); transition: filter .5s var(--out); }
.k-fi { display: grid; place-items: center; font: 500 13px/1 var(--ko); color: var(--td, var(--umber)); background: var(--paper); box-shadow: inset 0 0 0 1px var(--ink-r); filter: none; }   /* reading face: the display face makes a small 이 read as OI */
.k-fi [lang="en"] { font-family: var(--lat); font-weight: 640; }
.k-fx { margin-left: 6px; font: 640 13px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); }
.k-lab > a:hover .k-faces img { filter: grayscale(0) saturate(.9); }
.k-ct-who { display: flex; align-items: center; gap: 14px; }
.k-ct-who img { width: 40px; height: 40px; flex: none; object-fit: cover; object-position: 50% 20%; filter: grayscale(1) contrast(1.04); background: var(--tint); }
.k-ct-p { display: block; font-size: 15px; line-height: 1.5; color: var(--ink); }
.k-ct-e { display: block; margin-top: 2px; font-family: var(--lat); font-size: 15px; color: var(--ink); }
.k-ct .k-lab-go { padding-top: 12px; }

/* ================================================================ data centers =============================================== */
.k-dc-h { margin-top: 24px; }
.k-dc-logo { display: flex; align-items: center; height: 40px; }
.k-dc-logo img { width: auto; max-width: none; }
.k-dc-logo .l1 { height: 41.6px; margin-left: -3.7px; }
.k-dc-logo .l2 { height: 62.4px; margin-left: -15.6px; }
.k-dc .k-d { margin-top: 16px; }
.k-dc-l { margin-top: 12px; }
.k-dcb { padding: clamp(24px, 2.6vw, 40px); background: var(--tt, var(--tint)); }
.k-dcb .k-dc-logo { height: 44px; }
.k-dcb .l1 { height: 44px; margin-left: -3.9px; }
.k-dcb .l2 { height: 66px; margin-left: -16.5px; }
.k-dcb-s { margin-top: 14px; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); }
.k-dcb-b { margin-top: 20px; }
.k-dcb .k-prose p { font-size: 15.5px; line-height: 1.8; }
.k-dcb .k-prose p[lang="en"] { font-size: 15px; line-height: 1.62; }

/* ================================================================ organisation chart ===================================== */
.k-org-nm { font: 400 clamp(22px, 1.8vw, 28px)/1.2 var(--dsp); letter-spacing: -.008em; }
.k-org-nm [lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: 1.08em; line-height: 1.08; }
.k-org-dr { margin-top: 4px; font-size: 13.5px; line-height: 1.5; color: var(--ink-3); }
.k-org-b { position: relative; margin-top: 20px; padding-top: 28px; }
.k-org-b::before { content: ""; position: absolute; left: 0; top: 0; width: 1px; height: 28px; background: var(--ink-r2); }
.k-org-b > .k-rule { position: absolute; left: 0; top: 28px; right: calc((100% - (var(--n) - 1) * 16px) / var(--n) - 1px); }
.k-org-u { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); column-gap: 16px; }
.k-org-it { position: relative; padding-top: 20px; }
.k-org-it::before { content: ""; position: absolute; left: 0; top: 0; width: 1px; height: 20px; background: var(--ink-r2); }
.k-org-it.is-cur::before { width: 3px; background: var(--td); }
.k-org-x { display: block; height: 100%; padding: 14px 14px 16px; text-decoration: none; color: inherit; box-shadow: inset 0 0 0 1px var(--ink-r); transition: background-color .3s ease; }
.k-org-it.is-cur .k-org-x { background: var(--tt); box-shadow: none; }
a.k-org-x:hover { background: var(--tt); }
.k-org-l { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.k-org-l b { font-family: var(--lat); font-stretch: 62%; font-weight: 860; font-size: clamp(19px, 1.6vw, 24px); line-height: 1.08; white-space: nowrap; color: var(--ink); }
.k-org-it.is-cur .k-org-l b { color: var(--td); }
a.k-org-x:hover .k-ar { transform: translateX(4px); }
.k-org-tm { display: block; margin-top: 6px; font-size: 13px; line-height: 1.5; color: var(--ink-3); }
.k-org-here { display: block; margin-top: 8px; font-size: 12.5px; line-height: 1.5; font-weight: 500; color: var(--td); }

/* ================================================================ people ================================================ */
.k-ppl { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); column-gap: clamp(12px, 1.2vw, 20px); row-gap: 32px; align-content: start; }
.k-ppl--l { grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: clamp(16px, 1.7vw, 28px); row-gap: 40px; }
.k-mem { min-width: 0; }
.k-mem .k-ph { aspect-ratio: 4 / 5; }
.k-mem .k-pp { top: -5%; bottom: -5%; }
.k-mem:hover .k-im { filter: saturate(1) contrast(1); transform: scale(1.035); }
.k-ini { position: absolute; inset: 0; display: grid; place-items: center; font: 400 clamp(36px, 3.4vw, 56px)/1 var(--dsp); color: var(--td, var(--umber)); background: var(--tt, var(--tint)); }
.k-ini [lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 860; }
.k-mt { margin-top: 12px; }
.k-nm { font-size: 16.5px; line-height: 1.35; font-weight: 500; color: var(--ink); }
.k-nm [lang="en"] { font-weight: 640; letter-spacing: -.006em; }
.k-role { margin-top: 4px; font-size: 12.5px; line-height: 1.46; color: var(--ink-2); }
.k-ppl--l .k-nm { font-size: 18px; }
.k-ppl--l .k-role { font-size: 13.5px; }
.k-ppl--s .k-nm { font-size: 15px; }
.k-ppl--s .k-role { font-size: 12px; }
.k-ppl--s .k-ini { font-size: clamp(28px, 2.4vw, 40px); }
.k-team .k-note { margin-top: 10px; }
/* jump links */
.k-jump ul { display: flex; flex-wrap: wrap; gap: 0 28px; }
.k-jump a { display: inline-flex; align-items: center; gap: 10px; padding: 10px 0; color: var(--ink); text-decoration: none; font-size: 15px; line-height: 1.3; font-weight: 500; }
.k-jn-l { background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat; padding-bottom: 3px; transition: background-size .35s var(--out); }
.k-jump a:hover .k-jn-l { background-size: 100% 1px; }
.k-jn-c { align-self: flex-start; font: 640 11px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); font-variant-numeric: tabular-nums; }
/* person feature */
.k-ft { display: grid; grid-template-columns: clamp(156px, 15vw, 232px) minmax(0, 1fr); grid-template-areas: "pic who" "pic cv"; grid-template-rows: auto 1fr;
  column-gap: clamp(24px, 2.6vw, 44px); align-items: start; }
.k-ft.has-q { grid-template-areas: "pic q" "pic who" "pic cv"; grid-template-rows: auto auto 1fr; }
.k-ft + .k-ft { margin-top: clamp(48px, 4.4vw, 64px); }
.k-ft-pic { grid-area: pic; }
.k-ft-pic .k-ph { aspect-ratio: 4 / 5; }
.k-ft-pic .k-im { object-position: 42% 28%; }
.k-ft-q { grid-area: q; margin-bottom: 28px; max-width: 34em; }
.k-ft-q p { font-size: clamp(16.5px, 1.3vw, 19px); line-height: 1.86; color: var(--ink); text-wrap: pretty; }
.k-ft-q p[lang="en"] { line-height: 1.66; }
.k-ft-who { grid-area: who; }
.k-ft-nm { font-size: 20px; line-height: 1.35; font-weight: 500; color: var(--ink); }
.k-ft-nm [lang="en"] { font-weight: 640; }
.k-ft-rl { margin-left: 12px; font-size: 13.5px; font-weight: 400; color: var(--ink-3); }
.k-ft-cv { grid-area: cv; }
.k-ft-cv ul { margin-top: 10px; display: grid; gap: 2px; font-size: 13.5px; line-height: 1.7; color: var(--ink-2); }
.k-ft-cv ul[lang="en"] { line-height: 1.55; gap: 4px; }
.k-ft-cv .k-mail { display: inline-block; margin-top: 16px; }

/* quote, box, logos, map */
.k-pq blockquote p { font-size: clamp(19px, 1.6vw, 23px); line-height: 1.75; font-weight: 500; color: var(--ink); max-width: 30em; text-indent: -.42em; text-wrap: pretty; }
.k-pq blockquote p[lang="en"] { line-height: 1.55; font-weight: 500; }
.k-pq-by { display: flex; align-items: center; gap: 12px; margin-top: 22px; font-size: 13.5px; color: var(--ink-2); }
.k-pq-by::before { content: ""; width: 14px; height: 2px; flex: none; background: var(--umber); }
.k-pq-face { width: 36px; height: 36px; object-fit: cover; object-position: 50% 20%; filter: grayscale(1) contrast(1.04); }
.k-pq + .k-prose { margin-top: clamp(32px, 3vw, 44px); }
.k-box { padding: clamp(22px, 2.4vw, 36px); box-shadow: inset 0 0 0 1px var(--ink-r); }
.k-box--tone { background: var(--tt); box-shadow: none; }
.k-bx { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 32px; align-items: center; }
.k-bx-m img { width: 100%; height: auto; mix-blend-mode: multiply; }
.k-bx-b h3, .k-box h3 { font: 400 clamp(19px, 1.5vw, 22px)/1.3 var(--dsp); }
.k-bx-b h3 [lang="en"], .k-box h3[lang="en"] { font-family: var(--lat); font-stretch: 62%; font-weight: 820; font-size: 1.1em; }
.k-bx-b p, .k-box p { margin-top: 8px; font-size: 14.5px; line-height: 1.7; color: var(--ink-2); }
.k-sb > * + .k-box, .k-sb > * + .k-dcb { margin-top: clamp(32px, 3vw, 44px); }
.k-logos { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: 1px solid var(--ink-r); }
.k-logos li { display: grid; place-items: center; height: 112px; padding: 18px 22px; border-bottom: 1px solid var(--ink-r); }
.k-logos img { max-height: 60px; width: auto; object-fit: contain; }
.k-lg { position: relative; display: block; overflow: hidden; width: calc(var(--lw) * 1px); max-width: 100%; }
.k-lg img { position: absolute; max-width: none; max-height: none; }
.k-map { position: relative; aspect-ratio: 2 / 1; background: var(--tint); }
.k-map::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 0 1px var(--ink-r); pointer-events: none; }
.k-map iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; filter: saturate(.5) contrast(.97); }
.k-map-ph { position: absolute; inset: 0; display: grid; place-items: center; font: 500 13px/1 var(--lat); letter-spacing: .04em; color: var(--ink-3); }
.k-sb > * + .k-map { margin-top: clamp(32px, 3vw, 44px); }
.k-map-l { margin-top: 12px; }

/* ================================================================ lists (C2's publication list) ======================== */
.k-ctl { margin-top: clamp(24px, 2.4vw, 36px); }
.k-f + .k-f { margin-top: 24px; }
.k-fl { margin: 0 0 4px; font-size: 12px; line-height: 1.4; letter-spacing: .02em; color: var(--ink-3); }
.k-fb { position: relative; display: grid; justify-content: start; justify-items: start; column-gap: 24px; }
.k-f--year .k-fb { grid-template-columns: repeat(4, minmax(0, 1fr)); max-width: 288px; column-gap: 16px; }
.k-f--team .k-fb, .k-f--status .k-fb, .k-f--country .k-fb { grid-template-columns: repeat(2, max-content); }
.k-fb button { appearance: none; -webkit-appearance: none; margin: 0; padding: 8px 0; border: 0; border-radius: 0; background: none; cursor: pointer;
  font: 500 15px/1.3 var(--ko); color: var(--ink-3); text-align: left; white-space: nowrap; transition: color .2s ease; }
.k-fb button [lang="en"] { font-family: var(--lat); font-weight: 500; }
.k-num { font-family: var(--lat); font-stretch: 62%; font-weight: 640; font-size: 18px; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; }
.k-fb button:hover, .k-fb button[aria-pressed="true"] { color: var(--ink); }
.k-fb:not(.has-ind) button[aria-pressed="true"] .k-bl { box-shadow: 0 2px 0 var(--umber); }
.k-ind { position: absolute; left: 0; top: 0; width: 0; height: 2px; background: var(--umber); pointer-events: none; }
.k-fb:not(.has-ind) .k-ind { display: none; }
.k-bc { display: inline-block; vertical-align: top; font: 640 11px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink-3); }
.k-fb button[aria-pressed="true"] .k-bc { color: var(--ink-2); }
.k-tally { margin: 32px 0 8px; overflow: hidden; font-size: 13.5px; line-height: 1.4; color: var(--ink-2); }
.k-tally [data-n] { display: inline-block; }
.k-cn { font: 640 18px/1 var(--lat); font-stretch: 62%; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink); }
.k-reel { display: flex; align-items: flex-end; gap: 1px; height: 30px; }
.k-reel i { flex: 1 1 0; min-width: 0; height: 100%; background: var(--ink); opacity: .13; transform-origin: 50% 100%; transform: scaleY(.42); }
.k-reel i.on { opacity: .6; transform: none; }
.k-reel i.cur { opacity: 1; background: var(--umber); }
.k-reel.live i { transition: opacity .3s ease, transform .45s var(--out), background-color .3s ease; transition-delay: calc(var(--d, 0) * 1ms); }
.k-reel-y { display: flex; justify-content: space-between; margin: 8px 0 0; font: 640 12px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); font-variant-numeric: tabular-nums; }
.k-lw { position: relative; grid-column: 2; min-width: 0; }
.k-top { position: absolute; left: 0; top: -150px; width: 1px; height: 1px; pointer-events: none; }
.k-list { border-top: 1px solid var(--ink-r); }
.k-row { display: grid; grid-template-columns: 58px minmax(0, 1fr) 128px; grid-template-areas: "yr tx tm"; align-items: baseline; column-gap: 24px; padding: 16px 0; border-bottom: 1px solid var(--ink-r); }
.k-yr { grid-area: yr; font: 640 18px/1.4 var(--lat); font-stretch: 62%; letter-spacing: .01em; font-variant-numeric: tabular-nums lining-nums; color: var(--ink); }
.k-st { font: 500 13.5px/1.6 var(--ko); letter-spacing: 0; }
.k-st [lang="en"] { font-family: var(--lat); }
.k-tx { grid-area: tx; min-width: 0; max-width: 680px; }
.k-ti { font-size: 16.5px; line-height: 1.46; font-weight: 500; color: var(--ink); overflow-wrap: anywhere; }
.k-ti[lang="en"] { letter-spacing: -.004em; }
.k-au { margin-top: 6px; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); overflow-wrap: anywhere; }
.k-jn { margin-top: 2px; font-size: 13.5px; line-height: 1.5; font-weight: 500; color: var(--ink); }
.k-tm { grid-area: tm; display: flex; justify-content: flex-end; align-items: baseline; gap: 8px; font-size: 12px; line-height: 1.45; color: var(--ink-3); text-align: right; white-space: nowrap; }
.k-tm .k-mk { width: 7px; height: 7px; align-self: center; }
.k-row--e { display: block; padding: 24px 0 28px; font-size: 18px; line-height: 1.45; font-weight: 500; color: var(--ink); }
.k-pg { display: flex; align-items: center; gap: 12px; margin-top: 24px; }
.k-pg[hidden] { display: none; }
.k-pg button { appearance: none; -webkit-appearance: none; width: 44px; height: 44px; margin: 0; padding: 0; display: grid; place-items: center; border: 1px solid var(--ink-r2);
  border-radius: 0; background: transparent; color: var(--ink); cursor: pointer; transition: background-color .2s ease, color .2s ease, border-color .2s ease, transform .12s ease; }
.k-pg svg, .k-gl-vbar svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.6; transition: transform .3s var(--out); }
.k-pg button:hover:not(:disabled) { background: var(--ink); border-color: var(--ink); color: var(--paper); }
.k-pg button[data-p="1"]:hover:not(:disabled) svg { transform: translateX(2px); }
.k-pg button[data-p="-1"]:hover:not(:disabled) svg { transform: translateX(-2px); }
.k-pg button:active:not(:disabled) { transform: scale(.94); }
.k-pg button:disabled { opacity: .3; cursor: default; }
.k-pi { display: inline-block; overflow: hidden; min-width: 4.6em; text-align: center; font: 640 18px/44px var(--lat); font-stretch: 62%; letter-spacing: .02em; font-variant-numeric: tabular-nums lining-nums; }
.k-pi > span { display: inline-block; }
.k-ls-foot { margin-top: 28px; }
.k-ls .k-ctl { margin-top: 0; margin-bottom: 24px; }

/* ================================================================ video ================================================= */
.k-vid .k-in { grid-template-rows: auto auto 1fr; }   /* the player spans into the 1fr row: the heading row keeps its own height */
.k-vl { grid-column: 1; grid-row: 3; min-width: 0; }
.k-vs { grid-row: 2 / span 2; }
.k-scr { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: var(--ink-2); }
.k-scr::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 0 1px var(--ink-r2); pointer-events: none; }   /* a white poster (the whiteboard intro) still reads as a frame */
.k-poster { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(.86) contrast(.97) brightness(1.02); transition: opacity .3s ease; }
.k-scr video { position: absolute; inset: 0; width: 100%; height: 100%; background: #000; }
.k-scr.on .k-poster, .k-scr.on .k-play { opacity: 0; pointer-events: none; }
.k-play { position: absolute; left: 50%; top: 50%; width: 64px; height: 64px; margin: -32px 0 0 -32px; padding: 0; border: 0; border-radius: 0; cursor: pointer;
  display: grid; place-items: center; background: rgba(15, 14, 12, .86); color: var(--paper); transition: background-color .2s ease, transform .12s ease, opacity .2s ease; }
.k-play svg { width: 22px; height: 22px; margin-left: 3px; fill: currentColor; }
.k-play:hover { background: var(--ink); transform: scale(1.04); }   /* an ink chip reads on a white poster and on footage alike */
.k-play:active { transform: scale(.94); }
.k-play:focus-visible { outline: 2px solid var(--ink); outline-offset: 0; box-shadow: 0 0 0 4px var(--paper); }
.k-now { display: flex; justify-content: space-between; gap: 16px; align-items: baseline; margin-top: 16px; }
.k-now-t { font-size: 16.5px; line-height: 1.4; font-weight: 500; }
.k-now-m, .k-pm { font: 640 14px/1.3 var(--lat); font-stretch: 62%; letter-spacing: .02em; font-variant-numeric: tabular-nums; color: var(--ink-3); flex: none; }
.k-plist { margin-top: clamp(24px, 2.4vw, 32px); border-top: 1px solid var(--ink-r); }
.k-plist li { border-bottom: 1px solid var(--ink-r); }
.k-plist button { position: relative; display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 14px; align-items: center; width: 100%; padding: 14px 0 14px 14px;
  border: 0; border-radius: 0; background: none; text-align: left; cursor: pointer; }
.k-plist button::before { content: ""; position: absolute; left: 0; top: 14px; bottom: 14px; width: 2px; background: var(--umber); transform: scaleY(0); transition: transform .4s var(--out); }
.k-plist button[aria-current="true"]::before { transform: none; }
.k-plist img { width: 96px; aspect-ratio: 16 / 9; object-fit: cover; background: var(--tint); filter: saturate(.86) contrast(.97); }
.k-pt { display: block; font-size: 14.5px; line-height: 1.45; font-weight: 500; color: var(--ink-2); transition: color .2s ease; }
.k-plist button[aria-current="true"] .k-pt, .k-plist button:hover .k-pt { color: var(--ink); }
.k-pm { display: block; margin-top: 4px; font-size: 13px; }
.k-vstack .k-plist { margin-top: 24px; }

/* ================================================================ gallery ================================================ */
.k-gteaser { display: grid; gap: clamp(24px, 2.4vw, 36px); }
.k-gt-row { display: flex; gap: clamp(12px, 1.2vw, 20px); }
.k-gt { flex: var(--r) 1 0; min-width: 0; }
.k-gt > a { display: block; text-decoration: none; color: inherit; }
.k-gt .k-ph, .k-gl-open { aspect-ratio: var(--r); }
.k-gt .k-im, .k-gl-open .k-im { object-position: 50% 50%; filter: saturate(.9) contrast(.98); }
.k-gt > a:hover .k-im { filter: saturate(1) contrast(1); transform: scale(1.02); }
.k-gt figcaption, .k-gl-it figcaption { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-top: 10px; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); }
.k-gt > a:hover .k-cp { color: var(--ink); }
.k-cy { flex: none; font: 640 14px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); font-variant-numeric: tabular-nums; }
.k-gl { position: relative; }
.k-gl-f { margin-bottom: 28px; }
.k-gl-f[hidden] { display: none; }
.k-gl-f .k-fb { grid-template-columns: repeat(7, max-content); max-width: none; column-gap: 24px; }
.k-gl-grid { display: flex; flex-wrap: wrap; gap: 28px 16px; align-content: flex-start; }
.k-gl-grid::after { content: ""; flex: 999 1 0; }
.k-gl-grid.jx::after { display: none; }
.k-gl-it { flex: var(--r) 1 calc(var(--r) * 250px); min-width: 0; }
.k-gl-it[hidden] { display: none; }
.k-gl-open { width: 100%; border: 0; padding: 0; cursor: zoom-in; background: none; }
.k-gl .k-pg { margin-top: 36px; }
.k-gl-view { position: absolute; left: 0; right: 0; z-index: 6; background: var(--paper); border-top: 1px solid var(--ink); border-bottom: 1px solid var(--ink-r); opacity: 0; transform: scale(.985);
  transition: opacity .24s ease, transform .24s var(--out); }
.k-gl-view.on { opacity: 1; transform: none; }
.k-gl-view:focus { outline: none; }
.k-gl-view[hidden] { display: none; }
.k-gl-vbox { position: absolute; inset: 0; display: grid; grid-template-rows: minmax(0, 1fr) auto; gap: 14px; padding: 20px 0 16px; }
.k-gl-vimg { position: relative; min-height: 0; }
.k-gl-vimg img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }
.k-gl-vbar { display: flex; align-items: center; flex-wrap: wrap; gap: 8px 12px; }
.k-gl-vcap { flex: 1 1 16em; font-size: 14.5px; line-height: 1.5; color: var(--ink); }
.k-gl-vcap .k-cy { margin-left: 12px; }
.k-gl-vn { font: 640 15px/1 var(--lat); font-stretch: 62%; letter-spacing: .02em; color: var(--ink-3); font-variant-numeric: tabular-nums; }
.k-gl-vbar button { height: 44px; min-width: 44px; padding: 0 14px; display: inline-grid; place-items: center; border: 1px solid var(--ink-r2); border-radius: 0; background: none; cursor: pointer;
  color: var(--ink); font-size: 14px; font-weight: 500; transition: background-color .2s ease, color .2s ease, border-color .2s ease; }
.k-gl-vbar button:hover { background: var(--ink); border-color: var(--ink); color: var(--paper); }

/* ================================================================ the inner-page hero ====================================
   A frame on the sheet from the 34% axis to the right margin (photo, lab tint or logo). The title stands at the frame's
   left edge; the frame's bottom edge crosses its first line mid-glyph (--k em below the line top: KO .39, EN .41,
   measured): two layers set from the same rules, the h1 (ink) under the frame and an aria-hidden copy inside it (paper
   white on a photograph, the deep tone on a tint). Sized to fit the frame (--em: the title's width in em). */
.k-hero {
  --ft: clamp(24px, 2.2vw, 32px); --fh: clamp(240px, 22vw, 340px); --fb: calc(var(--ft) + var(--fh));
  --fl: var(--fx); --fr: calc(var(--ox) + var(--m)); --fw: calc(var(--W) * .66 - var(--m));
  --hmax: clamp(64px, 7.6vw, 132px); --em: var(--em-ko); --k: .39;
  --hs: min(var(--hmax), calc(var(--fw) * .94 / var(--em)));
  position: relative; isolation: isolate; background: var(--paper); padding-top: var(--fb);
}
html[data-lang="en"] .k-hero { --em: var(--em-en); --k: .41; }
.k-hero--tone { --fh: clamp(150px, 13vw, 220px); }    /* a field with nothing in it stays low: it frames the title, no more */
.k-hero--logo { --fh: clamp(200px, 17vw, 280px); }
.k-hf { position: absolute; z-index: 2; top: var(--ft); left: var(--fl); right: var(--fr); height: var(--fh); overflow: hidden; background: var(--ink-2); }
.k-hf--tone, .k-hf--logo { background: var(--tt); }
.k-hf::after { content: ""; position: absolute; inset: 0; z-index: 4; pointer-events: none; box-shadow: inset 0 1px 0 var(--ink-r), inset 1px 0 0 var(--ink-r), inset -1px 0 0 var(--ink-r); }
.k-hf--tone::after, .k-hf--logo::after { display: none; }
.k-hpar { position: absolute; left: 0; right: 0; top: -8%; bottom: 0; will-change: transform; }
.k-hmed { position: absolute; inset: 0; overflow: hidden; filter: saturate(.86) contrast(.97) brightness(1.02); transform-origin: 50% 60%; }
.k-himg { width: 100%; height: 100%; object-fit: cover; object-position: var(--fp, 50% 40%); }
/* a local shade under the white part of the title only (bottom-left of the photograph), never a scrim */
.k-hsh { position: absolute; left: 0; bottom: 0; z-index: 1; width: calc(var(--em) * var(--hs) * 1.08 + 48px); max-width: 100%; height: calc(var(--hs) * (var(--k) + .55));
  background: linear-gradient(0deg, rgba(15, 14, 12, .4) 0%, rgba(15, 14, 12, .3) 34%, rgba(15, 14, 12, .1) 70%, rgba(15, 14, 12, 0) 100%);
  -webkit-mask-image: linear-gradient(90deg, #000 72%, transparent 100%); mask-image: linear-gradient(90deg, #000 72%, transparent 100%); pointer-events: none; }
.k-hlg { position: absolute; inset: 0; display: flex; align-items: center; padding: 0 clamp(28px, 4vw, 64px); }
.k-hlogo { height: clamp(64px, 30%, 112px); width: auto; max-width: 70%; object-fit: contain; mix-blend-mode: multiply; }
.k-hk, .k-hw { margin: 0; font-weight: 400; width: var(--fw); max-width: var(--fw); }
.k-hin { row-gap: 0; }
.k-hk { position: relative; z-index: 1; grid-column: 2; grid-row: 1; margin-top: calc(var(--hs) * var(--k) * -1); color: var(--ink); }
.k-hk.sr { position: absolute !important; }
.k-hw { position: absolute; z-index: 3; left: calc(var(--tx) + var(--c1) + var(--gut) - var(--fl)); top: calc(var(--fh) - var(--hs) * var(--k)); color: var(--paper); pointer-events: none;
  text-shadow: 0 0 1px rgba(15, 14, 12, .24), 0 1px 10px rgba(15, 14, 12, .3); }
.k-hf--tone .k-hw { color: var(--td); text-shadow: none; }
.k-ht { display: block; font-size: var(--hs); }
.k-ht:lang(ko) { font-family: var(--dsp); line-height: .98; letter-spacing: -.012em; margin-left: -.045em; }
.k-ht:lang(en) { font-family: var(--lat); font-stretch: 62%; font-weight: 860; line-height: .86; letter-spacing: -.004em; text-transform: uppercase; margin-left: -.03em; }
.k-hinst { grid-column: 1; grid-row: 2; margin-top: 22px; font-size: 13.5px; line-height: 1.45; font-weight: 500; color: var(--ink-2); max-width: 22em; }
.k-hlow { grid-column: 2; grid-row: 2; margin-top: 20px; min-width: 0; }
.k-halt { font-size: clamp(17px, 1.35vw, 20px); line-height: 1.5; font-weight: 500; color: var(--ink); }
.k-halt [lang="en"], .k-halt[lang="en"] { font-weight: 500; }
.k-hlead { margin-top: 12px; }
.k-hlead p { max-width: 35em; font-size: clamp(15.5px, 1.2vw, 17px); line-height: 1.75; color: var(--ink-2); text-wrap: pretty; }
.k-hlead p[lang="en"] { line-height: 1.6; }
.k-hx { margin-top: clamp(24px, 2.4vw, 32px); }
.k-hx .k-rec { margin-top: 4px; }
.k-hero--logo .k-hlow { margin-top: clamp(24px, 2.4vw, 32px); }
.k-hero--logo .k-hinst { margin-top: clamp(26px, 2.6vw, 34px); }
/* the cut line: drawn across the frame's middle at first paint (CSS), held, split (script) */
.k-he { position: absolute; z-index: 5; left: var(--fl); right: var(--fr); top: calc(var(--ft) + var(--fh) / 2); height: 1px; margin-top: -.5px; background: var(--ink);
  transform-origin: 0 50%; transform: scaleX(0); opacity: 0; pointer-events: none; }
html.js:not(.rm) .k-he-t { animation: k-draw .62s cubic-bezier(.65, 0, .35, 1) .08s both; }
@keyframes k-draw { from { transform: scaleX(0); opacity: 1; } to { transform: scaleX(1); opacity: 1; } }
html.all .k-he, html.rm .k-he, .k-hero.is-done .k-he { display: none; }

/* ================================================================ reveal states: hidden only when motion will run ===== */
html.js:not(.rm) [data-a]:not(.on) { opacity: 0; }
html.js:not(.rm) .k-hf[data-a]:not(.on) { opacity: 1; clip-path: inset(50% 0 50% 0); }
html.rm *, html.rm *::before, html.rm *::after { transition: none !important; animation: none !important; }

/* ================================================================ desktop widths between (Wix shows 980+ and 320) ====== */
@media (max-width: 1199px) {
  .k-row { grid-template-columns: 52px minmax(0, 1fr) 112px; column-gap: 20px; }
  .k-ppl--m .k-nm, .k-ppl--s .k-nm { font-size: 15px; }
}
@media (max-width: 899px) {
  .k-ppl, .k-ppl--s { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .k-f--year .k-fb { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .k-org-u { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 16px; }
  .k-org-b > .k-rule { display: none; }
}

/* ================================================================ 320 (Wix mobile): one column, the same parts ========= */
@media (max-width: 760px) {
  body { font-size: 15.5px; }
  .k-in { grid-template-columns: minmax(0, 1fr); column-gap: 0; }
  .k-in > * { grid-column: 1 !important; }
  .k-sh { margin-bottom: 20px; }
  .k-h { font-size: 26px; }
  .k-h [lang="en"] { font-size: 1.08em; }
  .k-note { margin-top: 8px; max-width: none; }
  .k-sec--wide .k-swl { grid-row: auto; justify-self: start; order: 9; margin-top: 20px; }
  .k-sec--wide .k-sb { margin-top: 0; }
  .k-sec--wide .k-in { display: flex; flex-direction: column; align-items: stretch; }
  .k-ch { --hs: 34px; }
  .k-ch-en .l { font-size: calc(var(--hs) * 1.06); }
  .k-chs .k-leadw { margin-top: 16px; }
  .k-lead { font-size: 15px; line-height: 1.72; }
  .k-lead[lang="en"] { font-size: 15px; line-height: 1.58; }
  .k-prose p { font-size: 15.5px; line-height: 1.82; }
  .k-prose p[lang="en"] { font-size: 15px; line-height: 1.6; }
  .k-kv { grid-template-columns: minmax(0, 1fr); }
  .k-kv dt { padding: 14px 0 0; }
  .k-kv dd { padding: 2px 0 14px; border-top: 0; font-size: 15.5px; }
  .k-kv dt:last-of-type { border-bottom: 0; }
  .k-cols, .k-c3, .k-c4 { grid-template-columns: minmax(0, 1fr); gap: 36px; }
  .k-m2 { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 12px; }
  .k-m2 .k-h3 { font-size: 16px; margin-top: 12px; }
  .k-m2 .k-d { font-size: 13px; line-height: 1.6; }
  .k-m2 .k-figs .k-fg, .k-m2.k-figs .k-fg { margin-top: 12px; }
  .k-h3 { font-size: 21px; margin-top: 14px; }
  .k-d { font-size: 14.5px; }
  .k-rec { grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 8px; padding-top: 10px; }
  .k-rec-n { font-size: 26px; }
  .k-rec-l { margin-top: 4px; font-size: 11px; line-height: 1.3; }
  .k-rec-l [lang="en"] { font-size: 11px; }
  .k-lab > a { grid-template-columns: minmax(0, 1fr) 24px; grid-template-areas: "h go" "b b"; row-gap: 10px; padding: 20px 0 22px; }
  .k-lab-h { grid-area: h; }
  .k-lab-b { grid-area: b; }
  .k-lab-go { grid-area: go; padding-top: 6px; }
  .k-lab > a::before { inset: 1px -8px 0; }
  .k-lab-n { font-size: 26px; }
  .k-lab-d { font-size: 15px; line-height: 1.68; }
  .k-faces img, .k-fi { width: 28px; height: 28px; }
  .k-dc-logo { height: 32px; }
  .k-dc-logo .l1 { height: 34.6px; margin-left: -3px; }
  .k-dc-logo .l2 { height: 52px; margin-left: -13px; }
  .k-dcb { padding: 22px 18px; }
  .k-dcb .k-dc-logo { height: 32px; }
  .k-org-b { margin-top: 12px; padding-top: 0; }
  .k-org-b::before, .k-org-b > .k-rule { display: none; }
  .k-org-u { grid-template-columns: minmax(0, 1fr); row-gap: 0; }
  .k-org-it { padding: 6px 0 6px 24px; }
  .k-org-it::before { top: 50%; width: 16px; height: 1px; }
  .k-org-it.is-cur::before { height: 3px; margin-top: -1px; width: 16px; }
  .k-org-it::after { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 1px; background: var(--ink-r2); }
  .k-org-it:first-child::after { top: -12px; }
  .k-org-it:last-child::after { bottom: 50%; }
  .k-org-x { padding: 12px 14px 14px; }
  .k-org-l b { font-size: 21px; }
  .k-ppl, .k-ppl--m { grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 8px; row-gap: 24px; }
  .k-ppl--m .k-mt { margin-top: 8px; }
  .k-ppl--m .k-nm { font-size: 14.5px; }
  .k-ppl--m .k-role { font-size: 11.5px; line-height: 1.4; }
  .k-ppl--l, .k-ppl--s { grid-template-columns: minmax(0, 1fr); row-gap: 16px; }
  .k-ppl--l .k-mem, .k-ppl--s .k-mem { display: grid; grid-template-columns: 112px minmax(0, 1fr); column-gap: 16px; align-items: end; }
  .k-ppl--s .k-mem { grid-template-columns: 64px minmax(0, 1fr); align-items: center; }
  .k-ppl--l .k-mt, .k-ppl--s .k-mt { margin: 0 0 2px; }
  .k-ppl--s .k-ini { font-size: 24px; }
  .k-jump ul { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 16px; }
  .k-jump a { font-size: 14px; padding: 9px 0; }
  .k-ft, .k-ft.has-q { grid-template-columns: 112px minmax(0, 1fr); grid-template-areas: "pic who" "cv cv"; grid-template-rows: auto; column-gap: 16px; align-items: end; }
  .k-ft.has-q { grid-template-areas: "pic who" "q q" "cv cv"; }
  .k-ft-q { margin: 24px 0 0; }
  .k-ft-q p { font-size: 16px; line-height: 1.85; }
  .k-ft-nm { font-size: 18px; }
  .k-ft-rl { display: block; margin: 4px 0 0; }
  .k-ft-cv { margin-top: 18px; }
  .k-ft-cv ul { margin-top: 0; font-size: 13px; }
  .k-pq blockquote p { font-size: 17.5px; line-height: 1.8; }
  .k-bx { grid-template-columns: 72px minmax(0, 1fr); gap: 18px; align-items: start; }
  .k-box { padding: 20px 18px; }
  .k-logos { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .k-logos li { height: 84px; padding: 14px; }
  .k-logos img { max-height: 46px; }
  .k-lg { width: calc(var(--lw) * .74px); }
  .k-map { aspect-ratio: 4 / 3; }
  .k-ctl { margin-top: 16px; margin-bottom: 24px; }
  .k-fb { column-gap: 16px; }
  .k-f--team .k-fb, .k-f--status .k-fb, .k-f--country .k-fb { grid-template-columns: repeat(2, minmax(0, 1fr)); width: 100%; }
  .k-f--year .k-fb { grid-template-columns: repeat(4, minmax(0, 1fr)); width: 100%; max-width: none; }
  .k-fb button { padding: 12px 0; }
  .k-f + .k-f { margin-top: 16px; }
  .k-tally { margin: 24px 0 8px; }
  .k-reel { height: 24px; }
  .k-row { grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "yr tm" "tx tx"; row-gap: 4px; padding: 16px 0; }
  .k-yr { font-size: 15px; }
  .k-ti { font-size: 15px; line-height: 1.48; }
  .k-au, .k-jn { font-size: 12px; }
  .k-vid .k-in { display: flex; flex-direction: column; align-items: stretch; }
  .k-vid .k-sh { order: 1; }
  .k-vs { order: 2; }
  .k-vl { order: 3; }
  .k-play { width: 52px; height: 52px; margin: -26px 0 0 -26px; }
  .k-play svg { width: 18px; height: 18px; }
  .k-now { flex-direction: column; gap: 2px; margin-top: 12px; }
  .k-now-t { font-size: 15.5px; }
  .k-plist { margin-top: 16px; }
  .k-gteaser { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 10px; }
  .k-gt-row { display: contents; }
  .k-gt { --r: 4 / 3; }
  .k-gt-row:first-child .k-gt:first-child { grid-column: 1 / -1; --r: 3 / 2; }
  .k-gt figcaption, .k-gl-it figcaption { display: block; font-size: 12.5px; margin-top: 7px; }
  .k-cy { display: block; margin-top: 3px; font-size: 12px; }
  .k-gl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 10px; }
  .k-gl-grid::after { display: none; }
  .k-gl-it { --r: 4 / 3; }
  .k-gl-open { aspect-ratio: 4 / 3; }
  .k-gl-f .k-fb { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  /* hero: the frame spans the width; the title starts at the margin */
  .k-hero { --ft: 16px; --fh: 196px; --fl: 0px; --fr: 0px; --fw: calc(100vw - 2 * var(--m)); --hmax: 54px; }
  html[data-lang="en"] .k-hero { --hmax: 46px; }
  .k-hero--tone { --fh: 120px; }
  .k-hero--logo { --fh: 168px; }
  .k-hw { left: var(--m); }
  .k-himg { object-position: var(--fpm, var(--fp, 50% 40%)); }
  .k-hlg { padding: 0 24px; }
  .k-hlogo { height: 34%; max-width: 76%; }
  .k-hinst { grid-row: auto; margin-top: 14px; font-size: 12px; }
  .k-hlow { grid-row: auto; margin-top: 12px; }
  .k-halt { font-size: 16.5px; }
  .k-hlead p { font-size: 15px; line-height: 1.68; }
  .k-hlead p[lang="en"] { font-size: 14.5px; line-height: 1.55; }
  .k-hx { margin-top: 22px; }
}
"""

# ================================================================== JS (after the runtime; GSAP is optional)
KIT_JS = r"""
/* RIHE kit (tools/kit.py): lists, gallery, video, the language height lock, motion. Every module is guarded: if one
   throws, everything is shown (RIHE.showAll). Motion only with GSAP and without reduced motion. */
(function () {
  'use strict';
  var R = window.RIHE, doc = document, root = doc.documentElement;
  if (!R) return;
  R.motionReady();
  var g = window.gsap, ST = window.SplitText, CE = window.CustomEase, reduce = !!R.reduce;
  var $$ = function (s, c) { return [].slice.call((c || doc).querySelectorAll(s)); };
  var phone = function () { return !!(window.matchMedia && matchMedia('(max-width: 760px)').matches); };
  var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;'); }
  function la(s) { return /[가-힣]/.test(String(s || '')) ? ' lang="ko"' : ' lang="en"'; }
  function t2(p) { return '<span data-l="ko">' + p[0] + '</span><span data-l="en" lang="en">' + p[1] + '</span>'; }
  function run(name, fn) { try { fn(); } catch (err) { if (window.console) console.error('kit ' + name, err); R.showAll(); } }
  if (g) {
    var pl = [ST, CE].filter(Boolean);
    if (pl.length) g.registerPlugin.apply(g, pl);
    if (CE && !CE.get('cxGate')) { CE.create('cxGate', 'M0,0 C0.5,0 0.14,1 1,1'); CE.create('cxDraw', 'M0,0 C0.65,0 0.35,1 1,1'); }
  }
  var EGATE = g && CE ? 'cxGate' : 'expo.inOut', EDRAW = g && CE ? 'cxDraw' : 'power2.inOut';
  var anim = !!g && !reduce;
  var tls = [];
  function keep(tl) { tls.push(tl); return tl; }
  function finishAll() { tls.forEach(function (tl) { try { tl.progress(1); } catch (e) {} }); }
  R.showHooks.push(finishAll);
  R.onLang(finishAll);
  var fontsIn = (doc.fonts && doc.fonts.ready) ? Promise.race([doc.fonts.ready, wait(1500)]) : Promise.resolve();
  // a number that changes turns over like the hero's counters
  function turn(el, d) {
    if (!el || !anim) return;
    g.fromTo(el, { yPercent: 85 * d, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: .5, ease: 'expo.out', overwrite: true, clearProps: 'transform,opacity,visibility' });
  }
  // the pressed filter: a 2 px umber bar slides under it
  function indicators(box, animate) {
    $$('.k-fb', box).forEach(function (fb) {
      var ind = fb.querySelector('.k-ind'), b = fb.querySelector('button[aria-pressed="true"]');
      if (!ind || !b || !fb.offsetWidth) return;
      var lab = b.querySelector('.k-bl') || b;   // .k-fb is the label's offsetParent (buttons are not positioned)
      var x = lab.offsetLeft, y = lab.offsetTop + lab.offsetHeight + 1, w = lab.offsetWidth;
      fb.classList.add('has-ind');
      if (g && animate && anim) g.to(ind, { x: x, y: y, width: w, duration: .5, ease: 'expo.out', overwrite: true });
      else if (g) g.set(ind, { x: x, y: y, width: w });
      else { ind.style.transform = 'translate(' + x + 'px,' + y + 'px)'; ind.style.width = w + 'px'; }
    });
  }

  /* ================================================================ lists (RIHE.list; works without GSAP) */
  run('lists', function () {
    $$('[data-list]').forEach(function (box) {
      var src = box.querySelector('script.k-ls-data');
      if (!src) return;
      var J = JSON.parse(src.textContent), kind = J.kind;
      function lab(map, k) { var p = map[k]; return p ? t2(p) : esc(k); }
      function row(d) {
        if (kind === 'patent') return '<li class="k-row k-row--pt" data-i="' + d.i + '"><span class="k-yr k-st">' + lab(J.status, d.status) + '</span><div class="k-tx">' +
          '<p class="k-ti" lang="ko">' + esc(d.title) + '</p></div><span class="k-tm">' + (d.country ? lab(J.country, d.country) : '') + '</span></li>';
        var s = kind === 'report' ? d.event : d.journal, tm = '';
        if (kind === 'pub' && J.team && J.teams[d.team]) tm = '<i class="k-mk" style="--tt:var(--t-' + J.tones[d.team] + ');--td:var(--d-' + J.tones[d.team] + ')" aria-hidden="true"></i>' + t2(J.teams[d.team]);
        return '<li class="k-row" data-i="' + d.i + '"><span class="k-yr">' + d.year + '</span><div class="k-tx">' +
          '<p class="k-ti"' + la(d.title) + '>' + esc(d.title) + '</p><p class="k-au"' + la(d.authors) + '>' + esc(d.authors) + '</p>' +
          '<p class="k-jn"' + la(s) + '>' + esc(s) + '</p></div><span class="k-tm">' + tm + '</span></li>';
      }
      var ticks = box.querySelector('[data-ticks]'), pi = box.querySelector('[data-pi]'), tally = box.querySelector('[data-n]');
      var lwrap = box.querySelector('.k-lw'), pgr = box.querySelector('.k-pg'), anchor = box.querySelector('.k-top');
      var dir = 1, shown = !anim, pressed = null;
      box.addEventListener('click', function (ev) { var p = ev.target.closest && ev.target.closest('button[data-p]'); if (p) { dir = +p.getAttribute('data-p'); pressed = p; } }, true);
      // the engine reserves the tallest page on the list itself; hold it on the wrapper instead, so the pager always
      // follows the rows and a short page leaves its spare height after the pager (the total is the same)
      function reserve(ul) {
        var mh = parseFloat(ul.style.minHeight) || 0;
        if (!mh || !lwrap || !pgr) return;
        ul.style.minHeight = '';
        var foot = box.querySelector('.k-ls-foot'), fh = 0;
        if (foot) {   // the link under the pager, in the taller of its two languages
          var cl = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko', f1 = foot.getBoundingClientRect().height;
          root.setAttribute('data-lang', cl === 'en' ? 'ko' : 'en');
          fh = Math.max(f1, foot.getBoundingClientRect().height) + (parseFloat(getComputedStyle(foot).marginTop) || 0);
          root.setAttribute('data-lang', cl);
        }
        lwrap.style.minHeight = Math.ceil(mh + pgr.offsetHeight + (parseFloat(getComputedStyle(pgr).marginTop) || 0) + fh) + 'px';
      }
      // the first or last page disables the pressed button: keep the keyboard on the pager
      function keepFocus() {
        if (!pressed || !pressed.disabled) return;
        var a = doc.activeElement;
        if (a && a !== doc.body && a !== pressed) return;
        var other = box.querySelector('button[data-p="' + (-dir) + '"]');
        if (other && !other.disabled) { try { other.focus({ preventScroll: true }); } catch (e) {} }
      }
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
      // every option carries its count under the other filters: a combination with nothing in it reads 0 before it is pressed
      function counts(animate) {
        var f = {};
        opts.forEach(function (b) { if (b.getAttribute('aria-pressed') === 'true') f[b.getAttribute('data-k')] = b.getAttribute('data-v'); });
        opts.forEach(function (b) {
          var c = b.querySelector('.k-bc'), x = {}, n = 0, y;
          if (!c) return;
          for (y in f) x[y] = f[y];
          x[b.getAttribute('data-k')] = b.getAttribute('data-v');
          J.items.forEach(function (d) { if (hit(d, x)) n++; });
          if (c.textContent !== String(n)) { c.textContent = n; if (animate) turn(c, 1); }
        });
      }
      function tallyNum() {
        $$('[data-l]', tally).forEach(function (s) { if (!s.querySelector('.k-cn')) s.innerHTML = s.textContent.replace(/^(\d+)/, '<b class="k-cn">$1</b>'); });
      }
      // paging from the pager under the list: bring the list's top back on screen (the anchor sits 150 px above the list)
      function toTop() {
        var b = R.band, top = R.rect(lwrap).top;
        var above = b && b.ok ? top < b.top + 40 : lwrap.getBoundingClientRect().top < 0;
        if (above && anchor && anchor.scrollIntoView) anchor.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }
      // the tallest page of both languages: the engine measures the language on screen; a second pass measures the
      // other one (rows hold both languages, so nothing is re-rendered for it) and the list keeps the taller reserve
      var api = null, other = false;
      function both(ul) {
        if (!api) return;
        var mine = parseFloat(ul.style.minHeight) || 0, cur = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko';
        other = true; root.setAttribute('data-lang', cur === 'en' ? 'ko' : 'en');
        try { api.measure(); } finally { root.setAttribute('data-lang', cur); other = false; }
        ul.style.minHeight = Math.max(mine, parseFloat(ul.style.minHeight) || 0) + 'px';
      }
      function after(ul, reason) {
        if (reason === 'measure') { if (other) return; both(ul); reserve(ul); }
        var cur = {};
        [].forEach.call(ul.children, function (li) { var i = li.getAttribute('data-i'); if (i !== null) cur[i] = 1; });
        if (ticks) for (var i = 0; i < ticks.children.length; i++) ticks.children[i].classList.toggle('cur', !!cur[i]);
        if (tally) tallyNum();
        if (reason !== 'page') counts(reason !== 'measure' && anim && shown);
        indicators(box, reason !== 'measure');
        if (reason === 'page') { keepFocus(); toTop(); }
        if (reason === 'measure' || !anim || !shown) return;
        // the next page is a cut, not a crossfade: the rows come up in about 300 ms, top first
        g.fromTo(ul.children, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: .4, stagger: .018, ease: 'expo.out', overwrite: true, clearProps: 'transform,opacity,visibility' });
        if (reason === 'page') turn(pi, dir); else { turn(tally, 1); turn(pi, 1); }
      }
      api = R.list(box, { data: J.items, size: J.size || 10, render: row, empty: J.empty, after: after });
      api.measure();   // the engine's first measure ran before api existed: once more with both languages
      box._api = api;
      // the count and the page number speak when the visitor changes them, not while the page loads
      (doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve()).then(function () {
        setTimeout(function () { [box.querySelector('.k-tally'), box.querySelector('.k-pi')].forEach(function (el) { if (el) el.setAttribute('aria-live', 'polite'); }); }, 0);
      });
      box._shown = function () { shown = true; if (ticks) ticks.classList.add('live'); };
      if (!anim) box._shown();
    });
  });

  /* ================================================================ gallery: year filter, 12 per page, in-place viewer,
     live list from Wix page code. The grid reserves the height of its tallest page and filter, so nothing moves. */
  run('gallery', function () {
    $$('[data-gallery]').forEach(function (gl) {
      function el(tag, cls, txt) { var n = doc.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
      var grid = gl.querySelector('.k-gl-grid'), all = $$('.k-gl-it', grid), size = +gl.getAttribute('data-size') || 12;
      var st = { year: 'all', page: 0 }, vis = all, keepPager = false;
      var pager = gl.querySelector('.k-pg'), pi = pager.querySelector('[data-pi]'), prev = pager.querySelector('[data-p="-1"]'), next = pager.querySelector('[data-p="1"]');
      var view = gl.querySelector('.k-gl-view'), vimg = doc.createElement('img'), vcap = view.querySelector('.k-gl-vcap'), vn = view.querySelector('.k-gl-vn');
      var cur = -1, opener = null, closing = 0;
      function pick(y) { return all.filter(function (f) { return y === 'all' || f.getAttribute('data-year') === y; }); }
      function show(list, p) { all.forEach(function (f) { f.hidden = true; }); list.slice(p * size, p * size + size).forEach(function (f) { f.hidden = false; }); }
      function counts() { $$('button[data-k="year"]', gl).forEach(function (b) { var c = b.querySelector('.k-bc'); if (c) c.textContent = pick(b.getAttribute('data-v')).length; }); }
      function apply(animate) {
        vis = pick(st.year);
        var pages = Math.max(1, Math.ceil(vis.length / size));
        if (st.page >= pages) st.page = pages - 1;
        show(vis, st.page); justify();
        pager.hidden = pages < 2 && !keepPager; pager.style.visibility = pages < 2 ? 'hidden' : '';
        pi.textContent = (st.page + 1) + ' / ' + pages;
        prev.disabled = st.page === 0; next.disabled = st.page >= pages - 1;
        $$('button[data-k="year"]', gl).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-v') === st.year)); });
        indicators(gl, animate);
      }
      // balanced justified rows on desktop: the row breaks that keep every row closest to a target height
      var narrow = window.matchMedia ? matchMedia('(max-width: 760px)') : { matches: false };
      function justify() {
        var fs = all.filter(function (f) { return !f.hidden; });
        all.forEach(function (f) { f.style.flex = ''; });
        grid.classList.remove('jx');
        if (narrow.matches || !fs.length) return;
        var W = grid.clientWidth - 1, gap = parseFloat(getComputedStyle(grid).columnGap) || 16;
        var T = Math.max(220, Math.min(320, W * 0.24)), n = fs.length, rs = fs.map(function (f) { return parseFloat(f.style.getPropertyValue('--r')) || 4 / 3; });
        var best = [0], from = [0];
        for (var i = 1; i <= n; i++) {
          best[i] = Infinity;
          for (var j = i - 1, S = 0; j >= 0; j--) {
            S += rs[j];
            var h = (W - gap * (i - j - 1)) / S, c = (i === n && h > T) ? 0 : (h - T) * (h - T);
            if (best[j] + c < best[i]) { best[i] = best[j] + c; from[i] = j; }
            if (h < T * 0.45) break;
          }
        }
        for (var e2 = n; e2 > 0; e2 = from[e2]) {
          var b = from[e2], S2 = 0, k;
          for (k = b; k < e2; k++) S2 += rs[k];
          var hh = Math.min((W - gap * (e2 - b - 1)) / S2, e2 === n ? T : Infinity);
          for (k = b; k < e2; k++) fs[k].style.flex = '0 0 ' + Math.floor(rs[k] * hh * 100) / 100 + 'px';
        }
        grid.classList.add('jx');
      }
      // the tallest page of any year, in both languages (captions wrap differently), so nothing moves on a language switch
      function reserve() {
        grid.style.minHeight = ''; keepPager = false;
        var max = 0, ys = $$('button[data-k="year"]', gl).map(function (b) { return b.getAttribute('data-v'); });
        var cl = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko';
        if (!ys.length) ys = ['all'];
        [cl, cl === 'en' ? 'ko' : 'en'].forEach(function (l) {
          root.setAttribute('data-lang', l);
          ys.forEach(function (y) {
            var li = pick(y), n = Math.ceil(li.length / size);
            if (n > 1) keepPager = true;
            for (var p = 0; p < n; p++) { show(li, p); justify(); max = Math.max(max, Math.ceil(grid.getBoundingClientRect().height)); }
          });
        });
        root.setAttribute('data-lang', cl);
        if (max) grid.style.minHeight = max + 'px';
        counts(); apply(false);
      }
      // the visible part of the gallery (the runtime's sentinel band, in document px)
      var bd = null;
      fontsIn.then(function () { R.onBand(function (b) { bd = b.ok ? b : null; }); });   // after the heights have settled
      function vband() { if (!bd) return null; var r = R.rect(gl); return { top: bd.top - r.top, bottom: bd.bottom - r.top }; }
      function fill() {
        var f = vis[cur], im = f.querySelector('img');
        vimg.src = f.getAttribute('data-full');
        if (!vimg.parentNode) view.querySelector('.k-gl-vimg').appendChild(vimg);
        vimg.alt = im ? im.alt : '';
        vcap.innerHTML = f.querySelector('figcaption').innerHTML;
        vn.textContent = (cur + 1) + ' / ' + vis.length;
      }
      var lastC = 0;
      function place(from) {
        var W = gl.offsetWidth, H = gl.offsetHeight, b = vband(), gr = gl.getBoundingClientRect();
        var r = parseFloat(vis[cur].style.getPropertyValue('--r')) || 4 / 3;
        if (W < 600) r = Math.max(r, 0.75);
        var bar = view.querySelector('.k-gl-vbar').offsetHeight + 50;
        var h = Math.min(H, W / r + bar, 760, Math.max(320, W * (W < 600 ? 1.6 : 0.62) + bar));
        if (b) h = Math.min(h, Math.max(320, b.bottom - b.top - 24));
        var c = b ? (b.top + b.bottom) / 2 : from ? (from.getBoundingClientRect().top + from.getBoundingClientRect().bottom) / 2 - gr.top : lastC;
        lastC = c;
        var top = Math.max(0, Math.min(H - h, c - h / 2));
        view.style.top = Math.round(top) + 'px'; view.style.height = Math.round(h) + 'px';
      }
      function open(i, from) {
        if (i < 0) return;
        clearTimeout(closing); cur = i; opener = from; fill();
        view.hidden = false; place(from);
        requestAnimationFrame(function () { view.classList.add('on'); });
        try { view.querySelector('.k-gl-close').focus({ preventScroll: true }); } catch (e) {}
      }
      function close(stay) {
        if (view.hidden) return;
        view.classList.remove('on');
        closing = setTimeout(function () { view.hidden = true; }, reduce ? 0 : 200);
        if (!stay && opener && doc.contains(opener)) try { opener.focus({ preventScroll: true }); } catch (e) {}
      }
      function stepTo(dx) { cur = (cur + dx + vis.length) % vis.length; fill(); place(null); }
      gl.addEventListener('click', function (ev) {
        var tg = ev.target.closest('button[data-k="year"]'), p = ev.target.closest('.k-pg [data-p]'), o = ev.target.closest('.k-gl-open');
        if (tg || (p && !p.disabled)) close(true);
        if (tg) { st.year = tg.getAttribute('data-v'); st.page = 0; apply(true); }
        if (p && !p.disabled) { st.page += +p.getAttribute('data-p'); apply(false); }
        if (o) open(vis.indexOf(o.parentNode), o);
        if (ev.target.closest('.k-gl-close')) close(false);
        if (ev.target.closest('.k-gl-prev')) stepTo(-1);
        if (ev.target.closest('.k-gl-next')) stepTo(1);
      });
      view.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape') { ev.preventDefault(); close(); }
        else if (ev.key === 'ArrowLeft') { ev.preventDefault(); stepTo(-1); }
        else if (ev.key === 'ArrowRight') { ev.preventDefault(); stepTo(1); }
        else if (ev.key === 'Tab') {
          var bs = $$('button', view), i = bs.indexOf(doc.activeElement);
          if (ev.shiftKey && i <= 0) { ev.preventDefault(); bs[bs.length - 1].focus({ preventScroll: true }); }
          else if (!ev.shiftKey && i === bs.length - 1) { ev.preventDefault(); bs[0].focus({ preventScroll: true }); }
        }
      });
      apply(false); reserve();
      var lastW = gl.offsetWidth, rt = 0;
      window.addEventListener('resize', function () { if (gl.offsetWidth === lastW) return; lastW = gl.offsetWidth; clearTimeout(rt); rt = setTimeout(reserve, 150); });
      if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(reserve);
      R.onLang(reserve);

      if (!gl.hasAttribute('data-live')) return;
      /* ---------- live list: {type:'gallery', items:[...]} replaces the baked photos (tools/pages_v2/gallery.md) ---------- */
      var got = '';
      function urls(it) {
        var s = String(it.src || it.media || '').trim(), id = '', name = String(it.file || ''), w = +it.width || 0, h = +it.height || 0, m;
        if ((m = /^wix:image:\/\/v1\/([^\/#]+)(?:\/([^#]*))?(?:#(.*))?$/.exec(s))) {
          id = m[1];
          try { name = name || decodeURIComponent(m[2] || ''); } catch (e) {}
          var fw = /originWidth=(\d+)/.exec(m[3] || ''), fh = /originHeight=(\d+)/.exec(m[3] || '');
          if (!w && fw) w = +fw[1]; if (!h && fh) h = +fh[1];
        } else if ((m = /^https:\/\/static\.wixstatic\.com\/media\/([^\/?#\s]+)/.exec(s))) id = m[1];
        else if (/^[\w.-]+~mv2\.[a-z]+$/i.test(s)) id = s;
        else if (/^https:\/\/[^\s"'<>]+$/.test(s)) return { src: s, mid: '', full: s, w: w, h: h };
        else return null;
        var stem = encodeURIComponent(String(name || id).replace(/\.[^.]*$/, '')) || 'photo';
        var u = function (px, q) { return 'https://static.wixstatic.com/media/' + id + '/v1/fit/w_' + px + ',h_' + px + ',q_' + q + ',enc_auto/' + stem + '.jpg'; };
        return { src: u(600, 80), mid: u(1200, 85), full: u(1600, 85), w: w, h: h };
      }
      function pair(ko, en, enOk) {
        var a = el('span', '', ko), b = el('span', '', en);
        a.setAttribute('data-l', 'ko'); b.setAttribute('data-l', 'en'); b.lang = enOk ? 'en' : 'ko';
        var s = el('span', 'k-cp'); s.appendChild(a); s.appendChild(b); return s;
      }
      function figure(it) {
        var u = urls(it); if (!u) return null;
        var ko = String(it.caption_ko || '').trim(), enOk = !!String(it.caption_en || '').trim(), en = enOk ? String(it.caption_en).trim() : ko;
        var y = (/\d{4}/.exec(String(it.year == null ? '' : it.year)) || [''])[0];
        var r = u.w > 0 && u.h > 0 ? u.w / u.h : 4 / 3;
        r = Math.min(4, Math.max(0.4, r));
        var f = el('figure', 'k-gl-it');
        f.style.setProperty('--r', r.toFixed(4)); f.setAttribute('data-year', y); f.setAttribute('data-full', u.full);
        var b = el('button', 'k-gl-open k-ph'); b.type = 'button';
        b.setAttribute('data-aria-ko', '크게 보기: ' + ko); b.setAttribute('data-aria-en', 'View larger: ' + en);
        var pp = el('span', 'k-pp'), im = el('img', 'k-im'); im.loading = 'lazy'; im.decoding = 'async'; im.width = 600; im.height = Math.round(600 / r);
        im.setAttribute('data-alt-ko', String(it.alt_ko || ko)); im.setAttribute('data-alt-en', String(it.alt_en || en));
        if (u.mid) { im.sizes = '(max-width: 760px) 50vw, 420px'; im.srcset = u.src + ' 600w, ' + u.mid + ' 1200w'; }
        im.src = u.src;
        pp.appendChild(im); b.appendChild(pp); f.appendChild(b);
        var fc = el('figcaption'); fc.appendChild(pair(ko, en, enOk));
        if (y && !(ko.indexOf(y) >= 0 && en.indexOf(y) >= 0)) fc.appendChild(el('span', 'k-cy', y));
        f.appendChild(fc);
        return f;
      }
      function toggles(ys) {
        var box = gl.querySelector('.k-gl-f');
        if (!box) return;
        var fb = box.querySelector('.k-fb'), ind = fb.querySelector('.k-ind');
        $$('button', fb).forEach(function (b) { fb.removeChild(b); });
        function add(v, labHtml) {
          var b = el('button'); b.type = 'button'; b.setAttribute('data-k', 'year'); b.setAttribute('data-v', v); b.setAttribute('aria-pressed', String(v === 'all'));
          b.innerHTML = '<span class="k-bl">' + labHtml + '</span> <span class="k-bc"></span>';
          fb.insertBefore(b, ind);
        }
        add('all', t2(['전체', 'All']));
        ys.forEach(function (y) { add(y, '<span class="k-num">' + esc(y) + '</span>'); });
        fb.classList.remove('has-ind');
        box.hidden = ys.length < 2;
      }
      function setItems(items) {
        var sig; try { sig = JSON.stringify(items); } catch (e) { return; }
        if (sig === got) return;
        var figs = items.slice(0, 500).map(figure).filter(Boolean);
        if (!figs.length) return;
        got = sig;
        if (!view.hidden) { view.classList.remove('on'); view.hidden = true; }
        grid.innerHTML = '';
        figs.forEach(function (f) { grid.appendChild(f); });
        all = figs;
        var ys = []; figs.forEach(function (f) { var y = f.getAttribute('data-year'); if (y && ys.indexOf(y) < 0) ys.push(y); });
        ys.sort(function (a, b) { return b.localeCompare(a); });
        toggles(ys);
        st = { year: 'all', page: 0 };
        R.setLang(R.lang);
        reserve();
        gl.setAttribute('data-source', 'live');
      }
      window.addEventListener('message', function (ev) {
        var d = ev.data;
        if (typeof d === 'string' && d.charAt(0) === '{') { try { d = JSON.parse(d); } catch (err) { return; } }
        if (d && d.type === 'gallery' && Array.isArray(d.items)) setItems(d.items);
      });
      function ready() { try { if (window.parent && window.parent !== window && !got) window.parent.postMessage({ type: 'ready' }, '*'); } catch (e) {} }
      ready(); setTimeout(ready, 1500); setTimeout(ready, 4000);
    });
  });

  /* ================================================================ video player: poster and playlist; plays only on click */
  run('video', function () {
    $$('[data-player]').forEach(function (pl) {
      var scr = pl.querySelector('.k-scr'), poster = scr.querySelector('.k-poster'), playBtn = scr.querySelector('.k-play');
      var items = $$('.k-plist button', pl), cur = 0, video = null;
      var nowT = pl.querySelector('.k-now-t'), nowM = pl.querySelector('.k-now-m');
      function title(b, l) { var n = b.querySelector('.k-pt [data-l="' + l + '"]'); return n ? n.textContent : ''; }
      function sync() {
        var b = items[cur]; if (!b) return;
        nowT.innerHTML = b.querySelector('.k-pt').innerHTML;
        nowM.textContent = b.querySelector('.k-pm').textContent;
        playBtn.setAttribute('data-aria-ko', '재생: ' + title(b, 'ko'));
        playBtn.setAttribute('data-aria-en', 'Play: ' + title(b, 'en'));
        playBtn.setAttribute('aria-label', R.lang === 'en' ? 'Play: ' + title(b, 'en') : '재생: ' + title(b, 'ko'));
      }
      function stop() { if (video) { video.pause(); video.removeAttribute('src'); video.load(); scr.removeChild(video); video = null; } scr.classList.remove('on'); }
      function start() {
        var b = items[cur]; stop();
        video = doc.createElement('video');
        video.controls = true; video.playsInline = true; video.preload = 'metadata';
        video.poster = b.getAttribute('data-poster'); video.src = b.getAttribute('data-src');
        video.setAttribute('aria-label', title(b, R.lang));
        scr.appendChild(video); scr.classList.add('on');
        var p = video.play(); if (p && p.catch) p.catch(function () {});
        try { video.focus({ preventScroll: true }); } catch (e) {}
      }
      function select(i, play) {
        cur = i;
        items.forEach(function (b, j) { b.setAttribute('aria-current', String(j === i)); });
        stop(); poster.src = items[i].getAttribute('data-poster'); sync();
        if (play) start();
      }
      playBtn.addEventListener('click', start);
      items.forEach(function (b, i) { b.addEventListener('click', function () { select(i, true); }); });
    });
  });

  /* ================================================================ one height for both languages
     The Wix element has one fixed height for KO and EN. Each [data-lk] block reserves the taller of its two languages
     (both measured in one synchronous pass, never painted), so switching the language never moves anything. Runs after
     the lists and the gallery have reserved their heights (their hooks are registered first). */
  run('lock', function () {
    // innermost blocks first: a section is measured with its nested blocks (list controls) already locked, else the
    // stacked column at 320 could outgrow the section's lock by what the nested lock adds
    function lock() {
      var els = $$('[data-lk]'), cur = root.getAttribute('data-lang') === 'en' ? 'en' : 'ko', top = 0;
      els.forEach(function (el) { el.style.minHeight = ''; });
      var lv = els.map(function (el) { var n = 0, x = el.parentElement; while (x) { if (x.hasAttribute('data-lk')) n++; x = x.parentElement; } top = Math.max(top, n); return n; });
      for (var L = top; L >= 0; L--) {
        var set = els.filter(function (el, i) { return lv[i] === L; });
        var a = set.map(function (el) { return el.getBoundingClientRect().height; });
        root.setAttribute('data-lang', cur === 'en' ? 'ko' : 'en');
        var b = set.map(function (el) { return el.getBoundingClientRect().height; });
        root.setAttribute('data-lang', cur);
        set.forEach(function (el, i) { el.style.minHeight = Math.ceil(Math.max(a[i], b[i])) + 'px'; });
      }
    }
    R.lock = lock;
    lock();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(lock);
    R.onLang(lock);
    // a face first needed by the other language (measured above while hidden) loads only now: measure again once it is in
    if (doc.fonts && doc.fonts.addEventListener) {
      var fl = 0;
      doc.fonts.addEventListener('loadingdone', function () {
        clearTimeout(fl);
        fl = setTimeout(function () { $$('[data-list]').forEach(function (b) { if (b._api) b._api.measure(); }); lock(); }, 120);
      });
    }
    var lw = root.clientWidth, lz = 0;
    window.addEventListener('resize', function () { clearTimeout(lz); lz = setTimeout(function () { if (root.clientWidth !== lw) { lw = root.clientWidth; lock(); } }, 260); });
  });

  /* ================================================================ motion (GSAP; none under reduced motion) */
  run('motion', function () {
    if (!g) { R.showAll(); return; }
    if (reduce) return;
    function safe(fn) { return function (el) { try { fn(el); } catch (err) { if (window.console) console.error(err); R.showAll(); } }; }
    var FILTER = 'saturate(0.86) contrast(0.97) brightness(1.02)';
    function decoded(ims, cap) {
      return Promise.race([Promise.all(ims.map(function (im) {
        if (!im || !im.decode) return null;
        return im.decode().catch(function () {});
      })), wait(cap)]);
    }
    // frames are cut open like the hero: an ink line through the middle, a beat, the picture opens from it (both ways)
    // with its rack focus. Waits for the pictures (600 ms at most).
    function cutOpen(el, phs, at) {
      var pps = phs.map(function (p) { return p.querySelector('.k-pp, .k-ini'); }).filter(Boolean);
      var cuts = phs.map(function (p) { return p.querySelector('.k-cut'); }).filter(Boolean);
      var ims = phs.map(function (p) { return p.querySelector('.k-im'); }).filter(Boolean);
      var blur = ims.filter(function (im) { return !im.closest('.k-plate'); });
      g.set(pps, { clipPath: 'inset(50% 0% 50% 0%)' }); g.set(blur, { scale: 1.08, filter: 'blur(9px)' });
      el.classList.add('is-cut');
      ims.forEach(function (im) { if (im.loading === 'lazy') im.loading = 'eager'; });
      var over = false, gate = null;
      var clear = function () { g.set(pps.concat(cuts, ims), { clearProps: 'transform,opacity,visibility,clipPath,filter' }); el.classList.remove('is-cut'); };
      keep({ progress: function () { over = true; if (gate) gate.progress(1); else clear(); } });
      decoded(ims, 600).then(function () {
        if (over) return;
        var s = Math.min(.08, .6 / Math.max(1, pps.length));
        gate = keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: clear, delay: at || 0 })
          .to(cuts, { scaleX: 1, duration: .4, stagger: s, ease: EDRAW }, 0)
          .fromTo(pps, { clipPath: 'inset(50% 0% 50% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, stagger: s, ease: EGATE }, .55)
          .to(cuts, { autoAlpha: 0, duration: .3, stagger: s, ease: 'power1.in' }, .8)
          .to(blur, { scale: 1, filter: 'blur(0px)', duration: 1.4, stagger: s, ease: 'power2.out' }, .59));
      }, clear);
    }
    // a block: its hairlines are drawn, its items rise, its frames are cut open; a block without parts rises as one
    function rise(el) {
      var ru = $$('.k-rule', el), ai = $$('[data-ai]', el), ph = $$('.k-ph', el);
      var late = ai.filter(function (x) { return x.closest('.k-mem'); }), early = ai.filter(function (x) { return !x.closest('.k-mem'); });
      var whole = !ai.length && !ru.length && !ph.length;
      if (ru.length) g.set(ru, { scaleX: 0 });
      if (ai.length) g.set(ai, { autoAlpha: 0, y: 14 });
      g.set(el, whole ? { autoAlpha: 0, y: 16 } : { autoAlpha: 1 });
      el.classList.add('on');
      var tl = keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: function () { g.set(ru.concat(ai, [el]), { clearProps: 'transform,opacity,visibility' }); } }));
      if (whole) tl.to(el, { autoAlpha: 1, y: 0, duration: .9 }, 0);
      if (ru.length) tl.to(ru, { scaleX: 1, duration: .8, stagger: .08, ease: EDRAW }, 0);
      if (early.length) tl.to(early, { autoAlpha: 1, y: 0, duration: .8, stagger: Math.min(.06, .5 / early.length) }, ru.length ? .12 : 0);
      if (late.length) tl.to(late, { autoAlpha: 1, y: 0, duration: .6, stagger: Math.min(.08, .6 / late.length) }, .95);
      if (ph.length) cutOpen(el, ph, ru.length ? .1 : 0);
    }
    // a section head: the cut line across the grid is drawn, the heading rises through its mask, the note follows
    function head(el) {
      var inn = el.parentNode, ln = inn ? inn.querySelector(':scope > .k-ln') : null;
      var hl = el.querySelector('.k-hl'), rest = $$(':scope > :not(.k-h):not([data-a])', el);
      if (ln) { g.set(ln, { scaleX: 0 }); ln.classList.add('on'); }
      if (hl) g.set(hl, { yPercent: 108 });
      if (rest.length) g.set(rest, { autoAlpha: 0, y: 10 });
      el.classList.add('on');
      var tl = keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: function () { g.set([ln, hl].concat(rest).filter(Boolean), { clearProps: 'transform,opacity,visibility' }); } }));
      if (ln) tl.to(ln, { scaleX: 1, duration: .8, ease: EDRAW }, 0);
      if (hl) tl.to(hl, { yPercent: 0, duration: 1.05 }, .08);
      if (rest.length) tl.to(rest, { autoAlpha: 1, y: 0, duration: .7, stagger: .06 }, .3);
    }
    // chapter heading: the authored lines rise through their masks
    function chap(h) {
      var ls = $$('[data-l="' + R.lang + '"] .l', h);
      g.set(ls, { yPercent: 108 });
      h.classList.add('on');
      keep(g.to(ls, { yPercent: 0, duration: 1.05, stagger: .1, ease: 'expo.out', clearProps: 'transform' }));
    }
    // leads: the lines rise into focus (the hero's statement and its rack focus)
    function leadIn(w) {
      fontsIn.then(safe(function () {
        var p = w.querySelector('[data-l="' + R.lang + '"]') || w.firstElementChild;
        var sp = ST ? new ST(p, { type: 'lines', mask: 'lines', linesClass: 'k-ll' }) : null;
        var tg = sp ? sp.lines : [p];
        g.set(tg, sp ? { yPercent: 135, filter: 'blur(6px)' } : { autoAlpha: 0, y: 14, filter: 'blur(6px)' });
        w.classList.add('on');
        keep(g.to(tg, { yPercent: 0, y: 0, autoAlpha: 1, filter: 'blur(0px)', duration: 1, stagger: .08, ease: 'expo.out',
          onComplete: function () { if (sp) sp.revert(); else g.set(tg, { clearProps: 'all' }); } }));
      }));
    }
    // the record as counter wheels: every digit starts at 0 and lower places travel a full turn further
    function wheels(nums) {
      var out = [];
      nums.forEach(function (n, ni) {
        var s = n.getAttribute('data-n'), html = '';
        for (var i = 0; i < s.length; i++) {
          var k = i * 10 + (+s.charAt(i)), cells = '';
          for (var j = 0; j <= k; j++) cells += '<span>' + (j % 10) + '</span>';
          html += '<span class="k-dg"><span class="k-strip">' + cells + '</span></span>';
        }
        n.innerHTML = html;
        $$('.k-strip', n).forEach(function (st) { var k = st.children.length - 1; out.push({ el: st, to: -100 * k / (k + 1), n: ni }); });
      });
      return out;
    }
    function rec(el) {
      var items = $$('[data-ai]', el), nums = $$('.k-dgw', el);
      var wh = wheels(nums);
      g.set(items, { autoAlpha: 0, y: 12 }); g.set(el, { '--rs': '0%' });
      el.classList.add('on');
      var tl = keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: function () {
        nums.forEach(function (n) { n.textContent = n.getAttribute('data-n'); });
        g.set(items, { clearProps: 'transform,opacity,visibility' }); el.style.removeProperty('--rs');
      } }));
      tl.to(el, { '--rs': '100%', duration: .8, ease: EDRAW }, 0).to(items, { autoAlpha: 1, y: 0, duration: .7, stagger: .07 }, .1);
      wh.forEach(function (w) { tl.to(w.el, { yPercent: w.to, duration: 1.4, ease: 'power4.out' }, .12 + w.n * .07); });
    }
    // the list: the controls settle, the reel runs through its frames, the first page comes up
    function listIn(lw) {
      var box = lw.closest('[data-list]'), ctl = box.querySelector('.k-ctl'), rows = $$('.k-row', lw), tk = $$('.k-reel i', box), pg = lw.querySelector('.k-pg'), ft = lw.querySelector('.k-ls-foot');
      var parts = [ctl, pg, ft].filter(Boolean);
      g.set(parts, { autoAlpha: 0, y: 10 }); g.set(rows, { autoAlpha: 0, y: 12 }); g.set(tk, { scaleY: 0 });
      lw.classList.add('on'); if (ctl) ctl.classList.add('on');
      keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: function () {
        g.set(parts.concat(rows, tk), { clearProps: 'transform,opacity,visibility' });
        if (box._shown) box._shown();
      } })
        .to(ctl, { autoAlpha: 1, y: 0, duration: .7 }, .05)
        .to(tk, { scaleY: function (i) { return tk[i].classList.contains('on') ? 1 : .42; }, duration: .5, stagger: Math.min(.003, .4 / Math.max(1, tk.length)) }, .12)
        .to(rows, { autoAlpha: 1, y: 0, duration: .7, stagger: .03 }, .1)
        .to(pg ? [pg].concat(ft ? [ft] : []) : [], { autoAlpha: 1, y: 0, duration: .6 }, .4));
    }
    // the inner-page hero: the ink line is drawn (CSS), the title lands (both layers on one timetable), the line holds a
    // beat and splits, the frame opens from it onto the decoded picture with its rack focus, the rest follows
    function heroIn(h) {
      if (h._run) return; h._run = 1;
      var f = h.querySelector('.k-hf'), et = h.querySelector('.k-he-t'), eb = h.querySelector('.k-he-b');
      var tk = h.querySelector('.k-hk'), tw = h.querySelector('.k-hw'), med = h.querySelector('.k-hmed'), im = h.querySelector('.k-himg'), logo = h.querySelector('.k-hlogo');
      var inst = h.querySelector('.k-hinst'), low = h.querySelector('.k-hlow'), splits = [];
      function pick(layer) { return layer ? (layer.querySelector('.k-ht[data-l="' + R.lang + '"]') || layer.querySelector('.k-ht:not([data-l])')) : null; }
      var a = pick(tk), b = pick(tw), ma = [], mb = [];
      var latin = !!(a && a.getAttribute('lang') === 'en');
      if (ST && a && !tk.classList.contains('sr')) {
        var o = { type: latin ? 'words,lines' : 'chars,lines', mask: 'lines', linesClass: 'k-tl' };
        var s1 = new ST(a, o); splits.push(s1); ma = latin ? s1.words : s1.chars;
        if (b) { var s2 = new ST(b, o); splits.push(s2); mb = latin ? s2.words : s2.chars; }
      }
      var sx = 0, m = /matrix\(([-\d.e]+)/.exec(getComputedStyle(et).transform || '');
      if (m) sx = Math.max(0, Math.min(1, parseFloat(m[1])));
      et.style.animation = 'none';
      g.set(et, { scaleX: sx, autoAlpha: 1, y: 0 }); g.set(eb, { scaleX: 1, autoAlpha: 0, y: 0 });
      if (ma.length) g.set(ma.concat(mb), { yPercent: 118 });
      var kids = (low ? [].slice.call(low.children) : []), quiet = [inst].concat(kids).filter(Boolean);
      g.set(quiet, { autoAlpha: 0, y: 14 });
      if (med) g.set(med, { filter: FILTER + ' blur(' + (phone() ? 6 : 10) + 'px)', scale: 1.05 });
      if (logo) g.set(logo, { autoAlpha: 0, scale: .97 });
      function gateTo(p) { var v = p.toFixed(2) + '%'; f.style.clipPath = 'inset(' + v + ' 0% ' + v + ' 0%)'; }
      gateTo(50);
      $$('[data-a]', h).forEach(function (x) { x.classList.add('on'); });
      var left = 2;
      function done() {
        if (--left > 0) return;
        splits.forEach(function (s) { try { s.revert(); } catch (e) {} });
        f.style.clipPath = '';
        g.set([med, logo].concat(quiet).filter(Boolean), { clearProps: 'transform,opacity,visibility,filter' });
        h.classList.add('is-done');
      }
      var draw = (1 - sx) * .45, open = Math.max(draw + .3, .5);
      var half = function () { return f.getBoundingClientRect().height / 2 + .5; };
      var gate = { p: 50 };
      var gtl = keep(g.timeline({ paused: true, onComplete: done })
        .set(eb, { autoAlpha: 1 }, 0)
        .to(gate, { p: 0, duration: 1.05, ease: EGATE, onUpdate: function () { gateTo(gate.p); } }, 0)
        .to(et, { y: function () { return -half(); }, duration: 1.05, ease: EGATE }, 0)
        .to(eb, { y: function () { return half(); }, duration: 1.05, ease: EGATE }, 0)
        .to([et, eb], { autoAlpha: 0, duration: .45, ease: 'power1.in' }, .62));
      if (med) gtl.to(med, { filter: FILTER + ' blur(0px)', scale: 1, duration: 1.6, ease: 'power2.out' }, .05);
      if (logo) gtl.to(logo, { autoAlpha: 1, scale: 1, duration: 1, ease: 'expo.out' }, .5);
      var pic = new Promise(function (res) {
        if (!im) return res();
        var dec = function () { var q = im.decode ? im.decode() : null; if (q && q.then) q.then(res, res); else res(); };
        if (im.complete && im.naturalWidth) dec(); else { im.addEventListener('load', dec, { once: true }); im.addEventListener('error', res, { once: true }); }
      });
      var tl = keep(g.timeline({ defaults: { ease: 'expo.out' }, onComplete: done }));
      tl.to(et, { scaleX: 1, duration: draw, ease: EDRAW }, 0);
      if (ma.length) tl.to(ma, { yPercent: 0, duration: .92, stagger: latin ? .07 : .05 }, .04).to(mb, { yPercent: 0, duration: .92, stagger: latin ? .07 : .05 }, .04);
      tl.call(function () { Promise.race([pic, wait(1000)]).then(function () { if (!gtl.progress()) gtl.play(); }); }, null, open);
      if (inst) tl.to(inst, { autoAlpha: 1, y: 0, duration: .8 }, open + .4);
      if (kids.length) tl.to(kids, { autoAlpha: 1, y: 0, duration: .9, stagger: .08 }, open + .46);
    }
    var OPT = { head: { threshold: .5, px: 60 }, chap: { threshold: .35, px: 60 }, lead: { threshold: .4, px: 50 }, list: { threshold: .08, px: 160 },
      rec: { threshold: .4, px: 40 }, rise: { threshold: .15, px: 140 } };
    var MOT = { head: head, chap: chap, lead: leadIn, list: listIn, rec: rec, rise: rise };
    $$('[data-a]').forEach(function (el) {
      if (el.closest('.cx')) return;                                           // the Home hero has its own script
      var m = el.getAttribute('data-m') || 'rise';
      if (m === 'ln' || m === 'ctl' || m === 'hp') return;                     // drawn by their head, their list, their hero
      R.inview(el, safe(MOT[m] || rise), OPT[m] || OPT.rise);
    });
    var hero = doc.querySelector('.k-hero');
    if (hero) {
      var en = R.lang === 'en', tx = (hero.querySelector('.k-hk .k-ht[data-l="' + R.lang + '"], .k-hk .k-ht:not([data-l])') || {}).textContent || '';
      var lat = !/[가-힣]/.test(tx);
      var face = Promise.resolve();
      try { if (doc.fonts && doc.fonts.load) face = doc.fonts.load(lat ? '860 100px Archivo' : '400 100px "Black Han Sans"', tx || 'A').catch(function () {}); } catch (e) {}
      var go = safe(heroIn), safety = setTimeout(function () { go(hero); }, 2200);
      Promise.race([face, wait(600)]).then(function () { R.inview(hero, function (h) { clearTimeout(safety); go(h); }, { threshold: .1, px: 120 }); });
    }

    // scroll: images load before they reach the screen (rootMargin is ignored in the Wix iframe: the sentinel band says
    // how far the visible part is); the hero photograph and the faculty portraits drift a little against the page
    function bands() {
      var lazy = $$('img[loading="lazy"]').map(function (im) { return { im: im, top: null }; });
      R.onBand(function (b) {
        if (!b.ok || !lazy.length) return;
        lazy = lazy.filter(function (o) {
          if (o.top === null) o.top = R.rect(o.im).top;
          if (o.top < b.bottom + 1400) { o.im.loading = 'eager'; return false; }
          return true;
        });
      });
      if (phone()) return;
      var drift = [];
      var hp = doc.querySelector('.k-hero .k-hpar');
      if (hp) {
        var qh = g.quickTo(hp, 'y', { duration: .6, ease: 'power3.out' });
        drift.push(function (b) { var r = R.rect(hp.parentNode), d = Math.max(0, Math.min(b.top - r.top, r.h)); qh(d * .08); });
      }
      $$('.k-ppl--l .k-pp').forEach(function (pp) {
        var q = g.quickTo(pp, 'yPercent', { duration: .8, ease: 'power3.out' });
        drift.push(function () { var p = R.progress(R.rect(pp.parentNode)); if (p !== null) q((.5 - p) * 7); });
      });
      if (drift.length) R.onBand(function (b) { if (b.ok) drift.forEach(function (fn) { fn(b); }); });
    }
    fontsIn.then(function () { requestAnimationFrame(function () { requestAnimationFrame(bands); }); });
  });
})();
"""
