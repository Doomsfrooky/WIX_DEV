#!/usr/bin/env node
// One screenshot, optionally cropped to an element.
//   node tools/verify/shoot.js <page> <out.png> [--width 1280] [--height 800] [--lang en] [--sel ".labs"] [--wait 1500] [--scale 2] [--full]
'use strict';
const V = require('./lib');
(async () => {
  const [target, out] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const w = +V.arg('width', 1280), h = +V.arg('height', w <= 400 ? 560 : 800);
  const b = await V.launch();
  const p = await V.newPage(b, { width: w, height: h, scale: +V.arg('scale', 1) });
  await p.goto(V.withLang(await V.urlFor(target), V.arg('lang')), { waitUntil: 'load' });
  const sel = V.arg('sel');
  if (sel) { await p.locator(sel).first().scrollIntoViewIfNeeded(); }
  await p.waitForTimeout(+V.arg('wait', 1500));
  if (sel) await p.locator(sel).first().screenshot({ path: out });
  else await p.screenshot({ path: out, fullPage: V.flag('full') });
  console.log(out, p.log.errors.length ? p.log.errors : '');
  await b.close(); await V.stop();
})();
