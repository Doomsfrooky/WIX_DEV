#!/usr/bin/env python3
"""Shared, design-free layer for every RIHE page and design direction.

Content and facts (copy, data/*.json), the KO/EN helpers (t, tt), links (link, more, ext), media URL helpers
(img, wix, imgur) and people helpers. No CSS, no components, no motion: those belong to a design kit
(tools/kit.py for round 2, tools/kits/<direction>.py for round 3). A kit does `from core import *`.
"""
import html
import html.parser
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.smilesnail.org'
# English pages live under SITE + EN_PREFIX + path. Wix Multilingual is OFF on the live site today,
# so /en/... returns 404 until it is enabled. Set EN_PREFIX = '' to keep English links on the Korean URLs.
EN_PREFIX = '/en'
PREVIEW = False          # build.py sets this; True adds the small KO/EN toggle
ROBOTS = 'noindex, indexifembedded'   # content pages: indexed only inside smilesnail.org, never as github.io pages

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
              '연세대학교 원주의과대학원 의료정보통계학과 겸임교수', '대한청각학회 연구이사 · 차세대 한림원 회원(2022.1~)'],
    lines_en=['Professor and Chair, Department of Otorhinolaryngology, Yonsei University Wonju College of Medicine',
              'Adjunct Professor, Department of Digital Healthcare, Yonsei University Mirae Campus',
              'Adjunct Professor, Department of Medical Informatics and Biostatistics, Yonsei University Wonju Graduate School of Medicine',
              'Director of Research, Korean Audiological Society · Member, Young Korean Academy of Science and Technology (since 2022)'],
    # shorter English credentials for Home, so EN is not much taller than KO in the fixed-height iframe
    lines_en_short=['Professor and Chair, Otorhinolaryngology, Yonsei Wonju College of Medicine',
                    'Adjunct Professor of Digital Healthcare and of Medical Informatics and Biostatistics, Yonsei University',
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

NAME_EN = {'이은수': 'Lee, Eun Soo', '이동우': 'Lee, Dongwoo',   # 2026-11-10, as the client wrote them
           '서영준': 'Young Joon Seo', '공태훈': 'Tae Hoon Kong', '기재홍': 'Jaehong Key', '변유선': 'Yuseon Byun', '이동혁': 'Donghyeok Lee',
           '윤철영': 'Chul Young Yoon', '이현수': 'Hyun Su Lee', '전진희': 'Jinhui Jeon', '강철영': 'Chulyoung Kang'}
ROLE_EN = {'교수': 'Professor', '연구소장': 'Director', '연구교수': 'Research Professor', '팀장': 'Team Leader', 'Post-doc': 'Postdoctoral Researcher',
           '박사과정': 'Ph.D. Student', '석사과정': 'M.S. Student', '학부연구원': 'Undergraduate Researcher', '연구원': 'Researcher',
           '연구간호사': 'Research Nurse', 'CTO': 'CTO', '개발': 'Development', 'AI개발': 'AI Development', '영업': 'Sales', 'QA': 'QA',
           '인증': 'Certification', '전략': 'Strategy', '이비인후과': 'Otorhinolaryngology', '생체공학과': 'Biomedical Engineering',
           '홍보': 'Public Relations', 'AI': 'AI', 'PM': 'Project Manager', 'PL': 'Project Leader'}
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
    """imgur variant: size 'b' = 160 px square crop, 'm' = 320 px, 'l' = 640 px, '' = original.
    Only i.imgur.com URLs get a size suffix; repository photos (media/...) and other URLs pass through unchanged."""
    if not size or not str(src).startswith('https://i.imgur.com/'):
        return src
    root_, ext_ = os.path.splitext(src)
    return f'{root_}{size}{ext_}'


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
        en = NAME_EN[name]
        return ko, (en.split(',')[0] if ',' in en else en.split()[-1])[0]
    return ko, ko


def member_role(m):
    """(ko, en) role line. A dict may set 'role_ko'/'role_en' directly (alumni: '박사 · 2022년 졸업' / 'Ph.D. · 2022')."""
    if m.get('role_ko') or m.get('role_en'):
        return m.get('role_ko', ''), m.get('role_en') or m.get('role_ko', '')
    ko = ' · '.join(x for x in [m.get('role', ''), m.get('dept', '')] if x)
    en = ' · '.join(x for x in [role_en(m.get('role', '')), role_en(m.get('dept', ''))] if x)
    return ko, en


# ================================================================== runtime (design-free)
# Everything below is shared infrastructure: language switching, safe reveals, the sentinel band (outer scroll
# position inside the Wix iframe), smooth in-page jumps and a headless fixed-height list engine. A kit adds its own
# CSS, markup and motion on top. No colours, fonts or layout here.

VENDOR_GSAP = 'gsap@3.15.0'          # site/vendor/<this>/  (npm gsap 3.15.0, see site/vendor/README.md)
VENDOR = {'gsap': f'{VENDOR_GSAP}/gsap.min.js', 'split': f'{VENDOR_GSAP}/SplitText.min.js',
          'ease': f'{VENDOR_GSAP}/CustomEase.min.js', 'draw': f'{VENDOR_GSAP}/DrawSVGPlugin.min.js'}

# runs in <head> before first paint: html.js (motion hiding allowed), the language from ?lang=, html.rm for reduced motion
HEAD_JS = ("(function(d){try{d.classList.add('js');var m=/[?&]lang=(en|ko)/.exec(location.search);"
           "if(m){d.setAttribute('data-lang',m[1]);d.lang=m[1];}"
           "if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('rm');}catch(e){}})(document.documentElement);")

CORE_CSS = r"""
[data-lang="ko"] [data-l="en"], [data-lang="en"] [data-l="ko"] { display: none !important; }
.sr { position: absolute !important; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
/* reveal safety. A kit hides [data-a] blocks (and [data-ai] items inside them) under html.js:not(.rm) until they get .on. If the main script never
   reaches setup (.ready), a CSS timer shows everything 2.6 s after first style; html.all shows everything at once. */
@keyframes rihe-show { to { opacity: 1; transform: none; clip-path: none; filter: none; visibility: visible; } }
html.js:not(.ready) [data-a], html.js:not(.ready) [data-ai] { animation: rihe-show .01s linear 2.6s forwards; }
html.all [data-a], html.all [data-ai] { opacity: 1 !important; transform: none !important; clip-path: none !important; filter: none !important; visibility: visible !important; }
#rihe-band { position: absolute; left: 0; top: 0; width: 1px; pointer-events: none; visibility: hidden; }
#rihe-band i { position: absolute; left: 0; width: 1px; display: block; }
.rihe-lang { position: absolute; top: 10px; right: 10px; z-index: 30; display: flex; gap: 2px; padding: 2px; background: rgba(255,255,255,.92); border: 1px solid rgba(0,0,0,.12); border-radius: 4px; }
.rihe-lang button { font: 500 11px/1 ui-monospace, Menlo, monospace; letter-spacing: .04em; border: 0; background: none; color: #555; padding: 6px 9px; border-radius: 3px; cursor: pointer; }
.rihe-lang button[aria-pressed="true"] { background: #222; color: #fff; }
"""

CORE_JS = r"""
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var R = window.RIHE = window.RIHE || {};
  R.SITE = '%SITE%'; R.ENP = '%ENP%';
  R.reduce = root.classList.contains('rm');
  R.lang = 'ko'; R.hooks = []; R.showHooks = [];
  R.each = function (sel, f, ctx) { [].forEach.call((ctx || doc).querySelectorAll(sel), f); };
  R.onLang = function (f) { R.hooks.push(f); };
  R.inFrame = (function () { try { return window.top !== window.self; } catch (e) { return true; } })();

  /* ---------- safety: content never stays hidden ---------- */
  R.showAll = function () {
    if (root.classList.contains('all')) return;
    root.classList.add('all');
    R.each('[data-a]', function (el) { el.classList.add('on'); });
    R.showHooks.forEach(function (f) { try { f(); } catch (e) {} });
  };
  R.motionReady = function () { R.motion = true; };
  // the kit's motion module must call RIHE.motionReady() within 3 s (vendor scripts load deferred), else show everything
  setTimeout(function () { if (!R.motion && doc.querySelector('[data-a]')) R.showAll(); }, 3000);

  /* ---------- inview: IntersectionObserver with thresholds only. In a cross-origin iframe (Wix + github.io)
     rootMargin is ignored and rootBounds is null; the implicit root is the top-level viewport. ---------- */
  var ioAlive = false, ioCount = 0;
  var TH = [0, .02, .05, .1, .15, .2, .25, .3, .4, .5, .6, .75, .9, 1];
  // fn(el) once el is th visible (ratio) or at least px tall on screen (tall blocks never reach a high ratio)
  R.inview = function (el, fn, o) {
    o = o || {};
    var th = o.threshold == null ? .15 : o.threshold, px = o.px == null ? 140 : o.px;
    if (R.reduce || !('IntersectionObserver' in window)) { fn(el); return; }
    ioCount++;
    var io = new IntersectionObserver(function (es) {
      ioAlive = true;
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        if (e.intersectionRatio >= th || e.intersectionRect.height >= px) { io.disconnect(); fn(el); }
      });
    }, { threshold: TH });
    io.observe(el);
  };
  // fn(true|false) whenever el enters or leaves the screen: pause work off-screen
  R.visible = function (el, fn) {
    if (!('IntersectionObserver' in window)) { fn(true); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { fn(e.isIntersecting); }); }, { threshold: 0 }).observe(el);
  };
  setTimeout(function () { if (ioCount && !ioAlive) R.showAll(); }, 1500);
  doc.addEventListener('visibilitychange', function () { R.hidden = doc.hidden; });

  /* ---------- band: the visible part of this document, in document px, also inside a tall cross-origin iframe.
     100 px sentinels tile the whole document; thresholds every 1 % make each straddling sentinel report its
     intersectionRect at 1 px steps. band = {top, bottom, h, ok}. Subscribe with RIHE.onBand(fn). ---------- */
  var band = R.band = { top: 0, bottom: 0, h: 0, ok: false, docH: 0 };
  var bandFns = [], bandOn = false;
  R.onBand = function (fn) { bandFns.push(fn); startBand(); if (band.ok) fn(band); };
  function startBand() {
    if (bandOn || !('IntersectionObserver' in window)) return;
    bandOn = true;
    var box = doc.createElement('div'); box.id = 'rihe-band'; box.setAttribute('aria-hidden', 'true');
    doc.body.appendChild(box);
    var S = 100, th = [], vis = {}, io = null, raf = 0;
    for (var i = 0; i <= 100; i++) th.push(i / 100);
    function emit() {
      raf = 0;
      var t = Infinity, b = -Infinity;
      for (var k in vis) { if (vis[k][0] < t) t = vis[k][0]; if (vis[k][1] > b) b = vis[k][1]; }
      band.ok = t !== Infinity;
      if (band.ok) { band.top = t; band.bottom = b; band.h = b - t; }
      for (var j = 0; j < bandFns.length; j++) { try { bandFns[j](band); } catch (e) {} }
    }
    // the document height without the band itself (its sentinels count in scrollHeight: measured with them, a band
    // built while the page was taller would hold the page at that height for good, a blank tail under the content)
    function docH() { box.style.display = 'none'; var h = Math.max(root.scrollHeight, doc.body.scrollHeight); box.style.display = ''; return h; }
    function build() {
      if (io) io.disconnect();
      vis = {}; box.innerHTML = '';
      var H = docH(); band.docH = H; box.style.height = H + 'px';
      io = new IntersectionObserver(function (es) {
        var sy = R.inFrame ? 0 : (window.scrollY || 0);   // top-level preview: rects are viewport-relative
        es.forEach(function (e) {
          var k = e.target.getAttribute('data-i');
          if (e.isIntersecting && e.intersectionRatio > 0) vis[k] = [e.intersectionRect.top + sy, e.intersectionRect.bottom + sy];
          else delete vis[k];
        });
        if (!raf) raf = requestAnimationFrame(emit);
      }, { threshold: th });
      for (var y = 0, n = 0; y < H; y += S, n++) {
        var s = doc.createElement('i');
        s.style.top = y + 'px'; s.style.height = Math.min(S, H - y) + 'px'; s.setAttribute('data-i', n);
        box.appendChild(s); io.observe(s);
      }
    }
    build();
    var rz = 0;
    function rebuild() { clearTimeout(rz); rz = setTimeout(function () { if (docH() !== band.docH) build(); }, 160); }
    window.addEventListener('resize', rebuild);
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { if (docH() !== band.docH) build(); });
    // any later change of the page's height (height locks, a list or gallery that reserves again) re-tiles the band;
    // the band is absolutely positioned, so it never changes the body's own size (no loop)
    if (window.ResizeObserver) new ResizeObserver(rebuild).observe(doc.body);
  }
  // element box in document px (the iframe never scrolls, so this is stable while the outer page scrolls)
  R.rect = function (el) { var r = el.getBoundingClientRect(), sy = R.inFrame ? 0 : (window.scrollY || 0); return { top: r.top + sy, bottom: r.bottom + sy, h: r.height }; };
  // 0 when el's top meets the band's bottom edge (entering), 1 when its bottom meets the band's top edge (leaving)
  R.progress = function (r) { if (!band.ok) return null; var p = (band.bottom - r.top) / (band.h + r.h); return p < 0 ? 0 : p > 1 ? 1 : p; };

  /* ---------- language: ?lang=en|ko before first paint (head script), postMessage({lang}), preview toggle ---------- */
  function setLang(l) {
    R.lang = l === 'en' ? 'en' : 'ko';
    var en = R.lang === 'en';
    root.setAttribute('data-lang', R.lang); root.lang = R.lang;
    R.each('[data-path]', function (a) { a.href = R.SITE + (en ? R.ENP : '') + a.getAttribute('data-path'); });
    R.each('[data-alt-en]', function (im) {
      if (!im.hasAttribute('data-alt-ko')) im.setAttribute('data-alt-ko', im.alt);
      im.alt = im.getAttribute(en ? 'data-alt-en' : 'data-alt-ko');
    });
    R.each('[data-aria-en]', function (x) {
      if (!x.hasAttribute('data-aria-ko')) x.setAttribute('data-aria-ko', x.getAttribute('aria-label') || '');
      x.setAttribute('aria-label', x.getAttribute(en ? 'data-aria-en' : 'data-aria-ko'));
    });
    R.each('.rihe-lang button', function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-set') === R.lang)); });
    R.hooks.forEach(function (f) { try { f(R.lang); } catch (e) {} });
  }
  R.setLang = setLang;
  // Wix page code: $w('#html1').postMessage({ lang: 'en' })
  window.addEventListener('message', function (e) { var d = e.data; if (d && (d.lang === 'en' || d.lang === 'ko') && d.lang !== R.lang) setLang(d.lang); });
  doc.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.rihe-lang button'); if (b) setLang(b.getAttribute('data-set')); });
  var m = /[?&]lang=(en|ko)/.exec(location.search);
  setLang(m ? m[1] : (root.getAttribute('data-lang') || 'ko'));

  /* ---------- smooth in-page jumps. A plain #fragment click inside the cross-origin iframe does not scroll the
     Wix page; scrollIntoView does (it scrolls every ancestor scroller). ---------- */
  R.jump = function (id) {
    var el = doc.getElementById(id); if (!el) return;
    el.scrollIntoView({ behavior: R.reduce ? 'auto' : 'smooth', block: 'start' });
    var f = el.matches('h1,h2,h3,[tabindex]') ? el : (el.querySelector('h2,h3') || el);
    if (!f.hasAttribute('tabindex')) f.setAttribute('tabindex', '-1');
    try { f.focus({ preventScroll: true }); } catch (e) {}
  };
  doc.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a && a.getAttribute('href').length > 1 && !a.hasAttribute('data-no-jump')) { e.preventDefault(); R.jump(a.getAttribute('href').slice(1)); }
  });

  /* ---------- headless list: filter, paginate, and reserve the tallest page so the height never changes ----------
     RIHE.list(el, {data, size, render(d) -> html, empty: html, after(ul, reason)}). Markup inside el:
       [data-items] list element · button[data-k][data-v] filter toggles (aria-pressed) · button[data-p="-1"|"1"] pager
       [data-n] count · [data-pi] "page / pages" (any number) · [data-ticks] container whose children get .on per item */
  R.list = function (el, o) {
    var data = o.data, size = o.size || 10, ul = el.querySelector('[data-items]');
    var st = { page: 0, f: {} }, base = 0;
    R.each('button[data-k]', function (b) { st.f[b.getAttribute('data-k')] = 'all'; }, el);
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
    function measure() {
      ul.style.minHeight = '';
      ul.innerHTML = data.map(o.render).join('') + o.empty;
      var lis = ul.children, hs = [], total = ul.getBoundingClientRect().height, best = 0;
      for (var i = 0; i < lis.length; i++) { hs.push(lis[i].getBoundingClientRect().height); total -= hs[i]; }
      var empty = hs.pop(), keep = {}, k, combos = [{}];
      for (k in st.f) keep[k] = st.f[k];
      Object.keys(st.f).forEach(function (key) {
        var vals = [].map.call(el.querySelectorAll('button[data-k="' + key + '"]'), function (b) { return b.getAttribute('data-v'); }), nx = [];
        combos.forEach(function (c) { vals.forEach(function (v) { var x = {}; for (var y in c) x[y] = c[y]; x[key] = v; nx.push(x); }); });
        combos = nx;
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
      st.f = keep; base = total;
      ul.style.minHeight = Math.ceil(base + best - .01) + 'px';
      draw('measure');
    }
    function draw(reason) {
      var r = rows(), pages = Math.max(1, Math.ceil(r.length / size));
      if (st.page >= pages) st.page = pages - 1;
      var view = r.slice(st.page * size, st.page * size + size);
      ul.innerHTML = view.length ? view.map(function (i) { return o.render(data[i]); }).join('') : o.empty;
      var on = {}; r.forEach(function (i) { on[i] = 1; });
      var tk = el.querySelector('[data-ticks]');
      if (tk) for (var i = 0; i < tk.children.length; i++) tk.children[i].classList.toggle('on', !!on[i]);
      R.each('[data-n]', function (n) { n.innerHTML = '<span data-l="ko">' + r.length + '건</span><span data-l="en" lang="en">' + r.length + (r.length === 1 ? ' item' : ' items') + '</span>'; }, el);
      R.each('[data-pi]', function (n) { n.textContent = (st.page + 1) + ' / ' + pages; }, el);
      R.each('button[data-p]', function (b) { var d = +b.getAttribute('data-p'); b.disabled = d < 0 ? st.page === 0 : st.page >= pages - 1; }, el);
      R.each('button[data-k]', function (b) { b.setAttribute('aria-pressed', String(st.f[b.getAttribute('data-k')] === b.getAttribute('data-v'))); }, el);
      if (o.after) o.after(ul, reason);
    }
    el.addEventListener('click', function (e) {
      var tg = e.target.closest('button[data-k]'), p = e.target.closest('button[data-p]');
      if (tg) { st.f[tg.getAttribute('data-k')] = tg.getAttribute('data-v'); st.page = 0; draw('filter'); }
      if (p && !p.disabled) { st.page += +p.getAttribute('data-p'); draw('page'); }
    });
    var lastW = el.offsetWidth, rz = 0;
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (el.offsetWidth !== lastW) { lastW = el.offsetWidth; measure(); } }, 200); });
    R.onLang(measure);
    measure();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(measure);
    return { redraw: draw, measure: measure };
  };

  root.classList.add('ready');
})();
"""


class _TextIn(html.parser.HTMLParser):
    """Collects the characters inside given tags / classes (for Google Fonts text= subsets)."""

    def __init__(self, tags, classes):
        super().__init__()
        self.tags, self.classes, self.stack, self.chars = set(tags), set(classes), [], set()

    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'img', 'input', 'meta', 'link', 'source', 'wbr', 'hr'):
            return
        cls = set((dict(attrs).get('class') or '').split())
        self.stack.append(tag in self.tags or bool(cls & self.classes))

    def handle_endtag(self, tag):
        if tag in ('br', 'img', 'input', 'meta', 'link', 'source', 'wbr', 'hr'):
            return
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if any(self.stack):
            self.chars.update(data)


