#!/usr/bin/env node
// Run a page the way Wix shows it: tools/wix-sim.html on http://localhost:8001 with the page in a fixed-height,
// non-scrolling iframe from http://127.0.0.1:8002 (a different origin, as smilesnail.org vs github.io).
// The outer page is scrolled top to bottom; then every element inside the iframe must have been revealed.
//   node tools/verify/wixsim.js site/home.html <outdir> [--w 1280|320] [--lang en] [--step 140] [--shots 6] [--h 6000]
//   node tools/verify/wixsim.js https://rawcdn.githack.com/.../site/home.html <outdir>   (inner from the web)
// Output JSON: crossOrigin (must be true), stillInvisible (must be 0), errors, iframe height,
// band accuracy if the page exposes RIHE.band ({top, bottom} in document px): max error against the true visible band.
// PNGs: t0000..t2500 (first screen over time), s01..sNN (screens down the page while scrolling).
'use strict';
const V = require('./lib');
(async () => {
  const [target, out = 'wixsim-out'] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const w = +V.arg('w', 1280), mobile = w === 320, lang = V.arg('lang');
  V.outDir(out);
  await V.serve(V.OUTER);
  const inner = V.withLang(await V.urlFor(target, V.INNER), lang);
  const b = await V.launch();
  // the Wix element has a fixed height: measure the page on its own first (as docs/wix-heights.md does), unless --h is given
  let h = +V.arg('h', 0);
  if (!h) {
    const m = await V.newPage(b, { width: mobile ? 320 : w, height: 800 });
    await m.goto(inner, { waitUntil: 'load' }); await m.evaluate(() => document.fonts && document.fonts.ready); await m.waitForTimeout(600);
    h = await m.evaluate(() => Math.ceil(document.documentElement.getBoundingClientRect().height)); await m.ctx.close();
  }
  const outer = `http://localhost:${V.OUTER}/tools/wix-sim.html?hud=0&w=${mobile ? 320 : ''}&h=${h}&src=${encodeURIComponent(inner)}`;
  const p = await V.newPage(b, mobile ? { width: 320, height: 693 } : { width: w, height: 900 });
  const t0 = Date.now();
  await p.goto(outer, { waitUntil: 'load', timeout: 60000 });
  const fr = p.frames().find((f) => f !== p.mainFrame());
  if (!fr) { console.error('no iframe'); process.exit(1); }
  await fr.waitForLoadState('load');
  for (const ms of [0, 300, 700, 1200, 1800, 2500]) {
    const wait = ms - (Date.now() - t0); if (wait > 0) await p.waitForTimeout(wait);
    await p.screenshot({ path: `${out}/t${String(ms).padStart(4, '0')}.png` });
  }
  const crossOrigin = await fr.evaluate(() => { try { void window.top.location.href; return false; } catch (e) { return true; } });
  await p.waitForTimeout(300);
  const total = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  const step = +V.arg('step', 140), shots = +V.arg('shots', 6);
  let shot = 0, nextShot = 0, bandErr = null, bandSamples = 0;
  for (let y = 0; y <= total; y += step) {
    await p.evaluate((v) => window.scrollTo(0, v), y);
    await p.waitForTimeout(70);
    const truth = await p.evaluate(() => { const r = window.SIM.iframe.getBoundingClientRect(); return { top: Math.max(0, -r.top), bottom: Math.min(r.height, innerHeight - r.top) }; });
    const est = await fr.evaluate(() => (window.RIHE && window.RIHE.band) ? { top: window.RIHE.band.top, bottom: window.RIHE.band.bottom } : null).catch(() => null);
    if (est && truth.bottom > truth.top) { const e = Math.max(Math.abs(est.top - truth.top), Math.abs(est.bottom - truth.bottom)); bandErr = Math.max(bandErr || 0, e); bandSamples++; }
    if (y >= nextShot && shot < shots) { shot++; await p.screenshot({ path: `${out}/s${String(shot).padStart(2, '0')}.png` }); nextShot += total / Math.max(1, shots - 1); }
  }
  await p.waitForTimeout(1500);
  const a = await fr.evaluate(V.AUDIT);
  const res = { page: target, mode: mobile ? '320 mobile' : `${w} desktop`, outer, crossOrigin, iframeHeight: h, docHeight: a.height,
    stillInvisible: a.stillInvisible.length, sample: a.stillInvisible.slice(0, 8), brokenImages: a.brokenImages,
    band: bandSamples ? { samples: bandSamples, maxErrorPx: Math.round(bandErr * 10) / 10 } : 'page has no RIHE.band',
    errors: p.log.errors.concat(p.log.failed).slice(0, 10) };
  console.log(JSON.stringify(res, null, 1));
  if (!crossOrigin || res.stillInvisible || res.errors.length) process.exitCode = 1;
  await b.close(); await V.stop();
})();
