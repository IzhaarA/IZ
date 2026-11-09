import os
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D,'make.py')).read().split('BASE =')[0])   # reuse CATS, PRODS, I, svg, ICON
CATS[0]=('Tribal Blankets','Basotho · Ndebele · Xhosa','bs_trb-014')
ICON['menu'] = '<path d="M3 7h18M3 12h18M3 17h18"/>'
ICON['user'] = '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>'
sv = lambda k, s=24, w=1.6: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'
FONTS = open(os.path.join(D,'fonts/fonts.css')).read().replace('url(gf','url(fonts/gf')
BASE = """*{box-sizing:border-box;margin:0;padding:0}a{color:inherit;text-decoration:none}body{padding-bottom:0}
.cr.e{font-weight:500}.cr.f{font-weight:700;text-transform:uppercase;font-size:13px}.cr{display:flex;gap:22px;overflow-x:auto;scrollbar-width:none;white-space:nowrap;padding:0 0 12px;font-size:14px;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}.cr::-webkit-scrollbar{display:none}
@media(min-width:900px){.cr{display:none}}
.w{max-width:1440px;margin:0 auto;padding:0 16px}img{display:block}
.scroll{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}.scroll::-webkit-scrollbar{display:none}.scroll>*{scroll-snap-align:start}
.bnav{position:fixed;left:0;right:0;bottom:0;height:64px;display:flex;z-index:9}
.bnav a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:11px;position:relative}
.bnav a i{position:absolute;top:6px;left:56%;font-style:normal;font-size:10px;border-radius:10px;padding:0 5px}
.bg{background-size:cover;background-position:center}
.desk{display:none!important}
@media(min-width:900px){.bnav{display:none}body{padding-bottom:0}.desk{display:flex!important}.mob{display:none!important}.w{padding:0 40px}}"""
def bnav(cls=''):
    return ''
def _old(cls=''):
    items = [('home','Home'),('grid','Shop'),('search','Search'),('bag','Basket'),('chat','WhatsApp')]
    return f'<nav class="bnav {cls}">' + ''.join(f'<a class="{"on" if k=="home" else ""}{" wa" if k=="chat" else ""}">{sv(k,24,1.7)}<span>{l}</span>{"<i>2</i>" if k=="bag" else ""}</a>' for k,l in items) + '</nav>'
