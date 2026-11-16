# Easier navigation (based on what Takealot, Amazon, Woolworths, M&S and Baymard's research do best).
# Usage: python3 patch-nav.py public/index.html   (run after patch-home.py)
#  1. Menu button: full category menu with photos, grouped by department, sub-categories open in place
#  2. Search suggestions while typing (categories + products with photo and price)
#  3. Breadcrumbs on category pages (Home › Tribal Blankets › Basotho)
#  4. "Load more" instead of page numbers (shows how many of how many)
#  5. Sub-category buttons with small photos; the long "Browse" list is hidden on phones (the menu replaces it)
import sys, re
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'id="mnav"' in s:
    print('nav already patched'); sys.exit()

def sub(pat, rep, flags=re.S):
    global s
    s2, n = re.subn(pat, rep, s, count=1, flags=flags)
    if not n: raise SystemExit('pattern not found: ' + pat[:80])
    s = s2

# menu button in the header + search suggestions box + breadcrumbs
sub(r'(<header class="top">\s*<div class="bar">)', r'\1<button class="mbtn" onclick="openMenu()" aria-label="Open menu"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg><span>Menu</span></button>')
sub(r'(<input name="q" id="q"[^>]*>)', r'\1<div class="sugg" id="sugg"></div>')
sub(r'(<form class="search")', r'\1 autocomplete="off"')
sub(r'(<div class="toolbar"><h2 id="shopTitle">)', r'<nav class="crumbs" id="crumbs" aria-label="You are here"></nav>\1')
sub(r'(<button id="moreBtn" onclick=")toggleMore\(event\)', r'\1(innerWidth<=900?(event.stopPropagation(),openMenu()):toggleMore(event))')
MENU = '''<div class="mnav" id="mnav" onclick="if(event.target===this)closeMenu()"><div class="mpanel" role="dialog" aria-label="Menu">
<div class="mhead"><b>Shop by category</b><button onclick="closeMenu()" aria-label="Close menu">×</button></div><div id="mbody"></div></div></div>'''
sub(r'(<div class="overlay" id="overlay")', MENU + r'\n\1')

