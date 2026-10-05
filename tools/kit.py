#!/usr/bin/env python3
"""RIHE design system ("Cochlea"), shared by every page in tools/pages/*.py.

Read tools/KIT.md first. In short:

    import kit
    from kit import t, link, more, sec

    def render():
        body = kit.page_hero(t('연구실', 'Labs'), lead=t('...', '...'))
        body += sec(t('소개', 'About'), kit.prose([('한국어 문단', 'English paragraph')]))
        return kit.page('Labs', 'navy', body)

Everything returns plain HTML strings. Every visible string is a KO/EN pair made with t().
Copy that is shared between pages (labs, research areas, director, data centers, names) lives
in the COPY section below; the rest of the round-1 copy is in tools/build_v1.py.
"""
import html
import html.parser
import json
import math
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.smilesnail.org'
# English pages live under SITE + EN_PREFIX + path. Wix Multilingual is OFF on the live site today,
# so /en/... returns 404 until it is enabled. Set EN_PREFIX = '' to keep English links on the Korean URLs.
EN_PREFIX = '/en'
PREVIEW = False          # build.py sets this; True adds the small KO/EN toggle

# Noto Sans KR (reading) and DM Mono (measurements) load normally. Hahmlet (display only) is requested with
# Google Fonts' text= parameter: page() collects every character set in a serif element and asks for just those
# glyphs, one small file instead of ~340 KB of Korean slices. Anything set in Hahmlet must therefore use an element
# listed in SERIF_TAGS / SERIF_CLASSES (or the .serif utility class).
FONT_URL = 'https://fonts.googleapis.com/css2?family=DM+Mono:wght@400&family=Noto+Sans+KR:wght@400;500&display=swap'
SERIF_URL = 'https://fonts.googleapis.com/css2?family=Hahmlet:wght@300;400&display=swap&text='
SERIF_TAGS = {'h1', 'h2', 'h3'}
SERIF_CLASSES = {'serif', 'oc-n', 'nm', 'ini', 't', 'pt', 'ft-nm'}   # .pt: video titles are copied into the serif .now .t


def load(name):
    with open(os.path.join(ROOT, 'data', name + '.json'), encoding='utf-8') as f:
        return json.load(f)


PUBS, REPORTS, PATENTS = load('publications'), load('reports'), load('patents')
PEOPLE, GALLERY, VIDEOS = load('people'), load('gallery'), load('videos')
TEAMS = {tm['key']: tm for tm in PEOPLE}

# ================================================================== tokens
COLORS = {'navy': '#1b3d6f', 'basic': '#2e8b57', 'hearing': '#4e7595', 'head': '#2e6e9e',
          'audiso': '#9a6f07', 'collab': '#7a8494', 'ink': '#131b2a'}
PATHS = {'home': '/', 'about': '/about', 'research': '/project', 'people': '/people', 'basic-lab': '/about-1',
         'hearing-lab': '/hearing-lab', 'head-lab': '/head-lab', 'audiso': '/audiso', 'contact': '/연락처',
         'gallery': '/gallery'}

# ================================================================== COPY (from tools/build_v1.py unless noted)
INST = ('연세대학교 원주세브란스기독병원', 'Yonsei University · Wonju Severance Christian Hospital')
NAME = ('청각재활연구소', 'Research Institute of Hearing Enhancement')
MISSION = ('난청의 기전에 대한 기초 연구를 바탕으로 치료제 개발, 임상 연구, 의료기기 개발까지 청각에 대한 전주기적 연구를 하는 연구소입니다.',
           'Built on basic research into the mechanisms of hearing loss, we conduct full-cycle hearing research, '
           'from drug development and clinical research to medical devices.')

# Research areas. The Korean titles are new in round 2 and need the client's confirmation.
AREAS = [
    dict(key='basic', ko='기초 연구', en='Basic sciences',
         d_ko='자성 나노입자로 줄기세포가 달팽이관으로 모이는 <span class="nw">효율(호밍)을</span> 높이고, 엑소좀·약물·재생 유전자를 유모세포에 전달합니다.',
         d_en='Enhancing stem-cell homing to the cochlea with nanoparticles and magnetic force, delivering exosomes, drugs and regenerative genes to hair cells.'),
    dict(key='data', ko='빅데이터·인공지능', en='Big data &amp; AI',
         d_ko='국내 유일의 한국인 청각 참조표준 데이터센터로서 청각 데이터의 표준을 만들고, 어지럼증 데이터를 인공지능으로 분석합니다.',
         d_en='As Korea’s only reference standard data center for hearing, we set standards for hearing data and analyse dizziness data with AI.'),
    dict(key='device', ko='의료기기', en='Medical devices',
         d_ko='마취 없이 시술하는 원스톱 중이염 환기관, 스마트 안진검사, VR 어지럼증 재활, 골전도 보청기 등 임상 수요에서 출발한 의료기기를 개발합니다.',
         d_en='A one-stop ventilation tube without anaesthesia, smart nystagmography, VR dizziness rehabilitation and bone conduction hearing aids, built from clinical needs.'),
    dict(key='clinical', ko='임상시험', en='Clinical trials',
         d_ko='골전도 보청기 임상시험을 중심으로, 기초 연구의 성과(엑소좀, 약물, 의료기기)를 임상시험으로 이어 갑니다.',
         d_en='Mainly clinical trials of bone conduction hearing aids; outputs of our basic research (exosomes, drugs, devices) move on to clinical trials.'),
]

LABS = [
    dict(key='basic', page='basic-lab', name='Basic Lab', team_ko='기초팀', team_en='Basic research team',
         d_ko='줄기세포·나노입자·약물 전달로 난청의 기전을 연구합니다.', d_en='Stem cells, nanoparticles and drug delivery for the mechanisms of hearing loss.'),
    dict(key='hearing', page='hearing-lab', name='Hearing Lab', team_ko='참조표준팀', team_en='Reference standard team',
         d_ko='한국인 청각 참조표준 데이터를 수집·생산합니다.', d_en='Collecting and producing Korean reference hearing data.'),
    dict(key='head', page='head-lab', name='HeAD Lab', team_ko='데이터팀', team_en='Data team',
         d_ko='청각 빅데이터와 인공지능으로 난청을 예측하고 관리합니다.', d_en='Hearing big data and AI for predicting and managing hearing loss.'),
    dict(key='audiso', page='audiso', name='Audiso', team_ko='오디에스오(주)', team_en='Audiso Co., Ltd.',
         d_ko='국내 최초 청력계 KOLAS 국제공인교정기관, 연구소 교원창업 기업입니다.', d_en='Korea’s first KOLAS-accredited audiometer calibration body; a faculty start-up of the institute.'),
]
LAB = {lb['key']: lb for lb in LABS}

TECH_TRANSFERS = 12      # 기술이전 건수: not in data/*.json; from the round-1 copy (build_v1.py)

DIRECTOR = dict(
    name_ko='서영준', name_en='Young Joon Seo', role_ko='연구소장', role_en='Director',
    photo='https://i.imgur.com/vIAp69Y.jpeg', email='okas2000@yonsei.ac.kr',
    lines_ko=['연세대학교 원주의과대학 이비인후과 주임교수', '연세대학교 미래캠퍼스 디지털헬스케어학과 겸임교수',
              '연세대학교 원주의과대학원 의학통계학과 겸임교수', '대한청각학회 연구이사 · 차세대 한림원 회원(2022.1~)'],
    lines_en=['Professor and Chair, Department of Otorhinolaryngology, Yonsei University Wonju College of Medicine',
              'Adjunct Professor, Department of Digital Healthcare, Yonsei University Mirae Campus',
              'Adjunct Professor, Department of Medical Statistics, Yonsei University Wonju Graduate School of Medicine',
              'Director of Research, Korean Audiological Society · Member, Young Korean Academy of Science and Technology (since 2022)'],
    # shorter English credentials for Home, so EN is not much taller than KO in the fixed-height iframe
    lines_en_short=['Professor and Chair, Otorhinolaryngology, Yonsei Wonju College of Medicine',
                    'Adjunct Professor, Digital Healthcare and Medical Statistics, Yonsei University',
                    'Director of Research, Korean Audiological Society · Member, Young Korean Academy of Science and Technology (since 2022)'],
    greeting_ko=('난청을 치료하는 임상의이자 난청을 연구하는 연구자로서, 청각재활연구소를 기반으로 융합 연구자의 길을 걸어왔습니다. '
                 '2015년부터 다양한 융합 연구를 선보인 연구소입니다. 세계 여러 나라 청각 특성화 연구소들과 어깨를 나란히 견줄 수 있는 연구소가 되겠습니다.'),
    greeting_en=('As a clinician who treats patients with hearing loss and a researcher who studies its pathophysiology, I have walked the path of a '
                 'translational researcher based on our Institute. Since 2015 the Institute has pursued a wide range of translational research, '
                 'and we will stand shoulder to shoulder with hearing research institutes around the world.'),
)

DATA_CENTERS = [
    dict(key='hearing', logo='https://i.imgur.com/s6VfJ2r.png', logo_w=252, logo_h=42, logo_cls='l1',
         ko='한국인 청각 참조표준데이터센터', en='Korea Hearing Standard-data Center',
         d_ko='한국인의 청각 분야 데이터를 수집·생산하고 보급하는 국내 유일 기관. 2019년 1월부터 운영.',
         d_en='Korea’s only center collecting, producing and distributing Korean hearing data, since January 2019.'),
    dict(key='head', logo='https://i.imgur.com/9cFssq8.png', logo_w=226, logo_h=62, logo_cls='l2',
         ko='청각 빅데이터센터', en='Korea Hearing Big-data Center',
         d_ko='산업계와 연구자에게 청각 분야의 빅데이터를 전문으로 제공하는 국내 유일 기관. 10만 건 이상의 데이터.',
         d_en='Korea’s only provider of hearing big data for industry and researchers, with over 100,000 records.'),
]

NAME_EN = {'서영준': 'Young Joon Seo', '공태훈': 'Tae Hoon Kong', '기재홍': 'Jaehong Key', '변유선': 'Yuseon Byun', '이동혁': 'Donghyeok Lee',
           '윤철영': 'Chul Young Yoon', '이현수': 'Hyun Su Lee', '전진희': 'Jinhui Jeon', '강철영': 'Chulyoung Kang'}
ROLE_EN = {'교수': 'Professor', '연구소장': 'Director', '연구교수': 'Research Professor', '팀장': 'Team Leader', 'Post-doc': 'Postdoctoral Researcher',
           '박사과정': 'Ph.D. Student', '석사과정': 'M.S. Student', '학부연구원': 'Undergraduate Researcher', '연구원': 'Researcher',
           '연구간호사': 'Research Nurse', 'CTO': 'CTO', '개발': 'Development', 'AI개발': 'AI Development', '영업': 'Sales', 'QA': 'QA',
           '인증': 'Certification', '전략': 'Strategy', '이비인후과': 'Otorhinolaryngology', '생체공학과': 'Biomedical Engineering'}
# people.json team key -> (colour key, KO heading, EN heading)
TEAM_META = {'faculty': ('navy', '교수진', 'Faculty'), 'basic': ('basic', '기초팀 · Basic Lab', 'Basic Lab'),
             'hearing': ('hearing', '참조표준팀 · Hearing Lab', 'Hearing Lab'), 'head': ('head', '데이터팀 · HeAD Lab', 'HeAD Lab'),
             'admin': ('ink', '행정팀', 'Administration'), 'audiso': ('audiso', '오디에스오(주) · Audiso', 'Audiso')}
# publication team key -> (KO, EN) label used in lists
TEAM_LABEL = {'basic': ('Basic Lab', 'Basic Lab'), 'hearing': ('Hearing Lab', 'Hearing Lab'),
              'head': ('HeAD Lab', 'HeAD Lab'), 'collab': ('협력·임상', 'Collab &amp; Medical')}
UI = {'all': ('전체', 'All'), 'team': ('팀', 'Team'), 'year': ('연도', 'Year'), 'status': ('구분', 'Status'),
      '등록': ('등록', 'Granted'), '출원': ('출원', 'Filed'), '대한민국': ('대한민국', 'Korea'), '미국': ('미국', 'USA'),
      '중국': ('중국', 'China'), '유럽': ('유럽', 'Europe'), 'prev': ('이전 페이지', 'Previous page'), 'next': ('다음 페이지', 'Next page'),
      'none': ('해당 조건의 항목이 없습니다.', 'No items match this filter.')}
UI['country'] = ('국가', 'Country')      # patents list: country filter (Research page)

e = html.escape


# ================================================================== helpers
def t(ko, en=None, tag='span', cls='', attrs=''):
    """KO/EN pair. t('연구소', 'Institute') -> <span data-l="ko">연구소</span><span data-l="en" lang="en">Institute</span>.
    en=None means the text is the same in both languages (no data-l wrapper; returned as is unless tag/cls/attrs given)."""
    c = f' class="{cls}"' if cls else ''
    a = f' {attrs}' if attrs else ''
    if en is None:
        return f'<{tag}{c}{a}>{ko}</{tag}>' if (cls or attrs or tag != 'span') else ko
    return f'<{tag}{c}{a} data-l="ko">{ko}</{tag}><{tag}{c}{a} data-l="en" lang="en">{en}</{tag}>'


def tt(pair, tag='span', cls='', attrs=''):
    """t() for a (ko, en) tuple."""
    return t(pair[0], pair[1], tag, cls, attrs)


def url(path):
    """Absolute production URL of a site path or page name ('people' or '/people')."""
    return SITE + PATHS.get(path, path)


def link(path, inner, cls='', attrs=''):
    """Link to another page of the site. path is a page name from PATHS or a site path ('/project#patents').
    English rewriting (EN_PREFIX) happens in the browser through data-path."""
    p = PATHS.get(path, path)
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{SITE}{p}" target="_top" data-path="{p}"{" " + attrs if attrs else ""}>{inner}</a>'


def ext(href, inner, cls='', attrs=''):
    """External link (new tab)."""
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{href}" target="_blank" rel="noopener"{" " + attrs if attrs else ""}>{inner}</a>'


def more(path, ko, en=None, cls='', d=None, external=False):
    """Navy text link with a moving arrow: '연구소 소개 →'."""
    c = 'more' + (' ' + cls if cls else '')
    inner = t(ko, en) + f'<i aria-hidden="true">{"↗" if external else "→"}</i>'
    st = f'style="--d:{d}"' if d is not None else ''
    return ext(path, inner, c, st) if external else link(path, inner, c, st)


def img(src, alt=('', ''), w=None, h=None, cls='', lazy=True, srcset='', sizes='', attrs=''):
    """<img>. alt is a (ko, en) pair (swapped by language) or '' for decorative images."""
    if isinstance(alt, str):
        alt = (alt, alt)
    a = f' alt="{e(alt[0])}"'
    if alt[1] and alt[1] != alt[0]:
        a += f' data-alt-en="{e(alt[1])}"'
    c = f' class="{cls}"' if cls else ''
    out = f'<img{c} src="{src}"{a}'
    if w:
        out += f' width="{w}" height="{h}"'
    if srcset:
        out += f' srcset="{srcset}" sizes="{sizes}"'
    if lazy:
        out += ' loading="lazy"'
    return out + (' ' + attrs if attrs else '') + '>'


def wix(media, file, w, h, mode='fill', q=85):
    """Resized Wix media URL. mode='fill' crops to w x h (centred), 'fit' fits inside w x h without cropping."""
    stem = os.path.splitext(file)[0]
    al = ',al_c' if mode == 'fill' else ''
    return f'https://static.wixstatic.com/media/{media}/v1/{mode}/w_{w},h_{h}{al},q_{q},enc_auto/{stem}.jpg'


def wix_poster(base, w=1280, h=720):
    """Poster frame URL from data/videos.json 'poster' / 'thumb' (https://static.wixstatic.com/media/<id>f00N.jpg)."""
    return f'{base}/v1/fill/w_{w},h_{h},al_c,q_85,enc_auto/poster.jpg'


def imgur(src, size=''):
    """imgur variant: size 'b' = 160 px square crop, 'm' = 320 px, 'l' = 640 px, '' = original."""
    if not size:
        return src
    root_, ext_ = os.path.splitext(src)
    return f'{root_}{size}{ext_}'


def rv(html_, d=None, tag='div', cls=''):
    """Wrap html in a reveal element (.rv) with stagger index d."""
    st = f' style="--d:{d}"' if d is not None else ''
    return f'<{tag} class="rv{" " + cls if cls else ""}"{st}>{html_}</{tag}>'


_RV = re.compile(r'class="[^"]*\b(rv|rule|bar)\b')


def sec(h, body, sid='', note='', cls='', aside=''):
    """Section on the hanging-heading grid: heading column (h2, optional note, optional aside html) | content column.
    h is HTML (usually t(...)). If body contains no .rv/.rule element, the whole body column fades in as one block."""
    i = f' id="{sid}"' if sid else ''
    n = f'<p class="note">{note}</p>' if note else ''
    brv = '' if _RV.search(body) else ' rv'
    return (f'<section class="sec wrap{" " + cls if cls else ""}"{i}><div class="sg">'
            f'<div class="sg-h rv" data-rv><h2>{h}</h2>{n}{aside}</div>'
            f'<div class="sg-b{brv}" data-rv>{body}</div></div></section>')


