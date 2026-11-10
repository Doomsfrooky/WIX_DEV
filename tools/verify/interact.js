#!/usr/bin/env node
// Height stability: click every control (filters, pager, gallery photos and viewer, video playlist, jump links)
// and check that the document height never changes.
//   node tools/verify/interact.js site/research.html [--width 1280] [--lang en]
'use strict';
const V = require('./lib');
(async () => {
  const [target] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !(all[i - 1] || '').startsWith('--'));
  const w = +V.arg('width', 1280);
  const b = await V.launch();
  const p = await V.newPage(b, { width: w, height: w <= 400 ? 560 : 800 });
  await p.goto(V.withLang(await V.urlFor(target), V.arg('lang')), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(1200);
  const H = () => p.evaluate(() => document.documentElement.scrollHeight);
  const h0 = await H();
  const n = await p.evaluate(() => {
    const els = [...document.querySelectorAll('button, [role="button"], [role="tab"], .gl-it, .gl-it a, [data-y], [data-pg]')].filter((e) => !e.closest('.lang-toggle'));
    els.forEach((e, i) => e.setAttribute('data-vi', i)); return els.length;
  });
  const changes = [];
  for (let i = 0; i < n; i++) {
    const loc = p.locator(`[data-vi="${i}"]`);
    if (!(await loc.isVisible().catch(() => false))) continue;
    const label = (await loc.evaluate((e) => (e.getAttribute('aria-label') || e.textContent || e.className).trim().slice(0, 40)));
    await loc.click({ timeout: 2000 }).catch(() => {});
    await p.waitForTimeout(250);
    const h = await H();
    if (h !== h0) changes.push({ control: label, before: h0, after: h });
    await p.keyboard.press('Escape'); await p.waitForTimeout(80);
  }
  console.log(JSON.stringify({ page: target, width: w, controls: n, height: h0, changes, errors: p.log.errors }, null, 1));
  if (changes.length || p.log.errors.length) process.exitCode = 1;
  await b.close(); await V.stop();
})();