JS = r'''
/* ---------- easier navigation ---------- */
const catImg = c => { const p = PRODUCTS.find(p => (p.category === c || p.category.startsWith(c + ' · ')) && p.img && !p.soldOut) || PRODUCTS.find(p => (p.category === c || p.category.startsWith(c + ' · ')) && p.img); return p ? tn(p.img) : ''; };
function openMenu() {
  const allc = [...new Set(PRODUCTS.map(p => p.category))], cnt = c => PRODUCTS.filter(p => p.category === c || p.category.startsWith(c + ' · ')).length;
  const nav = (c, lbl) => `state.cat='${esc(c)}';state.q='';closeMenu();go('shop');return false`;
  let h = `<div class="mquick"><a href="#" onclick="closeMenu();go('home');return false">Home</a><a href="#" onclick="${nav('all')}">All products</a><a href="#" onclick="closeMenu();openPage('track');return false">Track my order</a><a href="https://wa.me/${CONFIG.whatsapp}" target="_blank" rel="noopener">WhatsApp us</a></div>`;
  h += `<div class="mgrp">Popular</div>` + [['Ndebele', 'col:ndebele'], ['Tekkies & Hats', 'col:tekkies-hats'], ['The wedding look', 'col:wedding-look']].map(([l, c]) =>
    `<a class="mrow" href="#" onclick="${nav(c)}"><span class="mi" style="background-image:url('${tn((byId[COLLECTIONS[c].ids[0]] || {}).img || '')}')"></span><span class="mn">${esc(l)}</span><span class="mc">${COLLECTIONS[c].ids.filter(id => byId[id]).length}</span><i>›</i></a>`).join('');
  GROUPS.forEach(g => {
    h += `<div class="mgrp">${esc(g)}</div>`;
    const pars = [...new Set(allc.filter(c => PRODUCTS.some(p => p.group === g && p.category === c)).map(c => c.split(' · ')[0]))].sort();
    pars.forEach(par => {
      const subs = allc.filter(c => c.startsWith(par + ' · ')).sort();
      if (!subs.length) { h += `<a class="mrow" href="#" onclick="${nav(par)}"><span class="mi" style="background-image:url('${catImg(par)}')"></span><span class="mn">${esc(par)}</span><span class="mc">${cnt(par)}</span><i>›</i></a>`; return; }
      h += `<details class="mdet"><summary class="mrow"><span class="mi" style="background-image:url('${catImg(par)}')"></span><span class="mn">${esc(par)}</span><span class="mc">${cnt(par)}</span><i class="pl">+</i></summary>` +
        `<a class="msub" href="#" onclick="${nav(par)}">All ${esc(par)}</a>` + subs.map(c => `<a class="msub" href="#" onclick="${nav(c)}">${esc(c.slice(par.length + 3))}<span class="mc">${cnt(c)}</span></a>`).join('') + `</details>`;
    });
  });
  document.getElementById('mbody').innerHTML = h;
  document.getElementById('mnav').classList.add('open'); document.body.style.overflow = 'hidden';
}
function closeMenu() { document.getElementById('mnav').classList.remove('open'); document.body.style.overflow = ''; }
/* search suggestions while typing */
(function () {
  const q = document.getElementById('q'), box = document.getElementById('sugg'); let t;
  const hide = () => { box.classList.remove('open'); };
  q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => {
    const v = q.value.trim(); if (v.length < 2) return hide();
    const save = [state.q, state.cat, state.qLoose]; state.q = v; state.cat = 'all'; let list = []; try { list = filtered(); } catch (e) {} [state.q, state.cat, state.qLoose] = save;
    const lv = v.toLowerCase(), allc = [...new Set(PRODUCTS.map(p => p.category.split(' · ')[0]))].concat([...new Set(PRODUCTS.map(p => p.category))].filter(c => c.includes(' · ')));
    const cs = [...new Set(allc)].filter(c => c.toLowerCase().includes(lv)).slice(0, 3);
    if (!list.length && !cs.length) { box.innerHTML = `<div class="snone">No match for “${esc(v)}”. Try a colour or “blanket”.</div>`; box.classList.add('open'); return; }
    box.innerHTML = cs.map(c => `<a class="scat" href="#" onmousedown="event.preventDefault()" onclick="state.cat='${esc(c)}';state.q='';document.getElementById('sugg').classList.remove('open');go('shop');return false">${esc(c.replace(' · ', ' › '))}<span>Category</span></a>`).join('') +
      list.slice(0, 6).map(p => `<a class="sp" href="#" onmousedown="event.preventDefault()" onclick="document.getElementById('sugg').classList.remove('open');openProduct('${p.id}');return false"><span class="si" style="background-image:url('${tn(p.img || '')}')"></span><span class="sn">${esc(p.name)}<small>${esc(p.category.split(' · ').pop())}</small></span><b>${p.minPrice === p.maxPrice ? R(p.minPrice) : 'from ' + R(p.minPrice)}</b></a>`).join('') +
      (list.length ? `<a class="sall" href="#" onmousedown="event.preventDefault()" onclick="state.q=document.getElementById('q').value;state.cat='all';document.getElementById('sugg').classList.remove('open');go('shop');return false">See all ${list.length} results for “${esc(v)}” ›</a>` : '');
    box.classList.add('open'); }, 150); });
  q.addEventListener('blur', () => setTimeout(hide, 150));
  q.addEventListener('focus', () => { if (q.value.trim().length > 1) q.dispatchEvent(new Event('input')); });
  q.form.addEventListener('submit', hide);
})();
/* breadcrumbs, sub-category photos, load more */
const _renderGrid = renderGrid;
renderGrid = function () {
  const key = state.q + '|' + state.cat + '|' + state.sort;
  if (key !== state._lkey) { state._lkey = key; state.per = 24; }
  _renderGrid();
  const sg = document.getElementById('sugg'); if (sg) sg.classList.remove('open');
  const cr = document.getElementById('crumbs'); let c = '<a href="#" onclick="go(\'home\');return false">Home</a>';
  if (state.q) c += ' › <span>Search</span>';
  else if (state.cat === 'all') c += ' › <span>All products</span>';
  else if (COLLECTIONS[state.cat]) c += ` › <span>${esc(COLLECTIONS[state.cat].label)}</span>`;
  else { const i = state.cat.indexOf(' · '); if (i > -1) { const par = state.cat.slice(0, i); c += ` › <a href="#" onclick="state.cat='${esc(par)}';go('shop');return false">${esc(par)}</a> › <span>${esc(state.cat.slice(i + 3))}</span>`; } else c += ` › <span>${esc(state.cat)}</span>`; }
  cr.innerHTML = c;
  if (!state.q && state.cat.includes(' · ')) document.getElementById('shopTitle').textContent = state.cat.split(' · ').pop();
  document.querySelectorAll('#subcats button').forEach(b => { if (b.querySelector('.sci')) return; const m = (b.getAttribute('onclick') || '').match(/state\.cat='([^']*)'/); const im = m ? catImg(m[1].replace(/&amp;/g, '&')) : '';
    if (im) b.insertAdjacentHTML('afterbegin', `<span class="sci" style="background-image:url('${im}')"></span>`); });
};
renderPager = function (total, pages, start, count) {
  document.getElementById('pagerTop').innerHTML = '';
  const shown = start + count, pct = total ? Math.round(shown / total * 100) : 0;
  document.getElementById('pagerBot').innerHTML = total ? `<div class="lmore"><p>Showing ${shown} of ${total} products</p><div class="lbar"><span style="width:${pct}%"></span></div>` +
    (shown < total ? `<button onclick="state.per=(state.per==='all'?${total}:state.per)+24;renderGrid()">Load more</button>` : '') + `</div>` : '';
};
'''
sub(r"(\nbuildNav\(\); renderCart\(\); renderGrid\(\);)", JS.replace('\\', '\\\\') + r"\1")

