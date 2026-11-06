#!/usr/bin/env node
// Content must never stay hidden. Three runs, each must end with stillInvisible = 0:
//   nojs     JavaScript disabled
//   broken   the page's last <script> (the main script) removed, as if it failed to load or threw at once
//   reduced  prefers-reduced-motion: everything visible at once, no running animations after 300 ms
//   node tools/verify/fallback.js site/home.html [--width 320] [--out dir]
'use strict';
const V = require('./lib');
(async () => {
  const [target] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const w = +V.arg('width', 1280), out = V.arg('out');
  const url = await V.urlFor(target);
  const b = await V.launch();
  const res = {};
  for (const mode of ['nojs', 'broken', 'reduced']) {
    const p = await V.newPage(b, { width: w, height: w <= 400 ? 560 : 800, js: mode !== 'nojs', reduced: mode === 'reduced' });
    if (mode === 'broken') {
      await p.route(url.split('?')[0] + '*', async (route) => {
        const r = await route.fetch(); let body = await r.text();
        const i = body.lastIndexOf('<script>'); const j = body.indexOf('</script>', i);
        if (i > body.indexOf('</head>')) body = body.slice(0, i) + body.slice(j + 9);
        route.fulfill({ response: r, body });
      });
    }
    await p.goto(url, { waitUntil: 'load' });
    await p.waitForTimeout(mode === 'reduced' ? 300 : 3200);
    const running = mode === 'nojs' ? 0 : await p.evaluate(() => document.getAnimations().filter((a) => a.playState === 'running' && !(a.effect && a.effect.getTiming().iterations === Infinity && 0)).length);
    // whole page, no scrolling: hidden content must still show (the fallbacks are timed, not scroll-driven)
    const a = await p.evaluate(V.AUDIT);
    if (out) { V.outDir(out); await p.screenshot({ path: `${out}/${w}-${mode}.png`, fullPage: true }); }
    res[mode] = { stillInvisible: a.stillInvisible.length, sample: a.stillInvisible.slice(0, 6), runningAnimations: running, errors: p.log.errors.slice(0, 5) };
    await p.ctx.close();
  }
  console.log(JSON.stringify({ page: target, width: w, ...res }, null, 1));
  if (Object.values(res).some((r) => r.stillInvisible) || res.reduced.runningAnimations) process.exitCode = 1;
  await b.close(); await V.stop();
})();