def sec_wide(h, body, sid='', note='', link_html='', cls=''):
    """Full-width section (the gallery pattern): heading row with an optional link at the right, body below at full width."""
    i = f' id="{sid}"' if sid else ''
    n = f'<p class="note">{note}</p>' if note else ''
    brv = '' if _RV.search(body) else ' rv'
    lk = f'<div class="sw-link rv" data-rv>{link_html}</div>' if link_html else ''
    return (f'<section class="sec wrap sw{" " + cls if cls else ""}"{i}>'
            f'<div class="sw-head rv" data-rv><h2>{h}</h2>{n}</div>{lk}'
            f'<div class="sw-body{brv}" data-rv>{body}</div></section>')


def prose(paras, cls=''):
    """Paragraphs in one reading column. paras: list of (ko, en)."""
    return f'<div class="prose{" " + cls if cls else ""}">' + ''.join(t(k, en, 'p') for k, en in paras) + '</div>'


def bullets(ko_list, en_list):
    return (f'<ul class="bullets" data-l="ko">{"".join(f"<li>{x}</li>" for x in ko_list)}</ul>'
            f'<ul class="bullets" data-l="en" lang="en">{"".join(f"<li>{x}</li>" for x in en_list)}</ul>')


def kv(rows):
    """Definition list. rows: list of (label_html, value_html)."""
    return '<dl class="kv">' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in rows) + '</dl>'


LOGO_AREA = 5600     # px²: target visual area of one partner logo (logos() with sizes)


def _logo(s, a, o):
    """One sized logo: the visible mark (after trimming the file's own margins with crop=(top, right, bottom, left)
    fractions) gets the same area whatever its ratio, so a wide word mark and a square badge weigh the same."""
    w, h = o['w'], o['h']
    ct, cr, cb, cl = o.get('crop', (0, 0, 0, 0))
    fw, fh = 1 - cl - cr, 1 - ct - cb
    r = (w * fw) / (h * fh)
    H = max(20, min(o.get('max_h', 58), math.sqrt(o.get('area', LOGO_AREA) / r)))
    st = (f'left:{-cl / fw * 100:.2f}%;top:{-ct / fh * 100:.2f}%;width:{100 / fw:.2f}%;height:{100 / fh:.2f}%'
          + (';' + o['style'] if o.get('style') else ''))
    im = img(s, a, w, h, attrs='style="' + st + '"')
    return f'<span class="lg" style="--lw:{H * r:.1f};aspect-ratio:{r:.4f}">{im}</span>'


def logos(items):
    """Partner logo grid. items: list of (src, alt), or (src, alt, opts) with opts = dict(w, h: the file's pixel size;
    optional crop=(top, right, bottom, left) fractions of built-in whitespace to trim; style: extra css for the img,
    e.g. a filter for a white logo). With opts every logo is sized to the same visual area (LOGO_AREA)."""
    out = '<ul class="logos">'
    for i, it in enumerate(items):
        s, a = it[0], it[1]
        inner = _logo(s, a, it[2]) if len(it) > 2 and it[2] else img(s, a)
        out += f'<li class="rv" style="--d:{i % 4}">{inner}</li>'
    return out + '</ul>'


def btn(href, ko, en=None, external=True):
    inner = t(ko, en) + f'<i aria-hidden="true">{"↗" if external else "→"}</i>'
    return ext(href, inner, 'btn') if external else link(href, inner, 'btn')


def name_pair(name):
    """(ko, en) display name: romanised from NAME_EN when known, else the name as written."""
    return name, NAME_EN.get(name, name)


def role_en(s):
    return ' / '.join(ROLE_EN.get(x.strip(), x.strip()) for x in s.split('/')) if s else ''


def initials(name):
    """(ko, en) initial for a member without a photo: Hangul family-name syllable on KO; on EN the Latin
    family-name initial only when a romanised name exists in NAME_EN, else the same Hangul syllable."""
    ko = name.strip()[0]
    if name in NAME_EN:
        return ko, NAME_EN[name].split()[-1][0]
    return ko, ko


def member_role(m):
    """(ko, en) role line. A dict may set 'role_ko'/'role_en' directly (alumni: '박사 · 2022년 졸업' / 'Ph.D. · 2022')."""
    if m.get('role_ko') or m.get('role_en'):
        return m.get('role_ko', ''), m.get('role_en') or m.get('role_ko', '')
    ko = ' · '.join(x for x in [m.get('role', ''), m.get('dept', '')] if x)
    en = ' · '.join(x for x in [role_en(m.get('role', '')), role_en(m.get('dept', ''))] if x)
    return ko, en


# ================================================================== components
def _coil_svg(size=56):
    """Small closed coil for inner-page heroes (static SVG; drawn once by CSS)."""
    b, T, n = 0.0985, 2.6 * 2 * math.pi, 260
    a = math.atan(b)
    P = []
    for i in range(n + 1):
        tt_ = T * i / n
        r = math.exp(-b * tt_)
        ph = math.pi / 2 + a - tt_
        P.append((r * math.cos(ph), r * math.sin(ph)))
    minx, maxx = min(p[0] for p in P), max(p[0] for p in P)
    miny, maxy = min(p[1] for p in P), max(p[1] for p in P)
    pad = 1.5
    R = (size - 2 * pad) / (maxy - miny)
    W = (maxx - minx) * R + 2 * pad
    pts = [((x - minx) * R + pad, (y - miny) * R + pad) for x, y in P]
    y0 = pts[0][1]
    d = f'M0 {y0:.2f}H{pts[0][0]:.2f}' + ''.join(f'L{x:.2f} {y:.2f}' for x, y in pts[1:])
    return (f'<svg class="coil" viewBox="0 0 {W:.2f} {size}" width="{W:.0f}" height="{size}" aria-hidden="true" focusable="false">'
            f'<path d="{d}" pathLength="1"/></svg>'), size - y0


def page_hero(title, alt='', lead='', logo='', extra='', inst=INST, cls=''):
    """Inner-page hero: institute line, H1 (Hahmlet), optional alt line, the hairline that ends in a small coil
    (page accent colour, drawn once on load), optional lead and extra html (buttons, team nav).
    title/alt/lead: HTML (use t()) or (ko, en) tuples. logo: optional <img> html shown instead of the visible title
    (the title stays as hidden text for screen readers)."""
    def h(x):
        return tt(x) if isinstance(x, tuple) else x
    coil, off = _coil_svg()
    h1 = f'<h1 class="ld" style="--d:1">{h(title)}</h1>' if not logo else \
        f'<h1 class="ld h1-logo" style="--d:1"><span class="sr">{h(title)}</span>{logo}</h1>'
    return (f'<header class="hero hero-in wrap{" " + cls if cls else ""}">'
            f'<p class="inst ld" style="--d:0">{h(inst)}</p>{h1}'
            + (f'<p class="alt ld" style="--d:2">{h(alt)}</p>' if alt else '')
            + f'<div class="hline" aria-hidden="true" style="--off:{off:.1f}px"><i></i>{coil}</div>'
            + (f'<p class="lead ld" style="--d:3">{h(lead)}</p>' if lead else '')
            + (f'<div class="ld hero-x" style="--d:4">{extra}</div>' if extra else '')
            + '</header>')


def cochlea_hero(note=None):
    """Home hero: institute line, name, mission, About link, and the full tonotopic cochlea (JS-drawn, one ambient pulse).
    note: (ko, en) side note under the drawing (designer copy, awaiting client approval)."""
    note = note or ('<b>smilesnail의 ‘snail’, 달팽이관.</b> 입구에서는 높은 소리(20 kHz)를, 안쪽 끝에서는 낮은 소리(20 Hz)를 듣습니다.',
                    '<b>The ‘snail’ in smilesnail is the cochlea.</b> It hears high pitch (20 kHz) at its base and low pitch (20 Hz) at its apex.')
    return f"""<header class="hero hero-home wrap">
  <div class="stage">
    <p class="inst ld" style="--d:0">{tt(INST)}</p>
    <div class="title">
      <h1 class="ld" style="--d:1">{tt(NAME)}</h1>
      <p class="alt ld" style="--d:2"><span data-l="ko" lang="en">Research Institute of Hearing <span class="nw">Enhancement · RIHE</span></span><span data-l="en">청각재활연구소 · RIHE</span></p>
    </div>
    <svg class="cochlea" id="cochlea" aria-hidden="true" focusable="false"></svg>
  </div>
  <div class="below">
    <div class="ld" style="--d:3">
      <p class="mission">{tt(MISSION)}</p>
      {more('about', '연구소 소개', 'About the institute')}
    </div>
    <p class="figcap ld" style="--d:4">{tt(note)}</p>
  </div>
</header>"""


def ruled(items, cols=2, d0=0):
    """Ruled columns (research areas, mission/vision, subjects, data centers): each item = hairline that draws in,
    h3, text. items: list of (h3_html, body_html). cols: 1-4 (1 column on mobile)."""
    out = f'<div class="cols c{cols}">'
    for i, (h, b) in enumerate(items):
        d = d0 + i
        out += (f'<div class="col"><div class="rule" style="--d:{d}"></div>'
                f'<h3 class="rv" style="--d:{d + 1}">{h}</h3><div class="d rv" style="--d:{d + 2}">{b}</div></div>')
    return out + '</div>'


def areas(items=AREAS):
    """The four research areas as ruled columns (KO titles on KO, EN titles on EN)."""
    return ruled([(t(a['ko'], a['en']), t(a['d_ko'], a['d_en'], 'p')) for a in items], 2)


def plate(src, alt=('', ''), w=1600, h=1000, href='', srcset='', sizes='(max-width: 760px) 100vw, 400px', ratio=1.6, inset=.06):
    """Figure or diagram set as a framed sheet on a --wash panel of fixed ratio (default 16:10), like the video poster.
    Every plate in a row has the same height whatever the image's own ratio: the image is fitted inside the panel
    (inset 6%) at its natural ratio w/h, positioned in %, never cropped. href: optional link to the full-size original
    (new tab). Use it inside fig_cols(); alone it is a block that fills its column."""
    r = w / h
    iw = min(1 - 2 * inset, (1 - 2 * inset) / ratio * r)        # image width, in panel widths
    ih = iw / r * ratio                                           # image height, in panel heights
    st = f'left:{(1 - iw) / 2 * 100:.2f}%;top:{(1 - ih) / 2 * 100:.2f}%;width:{iw * 100:.2f}%;height:{ih * 100:.2f}%'
    im = img(src, alt, w, h, srcset=srcset, sizes=sizes, attrs=f'style="{st}"')
    pa = f' style="--pr:{ratio}"' if ratio != 1.6 else ''
    if href:
        if isinstance(alt, str):
            alt = (alt, alt)
        return (f'<a class="plate" href="{href}" target="_blank" rel="noopener"{pa} '
                f'aria-label="{e(alt[0])}: 원본 크기로 보기 (새 창)" data-aria-en="{e(alt[1])}: full size (new tab)">{im}</a>')
    return f'<span class="plate"{pa}>{im}</span>'


def fig_cols(items, cols=2, d0=0):
    """Ruled columns with a figure: hairline, plate (see plate()), h3, text. items: list of (plate_html, h3_html, body_html).
    Same rhythm as ruled(); cols 1-4 (1 column on mobile). Research page: the four project areas with their images."""
    out = f'<div class="cols c{cols} figs">'
    for i, (fg, h, b) in enumerate(items):
        d = d0 + (i % cols)
        out += (f'<div class="col"><div class="rule" style="--d:{d}"></div><div class="fg rv" style="--d:{d + 1}">{fg}</div>'
                f'<h3 class="rv" style="--d:{d + 2}">{h}</h3><div class="d rv" style="--d:{d + 3}">{b}</div></div>')
    return out + '</div>'


def _ticks(n, h=18):
    """Static SVG tick row: one tick per item, every tenth tick full height."""
    d = ''.join(f'M{i + .5} {0 if (i + 1) % 10 == 0 else h * .34:.1f}V{h}' for i in range(n))
    return f'<svg viewBox="0 0 {n} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="{d}"/></svg>'


def outcomes(rows, link_html=''):
    """Outcome counts with tick rows. rows: list of (n, ko, en). One tick = one item; the reveal runs at a constant
    rate per tick (duration proportional to n)."""
    mx = max(n for n, _, _ in rows)
    out = '<div class="oc">'
    for i, (n, ko, en) in enumerate(rows):
        out += (f'<div class="oc-row" style="--n:{n};--w:{n / mx:.4f};--d:{i}"><div class="oc-n rv" style="--d:{i}">{n}</div>'
                f'<div><p class="oc-t rv" style="--d:{i}">{t(ko, en)}</p><div class="bar">{_ticks(n)}<i></i></div></div></div>')
    out += '</div>'
    if link_html:
        out += f'<div class="oc-more rv" style="--d:{len(rows)}">{link_html}</div>'
    return out


def face(m, size=28):
    """One small face thumbnail (greyscale) or an initial tile, decorative (alt="")."""
    if m.get('photo'):
        return img(imgur(m['photo'], 'm'), '', size, size)
    ko, en = initials(m['name'])
    return f'<span class="ini">{t(ko, en) if en != ko else ko}</span>'


def faces(members, limit=6):
    """Strip of faces for a team (first `limit` members in people.json order) plus '+N'."""
    out = '<span class="faces" aria-hidden="true">' + ''.join(face(m) for m in members[:limit])
    if len(members) > limit:
        out += f'<span class="fx mono">+{len(members) - limit}</span>'
    return out + '</span>'


def lab_rows(labs=LABS, with_faces=True, current=None):
    """Linked lab rows: lab mark + name, team name and member count, description, face strip, arrow.
    Underlines in the lab colour on hover. current: lab key to mark as the current page."""
    out = '<ul class="labs">'
    for i, lb in enumerate(labs):
        mem = TEAMS.get(lb['key'], {}).get('members', [])
        cnt = t(f'{lb["team_ko"]} · <span class="nw">{len(mem)}명</span>', f'{lb["team_en"]} · <span class="nw">{len(mem)} members</span>') if mem else t(lb['team_ko'], lb['team_en'])
        fc = faces(mem) if (with_faces and mem) else ''
        cur = ' aria-current="page"' if lb['key'] == current else ''
        inner = (f'<span class="lb-h"><span class="nm"><b>{lb["name"]}</b></span><span class="tm">{cnt}</span></span>'
                 f'<span class="lb-b"><span class="ds">{t(lb["d_ko"], lb["d_en"])}</span>{fc}</span>'
                 f'<span class="go" aria-hidden="true">→</span>')
        out += f'<li class="rv{" cur" if cur else ""}" style="--d:{i}">' + link(lb['page'], inner, '', f'style="--c:var(--{lb["key"]})"{cur}') + '</li>'
    return out + '</ul>'


def data_centers(items=DATA_CENTERS, links=True):
    """The two national data centers: logo as heading, text, link to the lab that runs it."""
    out = '<div class="cols c2 dcs">'
    for i, dc in enumerate(items):
        lb = LAB[dc['key']]
        # the logos carry both the Korean and the English name, so the heading is the logo itself (alt per language)
        lg = img(dc['logo'], (dc['ko'], dc['en']), dc['logo_w'], dc['logo_h'], dc['logo_cls'])
        out += (f'<div class="col dc"><div class="rule" style="--d:{i}"></div>'
                f'<h3 class="rv" style="--d:{i + 1}"><span class="logo">{lg}</span></h3>'
                f'<p class="d rv" style="--d:{i + 2}">{t(dc["d_ko"], dc["d_en"])}</p>'
                + (f'<div class="rv" style="--d:{i + 3}">{more(lb["page"], lb["name"])}</div>' if links else '') + '</div>')
    return out + '</div>'


def feature(photo, name, role, lines=None, quote=None, email=None, alt=None):
    """Person feature (Director on Home, Director & Manager on lab pages).
    name, role: (ko, en). lines: (ko_list, en_list) credentials. quote: (ko, en) message. email: address."""
    alt = alt or (f'{name[0]} {role[0]} 사진', f'Portrait of {role[1]} {name[1]}')
    pic = img(photo, alt, 200, 250, 'ft-pic rv') if photo else \
        f'<span class="ft-pic ini rv" role="img" aria-label="{e(name[0])}">{tt(initials(name[0]))}</span>'
    q = f'<blockquote class="ft-q rv" style="--d:1">{t(quote[0], quote[1], "p")}</blockquote>' if quote else ''
    cv = ''
    if lines:
        cv += (f'<ul data-l="ko">{"".join(f"<li>{x}</li>" for x in lines[0])}</ul>'
               f'<ul data-l="en" lang="en">{"".join(f"<li>{x}</li>" for x in lines[1])}</ul>')
    if email:
        cv += f'<a class="mail" href="mailto:{email}">{email}</a>'
    who = f'<p class="ft-nm">{t(name[0], name[1]) if name[1] != name[0] else name[0]}<small>{t(role[0], role[1])}</small></p>'
    return (f'<div class="ft{" has-q" if quote else ""}">{pic}<div class="ft-who rv" style="--d:2">{who}</div>{q}'
            f'<div class="ft-cv rv" style="--d:3">{cv}</div></div>')


