// Shared beret TikTok template. Each page sets window.CFG before loading this file.
// Scenes: hook (fan of berets) → optional features → one colour per second → all colours → end card. No audio.
const C = window.CFG;
const $ = id => document.getElementById(id);
const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eo = x => 1 - Math.pow(1 - cl(x), 3);
const bk = x => { x = cl(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const pop = (el, t, t0, d = .35, from = .6) => { const k = bk((t - t0) / d); el.style.opacity = cl((t - t0) / (d * .5)); el.style.transform = `scale(${from + (1 - from) * k})`; };
const rise = (el, t, t0, d = .4, dy = 60) => { const k = eo((t - t0) / d); el.style.opacity = k; el.style.transform = `translateY(${dy * (1 - k)}px)`; };

// timeline
const T = {}; let t0 = 0;
T.s1 = [t0, t0 += 3.0];
if (C.features) T.s2 = [t0, t0 += 2.5];
T.s3 = [t0, t0 += C.cols.length];
T.s4 = [t0, t0 += 3.0];
T.s5 = [t0, t0 += 3.5];
window.DURATION = t0;

const STRIPES = '<div class="a stripes" style="top:0"></div><div class="a stripes" style="bottom:0"></div>';
document.body.innerHTML = `
<div class="sc" id="s1" style="background:#ffffff;color:#1b181d">${STRIPES}
  <img class="a" id="s1logo" src="img/mw-oval.png" style="left:420px;top:110px;width:240px">
  <div id="fan"></div>
  <div class="a ctr" id="s1tag" style="top:1180px"><span class="tag">${C.tag||"NEW IN"}</span></div>
  <div class="a ctr big" id="s1t1" style="top:1300px;text-shadow:none;color:#1b181d">${C.title1}</div>
  <div class="a ctr big" id="s1t2" style="top:1450px;color:#C3312B;text-shadow:none">${C.title2}</div>
  <div class="a ctr" id="s1sub" style="top:1640px;font-size:44px;font-weight:700;letter-spacing:6px;color:#1b181d">${C.hookSub || (C.cols.length+" COLOURS · R"+C.price)}</div>
</div>
${C.features ? `<div class="sc" id="s2" style="background:radial-gradient(circle at 50% 38%,#2c2630 0%,#1b181d 70%)">${STRIPES}
  <div class="a circ" id="s2ph" style="left:140px;top:250px;width:800px;height:800px;background-image:url(img/${C.featureImg})"></div>
  ${C.features.map((f, i) => `<div class="a ctr feat" id="f${i}" style="top:${1180 + i * 110}px"><span>✓</span> ${f}</div>`).join('')}
  <div class="a ctr serif" id="fq" style="top:${1200 + C.features.length * 110 + 40}px;font-size:84px">${C.featureLine}</div>
</div>` : ''}
<div class="sc" id="s3"><div class="a" id="s3bg" style="inset:0"></div>
  <div class="a" style="inset:0;background:radial-gradient(circle at 50% 38%,rgba(255,255,255,.65) 0%,rgba(255,255,255,0) 60%)"></div>${STRIPES}
  <div class="a ctr" id="s3n" style="top:140px;font-size:40px;font-weight:800;letter-spacing:10px"></div>
  <div class="a circ" id="s3ph" style="left:120px;top:300px;width:840px;height:840px"></div>
  <div class="a badge" id="s3b" style="left:760px;top:250px"><small>ONLY</small><b id="s3p">R${C.price}</b></div>
  <div class="a ctr big" id="s3name" style="top:1250px;font-size:128px;text-shadow:none"></div>
  <div class="a ctr" id="s3sub" style="top:1520px;font-size:40px;font-weight:700;letter-spacing:5px">${C.sub}</div>
</div>
<div class="sc" id="s4" style="background:#F6F0E9;color:#1b181d">${STRIPES}
  <div class="a ctr serif" id="s4t" style="top:120px;font-size:110px">${C.cols.length} colours.</div>
  <div class="a ctr" id="s4s" style="top:270px;font-size:46px;font-weight:800;letter-spacing:4px;color:#C3312B">${C.gridSub}</div>
  <div id="grid"></div>
</div>
<div class="sc" id="s5" style="background:radial-gradient(circle at 50% 35%,#2c2630 0%,#1b181d 70%)">${STRIPES}
  <img class="a" id="s5logo" src="img/mw-oval.png" style="left:290px;top:250px;width:500px">
  <div class="a ctr serif" id="s5t" style="top:760px;font-size:100px">${C.shopLine}</div>
  <div class="a ctr" id="s5url" style="top:910px"><span class="pill" style="font-size:84px;padding:26px 70px">makkies.co.za</span></div>
  <div class="a ctr" id="s5wa" style="top:1110px;font-size:56px;font-weight:800"><span style="color:#25D366">●</span> WhatsApp 072 323 5469</div>
  <div class="a ctr" id="s5d" style="top:1230px;font-size:40px;line-height:1.5;opacity:.9">Delivery across South Africa<br>PAXI to any PEP · or collect in Marabastad</div>
  <div class="a ctr" id="s5h" style="top:1480px;font-size:40px;font-weight:700;letter-spacing:4px;color:#FFC814">@makkiewholesalers</div>
</div>`;

// fan of berets for the hook
const FAN = C.fan, nF = FAN.length, fs = nF > 6 ? 360 : 420;
FAN.forEach((f, k) => {
  const x = 10 + (1080 - fs - 20) * k / (nF - 1), y = 560 + Math.pow(Math.abs(k - (nF - 1) / 2), 1.6) * 22, r = (k - (nF - 1) / 2) * 6;
  $('fan').insertAdjacentHTML('beforeend', `<div class="a circ" id="fb${k}" style="left:${x}px;top:${y}px;width:${fs}px;height:${fs}px;background-image:url(img/${f});--r:${r}deg"></div>`);
});
// grid: rows of up to 3, centred
C.cols.forEach((c, i) => {
  const row = Math.floor(i / 3), inRow = Math.min(3, C.cols.length - row * 3), col = i % 3, w = 300, gap = 50;
  const x = (1080 - (inRow * w + (inRow - 1) * gap)) / 2 + col * (w + gap);
  $('grid').insertAdjacentHTML('beforeend', `<div class="gcell" id="g${i}" style="left:${x}px;top:${420 + row * 430}px"><div class="circ" style="background-image:url(img/${c.grid})"></div><div class="nm">${c.name.toUpperCase()}</div></div>`);
});

function vis(id, t) { if (!T[id]) return; const [a, b] = T[id]; const fi = cl((t - a) / .12), fo = id === 's5' ? 1 : cl((b - t) / .12); $(id).style.opacity = (t >= a && t < b + 1e-4) ? Math.min(fi, fo) : 0; }
window.render = function (t) {
  ['s1', 's2', 's3', 's4', 's5'].forEach(id => vis(id, t));
  // S1 hook
  pop($('s1logo'), t, 0.1, .4, .4);
  FAN.forEach((f, k) => { const el = $('fb' + k), st = 0.2 + k * 0.12, q = bk((t - st) / .4);
    el.style.opacity = cl((t - st) / .15); el.style.transform = `translateY(${(1 - eo((t - st) / .45)) * 500}px) rotate(var(--r)) scale(${.7 + .3 * q})`; });
  pop($('s1tag'), t, 1.0, .35, .4); rise($('s1t1'), t, 1.2, .35, 120); rise($('s1t2'), t, 1.45, .35, 120); rise($('s1sub'), t, 1.8, .4, 40);
  // S2 features
  if (T.s2) { const a = T.s2[0], ph = $('s2ph'), k = bk((t - a) / .6);
    ph.style.opacity = cl((t - a) / .2); ph.style.transform = `rotate(${-140 * (1 - eo((t - a) / .8))}deg) scale(${.5 + .5 * k})`;
    C.features.forEach((f, i) => rise($('f' + i), t, a + .5 + i * .4, .3)); pop($('fq'), t, a + .5 + C.features.length * .4, .35, .8); }
  // S3 one colour per second
  const [a3, b3] = T.s3;
  if (t >= a3 && t < b3) { const i = Math.min(C.cols.length - 1, Math.floor(t - a3)), lt = (t - a3) - i, c = C.cols[i];
    $('s3bg').style.background = c.tint; ['s3name', 's3n', 's3sub'].forEach(id => $(id).style.color = c.ink);
    $('s3sub').textContent = c.sub || C.sub; $('s3n').textContent = String(i + 1).padStart(2, '0') + ' / ' + String(C.cols.length).padStart(2, '0');
    const ph = $('s3ph'); ph.style.backgroundImage = `url(img/${c.hero})`;
    ph.style.transform = `scale(${.7 + .3 * bk(lt / .35)}) rotate(${(1 - eo(lt / .5)) * -25}deg)`; ph.style.opacity = cl(lt / .12);
    $('s3p').textContent = 'R' + (c.price || C.price); $('s3name').textContent = c.name.toUpperCase(); rise($('s3name'), lt, 0.08, .3, 80);
    pop($('s3b'), lt, 0.15, .3, .5); $('s3b').style.transform += ' rotate(-10deg)'; }
  // S4 grid
  const a4 = T.s4[0]; pop($('s4t'), t, a4 + .05, .35, .7); rise($('s4s'), t, a4 + .3, .3, 40);
  C.cols.forEach((c, i) => pop($('g' + i), t, a4 + .4 + i * .12, .3, .3));
  // S5 end card
  const a5 = T.s5[0]; pop($('s5logo'), t, a5 + .05, .45, .3); rise($('s5t'), t, a5 + .4, .35, 60); pop($('s5url'), t, a5 + .7, .35, .5);
  if (t > a5 + 1.1) { const ph = (t - (a5 + 1.1)) / 0.6; const s = 1 + 0.16 * Math.pow(Math.sin(Math.PI * ph), 2); $('s5url').style.transform = `scale(${s})`; }
  rise($('s5wa'), t, a5 + 1.0, .3, 40); rise($('s5d'), t, a5 + 1.25, .3, 40); rise($('s5h'), t, a5 + 1.5, .3, 30);
};
render(0);
