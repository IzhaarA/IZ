import os
D = os.path.dirname(os.path.abspath(__file__))
CATS = [('Tribal Blankets', 'Basotho · Ndebele · Xhosa', 'bs_trb-013'), ('Mink Blankets', 'Soft & warm', 'um_mnk-014'),
        ('Shawls & Throws', 'Wedding · cloudsoft · plain', 'cloudsoft_gsh-004'), ('Czech Beads', 'Preciosa · ¼kg', 'pay_czech1'),
        ('Chinese Beads', '450g packets', 'ch_ch-28'), ('Ndebele', 'Ziela · axes · aprons', 'pay_ziela_gold'),
        ('Hats & Berets', 'Ndebele hats · berets', 'hat_ndh-002'), ('Kangas', 'R35 each', 'kg_kng-008'),
        ('Bangles', 'Copper · brass · matseka', 'bg_bng-001'), ('Haberdashery', 'Cotton · twine · wool', 'ct_cot-011')]
PRODS = [('Ukhamba', 'Ndebele blanket', 'R595', 'pay_ukhamba'), ('Wedding Shawl', 'White · 150×150cm', 'R175', 'pay_wedding_shawl'),
         ('Neck Ziela', 'Gold or silver', 'R150', 'pay_ziela_gold'), ('Sefate', 'Basotho blanket', 'R1,100', 'bs_trb-014'),
         ('Beetee Tekkies', 'Hand-painted', 'R250', 'pay_tekkies'), ('Xhosa Tribal Stripe', '3 colours', 'R300', 'pay_xhosa_black'),
         ('Paris Mink', 'Queen/king · 2ply', 'R775', 'um_mnk-014'), ('Umbhalo', 'Ndebele blanket', 'R595', 'pay_umbhalo')]
I = lambda n: f'img/{n}.jpg'
ICON = {  # simple line icons for the bottom bar
 'home': '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 'grid': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 'bag': '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 'chat': '<path d="M4 20l1.5-4A8 8 0 1 1 9 19z"/>'}
svg = lambda k, c='currentColor': f'<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'
def bottom_nav(dark):
    items = [('home', 'Home'), ('grid', 'Categories'), ('search', 'Search'), ('bag', 'Basket'), ('chat', 'WhatsApp')]
    return '<nav class="bnav">' + ''.join(f'<a class="{"on" if k == "home" else ""}{" wa" if k == "chat" else ""}">{svg(k)}<span>{l}</span>{"<i>0</i>" if k == "bag" else ""}</a>' for k, l in items) + '</nav>'
def pcard(p):
    return f'<div class="pc"><div class="pi" style="background-image:url({I(p[3])})"></div><div class="pt"><b>{p[0]}</b><small>{p[1]}</small><em>{p[2]}</em></div></div>'

