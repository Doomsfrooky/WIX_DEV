# RIHE design kit, stage 2 (direction C2): developer guide

This guide is for anyone writing a page in `tools/pages/<name>.py`. It is complete on purpose: **you build a page from
this guide alone and you do not edit `tools/kit.py`** (other agents build pages in parallel from the same kit). If a
component you need is missing or wrong, do not add page-local CSS or patch the kit: finish with what exists and report
the request (where, what, why) to the coordinator.

- The design itself (tokens, type, grid, motion, why): `DESIGN.md` at the repo root.
- The reference page: `tools/pages/home.py` (Home).
- Working examples of **every** component: `python3 tools/kit_demo.py` writes `site-preview/_kit.html` (photo hero and
  every section component), `_kit-lists.html` (tint hero with the record, a chapter, the three lists, the gallery) and
  `_kit-lab.html` (`kit.lab_page()` for HeAD Lab). Read `tools/kit_demo.py` next to this guide.
- Round 2 for reference only (not built): `tools/kit_v2.py`, `tools/pages_v2/*.py`, `tools/KIT_v2.md`. The copy in
  `tools/pages_v2/*.py` is the copy you port (it came from `tools/build_v1.py`).

## 1. Files and build

```
tools/core.py           design-free runtime: copy, data, t()/tt(), link()/ext(), img()/wix()/imgur(), RIHE.* (language,
                        safe reveals, the sentinel band, the list engine), page_shell()
tools/kit.py            the C2 design system: tokens, CSS, motion and list scripts, components, page()
tools/kit_assets/       the Home hero: hero.html, hero.css, hero.js, reel.json (the promo's byte ranges), reel.py, fonts.txt
tools/pages/<name>.py   one page: render() -> HTML via kit.page(...)
tools/build.py          python3 tools/build.py [--preview] [--only home,research]
site/<name>.html        production (Wix "website address" element; no language toggle)
site-preview/<name>.html  the same with a small KO/EN toggle (and site-preview/vendor/, copied by --preview)
```

Page names and paths (`kit.PATHS`): home `/`, about `/about`, research `/project`, people `/people`, basic-lab
`/about-1`, hearing-lab `/hearing-lab`, head-lab `/head-lab`, audiso `/audiso`, contact `/연락처`, gallery `/gallery`.
`build.py` builds only the modules that exist in `tools/pages/`.

**build.py fails the build** on: an em-dash (—) in visible copy; a `data-l="en"` element without `lang="en"`; a
`<script src>` that is not a relative `vendor/` path; a missing robots meta; any `vh`/`svh`/`dvh`/`lvh` unit or
`innerHeight` anywhere in the page.

The smallest page:

```python
"""Contact (/연락처)."""
import kit
from kit import t, sec


def render():
    hero = kit.page_hero(('연락처', 'Contact'), alt=('청각재활연구소에 문의하기', 'Get in touch'),
                         image=kit.gallery_photo('21.png', '50% 62%', '42% 50%', crop=(96, 2, 1295, 524)))
    body = (hero + '<main>'
            + sec(('연구소 안내', 'Visit us'), kit.kv([(('주소', 'Address'), t('...', '...'))]), 'visit')
            + '</main>')
    return kit.page('Contact', body)
```

Always: one `page_hero(...)` (or `home_hero()` on Home) first, then `<main>`, the sections, `</main>`.

## 2. Copy, data, languages, links

- **Copy stays as it is.** Port it from `tools/pages_v2/<page>.py` (round 2, which took it from `tools/build_v1.py`).
  Shared copy is in `core` (all re-exported by `kit`): `INST, NAME, MISSION, AREAS, LABS, LAB, DIRECTOR, DATA_CENTERS,
  NAME_EN, ROLE_EN, TEAM_META, TEAM_LABEL, UI, TECH_TRANSFERS, HOME_LEAD, SINCE, OUTCOMES, RESEARCH_TITLE,
  RESEARCH_LEAD, PEOPLE_TITLE, PEOPLE_LEAD`. Never invent facts, names, numbers, awards or copy. Author lists stay
  exactly as published.
- **Data is read at build time**: `kit.PUBS, kit.REPORTS, kit.PATENTS, kit.PEOPLE, kit.TEAMS[key], kit.GALLERY,
  kit.VIDEOS`. Never hard-code a count: `len(kit.PUBS)`. The client is sending new reports and People updates; the
  coordinator merges them into `data/*.json` and the pages must follow without edits.
- **Every visible string is a KO/EN pair.** `t('연구실', 'Labs')` -> `<span data-l="ko">연구실</span><span data-l="en"
  lang="en">Labs</span>`; `t(ko, en, 'p')` for a block; `tt(pair)` for a tuple; `t(text)` is language-neutral. Most kit
  components take `(ko, en)` tuples directly. A plain Latin string (a lab name, 'Audiso') is accepted where a heading or
  title is expected and is marked `lang="en"` by the kit.
- The language comes from `?lang=en|ko` (applied before first paint: no Korean flash on English) or Wix page code
  `postMessage({lang})`. `RIHE.lang`, `RIHE.onLang(fn)`.