CSS = r'''
/* product pop-up on phones: fit the visible screen (iPhone toolbars), scroll smoothly, buttons reachable */
@media(max-width:900px){.overlay{padding:8px;align-items:flex-start}.modal{max-height:calc(100vh - 16px);max-height:calc(100dvh - 16px);-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
.modal .pic{min-height:0}.modal .pic img{max-height:52vh;max-height:52dvh}.modal .info{padding-bottom:calc(32px + env(safe-area-inset-bottom))}.ovx{top:14px!important;right:14px!important}}
/* ---------- easier navigation ---------- */
.mbtn{display:none;background:transparent;border:0;color:#fff;align-items:center;gap:6px;font:700 14px var(--body);padding:4px 6px 4px 0;cursor:pointer}
.mbtn svg{width:26px;height:26px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round}
.mnav{position:fixed;inset:0;z-index:60;background:rgba(20,16,14,.45);display:none}.mnav.open{display:block}
.mpanel{position:absolute;left:0;top:0;bottom:0;width:min(420px,88vw);background:#fff;overflow-y:auto;overscroll-behavior:contain;box-shadow:var(--shadow)}
.mhead{position:sticky;top:0;background:var(--navy);color:#fff;display:flex;justify-content:space-between;align-items:center;padding:14px 16px;z-index:1}.mhead b{font-size:17px}
.mhead button{background:transparent;border:0;color:#fff;font-size:30px;line-height:1;cursor:pointer}
.mquick{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:14px 16px}.mquick a{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-weight:700;font-size:14px;color:var(--ink);text-decoration:none}
.mgrp{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--scarlet);padding:16px 16px 6px}
.mrow{display:flex;align-items:center;gap:12px;padding:8px 16px;color:var(--ink);text-decoration:none;border-bottom:1px solid #f0ece5;cursor:pointer;list-style:none;min-height:56px}
.mrow::-webkit-details-marker{display:none}.mi{width:44px;height:44px;border-radius:8px;flex:none;background:#F4EFE8 center/cover;border:1px solid var(--line)}
.mn{flex:1;font-weight:600;font-size:15px;line-height:1.25}.mc{color:var(--muted);font-size:13px}.mrow i{font-style:normal;font-size:20px;color:var(--muted);width:16px;text-align:center}
.mdet[open] .pl{transform:rotate(45deg)}.mdet[open]>summary{background:var(--bg)}
.msub{display:flex;justify-content:space-between;padding:12px 16px 12px 72px;font-size:14.5px;color:var(--ink);text-decoration:none;border-bottom:1px solid #f0ece5;background:#fcfbf8}
.search{position:relative}.sugg{display:none;position:absolute;left:0;right:0;top:calc(100% + 4px);background:#fff;color:var(--ink);border-radius:10px;box-shadow:0 14px 40px rgba(0,0,0,.25);z-index:30;overflow:hidden;max-height:70vh;overflow-y:auto}
.sugg.open{display:block}.sugg a{display:flex;align-items:center;gap:12px;padding:10px 14px;color:var(--ink);text-decoration:none;border-bottom:1px solid #f0ece5}
.scat{font-weight:700;justify-content:space-between}.scat span{font-weight:400;font-size:12px;color:var(--muted)}
.si{width:44px;height:44px;border-radius:6px;flex:none;background:#F4EFE8 center/cover}.sn{flex:1;font-size:14.5px;font-weight:600;line-height:1.25}.sn small{display:block;color:var(--muted);font-weight:400;font-size:12.5px}.sp b{font-size:14px;white-space:nowrap}
.sall{font-weight:700;color:var(--teal)!important;justify-content:center}.snone{padding:14px;color:var(--muted);font-size:14px}
.crumbs{font-size:13.5px;color:var(--muted);margin:0 0 8px}.crumbs a{color:var(--ink);font-weight:600}.crumbs span{color:var(--muted)}
.subcats{flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}.subcats::-webkit-scrollbar{display:none}
.subcats button{display:flex;align-items:center;gap:8px;white-space:nowrap;padding:6px 14px 6px 6px!important;flex:none}
.sci{width:32px;height:32px;border-radius:50%;background:#F4EFE8 center/cover;flex:none}
#pagerTop{display:none}#pagerBot{display:block}.shop>div{min-width:0}.lmore{text-align:center;width:100%;margin:10px 0 20px}.lmore p{margin:0 0 8px;color:var(--muted);font-size:14px}
.lbar{height:4px;background:var(--line);border-radius:4px;max-width:240px;margin:0 auto 14px;overflow:hidden}.lbar span{display:block;height:100%;background:var(--ink)}
.lmore button{background:#fff;border:1.5px solid var(--ink);border-radius:8px;padding:12px 34px;font:700 15px var(--body);cursor:pointer}
@media(max-width:700px){.brand.newlogo .full{max-width:50vw;height:auto}.mbtn span{display:none}}
@media(min-width:901px){.subcats{flex-wrap:wrap!important;overflow:visible}}
@media(max-width:900px){.mbtn{display:flex}aside.filters{display:none!important}.toolbar #sort{margin-left:auto}}
'''
sub(r"(</style>\s*</head>)", CSS.replace('\\', '\\\\') + r"\1")
open(P, 'w', encoding='utf-8').write(s)
print('navigation patched,', len(s) // 1024, 'KB')
