# RIHE design kit ("Cochlea"): developer guide

This guide is for anyone writing a page in `tools/pages/<name>.py`. Read it with `tools/kit.py` open beside it. Home (`tools/pages/home.py`) is the reference page.

## 1. How a page is built

```
tools/kit.py            design system: tokens, shared copy, helpers, components, CSS, JS
tools/pages/<name>.py   one page; exposes render() -> full HTML string (via kit.page)
tools/build.py          python3 tools/build.py [--preview] [--only home,research]
site/<name>.html        production file (paste into Wix; no language toggle)
site-preview/<name>.html  same page plus a small KO/EN toggle at the bottom right
```

Page names: `home, about, research, people, basic-lab, hearing-lab, head-lab, audiso, contact, gallery`. `build.py` skips any page module that does not exist yet.

The smallest possible page:

```python
import kit
from kit import t, sec, more

def render():
    body = (kit.page_hero(t('연락처', 'Contact'), lead=('청각재활연구소에 문의하기', 'Get in touch'))
            + '<main>'
            + sec(t('연구소 안내', 'Visit us'), kit.kv([(t('주소', 'Address'), t('...', '...'))]), 'visit')
            + '</main>')
    return kit.page('Contact', 'navy', body)
```

**What build.py checks:** it fails the build if visible copy contains an em-dash, if a `data-l="en"` element has no `lang="en"`, or if the page loads an external `<script src>`.

**Where the copy comes from.** Shared copy is in kit.py: `INST, NAME, MISSION, AREAS, LABS, DIRECTOR, DATA_CENTERS, NAME_EN, ROLE_EN, TEAM_META, TEAM_LABEL, UI, TECH_TRANSFERS`. Everything else is in `tools/build_v1.py`, which has all the round-1 KO/EN copy for every page, including lab intros, missions, subjects, alumni, Audiso strengths and products, partners and contact details. Port that copy as it is. Never invent facts, names, numbers or awards.

**Data:** use `kit.PUBS, kit.REPORTS, kit.PATENTS, kit.PEOPLE, kit.GALLERY, kit.VIDEOS` (loaded from `data/*.json`). `kit.TEAMS[key]` gives a people.json team (`faculty, basic, hearing, head, admin, audiso`). Derive counts from data with `len()`; never hard-code them.

## 2. Verify every page

```
python3 tools/build.py --preview --only <name>
cd <scratchpad> && NODE_PATH=/opt/node22/lib/node_modules node render.js /home/user/WIX_DEV/site-preview/<name>.html <out> --frames
```

Look at all four PNGs (1280 and 320, KO and EN) with the Read tool. `<scratchpad>/kit/demo.py` builds a page using every component (a working example of each call). The other helper scripts there are `shoot.js` (crop), `probe.js` (evaluate JS), `interact.js` (height stability), `heights.js` (iframe heights at 320-1920) and `fallback.js` (no-JS, script failure, reduced motion). `stillInvisible`, `brokenImages` and `errors` must all be 0. Any URL listed under "NOT IN MIRROR" has to be fetched first. Run this from the scratchpad: `python3 -c "from mirror import dl, dl_css; dl('<url>')"`. Use `dl_css` for Google Fonts CSS. Every page has its own Hahmlet subset URL, so run `dl_css` on it each time the page's serif text changes. Long URLs are stored under hashed file names, and that is expected.

## 3. KO/EN conventions

- **Every visible string is a pair.** `t(ko, en)` gives `<span data-l="ko">ko</span><span data-l="en" lang="en">en</span>`. CSS hides the language that is not active.
  - For block elements, pass the tag: `t(ko, en, 'p')`.
  - For a `(ko, en)` tuple, use `tt(pair)`.
  - `t(text)` with no English is language-neutral (lab names, years, emails).
- **Language source.** The language comes from `?lang=en|ko`, which a head script applies before first paint, so there is no flash of Korean. Wix page code can also send `postMessage({lang:'en'})`. In preview, the toggle sets it.
  - `window.RIHE.lang` holds the current language.
  - `RIHE.onLang(fn)` runs `fn` when the language changes.
