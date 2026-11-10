#!/usr/bin/env python3
"""data/*.json과 이 파일의 문구로 새 디자인 페이지 9개를 만든다.

    python3 tools/build.py            # site/<page>.html 생성 (Wix에 붙여넣을 파일)
    python3 tools/build.py --preview  # 오른쪽 아래 KO/EN 전환 버튼이 있는 미리보기용

- 페이지 하나 = 파일 하나. 같은 파일을 데스크톱(#html1)과 모바일(#mobileHtml1)에 모두 붙인다.
- 한국어/영어가 한 파일에 들어 있다. Wix 페이지 코드가 postMessage로 언어를 알려 준다.
- 논문·발표·특허·구성원은 data/*.json 한 곳에서 관리한다. 목록은 10개씩 넘겨 보게 해서
  iframe 높이가 거의 일정하다.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.smilesnail.org'
PREVIEW = '--preview' in sys.argv


def load(name):
    with open(os.path.join(ROOT, 'data', name + '.json'), encoding='utf-8') as f:
        return json.load(f)


PUBS, REPORTS, PATENTS, PEOPLE = load('publications'), load('reports'), load('patents'), load('people')
e = html.escape


def t(ko, en, tag='span', cls=''):
    """한국어/영어 한 쌍. 영어 쪽에는 lang="en"을 붙여 스크린리더가 영어로 읽게 한다."""
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-l="ko">{ko}</{tag}><{tag}{c} data-l="en" lang="en">{en}</{tag}>'


def link(path, inner, cls='', extra=''):
    return f'<a class="{cls}" href="{SITE}{path}" data-path="{path}" target="_top"{extra}>{inner}</a>'


def more(path, ko, en):
    return link(path, t(ko, en) + '<span aria-hidden="true">→</span>', 'more')


# ------------------------------------------------------------------ 공통 스타일
CSS = r"""
:root {
  --paper: #ffffff; --ink: #111b2e; --ink-2: #475569; --line: #e3e8f0; --grid: #edf1f6;
  --navy: #1b3d6f; --navy-soft: #eef3fa;
  --basic: #2e8b57; --hearing: #4e7595; --head: #2e6e9e; --audiso: #9a6f07; --collab: #6b4fa0;
  --accent: var(--navy);
  --sans: 'IBM Plex Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, Menlo, monospace;
  --ease: cubic-bezier(.23, 1, .32, 1);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { background: var(--paper); -webkit-text-size-adjust: 100%; }
body { font-family: var(--sans); color: var(--ink); background: var(--paper); line-height: 1.7; word-break: keep-all; overflow-wrap: anywhere; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; }
a { color: inherit; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 4px; }
html[data-lang="ko"] [data-l="en"], html[data-lang="en"] [data-l="ko"] { display: none !important; }
.wrap { max-width: 1120px; margin: 0 auto; padding: 0 40px; }
.label { font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); }

/* 머리 */
.hero { padding: 64px 0 48px; }
.hero h1 { font-size: 46px; line-height: 1.2; font-weight: 700; letter-spacing: -.02em; margin: 12px 0 10px; text-wrap: balance; }
.hero .sub { font-size: 17px; font-weight: 500; color: var(--accent); }
.hero .lead { font-size: 17px; color: var(--ink-2); max-width: 36em; margin-top: 14px; }
.hero .logo { height: 72px; width: auto; margin: 6px 0 4px; display: block; }
.hero .cta { margin-top: 22px; display: flex; gap: 12px; flex-wrap: wrap; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 6px; font-size: 15px; font-weight: 600; text-decoration: none; background: var(--accent); color: #fff; transition: opacity 150ms ease; }
.btn:hover { opacity: .88; }
.btn.ghost { background: none; color: var(--accent); border: 1px solid var(--line); }

/* 구역 */
section { padding: 56px 0; border-top: 1px solid var(--line); }
h2 { font-size: 26px; font-weight: 700; letter-spacing: -.01em; margin-bottom: 24px; }
h3 { font-size: 17px; font-weight: 600; }
.prose p { font-size: 16px; color: var(--ink-2); max-width: 44em; }
.prose p + p { margin-top: 12px; }
.muted { color: var(--ink-2); }
.more { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: var(--accent); text-decoration: none; }
.more span[aria-hidden] { transition: transform 200ms var(--ease); }
.more:hover span[aria-hidden] { transform: translateX(3px); }
.split { display: grid; grid-template-columns: 1.2fr 1fr; gap: 48px; align-items: center; }
.figure img { width: 100%; height: auto; border-radius: 6px; display: block; }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 2px solid var(--ink); }
.cols.c2 { grid-template-columns: repeat(2, 1fr); }
.cols.c4 { grid-template-columns: repeat(4, 1fr); }
.cols > * { padding: 20px 22px 18px; border-left: 1px solid var(--line); }
.cols.c2 > :nth-child(2n+1), .cols.c3 > :nth-child(3n+1), .cols.c4 > :nth-child(4n+1) { padding-left: 0; border-left: 0; }
.cols.c2 > :nth-child(n+3), .cols.c3 > :nth-child(n+4), .cols.c4 > :nth-child(n+5) { border-top: 1px solid var(--line); }
.cols.fig img { aspect-ratio: 4 / 3; object-fit: contain; }
.cols p { font-size: 14px; color: var(--ink-2); margin-top: 8px; line-height: 1.65; }
.cols img { width: 100%; height: auto; border-radius: 4px; margin-bottom: 14px; background: var(--grid); }
.bullets { list-style: none; margin-top: 14px; display: grid; gap: 6px; }
.bullets li { font-size: 15px; color: var(--ink-2); padding-left: 16px; position: relative; }
.bullets li::before { content: ''; position: absolute; left: 0; top: .72em; width: 6px; height: 1px; background: var(--accent); }
.quote { font-size: 18px; line-height: 1.75; border-left: 2px solid var(--accent); padding-left: 20px; max-width: 40em; }
.box { border: 1px solid var(--line); border-radius: 6px; padding: 24px; }
.box.tint { background: var(--navy-soft); border-color: transparent; }
.box .logo { height: 56px; width: auto; display: block; margin-bottom: 16px; }

/* 숫자 */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); }
.stat { padding-left: 24px; border-left: 1px solid var(--line); }
.stat:first-child { padding-left: 0; border-left: 0; }
.stat .n { font-family: var(--mono); font-size: 52px; font-weight: 500; line-height: 1.1; color: var(--accent); font-variant-numeric: tabular-nums; }
.stat .t { font-size: 15px; color: var(--ink-2); margin-top: 6px; }

/* 링크 목록(연구실 등) */
.rows { list-style: none; border-top: 2px solid var(--ink); }
.rows li { border-bottom: 1px solid var(--line); }
.rows a { display: grid; grid-template-columns: 220px 1fr auto; gap: 24px; align-items: baseline; padding: 18px 8px 18px 18px; text-decoration: none; position: relative; transition: background-color 200ms var(--ease); }
.rows a::before { content: ''; position: absolute; left: 0; top: 20px; bottom: 20px; width: 3px; border-radius: 2px; background: var(--c, var(--accent)); }
.rows a:hover { background: var(--navy-soft); }
.rows .name { font-size: 17px; font-weight: 600; }
.rows .sub { display: block; font-size: 13px; color: var(--ink-2); font-weight: 400; }
.rows .desc { font-size: 15px; color: var(--ink-2); }
.rows .go { font-family: var(--mono); color: var(--accent); }