def chars_in(body, tags=(), classes=(), extra=''):
    """Unique characters set inside the given tags/classes of body (scripts and styles skipped), plus ASCII and extra."""
    p = _TextIn(tags, classes)
    p.feed(re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S))
    chars = {c for c in p.chars if not c.isspace()} | {chr(i) for i in range(33, 127)} | set('·‘’“”…–') | set(extra)
    return ''.join(sorted(chars))


def gfont(spec, text=None):
    """Google Fonts css2 URL. spec: 'Noto+Serif+KR:wght@400;600'. text: only these glyphs (one small file)."""
    u = f'https://fonts.googleapis.com/css2?family={spec}&display=swap'
    return u + ('&text=' + urllib.parse.quote(text, safe='') if text else '')


def json_script(obj, id_=''):
    i = f' id="{id_}"' if id_ else ''
    return f'<script type="application/json"{i}>{json.dumps(obj, ensure_ascii=False).replace("</", "<" + chr(92) + "/")}</script>'


def page_shell(title, body, css='', js='', fonts=(), vendor=(), prefix='', robots=None, lang_toggle=False, comment='', html_attrs=''):
    """Whole document. css/js: the kit's. fonts: stylesheet URLs. vendor: keys of VENDOR or paths under site/vendor/.
    prefix: path from the output file to site/ ('' for site/x.html, '../' for site/_directions/x.html).
    The kit's js runs after the deferred vendor scripts (DOMContentLoaded); if it throws, everything is shown."""
    rob = robots or ROBOTS
    pre = ''.join(f'<link rel="preconnect" href="{h}"{" crossorigin" if "gstatic" in h else ""}>'
                  for h in ('https://fonts.googleapis.com', 'https://fonts.gstatic.com') if fonts)
    links = ''.join(f'<link href="{html.escape(u)}" rel="stylesheet">' for u in fonts)
    scripts = ''.join(f'<script src="{prefix}vendor/{VENDOR.get(v, v)}" defer></script>' for v in vendor)
    toggle = ('<div class="rihe-lang" role="group" aria-label="Language"><button type="button" data-set="ko" aria-pressed="true">KO</button>'
              '<button type="button" data-set="en" aria-pressed="false">EN</button></div>') if lang_toggle else ''
    if prefix:   # repository photos (data paths 'media/...', relative to site/) from pages that live deeper than site/
        body = re.sub(r'((?:src|href|poster)=")media/', lambda m: m.group(1) + prefix + 'media/', body)
        body = re.sub(r'srcset="[^"]*"', lambda m: re.sub(r'(^srcset="|,\s*)media/', lambda n: n.group(1) + prefix + 'media/', m.group(0)), body)
    kit_js = (f"document.addEventListener('DOMContentLoaded', function () {{ try {{\n{js}\n}} catch (err) {{ "
              f"if (window.console) console.error(err); window.RIHE && RIHE.showAll(); }} }});") if js else ''
    return f"""<!DOCTYPE html>
<html lang="ko" data-lang="ko"{(' ' + html_attrs) if html_attrs else ''}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="{rob}">
<title>{html.escape(title)}</title>
<!--
  자동 생성 파일입니다. 직접 고치지 말고 data/*.json, tools/kits/*.py, tools/core.py 를 고친 뒤 빌드하세요.{(chr(10) + '  ' + comment) if comment else ''}
-->
{pre}{links}
<script>{HEAD_JS}</script>
<style>{CORE_CSS}{css}</style>
{scripts}
</head>
<body>
{toggle}{body}
<script>{CORE_JS.replace('%SITE%', SITE).replace('%ENP%', EN_PREFIX)}</script>
<script>{kit_js}</script>
</body>
</html>
"""


