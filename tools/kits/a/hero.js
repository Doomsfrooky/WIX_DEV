/* RIHE · Home hero · direction A, academic classic · /67 final (judge's synthesis on the lens 4 skeleton).
   1. Text: the serif name is set in stages behind line masks (SplitText), the Oxford rule is drawn with a ruling-pen
      ease and takes the abbreviation, the imprint and the lead follow, the ledger is ruled and its figures rise into
      place. Direction A page: on desktop this ledger is the page's outcomes band, so the figures also count up while
      they rise (0.95 s each, power3.out, final by about 2.3 s). Everything is set by about 2.6 s.
   2. Media: the institute's own footage (Hearing Big-data Center film) is toned into one navy family in WebGL. The
      first picture develops out of the ear under examination: a front travels outward from it, the brightest tones
      leading. Toward the text the picture recedes into the navy ground by tone, measured from the text column. Two
      real takes (the ear examination, hands on an audiometer) alternate through a luminance-keyed dissolve. Phones get
      the first take with a CSS duotone and a circular develop; reduced motion and thrifty connections get a still.
      Data budget (CLAUDE.md, the film is 21.2 MB): the players never stream the film. Three byte ranges are fetched
      (the moov, then each take's samples from the keyframe before it), repacked into small MP4 clips in memory and
      played from Blob URLs: about 1.2 MB on desktop, 0.95 MB on phones, all within the first 3 s.
   3. A visible pause control (WCAG 2.2.2). Everything stops off-screen and in hidden tabs; the canvas redraws at film
      rate (24 fps) unless a transition is running.
   4. Scroll hand-off through RIHE.onBand only: the footage drifts and dims as the masthead leaves. */
var R = window.RIHE || {};
var hero = document.querySelector('.hx');
if (!hero) return;
var doc = document, G = window.gsap, ST = window.SplitText, CE = window.CustomEase;
var $ = function (s, c) { return (c || hero).querySelector(s); };
var $$ = function (s, c) { return [].slice.call((c || hero).querySelectorAll(s)); };
var reduce = !!R.reduce;
var phone = !!(window.matchMedia && matchMedia('(max-width: 760px)').matches);
var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
var thrifty = !!conn.saveData || /^(slow-2g|2g|3g)$/.test(conn.effectiveType || '');
// a script that starts after 1.6 s finds the CSS safety fade under way: it carries on from there, never hides again
var late = !!(window.performance && performance.now() > 1600);

if (G) {
  [ST, CE].forEach(function (p) { if (p) { try { G.registerPlugin(p); } catch (e) {} } });
  if (R.motionReady) R.motionReady();
} else if (R.showAll) {
  R.showAll();
}

/* =============================================================== 1. text */
var EASE = 'expo.out', DRAW = 'power2.inOut';
if (G && CE) {
  CE.create('hxOut', 'M0,0 C0.16,0.84 0.3,1 1,1');      // long, quiet settle
  CE.create('hxDraw', 'M0,0 C0.56,0 0.24,1 1,1');      // ruling pen: slow start, slow finish
  EASE = 'hxOut'; DRAW = 'hxDraw';
}
var splits = [], introTl = null, introDone = false;
function lang() { return R.lang === 'en' ? 'en' : 'ko'; }
function showFinal() { $$('[data-a]').forEach(function (el) { el.classList.add('on'); }); }
function revertSplits() { splits.forEach(function (s) { try { s.revert(); } catch (e) {} }); splits = []; }
function whenFonts(cb) {
  var done = false, go = function () { if (!done) { done = true; cb(); } };
  setTimeout(go, 700);
  try {
    var f = doc.fonts;
    Promise.all(lang() === 'ko'
      ? [f.load('600 90px "Noto Serif KR"', '청각재활연구소'), f.load('400 18px "Noto Serif KR"', '난청 연구'), f.load('400 40px "Source Serif 4"', '120')]
      : [f.load('500 64px "Source Serif 4"', 'Research'), f.load('italic 400 64px "Source Serif 4"', 'of'), f.load('400 18px "Source Serif 4"', 'Built 120')]
    ).then(go, go);
  } catch (e) { go(); }
}
function intro() {
  if (!G || !ST || reduce) { showFinal(); introDone = true; return; }
  var L = lang();
  var title = $('.hx-title [data-l="' + L + '"]'), lead = $('.hx-lead [data-l="' + L + '"]');
  var bar = $('.hx-rule i'), abbr = $('.hx-rule abbr'), footRule = $('.hx-foot-rule'), inst = $('.hx-inst'), link = $('.hx-link');
  var nums = $$('.hx-num'), labs = $$('.hx-lab'), seps = $$('.hx-ledger li + li');
  var st = new ST(title, { type: L === 'ko' ? 'lines,chars' : 'lines,words', mask: 'lines', linesClass: 'hx-ml' });
  var sl = new ST(lead, { type: 'lines', mask: 'lines', linesClass: 'hx-ml' });
  splits.push(st, sl);
  var parts = L === 'ko' ? st.chars : st.words, figs = [];
  if (!phone) { var sn = new ST(nums, { type: 'lines', mask: 'lines', linesClass: 'hx-ml' }); splits.push(sn); figs = sn.lines; }
  // from-states inline first, then lift the CSS hiding in one go: no frame shows text in a half state
  G.set(parts, { yPercent: 120 });
  G.set(sl.lines, { yPercent: 108 });
  if (figs.length) G.set(figs, { yPercent: 104 });
  G.set([bar, footRule], { scaleX: 0, transformOrigin: '0% 50%' });
  G.set(abbr, { autoAlpha: 0 });
  G.set([inst, link], { autoAlpha: 0, y: 10 });
  G.set(labs, { autoAlpha: 0, y: 6 });
  G.set(seps, { borderLeftColor: 'rgba(224, 231, 242, 0)' });    // the ledger's column rules come in after its baseline
  // direction A: on desktop this ledger is the page's outcomes band, so its figures count up while they rise
  // (tabular figures, so the columns never shift; done by about 2.5 s; the final value is in an .sr twin)
  var counts = figs.map(function (f) { var n = parseInt(f.textContent, 10) || 0; f.textContent = '0'; return { el: f, n: n, v: 0 }; });
  showFinal();
  var tl = introTl = G.timeline({ defaults: { ease: EASE }, onComplete: function () {
    introDone = true; revertSplits();
    G.set([bar, footRule, abbr, inst, link].concat(labs, seps), { clearProps: 'transform,opacity,visibility,borderLeftColor' });
  } });
  tl.to(parts, { yPercent: 0, duration: L === 'ko' ? 1.25 : 1.15, stagger: L === 'ko' ? 0.06 : 0.065 }, 0.05)
    .to(bar, { scaleX: 1, duration: 1.1, ease: DRAW }, 0.42)
    .to(inst, { autoAlpha: 1, y: 0, duration: 0.9 }, 0.66)
    .to(sl.lines, { yPercent: 0, duration: 1.05, stagger: 0.08 }, 0.78)
    .to(footRule, { scaleX: 1, duration: 1.3, ease: DRAW }, 0.9)
    .to(abbr, { autoAlpha: 1, duration: 0.8, ease: 'power1.out' }, 1.22)
    .to(seps, { borderLeftColor: 'rgba(224, 231, 242, .24)', duration: 0.7, stagger: 0.08, ease: 'power1.out' }, 1.25)
    .to(link, { autoAlpha: 1, y: 0, duration: 0.85 }, 1.25)
    .to(labs, { autoAlpha: 1, y: 0, duration: 0.85, stagger: 0.08 }, 1.38);
  if (figs.length) tl.to(figs, { yPercent: 0, duration: 1, stagger: 0.08 }, 1.18);
  counts.forEach(function (c, i) {
    tl.to(c, { v: c.n, duration: 0.95, ease: 'power3.out', onUpdate: function () { c.el.textContent = String(Math.round(c.v)); } }, 1.18 + i * 0.06);
  });
}