/* 사람 */
.person { display: grid; grid-template-columns: 200px 1fr; gap: 40px; align-items: start; }
.person + .person { margin-top: 36px; }
.person img, .person .ph { width: 100%; aspect-ratio: 1 / 1.05; object-fit: cover; border-radius: 6px; background: var(--grid); }
.person .who { font-size: 20px; font-weight: 700; }
.person .role { font-family: var(--mono); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.person ul { list-style: none; margin-top: 8px; font-size: 14px; color: var(--ink-2); }
.person ul li { padding: 2px 0; }
.mail { display: inline-block; margin-top: 14px; font-family: var(--mono); font-size: 14px; color: var(--accent); }
.members { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 28px 20px; }
.member { text-align: left; }
.member img, .member .ph { width: 100%; aspect-ratio: 1 / 1.1; object-fit: cover; border-radius: 6px; background: var(--grid); display: block; margin-bottom: 10px; }
.ph { display: flex !important; align-items: center; justify-content: center; font-size: 28px; font-weight: 600; color: var(--ink-2); }
.member .nm { font-size: 16px; font-weight: 600; line-height: 1.4; }
.member .rl { font-size: 13px; color: var(--ink-2); }
.team-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 22px; }
.team-nav a { font-size: 14px; padding: 6px 14px; border: 1px solid var(--line); border-radius: 999px; text-decoration: none; color: var(--ink-2); }
.team-nav a:hover { border-color: var(--accent); color: var(--accent); }
.team-h { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
.team-h h2 { margin: 0; }
.team-h .dot { width: 10px; height: 10px; border-radius: 2px; background: var(--c); align-self: center; }

/* 조직도 */
.org { display: grid; gap: 10px; }
.org .top { border: 1px solid var(--line); border-radius: 6px; padding: 14px 18px; font-weight: 600; }
.org .units { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.org .unit { border: 1px solid var(--line); border-radius: 6px; padding: 12px 14px; font-size: 14px; color: var(--ink-2); text-decoration: none; border-top: 3px solid var(--c); }
.org .unit.on { background: var(--navy-soft); color: var(--ink); font-weight: 600; }

/* 목록 (논문·발표·특허) */
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.chips .k { font-family: var(--mono); font-size: 12px; color: var(--ink-2); width: 44px; align-self: center; }
.chip { font: 500 13px var(--sans); padding: 5px 12px; border-radius: 999px; border: 1px solid var(--line); background: #fff; color: var(--ink-2); cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: #fff; }
.list-meta { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin: 14px 0 4px; font-size: 13px; color: var(--ink-2); }
.items { list-style: none; border-top: 2px solid var(--ink); }
.items li { padding: 14px 0; border-bottom: 1px solid var(--line); }
.items .ti { font-size: 15px; font-weight: 500; line-height: 1.55; }
.items .au { font-size: 13px; color: var(--ink-2); margin-top: 3px; }
.items .mt { font-family: var(--mono); font-size: 12px; color: var(--ink-2); margin-top: 5px; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.items .tm { color: var(--c); }
.pager { display: flex; align-items: center; gap: 10px; }
.pager button { font: 500 14px var(--mono); width: 34px; height: 34px; border-radius: 6px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; }
.pager button:disabled { opacity: .35; cursor: default; }
.pager .pg { font-family: var(--mono); font-size: 13px; min-width: 56px; text-align: center; }
.empty { padding: 28px 0; color: var(--ink-2); font-size: 14px; }

/* 파트너 */
.logos { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.logos div { border: 1px solid var(--line); border-radius: 6px; height: 96px; display: flex; align-items: center; justify-content: center; padding: 14px; }
.logos img { max-height: 64px; width: auto; object-fit: contain; }

/* 연락처 */
.kv { display: grid; grid-template-columns: 120px 1fr; gap: 10px 20px; font-size: 15px; }
.kv dt { font-family: var(--mono); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-2); padding-top: 3px; }
.map { width: 100%; height: 360px; border: 0; border-radius: 6px; background: var(--grid); }

/* 청력도 (홈) */
.audiogram { width: 100%; height: auto; display: block; overflow: visible; }
.audiogram .g { stroke: var(--grid); stroke-width: 1; }
.audiogram .g.major { stroke: #dde3ec; }
.audiogram .axis { font-family: var(--mono); font-size: 11px; fill: var(--ink-2); }
.audiogram .band { fill: var(--navy-soft); }
.audiogram .band-edge { stroke: var(--navy); stroke-width: 1.5; stroke-dasharray: 4 4; }
.audiogram .cap { font-size: 12px; fill: var(--navy); font-weight: 500; }
.hero-grid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 56px; align-items: center; }
.fig-note { margin-top: 10px; font-size: 12px; color: var(--ink-2); }

.lang-toggle { position: fixed; right: 16px; bottom: 16px; z-index: 5; display: flex; border: 1px solid var(--line); border-radius: 999px; background: #fff; padding: 3px; box-shadow: 0 4px 16px rgba(17, 27, 46, .08); }
.lang-toggle button { font: 500 13px var(--mono); border: 0; background: none; color: var(--ink-2); padding: 6px 12px; border-radius: 999px; cursor: pointer; }
.lang-toggle button[aria-pressed="true"] { background: var(--navy); color: #fff; }

.rise { opacity: 0; transform: translateY(12px); animation: rise 700ms var(--ease) forwards; animation-delay: calc(var(--i, 0) * 90ms); }
@keyframes rise { to { opacity: 1; transform: none; } }
.draw { stroke-dasharray: 600; stroke-dashoffset: 600; animation: draw 1200ms var(--ease) forwards; animation-delay: calc(200ms + var(--i, 0) * 40ms); }
@keyframes draw { to { stroke-dashoffset: 0; } }
.band { opacity: 0; animation: fade 900ms var(--ease) 700ms forwards; }
@keyframes fade { to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) {
  .rise, .band { opacity: 1; transform: none; animation: none; }
  .draw { stroke-dashoffset: 0; animation: none; }
  .more span[aria-hidden], .rows a, .btn { transition: none; }
}

/* 모바일 (Wix 모바일 레이아웃 320px) */
@media (max-width: 760px) {
  .wrap { padding: 0 18px; }
  .hero { padding: 36px 0 28px; }
  .hero h1 { font-size: 30px; }
  .hero .sub, .hero .lead { font-size: 15px; }
  .hero .logo { height: 52px; }
  .hero-grid, .split { grid-template-columns: 1fr; gap: 24px; }
  section { padding: 36px 0; }
  h2 { font-size: 21px; margin-bottom: 16px; }
  .cols, .cols.c2, .cols.c4 { grid-template-columns: 1fr; }
  .cols > *, .cols.c2 > *, .cols.c3 > *, .cols.c4 > * { padding: 16px 0; border-left: 0; border-top: 1px solid var(--line); }
  .cols > :first-child { border-top: 0; }
  .stats { grid-template-columns: 1fr; gap: 14px; }
  .stat, .stat:first-child { padding: 0 0 0 14px; border-left: 2px solid var(--accent); }
  .stat .n { font-size: 38px; }
  .rows a { grid-template-columns: 1fr auto; gap: 4px 12px; padding: 14px 4px 14px 14px; }
  .rows .desc { grid-column: 1 / -1; grid-row: 2; font-size: 14px; }
  .person { grid-template-columns: 1fr; gap: 16px; }
  .person img, .person .ph { width: 128px; }
  .quote { font-size: 15px; padding-left: 14px; }
  .members { grid-template-columns: repeat(2, 1fr); gap: 20px 14px; }
  .org .units { grid-template-columns: repeat(2, 1fr); }
  .logos { grid-template-columns: repeat(2, 1fr); }
  .logos div { height: 72px; }
  .kv { grid-template-columns: 1fr; gap: 2px; }
  .kv dd { margin-bottom: 10px; }
  .map { height: 240px; }
  .chips .k { width: 100%; }
  .list-meta { flex-direction: column; align-items: flex-start; }
}
"""

# ------------------------------------------------------------------ 공통 스크립트
JS = r"""
(function () {
  var SITE = 'https://www.smilesnail.org';
  var LANG = 'ko', hooks = [];
  window.RIHE = { onLang: function (f) { hooks.push(f); }, lang: function () { return LANG; } };
  function setLang(l) {
    LANG = l === 'en' ? 'en' : 'ko';
    document.documentElement.setAttribute('data-lang', LANG);
    document.documentElement.lang = LANG;
    document.querySelectorAll('[data-path]').forEach(function (a) {
      a.href = SITE + (LANG === 'en' ? '/en' : '') + a.getAttribute('data-path');
    });
    document.querySelectorAll('.lang-toggle button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-set') === LANG));
    });
    hooks.forEach(function (f) { f(LANG); });
  }
  // Wix 페이지 코드가 언어를 보냄: $w('#html1').postMessage({ lang: wixWindow.multilingual.currentLanguage })
  window.addEventListener('message', function (e) { if (e.data && e.data.lang) setLang(e.data.lang); });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.lang-toggle button');
    if (b) setLang(b.getAttribute('data-set'));
  });

  // ---- 목록: 필터 + 10개씩 넘기기 (높이가 거의 일정하게 유지됨)
  var TEAM = {
    basic: ['Basic Lab', 'Basic Lab'], hearing: ['Hearing Lab', 'Hearing Lab'],
    head: ['HeAD Lab', 'HeAD Lab'], collab: ['협력·임상', 'Collab & Medical']
  };
  var UI = {
    all: ['전체', 'All'], team: ['팀', 'Team'], year: ['연도', 'Year'], total: ['총 ', ''], unit: ['건', ' items'],
    prev: ['이전', 'Previous'], next: ['다음', 'Next'], none: ['해당 조건의 항목이 없습니다.', 'No items match this filter.'],
    '등록': ['등록', 'Granted'], '출원': ['출원', 'Filed'], '대한민국': ['대한민국', 'Korea'], '미국': ['미국', 'USA'],
    '중국': ['중국', 'China'], '유럽': ['유럽', 'Europe']
  };
  function u(k) { var v = UI[k]; return v ? v[LANG === 'en' ? 1 : 0] : k; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function mountList(root) {
    var data = JSON.parse(document.getElementById(root.getAttribute('data-src')).textContent);
    var kind = root.getAttribute('data-kind'), size = 10;
    var withTeams = root.hasAttribute('data-teams'), withYears = kind !== 'patent';
    var st = { team: 'all', year: 'all', page: 0 };
    // 연도 버튼: 최근 5개 연도 + 그 이전은 한 묶음 (데이터에 따라 자동)
    var years = [], cut = null;
    if (withYears) {
      years = data.map(function (d) { return d.year; }).filter(function (y, i, a) { return a.indexOf(y) === i; }).sort(function (a, b) { return b - a; });
      if (years.length > 6) { cut = years[5]; years = years.slice(0, 5); }
    }
    function pass(d) {
      if (st.team !== 'all' && d.team !== st.team) return false;
      if (st.year === 'all') return true;
      if (st.year === 'old') return d.year <= cut;
      return d.year === st.year;
    }
    function chips() {
      var h = '';
      if (withTeams) {
        h += '<div class="chips" role="group"><span class="k">' + u('team') + '</span>' + chip('team', 'all', u('all'));
        Object.keys(TEAM).forEach(function (k) {
          if (data.some(function (d) { return d.team === k; })) h += chip('team', k, TEAM[k][LANG === 'en' ? 1 : 0]);
        });
        h += '</div>';
      }
      if (withYears) {
        h += '<div class="chips" role="group"><span class="k">' + u('year') + '</span>' + chip('year', 'all', u('all'));
        years.forEach(function (y) { h += chip('year', y, y); });
        if (cut) h += chip('year', 'old', '~' + cut);
        h += '</div>';
      }
      return h;
    }
    function chip(k, v, label) {
      return '<button type="button" class="chip" data-k="' + k + '" data-v="' + v + '" aria-pressed="' + (String(st[k]) === String(v)) + '">' + label + '</button>';
    }
    function item(d) {
      if (kind === 'pub') {
        var tm = TEAM[d.team];
        return '<li><div class="ti">' + esc(d.title) + '</div><div class="au">' + esc(d.authors) + '</div><div class="mt"><span>' + d.year + '</span><span>' + esc(d.journal) + '</span>' +
          (withTeams && tm ? '<span class="tm" style="--c:var(--' + d.team + ')">' + tm[LANG === 'en' ? 1 : 0] + '</span>' : '') + '</div></li>';
      }
      if (kind === 'report') {
        return '<li><div class="ti">' + esc(d.title) + '</div><div class="au">' + esc(d.authors) + '</div><div class="mt"><span>' + d.year + '</span><span>' + esc(d.event) + '</span></div></li>';
      }
      return '<li><div class="ti">' + esc(d.title) + '</div><div class="mt"><span>' + u(d.status) + '</span>' + (d.country ? '<span>' + u(d.country) + '</span>' : '') + '</div></li>';
    }
    function render() {
      var rows = data.filter(pass), pages = Math.max(1, Math.ceil(rows.length / size));
      if (st.page >= pages) st.page = pages - 1;
      var view = rows.slice(st.page * size, st.page * size + size);
      root.innerHTML = chips() +
        '<div class="list-meta"><span>' + u('total') + rows.length + u('unit') + '</span>' +
        '<span class="pager"><button type="button" data-p="-1" aria-label="' + u('prev') + '"' + (st.page === 0 ? ' disabled' : '') + '>‹</button>' +
        '<span class="pg">' + (st.page + 1) + ' / ' + pages + '</span>' +
        '<button type="button" data-p="1" aria-label="' + u('next') + '"' + (st.page >= pages - 1 ? ' disabled' : '') + '>›</button></span></div>' +
        (view.length ? '<ul class="items"' + (LANG === 'en' ? '' : '') + '>' + view.map(item).join('') + '</ul>' : '<p class="empty">' + u('none') + '</p>');
    }
    root.addEventListener('click', function (e) {
      var c = e.target.closest('.chip'), p = e.target.closest('[data-p]');
      if (c) { var v = c.getAttribute('data-v'); st[c.getAttribute('data-k')] = /^\d+$/.test(v) ? +v : v; st.page = 0; render(); }
      if (p && !p.disabled) { st.page += +p.getAttribute('data-p'); render(); }
    });
    window.RIHE.onLang(render);
    render();
  }
  document.querySelectorAll('[data-list]').forEach(mountList);

  // ---- 청력도 격자 (홈)
  var g = document.getElementById('grid');
  if (g) {
    var NS = 'http://www.w3.org/2000/svg';
    var el = function (tag, a, txt) { var n = document.createElementNS(NS, tag); for (var k in a) n.setAttribute(k, a[k]); if (txt) n.textContent = txt; g.appendChild(n); };
    ['125', '250', '500', '1k', '2k', '4k', '8k'].forEach(function (f, i) {
      var x = 40 + i * 70;
      el('line', { x1: x, y1: 20, x2: x, y2: 280, 'class': 'g major draw', style: '--i:' + i });
      el('text', { x: x, y: 302, 'class': 'axis', 'text-anchor': 'middle' }, f);
    });
    for (var db = -10; db <= 120; db += 10) {
      var y = 20 + (db + 10) * 2;
      el('line', { x1: 40, y1: y, x2: 460, y2: y, 'class': 'g' + (db % 20 === 0 ? ' major' : '') + ' draw', style: '--i:' + (db + 10) / 10 });
      if (db % 20 === 0) el('text', { x: 30, y: y + 4, 'class': 'axis', 'text-anchor': 'end' }, String(db));
    }
    el('text', { x: 460, y: 322, 'class': 'axis', 'text-anchor': 'end' }, 'Hz');
    el('text', { x: 30, y: 12, 'class': 'axis', 'text-anchor': 'end' }, 'dB HL');
  }

  setLang(new URLSearchParams(location.search).get('lang') || 'ko');
})();
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500'
         '&family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">')


