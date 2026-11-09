#!/usr/bin/env node
// Document height at each width and language (what the Wix element height must cover).
//   node tools/verify/heights.js site/home.html [site/about.html ...] [--widths 320,980,1100,1280,1440,1920] [--sweep 20] [--md]
// Desktop height = max over the desktop widths; mobile = 320; '980' = the desktop height when the Wix element stays
// 980 wide. The table adds 24 px and rounds up to 10. --sweep N measures every N px from 980 to 1920 instead of the
// listed desktop widths (justified photo rows, as on /gallery, can peak between the usual widths).
'use strict';
const V = require('./lib');
(async () => {
  const pages = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  let widths = V.arg('widths', '320,980,1100,1280,1440,1920').split(',').map(Number);
  const sweep = +V.arg('sweep', 0);
  if (sweep > 0) { widths = [320]; for (let x = 980; x <= 1920; x += sweep) widths.push(x); if (widths[widths.length - 1] !== 1920) widths.push(1920); }
  const b = await V.launch();
  const rows = [];
  for (const pg of pages) {
    const base = await V.urlFor(pg);
    const r = { page: pg, h: {} };
    for (const lang of ['ko', 'en']) for (const w of widths) {
      const p = await V.newPage(b, { width: w, height: 800 });
      await p.goto(V.withLang(base, lang), { waitUntil: 'load' });
      await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(800);
      r.h[`${lang}@${w}`] = await p.evaluate(() => Math.ceil(document.documentElement.getBoundingClientRect().height));
      await p.ctx.close();
    }
    const pad = (x) => Math.ceil((x + 24) / 10) * 10;
    const desk = (l) => Math.max(...widths.filter((w) => w >= 980).map((w) => r.h[`${l}@${w}`] || 0));
    r.desktop = { ko: pad(desk('ko')), en: pad(desk('en')) }; r.mobile = { ko: pad(r.h['ko@320'] || 0), en: pad(r.h['en@320'] || 0) };
    r.w980 = pad(Math.max(r.h['ko@980'] || 0, r.h['en@980'] || 0));
    const at = (l) => widths.filter((w) => w >= 980).reduce((a, w) => ((r.h[`${l}@${w}`] || 0) > (r.h[`${l}@${a}`] || 0) ? w : a), 980);
    r.peak = { ko: at('ko'), en: at('en') };
    rows.push(r);
  }
  await b.close(); await V.stop();
  if (V.flag('md')) {
    console.log('| page | desktop KO / EN | desktop | 980 | mobile KO / EN | mobile | widest at |\n|---|---|---|---|---|---|---|');
    for (const r of rows) console.log(`| ${r.page} | ${r.desktop.ko} / ${r.desktop.en} | ${Math.max(r.desktop.ko, r.desktop.en)} | ${r.w980} | ${r.mobile.ko} / ${r.mobile.en} | ${Math.max(r.mobile.ko, r.mobile.en)} | ${r.peak.ko} / ${r.peak.en} |`);
  } else console.log(JSON.stringify(rows, null, 1));
})();