- **Attributes.** Image alt text is a pair: `img(src, (alt_ko, alt_en))` writes `alt` plus `data-alt-en`. For aria labels, write `aria-label="한국어" data-aria-en="English"`. The script swaps both.
- **Links between pages.** Use `link(page_or_path, inner)` or `more(page, ko, en)`. Both write `href="https://www.smilesnail.org/<path>" target="_top" data-path="/<path>"`. In English the script rewrites the link to `SITE + EN_PREFIX + path`.
  - Use page names from `kit.PATHS`: home `/`, about `/about`, research `/project`, people `/people`, basic-lab `/about-1`, hearing-lab `/hearing-lab`, head-lab `/head-lab`, audiso `/audiso`, contact `/연락처`, gallery `/gallery`.
  - Raw paths also work, for example `link('/project#patents', ...)`.
  - **Caution:** Wix Multilingual is OFF on the live site, so `/en/...` returns 404 today. Setting `kit.EN_PREFIX = ''` keeps English links on the Korean URLs until Multilingual is enabled.
- **Korean copy.** Keep the Korean natural and use the existing copy. Do not translate Korean from the English. Lab names (Basic Lab, Hearing Lab, HeAD Lab, Audiso) stay in Latin in both languages.
- **No em-dash characters** in visible copy (the build fails). Use a comma, a colon or ` · `.
- **Height budget.** English text runs longer than Korean. EN body text already gets tighter leading (1.7 against KO 1.8). If EN still runs much longer, shorten the EN copy on summary pages (see `DIRECTOR['lines_en_short']`). Do not shrink the type.

## 4. Tokens and type

| token | value | use |
|---|---|---|
| `--paper` | #ffffff | page ground (white only) |
| `--ink` / `--ink-2` | #131b2a / #566072 | text / secondary text (AA) |
| `--line` / `--mist` / `--wash` | #e3e7ed / #f4f6f9 / #eef2f7 | hairlines / image placeholders, initial tiles / panels (`.box`, video frame) |
| `--navy` | #1b3d6f | brand: links, numbers, ticks, active markers |
| `--basic --hearing --head --audiso --collab` | #2e8b57 #4e7595 #2e6e9e #9a6f07 #7a8494 | lab identity. Used only for 14x2 px marks, underlines, the hero coil and bullets. Never for text. |
| `--accent` | set by `page(accent=...)` | page colour (hero coil, bullets) |

Python: `kit.COLORS[key]`. In HTML, set `style="--c:var(--basic)"` on lab-coloured elements.

**Type** (Hahmlet is display only):
- **Hahmlet 300/400** for h1, h2, h3, lab names, people names, outcome numbers and initials.
- **Noto Sans KR 400/500** for everything you read: body text, the director quote, captions and UI.
- **DM Mono 400** for measurements: years, durations, counts, the pager and emails.

**Hahmlet is subset per page.** `page()` collects the characters inside serif elements and requests only those glyphs from Google Fonts (`text=`).
- Serif elements are the tags `h1 h2 h3` and the classes `serif oc-n nm ini t pt ft-nm`.
- To set other text in Hahmlet, add `class="serif"`. Never point CSS at `var(--serif)` on a new selector without adding the class to `SERIF_CLASSES`. Otherwise those glyphs will be missing.
- Text that JS creates at runtime must not be in Hahmlet unless the same characters already appear in a serif element (for example, the video title is copied from `.pt`).

**Scale, desktop then 320:**

| element | desktop | 320 |
|---|---|---|
| H1 inner pages | KO 56 / EN 46 / neutral 52, weight 300 | 36 / 29 / 34 |
| h2 | 30 | 24 |
| h3 | 22 | 19 |
| body | 15.5 / 1.8 | 15 |
| `.lead` | 18 | 16 |
| `.note` | 14 | 14 |
| mono | 12 | 12 |

**Layout:**
- Container 1200 px with 40 px gutters; 16 px gutters at 320.
- Sections are 120 px apart (72 px at 320).
- The mobile breakpoint is `max-width: 760px`. The same file serves Wix desktop (980 px and up) and Wix mobile (exactly 320 px).
- Corners: 3 px on images and panels, 2 px on thumbnails. No shadows except under the play button.
- Never use 100vh, position fixed or sticky, scroll-jacking, or content that grows a lot on click. Paginate instead.

## 5. Helpers (all return HTML strings)