def page(title, accent, body, data=None):
    scripts = ''
    for k, v in (data or {}).items():
        payload = json.dumps(v, ensure_ascii=False).replace('</', '<\\/')
        scripts += f'<script type="application/json" id="{k}">{payload}</script>'

    toggle = ('<div class="lang-toggle" role="group" aria-label="Language">'
              '<button type="button" data-set="ko" aria-pressed="true">KO</button>'
              '<button type="button" data-set="en" aria-pressed="false">EN</button></div>') if PREVIEW else ''
    return f"""<!DOCTYPE html>
<html lang="ko" data-lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — RIHE</title>
<!-- 자동 생성 파일: tools/build.py로 만듭니다. 직접 고치지 말고 data/*.json이나 build.py를 고치세요. -->
{FONTS}
<style>{CSS}
:root {{ --accent: {accent}; }}
</style>
</head>
<body>
{body}
{toggle}
{scripts}
<script>{JS}</script>
</body>
</html>
"""


def hero(label, title, sub='', lead='', extra=''):
    return f"""<header class="hero"><div class="wrap">
<p class="label rise" style="--i:0">{label}</p>
<h1 class="rise" style="--i:1">{title}</h1>
{f'<p class="sub rise" style="--i:2">{sub}</p>' if sub else ''}
{f'<p class="lead rise" style="--i:3">{lead}</p>' if lead else ''}
{extra}
</div></header>"""


def sec(h2, inner, sid=''):
    i = f' id="{sid}"' if sid else ''
    return f'<section{i}><div class="wrap"><h2>{h2}</h2>{inner}</div></section>'


def listing(kind, src, teams=False):
    return f'<div data-list data-kind="{kind}" data-src="{src}"{" data-teams" if teams else ""}></div>'


INST = 'Yonsei University · Wonju Severance Christian Hospital'
DIRECTOR_IMG = 'https://i.imgur.com/vIAp69Y.jpeg'
DC_REF_LOGO = 'https://i.imgur.com/s6VfJ2r.png'
DC_BIG_LOGO = 'https://i.imgur.com/9cFssq8.png'

UNITS = [  # 조직도와 연구실 링크
    ('audiso', '/audiso', 'Audiso Co., Ltd.', '오디에스오(주)', 'Audiso Co., Ltd.'),
    ('basic', '/about-1', 'Basic Lab', '기초팀', 'Basic research team'),
    ('hearing', '/hearing-lab', 'Hearing Lab', '참조표준팀', 'Reference standard team'),
    ('head', '/head-lab', 'HeAD Lab', '데이터팀', 'Data team'),
]


def org(on):
    units = ''.join(link(p, f'{n}', f'unit{" on" if k == on else ""}', f' style="--c:var(--{k})"') for k, p, n, _, _ in UNITS)
    return f'<div class="org"><div class="top">Research Institute of Hearing Enhancement (RIHE)</div><div class="units">{units}</div></div>'


def person(img, role, name, lines_ko, lines_en, extra=''):
    ph = f'<img src="{img}" alt="" width="200" height="210" loading="lazy">' if img else f'<div class="ph" role="img" aria-label="{name} 사진 준비 중">{name[0]}</div>'
    return f"""<div class="person">{ph}<div>
<p class="role">{role}</p><p class="who">{name}</p>
<ul data-l="ko">{''.join(f'<li>{x}</li>' for x in lines_ko)}</ul>
<ul data-l="en" lang="en">{''.join(f'<li>{x}</li>' for x in lines_en)}</ul>{extra}</div></div>"""


