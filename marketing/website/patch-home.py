# New home page ("Look G"): fast, phone-first, based on what top-selling shops do.
# Usage: python3 patch-home.py public/index.html      (photos come from home-g/, copied to public/home-g/)
# - replaces the home section (categories, main picture, trust row, best sellers, wedding look, bulk quote)
# - removes ~1.2 MB of category pictures that were stored inside the page (the main reason it was slow)
# - the full product grid now only shows on the shop/category pages, not under the home page
import sys, re, os, shutil
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'id="homeg"' in s:
    print('home already patched'); sys.exit()

def sub(pat, rep, flags=re.S, count=1):
    global s
    s2, n = re.subn(pat, rep, s, count=count, flags=flags)
    if not n: raise SystemExit('pattern not found: ' + pat[:80])
    s = s2

# 1) drop the inline base64 pictures (HERO_IMG is unused; TILE_IMGS only fed the old tiles)
sub(r"const HERO_IMG = 'data:image/[^']*';", "const HERO_IMG = '';")
sub(r"const TILE_IMGS = \{.*?\};\n", "const TILE_IMGS = {};\n")

# 2) new home markup
HOME = r'''<section id="home"><div id="homeg">
  <div class="hg-w"><div class="hg-chips" id="hgChips"></div></div>
  <div class="hg-hero"><div class="hg-hp" id="hgHero"></div>
    <div class="hg-ht"><small>December weddings &amp; ceremonies</small><h1>Traditional blankets, beads &amp; more, delivered to your door</h1>
    <p>Basotho, Ndebele and Xhosa blankets, wedding shawls and Czech beads. Wholesale prices, delivered anywhere in South Africa.</p>
    <a class="hg-btn" href="#" onclick="state.cat='Tribal Blankets';state.q='';go('shop');return false">Shop blankets</a><a class="hg-btn o" href="#" onclick="state.cat='Czech Glass Seed Beads';state.q='';go('shop');return false">Shop beads</a></div></div>
  <div class="hg-w">
    <div class="hg-trust">
      <div><svg viewBox="0 0 24 24"><path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg><p><b>Nationwide delivery</b>Courier or PAXI at any PEP</p></div>
      <div><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/></svg><p><b>Pay safely online</b>Card, Instant EFT, SnapScan</p></div>
      <div><svg viewBox="0 0 24 24"><path d="M4 10v10h16V10M3 6l2-3h14l2 3v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/></svg><p><b>Visit our shop</b>Oriental Complex, Marabastad</p></div>
      <div><svg viewBox="0 0 24 24"><path d="M4 20l1.5-4A8 8 0 1 1 9 19z"/></svg><p><b>WhatsApp help</b><span class="hg-wa"></span></p></div>
    </div>
    <h2 class="hg-h">Shop by category <a href="#" onclick="state.cat='all';state.q='';go('shop');return false">View all</a></h2>
    <div class="hg-cats" id="hgCats"></div>
    <h2 class="hg-h">Best sellers <a href="#" onclick="state.cat='all';state.q='';go('shop');return false">Shop all</a></h2>
    <div class="hg-prods" id="hgProds"></div>
    <div class="hg-look"><div class="hg-lp" id="hgLookPic"></div><div class="hg-lt"><h3>Shop the wedding look</h3><p>Everything in this photo, ready to order.</p><div id="hgLook"></div>
      <a class="hg-btn" href="#" onclick="state.cat='col:wedding-look';state.q='';go('shop');return false">Shop the look</a></div></div>
    <div class="hg-bulk"><div><h3>Buying for your shop or event?</h3><p>Stock prices on 10 pieces or more. Send us your list on WhatsApp and we&#8217;ll quote you the same day.</p></div>
      <a class="hg-btn wa" id="hgBulk" target="_blank" rel="noopener">WhatsApp for a quote</a></div>
  </div>
</div></section>'''
sub(r'<section id="home">.*?</section>', HOME.replace('\\', '\\\\'))

# 3) shop grid only on shop pages (it used to sit under the home page too)
sub(r'<section class="shop" id="shop">', '<section class="shop" id="shop" style="display:none">')
sub(r"document\.getElementById\('shop'\)\.style\.display = \(view === 'home' \|\| view === 'shop'\) \? '' : 'none';",
    "document.getElementById('shop').style.display = view === 'shop' ? '' : 'none';")