def page(name, css, body):
    open(os.path.join(D,name),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>{FONTS}{BASE}{css}</style></head><body>{body}</body></html>')
NAV = ['Blankets','Shawls','Beads','Ndebele','Hats','Kangas','Bangles','Haberdashery']

# ===================== D · LUXURY (Louis Vuitton-inspired) =====================
D_CSS = """body{font-family:Inter,Arial,sans-serif;color:#19110B;background:#fff;font-weight:400}
.ann{background:#F6F5F3;font-size:11.5px;letter-spacing:.06em;text-align:center;padding:9px}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #eee}
.hd{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;height:64px}.hd .l,.hd .r{display:flex;gap:16px;align-items:center;font-size:13px}.hd .r{justify-content:flex-end}
.hd img{height:34px}.hd .l span{font-size:13px}
.hero{display:block}.hero .bg{aspect-ratio:4/5;background-position:50% 30%}
.hero .t{text-align:center;padding:30px 16px 0}
.hero small{font-size:11px;letter-spacing:.25em;color:#6b625b}.hero h1{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:40px;line-height:1.05;margin:10px 0 18px}
.hero a{font-size:13px;letter-spacing:.06em;border-bottom:1px solid #fff;padding-bottom:3px}
.sec{padding:56px 0 8px;text-align:center}.sec h2{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:32px}.sec p{font-size:13px;color:#6b625b;margin:8px 0 26px}
.cats{display:grid;grid-template-columns:1fr 1fr;gap:28px 8px;text-align:center}.cats .bg{aspect-ratio:3/4;background-color:#F6F5F3}.cats b{display:block;font-weight:400;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;margin-top:12px}
.prods{display:grid;grid-template-columns:1fr 1fr;gap:28px 8px;text-align:center}.prods .bg{aspect-ratio:1;background-color:#F6F5F3;background-size:78%;background-repeat:no-repeat}
.prods b{display:block;font-weight:400;font-size:13px;margin-top:14px}.prods span{display:block;font-size:13px;color:#6b625b;margin-top:4px}
.link{display:inline-block;margin-top:30px;border:1px solid #19110B;border-radius:30px;padding:13px 30px;font-size:13px}
.edit{display:grid;grid-template-columns:1fr;gap:40px 16px;margin-top:56px}.edit a{display:block}.edit .ph{aspect-ratio:4/5}.edit .t{text-align:center;padding-top:18px}
.edit h3{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:28px;margin-bottom:6px}.edit span{font-size:13px;border-bottom:1px solid #19110B;padding-bottom:2px}
.serv{background:#F6F5F3;margin-top:56px;padding:44px 16px;text-align:center;display:grid;gap:26px}.serv b{display:block;font-weight:500;font-size:13px;letter-spacing:.12em;text-transform:uppercase}.serv span{font-size:13px;color:#6b625b}
.bnav{background:#fff;border-top:1px solid #eee}.bnav a{color:#9a918a}.bnav a.on{color:#19110B}.bnav a i{background:#19110B;color:#fff}
@media(min-width:900px){.hero h1{font-size:56px}.cats{grid-template-columns:repeat(4,1fr);gap:40px 16px}.prods{grid-template-columns:repeat(4,1fr);gap:40px 16px}
.hero .bg{aspect-ratio:auto;height:72vh}.edit{grid-template-columns:1fr 1fr}.serv{grid-template-columns:repeat(3,1fr)}.hd{height:76px}.hd img{height:48px}.dnav{justify-content:center;gap:34px;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;padding:0 0 16px}}"""
dcats = [CATS[0],CATS[2],CATS[3],CATS[5],CATS[1],CATS[6],CATS[7],CATS[8]]
page('look-d.html', D_CSS, f"""<div class="ann">Pay securely by card, Instant EFT or SnapScan</div>
<header><div class="w"><div class="hd"><div class="l">{sv('menu')}<span class="desk" style="gap:8px;align-items:center">{sv('search',20)} Search</span></div><img src="img/makkies-logo.png"><div class="r"><span class="desk">{sv('chat',22)}</span><span class="mob">{sv('search',22)}</span>{sv('bag',22)}</div></div><div class="cr mob">{''.join(f'<a>{n}</a>' for n in NAV)}</div>
<div class="desk dnav">{''.join(f'<a>{n}</a>' for n in NAV)}</div></div></header>
<a class="hero" style="display:block"><div class="bg" style="background-image:url(img/hi_trb013.jpg)"></div><div class="t"><small>THE DECEMBER EDIT</small><h1>Basotho Blankets</h1><span class="link" style="margin-top:4px">Discover the collection</span></div></a>
<div class="w"><div class="sec"><h2>Explore a Category</h2><p>Blankets, beads and traditional goods since Marabastad</p>
<div class="cats">{''.join(f'<a><div class="bg" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b></a>' for c in dcats)}</div></div>
<div class="sec"><h2>Popular Right Now</h2><p>Our customers' favourites this week</p>
<div class="prods">{''.join(f'<a><div class="bg" style="background-image:url({I(p[3])});background-size:cover"></div><b>{p[0]}</b><span>{p[2]}</span></a>' for p in PRODS)}</div><a class="link">View all products</a></div></div>
<div class="edit w"><a><div class="bg ph" style="background-image:url({I('pay_ukhamba')});background-position:50% 25%"></div><div class="t"><h3>Ndebele Blankets</h3><span>Shop now</span></div></a>
<a><div class="bg ph" style="background-image:url({I('pay_wedding_shawl')})"></div><div class="t"><h3>Wedding Shawls</h3><span>Shop now</span></div></a></div>
<div class="serv"><div><b>Delivery</b><span>Courier or PAXI anywhere in South Africa</span></div><div><b>Secure payment</b><span>Card, Instant EFT or SnapScan</span></div><div><b>Client services</b><span>WhatsApp 072 323 5469</span></div></div>{bnav()}""")

# ===================== E · SPORT (Nike-inspired) =====================
E_CSS = """body{font-family:Inter,Arial,sans-serif;color:#111;background:#fff}
.ann{background:#F5F5F5;text-align:center;padding:10px;font-size:13px;font-weight:500}.ann u{text-underline-offset:3px}
header{position:sticky;top:0;z-index:5;background:#fff}.hd{display:flex;align-items:center;height:60px;gap:16px}.hd img{height:38px;margin-right:auto}
.sp{display:flex;align-items:center;gap:8px;background:#F5F5F5;border-radius:30px;height:40px;padding:0 14px;color:#707072;font-size:15px}
.hd .ib{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.hero .bg{aspect-ratio:4/5;background-position:50% 30%}.ht{text-align:center;padding:26px 16px 10px}
.ht small{font-size:15px;font-weight:500}.ht h1{font-family:Oswald,Impact,sans-serif;font-weight:600;text-transform:uppercase;font-size:52px;line-height:.95;letter-spacing:-.5px;margin:8px 0 10px}
.ht p{font-size:16px;line-height:1.45;color:#444;max-width:420px;margin:0 auto 22px}.pill{display:inline-block;background:#111;color:#fff;border-radius:30px;padding:10px 20px;font-weight:500;font-size:16px;margin:0 4px 8px}
h2{font-size:23px;font-weight:500;padding:44px 0 16px;display:flex;justify-content:space-between;align-items:center}h2 span{font-size:15px}
.cc{flex:0 0 78%}.cc .bg{aspect-ratio:3/4}.cc b{display:block;font-weight:500;font-size:17px;margin-top:12px}
.pc{flex:0 0 62%}.pc .bg{aspect-ratio:1;background-color:#F5F5F5}.pc b{display:block;font-weight:500;font-size:16px;margin-top:12px}.pc small{display:block;color:#707072;font-size:15px}.pc em{display:block;font-style:normal;font-weight:500;font-size:16px;margin-top:6px}
.feat .bg{aspect-ratio:1}.feat .ft{padding:20px 0}.feat small{font-size:15px;font-weight:500}.feat h3{font-family:Oswald,Impact,sans-serif;font-weight:600;font-size:34px;text-transform:uppercase;line-height:1;margin:6px 0 16px}
.tr{display:grid;grid-template-columns:1fr;gap:0;border-top:1px solid #e5e5e5;margin-top:30px}.tr p{line-height:1.4}.tr div{padding:18px 0;border-bottom:1px solid #e5e5e5;font-size:16px;font-weight:500;display:flex;gap:12px;align-items:center}.tr span{color:#707072;font-weight:400;font-size:14px;display:block}
.bnav{background:#fff;border-top:1px solid #e5e5e5}.bnav a{color:#707072}.bnav a.on{color:#111}.bnav a i{background:#111;color:#fff}
@media(min-width:900px){.hero{display:grid;grid-template-columns:1fr 1fr;gap:12px}.hero .bg{aspect-ratio:auto;height:640px}.hero .b2{display:block!important}
.ht h1{font-size:96px}.cc{flex:0 0 calc(33.33% - 7px)}.pc{flex:0 0 calc(25% - 8px)}.feats{display:grid;grid-template-columns:1fr 1fr;gap:12px}.tr{grid-template-columns:repeat(3,1fr);gap:20px}
.dnav{gap:26px;font-size:16px;font-weight:500;margin:0 auto}.hd{height:72px}.hd img{margin-right:0}}"""
ecats = [CATS[0],CATS[2],CATS[3],CATS[5],CATS[1],CATS[6],CATS[7]]
page('look-e.html', E_CSS, f"""<div class="ann">Now accepting card, Instant EFT &amp; SnapScan · <u>Shop now</u></div>
<header><div class="w"><div class="hd"><img src="img/makkies-logo.png"><div class="desk dnav">{''.join(f'<a>{n}</a>' for n in NAV[:6])}</div><div class="sp desk">{sv('search',20,2)} Search</div><a class="ib mob">{sv('search',24,1.8)}</a><a class="ib">{sv('bag',24,1.8)}</a><a class="ib mob">{sv('menu',24,1.8)}</a></div></div><div class="cr mob e">{''.join(f'<a>{n}</a>' for n in NAV)}</div></header>
<div class="hero"><div class="bg" style="background-image:url(img/hi_trb013.jpg)"></div><div class="bg b2" style="display:none;background-image:url({I('pay_ukhamba')});background-position:50% 25%"></div></div>
<div class="ht"><small>December Weddings</small><h1>Wrapped in<br>tradition</h1><p>Basotho, Ndebele and Xhosa blankets — delivered across South Africa.</p><a class="pill">Shop Blankets</a><a class="pill">Shop Beads</a></div>
<div class="w"><h2>Shop by Category</h2><div class="scroll">{''.join(f'<a class="cc"><div class="bg" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b></a>' for c in ecats)}</div>
<h2>Popular Right Now <span>Shop all</span></h2><div class="scroll">{''.join(f'<a class="pc"><div class="bg" style="background-image:url({I(p[3])})"></div><b>{p[0]}</b><small>{p[1]}</small><em>{p[2]}</em></a>' for p in PRODS)}</div>
<h2>Featured</h2><div class="feats"><a class="feat"><div class="bg" style="background-image:url(img/hi_trb022.jpg)"></div><div class="ft"><small>Seanamarena &amp; Victoria</small><h3>Basotho Classics</h3><span class="pill" style="margin:0">Shop</span></div></a>
<a class="feat"><div class="bg" style="background-image:url({I('pay_czech2')})"></div><div class="ft"><small>Preciosa Czech beads</small><h3>Beads for every colour</h3><span class="pill" style="margin:0">Shop</span></div></a></div>
<div class="tr"><div>{sv('bag',26,1.6)}<p>Delivery nationwide<span>Courier to your door or PAXI at any PEP</span></p></div><div>{sv('grid',26,1.6)}<p>Pay your way<span>Card, Instant EFT, SnapScan or EFT</span></p></div><div>{sv('chat',26,1.6)}<p>Need help?<span>WhatsApp 072 323 5469</span></p></div></div></div>{bnav()}""")

# ===================== F · STREET (Adidas-inspired) =====================
F_CSS = """body{font-family:Archivo,Arial,sans-serif;color:#000;background:#fff}
.ann{background:#000;color:#fff;text-align:center;padding:10px;font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #eceff1}.hd{display:flex;align-items:center;height:60px;gap:18px}.hd img{height:38px;margin-right:auto}
.sq{display:flex;align-items:center;gap:10px;background:#ECEFF1;height:40px;padding:0 12px;font-size:14px;color:#767677;width:240px}
.hero{display:block}.hero .bg{aspect-ratio:4/5;background-position:50% 30%}
.hero .t{padding:26px 16px 0}.hero h1{font-weight:900;font-style:italic;text-transform:uppercase;font-size:34px;line-height:1}
.hero p{font-size:16px;line-height:1.45;color:#444;margin:10px 0 20px}
.btn{display:inline-flex;align-items:center;gap:16px;background:#000;color:#fff;font-weight:700;font-size:14px;letter-spacing:.08em;text-transform:uppercase;padding:14px 16px}
.btn.w2{background:#fff;color:#000;border:1px solid #000;box-shadow:none}
h2{font-weight:900;font-style:italic;text-transform:uppercase;font-size:26px;padding:40px 0 14px}
.tabs{display:flex;gap:20px;border-bottom:1px solid #eceff1;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:14px;overflow:hidden;white-space:nowrap}.tabs a{padding-bottom:8px;color:#767677}.tabs a.on{color:#000;box-shadow:inset 0 -3px 0 #000}
.pc{flex:0 0 58%;border:1px solid transparent}.pc .bg{aspect-ratio:1;background-color:#ECEFF1;position:relative}
.pc .pr{display:block;font-size:15px;font-weight:700;margin-top:6px}.pc b{display:block;font-weight:600;font-size:15px;margin-top:12px}.pc small{display:block;color:#767677;font-size:13px;margin-top:2px}
.cg{display:grid;grid-template-columns:1fr 1fr;gap:24px 10px}.cg .bg{aspect-ratio:1}.cg b{display:block;margin-top:10px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.ban{background:#FFE14F;margin-top:40px;padding:30px 16px;display:grid;gap:16px}.ban h3{font-weight:900;font-style:italic;text-transform:uppercase;font-size:30px;line-height:1}.ban p{font-size:15px}
.links{display:grid;grid-template-columns:1fr;margin-top:30px}.links a{display:flex;justify-content:space-between;padding:17px 0;border-bottom:1px solid #eceff1;font-weight:700;font-size:15px;text-transform:uppercase}
.bnav{background:#fff;border-top:1px solid #eceff1}.bnav a{color:#767677}.bnav a.on{color:#000;font-weight:700}.bnav a i{background:#000;color:#fff}
@media(min-width:900px){.hero{display:grid;grid-template-columns:1.4fr 1fr;align-items:center;background:#ECEFF1}.hero .bg{aspect-ratio:auto;height:600px;background-position:50% 15%}.hero .t{padding:60px}.hero h1{font-size:56px}.pc{flex:0 0 calc(25% - 8px)}.cg{grid-template-columns:repeat(4,1fr)}
.ban{grid-template-columns:2fr 1fr;align-items:center;padding:40px 60px}.links{grid-template-columns:repeat(4,1fr);gap:0 30px}.dnav{gap:24px;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.04em}.hd{height:70px}}"""
page('look-f.html', F_CSS, f"""<div class="ann">Delivery across SA · Pay by card or EFT</div>
<header><div class="w"><div class="hd"><img src="img/makkies-logo.png"><div class="desk dnav">{''.join(f'<a>{n}</a>' for n in NAV[:7])}</div><div class="sq desk">Search {sv('search',18,2)}</div><span class="mob">{sv('search',24,1.8)}</span>{sv('bag',24,1.8)}<span class="mob">{sv('menu',24,1.8)}</span></div></div><div class="cr mob f">{''.join(f'<a>{n}</a>' for n in NAV)}</div></header>
<a class="hero" style="display:block"><div class="bg" style="background-image:url({I('pay_ukhamba')})"></div><div class="t"><h1>Made for<br>the big day</h1><p>Ndebele, Basotho &amp; Xhosa blankets for every ceremony.</p><span class="btn">Shop blankets <span>→</span></span></div></a>
<div class="w"><h2>Popular right now</h2><div class="tabs"><a class="on">Best sellers</a><a>New in</a><a>Weddings</a><a>Beads</a></div>
<div class="scroll">{''.join(f'<a class="pc"><div class="bg" style="background-image:url({I(p[3])})"></div><b>{p[0]}</b><small>{p[1]}</small><span class="pr">{p[2]}</span></a>' for p in PRODS)}</div>
<h2>Shop by category</h2><div class="cg">{''.join(f'<a><div class="bg" style="background-image:url({I(c[2])})"></div><b>{c[0]}</b></a>' for c in dcats)}</div></div>
<div class="ban"><div><h3>Pay online, your way</h3><p style="margin-top:8px">Card, Instant EFT or SnapScan — safe and instant.</p></div><span class="btn" style="justify-self:start">Start shopping <span>→</span></span></div>
<div class="w"><div class="links">{''.join(f'<a>{n}<span>›</span></a>' for n in NAV)}</div></div>{bnav()}""")
print('ok')