def director_block(role_line=True):
    return person(DIRECTOR_IMG, 'Director', t('서영준 교수', 'Prof. Young Joon Seo'),
                  ['RIHE 연구소장', '연세대학교 원주세브란스기독병원 이비인후과'],
                  ['Director, RIHE', 'Department of Otorhinolaryngology, Wonju Severance Christian Hospital, Yonsei University'])


# ================================================================== 페이지
def home():
    counts = (len(PUBS), len(PATENTS))
    audiogram = f"""<figure class="rise" style="--i:2">
<svg class="audiogram" viewBox="0 0 480 330" aria-hidden="true">
<rect class="band" x="40" y="20" width="420" height="60"></rect><g id="grid"></g>
<line class="band-edge" x1="40" y1="80" x2="460" y2="80"></line>
<text class="cap" x="452" y="72" text-anchor="end" data-l="ko">정상 청력 범위 (≤ 20 dB HL)</text>
<text class="cap" x="452" y="72" text-anchor="end" data-l="en">Normal hearing (≤ 20 dB HL)</text></svg>
<figcaption class="fig-note">{t('청력도(audiogram). 가로축 주파수, 세로축 청력역치.', 'Audiogram: frequency across, hearing threshold down.')}</figcaption></figure>"""
    head = f"""<header class="hero"><div class="wrap hero-grid"><div>
<p class="label rise" style="--i:0">{INST}</p>
<h1 class="rise" style="--i:1">{t('청각재활연구소', 'Research Institute of Hearing Enhancement')}</h1>
<p class="sub rise" style="--i:2">{t('<span lang="en">Research Institute of Hearing Enhancement</span>', '청각재활연구소 · RIHE')}</p>
<p class="lead rise" style="--i:3">{t('난청의 기전에 대한 기초 연구를 바탕으로 치료제 개발, 임상 연구, 의료기기 개발까지 청각에 대한 전주기적 연구를 하는 연구소입니다. 난청 연구에서 세계 최고의 연구소가 되기 위해 노력합니다.',
    'Built on basic research into the mechanisms of hearing loss, we conduct full-cycle hearing research, from drug development and clinical research to medical devices, and strive to become the world’s best institute in hearing research.')}</p>
</div>{audiogram}</div></header>"""
    areas = f"""<div class="cols c4">{''.join(f'<div><h3>{h}</h3>{t(k, en_, "p")}</div>' for h, k, en_ in AREAS)}</div>
<p style="margin-top:22px">{more('/project', '논문·학회 발표·특허 보기', 'Publications, reports and patents')}</p>"""
    stats = f"""<div class="stats">
<div class="stat"><div class="n">{counts[0]}</div><div class="t">{t('학술지 논문', 'Journal articles')}</div></div>
<div class="stat"><div class="n">{counts[1]}</div><div class="t">{t('특허 (출원·등록)', 'Patents (filed and granted)')}</div></div>
<div class="stat"><div class="n">12</div><div class="t">{t('기술이전', 'Technology transfers')}</div></div></div>"""
    labs = '<ul class="rows">'
    for k, p, n, sko, sen, dko, den in LABS:
        inner = (f'<span class="name">{n}{t(sko, sen, cls="sub")}</span>'
                 f'<span class="desc">{t(dko, den)}</span><span class="go" aria-hidden="true">→</span>')
        style = f' style="--c:var(--{k})"'
        labs += f'<li>{link(p, inner, "", style)}</li>'
    labs += '</ul>'
    director = person(DIRECTOR_IMG, 'Director', t('서영준', 'Young Joon Seo'), DIRECTOR_KO, DIRECTOR_EN,
                      f'<blockquote class="quote" style="margin-top:18px">{t(GREETING_KO, GREETING_EN, "p")}</blockquote>'
                      '<a class="mail" href="mailto:okas2000@yonsei.ac.kr">okas2000@yonsei.ac.kr</a>')
    return page('Home', 'var(--navy)', head
                + sec(t('연구 분야', 'Research areas'), areas)
                + sec(t('성과', 'Outcomes'), stats)
                + sec(t('연구실', 'Labs'), labs)
                + sec(t('연구소장', 'Director'), director)
                + sec(t('데이터센터', 'Data centers'), DATA_CENTERS_HTML()))


AREAS = [
    ('Basic sciences',
     '자성 나노입자로 줄기세포가 달팽이관으로 모이는 효율(호밍)을 높이고, 엑소좀·약물·재생 유전자를 유모세포에 전달합니다.',
     'Enhancing stem-cell homing to the cochlea with nanoparticles and magnetic force, delivering exosomes, drugs and regenerative genes to hair cells.'),
    ('Big data &amp; AI',
     '국내 유일의 한국인 청각 참조표준 데이터센터로서 청각 데이터의 표준을 만들고, 어지럼증 데이터를 인공지능으로 분석합니다.',
     'As Korea’s only reference standard data center for hearing, we set standards for hearing data and analyse dizziness data with AI.'),
    ('Medical devices',
     '마취 없이 시술하는 원스톱 중이염 환기관, 스마트 안진검사, VR 어지럼증 재활, 골전도 보청기 등 임상 수요에서 출발한 의료기기를 개발합니다.',
     'A one-stop ventilation tube without anaesthesia, smart nystagmography, VR dizziness rehabilitation and bone conduction hearing aids, built from clinical needs.'),
    ('Clinical trials',
     '골전도 보청기 임상시험을 중심으로, 기초 연구의 성과(엑소좀, 약물, 의료기기)를 임상시험으로 이어 갑니다.',
     'Mainly clinical trials of bone conduction hearing aids; outputs of our basic research (exosomes, drugs, devices) move on to clinical trials.'),
]

LABS = [
    ('basic', '/about-1', 'Basic Lab', '기초팀', 'Basic research team',
     '줄기세포·나노입자·약물 전달로 난청의 기전을 연구합니다.', 'Stem cells, nanoparticles and drug delivery for the mechanisms of hearing loss.'),
    ('hearing', '/hearing-lab', 'Hearing Lab', '참조표준팀', 'Reference standard team',
     '한국인 청각 참조표준 데이터를 수집·생산합니다.', 'Collecting and producing Korean reference hearing data.'),
    ('head', '/head-lab', 'HeAD Lab', '데이터팀', 'Data team',
     '청각 빅데이터와 인공지능으로 난청을 예측하고 관리합니다.', 'Hearing big data and AI for predicting and managing hearing loss.'),
    ('audiso', '/audiso', 'Audiso', '오디에스오(주)', 'Audiso Co., Ltd.',
     '국내 최초 청력계 KOLAS 국제공인교정기관, 연구소 교원창업 기업입니다.', 'Korea’s first KOLAS-accredited audiometer calibration body; a faculty start-up of the institute.'),
]

DIRECTOR_KO = ['연세대학교 원주의과대학 이비인후과 주임교수', '연세대학교 미래캠퍼스 디지털헬스케어학과 겸임교수',
               '연세대학교 원주의과대학원 의학통계학과 겸임교수', '대한청각학회 연구이사 · 차세대 한림원 회원(2022.1~)']
DIRECTOR_EN = ['Professor and Chair, Department of Otorhinolaryngology, Yonsei University Wonju College of Medicine',
               'Adjunct Professor, Department of Digital Healthcare, Yonsei University Mirae Campus',
               'Adjunct Professor, Department of Medical Statistics, Yonsei University Wonju Graduate School of Medicine',
               'Director of Research, Korean Audiological Society · Member, Young Korean Academy of Science and Technology (since 2022)']
GREETING_KO = ('난청을 치료하는 임상의이자 난청을 연구하는 연구자로서, 청각재활연구소를 기반으로 융합 연구자의 길을 걸어왔습니다. '
               '2015년부터 다양한 융합 연구를 선보인 연구소입니다. 세계 여러 나라 청각 특성화 연구소들과 어깨를 나란히 견줄 수 있는 연구소가 되겠습니다.')
GREETING_EN = ('As a clinician who treats patients with hearing loss and a researcher who studies its pathophysiology, I have walked the path of a '
               'translational researcher based on our Institute. Since 2015 the Institute has pursued a wide range of translational research, '
               'and we will stand shoulder to shoulder with hearing research institutes around the world.')


