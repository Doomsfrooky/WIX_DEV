# tools/kits: round-3 design directions

One file (plus an optional folder of hero assets) per direction. **The kits share no design parts**: each has its own
tokens, type, markup, CSS and motion. What they share is design-free and lives in `tools/core.py`: copy, data, `t()`,
links, the runtime (`window.RIHE`: language, safe reveals, the sentinel band, jumps, the headless list engine) and the
page shell. `python3 tools/directions.py [a b c]` writes `site/_directions/<key>.html`.

```
tools/kits/a.py         render() -> whole document via core.page_shell(..., prefix='../', robots='noindex', lang_toggle=True)
tools/kits/a/           hero.html, hero.css, hero.js, fonts.txt (the synthesized /67 first screen, copied from site/_directions/_67/a/final/)
site/_directions/a.design.md   the direction's design document (tokens, type, grid, components, motion spec, verification)
```

## What a direction page contains (the same content in every direction)

1. **Home, first screen**: the /67 final hero. Then a short **outcomes** band: `core.OUTCOMES` with a count-up.
2. `core.sample_mark('Research 페이지 일부', 'Part of the Research page')`, then **Research**: `core.RESEARCH_TITLE`,
   `core.RESEARCH_LEAD`, and the **publication list**: all of `core.PUBS`, filters team (`core.pub_teams`,
   labels `core.TEAM_LABEL`) and year (`core.pub_years`, '~YYYY' means that year and earlier), 10 per page,
   first page as static HTML, then `RIHE.list(el, {data, size: 10, render, empty, after})` (fixed height: paging and
   filtering never change the page height). Titles/authors/journal get `core.lang_attr(...)`. Reading zone: calm.
3. `core.sample_mark('People 페이지 일부', 'Part of the People page')`, then **People**: `core.PEOPLE_TITLE`,
   `core.PEOPLE_LEAD`, the faculty (`core.TEAMS['faculty']`) and one lab team (`core.TEAMS['head']`, HeAD Lab),
   names via `core.name_pair`, roles via `core.member_role`, portraits from the data (imgur, keep the URL case),
   a member without a photo gets an initial tile (`core.initials`). Reading zone: calm.

No other sections, no invented copy. Lab names stay in Latin in both languages.

## Motion contract

- GSAP 3.15.0 from `site/vendor` (`vendor=('gsap', 'split', ...)` in `page_shell`). SplitText for line/character
  reveals (split only the visible language, after `document.fonts.ready`; re-split on `RIHE.onLang` if needed).
- Reveal-hidden elements: `[data-a]` blocks / `[data-ai]` items, hidden only under `html.js:not(.rm)`, made visible
  with `.on`. Trigger with `RIHE.inview(el, fn, {threshold})` (threshold-only: rootMargin is ignored in the Wix iframe).
  Call `RIHE.motionReady()` first thing; if `window.gsap` is missing call `RIHE.showAll()` and stop.
- Scroll-linked motion (parallax, scrubbed reveals) only through `RIHE.onBand` + `RIHE.rect` + `RIHE.progress`.
- Count-up for outcomes, hover micro-reactions, smooth in-page jumps (`<a href="#id">` is handled by the runtime).
- `html.rm` (prefers-reduced-motion): final state at once, nothing moves (the client's rule; it overrides the
  impeccable guidance that reduced motion may keep gentle motion).
- Pause loops/WebGL/video off-screen (`RIHE.visible`) and when the tab is hidden.
- Never: vh/svh/dvh/innerHeight, position fixed/sticky, wheel/touch preventDefault, window-scroll ScrollTrigger.

## Verify (all must pass)

```
python3 tools/directions.py a
node tools/verify/wixsim.js site/_directions/a.html <out> --w 1280   (and --w 320, and --lang en)
node tools/verify/render.js site/_directions/a.html <out> --widths 1920,1440,980,320 --langs ko,en --frames
node tools/verify/interact.js site/_directions/a.html   (and --width 320): height never changes
node tools/verify/fallback.js site/_directions/a.html   (and --width 320)
.claude/skills/impeccable/scripts/impeccable detect --json site/_directions/a.html
```