def director(short_en=True, quote=True):
    D = DIRECTOR
    return feature(imgur(D['photo'], 'l'), (D['name_ko'], D['name_en']), (D['role_ko'], D['role_en']),
                   (D['lines_ko'], D['lines_en_short'] if short_en else D['lines_en']),
                   (D['greeting_ko'], D['greeting_en']) if quote else None, D['email'])


def person_card(m, d=0, own=False, small=False):
    """People grid card: 4:5 portrait (or initial tile), name (Hahmlet), role.
    own=True: the card is its own reveal block (data-rv) and its stagger comes from its column in CSS (.people.rows)."""
    nm = name_pair(m['name'])
    rk, re_ = member_role(m)
    if m.get('photo'):
        ph = img(imgur(m['photo'], 'm' if small else 'l'), '', 240, 300)
    else:
        ko, en = initials(m['name'])
        ph = f'<span class="ini" aria-hidden="true">{t(ko, en) if en != ko else ko}</span>'   # the name follows
    name = t(nm[0], nm[1]) if nm[1] != nm[0] else nm[0]
    rl = f'<p class="rl">{t(rk, re_)}</p>' if rk else ''
    st = ' data-rv' if own else f' style="--d:{d % 4}"'
    return f'<li class="pc rv"{st}><span class="ph">{ph}</span><p class="nm">{name}</p>{rl}</li>'


def people_grid(members, small=False, rows=False):
    """Portrait grid (4 columns desktop, 2 at 320; small=True: 6 / 3 columns).
    rows=True: each card is observed on its own, so a long grid reveals row by row as it scrolls in
    (cards of one row share their top edge and appear together, staggered by column)."""
    cls = 'people' + (' sm' if small else '') + (' rows' if rows else '')
    return f'<ul class="{cls}">' + ''.join(person_card(m, i, rows, small) for i, m in enumerate(members)) + '</ul>'


def jump_nav(items, label=('이 페이지의 구성', 'On this page')):
    """In-page jump links (for page_hero(extra=...)). items: [(section id, label_html, colour key, count or None)].
    Each link: 14x2 colour mark, label, count in mono (read as '3명' / '3 members' by screen readers).
    JS_JUMP scrolls with scrollIntoView (a plain #fragment does not scroll the parent Wix page)."""
    out = f'<nav class="jump" aria-label="{e(label[0])}" data-aria-en="{e(label[1])}"><ul>'
    for sid, lab, ck, n in items:
        cnt = f'<span class="mono">{n}{t("명", " members", cls="sr")}</span>' if n is not None else ''
        out += f'<li><a href="#{sid}" style="--c:var(--{ck})"><span class="mark" aria-hidden="true"></span>{lab}{cnt}</a></li>'
    return out + '</ul></nav>'


def team_mark(key):
    return f'<span class="mark" style="--c:var(--{key})" aria-hidden="true"></span>'


def org_chart(current=None, labs=LABS):
    """Organisation chart (lab pages, About): the institute and its director at the root, the units (LABS) hanging
    from one hairline that draws in with the block. current: lab key to highlight (2 px drop line in the lab colour,
    name in ink, '현재 페이지' tag, not a link); the other units link to their pages. Desktop: one row of units;
    320: a vertical tree."""
    D = DIRECTOR
    root = (f'<div class="org-root rv"><p class="org-nm serif">{t(NAME[0] + " · RIHE", NAME[1])}</p>'
            f'<p class="org-dr">{t("연구소장 " + D["name_ko"], "Director · " + D["name_en"])}</p></div>')
    arrow = '<i aria-hidden="true">→</i>'
    out = f'<div class="org">{root}<div class="org-b" style="--n:{len(labs)}"><span class="rule" aria-hidden="true"></span><ul class="org-u">'
    for i, lb in enumerate(labs):
        cur = lb['key'] == current
        inner = (f'<span class="org-l"><span class="nm">{lb["name"]}</span>{"" if cur else arrow}</span>'
                 f'<span class="org-tm">{t(lb["team_ko"], lb["team_en"])}</span>'
                 + (f'<span class="org-here">{t("현재 페이지", "This page")}</span>' if cur else ''))
        body = f'<span class="org-x" aria-current="page">{inner}</span>' if cur else link(lb['page'], inner, 'org-x')
        out += f'<li class="org-it rv{" cur" if cur else ""}" style="--c:var(--{lb["key"]});--d:{i + 1}">{body}</li>'
    return out + '</ul></div></div>'


def dc_box(key, body='', since=None):
    """Data-center panel for a lab page: a --wash box whose heading is the center's logo (DATA_CENTERS[key], alt per
    language), an optional mono line (since: (ko, en)), then body html (prose, bullets)."""
    dc = next(d for d in DATA_CENTERS if d['key'] == key)
    lg = img(dc['logo'], (dc['ko'], dc['en']), dc['logo_w'], dc['logo_h'], dc['logo_cls'])
    s = f'<p class="dcb-s">{tt(since)}</p>' if since else ''
    return f'<div class="box dcb rv"><h3 class="dcb-h"><span class="logo">{lg}</span></h3>{s}{body}</div>'


# ---------------------------------------------------------------- quote, box, map, contact rows (About, Audiso, Contact)
def quote(text, cite=None, photo=None):
    """Pull quote at reading size (Noto Sans KR, not Hahmlet): text and cite are (ko, en); photo: optional small
    greyscale face beside the cite. About uses it for the director's opening line."""
    fc = img(imgur(photo, 'm'), '', 36, 36, 'pq-face') if photo else ''
    c = f'<figcaption class="pq-by rv" style="--d:1">{fc}<span>{tt(cite)}</span></figcaption>' if cite else ''
    return f'<figure class="pq"><blockquote class="rv">{tt(text, "p")}</blockquote>{c}</figure>'


def box(body, media='', cls=''):
    """Wash panel (.box). media: optional html set at the left (a badge or logo, e.g. the KOLAS mark), body at the
    right; at 320 the media sits above the body at a smaller size."""
    c = f' {cls}' if cls else ''
    if not media:
        return f'<div class="box rv{c}">{body}</div>'
    return f'<div class="box bx rv{c}"><div class="bx-m">{media}</div><div class="bx-b">{body}</div></div>'


def map_embed(src, title, link_href='', link_label=('지도에서 크게 보기', 'Open in Google Maps')):
    """Embedded map (Google Maps output=embed) in a fixed-ratio wash frame (2:1 desktop, 4:3 at 320), lazy-loaded,
    with a KO/EN title for screen readers (title + aria-label swapped by language). link_href: optional external
    link under the map."""
    title = (title, title) if isinstance(title, str) else title
    fr = (f'<div class="map rv"><span class="map-ph mono" aria-hidden="true">Google Maps</span><iframe src="{src}" title="{e(title[0])}" aria-label="{e(title[0])}" data-aria-en="{e(title[1])}" '
          f'loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')
    lk = f'<p class="map-l rv" style="--d:1">{more(link_href, link_label[0], link_label[1], external=True)}</p>' if link_href else ''
    return fr + lk


def contact_rows(items):
    """Team contacts on the lab-row pattern (.labs): lab mark + name, team, then the contact person (small greyscale
    face) and email; the whole row is a mailto link and underlines in the lab colour on hover.
    items: [dict(key=lab colour key, name='Basic Lab', team=(ko, en), person=(ko, en), email='...', photo='')]."""
    out = '<ul class="labs ct">'
    for i, it in enumerate(items):
        fc = img(imgur(it['photo'], 'm'), '', 40, 40) if it.get('photo') else ''
        inner = (f'<span class="lb-h"><span class="nm"><b>{it["name"]}</b></span><span class="tm">{tt(it["team"])}</span></span>'
                 f'<span class="lb-b ct-who">{fc}<span><span class="ct-p">{tt(it["person"])}</span>'
                 f'<span class="ct-e mono">{it["email"]}</span></span></span>'
                 f'<span class="go" aria-hidden="true">→</span>')
        out += f'<li class="rv" style="--d:{i}"><a href="mailto:{it["email"]}" style="--c:var(--{it["key"]})">{inner}</a></li>'
    return out + '</ul>'


# ---------------------------------------------------------------- video
def _vid_items(videos):
    out = '<ol class="playlist">'
    for i, v in enumerate(videos):
        meta = v['duration'] + (f' · {v["date"]}' if v.get('date') else '')
        out += (f'<li><button type="button" aria-current="{"true" if i == 0 else "false"}" data-src="{v["src"]}" '
                f'data-poster="{wix_poster(v["poster"])}">'
                f'{img(wix_poster(v["thumb"], 320, 180), "", 84, 47)}'
                f'<span><span class="pt">{t(v["title_ko"], v["title_en"])}</span><span class="pm mono">{meta}</span></span></button></li>')
    return out + '</ol>'


def _vid_screen(videos):
    v = videos[0]
    meta = v['duration'] + (f' · {v["date"]}' if v.get('date') else '')
    return (f'<div class="player rv"><div class="screen">'
            f'{img(wix_poster(v["poster"]), "", 1280, 720, "poster", lazy=True)}'
            f'<button type="button" class="play" aria-label="재생: {e(v["title_ko"])}" data-aria-en="Play: {e(v["title_en"])}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5z"/></svg></button></div>'
            f'<p class="now"><span class="t">{t(v["title_ko"], v["title_en"])}</span><span class="mono">{meta}</span></p></div>')


def videos_sec(h=None, videos=None, sid='videos', note=''):
    """Home-style video section: heading column = h2 + playlist, content column = 16:9 player.
    Static markup from data/videos.json. Plays only on click, native controls, height never changes."""
    videos = videos or VIDEOS
    h = h or t('영상', 'Videos')
    n = f'<p class="note">{note}</p>' if note else ''
    return (f'<!-- 영상: data/videos.json에서 만들어집니다. 영상을 추가·삭제하려면 그 파일을 고치고 build.py를 다시 실행하세요. -->'
            f'<section class="sec wrap vids" id="{sid}" data-player><div class="sg">'
            f'<div class="sg-h rv" data-rv><h2>{h}</h2>{n}{_vid_items(videos)}</div>'
            f'<div class="sg-b" data-rv>{_vid_screen(videos)}</div></div></section>')


def video_player(videos=None):
    """Stacked player for a content column: 16:9 player, then the playlist below it."""
    videos = videos or VIDEOS
    return f'<div class="vstack" data-player>{_vid_screen(videos)}<div class="rv" style="--d:1">{_vid_items(videos)}</div></div>'


# ---------------------------------------------------------------- gallery
def _photo_alt(p):
    return (p.get('alt_ko') or p['caption_ko'], p.get('alt_en') or p['caption_en'])


def gallery_teaser(photos=None, rows=(2, 3), h=None, note=None):
    """Home gallery teaser: full-width section, photos in justified rows (equal heights per row, no fixed classes),
    each linking to /gallery. photos default: first five entries of data/gallery.json."""
    photos = photos or GALLERY[:sum(rows)]
    h = h or t('갤러리', 'Gallery')
    note = note or t('학회와 수상, 그리고 연구소 사람들의 사진을 모았습니다.', 'Conferences, awards and the people of the institute.')
    body, k = '', 0
    for ri, cnt in enumerate(rows):
        body += '<div class="gt-row">'
        for p in photos[k:k + cnt]:
            r = p['width'] / p['height']
            src = wix(p['media'], p['file'], 600, 600, 'fit', 80)
            big = wix(p['media'], p['file'], 1200, 1200, 'fit', 85)
            sizes = '(max-width: 760px) 100vw, 620px' if (ri == 0 and k == 0) else '(max-width: 760px) 50vw, 380px'
            body += (f'<figure class="gt rv" style="--r:{r:.4f};--d:{k}">'
                     + link('gallery', f'<span class="ph">{img(src, "", 600, round(600 / r), srcset=f"{src} 600w, {big} 1200w", sizes=sizes)}</span>'
                            f'<figcaption><span>{t(p["caption_ko"], p["caption_en"])}</span>{_cap_year(p)}</figcaption>')
                     + '</figure>')
            k += 1
        body += '</div>'
    body = f'<div class="gteaser">{body}</div>'
    return ('<!-- 사진: data/gallery.json의 앞 다섯 장이 여기에 나옵니다. -->'
            + sec_wide(h, body, 'gallery', note, more('gallery', '갤러리 전체 보기', 'Open the gallery'), 'gal-sec'))


def _cap_year(p):
    """Mono year after a caption, left out when both captions already contain that year."""
    y = str(p.get('year', '') or '')
    if not y or (y in p.get('caption_ko', '') and y in p.get('caption_en', '')):
        return ''
    return f'<span class="mono">{y}</span>'


def gallery_grid(photos=None, per_page=12, years=True, live=False):
    """Full gallery (/gallery): year toggles, justified rows (no crop on desktop; 2-column 4:3 crop at 320),
    12 per page with a pager, and an in-place viewer that opens over the grid at the clicked photo
    (absolute, never position:fixed; centred in the visible band of a tall iframe).
    The grid reserves the height of its tallest page and filter, so paging and filtering never move the page.
    live=True: the baked list can be replaced at runtime. The page posts {type:'ready'} to window.parent and accepts
    {type:'gallery', items:[{src | media, width, height, caption_ko, caption_en, year, file?, alt_ko?, alt_en?}]}
    (src: wix:image://v1/..., https://static.wixstatic.com/media/<id> or any https URL; media: a Wix media id).
    Wix page code for a CMS collection: tools/pages/gallery.md."""
    photos = photos or GALLERY
    ys = sorted({p['year'] for p in photos if p.get('year')}, reverse=True)
    tg = ''
    if years and (len(ys) > 1 or live):
        tg = (f'<div class="tgs" role="group" aria-label="연도" data-aria-en="Year"{"" if len(ys) > 1 else " hidden"}>'
              f'<button type="button" class="tg" data-k="year" data-v="all" aria-pressed="true">{tt(UI["all"])}</button>'
              + ''.join(f'<button type="button" class="tg" data-k="year" data-v="{y}" aria-pressed="false">{y}</button>' for y in ys) + '</div>')
    figs = ''
    for i, p in enumerate(photos):
        r = p['width'] / p['height']
        src = wix(p['media'], p['file'], 600, 600, 'fit', 80)
        mid = wix(p['media'], p['file'], 1200, 1200, 'fit', 85)
        full = wix(p['media'], p['file'], 1600, 1600, 'fit', 85)
        alt = _photo_alt(p)
        hid = ' hidden' if i >= per_page else ''
        figs += (f'<figure class="gl-it" style="--r:{r:.4f}" data-year="{p.get("year", "")}" data-full="{full}"{hid}>'
                 f'<button type="button" class="gl-open" aria-label="크게 보기: {e(p["caption_ko"])}" data-aria-en="View larger: {e(p["caption_en"])}">'
                 f'{img(src, alt, 600, round(600 / r), srcset=f"{src} 600w, {mid} 1200w", sizes="(max-width: 760px) 50vw, 420px")}</button>'
                 f'<figcaption><span>{t(p["caption_ko"], p["caption_en"])}</span>{_cap_year(p)}</figcaption></figure>')
    pages = max(1, math.ceil(len(photos) / per_page))
    pager = (f'<nav class="pager"{" hidden" if pages < 2 else ""} aria-label="페이지" data-aria-en="Pages">'
             f'<button type="button" data-p="-1" aria-label="{UI["prev"][0]}" data-aria-en="{UI["prev"][1]}" disabled>‹</button>'
             f'<span class="pg mono">1 / {pages}</span>'
             f'<button type="button" data-p="1" aria-label="{UI["next"][0]}" data-aria-en="{UI["next"][1]}"{" disabled" if pages < 2 else ""}>›</button></nav>')
    viewer = ('<div class="gl-view" hidden role="dialog" aria-modal="true" tabindex="-1" aria-label="사진 보기" data-aria-en="Photo viewer">'
              '<div class="gl-vbox"><div class="gl-vimg"></div>'
              '<div class="gl-vbar"><p class="gl-vcap" aria-live="polite"></p><span class="gl-vn mono"></span>'
              '<button type="button" class="gl-prev" aria-label="이전 사진" data-aria-en="Previous photo">‹</button>'
              '<button type="button" class="gl-next" aria-label="다음 사진" data-aria-en="Next photo">›</button>'
              f'<button type="button" class="gl-close">{t("닫기", "Close")}</button></div></div></div>')
    return (f'<!-- 사진: data/gallery.json에서 만들어집니다. -->'
            f'<div class="gl" data-gallery data-size="{per_page}"{" data-live" if live else ""}>{tg}<div class="gl-grid">{figs}</div>{pager}{viewer}</div>')


# ---------------------------------------------------------------- lists
_HANGUL = re.compile('[\uac00-\ud7a3]')


def _lg(s):
    """lang attribute for a data string shown on both language pages: ko if it has Hangul, else en."""
    return ' lang="ko"' if _HANGUL.search(str(s or '')) else ' lang="en"'