# ================================================================== sample content for the round-3 direction pages
# Every string below already exists in round-1/2 copy (tools/build_v1.py, tools/pages/*.py, kit copy). Nothing new.
HOME_LEAD = (MISSION[0] + ' 난청 연구에서 세계 최고의 연구소가 되기 위해 노력합니다.',
             MISSION[1].rstrip('.') + ', and strive to become the world’s best institute in hearing research.')   # build_v1 home()
SINCE = ('2015년부터 다양한 융합 연구를 선보인 연구소입니다.', 'Since 2015 the Institute has pursued a wide range of translational research.')   # director greeting
OUTCOMES = [   # (number, (ko, en)); TECH_TRANSFERS comes from round-1 copy, the rest from data/*.json
    (len(PUBS), ('학술지 논문', 'Journal articles')),
    (len(REPORTS), ('학회 발표', 'Conference presentations')),
    (len(PATENTS), ('특허 (출원·등록)', 'Patents (filed and granted)')),
    (TECH_TRANSFERS, ('기술이전', 'Technology transfers')),
]
RESEARCH_TITLE = ('청각재활연구소의 연구 성과', 'Research output of the Institute')   # build_v1 research()
RESEARCH_LEAD = ('기초 연구, 빅데이터·인공지능, 의료기기, 임상시험을 아우르는 연구를 합니다. 연구소와의 협력을 언제나 환영합니다.',
                 'Our hearing research covers basic science, big data &amp; AI, medical devices and clinical trials. '
                 'We always welcome collaborations with our laboratory.')   # tools/pages/research.py