def DATA_CENTERS_HTML():
    return f"""<div class="cols c2">
<div>{link('/hearing-lab', f'<img src="{DC_REF_LOGO}" alt="" loading="lazy" style="height:56px;width:auto">', '', ' style="text-decoration:none"')}
<h3>{t('한국인 청각 참조표준데이터센터', 'Korea Hearing Standard-data Center')}</h3>
{t('한국인의 청각 분야 데이터를 수집·생산하고 보급하는 국내 유일 기관. 2019년 1월부터 운영.', 'Korea’s only center collecting, producing and distributing Korean hearing data, since January 2019.', 'p')}</div>
<div>{link('/head-lab', f'<img src="{DC_BIG_LOGO}" alt="" loading="lazy" style="height:56px;width:auto">', '', ' style="text-decoration:none"')}
<h3>{t('청각 빅데이터센터', 'Korea Hearing Big-data Center')}</h3>
{t('산업계와 연구자에게 청각 분야의 빅데이터를 전문으로 제공하는 국내 유일 기관. 10만 건 이상의 데이터.', 'Korea’s only provider of hearing big data for industry and researchers, with over 100,000 records.', 'p')}</div></div>"""


def about():
    partners = [('e73yTmH.jpeg', 'Cochlear'), ('Gt2yITF.jpeg', 'KRISS'), ('uYE9HkB.png', 'NCSRD 국가참조표준센터'),
                ('GdiAYNJ.jpeg', '대한청각학회'), ('7WGSBl9.png', 'ILIAS Biologics'), ('sH2hnnv.jpeg', 'M.I one'),
                ('bM7xqYi.png', 'Innoshuttle'), ('pkbfNok.jpeg', 'J&amp;KYM')]
    logos = '<div class="logos">' + ''.join(f'<div><img src="https://i.imgur.com/{f}" alt="{a}" loading="lazy"></div>' for f, a in partners) + '</div>'
    intro = f"""<blockquote class="quote">{t('“난청을 치료하는 임상의이자 난청을 연구하는 연구자로서, 청각재활연구소를 기반으로 융합 연구자의 길을 걸어왔습니다.” — 서영준 연구소장',
        '“As a clinician who treats hearing loss and a researcher who studies it, I have walked the path of a translational researcher based on this Institute.” — Director Young Joon Seo', 'p')}</blockquote>
<div class="prose" style="margin-top:24px">
{t('2015년부터 다양한 융합 연구를 선보인 연구소입니다. 세계 여러 나라 청각 특성화 연구소들과 어깨를 나란히 견줄 수 있는 연구소가 되겠습니다.', 'Since 2015 the Institute has presented a wide range of translational research, and we aim to stand shoulder to shoulder with specialised hearing institutes around the world.', 'p')}
{t('청각 특성화 연구소만의 독특한 시각과 연구 방식으로 수년 동안 발전해 온 청각재활연구소의 우수한 연구들을 볼 수 있습니다.', 'Here you can find the research the Institute has developed over the years with the perspective and methods of a hearing-specialised institute.', 'p')}</div>"""
    return page('About', 'var(--navy)',
                hero(INST, t('About RIHE', 'About RIHE'), t('청각재활연구소 소개', 'Research Institute of Hearing Enhancement'),
                     t('난청에 대한 기초 연구뿐만 아니라 의료기기 개발, 임상시험에 이르기까지 전주기적인 연구를 진행하는 연세대학교 공식 연구소입니다.',
                       'An official Yonsei University institute conducting full-cycle research, from basic research on hearing loss to medical device development and clinical trials.'))
                + sec(t('청각재활연구소', 'The Institute'), intro)
                + sec(t('조직', 'Organization'), org(None))
                + sec(t('데이터센터', 'Data centers'), DATA_CENTERS_HTML())
                + sec(t('협력 기관', 'Partners'), logos))


def research():
    imgs = ['JbUTgTe.jpeg', 'EgbUUiR.jpeg', 'xqYPd2L.jpeg', 'jNAHuk5.jpeg']
    projects = '<div class="cols c4 fig">' + ''.join(
        f'<div><img src="https://i.imgur.com/{im}" alt="" loading="lazy" width="400" height="260"><h3>{h}</h3>{t(k, en_, "p")}</div>'
        for im, (h, k, en_) in zip(imgs, AREAS)) + '</div>'
    patents_note = t('출원·등록 건을 모두 포함합니다.', 'Includes filed and granted patents.', 'p', 'muted')
    return page('Research', 'var(--navy)',
                hero(INST, 'Research', t('청각재활연구소의 연구 성과', 'Research output of the Institute'),
                     t('Basic science, Big data &amp; AI, 의료기기, 임상시험을 아우르는 연구를 합니다. 연구소와의 협력을 언제나 환영합니다.',
                       'Our hearing research covers basic science, big data &amp; AI, medical devices and clinical trials. We always welcome collaborations with our laboratory.'))
                + sec('Projects', projects)
                + sec('Publication', listing('pub', 'd-pubs', teams=True), 'publication')
                + sec('Report', listing('report', 'd-reports'), 'report')
                + sec('Patents', patents_note + '<div style="margin-top:12px"></div>' + listing('patent', 'd-patents'), 'patents'),
                {'d-pubs': PUBS, 'd-reports': REPORTS, 'd-patents': PATENTS})


ROLE_EN = {'교수': 'Professor', '연구소장': 'Director', '연구교수': 'Research Professor', '팀장': 'Team Leader', 'Post-doc': 'Postdoctoral Researcher',
           '박사과정': 'Ph.D. Student', '석사과정': 'M.S. Student', '학부연구원': 'Undergraduate Researcher', '연구원': 'Researcher',
           '연구간호사': 'Research Nurse', 'CTO': 'CTO', '개발': 'Development', 'AI개발': 'AI Development', '영업': 'Sales', 'QA': 'QA',
           '인증': 'Certification', '전략': 'Strategy', '이비인후과': 'Otorhinolaryngology', '생체공학과': 'Biomedical Engineering'}
NAME_EN = {'서영준': 'Young Joon Seo', '공태훈': 'Tae Hoon Kong', '기재홍': 'Jaehong Key', '변유선': 'Yuseon Byun', '이동혁': 'Donghyeok Lee',
           '윤철영': 'Chul Young Yoon', '이현수': 'Hyun Su Lee', '전진희': 'Jinhui Jeon', '강철영': 'Chulyoung Kang'}
TEAM_META = {'faculty': ('var(--navy)', '교수진', 'Faculty'), 'basic': ('var(--basic)', '기초팀 · Basic Lab', 'Basic Lab'),
             'hearing': ('var(--hearing)', '참조표준팀 · Hearing Lab', 'Hearing Lab'), 'head': ('var(--head)', '데이터팀 · HeAD Lab', 'HeAD Lab'),
             'admin': ('var(--ink-2)', '행정팀', 'Administration'), 'audiso': ('var(--audiso)', '오디에스오(주) · Audiso', 'Audiso')}


def role_en(s):
    return ' / '.join(ROLE_EN.get(x.strip(), x.strip()) for x in s.split('/')) if s else ''


def people():
    nav = '<nav class="team-nav">' + ''.join(f'<a href="#{tm["key"]}">{t(TEAM_META[tm["key"]][1].split(" · ")[0], TEAM_META[tm["key"]][2])}</a>' for tm in PEOPLE) + '</nav>'
    out = ''
    for tm in PEOPLE:
        c, ko, en = TEAM_META[tm['key']]
        cards = ''
        for m in tm['members']:
            nm = m['name']
            ph = (f'<img src="{m["photo"]}" alt="" width="150" height="165" loading="lazy">' if m['photo']
                  else f'<div class="ph" role="img" aria-label="{nm} 사진 준비 중">{nm[0]}</div>')
            rl_ko = ' · '.join(x for x in [m['role'], m['dept']] if x)
            rl_en = ' · '.join(x for x in [role_en(m['role']), role_en(m['dept'])] if x)
            name = t(nm, NAME_EN[nm]) if nm in NAME_EN else nm
            cards += f'<div class="member">{ph}<div class="nm">{name}</div><div class="rl">{t(rl_ko, rl_en)}</div></div>'
        out += (f'<section id="{tm["key"]}" style="scroll-margin-top:12px"><div class="wrap"><div class="team-h" style="--c:{c}"><span class="dot"></span>'
                f'<h2>{t(ko, en)}</h2></div><div class="members">{cards}</div></div></section>')
    return page('People', 'var(--navy)',
                hero(INST, 'People', t('함께 연구하는 사람들', 'The people of RIHE'),
                     t('연세대학교 원주세브란스기독병원 청각재활연구소(RIHE) 구성원을 소개합니다.', 'Meet the members of the Research Institute of Hearing Enhancement.'), nav)
                + out)


