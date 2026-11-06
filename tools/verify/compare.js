#!/usr/bin/env node
// Side-by-side comparison sheet: each page in a column, one row per width (first screen + whole page thumbnails).
//   node tools/verify/compare.js site/_directions/a.html site/_directions/b.html site/_directions/c.html <out> [--widths 980,1440,320] [--lang ko]
// Writes <out>/<name>-<width>-first.png, <name>-<width>-full.png and <out>/compare-first.png, compare-full.png.
'use strict';
const fs = require('fs');
const path = require('path');
const V = require('./lib');
(async () => {
  const pos = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const out = pos.pop(); const pages = pos;
  const widths = V.arg('widths', '980,1440,320').split(',').map(Number);
  const lang = V.arg('lang', 'ko');
  V.outDir(out);
  const b = await V.launch();
  const shots = {};
  for (const pg of pages) {
    const name = path.basename(pg, '.html');
    for (const w of widths) {
      const p = await V.newPage(b, { width: w, height: w <= 400 ? 560 : 800, scale: w <= 400 ? 2 : 1 });
      await p.goto(V.withLang(await V.urlFor(pg), lang), { waitUntil: 'load' });
      await p.evaluate(() => document.fonts && document.fonts.ready);
      await p.waitForTimeout(3200);   // let the load-in finish
      await p.screenshot({ path: `${out}/${name}-${w}-first.png` });
      await V.scrollThrough(p, 400, 50);
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400);
      await p.screenshot({ path: `${out}/${name}-${w}-full.png`, fullPage: true });
      shots[`${name}-${w}`] = true;
      await p.ctx.close();
    }
  }
  // compose with a plain HTML grid
  for (const kind of ['first', 'full']) {
    const cols = pages.map((pg) => path.basename(pg, '.html'));
    const cell = (n, w) => `<td><img src="file://${path.resolve(out, `${n}-${w}-${kind}.png`)}" style="width:${kind === 'first' ? (w <= 400 ? 220 : 560) : (w <= 400 ? 120 : 300)}px"></td>`;
    const html = `<html><body style="margin:0;padding:16px;background:#eceef1;font:600 14px system-ui">
<table style="border-spacing:14px"><tr><td></td>${cols.map((c) => `<td style="font-size:18px">${c.toUpperCase()}</td>`).join('')}</tr>
${widths.map((w) => `<tr><td style="vertical-align:top">${w}px</td>${cols.map((c) => cell(c, w)).join('')}</tr>`).join('')}</table></body></html>`;
    const f = path.resolve(out, `compare-${kind}.html`); fs.writeFileSync(f, html);
    const p = await V.newPage(b, { width: 1800, height: 1000 });
    await p.goto('file://' + f); await p.waitForTimeout(500);
    await p.screenshot({ path: `${out}/compare-${kind}.png`, fullPage: true });
    await p.ctx.close();
  }
  await b.close(); await V.stop();
  console.log(JSON.stringify({ out, pages, widths, sheets: ['compare-first.png', 'compare-full.png'] }));
})();