PEOPLE_TITLE = ('함께 연구하는 사람들', 'The people of RIHE')   # build_v1 people()
PEOPLE_LEAD = ('연세대학교 원주세브란스기독병원 청각재활연구소(RIHE) 구성원을 소개합니다.', 'Meet the members of the Research Institute of Hearing Enhancement.')
PUB_FILTERS = ('team', 'year')
TOTAL_MEMBERS = sum(len(tm['members']) for tm in PEOPLE)


def pub_years(items, keep=5):
    """Year filter values: the last `keep` years, then '~YYYY' for everything earlier (as in round 2)."""
    ys = sorted({d['year'] for d in items}, reverse=True)
    if len(ys) <= keep + 1:
        return [str(y) for y in ys]
    return [str(y) for y in ys[:keep]] + ['~' + str(ys[keep])]


def pub_teams(items):
    return [k for k in TEAM_LABEL if any(d.get('team') == k for d in items)]


def lang_attr(s):
    """lang="ko" when the string has Hangul, else lang="en" (publication titles, authors, journals)."""
    return ' lang="ko"' if re.search('[가-힣]', str(s or '')) else ' lang="en"'


def sample_mark(ko, en, sid=''):
    """Neutral scaffolding band between the page samples on a direction page ('Research 페이지 일부').
    Deliberately outside every design: grey mono label on a dotted rule. Not part of the design being judged."""
    i = f' id="{sid}"' if sid else ''
    return (f'<div class="rihe-sample"{i} role="note"><span><span data-l="ko">시안 구간 · {ko}</span>'
            f'<span data-l="en" lang="en">Sample · {en}</span></span></div>')


CORE_CSS += r"""
.rihe-sample { margin: 0; padding: 22px 16px; display: flex; align-items: center; gap: 14px; background: #fff; color: #8a8f98; font: 500 11px/1.4 ui-monospace, Menlo, monospace; letter-spacing: .06em; text-transform: uppercase; }
.rihe-sample::before, .rihe-sample::after { content: ""; flex: 1; border-top: 1px dashed #c9cdd3; }
"""