def _list_item(kind, d, teams):
    if kind == 'pub':
        tm = ''
        if teams and d.get('team') in TEAM_LABEL:
            tm = f'<span class="ls-tm" style="--c:var(--{d["team"]})">{tt(TEAM_LABEL[d["team"]])}</span>'
        return (f'<li><p class="ls-ti"{_lg(d["title"])}>{e(d["title"])}</p><p class="ls-au"{_lg(d["authors"])}>{e(d["authors"])}</p>'
                f'<p class="ls-mt"><span>{d["year"]}</span><span{_lg(d["journal"])}>{e(d["journal"])}</span>{tm}</p></li>')
    if kind == 'report':
        return (f'<li><p class="ls-ti"{_lg(d["title"])}>{e(d["title"])}</p><p class="ls-au"{_lg(d["authors"])}>{e(d["authors"])}</p>'
                f'<p class="ls-mt"><span>{d["year"]}</span><span{_lg(d["event"])}>{e(d["event"])}</span></p></li>')
    st = tt(UI.get(d['status'], (d['status'], d['status'])))
    co = f'<span>{tt(UI.get(d["country"], (d["country"], d["country"])))}</span>' if d.get('country') else ''
    return f'<li><p class="ls-ti" lang="ko">{e(d["title"])}</p><p class="ls-mt"><span>{st}</span>{co}</p></li>'   # patent titles are Korean


def listing(kind, items, filters=None, per_page=10, sid=''):
    """Paginated, filterable list with a tick ruler (one tick per item; ticks that match the filter are navy).
    kind: 'pub' | 'report' | 'patent'. items: list from data/*.json (already filtered for a lab page if needed).
    filters: subset of ('team', 'year', 'status', 'country'); default: pub -> ('team','year'), report -> ('year',), patent -> ('status',).
    The first page is static HTML; JS re-renders on filter/page and keeps a stable min-height."""
    if filters is None:
        filters = {'pub': ('team', 'year'), 'report': ('year',), 'patent': ('status',)}[kind]
    teams = 'team' in filters
    rows, cut = '', ''
    for k in filters:
        opts = []
        if k == 'team':
            opts = [(tk, tt(TEAM_LABEL[tk])) for tk in TEAM_LABEL if any(d.get('team') == tk for d in items)]
        elif k == 'year':
            ys = sorted({d['year'] for d in items}, reverse=True)
            if len(ys) > 6:
                cut = str(ys[5])
                ys = ys[:5]
            opts = [(str(y), str(y)) for y in ys] + ([('~' + cut, '~' + cut)] if cut else [])
        elif k == 'status':
            opts = [(s, tt(UI[s])) for s in ('등록', '출원') if any(d.get('status') == s for d in items)]
        elif k == 'country':   # patents: countries in UI order, then any others; items with no country show under 'All' only
            cs = [c for c in ('대한민국', '미국', '중국', '유럽') if any(d.get('country') == c for d in items)]
            cs += sorted({d.get('country') for d in items if d.get('country') and d.get('country') not in cs})
            opts = [(c, tt(UI.get(c, (c, c)))) for c in cs]
        if len(opts) < 2:
            continue
        rows += (f'<div class="tgs" role="group" aria-label="{UI[k][0]}" data-aria-en="{UI[k][1]}"><span class="k">{tt(UI[k])}</span>'
                 f'<button type="button" class="tg" data-k="{k}" data-v="all" aria-pressed="true">{tt(UI["all"])}</button>'
                 + ''.join(f'<button type="button" class="tg" data-k="{k}" data-v="{v}" aria-pressed="false">{lb}</button>' for v, lb in opts)
                 + '</div>')
    n = len(items)
    pages = max(1, math.ceil(n / per_page))
    ruler = ''.join(f'<line class="on" x1="{i + .5}" x2="{i + .5}" y1="{0 if (i + 1) % 10 == 0 else 5}" y2="14"/>' for i in range(n))
    first = ''.join(_list_item(kind, d, teams) for d in items[:per_page])
    payload = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
    i_ = f' id="{sid}"' if sid else ''
    return (f'<div class="ls"{i_} data-list data-kind="{kind}" data-size="{per_page}"{" data-teams" if teams else ""}>'
            f'<script type="application/json">{payload}</script>'
            + (f'<div class="ls-f{" kw" if "country" in filters else ""}">{rows}</div>' if rows else '')
            + f'<svg class="ls-ruler" viewBox="0 0 {n} 14" preserveAspectRatio="none" aria-hidden="true" focusable="false">{ruler}</svg>'
            f'<p class="ls-meta mono"><span class="ls-n">{t(f"{n}건", f"{n} items")}</span><span class="ls-pi">1 / {pages}</span></p>'
            f'<ol class="ls-items">{first}</ol>'
            f'<nav class="pager" aria-label="페이지" data-aria-en="Pages"><button type="button" data-p="-1" aria-label="{UI["prev"][0]}" data-aria-en="{UI["prev"][1]}" disabled>‹</button>'
            f'<span class="pg mono">1 / {pages}</span>'
            f'<button type="button" data-p="1" aria-label="{UI["next"][0]}" data-aria-en="{UI["next"][1]}"{" disabled" if pages < 2 else ""}>›</button></nav></div>')


