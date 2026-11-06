#!/usr/bin/env node
// Evaluate a JS expression in the page after load and print the JSON result.
//   node tools/verify/probe.js <page> "document.querySelectorAll('.rv').length" [--width 320] [--lang en] [--wait 1500]
'use strict';
const V = require('./lib');
(async () => {
  const [target, expr] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const w = +V.arg('width', 1280);
  const b = await V.launch();
  const p = await V.newPage(b, { width: w, height: w <= 400 ? 560 : 800 });
  await p.goto(V.withLang(await V.urlFor(target), V.arg('lang')), { waitUntil: 'load' });
  await p.waitForTimeout(+V.arg('wait', 1500));
  const r = await p.evaluate((src) => { try { return (0, eval)(src); } catch (e) { return 'ERROR ' + e.message; } }, expr);
  console.log(JSON.stringify({ result: r, errors: p.log.errors }, null, 1));
  await b.close(); await V.stop();
})();
