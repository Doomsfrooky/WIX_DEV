/* B · clinical modern · final (judge synthesis). Skeleton: lens 3 (first principles), one measurement.
   Grafted: the footage already rolling behind the closed window at 0.8x so the sweep uncovers moving pictures (lens 1),
   a pause control that stops everything and Save-Data / 2g / 3g stills (lens 2), the window's time axis and its
   progress line (lens 4), a loop that can never run past the clean shot and an autoplay-refused frame with a play
   button (lens 5), the link's arrow plotted by DrawSVG once the cursor has passed it (lens 6).
   Five seconds must establish four things: hearing (the field), a university hospital (the institution), measured output
   (the record) and real clinical work (the institute's own footage). The field's own instrument says the first directly:
   the audiogram frequency axis, 125 Hz to 8 kHz, is the spine of the composition. The motion is the act of measuring:
   one teal cursor sweeps the axis like a test tone, with a live readout that prints each octave as it passes. The name
   rises out of the axis where the cursor crosses it, the text and the window onto an audiometer in use are scanned in
   behind it, and the record registers when it reaches it. The window opens on the people (the members of RIHE); once
   the type has settled, their instrument dissolves in, already running. Then only the footage moves. */
(function () {
  var R = window.RIHE;
  var hero = document.getElementById('fp-hero');
  if (!hero || !R) return;
  R.motionReady();

  var doc = document;
  var G = window.gsap;
  var mobile = !!(window.matchMedia && window.matchMedia('(max-width: 760px)').matches);
  var win = hero.querySelector('.fp-win');
  var media = hero.querySelector('.fp-media');
  var reel = makeReel(win, mobile, R.reduce);

  if (R.reduce) { reel.still(); win.classList.add('fp-open'); return; }   // final composed state at once; no autoplay
  reel.start();                                         // rolling behind the closed window: moving when the sweep uncovers it
  if (!G) { R.showAll(); win.classList.add('fp-open'); return; }

  var SplitText = window.SplitText, CustomEase = window.CustomEase;
  try { G.registerPlugin.apply(G, [SplitText, CustomEase, window.DrawSVGPlugin].filter(Boolean)); } catch (e) {}
  var SWEEP = 'power2.inOut', OUT = 'expo.out';
  if (CustomEase) {
    SWEEP = CustomEase.create('fpSweep', 'M0,0 C0.24,0 0.2,1 1,1');   // a calibrated sweep: measured start, long settle into 8 kHz
    OUT = CustomEase.create('fpOut', 'M0,0 C0.12,0.82 0.24,1 1,1');
  }
  var css = getComputedStyle(hero);
  var TEAL = (css.getPropertyValue('--teal') || '#0a7671').trim();
  var MUTE = (css.getPropertyValue('--mute') || '#5a6d71').trim();

  var tl = null, splits = [], built = false, finished = false;
  var nums = [].map.call(hero.querySelectorAll('.fp-c'), function (el) { return { el: el, n: +el.getAttribute('data-count') }; });

  // content must never stay hidden: an error, a language switch or a new width ends in the final state
  R.showHooks.push(finish);
  R.onLang(function () { if (tl) finish(); });
  var w0px = window.innerWidth;
  window.addEventListener('resize', function () { if (tl && Math.abs(window.innerWidth - w0px) > 2) finish(); });

  var fonts = fontsReady(320);
  R.inview(hero, function () { fonts.then(build); }, { threshold: 0.2, px: 220 });
  setTimeout(function () { if (!built) build(); }, 1200);  // never wait longer than this for fonts or the observer

  function fontsReady(ms) {
    var list = [];
    if (doc.fonts && doc.fonts.load) {
      list = (R.lang === 'en' ? ['600 60px "Hanken Grotesk"'] : ['600 100px "Noto Sans KR"']).map(function (f) {
        return doc.fonts.load(f, /Noto/.test(f) ? '청각재활연구소' : 'Research').catch(function () {});
      });
    }
    return Promise.race([Promise.all(list), new Promise(function (r) { setTimeout(r, ms); })]);
  }

  function build() {
    if (built) return;
    built = true;
    var lang = R.lang === 'en' ? 'en' : 'ko';
    var inner = hero.querySelector('.fp-in');
    var axis = hero.querySelector('.fp-axis');
    var draw = hero.querySelector('.fp-draw');
    var ticks = [].slice.call(hero.querySelectorAll('.fp-tk'));
    var labels = ticks.map(function (t) { return t.querySelector('b'); });
    var rd = hero.querySelector('.fp-rd');
    var line = hero.querySelector('.fp-line');
    var h1 = hero.querySelector('.fp-title');
    var tSpan = h1.querySelector('[data-l="' + lang + '"]');
    var text = hero.querySelector('.fp-text');
    var inst = hero.querySelector('.fp-inst');
    var lead = hero.querySelector('.fp-lead');
    var link = hero.querySelector('.fp-link');
    var ledger = hero.querySelector('.fp-ledger');
    var rows = [].slice.call(hero.querySelectorAll('.fp-row'));

    var units = [];
    if (SplitText) {
      var ts = SplitText.create(tSpan, { type: lang === 'ko' ? 'lines,chars' : 'lines,words', mask: 'lines', linesClass: 'fp-sl' });
      splits.push(ts);
      units = lang === 'ko' ? ts.chars : ts.words;
    }

    // geometry: every cue is a position on the axis (0 = 125 Hz, 1 = 8 kHz)
    var iR = inner.getBoundingClientRect(), aR = axis.getBoundingClientRect(), wR = win.getBoundingClientRect();
    var AW = Math.max(1, aR.width), AX = aR.left - iR.left, AY = aR.top - iR.top;
    var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var xc = function (el) { var r = el.getBoundingClientRect(); return clamp01((r.left + r.width / 2 - aR.left) / AW); };
    var xl = function (el) { var r = el.getBoundingClientRect(); return clamp01((r.left - aR.left) / AW); };
    var w0 = clamp01((wR.left - aR.left) / AW), w1 = clamp01((wR.right - aR.left) / AW);
    var span = Math.max(0.0001, w1 - w0);

    // the cursor: from 7 px above the axis to the foot of the window
    var lineTop = Math.round(AY - 7);
    line.style.top = lineTop + 'px';
    line.style.height = Math.max(24, Math.round(wR.bottom - iR.top - lineTop)) + 'px';
    var setLineX = G.quickSetter(line, 'x', 'px');

    // the readout never runs past the end of the axis
    rd.textContent = '8.0 kHz';
    var rdW = rd.offsetWidth;
    rd.textContent = '125 Hz';

    // desktop: the text column is scanned in behind the cursor (soft edge); a phone stacks it, so it reads in order
    var tR = text.getBoundingClientRect();
    var useMask = !mobile && getComputedStyle(text).display !== 'contents' && tR.width > 0;
    var tx0 = tR.left - aR.left;

    var D = mobile ? 1.15 : 1.6, T0 = 0.12;
    var ease = G.parseEase(SWEEP);
    var tAt = function (x) {                               // time at which the eased cursor reaches x
      var lo = 0, hi = 1;
      for (var i = 0; i < 22; i++) { var m = (lo + hi) / 2; if (ease(m) < x) lo = m; else hi = m; }
      return T0 + D * (lo + hi) / 2;
    };

    var sweep = { p: 0 }, lastTxt = '', opened = false, opening = false;
    function paint() {
      var p = sweep.p, x = p * AW;
      draw.style.transform = 'scaleX(' + p.toFixed(5) + ')';
      setLineX(AX + x - 0.5);
      var f = 125 * Math.pow(2, 6 * p);                   // octaves are equal steps: 125 Hz x 2^(6p)
      var txt = f < 999.5 ? Math.round(f) + ' Hz' : (f / 1000).toFixed(1) + ' kHz';
      if (txt !== lastTxt) { rd.textContent = txt; lastTxt = txt; }
      rd.style.transform = 'translateX(' + Math.min(x, AW - rdW).toFixed(2) + 'px)';
      var q = clamp01((p - w0) / span);
      if (q >= 0.999) { if (!opened) { opened = true; win.classList.remove('fp-opening'); win.classList.add('fp-open'); } }
      else if (q > 0 && !opening) { opening = true; win.classList.add('fp-opening'); }
      var c = q >= 1 ? 'none' : 'inset(0% ' + ((1 - q) * 100).toFixed(3) + '% 0% 0%)';
      media.style.clipPath = c; media.style.webkitClipPath = c;
      if (useMask) {
        var e = x - tx0;
        var m = e > tR.width + 60 ? 'none' : 'linear-gradient(90deg, #000 ' + (e - 60).toFixed(1) + 'px, rgba(0,0,0,0) ' + (e - 4).toFixed(1) + 'px)';
        text.style.webkitMaskImage = m; text.style.maskImage = m;
      }
    }

    // hidden pieces first, then the containers may show
    G.set(units, { yPercent: lang === 'ko' ? 140 : 150 });
    G.set(labels, { opacity: 0 });
    G.set(rows, { autoAlpha: 0, y: 6 });
    G.set(line, { scaleY: 0, opacity: 0 });
    if (!useMask) {
      G.set([inst, link], { autoAlpha: 0, y: 8 });
      G.set(lead, { clipPath: 'inset(0% 0% 100% 0%)', y: 6 });
    }
    nums.forEach(function (o) { o.el.textContent = '0'; });
    paint();
    [h1, lead, inst, link, ledger, draw, media].forEach(function (el) { el.classList.add('on'); });
    rows.concat(labels).forEach(function (el) { el.classList.add('on'); });

    tl = G.timeline({ onComplete: done });

    // the cursor lands on the axis and drops to the foot of the window, then sweeps 125 Hz to 8 kHz
    tl.to(line, { scaleY: 1, opacity: 1, duration: 0.45, ease: 'power3.out' }, 0);
    tl.to(rd, { opacity: 1, duration: 0.2, ease: 'none' }, 0.05);
    tl.to(sweep, { p: 1, duration: D, ease: SWEEP, onUpdate: paint }, T0);
    tl.to([line, rd], { opacity: 0, duration: 0.34, ease: 'power1.in' }, T0 + D - 0.08);

    // each octave registers as the cursor crosses it: the tick turns teal, its label is printed and cools to grey
    ticks.forEach(function (tk, i) {
      var t = tAt(i / 6);
      tl.to(tk, { backgroundColor: TEAL, duration: 0.18, ease: 'none' }, t);
      tl.set(labels[i], { opacity: 1, color: TEAL }, t);
      tl.to(labels[i], { color: MUTE, duration: 0.8, ease: 'power1.inOut' }, t + 0.3);
    });

    // the name rises out of the axis, unit by unit, as the cursor passes beneath
    units.forEach(function (u) { tl.to(u, { yPercent: 0, duration: 0.9, ease: OUT }, Math.max(0, tAt(xc(u)) - 0.06)); });

    // a phone stacks the text under the window: affiliation first, the abstract unrolls, the way on comes last
    if (!useMask) {
      tl.to(inst, { autoAlpha: 1, y: 0, duration: 0.7, ease: OUT }, T0 + 0.1);
      tl.to(lead, { clipPath: 'inset(0% 0% 0% 0%)', y: 0, duration: 1.0, ease: OUT }, T0 + D * 0.5);
      tl.to(link, { autoAlpha: 1, y: 0, duration: 0.6, ease: OUT }, T0 + D + 0.2);
    }

    // the record registers when the cursor reaches it (on a phone the record sits last, so it follows the reading order)
    var tRec = mobile ? T0 + D * 0.7 : tAt(xl(ledger)) + 0.02;
    rows.forEach(function (row, i) {
      var t = tRec + i * 0.07;
      tl.to(row, { autoAlpha: 1, y: 0, duration: 0.5, ease: OUT }, t);
      var o = nums[i], c = { v: 0 };
      if (o) tl.to(c, { v: o.n, duration: 0.75, ease: 'power3.out', onUpdate: function () { o.el.textContent = String(Math.round(c.v)); } }, t + 0.04);
    });

    // the picture settles into its window as the cursor uncovers it (a slow focus pull, no blur on the video layer)
    var layer = hero.querySelector('.fp-depth');
    if (layer) {
      var s1 = mobile ? 1 : 1.07;                         // desktop keeps 7 % of headroom for the depth drift below
      G.set(layer, { scale: s1 + 0.07, transformOrigin: '50% 46%' });
      tl.to(layer, { scale: s1, duration: 1.9, ease: 'power2.out' }, Math.max(0, tAt(w0) - 0.05));
    }
    // the link's arrow is plotted once the cursor has passed it (a phone: just after the link arrives)
    var arrSvg = link.querySelector('.fp-arr'), arr = arrSvg && arrSvg.querySelector('path');
    if (arr && window.DrawSVGPlugin) {
      G.set(arr, { drawSVG: '0% 0%' });
      tl.to(arr, { drawSVG: '0% 100%', duration: 0.6, ease: 'power2.inOut' }, useMask ? tAt(xc(arrSvg)) + 0.04 : T0 + D + 0.4);
    }
    depth();
  }

  // a window, not a picture: on wide screens the footage sits a little deeper than its frame while the outer page
  // scrolls (RIHE.onBand: the visible band of this document, measured inside the non-scrolling Wix iframe).
  // The drift stays inside the clean band of the shot (no letterbox, no burned-in subtitles).
  function depth() {
    var layer = hero.querySelector('.fp-depth');
    if (mobile || !layer || !G.quickTo) return;
    var yTo = G.quickTo(layer, 'y', { duration: 0.7, ease: 'power3.out' });
    R.onBand(function () {
      var p = R.progress(R.rect(win));
      if (p == null) return;
      yTo((p - 0.5) * 2 * win.offsetHeight * 0.03);
    });
  }

  // tidy end state: splits reverted (plain text again, so later resizes and language switches reflow naturally)
  function done() {
    if (finished) return;
    finished = true;
    hero.classList.add('fp-done');
    splits.forEach(function (s) { try { s.revert(); } catch (e) {} });
    splits = [];
    nums.forEach(function (o) { o.el.textContent = String(o.n); });
    var q = function (s) { return [].slice.call(hero.querySelectorAll(s)); };
    G.set(q('.fp-line, .fp-rd'), { opacity: 0 });
    G.set(q('.fp-tk, .fp-tk b'), { clearProps: 'backgroundColor,color,opacity' });
    q('.fp-tk b').forEach(function (b) { b.classList.add('on'); });
    G.set(q('.fp-inst, .fp-lead, .fp-link, .fp-row'), { clearProps: 'clipPath,transform,opacity,visibility' });
    var text = hero.querySelector('.fp-text');
    if (text) { text.style.webkitMaskImage = ''; text.style.maskImage = ''; }
    if (media) { media.style.clipPath = 'none'; media.style.webkitClipPath = 'none'; }
    var draw = hero.querySelector('.fp-draw');
    if (draw) draw.style.transform = 'none';
    var arr = hero.querySelector('.fp-arr path');
    if (arr) G.set(arr, { clearProps: 'strokeDasharray,strokeDashoffset' });
    win.classList.remove('fp-opening');
    win.classList.add('fp-open');
    tl = null;
  }
  function finish() {
    if (tl) { try { tl.progress(1); } catch (e) {} }
    if (!finished && built) done();
    if (!built) {
      built = true; finished = true;
      R.each('[data-a],[data-ai]', function (el) { el.classList.add('on'); }, hero);
      nums.forEach(function (o) { o.el.textContent = String(o.n); });
    }
    hero.classList.add('fp-done');
    win.classList.remove('fp-opening');
    win.classList.add('fp-open');
    reel.start();
  }

  /* ---------- the reel: the institute's own edit of one pure-tone test ----------
     audiometer close-up, hands on the keys (112.05-114.29 s) -> the audiogram screen and booth camera (114.29-116.42 s),
     looped on one element at 0.8x; the jump back reads as the edit's own cut. The photo of the members is the window's
     base layer, so the cursor always uncovers a real picture whatever the network does. The video is fetched and started
     while the page parses (inline loader in hero.html), so on a normal connection the sweep uncovers footage that is
     already moving; otherwise it dissolves in over the photo the moment it plays. Phones, Save-Data and 2g/3g keep the
     photo: at 120 px tall the keys and screens are illegible and the bytes are real. */
  function makeReel(win, mobile, reduce) {
    var noop = function () {};
    var v = win && win.querySelector('.fp-v');
    var mediaEl = win && win.querySelector('.fp-media');
    var btn = win && win.querySelector('.fp-pz');
    var fill = win && win.querySelector('.fp-fill');
    var cn = navigator.connection;
    var slow = !!(cn && (cn.saveData || /2g|3g/.test(cn.effectiveType || '')));
    if (mobile || slow || !v || typeof v.play !== 'function' || !v.getAttribute('data-src')) return { start: noop, still: noop };
    var S = { a: 112.05, b: 116.42, first: 112.2, rate: 0.8 };
    var wanted = false, onScreen = true, userPaused = false, dead = false, raf = 0, lived = false, anyFrame = false;
    v.fpLoop = true;                                     // the hero now owns the loop (the inline loader stops guarding it)
    v.muted = true;
    // the inline loader fetches only the loop's bytes (v.fpClip, CLAUDE.md video budget); without it, the file itself
    if (!v.getAttribute('src') && !v.fpClip) { v.preload = 'metadata'; v.src = v.getAttribute('data-src'); }
    function rate() { try { v.defaultPlaybackRate = S.rate; v.playbackRate = S.rate; } catch (e) {} }
    rate();
    v.addEventListener('loadedmetadata', rate);

    function seek(t) { try { v.currentTime = t; } catch (e) {} }
    function sync() { if (btn) btn.setAttribute('aria-pressed', String(userPaused)); }
    function play() {
      rate();
      var p = v.play();
      if (p && p.catch) p.catch(function (err) {
        if (err && err.name === 'NotAllowedError') { userPaused = true; sync(); frameOnly(); }   // autoplay refused: a still and a play button
      });
    }
    function reveal() {
      if (anyFrame) return;
      anyFrame = true;
      v.classList.add('on');
      win.classList.add('fp-live');
      if (!lived && mediaEl) { lived = true; setTimeout(function () { mediaEl.classList.add('live'); }, 1000); }  // then hard cuts
    }
    // a paused, clean frame of the shot (never frame 0, never past the shot) may stand in for the footage
    function frameOnly() {
      var f = function () { if (!v.seeking && v.readyState >= 2 && v.currentTime >= S.a - 0.25 && v.currentTime < S.b) reveal(); };
      f(); ['loadeddata', 'seeked'].forEach(function (ev) { v.addEventListener(ev, f); });
    }
    function go() { return wanted && onScreen && !doc.hidden && !userPaused && !dead; }
    function loop() { if (!raf) raf = requestAnimationFrame(step); }
    function step() {
      raf = 0;
      if (!go()) return;
      if (!v.seeking) {
        var t = v.currentTime;
        if (t >= S.b || t < S.a - 0.25) seek(S.a);       // never runs past the clean shot into the promo's graphics
        else {
          if (!v.paused && v.readyState >= 2 && !win.classList.contains('fp-opening')) reveal();   // never swap pictures mid-reveal
          if (fill) fill.style.transform = 'scaleX(' + Math.min(1, Math.max(0, (t - S.a) / (S.b - S.a))).toFixed(4) + ')';
        }
      }
      if (v.paused && v.readyState >= 2) play();
      loop();
    }
    function resume() { if (go()) { play(); loop(); } }
    function pause() { if (raf) cancelAnimationFrame(raf); raf = 0; if (!v.paused) v.pause(); }
    v.addEventListener('error', function () {
      if (v.fpRetry) return;                             // the loader is retrying with the file itself
      dead = true; pause(); win.classList.remove('fp-live'); v.classList.remove('on');
    });
    R.visible(win, function (on) { onScreen = on; if (on) resume(); else pause(); });
    doc.addEventListener('visibilitychange', function () { if (doc.hidden) pause(); else resume(); });
    if (btn) btn.addEventListener('click', function () {
      userPaused = !userPaused;
      sync();
      if (userPaused) pause(); else resume();
    });

    if (reduce) {                                        // reduced motion: the footage's opening frame, never played, no controls
      var early = function () {
        if (!anyFrame && !v.seeking && v.readyState >= 2 && Math.abs(v.currentTime - S.first) < 0.35) { anyFrame = true; v.classList.add('on'); }
      };
      ['loadeddata', 'seeked', 'canplay'].forEach(function (ev) { v.addEventListener(ev, early); });
      return { start: noop, still: early };
    }
    return { start: function () { if (wanted) return; wanted = true; resume(); }, still: noop };
  }
})();