- **One height for both languages.** The kit reserves, block by block, the taller of the two languages (`data-lk`), so
  the page height is the same in KO and EN and the Wix element needs one height. You get this for free in every
  `sec()`, `list_sec()`, `chapter()`, `page_hero()`; the heading column of every section is locked too, so a body never
  moves when the language changes. Inside a block, parts still follow their own text (the hero's lines under a title of
  another length, a second `feature()` under a longer first one). The measurement lays the page out in the other
  language synchronously (`data-lang` and `lang` together, never painted) and loads that language's font glyphs first,
  so a face only the hidden language uses is measured as itself. Do not fight it with fixed heights.
- Image alt is a pair: `kit.img(src, ('대체 텍스트', 'Alt text'), w, h)`. aria-label pairs: `aria-label="..." data-aria-en="..."`.
- **Links between pages**: `kit.link(page, inner)` or `kit.more(page, ko, en)` (both `target="_top"` with `data-path`).
  Use page names from `kit.PATHS` or a site path (`'/project#report'`). External: `kit.ext(url, inner)`,
  `kit.more(url, ko, en, external=True)`, `kit.btn(url, label)`. Wix Multilingual is off: `/en/...` 404s today
  (`core.EN_PREFIX`; the coordinator decides).
- In-page anchors used across pages: Research `#publication`, `#report`, `#patents` (the lab pages link to
  `/project#report`); People team sections use the people.json keys (`#faculty`, `#basic`, ...). A jump inside a page
  lands 24 px below the top (152 px at 320, under Wix mobile's sticky 140 px header: `section[id]` has scroll-margin).
  **A link from another page lands at the top of the target page**: the Wix page's #fragment never reaches the
  cross-origin iframe. Forwarding it needs Wix page code (a proposal in DESIGN.md "Finish", awaiting the client).
- Lab names (Basic Lab, Hearing Lab, HeAD Lab, Audiso) stay in Latin in both languages.
- No em-dash in visible copy (comma, colon or ` · `).

## 3. Tokens, tones, type, grid (details and reasons: DESIGN.md)

| token | value | use |
|---|---|---|
| `--paper` | #ffffff | the one sheet (the Wix chrome is #ffffff too); the knockout's white |
| `--ink` / `--ink-2` / `--ink-3` | #0f0e0c / #4e4b47 / #696660 | text: 19.3 / 8.7 / 5.7 : 1 on white |
| `--ink-r` / `--ink-r2` | rgba(15,14,12,.12) / .28 | row hairlines, frame edges / column rules, buttons |
| `--tint` | #f1f1ef | an empty frame before its picture |
| `--umber` | #8a5a0e | the only text accent: arrows, the pressed-filter bar, the reel's current page, focus rings, small marks (5.9:1) |
| `--amber` | #e3a640 | the text selection only, never text |

**Lab tones** (`kit.TONES`): a pastel tint for surfaces (`--t-<key>`) and a deep tone for text and lines
(`--d-<key>`), AA on white and on the tint. Keys: `inst` (the institute: faculty and the non-lab pages), `basic`,
`hearing`, `head`, `audiso` (deep = umber, the logo's gold), `collab`, `admin`. `kit.TEAM_TONE` maps people.json and
publication team keys to tones. Components take `tone='basic'` (or set it for you); `kit.tone_style(key)` gives the
inline style if you ever need it. Where tones appear: the tab on a section's cut line (`sec(..., tone=)`), lab rows,
the org chart's current unit, the data-center panel, initial tiles, the jump-link and publication-team marks, a page
hero without a photograph (the tint field and the knockout in the deep tone), `box(tone=)`.

**Type.** Display: Black Han Sans (Korean) and Archivo condensed 62% weight 860 (Latin, caps in titles). Reading:
Noto Sans KR 400/500 (Korean) and Archivo (Latin). Numbers: Archivo condensed 640. Weights are 400 · 500 · 640 · 860
only. Reading sizes are C2's scale, **11 · 12 · 13.5 · 15 · 16.5 · 18 px** (Korean reading text sits .5 px above its
English twin at one step: 16.5 / 16, 15.5 / 15, 15 / 14.5); display sizes are clamps of their own. The kit requests
only the glyphs a page uses (Google Fonts `text=`); anything in the display face must be inside one of
`kit.DK_CLASSES` (all kit display elements are; a `box()` h3 is marked for you), so do not set Black Han Sans on your
own markup without `k-dk`. A live CMS gallery switches Noto Sans KR to the full unicode-range set automatically.

**Grid.** One axis: the left column ends one gutter before 34% of the width (the Home frame's left edge), the body
column starts on it. `W = min(100vw, 1640px)`, margin `clamp(28px, 3.75vw, 72px)` (16 px at 320), gutter
`clamp(20px, 2.4vw, 40px)`. Sections are `clamp(64px, 6.6vw, 112px)` apart (56 at 320). Corners are square. 320: one
column. Mobile breakpoint `max-width: 760px`; the same file serves Wix desktop (980-1920) and Wix mobile (320).

## 4. Components (all return HTML strings; `kit.` prefix omitted)

### Document and heroes

**`page(title, body, tone='inst', comment='', full_ko=None)`** — the whole document: fonts (subsets), the kit's CSS
(+ the Home hero's CSS when `home_hero()` is in the body), the runtime, GSAP 3.15 from `vendor/`, the kit's scripts.
`title` is plain text (' · RIHE' is added). `tone`: the page's lab tone (bullets, initial tiles and marks without their
own tone). `comment`: a Korean note in the head comment. Robots is `noindex, indexifembedded`.
`return kit.page('Hearing Lab', body, tone='hearing')`

**`home_hero()`** — Home only: the C2 hero (reel frame, knockout title, the record = `core.OUTCOMES` on counter wheels,
the lead, the link to the lists). Desktop: the frame's left edge cuts the title; 320: the photograph spans the width
and its bottom edge crosses the title's first line. The record counts data/*.json at build time.

**`page_hero(title, alt='', lead='', *, image=None, tone='inst', logo=None, inst=INST, extra='', cls='')`** — every
other page. A frame on the sheet from the 34% axis to the right margin, opened from an ink cut line (drawn, held for a
beat, split). The title stands at the frame's left edge and the frame's **bottom edge crosses its first line**: over a
photograph the part inside the frame is paper white (knockout), over a tint it is the tone's deep colour; below the
edge it is ink. It is sized to fit the frame (Korean up to 132 px, 54 px at 320; Latin titles are set in caps). 320:
the frame spans the width.
- `title`: `(ko, en)` or a Latin string (`'Basic Lab'`). `alt`: a subtitle line, `lead`: a paragraph; both `(ko, en)`
  or html. `inst`: the small line in the left column (default `kit.INST_LINE`, the hospital and university, whose
  English line breaks only after 'Yonsei University ·'; Audiso passes its own).
- Three kinds: **photo** `image=kit.gallery_photo(i, pos='50% 40%', pos_m=None)` (or a dict `src, w, h,
  alt=(ko, en), pos, pos_m, srcset`); **tint** (no image): the `tone` field, low, with the knockout in the deep tone;
  **logo** `logo=(src, w, h)`: the lab's logo inside the tint field instead of a visible title (the h1 stays as
  screen-reader text), used for HeAD Lab and Audiso. The logo is 40% of the frame's height (72-120 px), multiplied into
  the tint, through an alpha curve (`#k-flat`, alpha cubed) that fades a soft shadow baked into a transparent PNG
  (HeAD Lab's) and leaves a logo on a white ground (Audiso's JPEG) as it is. A flat logo file is still better.
- `extra`: html under the lead: `jump_nav(...)`, `record(...)`, `<p class="k-btns">` + `btn(...)`.
- `gallery_photo(key, pos='50% 40%', pos_m=None, crop=None)` picks a `data/gallery.json` entry by a stable key (part
  of its file name): `'IMG_0168'` members (960x640), `'IMG_6300'` ORL-HNS 2018 congress, `'IMG_8510'` award ceremony,
  `'IMG_8219'` KIMES 2019, `'IMG_7721'` the data center plaque, `'21.png'` the hospital campus (1391x660). An index
  works too, but new photos are added at the front, so indexes move. `pos` is the CSS object-position on the wide
  desktop frame (about 2.8:1), `pos_m` at 320 (about 1.6:1). `crop=(x, y, w, h)` (original pixels, Wix entries only)
  uses only that part of the photo: **`'21.png'` is a banner**, a CG rendering on a transparent strip (x < 95) above a
  band with the Yonsei logo and the institute's name (y > 528), so Contact passes `crop=(96, 2, 1295, 524)`.
- Examples:
  `page_hero(('연구소 소개', 'About RIHE'), alt=..., lead=..., image=kit.gallery_photo('IMG_0168', '50% 32%'))`
  `page_hero(('연구', 'Research'), alt=kit.RESEARCH_TITLE, lead=kit.RESEARCH_LEAD, extra=kit.record(...))`
  `page_hero('Audiso', alt=..., lead=..., logo=(kit.imgur('https://i.imgur.com/lQwB2st.jpeg', 'l'), 1858, 542), tone='audiso', inst='Audiology with ISO', extra='<p class="k-btns">' + kit.btn('https://audiso.co.kr/', 'audiso.co.kr') + kit.btn('https://xr.audiso.co.kr/', 'xr.audiso.co.kr') + '</p>')`

### Sections and text

**`sec(h, body, sid, note='', aside='', cls='', wide=False, tone=None, link_html='', level=2, lk=True)`** — the
standard section: an ink cut line across the grid (drawn in), the heading column (h2 in the display face, `note` in
small grey, `aside` html under it, e.g. a `more()` link) and the body column. `sid` is required (section id; the
heading gets `<sid>-h`). `tone`: a short tab in the lab's deep tone on the cut line (lab pages, People teams).
`wide=True` (or **`sec_wide(h, body, sid, note='', link_html='', cls='', tone=None)`**): the heading row with
`link_html` at its right and the body across both columns (gallery). A body without reveal blocks of its own appears
as one block. `level=3` under a `chapter()`. The section and its heading column each reserve the taller language
(`lk=False` turns both off).
`sec(('연구 분야', 'Research areas'), kit.areas(), 'research')`

**`chapter(ko, en, sid, lead_pair=None, one_line=False)`** — C2's big display heading across both columns in authored
lines (strings or lists of lines; lines never wrap), KO = EN height; optional lead in the body column. Use it to open
a big part of a page. `kit.chapter(['청각재활연구소의', '연구 성과'], ['Research output', 'of the Institute'], 'output', kit.RESEARCH_LEAD)`

**`lead(pair)`** — a lead paragraph whose lines rise into focus; inside a body column.

**`prose(paras, cls='')`** — reading paragraphs, `paras = [(ko, en), ...]`.

**`bullets(ko_list, en_list)`** — a list with short marks in the page's deep tone (umber without a tone).

**`kv(rows)`** — definition rows on hairlines: `[(label (ko, en) or html, value html), ...]`. Put the director's email
as `kit.mail(addr) + t('서영준 연구소장', 'Director Young Joon Seo', 'p', 'k-d')`.

**`ruled(items, cols=2, m2=False)`** — columns, each opened by a drawn hairline, an h3 in the display face and the
text: `[(h3 (ko, en) or html, body html), ...]`, 1-4 columns. Three or four columns become two below 1100 px (980 is
the whole desktop view when the Wix element stays 980 wide); one column at 320 (`m2=True` keeps two at 320). In a
two-column text grid an odd last item takes the whole row (`fig_cols()` plates never do).
Mission/Vision: `kit.ruled([(('미션', 'Mission'), t(ko, en, 'p')), (('비전', 'Vision'), t(ko, en, 'p'))], 2)`.

**`areas(items=AREAS)`** — the four research areas, 2 x 2.

**`plate(src, alt, w, h, href='', srcset='', sizes=..., ratio=1.6, inset=.06)`** — a figure or diagram as a sheet in a
hairline frame of fixed ratio (16:10): the image keeps its own ratio (pass its real `w`, `h`), fitted with a 6% margin,
never cropped; it is cut open when its block appears. `href`: the full-size original (new tab, zoom cursor).
**`fig_cols(items, cols=2, m2=False)`** — ruled columns with a plate: `[(plate html, h3, body html), ...]`.
**`figure_plate(f, alt, sizes='(max-width: 760px) 100vw, 50vw', **kw)`** — `plate()` for a repository figure made by
`python3 tools/media.py figure <file> --slug <name> [--crop x,y,w,h]`: `f` is what the command prints, `{src, widths, width,
height}`; the smallest copy is the `src`, all copies the `srcset`, the largest opens full size. Research projects:
`kit.figure_plate(FIGS[key][0], (ak, ae))` in `sec_wide()` (2026-11-09: the four round-1 imgur figures became repository
copies in `site/media/figures/`); HeAD Lab puts the big-data center's structure diagram inside its `dc_box()`.
Audiso products: `kit.fig_cols(items, 3, m2=True)` (two columns at 320).

**`record(items, links=None)`** — figures on counter wheels with labels on a hairline (the Home hero's record, for inner
pages): `items = [(n, (ko, en)), ...]` (`core.OUTCOMES` has the four totals); `links`: a target per item (`'#report'`
jumps in the page, a page name links, `None`); a linked label carries a hairline at rest (2 px and ink on hover).
Research hero extra:
`kit.record([(len(kit.PUBS), ('학술지 논문', 'Journal articles')), (len(kit.REPORTS), ('학회 발표', 'Conference presentations')), (len(kit.PATENTS), ('특허 (출원·등록)', 'Patents (filed and granted)'))], ['#publication', '#report', '#patents'])`

**`box(body, media='', cls='', tone=None)`** — a panel on a lab's tint (`tone`) or in a hairline frame; `media` (a badge
or logo img) at the left of the body, multiplied into the tint (112 px); at 320 it sits above the body, 72 px wide, and
the text keeps the full width. h3 and p inside are styled; the h3 is set in the display face and the kit marks it
`k-dk` (its glyphs go into the font subset). Audiso's KOLAS panel: `kit.box(t('KOLAS ...', '...', 'h3') + t('ISO ...', '...', 'p'), kit.img(kit.imgur('https://i.imgur.com/Ycn67aA.png', 'm'), ('KOLAS ...', 'KOLAS ...'), 886, 529), tone='audiso')`

