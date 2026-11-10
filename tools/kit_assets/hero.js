/* Stage 2 · the Home hero (tools/kit.py home_hero(); copied from tools/kits/cw/hero.js, the stage-1 archive; changed:
   at 320 the cut line's halves swap and the title does not drift, see the 320 composition in hero.css).
   C2 · hero · editorial cinematic on white (from C, the /67 final, ledger in site/_directions/_67/c/LEADERBOARD.md).
   Load-in: an ink cut line is drawn across the frame on the white sheet (CSS, first paint) -> the title lands in ink
   syllable by syllable through line masks (both of its layers on one timetable) -> the line holds a beat -> as soon as the
   photograph of the institute's members is decoded (never onto an empty frame), the line splits and the frame opens from it:
   wherever the picture opens under the title, its letters turn paper white (the white layer rides inside the frame), the
   upper half rides the frame's top edge out, the lower half settles on the paper under the photograph, where the title
   stands, turns umber and stays there as the reel's clock -> rack focus on the people while the statement comes into focus
   line by line -> the record turns over on counter wheels -> link, pause control.
   Then the field: hard cuts through the institute's own footage (clinic, audiometer, data, team, earbud fitting; burned-in
   subtitles cropped out), slow push-ins, back to the people. A shot that stalls is cut away, never held frozen.
   Data (CLAUDE.md, video data): ONE player, preload="metadata". REEL (tools/kits/cw/reel.json, injected by tools/kits/cw.py)
   lists the byte ranges of the four shots in the 21.2 MB promo; after the page's load event they are range-fetched
   (about 1.4 MB) and assembled with a precomputed header into a small video-only MP4 that plays from a Blob, so every cut
   is a local seek and nothing more is downloaded. If that fails (a browser that preflights Range, a changed file), the one
   player seeks the original file and plays only the two shots that sit within 15 s of each other (Chrome reads about
   3 MB ahead of a seek point). Save-Data, 2g and 3g get the photograph only.
   Film grain on desktop, a small scroll parallax through RIHE.onBand. Everything pauses off-screen, in a hidden tab and with
   the pause button. Reduced motion: the composed frame on the photograph at once; the button offers play. */