| signature | what it does | example |
|---|---|---|
| `t(ko, en=None, tag='span', cls='', attrs='')` | KO/EN pair | `t('연구실', 'Labs')` |
| `tt(pair, tag='span', cls='', attrs='')` | pair from a tuple | `tt(kit.INST)` |
| `link(path, inner, cls='', attrs='')` | site link (target _top, data-path) | `link('people', t('구성원', 'People'))` |
| `ext(href, inner, cls='', attrs='')` | external link, new tab | `ext('https://audiso.co.kr/', 'audiso.co.kr')` |
| `more(path, ko, en=None, cls='', d=None, external=False)` | navy text link with arrow | `more('gallery', '갤러리 전체 보기', 'Open the gallery')` |
| `btn(href, ko, en=None, external=True)` | outlined button link (wrap several in `<p class="btns">`) | `btn('https://xr.audiso.co.kr/', 'xr.audiso.co.kr')` |
| `img(src, alt=('', ''), w, h, cls='', lazy=True, srcset='', sizes='', attrs='')` | image; alt pair or '' (decorative) | `img(u, ('연구소 전경', 'Campus'), 800, 600)` |
| `wix(media, file, w, h, mode='fill', q=85)` | resized Wix media URL with `enc_auto` (fill = crop, fit = no crop) | `wix(p['media'], p['file'], 1200, 1200, 'fit')` |
| `wix_poster(base, w=1280, h=720)` | poster URL from videos.json `poster`/`thumb` | |
| `imgur(src, size='')` | imgur variant: `b` 160 px square, `m` 320, `l` 640 | `imgur(m['photo'], 'l')` |
| `rv(html, d=None, tag='div', cls='')` | wrap in a reveal element with stagger index | `rv(t('...', '...', 'p'), 2)` |
| `sec(h, body, sid='', note='', cls='', aside='')` | **the standard section**: hanging heading column (h2 + note + aside) and a content column | `sec(t('소개', 'About'), kit.prose(...), 'about')` |
| `sec_wide(h, body, sid='', note='', link_html='', cls='')` | full-width section, heading row with a link at the right (gallery pattern) | `sec_wide(t('갤러리', 'Gallery'), kit.gallery_grid(), 'gallery')` |
| `prose(paras, cls='')` | paragraphs in one 36em column; `paras = [(ko, en), ...]` | `kit.prose([('...', '...')])` |
| `bullets(ko_list, en_list)` | list with short accent rules | |
| `kv(rows)` | definition list; `rows = [(label_html, value_html)]` | contact details |
| `logos(items)` | partner logo grid, 4 columns (2 at 320); `items = [(src, alt)]` or `(src, alt, opts)`: with `opts = dict(w, h, crop=(top, right, bottom, left), style='')` every logo gets the same visual area (`LOGO_AREA`), whatever its ratio; `crop` trims whitespace built into the file (fractions), `style` adds css to the img (a filter for a white logo) | About: `(u, ('대한청각학회', 'Korean Audiological Society'), dict(w=959, h=453, crop=(.28, .14, .35, .13)))` |
| `team_mark(key)` | 14x2 px lab-colour mark | `kit.team_mark('head')` |
| `name_pair(name)` / `initials(name)` / `role_en(s)` / `member_role(m)` | people helpers (romanised name, KO/EN initial, role translation) | |
| `url(path)` | absolute production URL | |

## 6. Components

**Heroes**
- `page_hero(title, alt='', lead='', logo='', extra='', inst=INST, cls='')` is the hero for every inner page.
  - Layout: institute line, H1, an optional alt line, then the hairline that ends in a small closed coil, then an optional lead and extra.
  - The coil is in the page accent colour and draws once on load in pure CSS: the line goes out to the right and then coils. It works with no JS and has no ambient motion.
  - `title`, `alt` and `lead` take `t()` html or `(ko, en)` tuples.
  - `logo` replaces the visible title with an `<img>` html, keeping the title as hidden text. For HeAD Lab or Audiso: `logo=kit.img('https://i.imgur.com/QV0SgF2.png', ('HeAD Lab', 'HeAD Lab'), lazy=False)`.
  - `extra` takes buttons or a team nav.
  - Example: `kit.page_hero('Hearing Lab', alt=('참조표준팀', 'Reference standard team'), lead=('한국인 청각의 표준을 만들어가는 연구', 'Setting the standard for Korean hearing'))`.
- `cochlea_hero(note=None)` is for Home only: the full tonotopic cochlea, drawn by JS, with the page's one ambient pulse.

**Text blocks**
- `ruled(items, cols=2, d0=0)` gives ruled columns. `items = [(h3_html, body_html)]` and `cols` is 1 to 4 (always 1 at 320). Each hairline draws in before its text. Use it for Mission/Vision, research subjects, Audiso strengths and the products text.
  - Example: `kit.ruled([('Mission', t(ko, en, 'p')), ('Vision', t(ko, en, 'p'))])`.