/* =============================================================== 2. media */
var SRC = 'https://video.wixstatic.com/video/b8629b_b4d81b25a9d641439ec983afe489fd43/480p/mp4/file.mp4';
// Two continuous takes of the film, each kept clear of the editor's cuts:
//  A  an ENT clinician examines a patient's ear with an endoscope (2:53.2 to 2:57.75, the cut is at 2:57.75)
//  B  hands on a pure-tone audiometer, close up (1:52.06 to 1:54.24, hard cuts at 1:52.00 and 1:54.29), desktop only
// crop: the usable part of the frame (x0, y0, x1, y1): subtitles and caption labels are burned into the bottom.
// fx, fy: where the crop is anchored when the hero cuts into it. ear: the ear under examination, where the picture
// starts to develop (frame uv, measured on frames at 2:53.4, 2:55.8 and 2:57.2).
var SHOTS = [
  { t0: 173.2, t1: 177.75, rate: 0.8, fx: 0.72, fy: 0.5, crop: [0, 0, 1, 0.8], ear: [0.47, 0.32] },
  { t0: 112.06, t1: 114.24, rate: 0.7, fx: 0.9, fy: 0.4, crop: [0, 0, 1, 0.78] }
];
if (phone) SHOTS = SHOTS.slice(0, 1);
// the develop starts with the name (not after it) and front-loads its tones, so the picture is there inside the
// first-screen budget (CLAUDE.md: 2.5 s); a smoothstep over 2.8 s showed almost nothing for its first second
var MIX = 1.7, DEVELOP = 2.4, DEV_AT = 0.45;     // seconds
function devCurve(x) { return 1 - Math.pow(1 - x, 2.2); }
var vids = $$('.hx-v'), canvas = $('.hx-gl'), media = $('.hx-media'), film = $('.hx-film'), ctl = $('.hx-ctl');
var userPaused = false, onScreen = true, tabOn = !doc.hidden, introAt = 0, failed = false;
function still() {
  failed = true;
  hero.classList.remove('is-gl', 'is-dev'); hero.classList.add('is-still');
  vids.forEach(function (v) { try { v.pause(); v.removeAttribute('src'); v.load(); } catch (e) {} });
  if (ctl) ctl.hidden = true;
  stopLoop();
}