def lab(key, path, accent, name, team_ko, team_en, tagline, intro_ko, intro_en, extra, mission, manager, subjects, alumni, logo=None):
    pubs = [p for p in PUBS if p['team'] == key]
    subj = '<div class="cols c2">' + ''.join(f'<div><h3>{t(a, b)}</h3>{t(c_, d, "p")}</div>' for a, b, c_, d in subjects) + '</div>'
    mv = f'<div class="cols c{len(mission)}">' + ''.join(f'<div><h3>{h}</h3>{t(k, en_, "p")}</div>' for h, k, en_ in mission) + '</div>'
    people_ = director_block() + manager
    if alumni:
        alum = '<div class="members">'
        for nm, img, k, en_ in alumni:
            photo = f'<img src="{img}" alt="" loading="lazy">' if img else ''
            alum += f'<div class="member">{photo}<div class="nm">{nm}</div><div class="rl">{t(k, en_)}</div></div>'
        alum += '</div>'
    else:
        alum = t('아직 등록된 졸업생이 없습니다.', 'No alumni yet.', 'p', 'muted')
    title = f'<img class="logo" src="{logo}" alt="{name}">' if logo else name
    report_link = f'<p style="margin-top:28px">{more("/project", "학회 발표(Report) 목록은 Research 페이지에서 보기", "See conference reports on the Research page")}</p>'
    return page(name, accent,
                hero(INST + ' · RIHE', title, t(team_ko, team_en), tagline)
                + sec(t(f'{name} 소개', f'About {name}'), f'<div class="prose">{t(intro_ko, intro_en, "p")}</div>{extra}')
                + sec('Mission &amp; Vision', mv)
                + sec(t('조직', 'Organization'), org(key))
                + sec('Director &amp; Manager', people_)
                + sec('Research Subjects', subj)
                + sec('Publication', listing('pub', 'd-pubs') + report_link)
                + sec('Alumni', alum),
                {'d-pubs': pubs})


def manager(img, name_html, ko, en):
    return person(img, 'Manager', name_html, ko, en)


def basic_lab():
    return lab('basic', '/about-1', 'var(--basic)', 'Basic Lab', '기초팀', 'Basic research team',
               t('난청 치료의 근본을 탐구하는 기초연구', 'Basic research into the roots of hearing-loss treatment'),
               'Basic Lab은 청각재활연구소 산하 기초팀으로, 줄기세포, 나노입자, 약물 전달 등 난청의 기전에 대한 기초 연구를 수행합니다.',
               'Basic Lab is the basic research team of RIHE, studying the mechanisms of hearing loss through stem cells, nanoparticles and drug delivery.',
               '',
               [('Mission', '난청 치료를 위한 혁신적인 기초 연구 기반을 구축하고, 줄기세포 및 나노공학 기술을 활용한 새로운 치료 접근법을 개발합니다.',
                 'Build an innovative basic research foundation for treating hearing loss and develop new therapies using stem cells and nano-engineering.'),
                ('Vision', '기초과학의 성과를 임상에 적용하여, 난청 환자의 삶의 질 향상에 기여하는 세계적 수준의 연구실을 목표로 합니다.',
                 'A world-class lab that brings basic science into the clinic and improves the quality of life of people with hearing loss.')],
               manager('https://i.imgur.com/SkXdr8p.jpeg', '이은수', ['Basic Lab 팀장 · 연구교수'], ['Team Leader, Basic Lab · Research Professor']),
               [('줄기세포 호밍 및 나노입자 전달', 'Stem-cell homing and nanoparticle delivery', '자성 나노입자를 이용한 줄기세포의 내이 호밍 효율 향상 연구', 'Improving stem-cell homing to the inner ear with magnetic nanoparticles'),
                ('Exosome 기반 치료제 연구', 'Exosome-based therapeutics', '엑소좀을 활용한 내이 세포 보호 및 재생 치료제 개발', 'Exosome therapies that protect and regenerate inner-ear cells'),
                ('약물 독성 및 보호 메커니즘 연구', 'Ototoxicity and protection', '이독성 약물에 의한 내이 손상 기전 규명 및 보호 전략 연구', 'How ototoxic drugs damage the inner ear, and how to protect it'),
                ('내이 세포 재생 연구', 'Inner-ear cell regeneration', '유모세포 및 신경세포 재생을 위한 분자생물학적 접근', 'Molecular approaches to regenerating hair cells and neurons')],
               [])


def hearing_lab():
    items_ko = ['한국인 연령별/성별 청각 참조데이터 수집 및 생산 (국내 유일)', '한국인 청각 참조데이터 평가를 통한 참조데이터 자체 등급부여',
                '한국인 청각 참조데이터 등급부여 요청 및 참조표준 등록 요청', '국제공동연구를 통한 청각 데이터 생산 및 대규모 연구',
                '국제협력을 통한 국제 청각 데이터베이스 네트워크 구축', '이어폰/보청기 산업 및 의료기기 개발 데이터 제공',
                '난청 보건 사업 데이터 제공', '청각 관련 앱 개발 데이터 제공']
    items_en = ['Collecting and producing Korean reference hearing data by age and sex (the only one in Korea)', 'Grading reference data through our own evaluation',
                'Requesting grading and registration as national reference standards', 'Producing hearing data and large-scale studies through international collaboration',
                'Building an international hearing database network', 'Data for the earphone, hearing-aid and medical-device industries',
                'Data for public hearing-health programmes', 'Data for hearing-related app development']
    dc = f"""<div class="box tint" style="margin-top:28px"><img class="logo" src="{DC_REF_LOGO}" alt="한국인 청각 참조표준데이터센터 Korea Hearing Standard-data Center" loading="lazy">
<h3>{t('한국인 청각 참조표준데이터센터 (2019년 1월~)', 'Data center for Korean reference hearing (since January 2019)')}</h3>
<div class="prose" style="margin-top:10px">{t('한국인의 특성을 충분히 반영하지 못하는 기존 외국 기준 대신 한국인 청각 참조표준을 적용하면 진단과 검사의 정확도가 높아져 한국인 환자에게 더 나은 의료서비스를 제공할 수 있습니다. 한국인 청각 참조표준은 난청 보건 사업, 이어폰·보청기 등 의료기기, 청각 연구, skull simulator, 청각 치료 및 재활, 앱 개발 등에 적용될 예정입니다.',
    'Foreign standards do not fully reflect Korean characteristics. Applying Korean reference hearing standards makes diagnosis and testing more accurate and gives Korean patients better care. They will be applied to public hearing-health programmes, earphones, hearing aids and other devices, hearing research, skull simulators, treatment and rehabilitation, and app development.', 'p')}</div>
<ul class="bullets" data-l="ko">{''.join(f'<li>{x}</li>' for x in items_ko)}</ul><ul class="bullets" data-l="en" lang="en">{''.join(f'<li>{x}</li>' for x in items_en)}</ul></div>"""
    return lab('hearing', '/hearing-lab', 'var(--hearing)', 'Hearing Lab', '참조표준팀', 'Reference standard team',
               t('한국인 청각의 표준을 만들어가는 연구', 'Setting the standard for Korean hearing'),
               'Hearing Lab은 청각재활연구소 산하 참조표준팀으로, 한국인 청각 참조표준 데이터를 수집·생산하고 청각 연구를 수행합니다. 한국인의 특성을 반영한 청각 참조표준을 확립하여 더 정확한 청력 진단과 더 나은 의료서비스 제공을 목표로 합니다.',
               'Hearing Lab is the reference standard team of RIHE. We collect and produce Korean reference hearing data and aim for more accurate diagnosis and better care through standards that reflect Korean characteristics.',
               dc,
               [('Mission', '한국인 청각 참조데이터의 수집, 평가, 등급부여를 통해 국내 유일의 청각 참조표준 데이터센터를 운영하고 국제 네트워크를 구축합니다.',
                 'Run Korea’s only reference standard data center for hearing by collecting, evaluating and grading Korean hearing data, and build an international network.'),
                ('Vision', '한국인에게 최적화된 청각 참조표준을 확립하여 글로벌 청각 연구의 거점이 되고, 국민 청각 건강 증진에 기여합니다.',
                 'Establish hearing standards optimised for Koreans, become a hub of global hearing research and improve the nation’s hearing health.')],
               manager('https://i.imgur.com/2Q56Mj7.jpeg', t('변유선', 'Yuseon Byun'), ['Hearing Lab · 박사과정'], ['Hearing Lab · Ph.D. Student']),
               [('한국인 청각 참조표준 데이터 수집', 'Korean reference hearing data', '연령별·성별 한국인 청각 데이터의 체계적 수집 및 품질 관리', 'Systematic collection and quality control of Korean hearing data by age and sex'),
                ('청력검사 표준화 연구', 'Standardising hearing tests', '국제 표준에 부합하는 청력검사 절차 및 기준 수립', 'Hearing-test procedures and criteria that meet international standards'),
                ('보청기·이어폰 산업 데이터 제공', 'Data for industry', '청각 산업 및 의료기기 개발을 위한 표준 데이터 제공', 'Standard data for the hearing industry and medical-device development'),
                ('국제 청각 데이터베이스 네트워크', 'International hearing database network', '글로벌 청각 연구 기관과의 데이터 공유 및 공동 연구', 'Data sharing and joint research with hearing institutes worldwide')],
               [('이지현', '', '박사 · 2022년 졸업', 'Ph.D. · 2022'), ('류성화', '', '박사 · 2026년 졸업', 'Ph.D. · 2026')])