- `areas()` gives the four research areas (KO titles on KO).
- `fig_cols(items, cols=2, d0=0)` is `ruled()` with a figure: hairline, plate, h3, text. `items = [(plate_html, h3_html, body_html)]`. The Research page uses it for the four project areas with their images.
- `plate(src, alt, w, h, href='', srcset='', sizes=..., ratio=1.6)` sets an image or diagram as a framed sheet on a `--wash` panel of fixed ratio (16:10 by default), like the video poster. Pass the image's real `w`/`h`: it is fitted inside the panel at its own ratio (positioned in %, never cropped), so plates in a row are the same height whatever the image. `href` links the plate to the full-size original in a new tab (zoom-in cursor, navy outline on hover).
  - Example: `kit.plate(kit.imgur(u, 'l'), ('개요도', 'Diagram'), 1389, 879, href=u, srcset=f"{kit.imgur(u, 'l')} 640w, {kit.imgur(u, 'h')} 1024w")`.
- `outcomes(rows, link_html='')` gives counts with tick rows, one tick per item and every tenth tick tall. The reveal runs at a constant rate per tick. Example: `kit.outcomes([(len(kit.PUBS), '학술지 논문', 'Journal articles')])`.

**Labs and data centers**
- `lab_rows(labs=LABS, with_faces=True, current=None)` gives the linked lab rows: mark, name, team and member count, description, a greyscale face strip, and an arrow. On hover each row underlines in its lab colour.
  - On a lab page, pass `current='hearing'` to mark the current lab, and `with_faces=False` for the organisation block.