/* ---- WebGL: navy gradient map, tonal edge toward the text, develop out of the ear, luminance dissolve, grain */
var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';
var FS = [
  '#ifdef GL_FRAGMENT_PRECISION_HIGH', 'precision highp float;', '#else', 'precision mediump float;', '#endif',
  'uniform sampler2D uA,uB;uniform vec2 uRes,uSrc,uEar;uniform vec4 uCA,uCB;uniform vec3 uVA,uVB,uFade;',
  'uniform float uMix,uDev,uRad,uDim,uSeed;uniform vec3 uG,uC0,uC1,uC2,uC3;',
  // object-fit: cover of the usable crop c (frame uv), anchored at v.xy, zoomed by v.z
  'vec2 cover(vec2 uv,vec3 v,vec4 c){vec2 cs=(c.zw-c.xy)*uSrc;float ca=uRes.x/uRes.y,sa=cs.x/cs.y;',
  ' vec2 s=ca>sa?vec2(1.0,sa/ca):vec2(ca/sa,1.0);s/=v.z;vec2 o=(1.0-s)*v.xy;return c.xy+(o+uv*s)*(c.zw-c.xy);}',
  'float lum(vec3 c){return dot(c,vec3(0.2126,0.7152,0.0722));}',
  // a light unsharp mask on luminance: the 480p source holds up better at hero size
  'float tone(sampler2D t,vec2 uv){vec2 d=1.0/uSrc;float c=lum(texture2D(t,uv).rgb);',
  ' float b=lum(texture2D(t,uv+vec2(d.x,0.0)).rgb)+lum(texture2D(t,uv-vec2(d.x,0.0)).rgb)+lum(texture2D(t,uv+vec2(0.0,d.y)).rgb)+lum(texture2D(t,uv-vec2(0.0,d.y)).rgb);',
  ' return clamp(c+0.42*(c-0.25*b),0.0,1.0);}',
  'float h(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}',
  'float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(h(i),h(i+vec2(1.0,0.0)),f.x),mix(h(i+vec2(0.0,1.0)),h(i+vec2(1.0,1.0)),f.x),f.y);}',
  'vec3 ramp(float l){vec3 c=mix(uC0,uC1,smoothstep(0.0,0.42,l));c=mix(c,uC2,smoothstep(0.34,0.76,l));return mix(c,uC3,smoothstep(0.7,1.0,l));}',
  // a = 0: nothing of the image; a = 1: all of it. w: width of the front. Pixels with a higher key come through first.
  'float reveal(float a,float key,float w){float e=a*(1.0+w);return smoothstep(1.0-e,1.0+w-e,key);}',
  'void main(){vec2 uv=vec2(gl_FragCoord.x/uRes.x,1.0-gl_FragCoord.y/uRes.y);',
  ' vec2 q=uv*vec2(uRes.x/uRes.y,1.0);float n=vn(q*4.0)*0.65+vn(q*11.0)*0.35;',
  ' vec2 sa=cover(uv,uVA,uCA);float la=tone(uA,sa);float l=la;',
  ' if(uMix>0.0){float lb=tone(uB,cover(uv,uVB,uCB));l=mix(la,lb,reveal(uMix,lb*0.7+n*0.3,0.26));}',
  ' l=smoothstep(0.03,0.95,l);',
  // low key: a soft radial falloff and a darker top, so the title stays the brightest thing in the frame
  ' float r=length((uv-vec2(0.68,0.46))*vec2(1.0,0.8));vec3 col=ramp(l)*(1.0-0.22*smoothstep(0.32,0.95,r))*(1.0-0.2*(1.0-smoothstep(0.0,0.42,uv.y)));',
  ' float edge=mix(1.0,smoothstep(uFade.x,uFade.y,uv.x),uFade.z);',
  // the develop: a front travels out of the ear under examination; inside it the brightest tones lead
  ' float ear=1.0-clamp(length((sa-uEar)*vec2(uSrc.x/uSrc.y,1.0))/1.15,0.0,1.0);',
  ' float dk=mix(l*0.68+n*0.32,ear*0.62+l*0.32+n*0.06,uRad);',
  ' col=mix(uG,col,reveal(uDev,dk,mix(0.26,0.12,uRad))*reveal(edge,l*0.86+n*0.14,0.26));',
  ' col=mix(col,uG,uDim);',
  ' float g=dot(col,vec3(0.3,0.59,0.11));col+=(h(gl_FragCoord.xy+uSeed*61.7)-0.5)*0.045*(0.5+0.9*g);',
  ' gl_FragColor=vec4(col,1.0);}'
].join('\n');
function hex(c) { return [parseInt(c.slice(1, 3), 16) / 255, parseInt(c.slice(3, 5), 16) / 255, parseInt(c.slice(5, 7), 16) / 255]; }
// one hue family: the ground is the hero's own navy (#081a38), highlights stop short of the title's paper white
var TONES = { g: hex('#081a38'), c0: hex('#040d22'), c1: hex('#12305f'), c2: hex('#4b6ea8'), c3: hex('#bccbe2') };
function makeGL(cv) {
  var gl;
  try { gl = cv.getContext('webgl', { alpha: false, antialias: false, depth: false, stencil: false, premultipliedAlpha: false, powerPreference: 'low-power' }); } catch (e) { gl = null; }
  if (!gl) return null;
  function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); } return s; }
  var pr = gl.createProgram();
  gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
  gl.useProgram(pr);
  var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  var U = {};
  ['uA', 'uB', 'uRes', 'uSrc', 'uEar', 'uCA', 'uCB', 'uVA', 'uVB', 'uFade', 'uMix', 'uDev', 'uRad', 'uDim', 'uSeed', 'uG', 'uC0', 'uC1', 'uC2', 'uC3'].forEach(function (n) { U[n] = gl.getUniformLocation(pr, n); });
  var tex = [0, 1].map(function (i) {
    var t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, 1, 1, 0, gl.RGB, gl.UNSIGNED_BYTE, new Uint8Array([8, 26, 56]));
    return t;
  });
  gl.uniform1i(U.uA, 0); gl.uniform1i(U.uB, 1);
  gl.uniform2f(U.uSrc, 854, 480); gl.uniform2f(U.uEar, SHOTS[0].ear[0], SHOTS[0].ear[1]);
  gl.uniform3fv(U.uG, TONES.g); gl.uniform3fv(U.uC0, TONES.c0); gl.uniform3fv(U.uC1, TONES.c1); gl.uniform3fv(U.uC2, TONES.c2); gl.uniform3fv(U.uC3, TONES.c3);
  return {
    gl: gl,
    size: function () {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.25), w = Math.max(2, Math.round(cv.clientWidth * dpr)), hh = Math.max(2, Math.round(cv.clientHeight * dpr));
      if (cv.width !== w || cv.height !== hh) { cv.width = w; cv.height = hh; }
      gl.viewport(0, 0, w, hh); gl.uniform2f(U.uRes, w, hh);
    },
    upload: function (i, v) {
      gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex[i]);
      try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, v); } catch (e) {}
    },
    // a = index of the outgoing (or only) video, b = incoming
    draw: function (a, b, s) {
      gl.uniform1i(U.uA, a); gl.uniform1i(U.uB, b);
      gl.uniform3f(U.uVA, s.va[0], s.va[1], s.va[2]); gl.uniform3f(U.uVB, s.vb[0], s.vb[1], s.vb[2]);
      gl.uniform4f(U.uCA, s.ca[0], s.ca[1], s.ca[2], s.ca[3]); gl.uniform4f(U.uCB, s.cb[0], s.cb[1], s.cb[2], s.cb[3]);
      gl.uniform3f(U.uFade, s.fade[0], s.fade[1], 1);
      gl.uniform1f(U.uMix, s.mix); gl.uniform1f(U.uDev, s.dev); gl.uniform1f(U.uRad, s.rad); gl.uniform1f(U.uDim, s.dim); gl.uniform1f(U.uSeed, s.seed);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
  };
}

