import os
H=os.path.dirname(os.path.abspath(__file__))
FONTS="../../calendar-2027/source/fonts/local.css"
WA="072 323 5469"
def dots(n,i,col):
    return f'<div class="dots" style="color:{col}">'+''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n))+'</div>'
CSS="""*{box-sizing:border-box;margin:0;padding:0}body{background:#777}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Montserrat,sans-serif;color:#221F1D;background:var(--bg)}
.a{position:absolute}.serif{font-family:'DM Serif Display',serif;font-weight:400}
.bt{left:0;top:236px;width:1080px}.bb{left:0;bottom:70px;width:1080px}
.eyebrow{left:0;width:100%;top:78px;text-align:center;font-size:30px;font-weight:700;letter-spacing:6px;color:var(--acc)}
.eyebrow .ln{display:inline-block;width:60px;height:3px;background:var(--acc);vertical-align:middle;margin:0 18px}
.title{left:0;width:100%;top:120px;text-align:center;font-size:82px;font-weight:500;letter-spacing:2px;text-transform:uppercase}
.photo{left:50%;top:372px;height:740px;transform:translateX(-50%);box-shadow:0 18px 40px rgba(34,31,29,.18);border-radius:4px;overflow:hidden}
.photo img{height:100%;display:block}
.price{right:70px;top:322px;width:200px;height:200px;border-radius:50%;background:#C3312B;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg);box-shadow:0 12px 28px rgba(195,49,43,.4);border:6px solid #fff}
.price small{font-size:24px;font-weight:700;letter-spacing:3px}.price b{font-size:62px;font-weight:800;line-height:1}
.foot{left:0;width:100%;bottom:22px;text-align:center;font-size:24px;font-weight:600;letter-spacing:1px;color:#6b625a}
.dots{position:absolute;left:0;width:100%;top:30px;display:flex;justify-content:center;gap:10px}
.dots i{width:11px;height:11px;border-radius:50%;background:currentColor;opacity:.25}.dots i.on{opacity:1}
.swipe{right:60px;bottom:205px;font-size:30px;font-weight:800;letter-spacing:4px;color:var(--acc)}
.pill{display:inline-block;background:#221F1D;color:#fff;border-radius:60px;padding:14px 34px;font-weight:700;letter-spacing:3px;font-size:28px}
.grid{left:70px;top:372px;width:940px;display:grid;gap:22px}
.gi{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 8px 20px rgba(34,31,29,.12);text-align:center;padding-bottom:10px}
.gi .im{background-size:cover;background-position:center}
.gi .nm{font-size:21px;font-weight:700;letter-spacing:1px;margin-top:8px;text-transform:uppercase}
.gi .pr{font-size:26px;font-weight:800;color:#C3312B}
"""
def product_slide(n,i,set_,p):
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,i,set_['acc'])}
<div class="a eyebrow">{p['eyebrow']}</div><div class="a title">{p['name']}</div>
<img class="a bt" src="ph/{set_['bt']}"><div class="a photo"><img src="ph/{p['img']}.png"></div>
<div class="a price"><small>ONLY</small><b>R{p['price']}</b></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Order at makkies.co.za · WhatsApp {WA}</div></div>'''
def cover(n,set_,c):
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,0,set_['acc'])}
<img class="a" src="ph/logo.png" style="left:470px;top:62px;width:140px">
<div class="a eyebrow" style="top:150px">{c['eyebrow']}</div>
<div class="a serif" style="left:0;width:100%;top:190px;text-align:center;font-size:84px;line-height:1">{c['title']}</div>
<img class="a bt" src="ph/{set_['bt']}" style="top:300px">
<div class="a photo" style="top:420px;height:600px"><img src="ph/{c['img']}.png"></div>
<div class="a" style="left:0;width:100%;top:1052px;text-align:center"><span class="pill">{c['pill']}</span></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Swipe to see every style →</div></div>'''
def grid_slide(n,i,set_,g,items,cols,imh):
    cells=''.join(f'<div class="gi"><div class="im" style="height:{imh}px;background-image:url(ph/{p["img"]}.png)"></div><div class="nm">{p["short"]}</div><div class="pr">R{p["price"]}</div></div>' for p in items)
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,i,set_['acc'])}
<div class="a serif" style="left:0;width:100%;top:92px;text-align:center;font-size:78px">{g['title']}</div>
<div class="a" style="left:0;width:100%;top:190px;text-align:center;font-size:28px;font-weight:600;color:#6b625a">{g['sub']}</div>
<img class="a bt" src="ph/{set_['bt']}">
<div class="a grid" style="grid-template-columns:repeat({cols},1fr)">{cells}</div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">{g['foot']}</div></div>'''
def order_slide(n,set_,o):
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,n-1,set_['acc'])}
<img class="a bt" src="ph/{set_['bt']}" style="top:150px">
<img class="a" src="ph/logo.png" style="left:340px;top:350px;width:400px">
<div class="a serif" style="left:0;width:100%;top:580px;text-align:center;font-size:76px">Order today</div>
<div class="a" style="left:0;width:100%;top:700px;text-align:center"><span class="pill" style="font-size:54px;padding:22px 60px;letter-spacing:1px;text-transform:none">makkies.co.za</span></div>
<div class="a" style="left:0;width:100%;top:840px;text-align:center;font-size:40px;font-weight:700"><span style="color:#25D366">●</span> WhatsApp {WA}</div>
<div class="a" style="left:0;width:100%;top:920px;text-align:center;font-size:30px;line-height:1.5;color:#4a423b">{o}</div>
<img class="a bb" src="ph/{set_['bb']}" style="bottom:120px"><div class="a foot" style="bottom:50px;letter-spacing:4px;font-size:22px">MARABASTAD, PRETORIA · WHOLESALE &amp; RETAIL</div></div>'''

HATSET=dict(bg='#F6F0E9',acc='#C3312B',bt='border_ndebele_top.png',bb='border_ndebele_bot.png')
hats=[('Beige','beige',200,'58'),('White','white',200,'58'),('Beaded','beaded',200,'58'),('Black','black',200,'58'),
      ('Brown','brown',200,'58'),('Brown Pattern','brownpattern',200,'58'),("Women’s Hat",'womens',200,'One size'),('Painted Cap','cap',150,'58')]
N=len(hats)+3
hs=[cover(N,HATSET,dict(eyebrow='HATS · HAND-PAINTED',title='Ndebele Painted Hats',img='beige',pill='8 STYLES IN STOCK · FROM R150'))]
for k,(nm,img,pr,sz) in enumerate(hats):
    hs.append(product_slide(N,k+1,HATSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>SIZE {sz.upper()}')))
hs.append(grid_slide(N,N-2,HATSET,dict(title='Pick your style.',sub='Hand-painted Ndebele hats',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=h[0],img=h[1],price=h[2]) for h in hats],4,262))
hs.append(order_slide(N,HATSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))

XSET=dict(bg='#F2EBDB',acc='#C8642A',bt='border_xhosa_top.png',bb='border_xhosa_bot.png')
xs_=[('Black Stripe','xblack',300,'180 × 200 CM'),('Purple Stripe','xpurple',300,'180 × 220 CM'),('Red Stripe','xred',300,'180 × 220 CM')]
N2=len(xs_)+3
xs=[cover(N2,XSET,dict(eyebrow='TRIBAL BLANKETS · XHOSA',title='Xhosa Tribal Stripe',img='xblack',pill='3 COLOURS · R300 EACH'))]
for k,(nm,img,pr,sz) in enumerate(xs_):
    xs.append(product_slide(N2,k+1,XSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>{sz}')))
xs.append(grid_slide(N2,N2-2,XSET,dict(title='One classic. Three colours.',sub='Felt finish · 95% polyester, 5% cotton',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in xs_],3,560))
xs.append(order_slide(N2,XSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))


BSET=dict(bg='#F2EBDB',acc='#B23A2E',bt='border_basotho_top.png',bb='border_basotho_bot.png')
fr=[('Black / White','fblack',225),('Red / White','fred',225),('Grey / White','fgrey',225)]
N3=len(fr)+3
fs=[cover(N3,BSET,dict(eyebrow='TRIBAL BLANKETS · BASOTHO',title='Basotho Frill',img='fblack',pill='3 COLOURS · R225 EACH'))]
for k,(nm,img,pr) in enumerate(fr):
    fs.append(product_slide(N3,k+1,BSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>150 × 160 CM')))
fs.append(grid_slide(N3,N3-2,BSET,dict(title='Pick your colour.',sub='Fringed Basotho blanket · 150 × 160 cm',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in fr],3,560))
fs.append(order_slide(N3,BSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))

el=[('Black / White','eblack',275),('Blue','eblue',275),('Orange','eorange',275),('Red','ered',275),('Turquoise','eturq',275)]
N4=len(el)+3
es=[cover(N4,BSET,dict(eyebrow='TRIBAL BLANKETS · BASOTHO',title='Elizabeth Basotho',img='eturq',pill='5 COLOURS · R275 EACH'))]
for k,(nm,img,pr) in enumerate(el):
    es.append(product_slide(N4,k+1,BSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>150 × 160 CM')))
es.append(grid_slide(N4,N4-2,BSET,dict(title='Pick your colour.',sub='Basotho heritage blanket · 150 × 160 cm',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in el],3,300))
es.append(order_slide(N4,BSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))

for name,slides in (('hats',hs),('xhosa',xs),('frill',fs),('elizabeth',es)):
    open(os.path.join(H,f'ig_{name}.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>'+''.join(slides)+'</body></html>')
print(len(hs),len(xs))