- `faces(members, limit=6)` / `face(m)` give a face strip on its own. Members without a photo get a mist tile with an initial: the Hangul family-name syllable on KO, and on EN the Latin initial only if `NAME_EN` has a romanised name.
- `data_centers(items=DATA_CENTERS, links=True)` gives the two data-center logos as headings, a line of text each, and a link to the lab that runs it.
- `org_chart(current=None, labs=LABS)` gives the organisation chart: the institute and its director at the root, the units hanging from one hairline that draws in with the block. Each unit shows its name (Hahmlet) and team name and links to its page. `current` highlights one lab: a 2 px drop line in the lab colour, the name in ink, a small '현재 페이지 / This page' line, and no link (`aria-current="page"`). Unit names never wrap (Hahmlet 20 px, easing to 17 px toward 980). At 320 it becomes a vertical tree. About uses `kit.org_chart()`; lab pages use `kit.org_chart(current='hearing')`.
- `dc_box(key, body='', since=None)` gives a data-center panel for a lab page: a `.box` whose h3 is the center's logo (from `DATA_CENTERS`, alt per language), an optional small line (`since=('2019년 1월부터 운영', 'In operation since January 2019')`), then `body` (usually `prose(...) + bullets(...)`). Example: `kit.dc_box('head', kit.prose([(ko, en)]) + kit.bullets(ko_list, en_list))`.
- **Lab pages** share one template, `tools/pages/_lab.py` (`render_lab(key, tagline=, intro=, mission=, subjects=, manager=, alt=, logo=, dc=, alumni=)`); `basic-lab.py`, `hearing-lab.py` and `head-lab.py` only hold their copy. Order: hero (lab-colour coil; HeAD Lab's logo as the title, 60 px / 44 px at 320 via `page_hero(cls='hero-lablogo')` to match the Hahmlet titles of the other labs, `alt=''` since the h1 keeps the name as hidden text) > About > data center box > Mission/Vision(/Core Values) > Research subjects > Organization > Director & Manager (with a link to People and the team count) > Publication (team list, year filter, link to the Research page for reports) > Alumni (left out when there are none).

**People**
- `feature(photo, name, role, lines=None, quote=None, email=None, alt=None)` gives a person block: a 4:5 portrait, an optional quote (Noto, reading size), the name in Hahmlet, credentials and an email. At 320 the portrait (104 px) sits beside the name.
  - `name`, `role` and `quote` are `(ko, en)`; `lines` is `(ko_list, en_list)`.
  - Several in a row stack 56 px apart.
  - Example: `kit.feature('https://i.imgur.com/2Q56Mj7.jpeg', ('변유선', 'Yuseon Byun'), ('Manager', 'Manager'), (['Hearing Lab · 박사과정'], ['Hearing Lab · Ph.D. Student']))`.
- `director(short_en=True, quote=True)` is the director feature. Home uses the short EN credentials. About and lab pages use `short_en=False`, and lab pages use `quote=False`.
- `people_grid(members, small=False)` gives 4:5 portraits in 4 columns (2 at 320), with the name in Hahmlet and the role in Noto. `small=True` gives 6 columns for alumni (imgur 320 px files); at 320 it becomes a list (a 64 px portrait beside the name and role), because three columns broke long Korean department names mid-word.
  - `members` are people.json dicts (`name, role, dept, photo`). For alumni from build_v1, set the role line directly: `{'name': '김지원', 'photo': 'https://i.imgur.com/TWCotbS.jpeg', 'role_ko': '의료정보통계학과 석사 · 2025년 2월 졸업', 'role_en': 'M.S. · Feb 2025'}`. A member with an empty `photo` gets an initial tile.
  - `person_card(m, d)` gives a single card. An initial tile is `aria-hidden` (the name follows it). Names are 19 px, easing to 17 px toward 980 so short romanised names stay on one line in the narrow desktop columns.
  - `people_grid(members, rows=True)` makes each card its own reveal block, so a long grid fades in row by row as it scrolls in (cards of one row share their top edge; the stagger comes from the column, 4/2 or 6/3, in CSS). The People page uses it for every team.
  - Team heading pattern (People): `sec(kit.team_mark('basic') + 'Basic Lab', grid, 'basic', note=..., aside='<p class="h-more">' + more(...) + '</p>')`. A `.mark` as the first child of an h2 sits above the heading as a 14x2 lab-colour bar; `.h-more` spaces a link under the note.
- `jump_nav(items, label=(ko, en))` gives in-page jump links for `page_hero(extra=...)`: `items = [(section_id, label_html, colour_key, count_or_None)]`, each with a 14x2 mark and a mono count (screen readers hear '3명' / '3 members'); 2 columns at 320. A small JS module (included only when the page has `.jump`) scrolls with `scrollIntoView`, because a plain `#fragment` click inside the cross-origin Wix iframe does not scroll the parent page (verified in the harness); focus moves to the section's h2.
  - Example: `kit.jump_nav([('basic', 'Basic Lab', 'basic', 4), ('admin', t('행정팀', 'Administration'), 'ink', 4)], ('팀 바로가기', 'Jump to a team'))`.

**Video**
- `videos_sec(h=None, videos=None, sid='videos', note='')` gives a whole section: h2 and playlist in the heading column, the 16:9 player in the content column. At 320 the order is h2, player, then playlist.
- `video_player(videos=None)` gives a stacked player plus playlist for use inside any content column.
- Both are static markup built from `data/videos.json`. A video plays only on click, with native controls and sound, and the box height never changes. The poster sits as a framed sheet on a `--wash` panel, so the white whiteboard frame never reads as an empty box. Several players per page work.

**Gallery**
- `gallery_teaser(photos=None, rows=(2, 3), h=None, note=None)` is the Home teaser section: the first five entries of `data/gallery.json` in justified rows, each linking to /gallery. At 320 the first photo spans the width (3:2) and the other four sit in two pairs (4:3).
- `gallery_grid(photos=None, per_page=12, years=True, live=False)` is the full gallery for /gallery: year toggles, justified rows (no crop on desktop; 2 columns with a 4:3 crop at 320), a pager when there are more than 12 photos, and an in-place viewer.
  - The viewer is absolutely positioned inside `.gl`, never `position: fixed`. It covers the grid at the clicked photo, centred in the visible band of a tall iframe (IntersectionObserver `intersectionRect`), and clamped to the gallery.
  - It supports Esc and the arrow keys (also after a click on the photo: the layer takes focus, `tabindex=-1`), and focus returns to the thumbnail. A year toggle or the pager closes it, keeping focus on that control.
  - Put it in `sec_wide(...)`.
  - Photo dicts: `media, file, width, height, caption_ko, caption_en, year`, plus optional `alt_ko`/`alt_en`. The mono year after a caption is left out when both captions already name that year (ORL-HNS 2018, KIMES 2019); the year filter still uses it.
  - **Rows (desktop):** JS picks the row breaks that keep every row closest to a target height (about 24% of the width, 220 to 300 px); the last row may stay short. Without JS the CSS flex rows remain. At 320 every photo is cropped to 4:3.
  - **Fixed height:** the grid reserves the height of its tallest page of any year filter, and the pager keeps its line when any filter has two pages, so filtering and paging never move the page.
  - **Visible band:** thin probes down `.gl` (`.gl-pb`, `visibility: hidden`) are watched by IntersectionObserver; their `intersectionRect`s give the part of the gallery inside the top-level viewport, also inside a tall cross-origin iframe where one observer on the whole gallery would stop firing once the gallery is taller than the screen. The viewer's height follows the photo (its ratio plus the caption bar), capped by that band, and it re-centres on each step. While it is open, Tab stays inside it.
  - **`live=True`** (the /gallery page) makes the baked list replaceable at runtime: the page posts `{type: 'ready'}` to `window.parent` (again after 1.5 s and 4 s until a list arrives) and accepts `{type: 'gallery', items: [...]}`. Each item has `src` (a `wix:image://v1/...` URI, a `https://static.wixstatic.com/media/<id>` URL or any https URL) or `media` (a Wix media id), plus `width, height, caption_ko, caption_en, year` and optional `file, alt_ko, alt_en`. Year toggles and pager are rebuilt; captions go in as text; a list with no usable item is ignored. The Velo code for a CMS collection is in `tools/pages/gallery.md`.

**Lists**
- `listing(kind, items, filters=None, per_page=10, sid='')` gives a paginated, filterable list.
  - `kind` is `'pub' | 'report' | 'patent'`. The default filters are pub `('team','year')`, report `('year',)` and patent `('status',)`. Patents can also filter by country: `filters=('status', 'country')` (Korea, USA, China, Europe; items without a country appear under All only). Patent titles carry `lang="ko"`; publication and report titles, authors and journal/event names get `lang="ko"` when they contain Hangul and `lang="en"` otherwise, so screen readers switch voice on both language pages.
  - Years show as the last five years plus `~YYYY` for earlier ones. A filter row with fewer than two options is dropped.
  - A tick ruler shows one tick per item: ticks that match the filter are navy and the rest are grey.
  - The first page is static HTML. JS re-renders on filter or page change. It reserves the height of the tallest page of every filter combination (again on language change, resize and font load), so the list height never changes while paging or filtering. It lays every item out once and adds up item heights per page (one layout per list) instead of rendering each page; rendering each page blocked the first paint for about 0.5 s on Research. The cost: the list reserves the height of its tallest possible page, so a short page shows white space above the pager.
  - The JSON payload is embedded inside the component, so you do not pass `data=` to `page()`.
  - Lab page, team publications: `kit.listing('pub', [p for p in kit.PUBS if p['team'] == 'hearing'], filters=('year',))`.
  - Put filters on lists in content columns, as on the Research page: `sec('Publication', kit.listing('pub', kit.PUBS), 'publication')`.

**Quote, box, map, contact rows** (added for About, Audiso and Contact)
- `quote(text, cite=None, photo=None)` gives a pull quote at reading size (Noto Sans KR 21 px, 17.5 at 320, opening mark hung into the margin) with a cite line led by a 14x2 accent mark; `photo` adds a small greyscale face. `text` and `cite` are `(ko, en)`. A `.prose` (or `rv(prose)`) right after it gets 40 px of space. About: `kit.quote(('“…”', '“…”'), ('서영준 연구소장', 'Director Young Joon Seo'))`.
- `box(body, media='', cls='')` gives a `.box` wash panel; with `media` (a badge or logo img) it becomes a two-column `.bx` panel, media 112 px wide at the left (72 px at 320). White in the media image blends into the wash (`mix-blend-mode: multiply`). After another block in a content column it gets 40 px of space. Audiso: the KOLAS mark and its KC24-437 line.
- `map_embed(src, title, link_href='', link_label=(ko, en))` gives a Google Maps `output=embed` iframe in a 2:1 wash frame (4:3 at 320), lazy-loaded, desaturated to sit with the palette, with a KO/EN accessible name (`title` + swapped `aria-label`) and an optional external link under it. The frame keeps its height whether or not the map loads (offline render shows the wash with a quiet "Google Maps" label).
- `contact_rows(items)` gives mailto rows on the lab-row pattern (`.labs.ct`): lab mark and name, team, then the contact person with a 40 px greyscale face and the email in mono; underlines in the lab colour on hover. `items = [dict(key, name, team=(ko, en), person=(ko, en), email, photo)]`.
- `<div class="m2">` around `fig_cols()` or `ruled()` keeps two columns at 320 (smaller h3 and text). Use it for short, image-led items such as Audiso's products; it saved about 1200 px of mobile height there.

**Small blocks and the document**
- `.box` is a wash panel for a data-center box on a lab page: `'<div class="box">' + ... + '</div>'`. Inside, use a logo `img` with `class="dc-logo"`, or `style="height:56px;width:auto"`.
- `page(title, accent='navy', body='', data=None, hold=None, comment='')` builds the whole document: fonts (with the Hahmlet subset), CSS, the head language script, body, the preview toggle and only the JS modules the body needs.
  - `accent` is a lab key or a CSS colour.
  - `hold` is how many ms to hold reveals of sections already on screen at load: 1700 with the cochlea, 900 otherwise. It is counted from the first animation frame (when the hero animations start), not from when the script starts.
  - `comment` adds a Korean note for the client in the head comment.

## 7. CSS class conventions

- **Layout:** `.wrap` (container), `.sec` (section spacing), `.sg` / `.sg-h` / `.sg-b` (the hanging grid: a 236 px heading column, a 72 px gap, then content), `.sw` / `.sw-head` / `.sw-link` / `.sw-body` (wide section).
- **Text:** `h2`, `h3`, `.note` (small grey text under h2), `.lead`, `.prose`, `.d` (secondary paragraph), `.mono`, `.serif`, `.nw` (no wrap), `.sr` (screen-reader only).
- **Links:** `.more` (text link plus `<i>` arrow), `.btn`, `.btns`, `.mail`.
- **Components:** `.cols.c1-4 > .col` (ruled columns), `.figs` / `.fg` / `.plate` (figure columns), `.rule` (hairline that draws in), `.oc` (outcomes), `.labs` (lab rows), `.faces`, `.ini` (initial tile), `.dcs/.dc`, `.ft` (person feature), `.people/.pc`, `.screen/.playlist/.now` (video), `.gteaser/.gt-row/.gt` (teaser), `.gl/.gl-grid/.gl-it/.gl-view` (gallery), `.tgs/.tg` (text toggles with the 2 px navy active bar), `.pager`, `.ls*` (lists), `.bullets`, `.kv`, `.logos` (`.lg` sized logo), `.box` (`.bx/.bx-m/.bx-b` with media), `.pq` (quote), `.map/.map-l`, `.ct` (contact rows), `.m2` (two columns at 320), `.media`, `.mark`.
- **Colour:** `style="--c:var(--head)"` sets the lab colour on `.labs a`, `.mark` and `.ls-tm`.
- **Stagger index:** `style="--d:N"` (80 ms per step for reveals, 110 ms for the hero load-in).
- **Writing raw HTML:** reuse these classes. Do not add page-local `<style>` unless a component truly does not exist. If it does not, add it to kit.py so every page shares it.

## 8. Motion rules (do not break these)

**Animated properties.** Animate only `transform`, `opacity` and SVG `stroke-dashoffset`. The ease is `var(--ease)` = `cubic-bezier(.22,1,.36,1)`.

**Ambient motion.** There is at most one continuous motion on the whole site: Home's cochlea pulse. It is paused off-screen and when the tab is hidden. Inner pages have none.

**Reveal.**
- Put `data-rv` on a block. Its `.rv` children fade in (opacity only), staggered by `--d`, once the block is 8% visible. `.rv.up` adds a 12 px rise; keep it for images and figures.
- `.rule` hairlines draw with the block.
- A `[data-rv]` block nested inside another one (for example `people_grid(rows=True)` inside a `sec()` body) waits for its own intersection instead of appearing with its parent.
- `sec()` already marks the heading column and the content column. Components mark their own children. A body with no `.rv` inside fades in as a single block.

**Safety nets: content can never stay hidden.**
- Hidden states exist only under `html.js`, which the head script sets. Without JS nothing is hidden.
- If no IntersectionObserver callback arrives within 1.5 s, everything is revealed. If IntersectionObserver is unsupported, everything is revealed at once.
- If the main script never reaches the reveal setup, a CSS-only animation keyed on `html.js:not(.ready)` reveals everything about 2.5 s after first style. If the reveal setup itself throws, `html.rv-all` shows everything.
- The script adds `.ready` right after the reveal setup.

**Hold.** Sections already on screen at load wait (`page(hold=)`), so they follow the hero draw instead of competing with it.

**Outcome ticks.** A paper cover slides away linearly at 11 ms per tick, so 12 finishes almost at once and 120 takes 1.3 s.

**Hover.** Arrows move 4 px. Lab rows underline in their lab colour. Toggles grow their 2 px bar. The play button scales by 1.06. Gallery photos get no zoom.

**prefers-reduced-motion.** Every animation and transition is disabled globally (`*{animation:none!important;transition:none!important}`), everything is visible at once, the cochlea is drawn statically and no pulse runs.

**Page height.** The page height must not change on any interaction: paging, filtering, video play or switch, opening the viewer. Test it as `kit/interact.js` does in the scratchpad.

## 9. Content notes for the client (keep in sync)

- **Videos** are listed in `data/videos.json` (`title_ko, title_en, duration, date, src, poster, thumb`). Add or remove an entry and rebuild. Use the mp4 URL exactly as Wix's "Copy URL" gives it, because only some resolutions exist. The posters are Wix's automatic frames (`f001`, `f002`, `f003`). A designed still uploaded to Wix would be better, especially for the whiteboard intro video.
- **Photos** are listed in `data/gallery.json`. The Home teaser shows the first five; /gallery shows all of them, 12 per page. Once the Velo code in `tools/pages/gallery.md` is on the /gallery page, the CMS collection `Gallery` replaces that list there (the Home teaser still uses `data/gallery.json`).
- **Copy awaiting client approval:**
  - the KO research-area titles (기초 연구 / 빅데이터·인공지능 / 의료기기 / 임상시험);
  - the hero side note on Home ("smilesnail의 ‘snail’, 달팽이관..." and its English), which is designer copy;
  - the shortened English director credentials on Home;
  - the KO page titles and labels added in the final pass: People H1 '구성원' (the Wix menu says 'People'; the other inner pages already use Korean H1s: 연구소 소개, 연구, 갤러리, 연락처), the lab pages' first heading '연구실 소개' / 'About the lab' (the H1 already names the lab), and Audiso's '미션 · 비전' / '미션' / '비전' (as on the lab pages).
- `TECH_TRANSFERS = 12` comes from the round-1 copy, not from data.
- **Iframe heights for every page** (final pass, 2026-10-05; site/*.html). Method: the maximum document height over widths 980, 1280 and 1920 (1100 and 1440 checked too, never taller) and over every list filter and page, gallery year and page, viewer and video switch (`<scratchpad>/fin/hall.js`), plus 24 px, rounded up to 10. Every interaction kept the height exactly constant. Mobile is the same at 320.

  | page | desktop KO / EN | desktop, one height | mobile KO / EN | mobile, one height |
  |---|---|---|---|---|
  | home | 4760 / 5020 | 5020 | 5600 / 5950 | 5950 |
  | about | 3280 / 3350 | 3350 | 3770 / 4000 | 4000 |
  | research | 5950 / 5960 | 5960 | 8650 / 8780 | 8780 |
  | people | 4480 / 4460 | 4480 | 6350 / 6430 | 6430 |
  | basic-lab | 4140 / 4190 | 4190 | 5300 / 5560 | 5560 |
  | hearing-lab | 5150 / 5320 | 5320 | 6460 / 6880 | 6880 |
  | head-lab | 5310 / 5380 | 5380 | 6840 / 7180 | 7180 |
  | audiso | 3290 / 3400 | 3400 | 4410 / 4410 | 4410 |
  | contact | 1690 / 1720 | 1720 | 1650 / 1710 | 1710 |
  | gallery | 1980 / 1970 | 1980 | 1700 / 1740 | 1740 |

  - Desktop is tallest at 980 for most pages (narrower columns). People is tallest at 1280 and up (the portraits grow with the column).
  - Lists reserve the height of their tallest page, so they grow only when data/*.json gains a longer page; re-measure after large data updates. A People team grows by one row (about 330 px desktop, 270 px mobile) each time its count passes a multiple of 4 (2 on mobile); lab alumni add a row every 6 on desktop and about 96 px per person on mobile.
  - Gallery fed from the CMS: a full page of 12 photos needs up to 2750 desktop and 2350 mobile, and 13 or more add the pager line: 2820 desktop, 2420 mobile (details in `tools/pages/gallery.md`).
- **About gallery:** the old small Pro Gallery at the bottom of /about is replaced by the same teaser as Home (first five photos of data/gallery.json, linking to /gallery). The Pro Gallery element can be deleted from /about once /gallery is live, unless /gallery reads it through the backend API (see REVIEW notes), in which case keep it collapsed there.
- **Partner logos:** the ILIAS Biologics file is outline lettering (thin grey strokes, transparent fill), so on white it reads light; it is drawn with a thin dark edge to hold its weight. A solid dark-on-light version from ILIAS would be better. NCSRD and ILIAS are the only PNGs with transparency, so they are served as the original files; every other logo wider than 640 px uses imgur's 640 px copy (imgur thumbnails flatten transparency onto black).
