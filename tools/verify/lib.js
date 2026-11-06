// Shared helpers for the verification scripts in tools/verify/. Node + the pre-installed Playwright.
//   const V = require('./lib');
// Targets: a path under the repo (site/home.html), an absolute path, or an http(s) URL.
// Pages are served over http from two local servers so cross-origin tests are real:
//   http://localhost:8001  (outer: tools/wix-sim.html)    http://127.0.0.1:8002  (inner: site pages)
// Set MIRROR=1 to answer external requests from tools/verify/.mirror (see mirror.py); misses are listed.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..');
const MIRROR_DIR = path.join(__dirname, '.mirror');
const OUTER = 8001, INNER = 8002;

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.woff2': 'font/woff2', '.mp4': 'video/mp4', '.md': 'text/plain; charset=utf-8' };

const servers = {};
function serve(port) {
  if (servers[port]) return servers[port];
  servers[port] = new Promise((resolve, reject) => {
    const s = http.createServer((req, res) => {
      const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      let f = path.join(ROOT, u);
      if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
      if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) { res.writeHead(404); return res.end('404'); }
      res.writeHead(200, { 'content-type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream', 'cache-control': 'no-store', 'access-control-allow-origin': '*' });
      fs.createReadStream(f).pipe(res);
    });
    s.on('error', (e) => (e.code === 'EADDRINUSE' ? resolve(null) : reject(e)));   // someone (another run) already serves the repo there
    s.listen(port, () => resolve(s));
  });
  return servers[port];
}
async function stop() { for (const p of Object.keys(servers)) { const s = await servers[p]; if (s) s.close(); delete servers[p]; } }

// repo path or URL -> URL served by the inner origin (127.0.0.1:8002)
async function urlFor(target, port = INNER) {
  if (/^https?:\/\//.test(target)) return target;
  await serve(port);
  const abs = path.resolve(ROOT, target);
  const host = port === OUTER ? 'localhost' : '127.0.0.1';
  return `http://${host}:${port}/` + path.relative(ROOT, abs).split(path.sep).map(encodeURIComponent).join('/');
}
function withLang(u, lang) { if (!lang) return u; const x = new URL(u); x.searchParams.set('lang', lang); return x.toString(); }

function mirrorName(url) {
  const clean = url.replace(/^https?:\/\//, '').replace(/[?#].*$/, '');
  const q = url.includes('?') ? '_' + crypto.createHash('sha1').update(url).digest('hex').slice(0, 12) : '';
  let name = clean.replace(/[^A-Za-z0-9._-]+/g, '_');
  if (name.length > 120) name = name.slice(0, 60) + '_' + crypto.createHash('sha1').update(clean).digest('hex').slice(0, 16);
  return name + q;
}

async function launch(opts = {}) {
  const browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required', '--enable-unsafe-swiftshader'] });
  return browser;
}

// new page with error collection; device: 'desktop' | 'mobile' | {width,height}
async function newPage(browser, { width = 1280, height = 800, reduced = false, js = true, scale = 1, mobile = false } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: scale, javaScriptEnabled: js,
    reducedMotion: reduced ? 'reduce' : 'no-preference', isMobile: mobile, hasTouch: mobile });
  const page = await ctx.newPage();
  const log = { errors: [], failed: [], missing: [] };
  page.on('pageerror', (e) => log.errors.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') log.errors.push('console: ' + m.text().slice(0, 300)); });
  page.on('requestfailed', (r) => { const t = r.failure() && r.failure().errorText; if (t !== 'net::ERR_ABORTED') log.failed.push(r.url().slice(0, 140) + ' ' + t); });
  // Headless Chrome gets 403 from i.imgur.com (the same files load in a normal browser and with plain curl), so imgur files
  // are always served from the mirror cache, fetched once with curl. This changes nothing on the real site.
  await ctx.route(/^https:\/\/i\.imgur\.com\//, (route) => {
    const u = route.request().url();
    const f = path.join(MIRROR_DIR, mirrorName(u));
    if (!fs.existsSync(f)) {
      fs.mkdirSync(MIRROR_DIR, { recursive: true });
      try { execFileSync('curl', ['-sSfL', '-o', f, u], { timeout: 30000 }); } catch (e) { log.failed.push(u + ' (curl ' + (e.status || e.message) + ')'); return route.abort(); }
    }
    const ext = path.extname(u.replace(/[?#].*$/, '')).toLowerCase();
    route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': TYPES[ext] || 'image/jpeg', 'access-control-allow-origin': '*' } });
  });
  if (process.env.MIRROR === '1') {
    await ctx.route(/^https:\/\//, async (route) => {
      const u = route.request().url();
      const f = path.join(MIRROR_DIR, mirrorName(u));
      if (fs.existsSync(f)) {
        const meta = fs.existsSync(f + '.type') ? fs.readFileSync(f + '.type', 'utf8') : (TYPES[path.extname(u.replace(/[?#].*$/, '')).toLowerCase()] || 'application/octet-stream');
        return route.fulfill({ status: 200, body: fs.readFileSync(f), headers: { 'content-type': meta, 'access-control-allow-origin': '*' } });
      }
      log.missing.push(u);
      return route.abort();
    });
  }
  page.log = log; page.ctx = ctx;
  return page;
}

// scroll a top-level page from top to bottom in steps so every reveal fires, then back to top
async function scrollThrough(page, step = 300, pause = 60) {
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y <= h; y += step) { await page.evaluate((v) => window.scrollTo(0, v), y); await page.waitForTimeout(pause); }
  await page.waitForTimeout(1200);
}

// in-page audit: elements that should be visible but are not, broken images, viewport-unit misuse
const AUDIT = () => {
  const out = { stillInvisible: [], brokenImages: [], height: document.documentElement.scrollHeight };
  const skip = (el) => el.closest('.sr,[aria-hidden="true"],[hidden],template,noscript');
  const cand = document.querySelectorAll('h1,h2,h3,h4,p,li,a,img,figure,button,td,th,dt,dd,blockquote,video,canvas,svg');
  for (const el of cand) {
    if (skip(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    let o = 1, x = el, hidden = false;
    while (x && x.nodeType === 1) {
      const cs = getComputedStyle(x);
      if (cs.display === 'none') { hidden = true; break; }
      if (cs.display !== 'contents') o *= parseFloat(cs.opacity);   // opacity on a display:contents box does not reach its children
      if (cs.visibility === 'hidden' && x === el) hidden = true;
      x = x.parentElement;
    }
    if (hidden) continue;   // display:none (other language etc.) is not "stuck"
    if (o < 0.05) out.stillInvisible.push((el.tagName.toLowerCase() + '.' + (el.className && el.className.baseVal === undefined ? el.className : '')).slice(0, 60) + ' "' + (el.textContent || el.alt || '').trim().slice(0, 40) + '"');
  }
  for (const im of document.images) if (im.complete && im.naturalWidth === 0 && im.getAttribute('src')) out.brokenImages.push(im.currentSrc || im.src);
  return out;
};

function outDir(d) { fs.mkdirSync(d, { recursive: true }); return d; }
function arg(name, def) { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : def; }
function flag(name) { return process.argv.includes('--' + name); }

module.exports = { ROOT, OUTER, INNER, MIRROR_DIR, serve, stop, urlFor, withLang, mirrorName, launch, newPage, scrollThrough, AUDIT, outDir, arg, flag };