def head_lab():
    items_ko = ['CDM, NHANES, UK Biobank 등 국내외 의료 빅데이터 활용 연구', '순음청력검사(PTA) 및 청성뇌간반응검사(ABR) 데이터 표준화',
                '건강보험공단 청력데이터 연동 추출', '청각 빅데이터 기반 AI 모델 개발 및 데이터 서비스', '산업체·연구자 대상 데이터 제공 및 기술 컨설팅']
    items_en = ['Research using medical big data at home and abroad (CDM, NHANES, UK Biobank)', 'Standardising pure-tone audiometry (PTA) and auditory brainstem response (ABR) data',
                'Linked extraction of hearing data from the National Health Insurance Service', 'AI models and data services built on hearing big data', 'Data provision and technical consulting for industry and researchers']
    dc = f"""<div class="box tint" style="margin-top:28px"><img class="logo" src="{DC_BIG_LOGO}" alt="청각 빅데이터센터 Korea Hearing Big-data Center" loading="lazy">
<h3>{t('청각 빅데이터센터 운영', 'Korea Hearing Big-data Center')}</h3>
<div class="prose" style="margin-top:10px">{t('산업계와 연구자에게 청각 분야의 빅데이터를 전문으로 제공하는 국내 유일 기관입니다. 10만 건 이상의 순음청력검사와 청성뇌간반응검사 데이터를 기반으로 라이프로그 데이터, 참조표준데이터, 보건의료빅데이터와 연계된 종합적인 청각빅데이터 제공을 목표로 합니다.',
    'Korea’s only provider of hearing big data for industry and researchers. Built on over 100,000 pure-tone audiometry and auditory brainstem response records, we aim to provide comprehensive hearing big data linked with lifelog, reference-standard and health big data.', 'p')}</div>
<ul class="bullets" data-l="ko">{''.join(f'<li>{x}</li>' for x in items_ko)}</ul><ul class="bullets" data-l="en" lang="en">{''.join(f'<li>{x}</li>' for x in items_en)}</ul></div>"""
    return lab('head', '/head-lab', 'var(--head)', 'HeAD Lab', '데이터팀 · RIHE Hearing AI &amp; Data Lab', 'Data team · RIHE Hearing AI &amp; Data Lab',
               t('데이터로 소리를 이해하고, AI로 미래를 예측하다', 'Understanding sound with data, predicting the future with AI'),
               'HeAD Lab은 청각 데이터와 인공지능 기술을 융합하여 난청 예측, 청력 건강 관리, 청각재활 분야의 솔루션을 개발합니다. 데이터 과학과 AI 기술로 청력 손실의 조기 발견부터 개인 맞춤형 청각재활까지 청각 건강 관리의 전 주기를 아우르는 연구를 수행합니다.',
               'HeAD Lab combines hearing data and AI to build solutions for predicting hearing loss, managing hearing health and hearing rehabilitation, covering the full cycle from early detection to personalised rehabilitation.',
               dc,
               [('Mission', '청각 건강 데이터의 표준화와 인공지능 기술 융합을 통해 난청 예방, 조기 진단 및 효과적인 재활을 위한 혁신적 솔루션을 개발하여 전 세계인의 청력 건강 증진에 기여합니다.',
                 'Standardise hearing-health data and combine it with AI to develop solutions for prevention, early diagnosis and effective rehabilitation of hearing loss worldwide.'),
                ('Vision', '빅데이터와 AI 기술을 활용한 청각 건강 관리의 글로벌 리더로서, 국제 표준을 선도하고 누구나 쉽게 접근할 수 있는 디지털 청각 건강 생태계를 구축합니다.',
                 'Lead hearing-health care with big data and AI, set international standards and build a digital hearing-health ecosystem open to everyone.'),
                ('Core Values', '혁신성 · 정확성 · 협력', 'Innovation · Precision · Collaboration')],
               manager('https://i.imgur.com/RC37iFm.jpeg', t('윤철영 팀장', 'Chul Young Yoon'), ['HeAD Lab 연구팀장', '연세대학교 의료정보통계학과'], ['Team Leader, HeAD Lab', 'Department of Medical Informatics and Biostatistics, Yonsei University']),
               [('Future Hearing Prediction', 'Future Hearing Prediction', '정상 청력자의 장기 데이터를 활용한 미래 청력 예측 AI 모델 개발', 'AI models that predict future hearing from long-term data of people with normal hearing'),
                ('Ototoxicity &amp; Drugs', 'Ototoxicity &amp; Drugs', '이독성 약물 데이터 분석 및 난청 발생 위험도 평가', 'Analysing ototoxic-drug data and the risk of hearing loss'),
                ('Eardrum Imaging', 'Eardrum Imaging', '고막 내시경 영상 기반 AI 분류 및 온디바이스 적용', 'AI classification of eardrum endoscopy images, on device'),
                ('Noise Map', 'Noise Map', '환경 소음과 건강 데이터를 융합한 소음지도 제작', 'Noise maps combining environmental noise and health data'),
                ('International Cohorts', 'International Cohorts', 'UK Biobank 및 NHIS/KNHANES 연계 연구', 'Research linking UK Biobank and NHIS/KNHANES'),
                ('Ear Age', 'Ear Age', '청력 기반 생물학적 나이 추정 및 청각 노화 연구', 'Estimating biological age from hearing, and ear ageing')],
               [('김지원', 'https://i.imgur.com/TWCotbS.jpeg', '의료정보통계학과 석사 · 2025년 2월 졸업', 'M.S. · Feb 2025'),
                ('이준헌', 'https://i.imgur.com/gQo7vUz.jpeg', '의료정보통계학과 석사 · 2026년 2월 졸업', 'M.S. · Feb 2026'),
                ('이주형', 'https://i.imgur.com/jXCJxED.jpeg', '의료정보통계학 석사 · 2023년 2월 졸업', 'M.S. · Feb 2023')],
               logo='https://i.imgur.com/QV0SgF2.png')