/* ---- the loop: two takes, double-buffered so a seek never shows; GL or CSS renders the result */
var ui = { mix: 0, dev: 0, rad: 1, dim: 0, seed: 0, va: [0.72, 0.5, 1], vb: [0.72, 0.5, 1], ca: SHOTS[0].crop, cb: SHOTS[0].crop, fade: [0.36, 0.7] };
var fadeTo = [0.36, 0.7];
var cur = 0, si = 0, mixing = false, mixT0 = 0, primed = [false, false], fresh = [false, false];
var R3 = null, raf = 0, devT0 = -1, lastSeed = 0, lastT = 0, started = false, developing = false, dimDirty = false;
function now() { return (window.performance && performance.now ? performance.now() : Date.now()) / 1000; }
function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
function nextOf(i) { return (i + 1) % SHOTS.length; }
// where the image may come through in full: just right of the text column, measured, so it follows the language
function measureFade() {
  var hb = hero.getBoundingClientRect(), W = hb.width || 1, right = 0;
  [$('.hx-lockup'), $('.hx-lead [data-l="' + lang() + '"]')].forEach(function (el) {
    var b = el && el.getBoundingClientRect();
    if (b && b.width) right = Math.max(right, b.right - hb.left);
  });
  if (!right) return;
  // bright tones pass the edge first, so the edge starts at the text's own right margin, not before it
  var x0 = Math.min(0.56, Math.max(0.3, right / W - 0.05));
  fadeTo = [x0, x0 + 0.34];
  if (!raf) { ui.fade = fadeTo.slice(); if (R3) R3.draw(cur, 1 - cur, ui); }
}
function prime(i, shot, cb) {
  var v = vids[i];
  primed[i] = false;
  function done() { v.removeEventListener('seeked', done); v.playbackRate = shot.rate; primed[i] = true; fresh[i] = true; if (cb) cb(); }
  function seek() { v.addEventListener('seeked', done); try { v.currentTime = shot.t0; } catch (e) { v.removeEventListener('seeked', done); } }
  if (v.readyState >= 1) seek();
  else v.addEventListener('loadedmetadata', function lm() { v.removeEventListener('loadedmetadata', lm); seek(); });
}
function watchFrames(i) {
  var v = vids[i];
  if (v.requestVideoFrameCallback) { var f = function () { fresh[i] = true; v.requestVideoFrameCallback(f); }; v.requestVideoFrameCallback(f); }
}
function play(v) { var p; try { p = v.play(); } catch (e) {} if (p && p.catch) p.catch(function () { if (!developing) still(); }); }
// the frame is anchored per take and drifts very slowly (one breath every ~40 s); the first view settles from 1.07
function view(shot, t) {
  var settle = devT0 < 0 ? 0 : Math.min(1, (t - devT0) / 7);
  var z = 1.012 + 0.022 * (0.5 - 0.5 * Math.cos(t * 0.16)) + 0.07 * Math.pow(1 - settle, 3);
  return [Math.min(0.98, shot.fx + 0.025 * Math.sin(t * 0.11)), shot.fy, z];
}
function frame() {
  raf = 0;
  if (!active()) return;
  var t = now(), dt = lastT ? Math.min(0.1, t - lastT) : 0, shot = SHOTS[si], A = vids[cur], nx = 1 - cur, nShot = SHOTS[nextOf(si)], B = vids[nx];
  lastT = t;
  var left = (shot.t1 - A.currentTime) / shot.rate;
  if (!mixing && primed[nx] && left <= MIX + 0.12) {
    mixing = true; mixT0 = t; play(B);
    if (!R3) { A.classList.remove('is-top'); B.classList.add('is-top', 'is-on'); }
  }
  if (A.currentTime >= shot.t1 - 0.03 && !A.paused) A.pause();      // never run into the editor's next cut
  var m = mixing ? Math.min(1, (t - mixT0) / MIX) : 0;
  ui.mix = ease(m);
  ui.va = view(shot, t); ui.vb = view(nShot, t); ui.ca = shot.crop; ui.cb = nShot.crop;
  var moving = mixing || (devT0 >= 0 && t - devT0 < 7);              // a transition is running: draw every frame
  if (devT0 >= 0) ui.dev = devCurve(Math.min(1, (t - devT0) / DEVELOP));
  var k = 1 - Math.exp(-dt * 4), f0 = ui.fade[0];
  ui.fade[0] += (fadeTo[0] - ui.fade[0]) * k; ui.fade[1] += (fadeTo[1] - ui.fade[1]) * k;
  if (Math.abs(ui.fade[0] - f0) > 1e-4) moving = true;
  var tick = false;
  if (t - lastSeed > 1 / 24) { ui.seed = (ui.seed + 0.6180339) % 1; lastSeed = t; tick = true; }   // grain at film rate
  if (R3) {
    if (fresh[cur] && A.readyState >= 2) { R3.upload(cur, A); fresh[cur] = !A.requestVideoFrameCallback; }
    if (mixing && fresh[nx] && B.readyState >= 2) { R3.upload(nx, B); fresh[nx] = !B.requestVideoFrameCallback; }
    // between transitions the picture changes at film rate only (new frames, grain): redraw on that tick, not at 60 fps
    if (moving || tick || dimDirty) { R3.draw(cur, nx, ui); dimDirty = false; }
  }
  if (mixing && m >= 1) {             // hand over: the incoming take becomes current, the old one seeks to the take after
    mixing = false; ui.mix = 0;
    A.pause();
    if (!R3) { A.style.transition = 'none'; A.classList.remove('is-on'); requestAnimationFrame(function () { A.style.transition = ''; }); }
    cur = nx; si = nextOf(si);
    prime(1 - cur, SHOTS[nextOf(si)]);
  }
  raf = requestAnimationFrame(frame);
}
function active() { return developing && !userPaused && onScreen && tabOn && !failed; }
function startLoop() {
  if (raf || !active()) return;
  var v = vids[cur];
  if (v.paused && v.currentTime < SHOTS[si].t1 - 0.05) play(v);
  if (mixing) play(vids[1 - cur]);
  lastT = 0;
  raf = requestAnimationFrame(frame);
}
function stopLoop() { if (raf) cancelAnimationFrame(raf); raf = 0; vids.forEach(function (v) { if (!v.paused) v.pause(); }); }
function sync() { if (active()) startLoop(); else stopLoop(); }
// phones (no WebGL): the CSS-toned picture opens out of the ear as a widening circle
function phoneDevelop() {
  var v = vids[cur], bw = v.clientWidth, bh = v.clientHeight, fh = film.clientHeight;
  if (!G || !bw || !bh) return;
  var s = Math.max(bw / 854, bh / 480), dw = 854 * s, dh = 480 * s;
  var ex = (bw - dw) * 0.64 + SHOTS[0].ear[0] * dw, ey = SHOTS[0].ear[1] * dh;    // object-position: 64% 0% (hero.css)
  var fx = Math.max(ex, bw - ex), fy = Math.max(ey, fh - ey);
  hero.style.setProperty('--hx-ex', ex.toFixed(1) + 'px'); hero.style.setProperty('--hx-ey', ey.toFixed(1) + 'px');
  film.style.setProperty('--hx-r', '0px');
  hero.classList.add('is-dev');
  G.to(film, { '--hx-r': Math.ceil(Math.sqrt(fx * fx + fy * fy) + 120) + 'px', duration: 2.4, ease: 'power1.out',
    onComplete: function () { hero.classList.remove('is-dev'); film.style.removeProperty('--hx-r'); } });
}
// the first take develops only when it is decoded AND the title has had its first beat
function develop() {
  if (developing || failed || !started || !introAt) return;
  var wait = Math.max(0, introAt + DEV_AT - now());   // as the first characters of the name rise
  setTimeout(function () {
    if (developing || failed) return;
    developing = true; devT0 = now();
    if (!R3) { phoneDevelop(); vids[cur].classList.add('is-top', 'is-on'); hero.classList.add('is-live'); }
    if (ctl) { ctl.hidden = false; if (G) G.fromTo(ctl, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.8, delay: 0.8 }); }
    sync();
  }, wait * 1000);
}
function bootMedia() {
  if (reduce || thrifty || !vids.length) { hero.classList.add('is-still'); return; }
  if (!phone) {
    try { R3 = makeGL(canvas); } catch (e) { R3 = null; }
    if (R3) {
      R3.size(); measureFade(); R3.draw(0, 1, ui);   // the canvas's first paint is the navy ground itself
      hero.classList.add('is-gl');
      canvas.addEventListener('webglcontextlost', function (e) { e.preventDefault(); R3 = null; hero.classList.remove('is-gl'); hero.classList.add('is-live'); vids[cur].classList.add('is-top', 'is-on'); }, false);
      var rz = 0;
      window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (R3) { R3.size(); measureFade(); if (!raf) R3.draw(cur, 1 - cur, ui); } }, 120); });
      if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { if (R3) measureFade(); });
    }
  }
  vids.forEach(function (v, i) {
    v.muted = true;
    v.addEventListener('error', function () { if (!developing || i === cur) still(); });
    watchFrames(i);
  });
  var giveUp = setTimeout(function () { if (!started) still(); }, 9000);
  // data budget (CLAUDE.md): the film is 21.2 MB and a playing <video> reads megabytes ahead of any seek, so the
  // takes are fetched as byte ranges and repacked into small in-memory clips (about 1.1 MB in all, see clips())
  var cl = clips(SRC);
  cl.get(0).then(function (url) {
    if (failed) return;
    vids[0].src = url;
    prime(0, SHOTS[0], function () {
      clearTimeout(giveUp);
      if (failed) return;
      started = true;
      if (R3 && vids[0].readyState >= 2) { R3.upload(0, vids[0]); fresh[0] = false; R3.draw(0, 1, ui); }
      develop();
      // the second buffer gets the next take's clip while the first one plays (one more range request, or none on phones)
      cl.get(nextOf(0)).then(function (u2) { if (failed) return; vids[1].src = u2; prime(1, SHOTS[nextOf(0)]); }, function () { if (SHOTS.length > 1) SHOTS = SHOTS.slice(0, 1); vids[1].src = url; prime(1, SHOTS[0]); });
    });
  }, function () { still(); });
}