**`quote(text, cite=None, photo=None)`** — a pull quote (Noto Sans KR 500, the opening mark hung), a cite line with a
short umber mark and an optional small face (`photo`: an imgur URL). `text`, `cite`: `(ko, en)`. A `prose()` right after
it gets the right space.

**`logos(items)`** — partner logos on a hairline grid, 4 columns (2 at 320); `items = [(src, (ko, en)), ...]` or
`(src, alt, dict(w, h, crop=(top, right, bottom, left), style=''))` for equal visual area (`LOGO_AREA`). About's list
with sizes and crops is `PARTNERS` in `tools/pages_v2/about.py` (keep the two transparent PNGs at full size; the other
files over 700 px wide use `kit.imgur(u, 'l')`).

**`map_embed(src, title, link_href='', link_label=...)`** — Google Maps `output=embed` in a 2:1 hairline frame (4:3 at
320), lazy, KO/EN accessible name, an external link under it. Contact's `MAP_SRC`/`MAP_LINK` are in
`tools/pages_v2/contact.py`.

**`contact_rows(items)`** — team contacts as mailto rows on the lab-row pattern (tone tab, hover tint): lab name and
team, the contact person with a small face, the email, and an envelope at the end (the row opens the mail app, not a
page). `items = [dict(key, name, team=(ko, en), person=(ko, en), email, photo), ...]` (Contact builds them from its
round-1 copy and data/people.json).