(function () {
  'use strict';
  var R = window.RIHE, doc = document;
  var hero = doc.querySelector('.cx');
  if (!R || !hero) return;
  var g = window.gsap;
  var $ = function (s) { return hero.querySelector(s); };
  var $$ = function (s) { return [].slice.call(hero.querySelectorAll(s)); };
  var frame = $('.cx-frame'), par = $('.cx-par'), media = $('.cx-media'), still = $('.cx-still');
  var stills = $$('.cx-still');                      // the people: the first photograph opens; the other (data-src) loads with the reel
  var title = $('.cx-hk'), titleW = $('.cx-hw');      // the title's two layers: ink (the h1) and paper white (in the frame)
  var v = $('.cx-v'), btn = $('.cx-pause'), grain = $('.cx-grain');
  var edgeT = $('.cx-edge-t'), edgeB = $('.cx-edge-b');
  var reduce = !!R.reduce;
  var phone = function () { return !!(window.matchMedia && matchMedia('(max-width: 760px)').matches); };
  var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var FILTER = 'saturate(0.86) contrast(0.97) brightness(1.02)';   // the white-surround grade (hero.css .cx-media)

  R.motionReady();
  if (!g) { R.showAll(); return; }
  var ST = window.SplitText, CE = window.CustomEase;
  g.registerPlugin.apply(g, [ST, CE].filter(Boolean));
  var EGATE = 'expo.inOut', EDRAW = 'power2.inOut';
  if (CE) {
    CE.create('cxGate', 'M0,0 C0.5,0 0.14,1 1,1');   // a beat to part, a decisive opening, a long settle
    CE.create('cxDraw', 'M0,0 C0.65,0 0.35,1 1,1');
    EGATE = 'cxGate'; EDRAW = 'cxDraw';
  }

  /* ---------------------------------------------------------------- the reel */
  var REEL = /*@REEL@*/null;
  var SW = REEL ? REEL.w : 854, SH = REEL ? REEL.h : 480;
  var STILL = { still: true, d: 3.2 };                 // the members of RIHE, one photograph or the other (d: seconds on screen)
  var conn = navigator.connection || {};
  var mode = (!REEL || !v || conn.saveData || /(^|-)(2g|3g)$/.test(conn.effectiveType || '')) ? 'lean' : 'clip';
  var SHOTS = [STILL];
  // clip: every shot, t0/t1 inside the assembled clip. seek: the original file, only the shots that sit close together.
  function setShots() {
    SHOTS = [STILL];
    if (mode === 'lean') return;
    REEL.shots.forEach(function (s) {
      if (mode === 'seek' && !s.near) return;
      var x = {}; for (var k in s) x[k] = s[k];
      if (mode === 'seek') { x.t0 = s.a; x.t1 = s.b; }
      SHOTS.push(x);
    });
  }
  setShots();
  function crop(s, W, H) {
    var A = W / H, uy0 = s.y0 * SH, uh = (s.y1 - s.y0) * SH, cw, ch;
    if (SW / uh > A) { ch = uh; cw = ch * A; } else { cw = SW; ch = cw / A; }
    var cx = Math.max(0, Math.min(SW - cw, s.fx * SW - s.ax * cw));
    var cy = Math.max(uy0, Math.min(uy0 + uh - ch, s.fy * SH - ch / 2));
    var k = W / cw;
    return { w: SW * k, h: SH * k, x: -cx * k, y: -cy * k, o: (s.fx * SW * k).toFixed(1) + 'px ' + (s.fy * SH * k).toFixed(1) + 'px' };
  }
  function nextIdx(i) { return (i + 1) % SHOTS.length; }
  function nextFoot(i) { var j = nextIdx(i); return SHOTS[j].still ? nextIdx(j) : j; }

  var slot = 0, onV = false;                     // shot on screen; whether the player is showing it (else the photograph)
  var cue = -1, ready = false, cutting = -1, cutAt = 0, srcSet = false;
  var want = !reduce, seen = true, live = false, begun = false, gateOpen = reduce, firstHold = true;
  var raf = 0, clock = null, kbS = null, kbV = null, gLast = 0, grainOn = false;
  var lastCT = -1, lastMove = 0, clockOn = false, lastK = -1, holding = false, primeT = 0;

  // the assembled clip: header (ftyp + video-only moov + mdat header) + the video samples cut from each fetched range
  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function buildClip() {
    if (!window.fetch || !window.Blob || !window.URL || !URL.createObjectURL) return Promise.reject(new Error('no fetch'));
    return Promise.all(REEL.ranges.map(function (r) {
      return fetch(REEL.src, { headers: { Range: 'bytes=' + r[0] + '-' + r[1] }, credentials: 'omit' }).then(function (res) {
        var cr = res.headers.get('content-range') || '';
        if (res.status !== 206 || cr.indexOf('bytes ' + r[0] + '-' + r[1] + '/' + REEL.size) !== 0) throw new Error('range');
        return res.arrayBuffer();
      });
    })).then(function (bufs) {
      var parts = [b64(REEL.head)];
      bufs.forEach(function (buf, i) {
        var pc = REEL.pieces[i], fp = new Uint8Array(buf, pc[0], 8), hex = '';
        for (var k = 0; k < 8; k++) hex += (fp[k] < 16 ? '0' : '') + fp[k].toString(16);
        if (hex !== REEL.fp[i]) throw new Error('file changed');       // the promo was re-encoded: do not play garbage
        for (var j = 0; j < pc.length; j += 2) parts.push(new Uint8Array(buf, pc[j], pc[j + 1]));
      });
      return URL.createObjectURL(new Blob(parts, { type: 'video/mp4' }));
    });
  }
  function fallback() {                          // clip failed -> seek the original; seek failed -> the photograph only
    var was = mode;
    mode = mode === 'clip' ? 'seek' : 'lean';
    setShots(); cue = -1; ready = false; cutting = -1;
    if (onV) toStill();
    if (mode === 'seek') { v.src = REEL.src; srcSet = true; prepIdle(); }
    else { try { v.removeAttribute('src'); v.load(); } catch (e) {} showClock(false); }
    return was;
  }
  function attach() {                            // after the load event: the first screen never waits for footage
    if (srcSet || mode === 'lean') return;
    srcSet = true;
    stills.forEach(function (im) {               // the other photograph of the people, for every other return to them
      var s = im.getAttribute('data-src');
      if (!s || im.getAttribute('src')) return;
      im.addEventListener('load', function () {  // decoded before the first cut to it: hidden, it is never painted, and the cut would show the empty frame
        var ok = function () { im.setAttribute('data-ok', ''); }, q = im.decode ? im.decode() : null;
        if (q && q.then) q.then(ok, function () {}); else ok();
      }, { once: true });
      im.setAttribute('srcset', im.getAttribute('data-srcset') || ''); im.setAttribute('src', s);
    });
    if (mode === 'clip') buildClip().then(function (u) { if (mode === 'clip') { v.src = u; prepIdle(); } }, function () { if (mode === 'clip') fallback(); });
    else { v.src = REEL.src; prepIdle(); }
  }
  if (v) v.addEventListener('error', function () { if (srcSet && mode !== 'lean' && v.getAttribute('src')) fallback(); });

  function place(i) {
    var s = SHOTS[i];
    if (!s || s.still || !media.clientWidth) return;
    var c = crop(s, media.clientWidth, media.clientHeight);
    g.set(v, { width: c.w, height: c.h, x: c.x, y: c.y, transformOrigin: c.o });
  }
  // position the one player on a shot's in point, paused; ready once that frame is decoded
  function toCue(i) {
    if (!v.getAttribute('src') || SHOTS[i].still) return;
    cue = i; ready = false;
    try { v.pause(); } catch (e) {}
    if (v.readyState >= 1) { try { v.currentTime = SHOTS[i].t0; } catch (e) {} }
    clearTimeout(primeT);
    primeT = setTimeout(function () { prime(i); }, 1200);
    check();
  }
  // some browsers (iOS Safari) decode no frame after a seek until the video has played once: play it unseen for a moment,
  // then seek back to the in point. A shot that still cannot show is never cut to (the people hold the frame).
  function prime(i) {
    if (ready || cue !== i || onV || !want) return;
    v.style.visibility = 'visible';
    var back = function () {
      if (onV || cue !== i) return;
      try { v.pause(); v.currentTime = SHOTS[i].t0; } catch (e) {}
      v.style.visibility = '';
    };
    var pr = v.play();
    if (pr && pr.then) pr.then(function () { setTimeout(back, 120); }, back); else setTimeout(back, 120);
  }
  function check() {
    if (cue < 0 || v.seeking || v.readyState < 2) return;
    if (Math.abs(v.currentTime - SHOTS[cue].t0) < .35) {
      ready = true;
      if (cutting === cue) land(cue);
    } else if (v.paused) { try { v.currentTime = SHOTS[cue].t0; } catch (e) {} }
  }
  if (v) {
    v.addEventListener('loadedmetadata', function () { if (cue >= 0) { try { v.currentTime = SHOTS[cue].t0; } catch (e) {} } });
    ['loadeddata', 'seeked', 'canplay'].forEach(function (ev) { v.addEventListener(ev, check); });
  }
  function prepIdle() {                          // while the photograph holds, cue the next shot
    if (mode === 'lean' || !begun || !srcSet || onV) return;
    var j = nextFoot(slot);
    if (cue !== j) toCue(j);
  }
  function playV(r) {
    v.defaultPlaybackRate = r; v.playbackRate = r;
    var pr = v.play();
    if (pr && pr.catch) pr.catch(function (e) { if (e && e.name === 'NotAllowedError') onBlocked(); });
  }
  // slow push-ins (Ken Burns on the photograph, a creep on the footage); none under reduced motion
  function pushIn(el, dur) { return reduce ? null : g.fromTo(el, { scale: 1 }, { scale: 1.05, duration: dur, ease: 'none' }); }
  function startStill(d) {
    if (clock) clock.kill();
    clock = g.to({}, { duration: d });
    if (kbS) kbS.kill();
    kbS = pushIn(still, d + 1.2);
  }
  // a bright shot under the white letters gets a little more of the local shade (the still always has it): when a shot lands, the patch of the
  // decoded frame under each line's white part is sampled (8 x 8 px; the assembled clip is a same-origin Blob, the
  // fallback's cross-origin file cannot be read and gets none); the brightest line decides. Set at the cut, never faded.
  var lumC = null, lumK = {};
  function patch(cx, vr, x0, x1, y0, y1) {
    var kx = v.videoWidth / vr.width, ky = v.videoHeight / vr.height;
    cx.drawImage(v, (x0 - vr.left) * kx, (y0 - vr.top) * ky, (x1 - x0) * kx, (y1 - y0) * ky, 0, 0, 8, 8);
    var d = cx.getImageData(0, 0, 8, 8).data, a = [];
    for (var i = 0; i < d.length; i += 4) a.push(.2126 * d[i] + .7152 * d[i + 1] + .0722 * d[i + 2]);
    a.sort(function (p, q) { return p - q; });
    return a[57] / 255;   // the 90th percentile, not the mean: a bright patch under part of a letter counts on a dark shot too
  }
  function boost(j) {
    var key = j + R.lang + doc.documentElement.clientWidth, k = lumK[key];
    if (k == null) {
      var lum = 0;
      try {
        if (!lumC) { lumC = doc.createElement('canvas'); lumC.width = lumC.height = 8; }
        var cx = lumC.getContext('2d', { willReadFrequently: true });
        var fr = frame.getBoundingClientRect(), vr = v.getBoundingClientRect();
        [].forEach.call(titleW.querySelectorAll('[data-l="' + R.lang + '"] .li'), function (li) {
          var r = li.getBoundingClientRect();
          var x0 = Math.max(fr.left, vr.left), x1 = Math.min(r.right, fr.right, vr.right), y0 = Math.max(r.top, fr.top, vr.top), y1 = Math.min(r.bottom, fr.bottom, vr.bottom);
          if (x1 - x0 > 4 && y1 - y0 > 4 && v.videoWidth) lum = Math.max(lum, patch(cx, vr, x0, x1, y0, y1));
        });
      } catch (e) { lum = 0; }
      k = lumK[key] = Math.max(0, Math.min(1, (lum - .42) / .3));
    }
    frame.style.setProperty('--sk', k.toFixed(2));
  }
  // back to the people: hard cut to the photograph
  function toStill() {
    var fromV = onV;
    onV = false; slot = 0; cutting = -1;
    frame.style.removeProperty('--sk');            // the still's own value (hero.css)
    g.set(v, { autoAlpha: 0 }); try { v.pause(); } catch (e) {}
    if (kbV) { kbV.kill(); kbV = null; }
    holding = false;
    var nx = stills[(stills.indexOf(still) + 1) % stills.length];   // the other photograph, once decoded (never with the photograph only)
    var ready = nx.hasAttribute('data-src') ? nx.hasAttribute('data-ok') : (nx.complete && nx.naturalWidth > 0);   // the first was decoded before the gate opened
    var swap = mode !== 'lean' && nx !== still && ready;
    if (swap) { g.set(still, { autoAlpha: 0 }); still = nx; g.set(still, { autoAlpha: 1 }); }
    if (fromV || swap || !kbS) { g.set(still, { scale: 1 }); startStill(STILL.d); }
    else { if (clock) clock.kill(); clock = g.to({}, { duration: STILL.d }); }   // the photograph only: its push-in runs on and holds, no snap back
    cue = -1; prepIdle();
  }
  // the cut lands on a decoded frame: crop, show, play
  function land(j) {
    cutting = -1;
    var s = SHOTS[j], from = onV;
    place(j);
    onV = true; slot = j; holding = false;
    g.set(v, { autoAlpha: 1, scale: 1 });
    if (titleW) boost(j);
    playV(s.r);
    if (kbV) kbV.kill();
    kbV = pushIn(v, (s.t1 - s.t0) / s.r + .3);
    if (!from && kbS) { kbS.kill(); kbS = null; }
    lastCT = -1; lastMove = performance.now();
  }
  // hard cut to the next shot; a shot that is not decoded yet is never cut to: the people hold the frame instead
  function advance() {
    var j = nextIdx(slot);
    if (SHOTS[j].still) { toStill(); return; }
    if (onV) {                                   // footage to footage: one player, so the cut is a seek (the last frame holds)
      try { v.pause(); } catch (e) {}
      cutting = j; cutAt = performance.now();
      toCue(j);
      return;
    }
    if (cue === j && ready) { land(j); return; }
    if (clock) clock.kill(); clock = g.to({}, { duration: .25 });   // the people hold the frame (the clock rests)
    holding = true;
    prepIdle();
  }
  function shotProgress() {
    var s = SHOTS[slot];
    if (s.still) return clock ? clock.progress() : 0;
    if (cutting >= 0) return 0;
    return Math.max(0, Math.min(1, (v.currentTime - s.t0) / (s.t1 - s.t0)));
  }
  function paintClock() {                        // the reel's clock runs down through each shot, toward the title
    if (!clockOn) return;
    var k = holding ? 0 : Math.round((1 - shotProgress()) * 500) / 500;
    if (k !== lastK) { lastK = k; edgeB.style.transform = 'scaleX(' + k + ')'; }
  }
  function loop() {
    raf = requestAnimationFrame(loop);
    var now = performance.now();
    if (grainOn && now - gLast > 41) {           // 24 fps grain
      gLast = now;
      grain.style.backgroundPosition = ((Math.random() * 160) | 0) + 'px ' + ((Math.random() * 160) | 0) + 'px';
    }
    if (cutting >= 0) { if (now - cutAt > 900) toStill(); }           // the seek did not land: back to the people
    else if (SHOTS[slot].still) { if (clock && clock.progress() >= 1) advance(); }
    else if (onV) {
      var ct = v.currentTime;
      if (ct >= SHOTS[slot].t1) advance();                               // out point: never run into the promo's next cut
      else if (ct !== lastCT) { lastCT = ct; lastMove = now; }
      else if (now - lastMove > 900) { lastMove = now; toStill(); }    // stalled: cut away rather than hold a frozen frame
    }
    paintClock();
  }
  function run() {
    if (!want || !seen || doc.hidden || !gateOpen) return;
    if (!begun) begin();
    if (SHOTS[slot].still) {
      if (!clock) startStill(firstHold ? 2.2 : STILL.d);   // first time: the gate and rack focus already gave the people a second
      else clock.resume();
      firstHold = false;
    } else if (onV && cutting < 0) playV(SHOTS[slot].r);
    if (kbS) kbS.resume();
    if (kbV) kbV.resume();
    lastMove = performance.now();
    if (!live) { live = true; loop(); }
  }
  function halt() {
    live = false; cancelAnimationFrame(raf); raf = 0;
    try { v.pause(); } catch (e) {}
    if (clock) clock.pause();
    if (kbS) kbS.pause();
    if (kbV) kbV.pause();
  }
  function begin() {
    if (begun) return; begun = true;
    if (mode === 'lean') return;
    if (doc.readyState === 'complete') attach(); else window.addEventListener('load', attach);
  }
  function showClock(on) {
    clockOn = on && mode !== 'lean' && !reduce;
    if (hero.classList.contains('cx-open')) g.to(edgeB, { autoAlpha: clockOn ? 1 : 0, duration: .5, overwrite: 'auto' });
  }
  function onBlocked() { want = false; halt(); setBtn(true); showClock(false); }

  /* pause control */
  function setBtn(paused) {
    if (!btn) return;
    btn.classList.toggle('is-paused', paused);
    var ko = paused ? '배경 영상 재생' : '배경 영상 일시정지', en = paused ? 'Play background video' : 'Pause background video';
    btn.setAttribute('data-aria-ko', ko); btn.setAttribute('data-aria-en', en);
    btn.setAttribute('aria-label', R.lang === 'en' ? en : ko);
  }
  if (btn) {
    btn.addEventListener('click', function () {
      want = !want;
      setBtn(!want);
      if (want) { gateOpen = true; showClock(true); run(); } else halt();
    });
  }
  R.visible(frame, function (on) { seen = on; if (on) run(); else halt(); });
  doc.addEventListener('visibilitychange', function () { if (doc.hidden) halt(); else run(); });
  var rz = 0;
  window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (onV) place(slot); }, 120); });

  /* ---------------------------------------------------------------- reduced motion: composed at once, the photograph */
  if (reduce) {
    if (btn) { btn.hidden = false; setBtn(true); }
    return;
  }

  /* film grain (desktop only; phones keep the plain grade) */
  (function makeGrain() {
    if (!grain || phone()) return;
    try {
      var c = doc.createElement('canvas'), n = 160; c.width = c.height = n;
      var x = c.getContext('2d'), d = x.createImageData(n, n), a = d.data;
      for (var i = 0; i < a.length; i += 4) { var v = (Math.random() * 255) | 0; a[i] = a[i + 1] = a[i + 2] = v; a[i + 3] = 255; }
      x.putImageData(d, 0, 0);
      grain.style.backgroundImage = 'url(' + c.toDataURL('image/png') + ')';
      grainOn = true;
    } catch (e) {}
  })();

  /* scroll: the picture drifts slower than the page, the title a touch faster (sentinel band, never window scroll) */
  // the band starts once fonts and the page's height locks have settled, so its sentinels are sized to the final document
  var py = g.quickTo(par, 'y', { duration: .6, ease: 'power3.out' });
  var ty = g.quickTo(title, 'y', { duration: .6, ease: 'power3.out' });
  var tw = titleW ? g.quickTo(titleW, 'y', { duration: .6, ease: 'power3.out' }) : function () {};   // the white layer moves with it
  (doc.fonts && doc.fonts.ready ? Promise.race([doc.fonts.ready, wait(1500)]) : Promise.resolve()).then(function () {
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      R.onBand(function (b) {
        if (!b.ok) return;
        var r = R.rect(frame), d = Math.max(0, Math.min(b.top - r.top, r.h)), k = phone() ? 0 : -d * .05;   // 320: the cut through the title stays put
        py(d * .09); ty(k); tw(k);
      });
    }); });
  });

  /* ---------------------------------------------------------------- the title sequence */
  var splits = [], tl = null, gtl = null, started = false, left = 2, asked = false;
  var nums = $$('.cx-n');
  // the gate opens only onto a decoded picture (1 s at most, then it opens anyway)
  var stillIn = new Promise(function (res) {
    var dec = function () { var q = still.decode ? still.decode() : null; if (q && q.then) q.then(res, res); else res(); };
    if (still.complete && still.naturalWidth) dec();
    else { still.addEventListener('load', dec, { once: true }); still.addEventListener('error', res, { once: true }); }
  });
  function gateTo(p) { var v = p.toFixed(2) + '%'; frame.style.clipPath = 'inset(' + v + ' 0% ' + v + ' 0%)'; }
  // the record as counter wheels: every digit starts at 0 and lower places travel a full turn further, like a counter
  function wheels() {
    var out = [];
    nums.forEach(function (n, ni) {
      var s = n.getAttribute('data-n'), html = '';
      for (var i = 0; i < s.length; i++) {
        var k = i * 10 + (+s.charAt(i)), cells = '';
        for (var j = 0; j <= k; j++) cells += '<span>' + (j % 10) + '</span>';
        html += '<span class="cx-dg"><span class="cx-strip">' + cells + '</span></span>';
      }
      n.innerHTML = html;
      [].forEach.call(n.querySelectorAll('.cx-strip'), function (st) {
        var k = st.children.length - 1;
        out.push({ el: st, to: -100 * k / (k + 1), n: ni });
      });
    });
    return out;
  }
  function unwheel() { nums.forEach(function (n) { n.textContent = n.getAttribute('data-n'); }); }
  function rescue() {
    try { if (tl) tl.kill(); if (gtl) gtl.kill(); } catch (e) {}
    try { splits.forEach(function (s) { s.revert(); }); } catch (e) {}
    splits = [];
    g.set($$('.cx-h .li, .cx-inst, .cx-lead, .cx-nums, .cx-nums li, .cx-more, .cx-pause, .cx-media'), { clearProps: 'transform,opacity,visibility,filter,--rs' });
    frame.style.clipPath = '';
    unwheel();
    hero.classList.add('cx-done');
    gateOpen = true; run();
    R.showAll();
  }
  function done() {
    if (--left > 0) return;
    try { splits.forEach(function (s) { s.revert(); }); } catch (e) {}
    splits = [];
    unwheel();
    frame.style.clipPath = '';
    g.set(media, { clearProps: 'filter,transform' });
    g.set($$('.cx-lead'), { clearProps: 'filter' });
    hero.classList.add('cx-done');
  }
  // the gate has opened: the lower edge now rests on the frame's bottom line and becomes the reel's clock
  function landed() {
    hero.classList.add('cx-open');
    g.set(edgeB, { clearProps: 'transform' });
    edgeB.style.transform = 'scaleX(1)';
    showClock(true);
    gateOpen = true; run();
  }
  function openGate() {
    if (asked) return; asked = true;
    Promise.race([stillIn, wait(1000)]).then(function () { if (gtl && !gtl.progress()) gtl.play(); });
  }
  function intro() {
    if (started) return; started = true; clearTimeout(safety);
    var en = R.lang === 'en', sel = en ? '.cx-h-en .li' : '.cx-h-ko .li';
    var lines = [].slice.call(title.querySelectorAll(sel)), linesW = titleW ? [].slice.call(titleW.querySelectorAll(sel)) : [];
    var lead = $('.cx-lead[data-l="' + (en ? 'en' : 'ko') + '"]');
    var inst = $('.cx-inst'), more = $('.cx-more'), list = $('.cx-nums'), items = $$('.cx-nums li');
    var marks = lines, marksW = linesW, leadLines = null;
    if (ST) {
      if (!en) {
        var s1 = new ST(lines, { type: 'chars', charsClass: 'cx-ch' }); splits.push(s1); marks = s1.chars;
        if (linesW.length) { var s1w = new ST(linesW, { type: 'chars', charsClass: 'cx-ch' }); splits.push(s1w); marksW = s1w.chars; }
      }
      // lines are only split once the text face is in (a late swap would re-break them inside their masks)
      if (bodyReady(en, lead)) { var s2 = new ST(lead, { type: 'lines', mask: 'lines', linesClass: 'cx-ll' }); splits.push(s2); leadLines = s2.lines; }
    }
    // take the slit over from the CSS animation wherever it is now
    var sx = 0, m = /matrix\(([-\d.e]+)/.exec(getComputedStyle(edgeT).transform || '');
    if (m) sx = Math.max(0, Math.min(1, parseFloat(m[1])));
    edgeT.style.animation = 'none';
    g.set(edgeT, { scaleX: sx, autoAlpha: 1, y: 0 });
    g.set(edgeB, { scaleX: 1, autoAlpha: 0, y: 0 });
    // starting states, set before the blocks are released so nothing flashes
    var wh = wheels();
    g.set(marks.concat(marksW), { yPercent: 118 });
    // 135%: the blur's halo waits wholly outside its mask (on white even a faint halo would show as a grey bar)
    if (leadLines) g.set(leadLines, { yPercent: 135, filter: 'blur(6px)' }); else g.set(lead, { autoAlpha: 0, y: 16, filter: 'blur(8px)' });
    g.set([inst, more], { autoAlpha: 0, y: 14 });
    g.set(items, { autoAlpha: 0, y: 12 });
    g.set(list, { '--rs': '0%' });
    gateTo(50);
    g.set(media, { filter: FILTER + ' blur(' + (phone() ? 7 : 13) + 'px)', scale: 1.05 });
    if (btn) { btn.hidden = false; g.set(btn, { autoAlpha: 0 }); setBtn(false); }
    $$('[data-a]').forEach(function (el) { el.classList.add('on'); });

    // the line finishes, then holds a beat (the title has mostly landed in ink) before it splits
    var draw = (1 - sx) * .45, open = Math.max(draw + .3, .5);
    var half = function () { return frame.getBoundingClientRect().height / 2 + .5; };
    var UMB = (getComputedStyle(doc.documentElement).getPropertyValue('--umber') || '').trim() || '#8a5a0e';
    // the cut: the line splits and the frame opens from it; the upper half rides the top edge out, the lower half comes to
    // rest on the paper under the photograph (the title's line) and turns umber: the reel's clock
    var gate = { p: 50 };
    // 320 (stage 2): the frame's bottom edge crosses the title, so the halves swap: the clock (edgeB) rides up to the
    // top edge and stays there, the other half rides down to the title's line and is gone (hero.css .cx-open at 320)
    var up = phone() ? 1 : -1;
    gtl = g.timeline({ paused: true, onComplete: done })
      .set(edgeB, { autoAlpha: 1 }, 0)
      .to(gate, { p: 0, duration: 1.05, ease: EGATE, onUpdate: function () { gateTo(gate.p); } }, 0)
      .to(edgeT, { y: function () { return up * half(); }, duration: 1.05, ease: EGATE }, 0)
      .to(edgeB, { y: function () { return -up * half(); }, duration: 1.05, ease: EGATE }, 0)
      .to(edgeT, { autoAlpha: 0, duration: .4, ease: 'power1.in' }, .6)
      .to(edgeB, { backgroundColor: UMB, duration: .6, ease: 'power1.out' }, .7)
      .call(landed, null, 1.06)
      // rack focus: the people come into focus as the title settles
      .to(media, { filter: FILTER + ' blur(0px)', scale: 1, duration: 1.6, ease: 'power2.out' }, .05);
    tl = g.timeline({ defaults: { ease: 'expo.out' }, onComplete: done });
    tl.to(edgeT, { scaleX: 1, duration: draw, ease: EDRAW }, 0)
      .to(marks, { yPercent: 0, duration: .92, stagger: en ? .075 : .05 }, .04)
      .to(marksW, { yPercent: 0, duration: .92, stagger: en ? .075 : .05 }, .04)   // the white layer, on the same timetable
      .call(openGate, null, open)
      .to(inst, { autoAlpha: 1, y: 0, duration: .8 }, open + .4)
      // the statement comes into focus as it rises, an echo of the rack focus
      .to(leadLines || lead, leadLines ? { yPercent: 0, filter: 'blur(0px)', duration: 1, stagger: .07 } : { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: 1 }, open + .46)
      .to(list, { '--rs': '100%', duration: .8, ease: EDRAW }, open + .5)
      .to(items, { autoAlpha: 1, y: 0, duration: .7, stagger: .07 }, open + .6);
    wh.forEach(function (w) { tl.to(w.el, { yPercent: w.to, duration: 1.4, ease: 'power4.out' }, open + .62 + w.n * .07); });
    tl.to(more, { autoAlpha: 1, y: 0, duration: .7 }, open + .85);
    if (btn) tl.to(btn, { autoAlpha: 1, duration: .6, ease: 'power1.out' }, open + 1.05);
  }
  function safe(fn) { return function () { try { fn(); } catch (e) { if (window.console) console.error(e); rescue(); } }; }
  function finish() {
    if (tl && tl.progress() < 1) tl.progress(1);
    if (gtl && gtl.progress() < 1) gtl.progress(1);
  }
  R.onLang(finish);
  R.showHooks.push(finish);
  begin();

  // Footage starts loading at the load event. The sequence waits only for the title face of the current language
  // (a small text= subset, max .6 s) and for the hero on screen; text faces load alongside and are checked at split time.
  function bodyReady(en, el) {
    try { return !doc.fonts || doc.fonts.check(en ? '400 16px Archivo' : '400 16px "Noto Sans KR"', el.textContent.slice(0, 60)); }
    catch (e) { return false; }
  }
  var safety = setTimeout(safe(intro), 2200);
  var fload = function (f, s) {
    try { var q = doc.fonts.load(f, s); return q && q.catch ? q.catch(function () {}) : Promise.resolve(); } catch (e) { return Promise.resolve(); }
  };
  var face = Promise.resolve();
  if (doc.fonts && doc.fonts.load) {
    var kt = fload('400 100px "Black Han Sans"', '청각재활연구소'), et = fload('860 100px Archivo', 'RESEARCH 0123456789');
    fload('400 16px "Noto Sans KR"', ($('.cx-lead[data-l="ko"]') || {}).textContent || '');
    fload('400 16px Archivo', 'Built on basic research');
    face = R.lang === 'en' ? et : kt;
  }
  Promise.race([face, wait(600)]).then(function () {
    R.inview(hero, safe(intro), { threshold: .1, px: 120 });
  });
})();