# 4) replace the old tiles / featured / bead-swatch rendering with the new home
sub(r"  document\.getElementById\('tiles'\)\.innerHTML = .*?document\.getElementById\('ubswatches'\)\.innerHTML = [^\n]*\n", "  renderHomeG();\n")

JS = r'''
/* ---------- home page (Look G) ---------- */
const HG = (window.HOMEG_BASE || '') + 'home-g/';
COLLECTIONS['col:wedding-look'] = {label: 'The wedding look', ids: ['TRB-003', 'NZL-001', 'SHW-011', 'NZL-002', 'SHW-002', 'TRB-002']};
function renderHomeG() {
  const th = id => (byId[id] && byId[id].img) ? tn(byId[id].img) : '';
  const go2 = c => `state.cat='${esc(c)}';state.q='';go('shop');return false`;
  const CH = [['All', 'all', HG + 'look.jpg'], ['Blankets', 'Tribal Blankets', HG + 'c-tribal.jpg'], ['Shawls', 'Shawls & Throws', HG + 'c-shawls.jpg'], ['Czech Beads', 'Czech Glass Seed Beads', HG + 'c-czech.jpg'],
    ['Chinese Beads', 'Chinese Glass Seed Beads', HG + 'c-chinese.jpg'], ['Ndebele', 'col:ndebele', HG + 'c-ndebele.jpg'], ['Hats & Tekkies', 'col:tekkies-hats', HG + 'c-hats.jpg'], ['Kangas', 'Kangas', HG + 'c-kangas.jpg'],
    ['Mink', 'Mink Blankets', HG + 'c-mink.jpg'], ['Berets', 'Berets', th('BER-008')], ['Bangles', 'Bangles', th('BNG-001')], ['Haberdashery', 'Haberdashery', th((PRODUCTS.find(p => p.category.startsWith('Haberdashery') && p.img) || {}).id)]];
  document.getElementById('hgChips').innerHTML = CH.map(([l, c, i]) => `<a href="#" onclick="${go2(c)}"><span style="background-image:url('${i}')"></span>${esc(l)}</a>`).join('');
  document.getElementById('hgHero').innerHTML = [['TRB-002', 'Umbhalo', 'h-umbhalo'], ['TRB-010', 'Khotso', 'h-khotso'], ['TRB-029', 'Xhosa Tribal Stripe', 'h-xhosa'], ['TRB-022', 'Elizabeth Basotho', 'h-elizabeth']].map(([id, l, i]) =>
    `<a href="#" onclick="openProduct('${id}');return false" style="background-image:url('${HG}${i}.jpg')" aria-label="${esc(l)}"><span>${esc(l)}</span></a>`).join('');
  document.getElementById('hgLookPic').style.backgroundImage = `url('${HG}look.jpg')`;
  const CATS = [['Tribal Blankets', 'Tribal Blankets', 'c-tribal'], ['Mink Blankets', 'Mink Blankets', 'c-mink'], ['Shawls & Throws', 'Shawls & Throws', 'c-shawls'], ['Czech Beads', 'Czech Glass Seed Beads', 'c-czech'],
    ['Chinese Beads', 'Chinese Glass Seed Beads', 'c-chinese'], ['Ndebele', 'col:ndebele', 'c-ndebele'], ['Hats & Tekkies', 'col:tekkies-hats', 'c-hats'], ['Kangas', 'Kangas', 'c-kangas']];
  document.getElementById('hgCats').innerHTML = CATS.map(([l, c, i]) => `<a href="#" onclick="${go2(c)}"><span class="hg-ci" style="background-image:url('${HG}${i}.jpg')"></span><b>${esc(l)}<i>›</i></b></a>`).join('');
  const BEST = ['TRB-003', 'SHW-011', 'NZL-001', 'TRB-011', 'TEK-002', 'TRB-029', 'MNK-014', 'TRB-002'];
  document.getElementById('hgProds').innerHTML = BEST.map(id => byId[id]).filter(p => p && !p.soldOut).map(p => {
    const one = p.variants.filter(v => !v.soldOut).length === 1 && p.variants.length === 1;
    return `<div class="hg-pc"><a href="#" onclick="openProduct('${p.id}');return false"><span class="hg-pi" style="background-image:url('${tn(p.img)}')"></span><b>${esc(p.name)}</b><small>${esc(p.category.split(' · ').pop())}</small></a>
      <div class="hg-pr"><span>${p.minPrice === p.maxPrice ? R(p.minPrice) : 'from ' + R(p.minPrice)}</span>${one ? `<button onclick="addToCart('${p.variants[0].id}',1)">Add</button>` : `<button onclick="openProduct('${p.id}')">Choose</button>`}</div></div>`; }).join('');
  document.getElementById('hgLook').innerHTML = ['TRB-003', 'NZL-001', 'SHW-011'].map(id => byId[id]).filter(Boolean).map(p => `<a class="hg-li" href="#" onclick="openProduct('${p.id}');return false"><span style="background-image:url('${tn(p.img)}')"></span><div><b>${esc(p.name)}</b><small>${esc(p.category.split(' · ').pop())}</small></div><em>${p.minPrice === p.maxPrice ? R(p.minPrice) : 'from ' + R(p.minPrice)}</em></a>`).join('');
  document.querySelectorAll('.hg-wa').forEach(e => e.textContent = waDisplay());
  document.getElementById('hgBulk').href = 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent('Hi Makkie Wholesalers, I would like a quote for: ');
}
'''
sub(r"(function go\(view\) \{)", JS.replace('\\', '\\\\') + r"\1")

