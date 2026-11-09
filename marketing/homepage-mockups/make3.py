import os
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D,'make2.py')).read().split('# ===================== D')[0])
ICON['truck']='<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>'
ICON['card']='<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/>'
ICON['shop']='<path d="M4 10v10h16V10M3 6l2-3h14l2 3v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/>'
CSS = """body{font-family:Inter,Arial,sans-serif;color:#1d1b19;background:#fff;font-size:15px}
.ann{background:#1d1b19;color:#fff;text-align:center;font-size:13px;padding:9px 12px}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #ece8e2}
.hd{display:flex;align-items:center;gap:14px;height:62px}.hd img{height:36px}.hd .sp{flex:1}
.ic{position:relative;display:flex}.ic i{position:absolute;top:-6px;right:-8px;background:#C3312B;color:#fff;font-style:normal;font-size:10.5px;font-weight:600;border-radius:9px;padding:1px 5px}
.srch{display:flex;align-items:center;gap:10px;height:46px;border:1.5px solid #d9d3cb;border-radius:8px;padding:0 14px;color:#8a837c;font-size:15px;margin-bottom:12px}
.srch b{margin-left:auto;background:#1d1b19;color:#fff;font-weight:600;font-size:13px;border-radius:6px;padding:7px 12px}
.chips{display:flex;gap:16px;overflow-x:auto;scrollbar-width:none;padding:2px 0 14px}.chips::-webkit-scrollbar{display:none}
.chips a{flex:none;width:68px;text-align:center;font-size:12px;font-weight:500;line-height:1.25;color:#4a4540}
.chips .bg{width:68px;height:68px;border-radius:50%;margin-bottom:6px;border:1px solid #ece8e2}
.hero{display:grid;background:#F4EFE8}.hero .bg{aspect-ratio:5/4;background-position:50% 25%}.hero .t{padding:26px 20px 30px}
.hero small{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#C3312B}
.hero h1{font-size:31px;line-height:1.12;font-weight:700;letter-spacing:-.02em;margin:8px 0 10px}.hero p{color:#5a544e;line-height:1.5;margin-bottom:20px}
.btn{display:inline-block;background:#1d1b19;color:#fff;border-radius:8px;padding:14px 22px;font-weight:600;font-size:15px;margin:0 8px 8px 0}.btn.o{background:#fff;color:#1d1b19;border:1.5px solid #1d1b19;padding:12.5px 20px}
.trust{display:grid;grid-template-columns:1fr 1fr;gap:18px 14px;padding:22px 0;border-bottom:1px solid #ece8e2}.trust div{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.35;color:#5a544e}.trust b{display:block;color:#1d1b19;font-size:14px}
.trust svg{flex:none;color:#C3312B}
h2{font-size:22px;font-weight:700;letter-spacing:-.01em;margin:38px 0 16px;display:flex;justify-content:space-between;align-items:baseline}h2 a{font-size:14px;font-weight:600;text-decoration:underline;text-underline-offset:3px}
.cg{display:grid;grid-template-columns:1fr 1fr;gap:12px}.cg a{display:block;background:#F4EFE8;border-radius:10px;overflow:hidden}.cg .bg{aspect-ratio:1}.cg b{display:flex;justify-content:space-between;font-size:14.5px;font-weight:600;padding:11px 12px}
.pg{display:grid;grid-template-columns:1fr 1fr;gap:22px 12px}.pc .bg{aspect-ratio:1;border-radius:10px;background-color:#F4EFE8}
.pc b{display:block;font-weight:600;font-size:14.5px;margin-top:10px}.pc small{display:block;color:#7a736c;font-size:13px;margin-top:2px}
.pc .pr{display:flex;align-items:center;justify-content:space-between;margin-top:8px}.pc .pr span{font-weight:700;font-size:16px}.pc .pr a{border:1.5px solid #1d1b19;border-radius:6px;font-size:13px;font-weight:600;padding:6px 11px}
.look{background:#F4EFE8;border-radius:12px;overflow:hidden;margin-top:40px}.look>.bg{aspect-ratio:4/3;background-position:50% 30%}.look .t{padding:20px}
.look h3{font-size:22px;font-weight:700;margin-bottom:4px}.look p{color:#5a544e;font-size:14px;margin-bottom:14px}
.li{display:flex;gap:12px;align-items:center;background:#fff;border-radius:8px;padding:8px;margin-bottom:8px}.li .bg{width:56px;height:56px;border-radius:6px;flex:none}.li b{display:block;font-size:14px;font-weight:600}.li small{color:#7a736c;font-size:13px}.li span{margin-left:auto;font-weight:700}
.bulk{border:1.5px solid #1d1b19;border-radius:12px;padding:22px 20px;margin-top:40px}.bulk h3{font-size:20px;font-weight:700;margin-bottom:6px}.bulk p{color:#5a544e;line-height:1.5;margin-bottom:16px}
.wa{background:#0A7A44!important;color:#fff}
footer{background:#1d1b19;color:#d9d3cb;margin-top:48px;padding:34px 0 40px;font-size:14px}footer .fg{display:grid;grid-template-columns:1fr 1fr;gap:26px}footer b{display:block;color:#fff;margin-bottom:10px;font-size:14px}footer a{display:block;margin-bottom:8px}
footer .ad{grid-column:1/-1;line-height:1.6}
@media(min-width:900px){.hd{height:76px;gap:28px}.hd img{height:46px}.srch{margin:0;flex:1;max-width:560px}.chips{justify-content:center;gap:34px}.chips a{width:84px;font-size:13px}.chips .bg{width:84px;height:84px}
.hero{grid-template-columns:1.25fr 1fr;align-items:center}.hero .bg{aspect-ratio:auto;height:520px}.hero .t{padding:56px}.hero h1{font-size:46px}
.trust{grid-template-columns:repeat(4,1fr)}.cg{grid-template-columns:repeat(4,1fr);gap:16px}.pg{grid-template-columns:repeat(4,1fr);gap:28px 16px}
.look{display:grid;grid-template-columns:1.2fr 1fr}.look>.bg{aspect-ratio:auto;min-height:440px}.look{align-items:center}.look .t{padding:40px}
.row2{display:grid;grid-template-columns:2fr 1fr;gap:24px;align-items:stretch}.row2 .bulk{margin-top:40px}footer .fg{grid-template-columns:2fr 1fr 1fr 1fr}footer .ad{grid-column:auto}}"""
chips = [('All','pay_ukhamba')]+[(n,c) for n,c in [('Blankets','bs_trb-014'),('Shawls','cloudsoft_gsh-004'),('Czech Beads','pay_czech1'),('Chinese Beads','ch_ch-28'),('Ndebele','pay_ziela_gold'),('Hats','hat_ndh-002'),('Kangas','kg_kng-008'),('Mink','um_mnk-014'),('Bangles','bg_bng-001')]]
cats = [CATS[0],CATS[1],CATS[2],CATS[3],CATS[4],CATS[5],CATS[6],CATS[7]]
search_bar = f'<div class="srch">{sv("search",20,2)}Search 590+ products…<b>Search</b></div>'
page('look-g.html', CSS, f"""<div class="ann">Delivery across SA &nbsp;·&nbsp; Pay by card, EFT or SnapScan</div>
<header><div class="w"><div class="hd">{sv('menu',24,1.8)}<img src="img/makkies-logo.png"><span class="desk" style="flex:1">{search_bar}</span><span class="sp mob"></span><a class="ic desk">{sv('chat',24,1.7)}</a><a class="ic">{sv('bag',25,1.7)}<i>2</i></a></div>
<div class="mob" style="display:block">{search_bar}</div>
</div></header><div class="w"><div class="chips" style="padding-top:14px">{''.join(f'<a><div class="bg" style="background-image:url({I(c)})"></div>{n}</a>' for n,c in chips)}</div></div>
<div class="hero"><div class="bg" style="background-image:url(img/hi_trb013.jpg)"></div><div class="t"><small>December weddings &amp; ceremonies</small><h1>Traditional blankets, beads &amp; more, delivered to your door</h1>
<p>Basotho, Ndebele and Xhosa blankets, wedding shawls and Czech beads. Wholesale prices, shipped across South Africa.</p><a class="btn">Shop blankets</a><a class="btn o">Shop beads</a></div></div>
<div class="w"><div class="trust"><div>{sv('truck',26,1.6)}<p><b>Nationwide delivery</b>Courier or PAXI at any PEP</p></div><div>{sv('card',26,1.6)}<p><b>Pay safely online</b>Card, Instant EFT, SnapScan</p></div>
<div>{sv('shop',26,1.6)}<p><b>Visit our shop</b>Oriental Complex, Marabastad</p></div><div>{sv('chat',26,1.6)}<p><b>WhatsApp help</b>072 323 5469</p></div></div>
<h2>Shop by category <a>View all</a></h2><div class="cg">{''.join(f'<a><div class="bg" style="background-image:url({I(c[2])})"></div><b>{c[0]}<span>›</span></b></a>' for c in cats)}</div>
<h2>Best sellers <a>Shop all</a></h2><div class="pg">{''.join(f'<div class="pc"><div class="bg" style="background-image:url({I(p[3])})"></div><b>{p[0]}</b><small>{p[1]}</small><div class="pr"><span>{p[2]}</span><a>Add</a></div></div>' for p in PRODS)}</div>
<div class="look"><div class="bg" style="background-image:url({I('pay_ukhamba')})"></div><div class="t"><h3>Shop the wedding look</h3><p>Everything in this photo, ready to order.</p>
<div class="li"><div class="bg" style="background-image:url({I('pay_ukhamba')})"></div><div><b>Ukhamba blanket</b><small>Ndebele · red &amp; black</small></div><span>R595</span></div>
<div class="li"><div class="bg" style="background-image:url({I('pay_ziela_gold')})"></div><div><b>Neck Ziela</b><small>Gold or silver</small></div><span>R150</span></div>
<div class="li"><div class="bg" style="background-image:url({I('pay_wedding_shawl')})"></div><div><b>Wedding Shawl</b><small>White · 150×150cm</small></div><span>R175</span></div>
<a class="btn" style="margin-top:8px">Shop the look</a></div></div>
<div class="bulk"><h3>Buying for your shop or event?</h3><p>Get stock prices on 10 pieces or more. Send us your list on WhatsApp and we'll quote you the same day.</p><a class="btn wa">WhatsApp for a quote</a></div></div>
<footer><div class="w"><div class="fg"><div class="ad"><b>Makkie Wholesalers</b>Shop D4, Pretoria Oriental Complex<br>Entrance 6, 7th Street, Marabastad<br>012 323 5469 · orders@makkies.co.za</div>
<div><b>Shop</b><a>Blankets</a><a>Shawls</a><a>Beads</a><a>Ndebele</a></div><div><b>Help</b><a>Delivery</a><a>Returns</a><a>Terms</a><a>Privacy</a></div></div></div></footer>""")
print('ok')