**`more(path, ko, en=None, cls='', external=False)`**, **`btn(href, ko, en=None, external=True)`** (wrap several in
`<p class="k-btns">`), **`mail(addr)`** (the address written out; its target reaches 24 px, 44 px at 320, without
moving the text), **`mark(tone_key)`** (a small square), **`nw(s)`** (no wrap), **`nw_paren(s)`**.

### Labs, data centers, organisation

**`lab_rows(labs=LABS, with_faces=True, current=None)`** — linked lab rows: name (display), team and member count,
description, small greyscale faces (colour on hover), arrow; each row has its lab's tone tab, and hover (or `current`)
fills it with the lab's tint.

**`faces(members, limit=6)`** — the face strip alone.

**`data_centers(items=DATA_CENTERS, links=True)`** — the two national data centers: the logo is the heading, a line of
text, a link to the lab.

**`dc_box(key, body='', since=None, tone=None)`** — the data-center panel on a lab page, on the lab's tint: logo heading,
an optional line, then body (usually `prose([...]) + bullets(ko_list, en_list)`).
`kit.dc_box('hearing', kit.prose([DC_TEXT]) + kit.bullets(DC_KO, DC_EN), since=('2019년 1월부터 운영', 'In operation since January 2019'))`

**`org_chart(current=None, labs=LABS)`** — the institute and its director at the root, the units hanging from a drawn
hairline; `current`: that unit on its tint with '현재 페이지 / This page', not linked. 320: a vertical tree.