# ================================================================== CSS
CSS = r"""
:root {
  --paper: #ffffff; --ink: #131b2a; --ink-2: #566072; --line: #e3e7ed; --mist: #f4f6f9; --wash: #eef2f7;
  --navy: #1b3d6f;
  --basic: #2e8b57; --hearing: #4e7595; --head: #2e6e9e; --audiso: #9a6f07; --collab: #7a8494;
  --accent: var(--navy);
  --serif: 'Hahmlet', 'Noto Serif KR', 'AppleMyungjo', serif;
  --sans: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --mono: 'DM Mono', ui-monospace, Menlo, monospace;
  --ease: cubic-bezier(.22, 1, .36, 1);
  --gut: 40px; --sec: 120px; --hcol: 236px; --hgap: 72px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { background: var(--paper); -webkit-text-size-adjust: 100%; }
body { font-family: var(--sans); font-size: 15.5px; line-height: 1.8; color: var(--ink); background: var(--paper);
  word-break: keep-all; overflow-wrap: anywhere; -webkit-font-smoothing: antialiased; overflow-x: hidden; padding-bottom: var(--sec); }
img { display: block; max-width: 100%; }
a { color: inherit; }
button { font: inherit; color: inherit; }
ul, ol { list-style: none; }
a:focus-visible, button:focus-visible, video:focus-visible { outline: 2px solid var(--navy); outline-offset: 3px; border-radius: 2px; }
html[data-lang="ko"] [data-l="en"], html[data-lang="en"] [data-l="ko"] { display: none !important; }
.nw { white-space: nowrap; }
html[data-lang="en"] body { line-height: 1.7; }   /* Latin needs less leading than Hangul */
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.mono { font-family: var(--mono); font-size: 12px; letter-spacing: .02em; }
.serif { font-family: var(--serif); font-weight: 300; }

/* ---------- layout ---------- */
.wrap { max-width: 1200px; margin: 0 auto; padding: 0 var(--gut); }
.sec { padding-top: var(--sec); }
.sg { display: grid; grid-template-columns: var(--hcol) minmax(0, 1fr); gap: 0 var(--hgap); align-items: start; }
h2 { font-family: var(--serif); font-weight: 400; font-size: 30px; line-height: 1.3; letter-spacing: -.01em; }
h3 { font-family: var(--serif); font-weight: 400; font-size: 22px; line-height: 1.35; letter-spacing: -.005em; }
.note { font-size: 14px; line-height: 1.7; color: var(--ink-2); margin-top: 14px; max-width: 18em; }
p.d, .d p, div.d { color: var(--ink-2); }
.d { margin-top: 10px; }
.lead { font-size: 18px; line-height: 1.75; max-width: 34em; }
.prose p { max-width: 36em; }
.prose p + p { margin-top: 14px; }
.sw { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "head link" "body body"; align-items: end; }
.sw-head { grid-area: head; margin-bottom: 44px; }
.sw-head .note { max-width: none; }
.sw-link { grid-area: link; margin-bottom: 48px; }
.sw-body { grid-area: body; }

/* ---------- links and buttons ---------- */
.more { display: inline-flex; align-items: baseline; gap: 8px; font-size: 14.5px; font-weight: 500; color: var(--navy); text-decoration: none; padding: 2px 0; }
.more i, .btn i { font-style: normal; display: inline-block; transition: transform 240ms var(--ease); }
.more:hover i, .btn:hover i { transform: translateX(4px); }
.more:hover span:not([aria-hidden]), .btn:hover span { text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1px; }
.btn { display: inline-flex; align-items: baseline; gap: 10px; padding: 9px 16px 10px; border: 1px solid var(--line); border-radius: 3px;
  font-size: 14.5px; font-weight: 500; color: var(--navy); text-decoration: none; }
.btn:hover { border-color: var(--navy); }
.btns { display: flex; flex-wrap: wrap; gap: 10px; }
.mail { font-family: var(--mono); font-size: 13px; color: var(--navy); text-underline-offset: 3px; }
.mark { display: inline-block; width: 14px; height: 2px; background: var(--c); vertical-align: middle; transform: translateY(-2px); }

/* ---------- hero (shared) ---------- */
.hero { padding-top: 64px; }
.inst { font-size: 14px; color: var(--ink-2); padding-top: 4px; }
.hero h1 { font-family: var(--serif); font-weight: 300; letter-spacing: -.02em; }
.hero .alt { margin-top: 16px; font-size: 15px; color: var(--ink-2); letter-spacing: .005em; }
.ld { animation: ld 900ms var(--ease) both; animation-delay: calc(var(--d, 0) * 110ms + 60ms); }
@keyframes ld { from { opacity: 0; transform: translateY(8px); } }

/* inner-page hero: title, hairline, small coil */
.hero-in h1 { margin-top: 40px; font-size: 52px; line-height: 1.12; text-wrap: balance; }
.hero-in h1 [data-l="ko"] { font-size: 56px; }
.hero-in h1 [data-l="en"] { font-size: 46px; display: block; }
.h1-logo img { height: 72px; width: auto; }
.hero-lablogo .h1-logo img { height: 60px; }   /* lab pages (HeAD Lab): the wordmark matches the 56 px Hahmlet titles of the other labs */
.hline { display: flex; align-items: flex-end; margin-top: 30px; color: var(--accent); }
.hline i { flex: 1; height: 1px; background: currentColor; opacity: .5; margin-bottom: var(--off); transform-origin: 0 50%;
  animation: hl-in 650ms cubic-bezier(.55, 0, .85, .45) 280ms both; }
.coil { flex: none; overflow: visible; }
.coil path { fill: none; stroke: currentColor; stroke-opacity: .5; stroke-width: 1.1; stroke-linecap: round; stroke-linejoin: round;
  stroke-dasharray: 1 1; animation: coil-in 1300ms cubic-bezier(.33, 1, .68, 1) 900ms both; }
@keyframes hl-in { from { transform: scaleX(0); } }
@keyframes coil-in { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
.hero-in .lead { margin-top: 28px; }
.hero-x { margin-top: 26px; }

/* home hero: the cochlea */
.stage { display: grid; position: relative; }
.stage > * { grid-area: 1 / 1; }
.hero-home .inst { align-self: start; z-index: 1; }
.hero-home .title { align-self: end; padding-bottom: 92px; max-width: var(--tw, 56%); z-index: 1; }
.hero-home h1 [data-l="ko"] { font-size: clamp(58px, 6vw, 76px); line-height: 1.08; }
.hero-home h1 [data-l="en"] { font-size: clamp(40px, 4.1vw, 52px); line-height: 1.1; display: block; text-wrap: balance; }
.cochlea { width: 100%; height: 480px; display: block; overflow: visible; }
.cochlea .sp { fill: none; stroke: var(--navy); stroke-opacity: .5; stroke-width: 1.1; stroke-linecap: round; stroke-linejoin: round; }
.cochlea .pulse { fill: none; stroke: var(--navy); stroke-width: 2.2; stroke-linecap: round; }
.cochlea .tk { opacity: 0; transition: opacity 700ms var(--ease); }
.cochlea .tk.on { opacity: 1; }
.cochlea .tk line { stroke: var(--navy); stroke-opacity: .6; stroke-width: 1; }
.cochlea text { font-family: var(--mono); font-size: 11.5px; letter-spacing: .02em; fill: var(--ink-2); }
.cochlea text.hl { fill: var(--navy); opacity: 0; }
.cochlea .dot { fill: var(--navy); opacity: 0; transform-box: fill-box; transform-origin: center; }
.cochlea .ring { fill: none; stroke: var(--navy); stroke-width: 1; opacity: 0; transform-box: fill-box; transform-origin: center; }
.below { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 64px; margin-top: 28px; align-items: start; }
.mission { font-size: 19px; line-height: 1.75; color: var(--ink); max-width: 31em; }
.below .more { margin-top: 22px; }
.figcap { font-size: 13px; line-height: 1.7; color: var(--ink-2); }
.figcap b { font-weight: 500; color: var(--ink); }

/* ---------- reveal (only when JS runs; CSS fallback if the script never gets going) ---------- */
html.js .rv { opacity: 0; transition: opacity 800ms var(--ease), transform 800ms var(--ease); transition-delay: calc(var(--d, 0) * 80ms); }
html.js .rv.up { transform: translateY(12px); }
html.js .in .rv, html.js .rv.in, html.rv-all .rv { opacity: 1; transform: none; }
.rule { height: 1px; background: var(--line); transform-origin: 0 50%; }
html.js .rule { transform: scaleX(0); transition: transform 1000ms var(--ease); transition-delay: calc(var(--d, 0) * 80ms); }
html.js .in .rule, html.rv-all .rule { transform: none; }
/* a [data-rv] block nested in a revealed block waits for its own intersection (people grid rows) */
html.js:not(.rv-all) .in .rv[data-rv]:not(.in) { opacity: 0; }
html.js:not(.ready) .rv, html.js:not(.ready) .rule { animation: kit-show 1ms linear 2500ms forwards; }
html.js:not(.ready) .bar i { animation: kit-gone 1ms linear 2500ms forwards; }
@keyframes kit-show { to { opacity: 1; transform: none; } }
@keyframes kit-gone { to { opacity: 0; } }

/* ---------- ruled columns ---------- */
.cols { display: grid; grid-template-columns: repeat(var(--c, 2), minmax(0, 1fr)); gap: 48px; }
.cols.c1 { --c: 1; } .cols.c3 { --c: 3; gap: 40px; } .cols.c4 { --c: 4; gap: 32px; }
.col h3 { margin-top: 20px; }
.col .d { max-width: 30em; }
.col .bullets { margin-top: 12px; }
.sg-b > .more, .sg-b > .rv > .more, .oc-more { margin-top: 40px; }
.oc-more { display: block; }

/* ---------- figure columns (plate = framed sheet on a wash panel) ---------- */
.figs .fg { margin-top: 20px; }
.figs .fg + h3 { margin-top: 18px; }
.plate { display: block; position: relative; aspect-ratio: var(--pr, 1.6); background: var(--wash); border-radius: 3px; }
.plate img { position: absolute; max-width: none; object-fit: contain; border-radius: 2px; background: var(--paper);
  box-shadow: 0 0 0 1px rgba(19, 27, 42, .1); transition: box-shadow 300ms var(--ease); }
a.plate { cursor: zoom-in; }
a.plate:hover img { box-shadow: 0 0 0 1px rgba(27, 61, 111, .55); }

/* ---------- outcomes ---------- */
.oc { display: grid; gap: 30px; }
.oc-row { display: grid; grid-template-columns: 132px minmax(0, 1fr); gap: 24px; align-items: end; }
.oc-n { font-family: var(--serif); font-weight: 300; font-size: 60px; line-height: .95; letter-spacing: -.02em; color: var(--navy); font-variant-numeric: lining-nums tabular-nums; }
.oc-t { font-size: 14.5px; color: var(--ink-2); margin-bottom: 8px; }
.bar { position: relative; overflow: hidden; height: 18px; width: calc(var(--w) * 100%); }
.bar svg { display: block; width: 100%; height: 100%; }
.bar path { stroke: var(--navy); stroke-opacity: .78; stroke-width: 1; vector-effect: non-scaling-stroke; fill: none; }
.bar i { position: absolute; inset: 0; background: var(--paper); }
html.js .bar i { transition: transform calc(var(--n) * 11ms) linear; transition-delay: calc(var(--d, 0) * 140ms + 300ms); }
html.js .in .bar i, html.rv-all .bar i { transform: translateX(101%); }
html:not(.js) .bar i { display: none; }

/* ---------- labs ---------- */
.labs { border-top: 1px solid var(--line); }
.labs li { position: relative; border-bottom: 1px solid var(--line); }
.labs a { display: grid; grid-template-columns: 230px minmax(0, 1fr) 28px; gap: 24px; align-items: baseline; padding: 26px 0 25px; text-decoration: none; position: relative; }
.labs a::after { content: ''; position: absolute; left: 0; right: 0; bottom: -1px; height: 1px; background: var(--c); transform: scaleX(0); transform-origin: 0 50%; transition: transform 500ms var(--ease); }
.labs a:hover::after, .labs a:focus-visible::after, .labs a[aria-current]::after { transform: none; }
.labs .nm { display: flex; align-items: baseline; gap: 12px; }
.labs .nm::before { content: ''; width: 14px; height: 2px; background: var(--c); flex: none; transform: translateY(-6px); }
.labs .nm b { font-family: var(--serif); font-weight: 400; font-size: 22px; line-height: 1.3; }
.labs .tm { display: block; font-size: 13px; color: var(--ink-2); margin: 2px 0 0 26px; }
.labs .ds { display: block; color: var(--ink-2); font-size: 15px; }
.labs .go { color: var(--navy); font-size: 16px; transition: transform 240ms var(--ease); justify-self: end; }
.labs a:hover .go { transform: translateX(4px); }
.faces { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; margin-top: 14px; }
.faces img, .faces .ini { width: 28px; height: 28px; border-radius: 2px; object-fit: cover; object-position: 50% 18%; filter: grayscale(1) contrast(1.04); opacity: .92; background: var(--mist); }
.ini { display: grid; place-items: center; background: var(--mist); color: var(--navy); font-family: var(--serif); font-weight: 300; line-height: 1; }
.faces .ini { font-size: 13px; opacity: 1; filter: none; }
.faces .fx { color: var(--ink-2); margin-left: 6px; }

/* ---------- data centers ---------- */
.dc h3 { font-size: 20px; margin-top: 28px; }
.dc .logo { display: flex; align-items: center; height: 36px; margin-bottom: 14px; }
.dc .logo img { width: auto; max-width: none; }
.dc .l1 { height: 41.6px; margin-left: -3.7px; }
.dc .l2 { height: 62.4px; margin-left: -15.6px; }
.dc .more { margin-top: 16px; }

/* ---------- video ---------- */
.screen { position: relative; aspect-ratio: 16 / 9; background: var(--wash); overflow: hidden; border-radius: 3px; }
.screen .poster { position: absolute; left: 6%; top: 6%; width: 88%; height: 88%; object-fit: cover; border-radius: 2px;
  box-shadow: 0 0 0 1px rgba(19, 27, 42, .1); background: var(--paper); transition: opacity 300ms ease; }
.screen video { position: absolute; inset: 0; width: 100%; height: 100%; background: #000; }
.screen.on .poster, .screen.on .play { opacity: 0; pointer-events: none; }
.play { position: absolute; left: 50%; top: 50%; width: 76px; height: 76px; margin: -38px 0 0 -38px; border-radius: 50%; border: 0; cursor: pointer;
  background: rgba(255, 255, 255, .96); box-shadow: 0 6px 30px rgba(15, 24, 40, .18); display: grid; place-items: center; transition: transform 300ms var(--ease), opacity 200ms ease; }
.play svg { width: 22px; height: 22px; margin-left: 4px; fill: var(--navy); }
.play:hover { transform: scale(1.06); }
.now { display: flex; justify-content: space-between; gap: 16px; margin-top: 16px; align-items: baseline; }
.now .t { font-family: var(--serif); font-size: 19px; }
.now .mono { color: var(--ink-2); flex: none; }
.playlist { margin-top: 30px; border-top: 1px solid var(--line); }
.playlist li { border-bottom: 1px solid var(--line); }
.playlist button { display: grid; grid-template-columns: 84px minmax(0, 1fr); gap: 14px; width: 100%; text-align: left; background: none; border: 0; cursor: pointer; padding: 14px 0 14px 14px; position: relative; align-items: center; }
.playlist button::before { content: ''; position: absolute; left: 0; top: 14px; bottom: 14px; width: 2px; background: var(--navy); transform: scaleY(0); transition: transform 400ms var(--ease); }
.playlist button[aria-current="true"]::before { transform: none; }
.playlist img { width: 84px; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 2px; background: var(--mist); }
.playlist .pt { font-size: 14px; line-height: 1.5; font-weight: 500; display: block; }
.playlist .pm { display: block; color: var(--ink-2); margin-top: 3px; }
.playlist button:hover .pt { color: var(--navy); }
.vstack .playlist { margin-top: 24px; }

/* ---------- person feature (director) ---------- */
.ft { display: grid; grid-template-columns: 200px minmax(0, 1fr); grid-template-areas: "pic who" "pic cv"; grid-template-rows: auto 1fr; gap: 0 52px; align-items: start; }
.ft.has-q { grid-template-areas: "pic q" "pic who" "pic cv"; grid-template-rows: auto auto 1fr; }
.ft-pic { grid-area: pic; width: 200px; aspect-ratio: 4 / 5; height: auto; object-fit: cover; object-position: 42% 30%; border-radius: 3px; background: var(--mist); }
.ft-pic.ini { font-size: 48px; }
.ft-q { grid-area: q; font-size: 17px; line-height: 1.95; max-width: 34em; margin-bottom: 30px; }
html[data-lang="en"] .ft-q { line-height: 1.75; }
.ft-who { grid-area: who; }
.ft-nm { font-family: var(--serif); font-size: 21px; line-height: 1.4; }
.ft-nm small { font-family: var(--sans); font-size: 13px; color: var(--ink-2); margin-left: 10px; }
.ft-cv { grid-area: cv; }
.ft-cv ul { font-size: 13.5px; line-height: 1.75; color: var(--ink-2); margin-top: 8px; }
.ft-cv .mail { display: inline-block; margin-top: 14px; }
.ft + .ft { margin-top: 56px; }

/* ---------- people grid ---------- */
.people { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 40px 24px; }
.people.sm { grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 28px 18px; }
.pc .ph { display: block; aspect-ratio: 4 / 5; border-radius: 3px; overflow: hidden; background: var(--mist); }
.pc .ph img { width: 100%; height: 100%; object-fit: cover; }
.pc .ini { width: 100%; height: 100%; font-size: 40px; }
.pc .nm { font-family: var(--serif); font-size: clamp(17px, 1.6vw, 19px); line-height: 1.35; margin-top: 14px; }
.pc .rl { font-size: 13px; line-height: 1.6; color: var(--ink-2); margin-top: 2px; }
.people.sm .nm { font-size: 16px; margin-top: 10px; }
.people.sm .ini { font-size: 30px; }
.people.rows > .pc:nth-child(4n+1) { --d: 0; } .people.rows > .pc:nth-child(4n+2) { --d: 1; }
.people.rows > .pc:nth-child(4n+3) { --d: 2; } .people.rows > .pc:nth-child(4n+4) { --d: 3; }
.people.sm.rows > .pc:nth-child(6n+1) { --d: 0; } .people.sm.rows > .pc:nth-child(6n+2) { --d: 1; } .people.sm.rows > .pc:nth-child(6n+3) { --d: 2; }
.people.sm.rows > .pc:nth-child(6n+4) { --d: 3; } .people.sm.rows > .pc:nth-child(6n+5) { --d: 4; } .people.sm.rows > .pc:nth-child(6n+6) { --d: 5; }

/* team heading (People): lab mark above the h2, optional link under the note */
.sg-h h2 > .mark:first-child { display: block; margin: 0 0 18px; transform: none; }
.sg-h .h-more { margin-top: 20px; }
.sg-h .h-more .more { font-size: 14px; }

/* ---------- in-page jump links (hero extra) ---------- */
.jump ul { display: flex; flex-wrap: wrap; gap: 6px 34px; }
.jump a { position: relative; display: inline-flex; align-items: baseline; gap: 10px; padding: 5px 0 6px; font-size: 14.5px; color: var(--ink); text-decoration: none; }
.jump .mark { transform: translateY(-3px); }
.jump .mono { color: var(--ink-2); }
.jump a::after { content: ''; position: absolute; left: 24px; right: 0; bottom: 0; height: 1px; background: var(--c); transform: scaleX(0); transform-origin: 0 50%; transition: transform 500ms var(--ease); }
.jump a:hover::after, .jump a:focus-visible::after { transform: none; }

/* ---------- gallery teaser ---------- */
.gteaser { display: grid; gap: 28px; }
.gt-row { display: flex; gap: 16px; }
.gt { flex: var(--r) 1 0; min-width: 0; }
.gt a { display: block; text-decoration: none; }
.gt .ph, .gl-open { display: block; overflow: hidden; border-radius: 3px; background: var(--mist); aspect-ratio: var(--r); }
.gt img, .gl-open img { width: 100%; height: 100%; object-fit: cover; }
.gt figcaption, .gl-it figcaption { display: flex; gap: 10px; align-items: baseline; justify-content: space-between; margin-top: 10px; font-size: 13.5px; line-height: 1.5; color: var(--ink-2); }
.gt figcaption .mono, .gl-it figcaption .mono { flex: none; }
.gt a:hover figcaption > span:first-child { color: var(--navy); }

/* ---------- full gallery + in-place viewer ---------- */
.gl { position: relative; }
.gl .tgs { margin-bottom: 28px; }
.gl-grid { display: flex; flex-wrap: wrap; gap: 28px 16px; align-content: flex-start; }   /* min-height is reserved by JS: rows stay packed at the top */
.gl .tgs[hidden] { display: none; }
.gl-grid.jx::after { display: none; }   /* JS sets each row's widths (balanced justified rows); the filler is not needed */
.gl-pb { position: absolute; left: 0; width: 1px; visibility: hidden; pointer-events: none; }   /* visible-band probes (JS) */
.gl-grid::after { content: ''; flex: 999 1 0; }
.gl-it { flex: var(--r) 1 calc(var(--r) * 250px); min-width: 0; }
.gl-it[hidden] { display: none; }
.gl-open { width: 100%; border: 0; padding: 0; cursor: zoom-in; }
.gl .pager { margin-top: 36px; }
.gl-view { position: absolute; left: 0; right: 0; z-index: 3; background: var(--paper); opacity: 0; transform: scale(.98); transition: opacity 240ms ease, transform 240ms var(--ease); }
.gl-view.on { opacity: 1; transform: none; }
.gl-view:focus { outline: none; }   /* tabindex -1: a click on the photo keeps Esc and the arrow keys working */
.gl-view[hidden] { display: none; }
.gl-vbox { position: absolute; inset: 0; display: grid; grid-template-rows: minmax(0, 1fr) auto; gap: 14px; padding: 8px 0; }
.gl-view { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }   /* the layer reads as a sheet over the grid */
.gl-view .gl-vbox { padding: 20px 0 16px; }
.gl-vimg { min-height: 0; position: relative; }
.gl-vimg img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }
.gl-vbar { display: flex; align-items: center; gap: 8px 14px; flex-wrap: wrap; }
.gl-vcap { flex: 1 1 16em; font-size: 14px; color: var(--ink); }
.gl-vcap .mono { margin-left: 12px; color: var(--ink-2); }
.gl-vn { color: var(--ink-2); }
.gl-vbar button { background: none; border: 1px solid var(--line); border-radius: 3px; height: 36px; min-width: 36px; padding: 0 12px; cursor: pointer; color: var(--navy); font-size: 14px; }
.gl-vbar button:hover { border-color: var(--navy); }

/* ---------- toggles, pager, lists ---------- */
.tgs { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 18px; }
.tgs .k { font-family: var(--mono); font-size: 11.5px; color: var(--ink-2); width: 44px; flex: none; }
.tg { position: relative; background: none; border: 0; padding: 5px 0 6px; font-size: 14px; color: var(--ink-2); cursor: pointer; }
.tg::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: var(--navy); transform: scaleX(0); transform-origin: 0 50%; transition: transform 400ms var(--ease); }
.tg:hover { color: var(--ink); }
.tg[aria-pressed="true"] { color: var(--ink); font-weight: 500; }
.tg[aria-pressed="true"]::after { transform: none; }
.pager { display: flex; align-items: center; gap: 4px; }
.pager[hidden] { display: none; }
.pager button { width: 36px; height: 36px; border: 0; background: none; color: var(--navy); font-size: 20px; line-height: 1; cursor: pointer; border-radius: 3px; }
.pager button:hover:not(:disabled) { background: var(--mist); }
.pager button:disabled { color: var(--line); cursor: default; }
.pager .pg { min-width: 60px; text-align: center; color: var(--ink-2); }
.ls-f { display: grid; gap: 4px; margin-bottom: 22px; }
.ls-f.kw .tgs .k { width: 58px; }   /* 'Country' needs a wider label column */
.ls-ruler { display: block; width: 100%; height: 14px; }
.ls-ruler line { stroke: var(--line); stroke-width: 1; vector-effect: non-scaling-stroke; }
.ls-ruler line.on { stroke: var(--navy); stroke-opacity: .8; }
.ls-meta { display: flex; justify-content: space-between; color: var(--ink-2); margin-top: 10px; }
.ls-items { border-top: 1px solid var(--line); margin-top: 10px; }
.ls-items li { padding: 16px 0 15px; border-bottom: 1px solid var(--line); }
.ls-ti { font-size: 15.5px; font-weight: 500; line-height: 1.55; }
.ls-au { font-size: 13.5px; line-height: 1.6; color: var(--ink-2); margin-top: 4px; }
.ls-mt { font-family: var(--mono); font-size: 12px; letter-spacing: .02em; color: var(--ink-2); margin-top: 6px; display: flex; flex-wrap: wrap; gap: 2px 16px; line-height: 1.6; }
.ls-tm { display: inline-flex; align-items: center; gap: 8px; }
.ls-tm::before { content: ''; width: 14px; height: 2px; background: var(--c); }
.ls-empty { padding: 28px 0; color: var(--ink-2); font-size: 14px; }
.ls .pager { margin-top: 20px; }

/* ---------- small blocks ---------- */
.bullets { display: grid; gap: 6px; }
.bullets li { color: var(--ink-2); padding-left: 22px; position: relative; font-size: 15px; line-height: 1.7; }
.bullets li::before { content: ''; position: absolute; left: 0; top: .85em; width: 10px; height: 1px; background: var(--accent); }
.kv { display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 14px 24px; }
.kv dt { font-size: 13.5px; color: var(--ink-2); padding-top: 1px; }
.logos { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; border-top: 1px solid var(--line); }
.logos li { display: grid; place-items: center; height: 112px; padding: 18px 22px; border-bottom: 1px solid var(--line); }
.logos img { max-height: 60px; width: auto; object-fit: contain; }
.box { background: var(--wash); border-radius: 3px; padding: 32px; }
.box .dc-logo { height: 56px; width: auto; margin-bottom: 18px; }
.media { border-radius: 3px; background: var(--mist); overflow: hidden; }
.media img { width: 100%; height: auto; }

/* ---------- organisation chart (org_chart: lab pages, About) ---------- */
.org-nm { font-size: 22px; line-height: 1.35; }
.org-dr { font-size: 13.5px; color: var(--ink-2); margin-top: 2px; }
.org-b { position: relative; margin-top: 18px; padding-top: 26px; }
.org-b::before { content: ''; position: absolute; left: 0; top: 0; width: 1px; height: 26px; background: var(--line); }
.org-b > .rule { position: absolute; left: 0; top: 26px; right: calc((100% - (var(--n) - 1) * 24px) / var(--n)); }
.org-u { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); gap: 0 24px; }
.org-it { position: relative; padding-top: 24px; }
.org-it::before { content: ''; position: absolute; left: 0; top: 0; width: 1px; height: 14px; background: var(--line); }
.org-it.cur::before { width: 2px; height: 24px; background: var(--c); }
a.org-x .nm { color: var(--ink-2); }
.org-x { display: block; text-decoration: none; }
.org-l { display: flex; align-items: baseline; gap: 8px; }
.org-l .nm { font-family: var(--serif); font-weight: 400; font-size: clamp(17px, 1.6vw, 20px); line-height: 1.35; white-space: nowrap; }
.org-l i { font-style: normal; font-size: 14px; color: var(--navy); transition: transform 240ms var(--ease); }
a.org-x:hover .nm { color: var(--navy); }
a.org-x:hover i { transform: translateX(4px); }
.org-tm { display: block; font-size: 13px; line-height: 1.6; color: var(--ink-2); margin-top: 2px; }
.org-here { display: block; font-size: 12.5px; line-height: 1.6; color: var(--ink-2); margin-top: 6px; }

/* ---------- data-center box (dc_box: lab pages) ---------- */
.dcb-h .logo { display: flex; align-items: center; height: 40px; }
.dcb-h img { width: auto; max-width: none; }
.dcb .l1 { height: 44px; margin-left: -3.9px; }
.dcb .l2 { height: 66px; margin-left: -16.5px; }
.dcb-s { font-size: 13px; color: var(--ink-2); margin-top: 14px; }
.dcb .prose { margin-top: 18px; }
.dcb .bullets { margin-top: 20px; }

.lang-toggle { position: fixed; right: 14px; bottom: 14px; z-index: 9; display: flex; border: 1px solid var(--line); border-radius: 3px; background: #fff; padding: 2px; }
.lang-toggle button { font: 400 12px var(--mono); border: 0; background: none; color: var(--ink-2); padding: 5px 10px; border-radius: 2px; cursor: pointer; }
.lang-toggle button[aria-pressed="true"] { background: var(--navy); color: #fff; }

/* ---------- reduced motion: fully static, everything visible ---------- */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  html.js .rv, html.js .rule { opacity: 1; transform: none; }
  .bar i { display: none; }
  .cochlea .tk { opacity: 1; }
  .coil path { stroke-dasharray: none; }
}

/* ---------- Wix mobile (320) ---------- */
@media (max-width: 760px) {
  :root { --gut: 16px; --sec: 72px; }
  body { font-size: 15px; }
  .sg { grid-template-columns: minmax(0, 1fr); gap: 0; }
  .sg-h { margin-bottom: 24px; }
  h2 { font-size: 24px; }
  .note { margin-top: 8px; max-width: none; }
  h3 { font-size: 19px; }
  .lead { font-size: 16px; }
  .hero { padding-top: 36px; }
  .inst { font-size: 13px; }
  .hero .alt { font-size: 13.5px; margin-top: 10px; }
  .hero-in h1 { margin-top: 22px; font-size: 34px; line-height: 1.15; }
  .hero-in h1 [data-l="ko"] { font-size: 36px; }
  .hero-in h1 [data-l="en"] { font-size: 29px; }
  .h1-logo img { height: 52px; }
  .hero-lablogo .h1-logo img { height: 44px; }
  .hline { margin-top: 22px; }
  .coil { width: 34px; height: 40px; }
  .hline i { margin-bottom: calc(var(--off) * 40 / 56); }
  .hero-in .lead { margin-top: 20px; }
  .stage { display: block; }
  .hero-home .title { max-width: none; padding: 0; margin-top: 18px; }
  .hero-home h1 [data-l="ko"] { font-size: 42px; }
  .hero-home h1 [data-l="en"] { font-size: 30px; line-height: 1.15; }
  .cochlea { height: 236px; margin-top: 30px; }
  .cochlea text { font-size: 10px; }
  .below { grid-template-columns: minmax(0, 1fr); gap: 22px; margin-top: 20px; }
  .mission { font-size: 16.5px; }
  .figcap { font-size: 12.5px; padding-top: 16px; border-top: 1px solid var(--line); }
  .cols, .cols.c3, .cols.c4 { grid-template-columns: minmax(0, 1fr); gap: 36px; }
  .col h3 { margin-top: 16px; }
  .sg-b > .more, .sg-b > .rv > .more, .oc-more { margin-top: 30px; }
  .oc { gap: 22px; }
  .oc-row { grid-template-columns: 78px minmax(0, 1fr); gap: 10px; }
  .oc-n { font-size: 36px; }
  .oc-t { font-size: 13.5px; margin-bottom: 6px; line-height: 1.5; }
  .bar { height: 14px; }
  .labs a { grid-template-columns: minmax(0, 1fr) 20px; gap: 6px 12px; padding: 20px 0 19px; }
  .labs .lb-b { grid-column: 1 / -1; grid-row: 2; padding-left: 26px; }
  .labs .ds { font-size: 14px; line-height: 1.7; }
  .labs .nm b { font-size: 20px; }
  .faces { margin-top: 12px; gap: 3px; }
  .faces img, .faces .ini { width: 26px; height: 26px; }
  .dc h3 { margin-top: 22px; font-size: 18px; }
  .dc .logo { height: 30px; margin-bottom: 12px; }
  .dc .l1 { height: 34.6px; margin-left: -3px; }
  .dc .l2 { height: 52px; margin-left: -13px; }
  .vids .sg { display: flex; flex-direction: column; align-items: stretch; }
  .vids .sg-h { display: contents; }
  .vids h2 { order: 0; margin-bottom: 24px; }
  .vids .sg-b { order: 1; }
  .vids .playlist { order: 2; margin-top: 20px; }
  .play { width: 60px; height: 60px; margin: -30px 0 0 -30px; }
  .play svg { width: 18px; height: 18px; }
  .now { flex-direction: column; gap: 2px; margin-top: 12px; }
  .now .t { font-size: 17px; }
  .ft, .ft.has-q { grid-template-columns: 104px minmax(0, 1fr); grid-template-areas: "pic who" "cv cv"; grid-template-rows: auto; gap: 0 18px; align-items: end; }
  .ft.has-q { grid-template-areas: "pic who" "q q" "cv cv"; }
  .ft-pic { width: 104px; }
  .ft-nm { font-size: 19px; }
  .ft-nm small { display: block; margin: 2px 0 0; }
  .ft-q { font-size: 16px; line-height: 1.9; margin: 24px 0 0; }
  .ft-cv { margin-top: 18px; }
  .ft-cv ul { margin-top: 0; font-size: 13px; }
  .people, .people.sm { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 26px 12px; }
  .pc .nm { font-size: 17px; margin-top: 10px; }
  .people.sm { grid-template-columns: minmax(0, 1fr); gap: 16px; }   /* alumni at 320: a list (3 columns broke 의료정보통계학과 mid-word) */
  .people.sm .pc { display: grid; grid-template-columns: 64px minmax(0, 1fr); grid-template-rows: auto 1fr; column-gap: 16px; }
  .people.sm .ph { grid-row: 1 / span 2; }
  .people.sm .nm { font-size: 16px; margin-top: 4px; }
  .people.sm .ini { font-size: 24px; }
  .people.rows > .pc:nth-child(2n+1) { --d: 0; } .people.rows > .pc:nth-child(2n) { --d: 1; }
  .people.sm.rows > .pc:nth-child(3n+1) { --d: 0; } .people.sm.rows > .pc:nth-child(3n+2) { --d: 1; } .people.sm.rows > .pc:nth-child(3n) { --d: 2; }
  .jump ul { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 16px; }
  .jump a { font-size: 14px; gap: 8px; padding: 6px 0 7px; white-space: nowrap; }
  .sw { grid-template-columns: minmax(0, 1fr); grid-template-areas: "head" "body" "link"; }
  .sw-head { margin-bottom: 24px; }
  .sw-link { margin: 26px 0 0; justify-self: start; }
  .gteaser { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 10px; }
  .gt-row { display: contents; }
  .gt { --r: 4 / 3; }
  .gteaser .gt:first-child { grid-column: 1 / -1; --r: 3 / 2; }
  .gt figcaption, .gl-it figcaption { display: block; font-size: 12.5px; margin-top: 7px; }
  .gt figcaption .mono, .gl-it figcaption .mono { display: block; font-size: 11px; margin-top: 1px; }
  .gl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 10px; }
  .gl-grid::after { display: none; }
  .gl-it { --r: 4 / 3; }
  .gl-it .gl-open { aspect-ratio: 4 / 3; }   /* the inline --r of each figure would otherwise win over the crop */
  .tgs { gap: 0 16px; }
  .tgs .k, .ls-f.kw .tgs .k { width: 100%; }
  .ls-items li { padding: 14px 0 13px; }
  .ls-ti { font-size: 15px; }
  .ls-au { font-size: 13px; }
  .kv { grid-template-columns: minmax(0, 1fr); gap: 2px; }
  .kv dd { margin-bottom: 14px; }
  .logos { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .logos li { height: 84px; padding: 14px; }
  .logos img { max-height: 46px; }
  .box { padding: 22px 18px; }
  .org-nm { font-size: 19px; }
  .org-b { margin-top: 12px; padding-top: 0; }
  .org-b::before, .org-b > .rule { display: none; }
  .org-u { grid-template-columns: minmax(0, 1fr); }
  .org-it { padding: 8px 0 8px 26px; }
  .org-it::before { top: 21px; width: 16px; height: 1px; }
  .org-it.cur::before { width: 16px; height: 2px; top: 20.5px; }
  .org-it::after { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 1px; background: var(--line); }
  .org-it:first-child::after { top: -12px; }
  .org-it:last-child::after { bottom: auto; height: 21px; }
  .org-l .nm { font-size: 18px; }
  .org-here { margin-top: 4px; }
  .dcb-h .logo { height: 30px; }
  .dcb .l1 { height: 34.6px; margin-left: -3px; }
  .dcb .l2 { height: 52px; margin-left: -13px; }
}
"""