CSS = r'''
/* ---------- home page (Look G) ---------- */
#homeg{background:#fff;padding-bottom:40px}
.hg-w{max-width:1240px;margin:0 auto;padding:0 16px}
.hg-chips{display:flex;gap:16px;overflow-x:auto;scrollbar-width:none;padding:14px 2px 14px}.hg-chips::-webkit-scrollbar{display:none}
.hg-chips a{flex:none;width:72px;text-align:center;font-size:12.5px;font-weight:600;line-height:1.25;color:var(--ink);text-decoration:none}
.hg-chips span{display:block;width:72px;height:72px;border-radius:50%;background:#F4EFE8 center/cover;border:1px solid var(--line);margin-bottom:6px}
.hg-hero{display:grid;background:#F4EFE8}.hg-hp{display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#F4EFE8}.hg-hp a{position:relative;aspect-ratio:1;background:#ddd center/cover;display:block}.hg-hp span{position:absolute;left:8px;bottom:8px;background:rgba(255,255,255,.94);color:var(--ink);font-size:13px;font-weight:700;padding:5px 10px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15)}.hg-ht{padding:24px 20px 28px}
.hg-ht small{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--scarlet)}
.hg-ht h1{font-family:var(--body);font-size:30px;line-height:1.12;font-weight:700;letter-spacing:-.02em;margin:8px 0 10px}.hg-ht p{color:var(--muted);margin:0 0 20px}
.hg-btn{display:inline-block;background:var(--ink);color:#fff!important;border-radius:8px;padding:13px 22px;font-weight:700;font-size:15px;margin:0 8px 8px 0;text-decoration:none;border:1.5px solid var(--ink);cursor:pointer}
.hg-btn.o{background:#fff;color:var(--ink)!important}.hg-btn.wa{background:var(--teal);border-color:var(--teal)}
.hg-trust{display:grid;grid-template-columns:1fr 1fr;gap:18px 14px;padding:22px 0;border-bottom:1px solid var(--line)}
.hg-trust div{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.35;color:var(--muted)}.hg-trust p{margin:0}.hg-trust b{display:block;color:var(--ink);font-size:14px}
.hg-trust svg{flex:none;width:26px;height:26px;fill:none;stroke:var(--scarlet);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.hg-h{font-family:var(--body);font-size:22px;font-weight:700;margin:36px 0 14px;display:flex;justify-content:space-between;align-items:baseline}
.hg-h a{font-size:14px;font-weight:700;color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.hg-cats{display:grid;grid-template-columns:1fr 1fr;gap:12px}.hg-cats a{display:block;background:#F4EFE8;border-radius:10px;overflow:hidden;color:var(--ink);text-decoration:none}
.hg-ci{display:block;aspect-ratio:1;background:center/cover}.hg-cats b{display:flex;justify-content:space-between;font-size:15px;padding:11px 12px}.hg-cats i{font-style:normal}
.hg-prods{display:grid;grid-template-columns:1fr 1fr;gap:22px 12px}.hg-pc a{color:var(--ink);text-decoration:none}
.hg-pi{display:block;aspect-ratio:1;border-radius:10px;background:#F4EFE8 center/cover}.hg-pc b{display:block;font-size:15px;margin-top:10px;line-height:1.25}.hg-pc small{display:block;color:var(--muted);font-size:13px}
.hg-pr{display:flex;align-items:center;justify-content:space-between;margin-top:8px}.hg-pr span{font-weight:700;font-size:16px}
.hg-pr button{background:#fff;border:1.5px solid var(--ink);border-radius:6px;font:700 13px var(--body);padding:6px 12px;cursor:pointer}
.hg-look{background:#F4EFE8;border-radius:12px;overflow:hidden;margin-top:40px}.hg-lp{aspect-ratio:4/3;background:50% 30%/cover}.hg-lt{padding:20px}
.hg-lt h3,.hg-bulk h3{font-family:var(--body);font-size:22px;margin:0 0 4px}.hg-lt p,.hg-bulk p{color:var(--muted);font-size:14px;margin:0 0 14px}
.hg-li{display:flex;gap:12px;align-items:center;background:#fff;border-radius:8px;padding:8px;margin-bottom:8px;color:var(--ink);text-decoration:none}
.hg-li span{width:56px;height:56px;border-radius:6px;flex:none;background:center/cover}.hg-li b{display:block;font-size:14px}.hg-li small{color:var(--muted);font-size:13px}.hg-li em{margin-left:auto;font-style:normal;font-weight:700;white-space:nowrap}
.hg-bulk{border:1.5px solid var(--ink);border-radius:12px;padding:22px 20px;margin-top:32px}
@media(min-width:900px){.hg-chips{flex-wrap:wrap;justify-content:center;gap:16px 18px;overflow:visible}.hg-chips a{width:78px;font-size:13px}.hg-chips span{width:78px;height:78px}
.hg-hero{grid-template-columns:1.25fr 1fr;align-items:center}.hg-hp{grid-template-rows:280px 280px}.hg-hp a{aspect-ratio:auto}.hg-hp span{font-size:14px;left:12px;bottom:12px}.hg-ht{padding:48px 56px}.hg-ht h1{font-size:44px}
.hg-trust{grid-template-columns:repeat(4,1fr)}.hg-cats{grid-template-columns:repeat(4,1fr);gap:16px}.hg-prods{grid-template-columns:repeat(4,1fr);gap:28px 16px}
.hg-look{display:grid;grid-template-columns:1.2fr 1fr;align-items:center}.hg-lp{aspect-ratio:auto;height:440px}.hg-lt{padding:40px}
.hg-bulk{display:flex;align-items:center;justify-content:space-between;gap:24px}.hg-bulk .hg-btn{margin:0}}
/* hover: circles and main photos grow slightly */
.hg-chips span{transition:transform .25s ease,box-shadow .25s ease}.hg-chips a:hover span,.hg-chips a:focus-visible span{transform:scale(1.12);box-shadow:0 6px 16px rgba(0,0,0,.18)}
.hg-chips{padding-top:18px;padding-bottom:18px}
.hg-hp{overflow:hidden}.hg-hp a{overflow:hidden;background-size:0 0!important}.hg-hp a:before{content:"";position:absolute;inset:0;background-image:inherit;background-size:cover;background-position:center;transition:transform .4s ease}.hg-hp a:hover:before,.hg-hp a:focus-visible:before{transform:scale(1.08)}.hg-hp span{z-index:1}
/* slimmer header and round help buttons on phones, so products get the screen */
@media(max-width:700px){header.top .bar{padding-top:8px;padding-bottom:8px;gap:8px;row-gap:8px}
.brand.newlogo{flex:1 1 auto;width:auto}.brand.newlogo .full{height:40px;width:auto;max-width:62vw}
.cartbtn{padding:6px 10px;font-size:14px}.search input{padding:9px 12px}nav.cats a{padding:9px 12px;font-size:13.5px}
.fab button{font-size:0;padding:13px;gap:0}.fab svg{width:24px;height:24px}}
'''
sub(r"(</style>\s*</head>)", CSS.replace('\\', '\\\\') + r"\1")

open(P, 'w', encoding='utf-8').write(s)
# copy the home photos next to the page
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(os.path.dirname(os.path.abspath(P)), 'home-g')
shutil.copytree(os.path.join(here, 'home-g'), dst, dirs_exist_ok=True)
print('home page patched,', len(s) // 1024, 'KB')
