import os
H=os.path.dirname(os.path.abspath(__file__))
FONTS="../../calendar-2027/source/fonts/local.css"
WA="072 323 5469"
def src(img): return img if '.' in img else img+'.png'      # photos from the website are .jpg, older cut-outs .png
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
.grid.sm{gap:12px}.grid.sm .gi{padding-bottom:6px;border-radius:8px}.grid.sm .nm{font-size:15px;margin-top:5px;letter-spacing:0}.grid.sm .pr{font-size:18px}
"""
def product_slide(n,i,set_,p):
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,i,set_['acc'])}
<div class="a eyebrow">{p['eyebrow']}</div><div class="a title" style="font-size:{82 if len(p['name'])<=16 else (66 if len(p['name'])<=22 else 56)}px;top:{120 if len(p['name'])<=16 else 128}px">{p['name']}</div>
<img class="a bt" src="ph/{set_['bt']}"><div class="a photo"><img src="ph/{src(p['img'])}"></div>
<div class="a price"><small>{p.get('pre','ONLY')}</small><b>R{p['price']}</b></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Order at makkies.co.za · WhatsApp {WA}</div></div>'''
def cover(n,set_,c):
    lg=c.get('logo','<img class="a" src="ph/logo.png" style="left:470px;top:62px;width:140px">')
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,0,set_['acc'])}
{lg}
<div class="a eyebrow" style="top:150px">{c['eyebrow']}</div>
<div class="a serif" style="left:0;width:100%;top:190px;text-align:center;font-size:84px;line-height:1">{c['title']}</div>
<img class="a bt" src="ph/{set_['bt']}" style="top:300px">
<div class="a photo" style="top:420px;height:600px;{c.get('pstyle','')}"><img src="ph/{src(c['img'])}"></div>
<div class="a price" style="right:120px;top:380px"><small>{c.get('pre','ONLY')}</small><b>R{c['price']}</b></div>
<div class="a" style="left:0;width:100%;top:1052px;text-align:center"><span class="pill">{c['pill']}</span></div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">Swipe to see every style →</div></div>'''
def grid_slide(n,i,set_,g,items,cols,imh,small=False):
    cells=''.join(f'<div class="gi"><div class="im" style="height:{imh}px;background-image:url(ph/{src(p["img"])})"></div><div class="nm">{p["short"]}</div><div class="pr">{p.get("ptxt","R"+str(p["price"]))}</div></div>' for p in items)
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,i,set_['acc'])}
<div class="a serif" style="left:0;width:100%;top:92px;text-align:center;font-size:78px">{g['title']}</div>
<div class="a" style="left:0;width:100%;top:190px;text-align:center;font-size:28px;font-weight:600;color:#6b625a">{g['sub']}</div>
<img class="a bt" src="ph/{set_['bt']}">
<div class="a grid{' sm' if small else ''}" style="grid-template-columns:repeat({cols},1fr)">{cells}</div>
<img class="a bb" src="ph/{set_['bb']}"><div class="a foot">{g['foot']}</div></div>'''
def order_slide(n,set_,o,logo=None):
    lg=logo or '<img class="a" src="ph/logo.png" style="left:340px;top:350px;width:400px">'
    return f'''<div class="slide" style="--bg:{set_['bg']};--acc:{set_['acc']}">{dots(n,n-1,set_['acc'])}
<img class="a bt" src="ph/{set_['bt']}" style="top:150px">
{lg}
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

# Lamberets (new MW oval for all future ads)
OVAL_COVER='<img class="a" src="ph/mw_oval.png" style="left:483px;top:44px;width:114px">'
OVAL_ORDER='<img class="a" src="ph/mw_oval.png" style="left:400px;top:318px;width:280px">'
lams=[('Bottle Green','lam_bottle-green'),('Maroon','lam_maroon'),('Mustard','lam_mustard'),('Emerald Green','lam_emerald'),
      ('Navy','lam_navy'),('Royal Blue','lam_royal-blue'),('Pink','lam_pink'),('Black','lam_black')]
NL=len(lams)+3
FANSTYLE='box-shadow:none;border-radius:0;height:520px;top:450px'
ls=[cover(NL,HATSET,dict(eyebrow='BERETS · LAMBERETS',title='Lamberet Berets',img='lam_fan',price=195,pill='8 COLOURS · 100% WOOL · R195',logo=OVAL_COVER,pstyle=FANSTYLE))]
for k,(nm,img) in enumerate(lams):
    ls.append(product_slide(NL,k+1,HATSET,dict(name=nm,img=img,price=195,eyebrow=f'{k+1:02d}<span class="ln"></span>12\'\' CROWN · 100% WOOL')))
ls.append(grid_slide(NL,NL-2,HATSET,dict(title='Pick your colour.',sub='Lamberet berets · 100% wool · made in South Africa',foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=195) for x in lams],4,214))
ls.append(order_slide(NL,HATSET,ORDER,logo=OVAL_ORDER))

# Plain Berets (new MW oval, no shelf photo)
pbs=[('Black','pb_black',85,"SIZE 12''"),('Blue','pb_blue',85,"SIZE 12''"),('Cream White','pb_cream-white',85,"SIZE 12''"),('Green','pb_green',85,"SIZE 12''"),('Navy','pb_navy',85,"SIZE 12''"),('Red','pb_red',85,"SIZE 12''"),('Yellow','pb_yellow',85,"SIZE 12''"),('ZCC Green','pb_zcc-green',105,"SIZE 12'' · LAMBSWOOL")]
NP=len(pbs)+3
pls=[cover(NP,HATSET,dict(eyebrow='BERETS · PLAIN',title='Plain Berets',img='plain_fan',price=85,pre='FROM',pill='8 COLOURS · SIZE 12\'\' · FROM R85',logo=OVAL_COVER,pstyle=FANSTYLE))]
for k,(nm,img,pr,ey) in enumerate(pbs):
    pls.append(product_slide(NP,k+1,HATSET,dict(name=nm,img=img,price=pr,eyebrow=f'{k+1:02d}<span class="ln"></span>{ey}')))
pls.append(grid_slide(NP,NP-2,HATSET,dict(title='Pick your colour.',sub="Plain berets · size 12'' · from R85",foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
   [dict(short=x[0],img=x[1],price=x[2]) for x in pbs],4,214))
pls.append(order_slide(NP,HATSET,ORDER,logo=OVAL_ORDER))

# Category ads, Oct 2026 (photos and prices from the website, collected by ../../category-ads-source/collect.py)
import json, re
from PIL import Image
AD=json.load(open(os.path.join(H,'..','..','category-ads-source','ads.json')))
def size(t): return re.sub(r'(\d)X(\d+)CM',r'\1 × \2 CM',t.upper())
def cat_set(SET,key,title,eyebrow,pill,gtitle,gsub,cols,imh,show=None,small=False,eye=lambda it:size(it['size'])):
    items=AD[key]; feat=[items[i] for i in show] if show else items
    fw,fh=Image.open(os.path.join(H,'ph',key+'_fan.png')).size; fan_h=min(560,int(1000*fh/fw))   # fan fits the slide width
    N=len(feat)+3; lo=min(it['price'] for it in items); same=all(it['price']==lo for it in items)
    out=[cover(N,SET,dict(eyebrow=eyebrow,title=title,img=key+'_fan',price=lo,pre='ONLY' if same else 'FROM',pill=pill,logo=OVAL_COVER,pstyle=f'box-shadow:none;border-radius:0;height:{fan_h}px;top:{450+(560-fan_h)//2}px'))]
    for k,it in enumerate(feat):
        out.append(product_slide(N,k+1,SET,dict(name=it['name'],img=it['img']+'.jpg',price=it['price'],pre='FROM' if it.get('multi') else 'ONLY',
            eyebrow=f"{k+1:02d}<span class='ln'></span>{eye(it)}")))
    out.append(grid_slide(N,N-2,SET,dict(title=gtitle,sub=gsub,foot='Wholesale & retail · bulk buyers, ask us for trade pricing'),
        [dict(short=it['name'],img=it['img']+'.jpg',price=it['price'],ptxt=('from ' if it.get('multi') else '')+'R'+str(it['price'])) for it in items],cols,imh,small))
    out.append(order_slide(N,SET,ORDER,logo=OVAL_ORDER))
    return out
WSET=dict(bg='#F6F0E9',acc='#8A5A2B',bt='border_shawl_top.png',bb='border_shawl_bot.png')
cads={
 'beaded-accessories':cat_set(HATSET,'beaded','Beaded Accessories','BEADED · HANDMADE','NECKLACES · NECK RINGS · SETS · FROM R50','Complete the look.',
    'Handmade beaded necklaces, neck rings and sets',5,150,small=True,eye=lambda it:('KIDS SIZE · ' if it['id']=='TRD-010' else '')+(it['size'].upper() or 'HANDMADE')),
 'ndebele-hats':cat_set(HATSET,'hats','Ndebele Painted Hats','HATS · HAND-PAINTED','7 STYLES IN STOCK · FROM R150','Pick your style.','Hand-painted Ndebele hats',4,262,
    eye=lambda it:'SIZE '+it['size'].upper()),
 'cloudsoft-shawls':cat_set(SSET,'cloudsoft','Cloudsoft Shawls','SHAWLS · CLOUDSOFT','7 COLOURS · 130 × 130 CM · R175','Pick your colour.','Cloudsoft shawl · 130 × 130 cm · 100% polyester',4,214,
    eye=lambda it:'130 × 130 CM'),
 'chenille-throws':cat_set(SSET,'chenille','Chenille Throws','SHAWLS · THROWS','14 COLOURS · 130 × 180 CM · R175','Pick your colour.','Plain chenille throw · 130 × 180 cm',5,150,small=True,
    eye=lambda it:'130 × 180 CM'),
 'plain-shawls':cat_set(SSET,'plainsh','Plain Shawls','SHAWLS · PLAIN','29 COLOURS IN STOCK · R95 EACH','29 colours.','Plain shawl · 120 × 120 cm · R95 each',6,92,
    show=[14,9,26,15,20,22,6,12,0,28],small=True,eye=lambda it:'120 × 120 CM'),
 'wool':cat_set(WSET,'wool','Rosebud Wool','KNITTING · DOUBLE KNIT','20 COLOURS · R20 A BALL · 5 FOR R95','20 colours.','100g balls · R20 each or R95 for a packet of 5',5,122,
    show=[1,3,9,5,12,13,18,11],small=True,eye=lambda it:'100G BALL · 5 FOR R95'),
 'towels':cat_set(WSET,'towels','Towels','TOWELS · BATH & GUEST','BATH SHEETS · HAND & GUEST TOWELS · FROM R35','Pick your towel.','Bath sheets, hand towels, guest towels and face cloths',3,240,
    eye=lambda it:{'TWL-001':'10 PER PACK · 30 × 45 OR 37 × 55 CM'}.get(it['id'],size(it['size']))+(' · OR 10 FOR R300' if 'Guest' in it['name'] else '')),
}
for name,slides in cads.items():
    open(os.path.join(H,f'ig_{name}.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>'+''.join(slides)+'</body></html>')

for name,slides in (('hats',hs),('xhosa',xs),('frill',fs),('elizabeth',es),('plain',ps),('soft',ss),('check',cs),('nblankets',nb),('naccess',na),('ntekkies',nt),('wooly',ws),('straw',sts),('pacino',pas),('lamberets',ls),('plainberets',pls)):
    open(os.path.join(H,f'ig_{name}.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>'+''.join(slides)+'</body></html>')
print(len(hs),len(xs))