/* ---- the takes as small clips. Only three byte ranges of the film are ever requested: the moov (sample tables),
   then each take's video samples from the keyframe before it. They are written into a minimal MP4 (ftyp, moov
   with one video track, mdat) and played from a Blob URL, so the players never touch the 21 MB file. A clip's time
   starts at that keyframe: the take's t0/t1 are shifted to it. Any failure rejects (the caller shows the still). */
function clips(src) {
  var TE = new TextEncoder(), moov = null, made = {};
  function get(a, b) {
    return fetch(src, { headers: { Range: 'bytes=' + a + '-' + b }, credentials: 'omit' }).then(function (r) {
      if (r.status !== 206) { try { r.body && r.body.cancel(); } catch (e) {} throw new Error('no range support: ' + r.status); }
      return r.arrayBuffer();
    }).then(function (ab) { return new Uint8Array(ab); });
  }
  function kids(u, s, e) {
    var dv = new DataView(u.buffer, u.byteOffset, u.byteLength), out = [], i = s;
    while (i + 8 <= e) {
      var sz = dv.getUint32(i), hl = 8, t = String.fromCharCode(u[i + 4], u[i + 5], u[i + 6], u[i + 7]);
      if (sz === 1) { sz = dv.getUint32(i + 8) * 4294967296 + dv.getUint32(i + 12); hl = 16; } else if (sz === 0) sz = e - i;
      if (sz < hl) break;
      out.push({ t: t, s: i, e: i + sz, b: i + hl }); i += sz;
    }
    return out;
  }
  function child(u, x, t) { var k = x ? kids(u, x.b, x.e) : []; for (var i = 0; i < k.length; i++) if (k[i].t === t) return k[i]; return null; }
  function path(u, x, ts) { for (var i = 0; i < ts.length && x; i++) x = child(u, x, ts[i]); return x; }
  // the video track's sample tables, flattened per sample
  function parse(u, mv) {
    var dv = new DataView(u.buffer, u.byteOffset, u.byteLength), tr = null;
    kids(u, mv.b, mv.e).forEach(function (k) {
      var h = k.t === 'trak' && path(u, k, ['mdia', 'hdlr']);
      if (h && !tr && String.fromCharCode(u[h.b + 8], u[h.b + 9], u[h.b + 10], u[h.b + 11]) === 'vide') tr = k;
    });
    if (!tr) throw new Error('no video track');
    var md = path(u, tr, ['mdia', 'mdhd']), tk = child(u, tr, 'tkhd'), st = path(u, tr, ['mdia', 'minf', 'stbl']), el = path(u, tr, ['edts', 'elst']);
    var B = function (t) { return child(u, st, t); }, stsz = B('stsz'), stts = B('stts'), ctts = B('ctts'), stss = B('stss'), stsc = B('stsc'), stco = B('stco'), co64 = B('co64');
    var o = { ts: dv.getUint32(md.b + (u[md.b] === 1 ? 20 : 12)), stsd: u.slice(B('stsd').s, B('stsd').e), wh: u.slice(tk.b + (u[tk.b] === 1 ? 88 : 76), tk.b + (u[tk.b] === 1 ? 96 : 84)) };
    var n = dv.getUint32(stsz.b + 8), fx = dv.getUint32(stsz.b + 4), i, j, k, e, c;
    o.n = n; o.size = []; o.dts = []; o.dur = []; o.cto = []; o.sync = null; o.off = [];
    for (i = 0; i < n; i++) o.size.push(fx || dv.getUint32(stsz.b + 12 + 4 * i));
    for (e = 0, k = 0, c = 0; e < dv.getUint32(stts.b + 4); e++) for (j = 0; j < dv.getUint32(stts.b + 8 + 8 * e) && k < n; j++, k++) { o.dts.push(c); o.dur.push(dv.getUint32(stts.b + 12 + 8 * e)); c += o.dur[k]; }
    for (i = 0; i < n; i++) o.cto.push(0);
    o.cv = ctts ? u[ctts.b] : 0;
    if (ctts) for (e = 0, k = 0; e < dv.getUint32(ctts.b + 4); e++) for (j = 0; j < dv.getUint32(ctts.b + 8 + 8 * e) && k < n; j++, k++) o.cto[k] = o.cv === 1 ? dv.getInt32(ctts.b + 12 + 8 * e) : dv.getUint32(ctts.b + 12 + 8 * e);
    if (stss) { o.sync = {}; for (e = 0; e < dv.getUint32(stss.b + 4); e++) o.sync[dv.getUint32(stss.b + 8 + 4 * e) - 1] = 1; }
    var cb = stco || co64, nch = dv.getUint32(cb.b + 4), ent = [];
    for (e = 0; e < dv.getUint32(stsc.b + 4); e++) ent.push([dv.getUint32(stsc.b + 8 + 12 * e) - 1, dv.getUint32(stsc.b + 12 + 12 * e)]);
    for (var ch = 0, s = 0, q = 0; ch < nch && s < n; ch++) {
      while (q + 1 < ent.length && ent[q + 1][0] <= ch) q++;
      var at = stco ? dv.getUint32(cb.b + 8 + 4 * ch) : dv.getUint32(cb.b + 8 + 8 * ch) * 4294967296 + dv.getUint32(cb.b + 12 + 8 * ch);
      for (j = 0; j < ent[q][1] && s < n; j++, s++) { o.off.push(at); at += o.size[s]; }
    }
    o.mt = 0;
    if (el) o.mt = Math.max(0, u[el.b] === 1 ? dv.getUint32(el.b + 16) * 4294967296 + dv.getUint32(el.b + 20) : dv.getInt32(el.b + 12));
    return o;
  }
  function be(x) { return [x >>> 24 & 255, x >>> 16 & 255, x >>> 8 & 255, x & 255]; }
  function cat(parts) { var len = 0, i, o = 0; for (i = 0; i < parts.length; i++) len += parts[i].length; var out = new Uint8Array(len); for (i = 0; i < parts.length; i++) { out.set(parts[i], o); o += parts[i].length; } return out; }
  function box(t, parts) { var body = cat(parts); return cat([new Uint8Array(be(body.length + 8)), TE.encode(t), body]); }
  function full(t, vf, parts) { return box(t, [new Uint8Array(be(vf))].concat(parts)); }
  function words(a) { var out = []; a.forEach(function (x) { out = out.concat(be(x)); }); return new Uint8Array(out); }
  function runs(a) { var r = []; a.forEach(function (x) { if (r.length && r[r.length - 1][1] === x) r[r.length - 1][0]++; else r.push([1, x]); }); return r; }
  var MAT = [0x10000, 0, 0, 0, 0x10000, 0, 0, 0, 0x40000000];
  // one take: samples from the keyframe at or before t0 to everything decoded before t1 (+ B-frame margin)
  function clip(o, shot) {
    var pt = function (j) { return (o.dts[j] + o.cto[j] - o.mt) / o.ts; }, i0 = -1, i1, j;
    for (j = 0; j < o.n && o.dts[j] / o.ts < shot.t0 + 1; j++) if ((!o.sync || o.sync[j]) && pt(j) <= shot.t0 + 1e-6) i0 = j;
    if (i0 < 0) throw new Error('no keyframe');
    for (i1 = i0; i1 + 1 < o.n && o.dts[i1 + 1] / o.ts < shot.t1 + 0.35; i1++);
    var lo = Infinity, hi = 0;
    for (j = i0; j <= i1; j++) { lo = Math.min(lo, o.off[j]); hi = Math.max(hi, o.off[j] + o.size[j]); }
    return get(lo, hi - 1).then(function (raw) {
      var N = i1 - i0 + 1, data = [], dur = 0, ctos = [], sync = [], sizes = [];
      for (j = i0; j <= i1; j++) { data.push(raw.subarray(o.off[j] - lo, o.off[j] - lo + o.size[j])); dur += o.dur[j]; ctos.push(o.cto[j]); sizes.push(o.size[j]); if (!o.sync || o.sync[j]) sync.push(j - i0 + 1); }
      var lead = o.cto[i0], show = Math.max(1, dur - lead), neg = ctos.some(function (x) { return x < 0; });
      var stts = runs(o.dur.slice(i0, i1 + 1)), ctr = runs(ctos);
      function moovFor(mdatAt) {
        var stbl = box('stbl', [o.stsd,
          full('stts', 0, [words([stts.length].concat([].concat.apply([], stts)))]),
          full('ctts', neg ? 0x01000000 : 0, [words([ctr.length].concat([].concat.apply([], ctr.map(function (r) { return [r[0], r[1] >>> 0]; }))))]),
          full('stss', 0, [words([sync.length].concat(sync))]),
          full('stsc', 0, [words([1, 1, N, 1])]),
          full('stsz', 0, [words([0, N].concat(sizes))]),
          full('stco', 0, [words([1, mdatAt])])]);
        var minf = box('minf', [full('vmhd', 1, [new Uint8Array(8)]), box('dinf', [full('dref', 0, [words([1]), full('url ', 1, [])])]), stbl]);
        var mdia = box('mdia', [full('mdhd', 0, [words([0, 0, o.ts, dur]), new Uint8Array([0x55, 0xc4, 0, 0])]),
          full('hdlr', 0, [words([0]), TE.encode('vide'), new Uint8Array(12), TE.encode('VideoHandler\u0000')]), minf]);
        var trak = box('trak', [full('tkhd', 3, [words([0, 0, 1, 0, show, 0, 0, 0, 0]), words(MAT), o.wh]),
          box('edts', [full('elst', 0, [words([1, show, lead, 0x10000])])]), mdia]);
        return box('moov', [full('mvhd', 0, [words([0, 0, o.ts, show, 0x10000]), new Uint8Array([1, 0]), new Uint8Array(10), words(MAT), new Uint8Array(24), words([2])]), trak]);
      }
      var ftyp = box('ftyp', [TE.encode('isom'), new Uint8Array(be(512)), TE.encode('isomiso2avc1mp41')]);
      var size0 = moovFor(0).length, mdat = cat(data);
      var file = [ftyp, moovFor(ftyp.length + size0 + 8), new Uint8Array(be(mdat.length + 8)), TE.encode('mdat'), mdat];
      var off = pt(i0);
      shot.t0 -= off; shot.t1 -= off;          // clip time 0 is the keyframe's presentation time
      return URL.createObjectURL(new Blob(file, { type: 'video/mp4' }));
    });
  }
  function head() {
    if (moov) return moov;
    return (moov = get(0, 262143).then(function (u) {
      var top = kids(u, 0, u.length), mv = null;
      top.forEach(function (k) { if (k.t === 'moov') mv = k; });
      if (!mv) throw new Error('moov not at the start');
      if (mv.e <= u.length) return parse(u, mv);
      return get(mv.s, mv.e - 1).then(function (m) { return parse(m, { t: 'moov', s: 0, e: m.length, b: mv.b - mv.s }); });
    }));
  }
  return { get: function (k) { return made[k] || (made[k] = head().then(function (o) { return clip(o, SHOTS[k]); })); } };
}