**`lab_page(key, *, tagline, intro, mission, subjects, manager, alt=None, logo=None, image=None, dc=None, alumni=(),
comment='')`** — a whole lab page (returns the document; Basic Lab, Hearing Lab, HeAD Lab). Order: hero > 연구실 소개 >
데이터센터 (if `dc`) > 미션 · 비전 > 연구 주제 > 조직 > 연구소장 · 매니저 (link to People with the team count) > 논문 (the lab's
publications from data, year filter, link to the conference reports on /project) > 졸업생 (if `alumni`). Every section
carries the lab's tone. Mission takes two columns at most: a third item (HeAD Lab's core values) takes the row
under them. Arguments are exactly round 2's `render_lab()` arguments in `tools/pages_v2/<lab>.py`
(`mission=[((ko, en), ko, en)]`, `subjects=[(title_ko, title_en, ko, en)]`, `manager=dict(photo, name=(ko, en),
lines=(ko_list, en_list))`, `alumni=[(name, photo, role_ko, role_en)]`), plus `image` and with `dc` built by
`kit.dc_box(...)`. `logo=('https://i.imgur.com/QV0SgF2.png', 981, 230)` for HeAD Lab.

### People

**`people_grid(members, size='m', tone=None)`** — portraits 4:5, each cut open from an ink line through its middle;
name, role lines. `size='l'`: 3 columns (faculty; a list with 112 px portraits at 320; the portraits drift a little
against the page on desktop); `'m'`: 6 columns on desktop, 3 at 320; `'s'`: 6 small columns, a list with 64 px
portraits at 320 (alumni). A member without a photo gets an initial on the tone's tint. Members are people.json dicts
(`name, role, dept, photo`; roles are translated with `ROLE_EN`, the department goes on its own line) or dicts with
`role_ko`/`role_en` (alumni).

**`team_sec(key, members=None, size=None, link_lab=True)`** — a People-page team section from people.json: heading (the
lab's Latin name, or the team's KO/EN name), the count note, a link to the lab page for the four labs, the tone tab and
the grid (`'l'` for the faculty, `'m'` otherwise). **`team_heading(key)`** gives `(heading, note)` alone.

