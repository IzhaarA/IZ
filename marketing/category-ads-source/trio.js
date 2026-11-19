// Shared helpers for the trio-*.html TikTok videos (1080x1920, no audio). Each page sets window.DURATION and window.render(t).
const $ = id => document.getElementById(id), cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eo = x => 1 - Math.pow(1 - cl(x), 3), eio = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const bk = x => { x = cl(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const slam = (el, t, t0, d = .22, from = 2.2) => { const k = eo((t - t0) / d); el.style.opacity = cl((t - t0) / .05); el.style.transform = `scale(${from - (from - 1) * k})`; };
const pop = (el, t, t0, d = .35, from = .3, rot = 0) => { const k = bk((t - t0) / d); el.style.opacity = cl((t - t0) / .1); el.style.transform = `scale(${from + (1 - from) * k}) rotate(${rot}deg)`; };
const rise = (el, t, t0, d = .3, dy = 60) => { const k = eo((t - t0) / d); el.style.opacity = k; el.style.transform = `translateY(${dy * (1 - k)}px)`; };
const fade = (el, t, t0, d = .3) => { el.style.opacity = cl((t - t0) / d); };
const img = n => `img/${n}.jpg`;
const rnd = s => { const x = Math.sin(s * 999.7) * 43758.5453; return x - Math.floor(x); };
const preload = names => names.forEach(n => { const i = new Image(); i.src = img(n); });
// scenes: [['s1', dur], ...] -> {s1:[t0,t1], ...}; returns the id showing at t
function scenes(list) { const T = {}; let t = 0; list.forEach(([id, d]) => { T[id] = [t, t + d]; t += d; }); T.end = t; return T; }
function show(T, t) { const ids = Object.keys(T).filter(k => k !== 'end'); const cur = ids.find(id => t >= T[id][0] && t < T[id][1]) || ids[ids.length - 1];
  ids.forEach(id => $(id).style.opacity = id === cur ? 1 : 0); return [cur, t - T[cur][0]]; }
// confetti inside element `box`
function makeConf(box, n, colours) { for (let k = 0; k < n; k++) box.insertAdjacentHTML('beforeend', `<div class="conf" style="background:${colours[k % colours.length]}"></div>`); }
function conf(box, lt, x0 = 540, y0 = 700) { [...box.children].forEach((el, c) => { const d = lt; if (d < 0) { el.style.opacity = 0; return; }
  const ang = rnd(c) * Math.PI * 2, sp = 500 + rnd(c + 7) * 900, x = x0 + Math.cos(ang) * sp * d, y = y0 + Math.sin(ang) * sp * d * .8 + 1400 * d * d;
  el.style.opacity = cl(2.4 - d); el.style.left = x + 'px'; el.style.top = y + 'px'; el.style.transform = `rotate(${d * 720 * (rnd(c + 3) - .5)}deg)`; }); }
// count from a to b between t0 and t1
const count = (t, t0, t1, a, b) => Math.round(a + (b - a) * eio((t - t0) / (t1 - t0)));
const Rf = v => 'R' + v.toLocaleString('en-ZA').replace(/\s/g, ',');
// shrink a text element until it fits the width
function fit(el, max, start, min = 40) { let f = start; el.style.fontSize = f + 'px'; while (el.scrollWidth > max && f > min) { f -= 3; el.style.fontSize = f + 'px'; } }
