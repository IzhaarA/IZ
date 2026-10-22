// Instagram carousel (1080×1350 slides) in the same look as the version 2 TikTok videos, from the same window.CFG.
// Slides: cover → one per product (CFG.citems, else CFG.items) → one per colour of the set → all products → order today.
const C = window.CFG;
const L = Object.assign({ band: 'ndebele', hook: 'fan', sticker: 'circle', hl: '#D8232A' }, C.look || {});
const PAL = L.pal || [{ bg: '#E6ECF6', acc: '#0350EA' }, { bg: '#F6E6E3', acc: '#D8232A' }, { bg: '#E4F0E8', acc: '#05A463' }, { bg: '#F8EFD6', acc: '#C99400' }, { bg: '#EEE6F0', acc: '#45203F' }];
const CREAM = '#F6F0E9', BT = `img/border_${L.band}_top.png`, BB = `img/border_${L.band}_bot.png`;
const PAT = 'url("data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" fill="none" stroke="#000" stroke-width="7"><path d="M20 120h40v-40h40v-40h40v40h40v40h40M20 120h40v40h40v40h40v-40h40v-40h40"/><rect x="104" y="104" width="32" height="32"/></svg>') + '")';
const HOOK = { fan: [[90, 300, 360, -9], [360, 250, 360, 3], [630, 300, 360, 10]], hero: [[250, 230, 580, -3]],
  mosaic: [[220, 250, 300, -4], [560, 235, 300, 3], [235, 565, 300, 2], [575, 550, 300, -3]] }[L.hook];
const items = C.citems || C.items, sets = C.set ? C.set.cols : [], N = 1 + items.length + sets.length + 2;
const frame = (img, w, x, y, r = 0) => `<div class="a frame" style="width:${w}px;height:${w}px;left:${x}px;top:${y}px;transform:rotate(${r}deg)"><div class="fin"><div class="ph" style="background-image:url(img/${img})"></div></div></div>`;
const sticker = (pre, price, x, y) => `<div class="a sticker ${L.sticker}" style="left:${x}px;top:${y}px;transform:rotate(-10deg) scale(.86)"><small>${pre}</small><b>R${price}</b></div>`;
const dots = i => `<div class="a ctr cdots">${Array.from({ length: N }, (_, k) => `<i class="${k === i ? 'on' : ''}"></i>`).join('')}</div>`;
const slide = (i, bg, html) => `<div class="slide" style="background:radial-gradient(circle at 50% 32%,#fff 0%,${bg} 64%)"><div class="a pat" style="background-image:${PAT}"></div>${dots(i)}${html}<div class="a stripes" style="bottom:0;height:12px"></div></div>`;
const product = (i, p, pal, k, n, label) => slide(i, pal.bg, `<img class="a" src="${BT}" style="left:0;top:0;width:1080px">
  <div class="a" style="left:60px;top:${BAND + 24}px"><span class="chip" style="background:#1b181d;color:#fff;font-size:30px;padding:10px 26px">${label || String(k + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0')}</span></div>
  ${frame(p.img, 700, 190, BAND + 70, -2)}${sticker(p.pre || 'ONLY', p.price, 760, BAND + 20)}
  <div class="a ctr big fit" data-max="120" style="top:${BAND + 830}px">${p.name.toUpperCase()}</div>
  ${p.chip ? `<div class="a ctr" style="top:${BAND + 970}px"><span class="chip" style="background:${pal.acc};color:#fff;font-size:32px">${p.chip}</span></div>` : ''}
  <div class="a ctr" style="top:${BAND + 1050}px;font-size:32px;font-weight:700;letter-spacing:4px">${p.sub || ''}</div>
  <div class="a ctr foot">Order at makkies.co.za · WhatsApp 072 323 5469</div>`);
const BAND = { ndebele: 102, shawl: 80, straw: 86, basotho: 83, xhosa: 124 }[L.band] || 102;

