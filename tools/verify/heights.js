#!/usr/bin/env node
// Document height at each width and language (what the Wix element height must cover).
//   node tools/verify/heights.js site/home.html [site/about.html ...] [--widths 320,980,1100,1280,1440,1920] [--md]
// Desktop height = max over the desktop widths; mobile = 320. The table adds 24 px and rounds up to 10.
'use strict';
const V = require('./lib');
(async () => {
  const pages = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const widths = V.arg('widths', '320,980,1100,1280,1440,1920').split(',').map(Number);
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
    rows.push(r);
  }
  await b.close(); await V.stop();
  if (V.flag('md')) {
    console.log('| page | desktop KO / EN | desktop | mobile KO / EN | mobile |\n|---|---|---|---|---|');
    for (const r of rows) console.log(`| ${r.page} | ${r.desktop.ko} / ${r.desktop.en} | ${Math.max(r.desktop.ko, r.desktop.en)} | ${r.mobile.ko} / ${r.mobile.en} | ${Math.max(r.mobile.ko, r.mobile.en)} |`);
  } else console.log(JSON.stringify(rows, null, 1));
})();
