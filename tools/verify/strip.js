#!/usr/bin/env node
// Filmstrip: lay time-ordered frames side by side with their labels (for showing motion in a report).
//   node tools/verify/strip.js <out.png> <frame1.png> <frame2.png> ... [--width 300] [--cols 6] [--title "A · 1280"]
// Labels come from the file names (t0300 -> 0.3 s, s02 -> scroll 2).
'use strict';
const fs = require('fs');
const path = require('path');
const V = require('./lib');
(async () => {
  const pos = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const out = pos.shift(); const frames = pos;
  const w = +V.arg('width', 300), cols = +V.arg('cols', Math.min(6, frames.length)), title = V.arg('title', '');
  const label = (f) => { const b = path.basename(f, '.png'); const m = /t(\d{4})/.exec(b); if (m) return (+m[1] / 1000).toFixed(1) + ' s'; const s = /s(\d\d)/.exec(b); return s ? 'scroll ' + (+s[1]) : b; };
  const cells = frames.map((f) => `<td style="vertical-align:top"><img src="file://${path.resolve(f)}" style="width:${w}px;display:block;border:1px solid #d5d8dd"><div style="margin-top:6px">${label(f)}</div></td>`);
  const rows = []; for (let i = 0; i < cells.length; i += cols) rows.push('<tr>' + cells.slice(i, i + cols).join('') + '</tr>');
  const html = `<html><body style="margin:0;padding:14px;background:#f1f2f4;font:600 13px system-ui;color:#333">${title ? `<div style="font-size:16px;margin:0 0 10px 4px">${title}</div>` : ''}<table style="border-spacing:10px">${rows.join('')}</table></body></html>`;
  const tmp = out.replace(/\.png$/, '.html'); fs.writeFileSync(tmp, html);
  const b = await V.launch(); const p = await V.newPage(b, { width: Math.min(2400, cols * (w + 24) + 40), height: 400 });
  await p.goto('file://' + path.resolve(tmp)); await p.waitForTimeout(300);
  await p.screenshot({ path: out, fullPage: true }); await b.close(); fs.unlinkSync(tmp);
  console.log(out);
})();
