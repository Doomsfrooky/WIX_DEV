#!/usr/bin/env node
// Document height at each width and language (what the Wix element height must cover).
//   node tools/verify/heights.js site/home.html [site/about.html ...] [--widths 320,980,1100,1280,1440,1920] [--sweep 20] [--fine [step]] [--md]
// Desktop height = max over the desktop widths; mobile = 320; '980' = the desktop height when the Wix element stays
// 980 wide. The table adds 24 px and rounds up to 10. --sweep N measures every N px from 980 to 1920 instead of the
// listed desktop widths (justified photo rows, as on /gallery, can peak between the usual widths).
// --fine [step] (the values for docs/wix-heights.md): one load per page, then the viewport is resized from 980 to 1920
// every <step> px (default 1) and the height is read once it is stable; the highest widths are refined to 1 px and
// measured again with fresh loads in both languages, with 320 and 980; the desktop value is the larger of the two.
// The five usual widths missed peaks of up to 67 px (2026-11-10): content that stops growing at the 1640 px cap
// (about 1700), the two-column breakpoint below 1100 (Audiso, 58 px), and justified photo rows (gallery, 67 px;
// --sweep 20 still missed 29 px). The resize pass
// reads KO only: every page reserves the larger language's height per section, and the fresh loads check both.
'use strict';
const V = require('./lib');

async function resizeSweep(b, url, widths) {
  const p = await V.newPage(b, { width: widths[0], height: 800 });
  await p.goto(url, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(1500);
  const H = () => p.evaluate(() => Math.ceil(document.documentElement.getBoundingClientRect().height));
  const out = {};
  for (const w of widths) {
    await p.setViewportSize({ width: w, height: 800 });
    await p.waitForTimeout(420);                     // the kit's resize handlers settle within 260 ms
    let h = await H();
    for (let n = 0; n < 10; n++) { await p.waitForTimeout(120); const h2 = await H(); if (h2 === h) break; h = h2; }
    out[w] = h;
  }
  await p.ctx.close();
  return out;
}

async function fresh(b, base, lang, w) {
  const p = await V.newPage(b, { width: w, height: 800 });
  await p.goto(V.withLang(base, lang), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(800);
  const h = await p.evaluate(() => Math.ceil(document.documentElement.getBoundingClientRect().height));
  await p.ctx.close();
  return h;
}

(async () => {
  const pages = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--')
    && !((all[i - 1] === '--fine') && /^\d+$/.test(a)));
  let widths = V.arg('widths', '320,980,1100,1280,1440,1920').split(',').map(Number);
  const sweep = +V.arg('sweep', 0);
  const fi = process.argv.indexOf('--fine');
  const fine = fi < 0 ? 0 : (/^\d+$/.test(process.argv[fi + 1] || '') ? +process.argv[fi + 1] : 1);
  if (sweep > 0) { widths = [320]; for (let x = 980; x <= 1920; x += sweep) widths.push(x); if (widths[widths.length - 1] !== 1920) widths.push(1920); }
  const b = await V.launch();
  const rows = [];
  const pad = (x) => Math.ceil((x + 24) / 10) * 10;
  for (const pg of pages) {
    const base = await V.urlFor(pg);
    const r = { page: pg, h: {} };
    let ws = widths;
    if (fine) {
      const list = []; for (let x = 980; x <= 1920; x += fine) list.push(x); if (list[list.length - 1] !== 1920) list.push(1920);
      const sw = await resizeSweep(b, V.withLang(base, 'ko'), list);
      const top = Object.keys(sw).map(Number).sort((a, c) => sw[c] - sw[a]).slice(0, 6);
      const near = [];
      for (const w of top) for (let d = -(fine - 1); d <= fine - 1; d++) if (d && w + d >= 980 && w + d <= 1920 && !(w + d in sw)) near.push(w + d);
      if (near.length) Object.assign(sw, await resizeSweep(b, V.withLang(base, 'ko'), [...new Set(near)].sort((a, c) => a - c)));
      r.sweep = sw;
      const best = Object.keys(sw).map(Number).sort((a, c) => sw[c] - sw[a]);
      ws = [...new Set([320, 980, ...best.slice(0, 3), 1920])];
    }
    for (const lang of ['ko', 'en']) for (const w of ws) r.h[`${lang}@${w}`] = await fresh(b, base, lang, w);
    const deskW = ws.filter((w) => w >= 980);
    const sweepMax = r.sweep ? Math.max(...Object.values(r.sweep)) : 0;
    const desk = (l) => Math.max(sweepMax, ...deskW.map((w) => r.h[`${l}@${w}`] || 0));
    r.desktop = { ko: pad(desk('ko')), en: pad(desk('en')) }; r.mobile = { ko: pad(r.h['ko@320'] || 0), en: pad(r.h['en@320'] || 0) };
    r.w980 = pad(Math.max(r.h['ko@980'] || 0, r.h['en@980'] || 0, (r.sweep && r.sweep[980]) || 0));
    const at = (l) => {
      const all = Object.assign({}, r.sweep || {}); for (const w of deskW) all[w] = Math.max(all[w] || 0, r.h[`${l}@${w}`] || 0);
      return Object.keys(all).map(Number).reduce((a, w) => (all[w] > (all[a] || 0) ? w : a), 980);
    };
    r.peak = { ko: at('ko'), en: at('en') };
    if (r.sweep) { r.sweepMax = sweepMax; delete r.sweep; }
    rows.push(r);
    if (fine) console.error(`${pg}: desktop ${Math.max(r.desktop.ko, r.desktop.en)} (raw ${Math.max(desk('ko'), desk('en'))} at ${r.peak.ko}), 980 ${r.w980}, mobile ${Math.max(r.mobile.ko, r.mobile.en)}`);
  }
  await b.close(); await V.stop();
  if (V.flag('md')) {
    console.log('| page | desktop KO / EN | desktop | 980 | mobile KO / EN | mobile | widest at |\n|---|---|---|---|---|---|---|');
    for (const r of rows) console.log(`| ${r.page} | ${r.desktop.ko} / ${r.desktop.en} | ${Math.max(r.desktop.ko, r.desktop.en)} | ${r.w980} | ${r.mobile.ko} / ${r.mobile.en} | ${Math.max(r.mobile.ko, r.mobile.en)} | ${r.peak.ko} / ${r.peak.en} |`);
  } else console.log(JSON.stringify(rows, null, 1));
})();