def audiso():
    strengths = [('현직 이비인후과 전문의', 'Practising ENT specialist', '원주세브란스기독병원 이비인후과 교수로 활동하며, 진료와 수술에서 얻은 청각 관련 최신 데이터를 활용해 최적의 서비스를 제공합니다.', 'Led by an ENT professor at Wonju Severance Christian Hospital, using the latest hearing data from clinical practice and surgery.'),
                 ('KOLAS 국제공인교정기관', 'KOLAS-accredited', '청각 관련 국내 최초 청력계 기골도 분야 KOLAS 국제공인교정기관으로 인정받았습니다.', 'Korea’s first KOLAS-accredited calibration body for audiometer air and bone conduction.'),
                 ('청각 분야 전문가', 'Hearing specialists', '소속 직원 모두 청각학 전공자로, 청각에 대한 전문 지식을 활용해 높은 수준의 서비스를 제공합니다.', 'All staff majored in audiology.'),
                 ('출장 교정 서비스', 'On-site calibration', '전국 모두 직접 방문이 가능하며, 어디에서나 편리하게 출장 교정 서비스를 받을 수 있습니다.', 'We visit sites anywhere in Korea.'),
                 ('일정 맞춤 서비스', 'Flexible scheduling', '고객 일정에 맞추어 원하는 날짜로 진행할 수 있도록 예약신청 시스템을 제공합니다.', 'Book the date that suits you through our reservation system.'),
                 ('교육 서비스 제공', 'Training', '교정 외에 환경, 검사자 등 청각 검사기기를 제외한 요소에 대한 교육 서비스를 제공합니다.', 'Training on test environments and examiners, beyond the devices themselves.')]
    products = [('uTtErq7.jpeg', 'WithHear, 난청 선별진단기기', 'WithHear hearing screening device', '난청의 조기 진단을 위한 청각검사, AI 고막 검사 기능을 탑재한 선별 진단 기기 개발 및 보급', 'A screening device with hearing tests and AI eardrum examination for early diagnosis of hearing loss.'),
                ('6Hgxcfl.jpeg', '의료 가상현실 시뮬레이터', 'Medical VR simulators', '청력검사, 이석증 진단치료, 측두골 임플란트 삽입 수술 등 임상실습 주제를 디지털트윈 및 리얼타임 렌더링 VR 시뮬레이션으로 개발', 'Digital-twin, real-time VR simulations for clinical training: hearing tests, BPPV diagnosis and treatment, temporal-bone implant surgery.'),
                ('KsgzHqL.jpeg', '어지럼증 디지털 치료제', 'Digital therapeutic for dizziness', '어지럼증을 치료하고 자세 균형을 회복할 수 있도록 재활운동을 제공하는 가상현실 기반의 맞춤 전정재활 훈련용 소프트웨어 개발', 'VR-based, personalised vestibular rehabilitation software for treating dizziness and restoring balance.'),
                ('lcbkdkk.jpeg', '모두의 보청기', 'Hearing aids for everyone (app)', '보청기 정보, 전문 병원 및 보청기 센터 위치기반 서비스, 난청 챗봇 상담 기능을 탑재한 애플리케이션 개발', 'An app with hearing-aid information, location-based clinic and centre search, and a hearing-loss chatbot.'),
                ('Ltm00mT.jpeg', '의사가 알려주는 디지털 치료제', 'Digital Therapeutics (book)', '디지털 치료기기의 개념부터 활용 사례, 의료법과 개인정보 보호까지 다룬 DTx 전문 서적 발간', 'A book on digital therapeutics, from concepts and cases to medical law and privacy.'),
                ('dYhZ1vM.jpeg', '피스탑 트리플케어', 'Peace Stop Triple Care', '소리에 민감한 귀 및 감각기관의 균형 관리를 위한 영양소를 공급해 주는 건강 기능 식품 개발', 'A health functional food supplying nutrients for ears sensitive to sound and the balance of the sensory organs.')]
    st_html = '<div class="cols c3">' + ''.join(f'<div><h3>{t(a, b)}</h3>{t(c_, d, "p")}</div>' for a, b, c_, d in strengths) + '</div>'
    pr_html = '<div class="cols c3 fig">' + ''.join(
        f'<div><img src="https://i.imgur.com/{im}" alt="" loading="lazy" width="400" height="300"><h3>{t(a, b)}</h3>{t(c_, d, "p")}</div>' for im, a, b, c_, d in products) + '</div>'
    kolas = f"""<div class="box" style="margin-top:28px;display:flex;gap:20px;align-items:center;flex-wrap:wrap"><img src="https://i.imgur.com/Ycn67aA.png" alt="KOLAS KC24-437" loading="lazy" style="width:96px;height:auto">
<div style="flex:1;min-width:200px"><h3>{t('KOLAS 국제공인교정기관 인정 (KC24-437)', 'KOLAS accredited calibration body (KC24-437)')}</h3>{t('ISO 국제 표준에 기반한 정확한 청력계 교정 서비스를 제공합니다.', 'Accurate audiometer calibration based on ISO international standards.', 'p', 'muted')}</div></div>"""
    intro_ko = ['(주)오디에스오는 국내 유일 국가인정 청력계 교정기관으로서, 보다 정확한 난청 진단 및 치료의 발전에 기여하고자 설립되었습니다.',
                '대한민국 참조표준데이터센터인 한국인 청각 데이터센터에서 시작하여, 2018년부터 한국인의 정상 청력을 측정하기 위한 기기 교정, 표준검사 지침, 환경 교정 등의 표준절차를 바탕으로 국내 어디서나 인증된 청력검사를 받을 수 있도록 힘쓰고 있습니다.',
                '검사자와 환경에 대한 교육으로 교정 이후에도 지속적인 관리를 지원하며, VR 시뮬레이션과 AI 기술 등 청각 관련 사업과의 협력을 통해 교정받는 기관과 함께 성장하는 파트너가 되겠습니다.']
    intro_en = ['Audiso is Korea’s only nationally accredited audiometer calibration body, founded to advance more accurate diagnosis and treatment of hearing loss.',
                'Starting from the Korean hearing reference data center, since 2018 we have built standard procedures for device calibration, standard test guidelines and environment calibration so that certified hearing tests are available anywhere in Korea.',
                'We support examiners and test environments after calibration through training, and work with VR simulation and AI partners to grow together with the institutions we serve.']
    return page('Audiso', 'var(--audiso)',
                hero('Audiology with ISO', '<img class="logo" src="https://i.imgur.com/lQwB2st.jpeg" alt="Audiso 오디에스오">',
                     t('오디에스오(주) · 청각재활연구소 교원창업 기업', 'Audiso Co., Ltd. · faculty start-up of RIHE'),
                     t('청력계 KOLAS 인정 교정기관 · 청각 솔루션 전문기업', 'KOLAS-accredited audiometer calibration · hearing solutions'),
                     '<p class="cta"><a class="btn" href="https://audiso.co.kr/" target="_blank" rel="noopener">audiso.co.kr ↗</a>'
                     '<a class="btn ghost" href="https://xr.audiso.co.kr/" target="_blank" rel="noopener">xr.audiso.co.kr ↗</a></p>')
                + sec(t('Audiso 소개', 'About Audiso'), '<div class="prose">' + ''.join(t(a, b, 'p') for a, b in zip(intro_ko, intro_en)) + '</div>' + kolas)
                + sec(t('오디에스오의 강점', 'Why Audiso'), st_html)
                + sec('Mission &amp; Vision', '<div class="cols c2">'
                      + f'<div><h3>Mission</h3>{t("국내 유일 국가인정 청력계 교정기관으로서, 표준화된 청력검사 환경 구축과 청각 솔루션 상용화를 통해 국민 청각 건강 증진에 기여합니다.", "As Korea’s only accredited audiometer calibration body, improve national hearing health through standardised test environments and commercial hearing solutions.", "p")}</div>'
                      + f'<div><h3>Vision</h3>{t("KOLAS 국제공인교정 기반의 정확한 청각 서비스와 혁신적 디지털 헬스케어 솔루션으로, 청각 분야의 글로벌 파트너로 성장합니다.", "Grow into a global partner in hearing with accurate KOLAS-based services and digital healthcare solutions.", "p")}</div></div>')
                + sec(t('조직', 'Organization'), org('audiso'))
                + sec('Products', pr_html))


def contact():
    teams = [('basic', '기초팀', 'Basic Lab', '이은수', 'es1121@yonsei.ac.kr'),
             ('hearing', '참조표준팀', 'Hearing Lab', '변유선', 'uuuseon@yonsei.ac.kr'),
             ('head', '데이터팀', 'HeAD Lab', '윤철영', 'fezro@yonsei.ac.kr')]
    info = f"""<div class="split" style="align-items:start"><dl class="kv">
<dt>{t('주소', 'Address')}</dt><dd>{t('강원특별자치도 원주시 일산로 20<br>연세대학교 원주세브란스기독병원 의학관 318호 (26426)', 'Room 318, Medical Science Building, Wonju Severance Christian Hospital, Yonsei University<br>20 Ilsan-ro, Wonju, Gangwon-do 26426, Korea')}</dd>
<dt>{t('이메일', 'Email')}</dt><dd><a class="mail" style="margin:0" href="mailto:okas2000@yonsei.ac.kr">okas2000@yonsei.ac.kr</a><br><span class="muted" style="font-size:14px">{t('서영준 연구소장', 'Director Young Joon Seo')}</span></dd>
<dt>{t('소속', 'Affiliation')}</dt><dd>{t('연세대학교 원주의과대학 · 원주세브란스기독병원 이비인후과 · 청각재활연구소', 'Yonsei University Wonju College of Medicine · Department of Otorhinolaryngology, Wonju Severance Christian Hospital · RIHE')}</dd>
</dl><iframe class="map" title="{e('원주세브란스기독병원 지도')}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
src="https://www.google.com/maps?q=%EC%9B%90%EC%A3%BC%EC%84%B8%EB%B8%8C%EB%9E%80%EC%8A%A4%EA%B8%B0%EB%8F%85%EB%B3%91%EC%9B%90&amp;z=15&amp;output=embed"></iframe></div>"""
    rows = '<ul class="rows">' + ''.join(
        f'<li><a href="mailto:{m}" style="--c:var(--{k})"><span class="name">{en}<span class="sub" data-l="ko">{ko}</span></span>'
        f'<span class="desc">{t("담당자 " + p, NAME_EN.get(p, p))} · {m}</span><span class="go" aria-hidden="true">✉</span></a></li>'
        for k, ko, en, p, m in teams) + '</ul>'
    return page('Contact', 'var(--navy)',
                hero(INST, 'Contact', t('청각재활연구소에 문의하기', 'Get in touch'), t('연세대학교 원주세브란스기독병원 청각재활연구소 (RIHE)', 'Research Institute of Hearing Enhancement, Wonju Severance Christian Hospital, Yonsei University'))
                + sec(t('연구소 안내', 'Visit us'), info)
                + sec(t('팀별 연락처', 'Team contacts'), rows))


PAGES = {'home': home, 'about': about, 'research': research, 'people': people, 'basic-lab': basic_lab,
         'hearing-lab': hearing_lab, 'head-lab': head_lab, 'audiso': audiso, 'contact': contact}


def main():
    out_dir = os.path.join(ROOT, 'site-preview' if PREVIEW else 'site')
    os.makedirs(out_dir, exist_ok=True)
    for name, fn in PAGES.items():
        with open(os.path.join(out_dir, name + '.html'), 'w', encoding='utf-8') as f:
            f.write(fn())
        print(out_dir.split('/')[-1] + '/' + name + '.html')


if __name__ == '__main__':
    main()
