#!/usr/bin/env node
// Render a page at 1280 and 320, KO and EN, full-page PNGs plus an audit.
//   node tools/verify/render.js site/home.html <outdir> [--frames] [--widths 1280,320] [--langs ko,en]
// --frames also saves the first screen over time (0..2500 ms) at each width, to judge the load-in motion.
// Prints JSON: per shot stillInvisible / brokenImages / errors (all must be 0), height, missing mirror URLs.
'use strict';
const V = require('./lib');
(async () => {
  const [target, out = 'render-out'] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !['--widths', '--langs'].includes(all[i - 1]));
  if (!target) { console.error('usage: render.js <page> <outdir> [--frames]'); process.exit(2); }
  V.outDir(out);
  const widths = (V.arg('widths', '1280,320')).split(',').map(Number);
  const langs = V.arg('langs', 'ko,en').split(',');
  const base = await V.urlFor(target);
  const b = await V.launch();
  const report = [];
  for (const w of widths) for (const lang of langs) {
    const p = await V.newPage(b, { width: w, height: w <= 400 ? 560 : 800 });
    const u = V.withLang(base, lang);
    const t0 = Date.now();
    await p.goto(u, { waitUntil: 'load', timeout: 60000 });
    if (V.flag('frames')) {
      for (const ms of [0, 300, 700, 1200, 1800, 2500]) {
        const wait = ms - (Date.now() - t0); if (wait > 0) await p.waitForTimeout(wait);
        await p.screenshot({ path: `${out}/${w}-${lang}-t${String(ms).padStart(4, '0')}.png` });
      }
    }
    await p.evaluate(() => document.fonts && document.fonts.ready);
    await V.scrollThrough(p);
    await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
    const a = await p.evaluate(V.AUDIT);
    await p.screenshot({ path: `${out}/${w}-${lang}.png`, fullPage: true });
    report.push({ shot: `${w}-${lang}`, height: a.height, stillInvisible: a.stillInvisible.length, brokenImages: a.brokenImages.length, errors: p.log.errors.length + p.log.failed.length,
      detail: { stillInvisible: a.stillInvisible.slice(0, 10), brokenImages: a.brokenImages, errors: p.log.errors.concat(p.log.failed).slice(0, 10) }, notInMirror: p.log.missing });
    await p.ctx.close();
  }
  await b.close(); await V.stop();
  console.log(JSON.stringify(report, null, 1));
  if (report.some((r) => r.stillInvisible || r.brokenImages || r.errors)) process.exitCode = 1;
})();