/* =============================================================== 3. pause control, language, visibility */
function label() {
  if (!ctl) return;
  var on = !userPaused;
  ctl.setAttribute('aria-label', ctl.getAttribute('data-' + lang() + (on ? '-on' : '-off')));
  ctl.classList.toggle('is-paused', !on);
}
if (ctl) {
  ctl.addEventListener('click', function () { userPaused = !userPaused; label(); sync(); });
  label();
}
if (R.onLang) R.onLang(function () {
  label();
  // a language change while the masthead is still setting itself: finish at once, fade the new language in
  if (introTl && !introDone) {
    introTl.progress(1);
    if (G) G.fromTo($('.hx-copy'), { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.45, ease: 'power1.out' });
  }
  if (R3) requestAnimationFrame(measureFade);
});
if (R.visible) R.visible(hero, function (on) { onScreen = on; sync(); });
doc.addEventListener('visibilitychange', function () { tabOn = !doc.hidden; sync(); });

/* =============================================================== 4. scroll hand-off (sentinel band, never window scroll) */
if (!reduce && R.onBand && R.rect) {
  var box = R.rect(hero), lastOff = -1;
  window.addEventListener('resize', function () { box = R.rect(hero); });
  R.onBand(function (b) {
    if (!b.ok) return;
    var off = Math.max(0, Math.min(box.h, b.top - box.top));
    if (Math.abs(off - lastOff) < 0.5) return;
    lastOff = off;
    media.style.transform = off ? 'translate3d(0,' + (off * 0.22).toFixed(1) + 'px,0)' : '';
    ui.dim = 0.55 * (off / box.h); dimDirty = true;
    if (R3 && !raf && developing) R3.draw(cur, 1 - cur, ui);
  });
}

/* =============================================================== go */
function go() { introAt = now(); whenFonts(intro); develop(); }
if (reduce) { showFinal(); introDone = true; hero.classList.add('is-still'); }
else if (late || !G) {
  // read how far the CSS safety fade has got before claiming the hero (claiming stops it), then finish from there
  var blocks = $$('[data-a]'), ops = blocks.map(function (el) { return parseFloat(getComputedStyle(el).opacity) || 0; });
  showFinal(); hero.classList.add('is-run'); introDone = true;
  if (G) blocks.forEach(function (el, i) { if (ops[i] < 0.98) G.fromTo(el, { opacity: ops[i] }, { opacity: 1, duration: 0.25 + 0.5 * (1 - ops[i]), ease: 'power1.out', clearProps: 'opacity' }); });
  bootMedia(); introAt = now(); develop();
}
else {
  hero.classList.add('is-run');          // from here on the intro owns the reveals: the CSS safety fade stands down
  bootMedia();
  if (R.inview) R.inview(hero, go, { threshold: 0.05, px: 60 }); else go();
}