# quote, box with media, map, contact rows (About, Audiso, Contact). Kept as an addition so the main CSS stays untouched.
CSS += r"""
.pq blockquote p { font-size: 21px; line-height: 1.85; color: var(--ink); max-width: 31em; text-indent: -.42em; }
html[data-lang="en"] .pq blockquote p { line-height: 1.65; }
.pq-by { display: flex; align-items: center; gap: 12px; margin-top: 22px; font-size: 13.5px; color: var(--ink-2); }
.pq-by::before { content: ''; width: 14px; height: 2px; background: var(--accent); flex: none; }
.pq-face { width: 36px; height: 36px; border-radius: 2px; object-fit: cover; object-position: 50% 20%; filter: grayscale(1) contrast(1.04); background: var(--mist); }
.pq + .prose, .pq + .rv > .prose { margin-top: 40px; }
.bx { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 32px; align-items: center; }
.bx-m img { width: 100%; height: auto; mix-blend-mode: multiply; }
.bx h3 { font-size: 20px; }
.bx-b p { color: var(--ink-2); margin-top: 6px; font-size: 14.5px; line-height: 1.7; }
.sg-b > * + .bx { margin-top: 40px; }
.map { position: relative; aspect-ratio: 2 / 1; background: var(--wash); border-radius: 3px; overflow: hidden; }
.map iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; filter: saturate(.4); }
.sg-b > * + .map { margin-top: 44px; }
.map-l { margin-top: 14px; }
.sg-b > .map-l > .more { margin-top: 0; }
.map-ph { position: absolute; inset: 0; display: grid; place-items: center; color: var(--ink-2); }
.kv dd .d { margin-top: 2px; font-size: 14px; }
.ct-who { display: flex; align-items: center; gap: 14px; }
.ct-who img { width: 40px; height: 40px; border-radius: 2px; object-fit: cover; object-position: 50% 18%; filter: grayscale(1) contrast(1.04); background: var(--mist); flex: none; }
.ct-p { display: block; font-size: 15px; color: var(--ink); line-height: 1.5; }
.ct-e { display: block; color: var(--navy); margin-top: 2px; }
.ct a { align-items: center; }
.logos li { grid-template-columns: minmax(0, 1fr); }
.logos .lg { position: relative; display: block; overflow: hidden; width: calc(var(--lw) * 1px); max-width: 100%; }
.logos .lg img { position: absolute; max-width: none; max-height: none; }
@media (max-width: 760px) {
  .pq blockquote p { font-size: 17.5px; line-height: 1.85; }
  .pq + .prose, .pq + .rv > .prose { margin-top: 30px; }
  .bx { grid-template-columns: 72px minmax(0, 1fr); gap: 18px; align-items: start; }
  .bx h3 { font-size: 17px; }
  .bx-b p { font-size: 14px; }
  .sg-b > * + .bx { margin-top: 30px; }
  .map { aspect-ratio: 4 / 3; }
  .sg-b > * + .map { margin-top: 30px; }
  .ct a { align-items: baseline; }
  .ct-who { gap: 12px; }
  .ct-who img { width: 36px; height: 36px; }
  .logos .lg { width: calc(var(--lw) * .74px); }
  /* wrap fig_cols()/ruled() in <div class="m2"> to keep two columns at 320 (short items such as products) */
  .m2 > .cols { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 30px 14px; }
  .m2 .col h3 { font-size: 16px; line-height: 1.4; margin-top: 12px; }
  .m2 .figs .fg { margin-top: 14px; }
  .m2 .d p, .m2 p.d { font-size: 13px; line-height: 1.65; }
  html[data-lang="en"] .m2 h3 { font-size: 15.5px; }
  /* gallery teaser at 320: only the very first photo spans the row; the other four sit in two pairs
     (.gt:first-child above also matched the first photo of the second .gt-row, leaving photo 2 alone in its row) */
  .gteaser .gt-row + .gt-row .gt:first-child { grid-column: auto; --r: 4 / 3; }
}
"""

# ================================================================== JS
HEAD_JS = ("(function(d){try{d.classList.add('js');var m=/[?&]lang=(en|ko)/.exec(location.search);"
           "if(m){d.setAttribute('data-lang',m[1]);d.lang=m[1];}}catch(e){}})(document.documentElement);")

JS_CORE = r"""
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var SITE = '%SITE%', ENP = '%ENP%';
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var R = window.RIHE = { lang: 'ko', reduce: reduce, hooks: [] };
  R.onLang = function (f) { R.hooks.push(f); };
  R.each = function (sel, f, ctx) { [].forEach.call((ctx || doc).querySelectorAll(sel), f); };

  /* ---------- reveal: IO per [data-rv] block, 1.5 s fallback, hold while the hero draws ---------- */
  try {
    var hold = +(root.getAttribute('data-hold') || 0), T0 = Date.now();
    // the hero animations start with the first frame, after the page scripts (list measuring) have run: count the hold from there
    if (window.requestAnimationFrame) requestAnimationFrame(function () { T0 = Date.now(); });
    var blocks = [].slice.call(doc.querySelectorAll('[data-rv]'));
    var showNow = function (b) { b.classList.add('in'); };
    var show = function (b) { var w = hold - (Date.now() - T0); if (w > 0) setTimeout(function () { showNow(b); }, w); else showNow(b); };
    if (reduce || !('IntersectionObserver' in window)) blocks.forEach(showNow);
    else {
      var alive = false;
      var io = new IntersectionObserver(function (es) {
        alive = true;
        es.forEach(function (en) { if (en.isIntersecting) { io.unobserve(en.target); show(en.target); } });
      }, { threshold: 0.08 });
      blocks.forEach(function (b) { io.observe(b); });
      setTimeout(function () { if (!alive) blocks.forEach(show); }, 1500);
    }
  } catch (err) { root.classList.add('rv-all'); }
  root.classList.add('ready');

  /* ---------- language: ?lang=en, postMessage({lang}), preview toggle ---------- */
  function setLang(l) {
    R.lang = l === 'en' ? 'en' : 'ko';
    var en = R.lang === 'en';
    root.setAttribute('data-lang', R.lang); root.lang = R.lang;
    R.each('[data-path]', function (a) { a.href = SITE + (en ? ENP : '') + a.getAttribute('data-path'); });
    R.each('[data-alt-en]', function (im) {
      if (!im.hasAttribute('data-alt-ko')) im.setAttribute('data-alt-ko', im.alt);
      im.alt = im.getAttribute(en ? 'data-alt-en' : 'data-alt-ko');
    });
    R.each('[data-aria-en]', function (x) {
      if (!x.hasAttribute('data-aria-ko')) x.setAttribute('data-aria-ko', x.getAttribute('aria-label') || '');
      x.setAttribute('aria-label', x.getAttribute(en ? 'data-aria-en' : 'data-aria-ko'));
    });
    R.each('.lang-toggle button', function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-set') === R.lang)); });
    R.hooks.forEach(function (f) { try { f(R.lang); } catch (e) {} });
  }
  R.setLang = setLang;
  // Wix page code: $w('#html1').postMessage({ lang: wixWindowFrontend.multilingual.currentLanguage })
  window.addEventListener('message', function (e) { var d = e.data; if (d && (d.lang === 'en' || d.lang === 'ko')) setLang(d.lang); });
  doc.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.lang-toggle button'); if (b) setLang(b.getAttribute('data-set')); });
  var m = /[?&]lang=(en|ko)/.exec(location.search);
  setLang(m ? m[1] : (root.getAttribute('data-lang') || 'ko'));
})();
"""

