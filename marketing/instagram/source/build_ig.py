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
<div class="a eyebrow">{p['eyebrow']}</div><div class="a title" style="font-size:{82 if len(p['name'])<=16 else (66 if len(p['name'])<=22 else 56)}px;top:{120 if len(p['name'])<=16 else 128}px">{p['name']}</div>
<img class="a bt" src="ph/{set_['bt']}"><div class="a photo"><img src="ph/{p['img']}.png"></div>
<div class="a price"><small>{p.get('pre','ONLY')}</small><b>R{p['price']}</b></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Order at makkies.co.za · WhatsApp {WA}</div></div>'''
def cover(n,set_,c):
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,0,set_['acc'])}
<img class="a" src="ph/logo.png" style="left:470px;top:62px;width:140px">
<div class="a eyebrow" style="top:150px">{c['eyebrow']}</div>
<div class="a serif" style="left:0;width:100%;top:190px;text-align:center;font-size:84px;line-height:1">{c['title']}</div>
<img class="a bt" src="ph/{set_['bt']}" style="top:300px">
<div class="a photo" style="top:420px;height:600px"><img src="ph/{c['img']}.png"></div>
<div class="a price" style="right:120px;top:380px"><small>{c.get('pre','ONLY')}</small><b>R{c['price']}</b></div>
<div class="a" style="left:0;width:100%;top:1052px;text-align:center"><span class="pill">{c['pill']}</span></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Swipe to see every style →</div></div>'''
def grid_slide(n,i,set_,g,items,cols,imh):
    cells=''.join(f'<div class="gi"><div class="im" style="height:{imh}px;background-image:url(ph/{p["img"]}.png)"></div><div class="nm">{p["short"]}</div><div class="pr">{p.get("ptxt","R"+str(p["price"]))}</div></div>' for p in items)
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
hs=[cover(N,HATSET,dict(eyebrow='HATS · HAND-PAINTED',title='Ndebele Painted Hats',img='beige',price=200,pill='8 STYLES IN STOCK · FROM R150'))]
for k,(nm,img,pr,sz) in enumerate(hats):
    hs.append(product_slide(N,k+1,HATSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>SIZE {sz.upper()}')))
hs.append(grid_slide(N,N-2,HATSET,dict(title='Pick your style.',sub='Hand-painted Ndebele hats',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=h[0],img=h[1],price=h[2]) for h in hats],4,262))
hs.append(order_slide(N,HATSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))

XSET=dict(bg='#F2EBDB',acc='#C8642A',bt='border_xhosa_top.png',bb='border_xhosa_bot.png')
xs_=[('Black Stripe','xblack',300,'180 × 200 CM'),('Purple Stripe','xpurple',300,'180 × 220 CM'),('Red Stripe','xred',300,'180 × 220 CM')]
N2=len(xs_)+3
xs=[cover(N2,XSET,dict(eyebrow='TRIBAL BLANKETS · XHOSA',title='Xhosa Tribal Stripe',img='xblack',price=300,pill='3 COLOURS · R300 EACH'))]
for k,(nm,img,pr,sz) in enumerate(xs_):
    xs.append(product_slide(N2,k+1,XSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>{sz}')))
xs.append(grid_slide(N2,N2-2,XSET,dict(title='One classic. Three colours.',sub='Felt finish · 95% polyester, 5% cotton',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in xs_],3,560))
xs.append(order_slide(N2,XSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))


BSET=dict(bg='#F2EBDB',acc='#B23A2E',bt='border_basotho_top.png',bb='border_basotho_bot.png')
fr=[('Black / White','fblack',225),('Red / White','fred',225),('Grey / White','fgrey',225)]
N3=len(fr)+3
fs=[cover(N3,BSET,dict(eyebrow='TRIBAL BLANKETS · BASOTHO',title='Basotho Frill',img='fblack',price=225,pill='3 COLOURS · R225 EACH'))]
for k,(nm,img,pr) in enumerate(fr):
    fs.append(product_slide(N3,k+1,BSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>150 × 160 CM')))
fs.append(grid_slide(N3,N3-2,BSET,dict(title='Pick your colour.',sub='Fringed Basotho blanket · 150 × 160 cm',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in fr],3,560))
fs.append(order_slide(N3,BSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))

el=[('Black / White','eblack',275),('Blue','eblue',275),('Orange','eorange',275),('Red','ered',275),('Turquoise','eturq',275)]
N4=len(el)+3
es=[cover(N4,BSET,dict(eyebrow='TRIBAL BLANKETS · BASOTHO',title='Elizabeth Basotho',img='eturq',price=275,pill='5 COLOURS · R275 EACH'))]
for k,(nm,img,pr) in enumerate(el):
    es.append(product_slide(N4,k+1,BSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>150 × 160 CM')))
es.append(grid_slide(N4,N4-2,BSET,dict(title='Pick your colour.',sub='Basotho heritage blanket · 150 × 160 cm',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in el],3,300))
es.append(order_slide(N4,BSET,'Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'))


SSET=dict(bg='#F6F0E9',acc='#B23A2E',bt='border_shawl_top.png',bb='border_shawl_bot.png')
ORDER='Delivery across South Africa · PAXI to any PEP store<br>or collect from Shop D4, Pretoria Oriental Complex, Marabastad'
def shawl_set(title,items,price,size,pill,gsub,cols,imh,eyeword='COLOURS'):
    N=len(items)+3
    out=[cover(N,SSET,dict(eyebrow='SHAWLS · THROWS',title=title,img=items[0][1],price=price,pill=pill))]
    for k,(nm,img) in enumerate(items):
        out.append(product_slide(N,k+1,SSET,dict(name=nm,img=img,price=price,eyebrow=f'{k+1:02d}<span class="ln"></span>{size}')))
    out.append(grid_slide(N,N-2,SSET,dict(title='Pick your colour.' if eyeword=='COLOURS' else 'Pick your design.',sub=gsub,foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
        [dict(short=i[0],img=i[1],price=price) for i in items],cols,imh))
    out.append(order_slide(N,SSET,ORDER))
    return out
ps=shawl_set('Plain Shawls',[('Emerald','pemerald'),('Black','pblack'),('Grey','pgrey'),('Royal Blue','proyal'),('Yellow','pyellow'),('Magenta','pmagenta'),('Dusty Pink','pdusty'),('Red','pred')],
   95,'120 × 120 CM','29 COLOURS IN STOCK · R95 EACH','8 shown · 29 colours in stock · see them all at makkies.co.za',4,262)
ss=shawl_set('Soft Touch Shawls',[('Green','sgreen'),('Blue','sblue'),('Red','sred'),('Charcoal','scharcoal'),('Mustard','smustard'),('Pink','spink')],
   150,'130 × 130 CM','6 COLOURS IN STOCK · R150 EACH','Soft touch shawl · 130 × 130 cm',3,300)
cs=shawl_set('Small Check Shawls',[('Multi Stripe','cmulti'),('Rose','crose'),('Navy Check','cnavy'),('Brown Check','cbrown'),('Black Check','cblack')],
   60,'120 × 120 CM','5 DESIGNS IN STOCK · R60 EACH','Small check shawl · 120 × 120 cm',3,300,eyeword='DESIGNS')


NSET=HATSET
def coll(title,eyebrow,hero,pill,items,gtitle,gsub,cols,imh):
    N=len(items)+3
    h=[it for it in items if it['i']==hero][0]
    out=[cover(N,NSET,dict(eyebrow=eyebrow,title=title,img=hero,price=h['p'],pre=h.get('pre','ONLY'),pill=pill))]
    for k,it in enumerate(items):
        out.append(product_slide(N,k+1,NSET,dict(name=it['n'],img=it['i'],price=it['p'],pre=it.get('pre','ONLY'),eyebrow=f"{k+1:02d}<span class='ln'></span>{it['e']}")))
    out.append(grid_slide(N,N-2,NSET,dict(title=gtitle,sub=gsub,foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
        [dict(short=it.get('s',it['n']),img=it['i'],price=it['p'],ptxt=('from ' if it.get('pre')=='FROM' else '')+'R'+str(it['p'])) for it in items],cols,imh))
    out.append(order_slide(N,NSET,ORDER))
    return out
nb=coll('Ndebele Blankets','NDEBELE COLLECTION','nukhamba','9 DESIGNS · FROM R170',[
  dict(n='Mini Umbhalo',i='nminiumbhalo',p=365,e='110 × 130 CM'),
  dict(n='Umbhalo',i='numbhalo',p=595,e='150 × 160 CM'),
  dict(n='Ukhamba',i='nukhamba',p=595,e='150 × 160 CM'),
  dict(n='Ibhidi',i='nibhidi',p=595,e='150 × 160 CM'),
  dict(n='Msosiswa',i='nmsosiswa',p=365,e='110 × 130 CM · 7 COLOURS'),
  dict(n='Ndebele Furpile',s='Ndebele Furpile',i='nfurpile',p=170,pre='FROM',e='2 SIZES · R170 / R230'),
  dict(n='Beetee Furpile',i='nbeetee',p=170,pre='FROM',e='2 SIZES · R170 / R230'),
  dict(n='Unosinky',i='nunosinky',p=595,e='140 × 180 CM · 2 COLOURS'),
  dict(n='Indlovukazi',i='nindlovukazi',p=550,e='150 × 160 CM')],
  'Pick your blanket.','Ndebele heritage blankets · 9 designs',3,172)
na=coll('Ndebele Accessories','NDEBELE COLLECTION','nneckgold','ZIELA · CHOKERS · BELTS · FROM R40',[
  dict(n='Leg Ziela',i='nlegziela',p=60,pre='FROM',e='5M R60 · 10M R120 · 100M R1100'),
  dict(n='Thick Ziela',i='nthickziela',p=60,pre='FROM',e='5M R60 · 10M R120 · 100M R1100'),
  dict(n='Neck Ziela — Gold',s='Neck Ziela Gold',i='nneckgold',p=150,e='BUTTON NECK ZIELA · READY-MADE'),
  dict(n='Neck Ziela — Silver',s='Neck Ziela Silver',i='nnecksilver',p=150,e='BUTTON NECK ZIELA · READY-MADE'),
  dict(n='Ndebele Choker',s='Choker',i='nchoker',p=75,e='TRADITIONAL RING CHOKER'),
  dict(n='Ndebele Bracelet',s='Bracelet',i='nbracelet',p=40,pre='FROM',e='SHORT R40 · LONG R80'),
  dict(n='Ndebele Belt',s='Belt',i='nbelt',p=120,e='TRADITIONAL GOLD BELT')],
  'Complete the look.','Traditional Ndebele accessories',4,250)
nt=coll('Ndebele Tekkies','NDEBELE COLLECTION','ntekndebele','3 STYLES · UK3–UK8 · FROM R150',[
  dict(n='Beaded Tekkies',s='Beaded',i='ntekbeaded',p=150,e='UK3–UK8 · CANVAS'),
  dict(n='Beetee Tekkies',s='Beetee Painted',i='ntekbeetee',p=250,e='HAND-PAINTED · UK3–UK8 · CANVAS'),
  dict(n='Ndebele Tekkies',s='Ndebele Painted',i='ntekndebele',p=200,e='HAND-PAINTED · UK3–UK8 · CANVAS')],
  'Pick your pair.','Hand-finished canvas tekkies · UK3–UK8',3,520)


STSET=dict(bg='#F6F0E9',acc='#8A5A2B',bt='border_straw_top.png',bb='border_straw_bot.png')
def simple_set(SET,title,eyebrow,items,price,size,pill,gtitle,gsub,cols,imh):
    N=len(items)+3
    out=[cover(N,SET,dict(eyebrow=eyebrow,title=title,img=items[0][1],price=price,pill=pill))]
    for k,(nm,img) in enumerate(items):
        out.append(product_slide(N,k+1,SET,dict(name=nm,img=img,price=price,eyebrow=f'{k+1:02d}<span class="ln"></span>{size}')))
    out.append(grid_slide(N,N-2,SET,dict(title=gtitle,sub=gsub,foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
        [dict(short=i[0],img=i[1],price=price) for i in items],cols,imh))
    out.append(order_slide(N,SET,ORDER))
    return out
ws=shawl_set('Small Wooly Shawls',[('Camel','wcamel'),('Mauve','wmauve'),('Grey','wgrey'),('Brown','wbrown'),('Black','wblack')],
   90,'100 × 100 CM','5 COLOURS IN STOCK · R90 EACH','Small wooly shawl · 100 × 100 cm',3,300)
sts=simple_set(STSET,'Straw Hats','HATS · CLASSIC STRAW',[('Cream White','stcream'),('Black','stblack'),('Brown','stbrown'),('White','stwhite')],
   125,'SIZE 58','4 COLOURS IN STOCK · R125 EACH','Pick your colour.','Classic straw hat · size 58',2,300)
pas=simple_set(STSET,'Pacino Felted Hats',"MEN'S HATS · FELTED",[('Black','pablack'),('Brown','pabrown'),('Grey','pagrey'),('Navy','panavy')],
   125,'SIZE 57','4 COLOURS IN STOCK · R125 EACH','Pick your colour.',"Men's felted hat · size 57",2,300)

for name,slides in (('hats',hs),('xhosa',xs),('frill',fs),('elizabeth',es),('plain',ps),('soft',ss),('check',cs),('nblankets',nb),('naccess',na),('ntekkies',nt),('wooly',ws),('straw',sts),('pacino',pas)):
    open(os.path.join(H,f'ig_{name}.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>'+''.join(slides)+'</body></html>')
print(len(hs),len(xs))
