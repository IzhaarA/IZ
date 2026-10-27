// Category TikTok template, version 2. Each page sets window.CFG before loading this file. No audio.
// Scenes: hook → one product at a time (CFG.items) → optional colour set (CFG.set) → all products (CFG.grid) → end card.
// Soft backgrounds keep the products in front: every product scene starts with a striped wipe, the photo comes in on a
// white frame and slowly zooms, and the price lands as a sticker. CFG.per is the time per product, CFG.setPer per colour.
// CFG.look varies each video: pal (background/accent pairs), band (border images), hook ('fan' | 'hero' | 'mosaic'),
// enter ('right' | 'left' | 'up' | 'zoom'), sticker ('circle' | 'tag'), hl (title highlight colour), tilt (wipe angle).
// Optional, to keep viewers watching: CFG.q = ['LINE', 'LINE'] opens with a question over fast-flashing photos (CFG.qPhotos),
// CFG.ask puts a pulsing 'comment your number' line under the grid (grid tiles get numbers), CFG.endKick a banner on the end card.
const C = window.CFG, PER = C.per || 2.4, SPER = C.setPer || 1.7;
const L = Object.assign({ band: 'ndebele', hook: 'fan', enter: 'right', sticker: 'circle', hl: '#D8232A', tilt: -14 }, C.look || {});
const $ = id => document.getElementById(id);
const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eo = x => 1 - Math.pow(1 - cl(x), 3);
const eio = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const bk = x => { x = cl(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const show = (el, o) => { el.style.opacity = o; };
const pop = (el, t, t0, d = .35, from = .6, rot = 0) => { const k = bk((t - t0) / d); el.style.opacity = cl((t - t0) / (d * .5)); el.style.transform = `scale(${from + (1 - from) * k}) rotate(${rot}deg)`; };
const rise = (el, t, t0, d = .4, dy = 60) => { const k = eo((t - t0) / d); el.style.opacity = k; el.style.transform = `translateY(${dy * (1 - k)}px)`; };
const slam = (el, t, t0, d = .3) => { const k = eo((t - t0) / d); el.style.opacity = cl((t - t0) / .08); el.style.transform = `scale(${2.2 - 1.2 * k})`; };

// soft backgrounds so the products stand out; each product scene takes the next one, the accent colours the chip
const PAL = L.pal || [{ bg: '#E6ECF6', acc: '#0350EA' }, { bg: '#F6E6E3', acc: '#D8232A' }, { bg: '#E4F0E8', acc: '#05A463' }, { bg: '#F8EFD6', acc: '#C99400' }, { bg: '#EEE6F0', acc: '#45203F' }];
const INK = '#1b181d', CREAM = '#F6F0E9';
const STRIPE = 'linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96% 100%)';
// faint geometric Ndebele pattern drawn over the coloured backgrounds
const PAT = 'url("data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" fill="none" stroke="#000" stroke-width="7"><path d="M20 120h40v-40h40v-40h40v40h40v40h40M20 120h40v40h40v40h40v-40h40v-40h40"/><rect x="104" y="104" width="32" height="32"/></svg>') + '")';

// timeline
const T = {}; let t0 = 0;
if (C.q) T.q = [t0, t0 += 2.1];
T.hook = [t0, t0 += 3.6];
C.items.forEach((it, i) => T['i' + i] = [t0, t0 += PER]);
if (C.set) { T.set = [t0, t0 += .9 + C.set.cols.length * SPER]; }
T.grid = [t0, t0 += 3.6];
T.end = [t0, t0 += 4.2];
window.DURATION = t0;
const scenes = Object.keys(T);

// hook photo layouts: [left, top, size, tilt] per photo
const HOOK = { fan: [[60, 470, 430, -9], [325, 400, 430, 3], [590, 470, 430, 10]], hero: [[190, 280, 700, -3]],
  mosaic: [[170, 290, 350, -4], [560, 270, 350, 3], [190, 640, 350, 2], [580, 620, 350, -3]] }[L.hook];
const BT = `img/border_${L.band}_top.png`, BB = `img/border_${L.band}_bot.png`;
const frame = (id, w, extra = '') => `<div class="a frame" id="${id}" style="width:${w}px;height:${w}px;${extra}"><div class="fin"><div class="ph" id="${id}i"></div></div></div>`;
document.body.innerHTML = `
<div class="a" id="bg" style="inset:0"></div><div class="a" id="pat" style="inset:-240px;background-image:${PAT};opacity:.05"></div>
${C.q ? `<div class="sc" id="qs">
  <div class="a" id="qbg" style="inset:-60px;background-size:cover;background-position:center"></div>
  <div class="a" style="inset:0;background:linear-gradient(180deg,rgba(27,24,29,.55),rgba(27,24,29,.25) 40%,rgba(27,24,29,.75))"></div>
  ${C.q.map((w, k) => `<div class="a ctr" id="q${k}" style="top:${760 - (C.q.length - 1) * 95 + k * 190}px"><span class="${k === C.q.length - 1 ? 'hl' : ''}" style="display:inline-block;font-weight:900;font-size:150px;line-height:1.05;color:#fff;padding:4px 30px;${k === C.q.length - 1 ? `background:${L.hl}` : 'text-shadow:0 8px 30px rgba(0,0,0,.5)'}">${w}</span></div>`).join('')}
</div>` : ''}
<div class="sc" id="hook">
  <img class="a" id="hlogo" src="img/mw_oval.png" style="left:430px;top:120px;width:220px">
  ${HOOK.map((h, k) => frame('hp' + k, h[2], `left:${h[0]}px;top:${h[1]}px`)).join('')}
  <div class="a ctr" id="htag" style="top:1000px"><span class="chip" style="background:#1b181d;color:#fff">${C.tag}</span></div>
  <div class="a ctr big" id="ht1" style="top:1090px;color:#1b181d">${C.title1}</div>
  <div class="a ctr" id="ht2w" style="top:1250px"><span class="hl" id="ht2" style="background-image:linear-gradient(${L.hl},${L.hl})">${C.title2}</span></div>
  <div class="a ctr" id="hsub" style="top:1450px;font-size:42px;font-weight:800;letter-spacing:6px;color:#1b181d">${C.hookSub}</div>
  <div class="a sticker ${L.sticker}" id="hst" style="left:790px;top:${L.hook === 'hero' ? 230 : 760}px"><small>${C.hookPre || "FROM"}</small><b>R${C.lowest}</b></div>
</div>
<div class="sc" id="prod">
  <img class="a" src="${BT}" style="left:0;top:0;width:1080px">
  <div class="a" id="pcount" style="left:60px;top:150px;margin-top:10px"><span class="chip" style="background:#1b181d;color:#fff" id="pcountt"></span></div>
  ${frame('pf', 820, 'left:130px;top:230px')}
  <div class="a sticker ${L.sticker}" id="pst" style="left:770px;top:170px"><small id="ppre">ONLY</small><b id="pp"></b></div>
  <div class="a ctr big" id="pname" style="top:1140px"></div>
  <div class="a ctr" id="pchipw" style="top:1320px"><span class="chip" id="pchip" style="color:#fff;border:none"></span></div>
  <div class="a ctr" id="psub" style="top:1430px;font-size:40px;font-weight:700;letter-spacing:4px"></div>
  <img class="a" src="${BB}" style="left:0;bottom:0;width:1080px">
</div>
${C.set ? `<div class="sc" id="set">
  <img class="a" src="${BT}" style="left:0;top:0;width:1080px">
  <div class="a ctr" id="sh1" style="top:140px;font-size:44px;font-weight:800;letter-spacing:8px">${C.set.kicker}</div>
  <div class="a ctr serif" id="sh2" style="top:200px;font-size:96px">${C.set.title}</div>
  ${frame('sf', 740, 'left:170px;top:350px')}
  <div class="a sticker ${L.sticker}" id="sst" style="left:740px;top:320px"><small>ONLY</small><b>R${C.set.price}</b></div>
  <div class="a ctr big" id="sname" style="top:1110px"></div>
  <div class="a ctr" id="sdots" style="top:1300px">${C.set.cols.map((c, k) => `<i id="sd${k}" style="background:${c.dot}"></i>`).join('')}</div>
  <div class="a ctr" id="ssub" style="top:1400px;font-size:40px;font-weight:700;letter-spacing:4px">${C.set.sub || C.set.cols.length + ' COLOURS · R' + C.set.price + ' A SET'}</div>
  <img class="a" src="${BB}" style="left:0;bottom:0;width:1080px">
</div>` : ''}
<div class="sc" id="grid">
  <div class="a ctr serif" id="gt" style="top:170px;font-size:110px;color:#1b181d">${C.gridTitle}</div>
  <div class="a ctr" id="gs" style="top:320px;font-size:42px;font-weight:800;letter-spacing:5px;color:#D8232A">${C.gridSub}</div>
  <div id="gcells"></div>
  ${C.ask ? `<div class="a ctr" id="gask" style="top:1640px"><span class="pill" style="font-size:46px;padding:22px 46px;background:${L.hl};color:#fff">${C.ask}</span></div>` : ''}
</div>
<div class="sc" id="end">
  ${C.endKick ? `<div class="a ctr" id="ekick" style="top:130px"><span class="chip" style="background:${L.hl};color:#fff;font-size:44px">${C.endKick}</span></div>` : ''}
  <img class="a" id="elogo" src="img/mw_oval.png" style="left:300px;top:250px;width:480px">
  <div class="a ctr serif" id="et" style="top:770px;font-size:100px;color:#1b181d">${C.shopLine}</div>
  <div class="a ctr" id="eurl" style="top:920px"><span class="pill" style="font-size:84px;padding:26px 70px;background:#1b181d;color:#fff">makkies.co.za</span></div>
  <div class="a ctr" id="ewa" style="top:1120px;font-size:56px;font-weight:800;color:#1b181d"><span style="color:#25D366">●</span> WhatsApp 072 323 5469</div>
  <div class="a ctr" id="ed" style="top:1240px;font-size:40px;line-height:1.5;color:#4a423b">Delivery across South Africa<br>PAXI to any PEP · or collect in Marabastad</div>
  <div class="a ctr" id="eh" style="top:1490px;font-size:40px;font-weight:700;letter-spacing:4px;color:#C3312B">@makkiewholesalers</div>
</div>
<div class="a" id="wipe" style="left:-200px;top:-200px;width:1480px;height:2320px;background:${STRIPE} left/80px 100% no-repeat,${STRIPE} right/80px 100% no-repeat,#F6F0E9;opacity:0"></div>
<div class="a" id="bars" style="left:40px;top:${{ ndebele: 116, shawl: 94, straw: 100, basotho: 97, xhosa: 138 }[L.band] || 116}px;width:1000px;height:10px;display:flex;gap:8px"></div>
<div class="a stripes" style="bottom:0;height:16px"></div>`;

// one progress bar segment per product
const NSEG = C.items.length + (C.set ? 1 : 0);
for (let i = 0; i < NSEG; i++) $('bars').insertAdjacentHTML('beforeend', `<i id="bar${i}"><b></b></i>`);
// grid cells
const GC = C.gridCols || 3, CELL = C.cell || 270, GAP = CELL < 200 ? 18 : 34, ROWH = CELL + (CELL < 200 ? 84 : 120), SM = CELL < 200;
// a grid item with `more` is a tile saying how many more we keep ("+29") instead of a photo
const MORE = s => `display:flex;align-items:center;justify-content:center;background:#1b181d;color:#fff;font-weight:900;font-size:${Math.round(s * .3)}px`;
C.grid.forEach((g, i) => {
  const row = Math.floor(i / GC), inRow = Math.min(GC, C.grid.length - row * GC), col = i % GC;
  const x = (1080 - (inRow * CELL + (inRow - 1) * GAP)) / 2 + col * (CELL + GAP);
  $('gcells').insertAdjacentHTML('beforeend', `<div class="a gcell" id="g${i}" style="left:${x}px;top:${450 + row * ROWH}px;width:${CELL}px${SM ? ';padding:6px 6px 8px' : ''}">
    <div class="gph" style="height:${CELL - (SM ? 12 : 20)}px;${g.more ? MORE(CELL) : `background-image:url(img/${g.img})`}">${g.more ? g.more : ''}</div><div class="gnm"${SM ? ' style="font-size:17px;margin-top:6px"' : ''}>${C.ask && !g.more ? `<span style="display:inline-block;background:#1b181d;color:#fff;border-radius:40px;padding:0 ${SM ? 8 : 12}px;margin-right:6px">${i + 1}</span>` : ''}${g.name}</div><div class="gpr"${SM ? ' style="font-size:22px"' : ''}>${g.ptxt || 'R' + g.price}</div></div>`);
});
function fit(el, max) { el.style.whiteSpace = 'nowrap'; let f = max; el.style.fontSize = f + 'px'; const r = document.createRange(); r.selectNodeContents(el);
  while (r.getBoundingClientRect().width > 980 && f > 40) { f -= 4; el.style.fontSize = f + 'px'; } }
fit($('ht1'), 170); fit($('ht2'), 150); fit($('et'), 100);
(C.q || []).forEach((w, k) => fit($('q' + k).firstChild, 150));
HOOK.forEach((h, k) => $('hp' + k + 'i').style.backgroundImage = `url(img/${C.hookPhotos[k % C.hookPhotos.length]})`);

const at = (id, t) => t >= T[id][0] && t < T[id][1];
function setText(el, s, max) { if (el.dataset.s !== s) { el.dataset.s = s; el.textContent = s; if (max) fit(el, max); } }
// the striped wipe covering each cut between scenes
function wipe(t) {
  let best = 1e9; for (const id of scenes) if (id !== 'hook') best = Math.min(best, Math.abs(t - T[id][0]) < .3 ? t - T[id][0] : 1e9);
  const w = $('wipe');
  if (best > 1e8) { w.style.opacity = 0; return; }
  const k = (best + .3) / .6;                       // 0 → 1 across the cut
  w.style.opacity = 1; w.style.transform = `rotate(${L.tilt}deg) translateX(${(eio(k) * 2 - 1) * 1500 * (L.tilt < 0 ? 1 : -1)}px)`;
}

window.render = function (t) {
  // background and scene visibility
  let cur = scenes.find(id => at(id, t)) || 'end';
  const pal = cur.startsWith('i') && cur !== 'grid' ? PAL[+cur.slice(1) % PAL.length] : cur === 'set' ? PAL[C.items.length % PAL.length] : { bg: CREAM, acc: '#C3312B' };
  $('bg').style.background = `radial-gradient(circle at 50% 30%,#fff 0%,${pal.bg} 62%)`; document.body.style.color = INK;
  $('pat').style.transform = `translate(${(t * 40) % 240}px,${(t * 24) % 240}px)`;
  ['qs', 'hook', 'prod', 'set', 'grid', 'end'].forEach(id => $(id) && show($(id), (id === 'prod' ? cur.startsWith('i') && cur !== 'grid' : cur === (id === 'qs' ? 'q' : id)) ? 1 : 0));
  wipe(t);
  // progress bars
  for (let i = 0; i < NSEG; i++) { const id = i < C.items.length ? 'i' + i : 'set', [a, b] = T[id];
    $('bar' + i).firstChild.style.width = cl((t - a) / (b - a)) * 100 + '%'; }
  $('bars').style.opacity = (cur === 'q' || cur === 'hook' || cur === 'end' || cur === 'grid') ? 0 : 1;
  // opening question: photos flash behind words that slam in one by one
  if (cur === 'q') {
    const QP = C.qPhotos || C.hookPhotos, n = Math.floor(t / .3) % QP.length;
    $('qbg').style.backgroundImage = `url(img/${QP[n]})`; $('qbg').style.transform = `scale(${1.15 - .1 * ((t % .3) / .3)})`;
    C.q.forEach((w, k) => slam($('q' + k), t, .15 + k * .38, .28));
  }

  // hook
  if (cur === 'hook') {
    t -= T.hook[0];                                   // hook animation times are from the start of the hook
    pop($('hlogo'), t, .05, .4, .3);
    HOOK.forEach((h, k) => { const el = $('hp' + k), st = .2 + k * .16, q = eo((t - st) / .5), r = h[3];
      el.style.opacity = cl((t - st) / .12);
      el.style.transform = L.hook === 'hero' ? `scale(${.4 + .6 * bk((t - st) / .6) + .02 * Math.sin(t * 2)}) rotate(${r}deg)`
        : `translate${L.hook === 'mosaic' ? 'X' : 'Y'}(${(1 - q) * (L.hook === 'mosaic' && k % 2 === 0 ? -900 : 900)}px) rotate(${r * q + (1 - q) * 30}deg) scale(${1 + .03 * Math.sin(t * 2 + k)})`;
      $('hp' + k + 'i').style.transform = `scale(${1.05 + .05 * (t / 3.6)})`; });
    pop($('htag'), t, .9, .3, .3); slam($('ht1'), t, 1.1);
    const k2 = eo((t - 1.45) / .35); $('ht2w').style.opacity = cl((t - 1.4) / .1); $('ht2').style.backgroundSize = `${k2 * 100}% 100%`;
    rise($('hsub'), t, 1.9, .35, 40);
    pop($('hst'), t, 2.3, .45, .2, -12 + 4 * Math.sin(t * 5));
  }
  // products
  if (cur.startsWith('i') && cur !== 'grid') {
    const i = +cur.slice(1), it = C.items[i], lt = t - T[cur][0];
    setText($('pcountt'), String(i + 1).padStart(2, '0') + ' / ' + String(C.items.length).padStart(2, '0'));
    $('pfi').style.backgroundImage = `url(img/${it.img})`;
    const q = eo((lt - .15) / .55); $('pf').style.opacity = cl((lt - .15) / .1);
    $('pf').style.transform = { right: `translateX(${(1 - q) * 1100}px) rotate(${-3 + (1 - q) * 18}deg)`, left: `translateX(${(q - 1) * 1100}px) rotate(${3 - (1 - q) * 18}deg)`,
      up: `translateY(${(1 - q) * 1400}px) rotate(${2 - (1 - q) * 8}deg)`, zoom: `scale(${.55 + .45 * bk((lt - .15) / .55)}) rotate(${-2 + (1 - q) * 10}deg)` }[L.enter];
    $('pfi').style.transform = `scale(${1.02 + .1 * cl(lt / PER)})`;
    setText($('pname'), it.name.toUpperCase(), 140); rise($('pname'), lt, .35, .35, 90);
    $('pchip').style.background = pal.acc;
    setText($('pchip'), it.chip || ''); $('pchipw').style.display = it.chip ? '' : 'none'; pop($('pchipw'), lt, .6, .35, .3, -3);
    setText($('psub'), it.sub || ''); rise($('psub'), lt, .75, .35, 30);
    setText($('pp'), 'R' + it.price); setText($('ppre'), it.pre || 'ONLY');
    pop($('pst'), lt, .55, .45, .2, -12 + 5 * Math.sin(lt * 6) * cl(1 - (lt - .55) / 1.2));
    $('pcount').style.opacity = cl(lt / .2);
  }
  // colour set
  if (cur === 'set') {
    const lt = t - T.set[0], j = Math.min(C.set.cols.length - 1, Math.max(0, Math.floor((lt - .9) / SPER))), c = C.set.cols[j], lj = lt - .9 - j * SPER;
    rise($('sh1'), lt, .1, .3, 30); pop($('sh2'), lt, .25, .4, .7);
    $('sfi').style.backgroundImage = `url(img/${c.img})`;
    const enter = lt < .9 ? eo((lt - .3) / .5) : 1, sw = lt >= .9 ? eo(lj / .3) : 1;
    $('sf').style.opacity = cl((lt - .3) / .1);
    $('sf').style.transform = `translateX(${(1 - enter) * 1100 + (1 - sw) * 300}px) rotate(${-2 + (1 - sw) * 6}deg) scale(${.94 + .06 * sw})`;
    $('sfi').style.transform = `scale(${1.02 + .08 * cl(lj / SPER)})`;
    setText($('sname'), c.name.toUpperCase(), 140); $('sname').style.opacity = lt >= .9 ? cl(lj / .15) : 0;
    pop($('sst'), lt, .6, .45, .2, -12 + 4 * Math.sin(lt * 4));
    C.set.cols.forEach((cc, k) => $('sd' + k).style.transform = `scale(${k === j && lt >= .9 ? 1.5 : 1})`);
    rise($('ssub'), lt, .7, .35, 30); rise($('sdots'), lt, .6, .35, 30);
  }
  // grid
  if (cur === 'grid') {
    const lt = t - T.grid[0];
    pop($('gt'), lt, .1, .4, .7); rise($('gs'), lt, .3, .3, 40);
    C.grid.forEach((g, i) => pop($('g' + i), lt, .45 + i * Math.min(.12, 1.4 / C.grid.length), .35, .3, [-3, 2, -1, 3][i % 4]));
    if (C.ask) { pop($('gask'), lt, 1.9, .4, .4); if (lt > 2.3) $('gask').style.transform = `scale(${1 + .07 * Math.pow(Math.sin(Math.PI * (lt - 2.3) / .6), 2)})`; }
  }
  // end card
  if (cur === 'end') {
    const lt = t - T.end[0];
    pop($('elogo'), lt, .05, .5, .3); if (C.endKick) pop($('ekick'), lt, .2, .4, .4, -2); rise($('et'), lt, .4, .35, 60); pop($('eurl'), lt, .7, .35, .5);
    if (lt > 1.1) $('eurl').style.transform = `scale(${1 + .14 * Math.pow(Math.sin(Math.PI * (lt - 1.1) / .7), 2)})`;
    rise($('ewa'), lt, 1.0, .3, 40); rise($('ed'), lt, 1.25, .3, 40); rise($('eh'), lt, 1.5, .3, 30);
  }
};
render(0);