let html = '', s = 0;
// cover
html += slide(s++, CREAM, `<img class="a" src="img/mw_oval.png" style="left:470px;top:60px;width:140px">
  ${HOOK.map((h, k) => frame(C.hookPhotos[k % C.hookPhotos.length], h[2], h[0], h[1], h[3])).join('')}
  ${sticker(C.hookPre || 'FROM', C.lowest, L.hook === 'hero' ? 790 : 800, L.hook === 'hero' ? 190 : 640)}
  <div class="a ctr" style="top:${L.hook === 'mosaic' ? 900 : 860}px"><span class="chip" style="background:#1b181d;color:#fff;font-size:32px">${C.tag}</span></div>
  <div class="a ctr big fit" data-max="140" style="top:${L.hook === 'mosaic' ? 970 : 935}px">${C.title1}</div>
  <div class="a ctr" style="top:${L.hook === 'mosaic' ? 1105 : 1075}px"><span class="hl fit" data-max="120" style="background:${L.hl}">${C.title2}</span></div>
  <div class="a ctr" style="top:1255px;font-size:32px;font-weight:800;letter-spacing:5px">${C.hookSub} · SWIPE →</div>`);
items.forEach((p, k) => html += product(s++, p, PAL[k % PAL.length], k, items.length));
sets.forEach((c, k) => html += product(s++, { name: c.name, img: c.img, price: C.set.price, chip: C.set.kicker, sub: C.set.sub || (sets.length + ' COLOURS · R' + C.set.price + ' A SET') },
  PAL[(items.length + k) % PAL.length], k, sets.length, `COLOUR ${k + 1} / ${sets.length}`));
// all products
const G = C.grid, cols = C.gridCols || 3, rows = Math.ceil(G.length / cols), gap = cols > 4 ? 16 : 26, txt = cols > 4 ? 62 : 86;
const cell = Math.floor(Math.min((960 - (cols - 1) * gap) / cols, (900 - (rows - 1) * gap) / rows - txt)), sm = cell < 170;
html += slide(s++, CREAM, `<div class="a ctr serif" style="top:80px;font-size:92px">${C.gridTitle}</div>
  <div class="a ctr" style="top:200px;font-size:34px;font-weight:800;letter-spacing:5px;color:#D8232A">${C.gridSub}</div>
  ${G.map((g, i) => { const r = Math.floor(i / cols), inRow = Math.min(cols, G.length - r * cols), c = i % cols, x = (1080 - (inRow * cell + (inRow - 1) * gap)) / 2 + c * (cell + gap);
    return `<div class="a gcell" style="left:${x}px;top:${290 + r * (cell + txt + gap)}px;width:${cell}px;${sm ? 'padding:6px 6px 8px' : ''}"><div class="gph" style="height:${cell - (sm ? 12 : 20)}px;${g.more ? `display:flex;align-items:center;justify-content:center;background:#1b181d;color:#fff;font-weight:900;font-size:${Math.round(cell * .3)}px` : `background-image:url(img/${g.img})`}">${g.more || ''}</div>
      <div class="gnm" style="${sm ? 'font-size:15px;margin-top:5px' : 'font-size:21px'}">${g.name}</div><div class="gpr" style="${sm ? 'font-size:19px' : 'font-size:28px'}">${g.ptxt || 'R' + g.price}</div></div>`; }).join('')}
  <div class="a ctr foot">Wholesale &amp; retail · bulk buyers, ask us for trade pricing</div>`);
// order today
html += slide(s++, CREAM, `<img class="a" src="${BT}" style="left:0;top:150px;width:1080px">
  <img class="a" src="img/mw_oval.png" style="left:370px;top:320px;width:340px">
  <div class="a ctr serif" style="top:650px;font-size:90px">Order today</div>
  <div class="a ctr" style="top:790px"><span class="pill" style="font-size:66px;padding:22px 60px;background:#1b181d;color:#fff">makkies.co.za</span></div>
  <div class="a ctr" style="top:950px;font-size:46px;font-weight:800"><span style="color:#25D366">●</span> WhatsApp 072 323 5469</div>
  <div class="a ctr" style="top:1040px;font-size:32px;line-height:1.5;color:#4a423b">Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad</div>
  <div class="a ctr foot" style="letter-spacing:4px">MARABASTAD, PRETORIA · WHOLESALE &amp; RETAIL</div>`);
document.body.innerHTML = html;
// shrink lines of big text until they fit the width
document.querySelectorAll('.fit').forEach(el => { el.style.whiteSpace = 'nowrap'; let f = +el.dataset.max; el.style.fontSize = f + 'px';
  const r = document.createRange(); r.selectNodeContents(el); while (r.getBoundingClientRect().width > 960 && f > 36) { f -= 4; el.style.fontSize = f + 'px'; } });