JS_COCHLEA = r"""
/* ---------- home cochlea: a tonotopic map drawn as one line, then one ambient pulse ----------
   Greenwood (1990): f = 165.4 (10^(2.1 x) - 0.88), x = 0 at the apex, 1 at the base. */
(function () {
  'use strict';
  var doc = document, svg = doc.getElementById('cochlea'), NS = 'http://www.w3.org/2000/svg';
  if (!svg) return;
  var reduce = window.RIHE.reduce;
  var C = null, visible = true, waiting = false, timer = 0, pIdx = 0;
  var FREQS = [20000, 8000, 4000, 2000, 1000, 500, 250, 125, 20];
  var PULSE = [4000, 1000, 250, 8000, 2000, 500, 125];
  function el(tag, attrs, parent) { var n = doc.createElementNS(NS, tag); for (var k in attrs) n.setAttribute(k, attrs[k]); (parent || svg).appendChild(n); return n; }
  function place(f) { return Math.log(f / 165.4 + 0.88) / Math.LN10 / 2.1; }
  function fmt(f) { return f >= 1000 ? (f / 1000) + ' kHz' : f + ' Hz'; }
  function build(animate) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var box = svg.getBoundingClientRect(), W = box.width, H = box.height;
    if (!W || !H) return;
    var small = W < 560;
    var b = 0.0985, T = 2.6 * 2 * Math.PI, a = Math.atan(b), N = 900, i;
    var U = [], minX = 1e9, maxX = -1e9, minY = 1e9, maxY = -1e9;
    for (i = 0; i <= N; i++) {
      var t = T * i / N, r = Math.exp(-b * t), ph = Math.PI / 2 + a - t;
      var x = r * Math.cos(ph), y = r * Math.sin(ph);
      U.push([x, y]);
      if (x < minX) minX = x; if (x > maxX) maxX = x; if (y < minY) minY = y; if (y > maxY) maxY = y;
    }
    var below = small ? 34 : 44, padR = small ? 40 : 70, padT = small ? 6 : 10;
    var R = Math.min((H - below - padT) / (maxY - minY), (small ? W * 0.66 : W * 0.36) / (maxX - minX));
    var yl = H - below, s0 = U[0];
    var cx = W - padR - maxX * R, cy = yl - s0[1] * R;
    var P = U.map(function (p) { return [cx + p[0] * R, cy + p[1] * R]; });
    var lead = P[0][0];
    var cum = [0], Lsp = 0;
    for (i = 1; i < P.length; i++) { Lsp += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); cum.push(Lsp); }
    var total = lead + Lsp;
    var d = 'M0 ' + yl.toFixed(2) + 'H' + P[0][0].toFixed(2);
    for (i = 1; i < P.length; i++) d += 'L' + P[i][0].toFixed(2) + ' ' + P[i][1].toFixed(2);
    var line = el('path', { d: d, 'class': 'sp' });
    var ticks = [], tickBy = {};
    FREQS.forEach(function (f) {
      var s = (1 - place(f)) * Lsp; if (s < 0) s = 0; if (s > Lsp) s = Lsp;
      var j = 1; while (j < cum.length - 1 && cum[j] < s) j++;
      var u = (s - cum[j - 1]) / ((cum[j] - cum[j - 1]) || 1);
      var px = P[j - 1][0] + (P[j][0] - P[j - 1][0]) * u, py = P[j - 1][1] + (P[j][1] - P[j - 1][1]) * u;
      var tx = P[j][0] - P[j - 1][0], ty = P[j][1] - P[j - 1][1], tl = Math.hypot(tx, ty) || 1;
      var nx = ty / tl, ny = -tx / tl;
      if (nx * (px - cx) + ny * (py - cy) < 0) { nx = -nx; ny = -ny; }
      var apex = f === 20, len = small ? 5 : 7, gap = small ? 6 : 8;
      var g = el('g', { 'class': 'tk' });
      el('line', { x1: px, y1: py, x2: px + nx * len, y2: py + ny * len }, g);
      var lx, ly, anchor;
      if (apex) { lx = cx; ly = cy + 4; anchor = 'middle'; }
      else {
        lx = px + nx * (len + gap); ly = py + ny * (len + gap);
        anchor = nx > 0.35 ? 'start' : nx < -0.35 ? 'end' : 'middle';
        ly += ny > 0.35 ? 9 : ny < -0.35 ? -2 : 4;
      }
      var label = small && (f === 8000 || f === 2000 || f === 500 || f === 125) ? '' : fmt(f), hl = null;
      if (label) {
        el('text', { x: lx, y: ly, 'text-anchor': anchor }, g).textContent = label;
        hl = el('text', { x: lx, y: ly, 'text-anchor': anchor, 'class': 'hl' }, g); hl.textContent = label;
      }
      var tk = { f: f, pos: lead + s, x: px, y: py, g: g, hl: hl };
      ticks.push(tk); tickBy[f] = tk;
    });
    var pulse = el('path', { d: d, 'class': 'pulse', 'stroke-dasharray': '1 ' + (total + 10), 'stroke-dashoffset': 2 });
    var ring = el('circle', { 'class': 'ring', cx: 0, cy: 0, r: small ? 8 : 9.5 });
    var dot = el('circle', { 'class': 'dot', cx: 0, cy: 0, r: small ? 2.4 : 3 });
    C = { total: total, ticks: ticks, tickBy: tickBy, pulse: pulse, dot: dot, ring: ring, small: small, line: line };
    // the title may use everything left of the spiral and its labels
    var left = cx + minX * R;
    [].forEach.call(svg.querySelectorAll('text'), function (t) { try { left = Math.min(left, t.getBBox().x); } catch (e) {} });
    svg.parentNode.style.setProperty('--tw', Math.max(240, left - 40) + 'px');
    if (!animate || reduce) { ticks.forEach(function (k) { k.g.classList.add('on'); }); line.style.strokeDasharray = 'none'; schedule(1200); return; }
    line.style.strokeDasharray = total + ' ' + total;
    line.style.strokeDashoffset = total;
    var t2 = small ? 1700 : 1900, vJoin = 3 * (total - lead) / t2, t1 = Math.min(900, Math.max(250, 2 * lead / vJoin)), t0 = null;
    var dur = t1 + t2;
    function at(ms) {   // ease-in along the straight lead-in, ease-out (cubic) along the coil; speeds match at the join
      if (ms <= t1) { var u = ms / t1; return lead * u * u; }
      var v = Math.min(1, (ms - t1) / t2); return lead + (total - lead) * (1 - Math.pow(1 - v, 3));
    }
    function frame(ts) {
      if (t0 === null) t0 = ts;
      var u = Math.min(1, (ts - t0) / dur), len = at(ts - t0);
      line.style.strokeDashoffset = total - len;
      ticks.forEach(function (k) { if (!k.on && len >= k.pos - 2) { k.on = true; k.g.classList.add('on'); } });
      if (u < 1) requestAnimationFrame(frame);
      else { line.style.strokeDasharray = 'none'; schedule(1400); }
    }
    requestAnimationFrame(frame);
  }
  /* the one ambient motion: a tone enters at the base, slows, and comes to rest at its place */
  function schedule(ms) { clearTimeout(timer); if (reduce) return; timer = setTimeout(pulseOnce, ms); }
  function pulseOnce() {
    if (!C || !C.pulse.animate) return;
    if (!visible || doc.hidden) { waiting = true; return; }
    var k = C.tickBy[PULSE[pIdx++ % PULSE.length]];
    var seg = C.small ? 34 : 54, dur = 1500 + 1900 * (k.pos / C.total);
    C.pulse.setAttribute('stroke-dasharray', seg + ' ' + (C.total + seg * 2));
    C.pulse.setAttribute('stroke-dashoffset', seg);
    C.pulse.animate([{ strokeDashoffset: seg }, { strokeDashoffset: seg - k.pos }], { duration: dur, easing: 'cubic-bezier(.33,.5,.3,1)' });
    C.pulse.animate([{ opacity: 0 }, { opacity: .75, offset: .18 }, { opacity: .75, offset: .78 }, { opacity: 0 }], { duration: dur });
    setTimeout(function () {
      C.dot.setAttribute('cx', k.x); C.dot.setAttribute('cy', k.y);
      C.ring.setAttribute('cx', k.x); C.ring.setAttribute('cy', k.y);
      C.dot.animate([{ opacity: 0, transform: 'scale(.3)' }, { opacity: 1, transform: 'scale(1)', offset: .18 }, { opacity: 1, offset: .55 }, { opacity: 0, transform: 'scale(1)' }], { duration: 2200, easing: 'ease-out' });
      C.ring.animate([{ opacity: .45, transform: 'scale(.25)' }, { opacity: 0, transform: 'scale(1)' }], { duration: 1500, easing: 'cubic-bezier(.22,1,.36,1)' });
      if (k.hl) k.hl.animate([{ opacity: 0 }, { opacity: 1, offset: .2 }, { opacity: 1, offset: .6 }, { opacity: 0 }], { duration: 2400, easing: 'ease-in-out' });
    }, dur * 0.8);
    schedule(dur + 4200);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible && waiting) { waiting = false; schedule(600); }
    }).observe(svg);
  }
  doc.addEventListener('visibilitychange', function () { if (!doc.hidden && waiting) { waiting = false; schedule(600); } });
  var lastW = 0, rz = 0;
  window.addEventListener('resize', function () {
    clearTimeout(rz);
    rz = setTimeout(function () { var w = svg.getBoundingClientRect().width; if (w !== lastW) { lastW = w; build(false); } }, 150);
  });
  function go() { lastW = svg.getBoundingClientRect().width; build(true); }
  var once = false, f = function () { if (!once) { once = true; go(); } };
  if (doc.fonts && doc.fonts.ready) { doc.fonts.ready.then(f); setTimeout(f, 400); } else f();
})();
"""

JS_LIST = r"""
/* ---------- paginated, filterable lists (10 per page, stable min-height, tick ruler) ---------- */
(function () {
  'use strict';
  var R = window.RIHE;
  var TEAM = %TEAM%, UI = %UI%;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function t2(p) { return '<span data-l="ko">' + p[0] + '</span><span data-l="en" lang="en">' + p[1] + '</span>'; }
  function ui(k) { return t2(UI[k] || [esc(k), esc(k)]); }
  function lg(s) { return /[\uac00-\ud7a3]/.test(String(s || '')) ? ' lang="ko"' : ' lang="en"'; }   // data strings: Hangul -> ko, else en
  function item(kind, d, teams) {
    if (kind === 'pub') {
      var tm = teams && TEAM[d.team] ? '<span class="ls-tm" style="--c:var(--' + d.team + ')">' + t2(TEAM[d.team]) + '</span>' : '';
      return '<li><p class="ls-ti"' + lg(d.title) + '>' + esc(d.title) + '</p><p class="ls-au"' + lg(d.authors) + '>' + esc(d.authors) + '</p><p class="ls-mt"><span>' + d.year + '</span><span' + lg(d.journal) + '>' + esc(d.journal) + '</span>' + tm + '</p></li>';
    }
    if (kind === 'report') return '<li><p class="ls-ti"' + lg(d.title) + '>' + esc(d.title) + '</p><p class="ls-au"' + lg(d.authors) + '>' + esc(d.authors) + '</p><p class="ls-mt"><span>' + d.year + '</span><span' + lg(d.event) + '>' + esc(d.event) + '</span></p></li>';
    return '<li><p class="ls-ti" lang="ko">' + esc(d.title) + '</p><p class="ls-mt"><span>' + ui(d.status) + '</span>' + (d.country ? '<span>' + ui(d.country) + '</span>' : '') + '</p></li>';
  }
  R.each('[data-list]', function (el) {
    var data = JSON.parse(el.querySelector('script[type="application/json"]').textContent);
    var kind = el.getAttribute('data-kind'), size = +el.getAttribute('data-size') || 10, teams = el.hasAttribute('data-teams');
    var ul = el.querySelector('.ls-items'), ticks = el.querySelectorAll('.ls-ruler line');
    var nEl = el.querySelector('.ls-n'), piEl = el.querySelector('.ls-pi'), pgEl = el.querySelector('.pager .pg');
    var prev = el.querySelector('[data-p="-1"]'), next = el.querySelector('[data-p="1"]');
    var st = { page: 0, f: {} }, maxH = 0;
    R.each('.tg', function (b) { st.f[b.getAttribute('data-k')] = 'all'; }, el);
    function pass(d) {
      for (var k in st.f) {
        var v = st.f[k];
        if (v === 'all') continue;
        if (v.charAt(0) === '~') { if (!(+d[k] <= +v.slice(1))) return false; }
        else if (String(d[k]) !== v) return false;
      }
      return true;
    }
    function rows() { var r = []; data.forEach(function (d, i) { if (pass(d)) r.push(i); }); return r; }
    function draw(r, page) {
      var view = r.slice(page * size, page * size + size);
      ul.innerHTML = view.length ? view.map(function (i) { return item(kind, data[i], teams); }).join('') : '<li class="ls-empty">' + ui('none') + '</li>';
    }
    function hold() { var h = Math.ceil(ul.getBoundingClientRect().height); if (h > maxH) { maxH = h; ul.style.minHeight = maxH + 'px'; } }
    function measure() {   // reserve the tallest page of every filter combination so the list never changes height
      // One layout per list: every item (and the empty-state line) is laid out once and its height read; the items
      // are independent blocks, so the height of any page = list border + the sum of its items' heights.
      ul.style.minHeight = ''; maxH = 0;
      ul.innerHTML = data.map(function (d) { return item(kind, d, teams); }).join('') + '<li class="ls-empty">' + ui('none') + '</li>';
      var lis = ul.children, hs = [], base = ul.getBoundingClientRect().height, best = 0;
      for (var i = 0; i < lis.length; i++) { hs.push(lis[i].getBoundingClientRect().height); base -= hs[i]; }
      var empty = hs.pop();
      var keep = {}, k, combos = [{}];
      for (k in st.f) keep[k] = st.f[k];
      Object.keys(st.f).forEach(function (key) {
        var vals = [].map.call(el.querySelectorAll('.tg[data-k="' + key + '"]'), function (b) { return b.getAttribute('data-v'); }), next = [];
        combos.forEach(function (c) { vals.forEach(function (v) { var o = {}; for (var x in c) o[x] = c[x]; o[key] = v; next.push(o); }); });
        combos = next;
      });
      combos.forEach(function (c) {
        st.f = c;
        var r = rows();
        if (!r.length) best = Math.max(best, empty);
        for (var p = 0; p < r.length; p += size) {
          var s = 0;
          for (var j = p; j < Math.min(r.length, p + size); j++) s += hs[r[j]];
          if (s > best) best = s;
        }
      });
      st.f = keep;
      maxH = Math.ceil(base + best - .01); ul.style.minHeight = maxH + 'px';
      render();
    }
    function render() {
      var r = rows(), pages = Math.max(1, Math.ceil(r.length / size));
      if (st.page >= pages) st.page = pages - 1;
      draw(r, st.page); hold();
      var on = {}; r.forEach(function (i) { on[i] = 1; });
      for (var i = 0; i < ticks.length; i++) ticks[i].setAttribute('class', on[i] ? 'on' : '');
      nEl.innerHTML = '<span data-l="ko">' + r.length + '건</span><span data-l="en" lang="en">' + r.length + (r.length === 1 ? ' item' : ' items') + '</span>';
      piEl.textContent = pgEl.textContent = (st.page + 1) + ' / ' + pages;
      prev.disabled = st.page === 0; next.disabled = st.page >= pages - 1;
      R.each('.tg', function (b) { b.setAttribute('aria-pressed', String(st.f[b.getAttribute('data-k')] === b.getAttribute('data-v'))); }, el);
    }
    el.addEventListener('click', function (e) {
      var tg = e.target.closest('.tg'), p = e.target.closest('[data-p]');
      if (tg) { st.f[tg.getAttribute('data-k')] = tg.getAttribute('data-v'); st.page = 0; render(); }
      if (p && !p.disabled) { st.page += +p.getAttribute('data-p'); render(); }
    });
    var lastW = el.offsetWidth, rz = 0;
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (el.offsetWidth !== lastW) { lastW = el.offsetWidth; measure(); } }, 200); });
    R.onLang(measure);
    measure();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  });
})();
"""

JS_VIDEO = r"""
/* ---------- video player: poster + playlist; plays only on click, native controls, fixed 16:9 box ---------- */
(function () {
  'use strict';
  var R = window.RIHE;
  R.each('[data-player]', function (pl) {
    var screen = pl.querySelector('.screen'), poster = screen.querySelector('.poster'), playBtn = screen.querySelector('.play');
    var items = [].slice.call(pl.querySelectorAll('.playlist button')), cur = 0, video = null;
    var nowT = pl.querySelector('.now .t'), nowM = pl.querySelector('.now .mono');
    function title(b, l) { var n = b.querySelector('.pt [data-l="' + l + '"]'); return n ? n.textContent : ''; }
    function sync() {
      var b = items[cur]; if (!b) return;
      nowT.innerHTML = b.querySelector('.pt').innerHTML;
      nowM.textContent = b.querySelector('.pm').textContent;
      playBtn.setAttribute('data-aria-ko', '재생: ' + title(b, 'ko'));
      playBtn.setAttribute('data-aria-en', 'Play: ' + title(b, 'en'));
      playBtn.setAttribute('aria-label', R.lang === 'en' ? 'Play: ' + title(b, 'en') : '재생: ' + title(b, 'ko'));
    }
    function stop() { if (video) { video.pause(); video.removeAttribute('src'); video.load(); screen.removeChild(video); video = null; } screen.classList.remove('on'); }
    function start() {
      var b = items[cur]; stop();
      video = document.createElement('video');
      video.controls = true; video.playsInline = true; video.preload = 'auto';
      video.poster = b.getAttribute('data-poster'); video.src = b.getAttribute('data-src');
      video.setAttribute('aria-label', title(b, R.lang));
      screen.appendChild(video); screen.classList.add('on');
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
})();
"""