**`jump_nav(items, label=('이 페이지의 구성', 'On this page'))`** — in-page jump links for `page_hero(extra=)`:
`[(section id, label (ko, en) or a Latin string, tone key or None, count or None), ...]`; a count sits on the label's
baseline in small grey numerals. The runtime scrolls with `scrollIntoView` (a plain #fragment does not scroll the Wix
page); the section lands 24 px below the top, 152 px at 320 (under Wix mobile's sticky header).

**`feature(photo, name, role, lines=None, quote=None, email=None, alt=None)`** — a person: 4:5 portrait cut open, an
optional quote, name and role, credentials, email. `name`, `role`, `quote`: `(ko, en)`; `lines`: `(ko_list, en_list)`.
Two in a row are spaced for you. **`director(short_en=True, quote=True)`**: Home uses the defaults; About uses
`short_en=False, quote=False`.

**`role_lines(m)`**, **`member(m, size)`** — the pieces of a card, if you need them.

### Lists (publications, conference reports, patents)

**`list_sec(h, kind, items, sid, note='', filters=None, per_page=10, aside='', foot='', tone=None)`** — a whole list
section (C2's publication list, generalised). Heading column: heading, note and the controls (filters with a count on
every option, which turns over when another filter changes; the result count; **the reel: one frame per item**, newest
first, the matching frames lit, the page on screen in umber; first and last year under it). Body column: the rows and
the pager, which always follows the rows. Paging and filtering never change the page height (the tallest page of every
filter combination, in both languages, is reserved; the spare height sits after the pager). Paging from the bottom
brings the list's top back on screen.
- `kind`: `'pub'` (year | title, authors, journal | team mark), `'report'` (year | title, authors, event), `'patent'`
  (status | title in Korean | country). A list without the team column (reports, a lab's own publications) gives the
  text that width (`.k-row--nm`).
- `filters`: default pub `('team', 'year')`, report `('year',)`, patent `('status',)`; Research's patents use
  `('status', 'country')`; a lab page uses `('year',)`. Years: the last five plus one option for everything earlier,
  shown `~2021` in Korean and with a drawn ≤ mark (`≤2021`) in English (a tilde reads 'about' in English); screen
  readers hear '2021년까지' / '2021 and earlier'. A filter with fewer than two options is dropped.
- The reel has one frame per item; a short list (a lab's 17 to 41) keeps frames at 6 px at most, from the left, so it
  stays a tick strip and its first and last year stand at its ends.
- `note`: round 2's notes are in `kit.REEL_NOTE[kind]` (`'눈금 하나가 논문 한 편입니다.'`...). Do not port round 2's
  sentence about navy ticks: the reel is not navy any more.
- `foot`: html under the pager (the lab pages' link to `/project#report`); `aside`: html under the controls.
`kit.list_sec(('논문', 'Publication'), 'pub', kit.PUBS, 'publication', note=kit.REEL_NOTE['pub'])`

**`listing(kind, items, filters=None, per_page=10, sid='')`** — the same list stacked in one column (controls above the
rows) for a body column.

### Video and gallery

**`videos_sec(h=None, videos=None, sid='videos', note='')`** — heading and playlist in the heading column, the 16:9
player in the body column (320: heading, player, playlist; the 'now playing' line under the player is left out there,
because the playlist right under it says the same and its umber bar marks the current video). From
`data/videos.json`; plays only on click (preload metadata, native controls, an ink play chip that reads on a white
poster); the height never changes.
**`video_player(videos=None)`** — player and playlist stacked, for any body column.

**`gallery_teaser(photos=None, h=None, note=None, sid='gallery', rows=(2, 3))`** — Home and About: a wide section,
photos in justified rows linking to /gallery, each cut open; at 320 the first spans the width (3:2), the others sit in
pairs (4:3). Default photos: `gallery_pick(5)`.
**`gallery_pick(n, exclude=(), photos=None)`** — up to `n` photos in `data/gallery.json` order (newest first), one per
event: the same year and the same Korean caption before the first comma (`'제5회 청각재활연구소 워크샵, 팀 소개'`) count
as one event, so write the event first in captions. `exclude`: strings matched against file / media / src (About passes
its hero photo, `IMG_0168`).

**Photos in two kinds** (CLAUDE.md "사진"): `data/gallery.json` mixes Wix entries `{media, file, width, height, year,
caption_ko, caption_en}` and repository copies `{src: 'media/gallery/<year>/<year>-<nn>', widths: [480, 1024, 1600],
width, height, year, caption_ko, caption_en}` (files `<src>-<width>.jpg`). Every gallery component and
`gallery_photo()` draw both; if you need a URL yourself use **`photo_url(p, w, q=None, crop=None)`** (about `w` px:
Wix fitted, or the smallest stored width >= w; `crop` for Wix entries) and **`photo_srcset(p, ws=(600, 1200), crop=None)`**. People photos are Imgur URLs or
`media/people/<slug>.jpg`; `kit.imgur(u, size)` adds a size only to Imgur URLs. Data paths are relative to `site/`;
preview pages are rewritten to `../site/media/` by `page()`. New photos go in only through `python3 tools/media.py`
(a sheet year of `-` stores an undated photo: `media/gallery/undated/`, year `""`, at the end of the list, shown under
'전체' only and without a year label).
`CROP_POS` (kit.py, keyed by `src`) moves the 320 crops (4:3 in the gallery, 3:2 / 4:3 in the teasers) of photos whose
subject is off centre; desktop frames keep each photo's own shape, so it changes nothing there. `_cap_year()` shows the
year after a caption only in a language whose caption does not already contain it.

**`gallery_grid(photos=None, per_page=12, years=True, live=False)`** — /gallery: year filters with counts, justified
rows (no crop on desktop; two 4:3 columns at 320), 12 per page, the pager, a viewer that opens in place over the grid
(inside the visible band of the tall iframe, 12 px clear, even if that takes it past the gallery's own box; never past
the document's ends; Esc, arrow keys, focus kept inside). At 320 the year options wrap as a row of their own widths.
The grid reserves its tallest page (every year, both languages). Put it in `sec_wide(...)`. `live=True` keeps round 2's CMS protocol: the page posts
`{type: 'ready'}` to `window.parent` and accepts `{type: 'gallery', items: [{src | media, width, height, caption_ko,
caption_en, year, file?, alt_ko?, alt_en?}]}`; the Velo code, the CMS setup and the Wix heights for more photos are
in `tools/pages/gallery.md`.

## 5. Page recipes (round 2's order in C2; the copy is in tools/pages_v2/<page>.py)

These are the compositions the kit was built for. Keep the order; adapt only what the copy needs.

| page | hero | sections |
|---|---|---|
| about | `page_hero(('연구소 소개', 'About RIHE'), alt=<round 2's alt>, lead=..., image=gallery_photo('IMG_0168', '50% 32%'))` | `sec('청각재활연구소', quote(...) + prose([...]))` > `sec('연구소장', director(short_en=False, quote=False))` > `sec('조직', org_chart())` > `sec('데이터센터', data_centers())` > `sec('협력 기관', logos(PARTNERS))` > `gallery_teaser()` |
| research | `page_hero(('연구', 'Research'), alt=RESEARCH_TITLE, lead=RESEARCH_LEAD, extra=record(<3 lists>, ['#publication', '#report', '#patents']))` (tint `inst`) | `sec_wide('연구 분야' / 'Projects', fig_cols(<4 figure_plate()>, 2), 'projects', note=('그림을 누르면 원본 크기로 열립니다.', ...))` > `list_sec('논문' / 'Publication', 'pub', PUBS, 'publication', note=REEL_NOTE['pub'])` > `list_sec('학회 발표' / 'Report', 'report', REPORTS, 'report', ...)` > `list_sec('특허' / 'Patents', 'patent', PATENTS, 'patents', filters=('status', 'country'), ...)` |
| people | `page_hero(('구성원', 'People'), alt=PEOPLE_TITLE, lead=PEOPLE_LEAD, image=gallery_photo('IMG_0168', '50% 32%'), extra=jump_nav([(key, label, TEAM_TONE[key], count) for every team with members], ('팀 바로가기', 'Jump to a team')))` | `team_sec(key)` for every team in people.json order (faculty > basic > hearing > head > admin > audiso); labels: lab name for labs, `(TEAM_META ko, en)` otherwise |
| basic-lab | via `lab_page('basic', ...)` (no image: the basic tint) | lab template |
| hearing-lab | via `lab_page('hearing', ..., dc=dc_box('hearing', ..., since=...), alumni=..., image=gallery_photo('IMG_7721')?)` | lab template (the plaque photo is a suggestion for the client to confirm; without it the hero is the hearing tint) |
| head-lab | via `lab_page('head', ..., logo=('https://i.imgur.com/QV0SgF2.png', 981, 230), dc=dc_box('head', ...), alumni=...)` | lab template |
| audiso | `page_hero('Audiso', alt=..., lead=..., logo=(imgur(lQwB2st.jpeg, 'l'), 1858, 542), tone='audiso', inst='Audiology with ISO', extra=<two btn()>)` | `sec('Audiso 소개', prose(INTRO) + box(<KOLAS>, media, tone='audiso'))` > `sec('오디에스오의 강점', ruled(STRENGTHS, 3))` > `sec('미션 · 비전', ruled(<2>, 2))` > `sec('조직', org_chart(current='audiso'))` > `sec('제품', fig_cols(<6 plates>, 3, m2=True))`; `page(..., tone='audiso')`, sections with `tone='audiso'` |
| contact | `page_hero(('연락처', 'Contact'), alt=('청각재활연구소에 문의하기', 'Get in touch'), image=gallery_photo('21.png', '50% 62%', '42% 50%', crop=(96, 2, 1295, 524)))` (21.png is a banner: the crop takes its opaque rendering) | `sec('연구소 안내', kv(<address, email, affiliation>) + map_embed(...))` > `sec('팀별 연락처', contact_rows(<3 teams>))` |
| gallery | `page_hero(('갤러리', 'Gallery'), lead=..., image=gallery_photo('IMG_6300', '50% 40%'))` | `sec_wide(('사진', 'Photos'), gallery_grid(live=True), 'photos')` > `videos_sec()` |

Notes: labs pass `tone=` to every section (lab_page does it); the faculty tone is `inst`; give the Research and People
lists/teams no extra headings beyond the recipe. Hero images are suggestions from the existing photos; record your
choice in your report so the client can confirm it.

## 6. CSS classes and markup conventions

- You should not need raw markup or CSS. If you write raw HTML inside a body, use only these classes: `.k-btns`,
  `.nw`, `.sr`, `.k-d` (secondary paragraph), `.k-num` (a number in the counter numerals), `.k-dk` (text set in the
  display face by a component: puts its glyphs into the Black Han Sans subset). No page-local `<style>`.
- Component classes (for reading the output, not for re-use): layout `.k-sec .k-in .k-ln .k-sh .k-h .k-note .k-aside
  .k-sb .k-swl`, chapter `.k-ch .k-chs .k-leadw .k-lead`, text `.k-prose .k-bul .k-kv`, columns `.k-cols .k-col
  .k-rule .k-h3 .k-d .k-figs .k-plate`, frames `.k-ph .k-pp .k-im .k-cut .k-ini`, record `.k-rec`, labs `.k-labs .k-lab
  .k-faces`, data centers `.k-dcs .k-dc .k-dcb`, org `.k-org`, people `.k-ppl .k-mem .k-mi .k-jump .k-ft`, panels `.k-box
  .k-pq .k-logos .k-map .k-ct`, lists `.k-lsec .k-ls .k-ctl .k-f .k-fb .k-bc .k-ind .k-tally .k-reel .k-lw .k-list
  .k-row .k-pg .k-pi`, video `.k-vid .k-scr .k-play .k-now .k-plist`, gallery `.k-gteaser .k-gt .k-gl .k-gl-*`, inner
  hero `.k-hero .k-hf .k-hk .k-hw .k-he .k-hin .k-hinst .k-hlow`, Home hero `.cx*`.

## 7. Motion rules (the kit does all of this; do not add motion)

- **Reveal blocks**: an element with `data-a` is hidden under `html.js:not(.rm)` until the script reveals it (`.on`),
  when it is on screen (`RIHE.inview`: IntersectionObserver thresholds only; `rootMargin` is ignored in the cross-origin
  Wix iframe). In a block, the kit draws `.k-rule` hairlines, raises `[data-ai]` items and cuts open `.k-ph` frames; a
  block without parts rises as one. `data-m` names special motions: `head` (a section head: the cut line is drawn and
  the heading rises through its mask), `chap`, `lead` (lines rise into focus), `list`, `rec` (counter wheels), and
  `ln`/`ctl`/`hp` (parts revealed by their owner).
- **Order on load**: on an inner page nothing under the hero is revealed before the hero opens. Reveals that come due
  earlier wait for its frame to split (+.15 s), at most 1.4 s, so the next section's cut line is drawn as the frame
  opens. A section's body follows its heading by .25 s (at most .9 s of waiting when the heading is off screen). In a
  portrait block the names rise as the portraits open (.75 s). List controls start their list's reveal too (at 320
  they are on screen before the rows).
- **Safety nets** (never remove): hidden states exist only under `html.js` (set before first paint); the kit calls
  `RIHE.motionReady()` at once, else everything shows after 3 s; if no IntersectionObserver callback arrives within
  1.5 s everything shows; if the runtime never finishes, a CSS timer shows everything after 2.6 s; any module that
  throws shows everything (`RIHE.showAll()`); without GSAP everything shows and lists, gallery and video still work.
- **Reduced motion** (`html.rm`): everything visible at once, no transitions, no animations, the Home reel does not
  play (the pause button offers play). This is the client's rule and overrides any skill's advice.
- **Scroll**: only through the runtime's sentinel band (`RIHE.onBand`, `RIHE.rect`, `RIHE.progress`), never window
  scroll, ScrollTrigger, sticky, fixed, `preventDefault` on wheel or touch, or viewport-height units. The kit uses the
  band for the hero photographs' drift, the faculty portraits' drift (desktop) and to load images before they reach
  the screen.
- **Loops**: only the Home reel and its film grain (desktop), paused off-screen, in a hidden tab and by the button.
- **Hover**: arrows move 5 px, underlines thicken, lab rows take their tint, faces and portraits regain colour,
  buttons fill with ink, pager buttons press to 0.94.
- **Height**: no interaction changes the page height (lists, gallery, viewer, video, language switch).

## 8. Verify every page (repo root; one browser check at a time)

```
python3 tools/build.py --only <name> && python3 tools/build.py --preview --only <name>
node tools/verify/wixsim.js site/<name>.html <out> --w 1280      # and --w 320, and --w 1280 --lang en
    # crossOrigin true, stillInvisible 0, brokenImages [], errors [], band maxErrorPx small
node tools/verify/render.js site/<name>.html <out> --widths 1920,1440,980,320 --langs ko,en --frames
    # every shot: stillInvisible 0, brokenImages 0, errors 0; KO height = EN height at each width
node tools/verify/interact.js site/<name>.html                   # and --width 320: changes []
node tools/verify/fallback.js site/<name>.html                   # and --width 320: stillInvisible 0, reduced runningAnimations 0
node tools/verify/heights.js site/<name>.html --md               # then fill your row in docs/wix-heights.md
    # pages with justified photo rows (gallery): add --sweep 20 (every 20 px from 980 to 1920)
```

Last full run (2026-11-09, the stage-2 Finish build): all ten pages pass every check above (wix-sim 30 runs,
interact and fallback at 1280 and 320, KO = EN heights at every width); the results are in DESIGN.md "2단계 마무리"
and the heights in `docs/wix-heights.md`. Re-run them for any page whose module or data you change.

Look economically: the load-in as one strip (`node tools/verify/strip.js <out>/strip.png <out>/sim/t*.png --width 260
--cols 6`), widths and languages as one sheet (`node tools/verify/compare.js site/<name>.html <out>/cmp --widths
1920,1440,980,320`, add `--lang en`), details with `node tools/verify/shoot.js ... --sel ".k-lsec"`. Pipe long JSON
through grep. Screenshots under `/tmp/claude-0/stage2/<task>/`.

## 9. Pitfalls

- `sec()` and `chapter()` need a `sid`; ids must be unique on the page (a `section[id]` gets the jump margin).
- `.k-mt` is the underlined label of `more()`/`btn()`; a member card's text block is `.k-mi`. Do not reuse either.
- Pass `(ko, en)` tuples for headings and notes; html from `t()` works too. A Korean-only string in a heading would
  show on the English page: always give the pair.
- Round 2's `kit.rv()`, `kit.sec(..., note=t(...))` with `.rv` children, `listing()` notes about navy ticks,
  `cochlea_hero()`, `team_mark()`, `.serif`, `.mono`, `data-rv`, `data-hold`: gone. Use the components above.
- Images: keep imgur URLs' case; use `kit.imgur(u, 'l')` (640 px) for portraits and plates, `'m'` (320 px) for small
  faces; Wix media through `kit.wix(...)`, gallery entries through `gallery_photo()` / `photo_url()` (never
  `p['media']` directly: repository entries have none); repository photos stay relative (`media/...`).
- Do not call `core.page_shell` yourself; `kit.page()` does it.
- `site-preview/_kit*.html` are demos, not site pages.