BASE = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Source Sans 3',Arial,sans-serif;color:#221F1D}a{color:inherit;text-decoration:none}
.w{max-width:1180px;margin:0 auto;padding:0 16px}
.stripe{height:6px;background:linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96%)}
.search{display:flex;align-items:center;gap:10px;border-radius:14px;padding:0 16px;height:52px;font-size:17px;color:#7a736c}
.sec{padding:22px 0 6px}.sec h2{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:28px;margin-bottom:12px;display:flex;align-items:baseline;justify-content:space-between}
.sec h2 a{font-family:Arial;font-size:15px;color:#C3312B;font-weight:700}
.row{display:flex;gap:12px;overflow:hidden}.pc{flex:0 0 46%;border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.07)}
.pi{aspect-ratio:1;background-size:cover;background-position:center}.pt{padding:10px 12px 12px}.pt b{display:block;font-size:16px}
.pt small{display:block;color:#7a736c;font-size:13px;margin-top:2px}.pt em{display:block;font-style:normal;font-weight:800;font-size:18px;margin-top:6px}
.bnav{position:fixed;left:0;right:0;bottom:0;height:68px;display:flex;border-top:1px solid #e3ddd4;z-index:9}
.bnav a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:12px;font-weight:700;position:relative}
.bnav a i{position:absolute;top:7px;left:56%;background:#C3312B;color:#fff;font-style:normal;font-size:11px;border-radius:10px;padding:0 6px}
.trust{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:16px 0}.trust div{border-radius:12px;padding:12px;font-size:13px;font-weight:700;text-align:center}
.trust b{display:block;font-size:22px}
body{padding-bottom:80px}
@media(min-width:900px){.bnav{display:none}body{padding-bottom:0}.pc{flex:0 0 calc(25% - 9px)}.desk{display:flex!important}.mob{display:none!important}}
.desk{display:none}"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><style>@font-face{font-family:"DM Serif Display";src:url(/home/user/IZ/marketing/category-ads-source/fonts/dmserif.woff2)}</style>'

def page(name, css, body):
    open(os.path.join(D, name), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<style>@font-face{{font-family:"DM Serif Display";src:url(dmserif.woff2)}}{BASE}{css}</style></head><body>{body}</body></html>')

# ---------- A: clean & simple (white, big tiles) ----------
A_CSS = """body{background:#fff}.top{background:#0A7A44;color:#fff;font-size:13px;font-weight:700;text-align:center;padding:7px 10px}
header{background:#fff;padding:12px 0 14px;border-bottom:1px solid #eee}.hd{display:flex;align-items:center;justify-content:space-between}
.hd img{height:42px}.hd .bk{font-weight:800;font-size:15px;border:2px solid #221F1D;border-radius:30px;padding:6px 14px}
.search{background:#F2EFEA;margin-top:12px}
.cats{display:grid;grid-template-columns:1fr 1fr;gap:12px}.cat{border-radius:16px;overflow:hidden;background:#F7F4EF}
.cat .ci{aspect-ratio:4/3;background-size:cover;background-position:center}.cat b{display:block;font-size:17px;padding:10px 12px 2px}
.cat small{display:block;font-size:13px;color:#7a736c;padding:0 12px 12px}
.trust div{background:#F7F4EF}.bnav{background:#fff}.bnav a{color:#8a837c}.bnav a.on{color:#221F1D}.bnav a.wa{color:#0A7A44}
@media(min-width:900px){.cats{grid-template-columns:repeat(5,1fr)}.hd .search{margin:0 30px;flex:1}}"""
cats = ''.join(f'<a class="cat"><div class="ci" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b><small>{c[1]}</small></a>' for c in CATS)
page('look-a.html', A_CSS, f"""<div class="top">💳 Pay by card, Instant EFT or SnapScan · 🚚 Delivery across SA</div>
<header><div class="w"><div class="hd"><img src="img/makkies-logo.png"><div class="search desk">{svg('search')} Search blankets, beads, colours…</div><span class="bk">Basket 0</span></div>
<div class="search mob">{svg('search')} Search blankets, beads, colours…</div></div></header>
<div class="w"><div class="sec"><h2>Shop by category <a>See all →</a></h2><div class="cats">{cats}</div></div>
<div class="trust"><div><b>🚚</b>Delivery across SA</div><div><b>🔒</b>Secure payment</div><div><b>💬</b>WhatsApp help</div></div>
<div class="sec"><h2>Popular right now <a>See all →</a></h2><div class="row">{''.join(pcard(p) for p in PRODS)}</div></div></div>{bottom_nav(False)}""")

# ---------- B: warm heritage (cream, welcome banner, round shortcuts) ----------
B_CSS = """body{background:#F6F0E6}header{background:#1F1B1D;padding:12px 0 14px}.hd{display:flex;align-items:center;justify-content:space-between}
.hd img{height:44px}.hd .bk{color:#fff;font-weight:800;font-size:15px;border:2px solid rgba(255,255,255,.6);border-radius:30px;padding:6px 14px}
.search{background:#fff;margin-top:12px}
.hero{margin:16px 0 4px;border-radius:20px;overflow:hidden;background:#fff;display:grid;grid-template-columns:1fr}
.hero .hp{aspect-ratio:16/10;background-size:cover;background-position:50% 30%}.hero .ht{padding:18px 18px 20px}
.hero h1{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:32px;line-height:1.1}.hero p{color:#6F6A63;font-size:16px;margin:8px 0 14px}
.btn{display:inline-block;border-radius:30px;padding:12px 20px;font-weight:800;font-size:15px;margin:0 8px 8px 0}.b1{background:#C3312B;color:#fff}.b2{border:2px solid #221F1D}
.circ{display:flex;gap:14px;overflow:hidden;padding:4px 0}.circ a{flex:0 0 78px;text-align:center;font-size:12.5px;font-weight:700;line-height:1.2}
.circ i{display:block;width:78px;height:78px;border-radius:50%;background-size:cover;background-position:center;border:3px solid #fff;box-shadow:0 0 0 2px #C3312B;margin-bottom:6px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:12px}.tile{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:1}
.tile .ti{position:absolute;inset:0;background-size:cover;background-position:center}.tile b{position:absolute;left:10px;right:10px;bottom:10px;background:#fff;border-radius:10px;padding:8px 10px;font-size:15px}
.trust div{background:#fff}.bnav{background:#1F1B1D}.bnav a{color:#bfb7ae}.bnav a.on{color:#FFE14F}.bnav a.wa{color:#25D366}
@media(min-width:900px){.hero{grid-template-columns:1.1fr 1fr}.hero .hp{aspect-ratio:auto;order:2}.hero .ht{padding:44px}.hero h1{font-size:46px}
.tiles{grid-template-columns:repeat(4,1fr)}.circ{justify-content:space-between}.hd .search{margin:0 30px;flex:1}}"""
circ = ''.join(f'<a><i style="background-image:url({I(c[2])})"></i>{c[0]}</a>' for c in CATS)
tiles = ''.join(f'<a class="tile"><div class="ti" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b></a>' for c in CATS[:8])
page('look-b.html', B_CSS, f"""<header><div class="w"><div class="hd"><img src="img/logo-header.png"><div class="search desk">{svg('search')} Search blankets, beads, colours…</div><span class="bk">Basket 0</span></div>
<div class="search mob">{svg('search')} Search blankets, beads, colours…</div></div></header><div class="stripe"></div>
<div class="w"><div class="hero"><div class="hp" style="background-image:url({I('pay_ukhamba')})"></div><div class="ht"><h1>Blankets, beads &amp; traditional goods</h1>
<p>Wholesale &amp; retail from Marabastad, Pretoria. Delivered anywhere in South Africa.</p><a class="btn b1">Shop blankets</a><a class="btn b2">Shop beads</a></div></div>
<div class="sec"><div class="circ">{circ}</div></div>
<div class="sec"><h2>Shop by category <a>All →</a></h2><div class="tiles">{tiles}</div></div>
<div class="trust"><div><b>🚚</b>PAXI to any PEP</div><div><b>🔒</b>Card · EFT · SnapScan</div><div><b>💬</b>072 323 5469</div></div>
<div class="sec"><h2>Popular right now <a>All →</a></h2><div class="row">{''.join(pcard(p) for p in PRODS)}</div></div></div>{bottom_nav(True)}""")

# ---------- C: bold & simple (photo banner, tap-friendly list) ----------
C_CSS = """body{background:#fff}header{background:#fff;padding:12px 0 10px}.hd{display:flex;align-items:center;justify-content:space-between}
.hd img{height:40px}.hd .bk{font-weight:800;font-size:15px;background:#221F1D;color:#fff;border-radius:30px;padding:8px 14px}
.search{background:#F2EFEA;margin-top:10px}
.pills{display:flex;gap:8px;overflow:hidden;padding:10px 0 4px}.pills a{flex:none;border:1.5px solid #ddd6cc;border-radius:30px;padding:9px 16px;font-weight:700;font-size:14px}
.pills a.on{background:#221F1D;color:#fff;border-color:#221F1D}
.ban{position:relative;border-radius:20px;overflow:hidden;aspect-ratio:4/5;margin-top:8px}.ban .bi{position:absolute;inset:0;background-size:cover;background-position:50% 35%}
.ban .bt{position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.75));display:flex;flex-direction:column;justify-content:flex-end;padding:22px;color:#fff}
.ban small{font-weight:800;letter-spacing:3px;font-size:12px;color:#FFE14F}.ban h1{font-size:34px;font-weight:800;line-height:1.05;margin:6px 0 14px}
.ban a{align-self:flex-start;background:#fff;color:#221F1D;border-radius:30px;padding:12px 22px;font-weight:800}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}.two a{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:1;color:#fff}
.two .ti{position:absolute;inset:0;background-size:cover;background-position:center}.two b{position:absolute;left:0;right:0;bottom:0;padding:30px 12px 12px;font-size:19px;background:linear-gradient(transparent,rgba(0,0,0,.7))}
.list a{display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid #eee}.list i{width:64px;height:64px;border-radius:12px;background-size:cover;background-position:center;flex:none}
.list b{display:block;font-size:17px}.list small{color:#7a736c;font-size:13px}.list span{margin-left:auto;font-size:22px;color:#b3aba2}
.trust div{background:#F2EFEA}.bnav{background:#fff}.bnav a{color:#8a837c}.bnav a.on{color:#C3312B}.bnav a.wa{color:#0A7A44}
@media(min-width:900px){.ban{aspect-ratio:21/8}.ban h1{font-size:52px}.two{grid-template-columns:repeat(4,1fr)}.list{columns:2;column-gap:40px}.list a{break-inside:avoid}.hd .search{margin:0 30px;flex:1}}"""
pills = ''.join(f'<a class="{"on" if i == 0 else ""}">{c}</a>' for i, c in enumerate(['All', 'Blankets', 'Shawls', 'Beads', 'Ndebele', 'Hats', 'Kangas', 'Haberdashery']))
two = ''.join(f'<a><div class="ti" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b></a>' for c in (CATS[0], CATS[3], CATS[2], CATS[5]))
lst = ''.join(f'<a><i style="background-image:url({I(c[2])})"></i><div><b>{c[0]}</b><small>{c[1]}</small></div><span>›</span></a>' for c in CATS)
page('look-c.html', C_CSS, f"""<header><div class="w"><div class="hd"><img src="img/makkies-logo.png"><div class="search desk">{svg('search')} Search blankets, beads, colours…</div><span class="bk">Basket 0</span></div>
<div class="search mob">{svg('search')} Search blankets, beads, colours…</div><div class="pills">{pills}</div></div></header>
<div class="w"><div class="ban"><div class="bi" style="background-image:url({I('bs_trb-013')})"></div><div class="bt"><small>DECEMBER WEDDINGS</small><h1>Basotho blankets<br>from R250</h1><a>Shop now →</a></div></div>
<div class="two">{two}</div>
<div class="sec"><h2>All categories</h2><div class="list">{lst}</div></div>
<div class="trust"><div><b>🚚</b>Delivery across SA</div><div><b>🔒</b>Pay online safely</div><div><b>💬</b>WhatsApp us</div></div>
<div class="sec"><h2>Popular right now <a>See all →</a></h2><div class="row">{''.join(pcard(p) for p in PRODS)}</div></div></div>{bottom_nav(False)}""")
print('ok')