JS_GALLERY = r"""
/* ---------- gallery: year toggles, 12 per page, in-place viewer (absolute, centred in the visible band).
   The grid reserves the height of its tallest page and filter, so the page never moves.
   Visible band: thin probes down the gallery, each watched by IntersectionObserver; the visible ones (intersectionRect)
   give the part of the gallery inside the top-level viewport, also in a tall cross-origin iframe.
   data-live: the photo list can be replaced by {type:'gallery', items:[...]} from Wix page code (handshake {type:'ready'}). ---------- */
(function () {
  'use strict';
  var R = window.RIHE, doc = document;
  function el(tag, cls, txt) { var n = doc.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
  R.each('[data-gallery]', function (g) {
    var grid = g.querySelector('.gl-grid'), all = [].slice.call(g.querySelectorAll('.gl-it')), size = +g.getAttribute('data-size') || 12;
    var st = { year: 'all', page: 0 }, vis = all, keepPager = false;
    var pager = g.querySelector('.pager'), pg = pager.querySelector('.pg'), prev = pager.querySelector('[data-p="-1"]'), next = pager.querySelector('[data-p="1"]');
    var view = g.querySelector('.gl-view'), vimg = doc.createElement('img'), vcap = view.querySelector('.gl-vcap'), vn = view.querySelector('.gl-vn');
    var cur = -1, opener = null, closing = 0;
    function pick(y) { return all.filter(function (f) { return y === 'all' || f.getAttribute('data-year') === y; }); }
    function show(list, p) {
      all.forEach(function (f) { f.hidden = true; });
      list.slice(p * size, p * size + size).forEach(function (f) { f.hidden = false; });
    }
    function apply() {
      vis = pick(st.year);
      var pages = Math.max(1, Math.ceil(vis.length / size));
      if (st.page >= pages) st.page = pages - 1;
      show(vis, st.page); justify();
      pager.hidden = pages < 2 && !keepPager; pager.style.visibility = pages < 2 ? 'hidden' : '';
      pg.textContent = (st.page + 1) + ' / ' + pages;
      prev.disabled = st.page === 0; next.disabled = st.page >= pages - 1;
      R.each('.tg', function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-v') === st.year)); }, g);
    }
    /* balanced justified rows (desktop): choose the row breaks that keep every row closest to a target height
       (the last row may stay short); without JS the CSS flex rows remain */
    var narrow = window.matchMedia ? matchMedia('(max-width: 760px)') : { matches: false };
    function justify() {
      var fs = all.filter(function (f) { return !f.hidden; });
      all.forEach(function (f) { f.style.flex = ''; });
      grid.classList.remove('jx');
      if (narrow.matches || !fs.length) return;
      var W = grid.clientWidth - 1, gap = parseFloat(getComputedStyle(grid).columnGap) || 16;
      var T = Math.max(220, Math.min(300, W * 0.24)), n = fs.length, rs = fs.map(function (f) { return parseFloat(f.style.getPropertyValue('--r')) || 4 / 3; });
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
      for (var e = n; e > 0; e = from[e]) {
        var b = from[e], S2 = 0, k;
        for (k = b; k < e; k++) S2 += rs[k];
        var hh = Math.min((W - gap * (e - b - 1)) / S2, e === n ? T : Infinity);
        for (k = b; k < e; k++) fs[k].style.flex = '0 0 ' + Math.floor(rs[k] * hh * 100) / 100 + 'px';
      }
      grid.classList.add('jx');
    }
    /* reserve: the grid keeps the height of its tallest page of any filter (and the pager keeps its line) */
    function reserve() {
      grid.style.minHeight = ''; keepPager = false;
      var max = 0;
      R.each('.tg', function (b) {
        var l = pick(b.getAttribute('data-v')), n = Math.ceil(l.length / size);
        if (n > 1) keepPager = true;
        for (var p = 0; p < n; p++) { show(l, p); justify(); max = Math.max(max, Math.ceil(grid.getBoundingClientRect().height)); }
      }, g);
      if (!g.querySelector('.tg')) {
        for (var p = 0, n = Math.ceil(all.length / size); p < n; p++) { show(all, p); justify(); max = Math.max(max, Math.ceil(grid.getBoundingClientRect().height)); }
      }
      if (max) grid.style.minHeight = max + 'px';
      apply(); probes();
    }
    /* visible band from probes */
    var io = null, pbs = [], seen = {}, step = 48;
    if ('IntersectionObserver' in window) {
      var th = [0, 0.25, 0.5, 0.75, 1];
      io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          var p = en.target, off = p._y, r = en.intersectionRect, b = en.boundingClientRect;
          if (en.isIntersecting && r.height > 0) seen[p._i] = [off + r.top - b.top, off + r.bottom - b.top]; else delete seen[p._i];
        });
      }, { threshold: th });
    }
    function probes() {
      if (!io) return;
      pbs.forEach(function (p) { io.unobserve(p); g.removeChild(p); }); pbs = []; seen = {};
      for (var y = 0, H = g.offsetHeight, i = 0; y < H; y += step, i++) {
        var p = el('i', 'gl-pb'); p.setAttribute('aria-hidden', 'true');
        p._y = y; p._i = i; p.style.top = y + 'px'; p.style.height = Math.min(step, H - y) + 'px';
        g.appendChild(p); pbs.push(p); io.observe(p);
      }
    }
    function band() {
      var top = Infinity, bot = -Infinity;
      for (var k in seen) { top = Math.min(top, seen[k][0]); bot = Math.max(bot, seen[k][1]); }
      return top < bot ? { top: top, bottom: bot } : null;
    }
    function fill() {
      var f = vis[cur];
      vimg.src = f.getAttribute('data-full');
      if (!vimg.parentNode) view.querySelector('.gl-vimg').appendChild(vimg);
      vimg.alt = f.querySelector('img').alt;
      vcap.innerHTML = f.querySelector('figcaption').innerHTML;
      vn.textContent = (cur + 1) + ' / ' + vis.length;
    }
    /* height follows the photo (its ratio + the caption bar), capped by the visible band; centred in the band */
    var lastC = 0;
    function place(from) {
      var W = g.offsetWidth, H = g.offsetHeight, bd = band(), gr = g.getBoundingClientRect();
      var r = parseFloat(vis[cur].style.getPropertyValue('--r')) || 4 / 3;
      if (W < 600) r = Math.max(r, 0.75);
      var bar = view.querySelector('.gl-vbar').offsetHeight + 50;
      var h = Math.min(H, W / r + bar, 720, Math.max(320, W * (W < 600 ? 1.6 : 0.62) + bar));
      if (bd) h = Math.min(h, Math.max(320, bd.bottom - bd.top - 24));
      var c = bd ? (bd.top + bd.bottom) / 2 : from ? (from.getBoundingClientRect().top + from.getBoundingClientRect().bottom) / 2 - gr.top : lastC;
      lastC = c;
      var top = Math.max(0, Math.min(H - h, c - h / 2));
      view.style.top = Math.round(top) + 'px'; view.style.height = Math.round(h) + 'px';
    }
    function open(i, from) {
      if (i < 0) return;
      clearTimeout(closing); cur = i; opener = from; fill();
      view.hidden = false; place(from);
      requestAnimationFrame(function () { view.classList.add('on'); });
      view.querySelector('.gl-close').focus({ preventScroll: true });
    }
    function close(stay) {   /* stay: focus remains on the control that was clicked (a year toggle or the pager) */
      if (view.hidden) return;
      view.classList.remove('on');
      closing = setTimeout(function () { view.hidden = true; }, R.reduce ? 0 : 200);
      if (!stay && opener && doc.contains(opener)) try { opener.focus({ preventScroll: true }); } catch (e) {}
    }
    function stepTo(dx) { cur = (cur + dx + vis.length) % vis.length; fill(); place(null); }
    g.addEventListener('click', function (e) {
      var tg = e.target.closest('.tg'), p = e.target.closest('.pager [data-p]'), o = e.target.closest('.gl-open');
      if (tg || (p && !p.disabled)) close(true);   /* the viewer belongs to the list it was opened from */
      if (tg) { st.year = tg.getAttribute('data-v'); st.page = 0; apply(); }
      if (p && !p.disabled) { st.page += +p.getAttribute('data-p'); apply(); }
      if (o) open(vis.indexOf(o.parentNode), o);
      if (e.target.closest('.gl-close')) close(false);
      if (e.target.closest('.gl-prev')) stepTo(-1);
      if (e.target.closest('.gl-next')) stepTo(1);
    });
    view.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); stepTo(-1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); stepTo(1); }
      else if (e.key === 'Tab') {   /* keep focus inside the open viewer */
        var bs = [].slice.call(view.querySelectorAll('button')), i = bs.indexOf(doc.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); bs[bs.length - 1].focus({ preventScroll: true }); }
        else if (!e.shiftKey && i === bs.length - 1) { e.preventDefault(); bs[0].focus({ preventScroll: true }); }
      }
    });
    apply(); reserve();
    var lastW = innerWidth, rt = 0;
    window.addEventListener('resize', function () {
      if (innerWidth === lastW) return; lastW = innerWidth;
      clearTimeout(rt); rt = setTimeout(reserve, 150);
    });
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(reserve);
    R.onLang(reserve);

    if (!g.hasAttribute('data-live')) return;
    /* ---------- live list: {type:'gallery', items:[...]} replaces the baked photos ---------- */
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
    function pair(ko, en, lenOk) {
      var a = el('span', '', ko), b = el('span', '', en);
      a.setAttribute('data-l', 'ko'); b.setAttribute('data-l', 'en'); b.lang = lenOk ? 'en' : 'ko';
      var s = el('span'); s.appendChild(a); s.appendChild(b); return s;
    }
    function figure(it) {
      var u = urls(it); if (!u) return null;
      var ko = String(it.caption_ko || '').trim(), enOk = !!String(it.caption_en || '').trim(), en = enOk ? String(it.caption_en).trim() : ko;
      var y = (/\d{4}/.exec(String(it.year == null ? '' : it.year)) || [''])[0];
      var r = u.w > 0 && u.h > 0 ? u.w / u.h : 4 / 3;
      r = Math.min(4, Math.max(0.4, r));
      var f = el('figure', 'gl-it');
      f.style.setProperty('--r', r.toFixed(4)); f.setAttribute('data-year', y); f.setAttribute('data-full', u.full);
      var b = el('button', 'gl-open'); b.type = 'button';
      b.setAttribute('data-aria-ko', '크게 보기: ' + ko); b.setAttribute('data-aria-en', 'View larger: ' + en);
      var im = el('img'); im.loading = 'lazy'; im.width = 600; im.height = Math.round(600 / r);
      im.setAttribute('data-alt-ko', String(it.alt_ko || ko)); im.setAttribute('data-alt-en', String(it.alt_en || en));
      if (u.mid) { im.sizes = '(max-width: 760px) 50vw, 420px'; im.srcset = u.src + ' 600w, ' + u.mid + ' 1200w'; }
      im.src = u.src;
      b.appendChild(im); f.appendChild(b);
      var fc = el('figcaption'); fc.appendChild(pair(ko, en, enOk));
      if (y && !(ko.indexOf(y) >= 0 && en.indexOf(y) >= 0)) fc.appendChild(el('span', 'mono', y));   /* no repeated year when the caption names it */
      f.appendChild(fc);
      return f;
    }
    function toggles(ys) {
      var box = g.querySelector('.tgs');
      if (!box) {
        box = el('div', 'tgs'); box.setAttribute('role', 'group');
        box.setAttribute('aria-label', '연도'); box.setAttribute('data-aria-en', 'Year');
        g.insertBefore(box, grid);
      }
      box.innerHTML = '';
      var a = el('button', 'tg'); a.type = 'button'; a.setAttribute('data-k', 'year'); a.setAttribute('data-v', 'all');
      var k = el('span', '', '전체'), e2 = el('span', '', 'All');
      k.setAttribute('data-l', 'ko'); e2.setAttribute('data-l', 'en'); e2.lang = 'en';
      a.appendChild(k); a.appendChild(e2); box.appendChild(a);
      ys.forEach(function (y) { var b = el('button', 'tg', y); b.type = 'button'; b.setAttribute('data-k', 'year'); b.setAttribute('data-v', y); box.appendChild(b); });
      box.hidden = ys.length < 2;
    }
    function setItems(items) {
      var sig; try { sig = JSON.stringify(items); } catch (e) { return; }
      if (sig === got) return;
      var figs = items.slice(0, 500).map(figure).filter(Boolean);
      if (!figs.length) return;          /* nothing usable: keep the baked photos */
      got = sig;
      if (!view.hidden) { view.classList.remove('on'); view.hidden = true; }
      grid.innerHTML = '';
      figs.forEach(function (f) { grid.appendChild(f); });
      all = figs;
      var ys = []; figs.forEach(function (f) { var y = f.getAttribute('data-year'); if (y && ys.indexOf(y) < 0) ys.push(y); });
      ys.sort(function (a, b) { return b.localeCompare(a); });
      toggles(ys);
      st = { year: 'all', page: 0 };
      R.setLang(R.lang);                 /* alt and aria per language; its hook re-runs reserve() */
      reserve();
      g.setAttribute('data-source', 'live');
    }
    window.addEventListener('message', function (e) {
      var d = e.data;
      if (typeof d === 'string' && d.charAt(0) === '{') { try { d = JSON.parse(d); } catch (err) { return; } }
      if (d && d.type === 'gallery' && Array.isArray(d.items)) setItems(d.items);
    });
    function ready() { try { if (window.parent && window.parent !== window && !got) window.parent.postMessage({ type: 'ready' }, '*'); } catch (e) {} }
    ready(); setTimeout(ready, 1500); setTimeout(ready, 4000);
  });
})();
"""


class _SerifText(html.parser.HTMLParser):
    VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr', 'line', 'path', 'circle'}

    def __init__(self):
        super().__init__()
        self.stack, self.chars = [], set()

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        cls = set((dict(attrs).get('class') or '').split())
        self.stack.append(tag in SERIF_TAGS or bool(cls & SERIF_CLASSES))

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if any(self.stack):
            self.chars.update(data)


JS_JUMP = r"""
/* ---------- in-page jump links: a #fragment click inside a cross-origin iframe does not scroll the Wix page,
   but scrollIntoView does (it scrolls every ancestor, the parent page included). Focus follows for keyboard users. ---------- */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.jump a[href^="#"]');
    if (!a) return;
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (!el) return;
    e.preventDefault();
    try { el.scrollIntoView({ block: 'start', behavior: window.RIHE && RIHE.reduce ? 'auto' : 'smooth' }); } catch (err) { el.scrollIntoView(); }
    var h = el.querySelector('h2') || el;
    if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1');
    try { h.focus({ preventScroll: true }); } catch (err) {}
  });
})();
"""


def serif_font_url(body):
    """Hahmlet stylesheet URL limited to the characters this page sets in the serif face (plus ASCII)."""
    p = _SerifText()
    p.feed(re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S))
    chars = {c for c in p.chars if not c.isspace()} | set(chr(i) for i in range(33, 127)) | set('·‘’“”…–')
    return SERIF_URL + urllib.parse.quote(''.join(sorted(chars)), safe='')


def _js(body):
    mods = [JS_CORE.replace('%SITE%', SITE).replace('%ENP%', EN_PREFIX)]
    if 'id="cochlea"' in body:
        mods.append(JS_COCHLEA)
    if 'data-list' in body:
        mods.append(JS_LIST.replace('%TEAM%', json.dumps(TEAM_LABEL, ensure_ascii=False))
                    .replace('%UI%', json.dumps({k: list(v) for k, v in UI.items()}, ensure_ascii=False)))
    if 'data-player' in body:
        mods.append(JS_VIDEO)
    if 'data-gallery' in body:
        mods.append(JS_GALLERY)
    if 'class="jump"' in body:
        mods.append(JS_JUMP)
    return '\n'.join(mods)


def page(title, accent='navy', body='', data=None, hold=None, comment=''):
    """Full HTML document. title: plain text for <title>. accent: lab key ('basic', 'hearing', 'head', 'audiso', 'navy')
    or a CSS colour; it colours the hero coil, bullets and other accent marks.
    data: optional {id: json-serialisable} emitted as <script type="application/json" id=...>.
    hold: ms to hold reveals of sections already on screen at load (default 1700 with the cochlea, else 900).
    comment: extra Korean note for the client, placed in the head comment."""
    ac = COLORS.get(accent, accent)
    if hold is None:
        hold = 1700 if 'id="cochlea"' in body else 900
    scripts = ''
    for k, v in (data or {}).items():
        scripts += f'<script type="application/json" id="{k}">{json.dumps(v, ensure_ascii=False).replace("</", "<" + chr(92) + "/")}</script>'
    toggle = ('<div class="lang-toggle" role="group" aria-label="Language">'
              '<button type="button" data-set="ko" aria-pressed="true">KO</button>'
              '<button type="button" data-set="en" aria-pressed="false">EN</button></div>') if PREVIEW else ''
    return f"""<!DOCTYPE html>
<html lang="ko" data-lang="ko" data-hold="{hold}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} · RIHE</title>
<!--
  자동 생성 파일입니다. 직접 고치지 말고 data/*.json 또는 tools/pages/*.py, tools/kit.py를 고친 뒤
  python3 tools/build.py 를 실행하세요. 같은 파일을 Wix 데스크톱(#html1)과 모바일(#mobileHtml1) 요소에 붙입니다.{(chr(10) + '  ' + comment) if comment else ''}
-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT_URL}" rel="stylesheet">
<link href="{e(serif_font_url(body))}" rel="stylesheet">
<script>{HEAD_JS}</script>
<style>{CSS}
:root {{ --accent: {ac}; }}
</style>
</head>
<body>
{body}
{toggle}
{scripts}
<script>{_js(body)}</script>
</body>
</html>
"""
