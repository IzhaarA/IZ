"""Writes one TikTok page per category (<name>.html) from ads.json. The animation is in ad.js; render with render.cjs."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); AD = json.load(open(os.path.join(H, 'ads.json')))
CSS = re.search(r'<style>(.*?)</style>', open(os.path.join(H, '..', 'berets-tiktok-source', 'plain.html')).read(), re.S).group(1)
CSS += """.card .circ{background-size:cover;border-radius:34px;border:10px solid #fff;filter:none;box-shadow:0 26px 50px rgba(0,0,0,.35)}
.card .gcell .circ{border-width:5px;border-radius:16px;box-shadow:0 10px 20px rgba(0,0,0,.22)}"""
size = lambda t: re.sub(r'(\d)X(\d+)CM', r'\1 × \2 CM', t.upper())
def page(name, key, title1, title2, tag, hook, shop, sub, fan, per=1, show=None, gridCols=3, cell=280, gridTitle=None, gridSub=''):
    items = AD[key]; lo = min(i['price'] for i in items)
    cols = [dict(name=i['name'], hero=i['img'] + '.jpg', grid=i['img'] + '.jpg', ink=i['ink'], tint=i['tint'], price=i['price'],
                 pre='FROM' if i.get('multi') else 'ONLY', sub=sub(i)) for i in items]
    cfg = dict(tag=tag, title1=title1, title2=title2, price=lo, sub='', gridSub=gridSub, shopLine=shop, features=None, card=True,
               fan=[items[i]['img'] + '.jpg' for i in fan], cols=cols, hookSub=hook, per=per, show=show, gridCols=gridCols, cell=cell, gridTitle=gridTitle)
    open(os.path.join(H, name + '.html'), 'w').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/local.css"><style>'
        + CSS + '</style></head><body><script>window.CFG=' + json.dumps(cfg, ensure_ascii=False) + ';</script><script src="ad.js"></script></body></html>')

page('ndebele-hats', 'hats', 'NDEBELE', 'HATS', 'HAND-PAINTED', '7 STYLES · FROM R150', 'Shop Ndebele Hats',
     lambda i: 'HAND-PAINTED · SIZE ' + i['size'].upper(), [0, 1, 2, 3, 4, 5, 6], gridTitle='Pick your style.', gridSub='HAND-PAINTED · FROM R150')
page('cloudsoft-shawls', 'cloudsoft', 'CLOUDSOFT', 'SHAWLS', 'IN STOCK', '7 COLOURS · R175', 'Shop Cloudsoft Shawls',
     lambda i: '130 × 130 CM · 100% POLYESTER', [0, 1, 2, 3, 4, 5, 6], gridSub='R175 EACH · 130 × 130 CM')
page('chenille-throws', 'chenille', 'CHENILLE', 'THROWS', 'IN STOCK', '14 COLOURS · R175', 'Shop Chenille Throws',
     lambda i: '130 × 180 CM · CHENILLE', [0, 2, 4, 6, 8, 10, 12], per=.8, gridCols=4, cell=200, gridSub='R175 EACH · 130 × 180 CM')
page('plain-shawls', 'plainsh', 'PLAIN', 'SHAWLS', 'IN STOCK', '29 COLOURS · R95', 'Shop Plain Shawls',
     lambda i: '120 × 120 CM · R95 EACH', [14, 1, 22, 26, 20, 7, 15], per=.8, show=[14, 9, 26, 15, 20, 22, 6, 12, 0, 28], gridCols=6, cell=140, gridSub='R95 EACH · 120 × 120 CM')
page('wool', 'wool', 'ROSEBUD', 'WOOL', 'DOUBLE KNIT', '20 COLOURS · R20 A BALL', 'Shop Rosebud Wool',
     lambda i: '100G BALL · 5 FOR R95', [1, 3, 9, 5, 12, 18, 11], per=.8, show=[1, 3, 9, 5, 12, 13, 18, 11, 0, 7], gridCols=5, cell=170, gridSub='R20 A BALL · 5 FOR R95')
page('towels', 'towels', 'TOWELS', 'IN STOCK', 'BATH & GUEST', 'FROM R35', 'Shop Towels',
     lambda i: {'TWL-001': '10 PER PACK · 2 SIZES'}.get(i['id'], size(i['size'])) + (' · OR 10 FOR R300' if 'Guest' in i['name'] else ''),
     [3, 2, 1, 4, 5], per=1.1, gridTitle='Pick your towel.', gridSub='BATH · HAND · GUEST · FACE')

# Version 2 (bolder Ndebele look, ~2.4s per product): ad2.js
CSS2 = """@font-face{font-family:'DMSerif';src:url(fonts/dmserif.woff2) format('woff2')}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#1b181d;font-family:Montserrat,sans-serif;color:#fff;position:relative}
.sc{position:absolute;inset:0;opacity:0}.a{position:absolute}.ctr{left:0;width:100%;text-align:center}.serif{font-family:'DMSerif',serif;font-weight:400}
.big{font-weight:900;font-size:150px;line-height:1;letter-spacing:1px}
.chip{display:inline-block;font-weight:800;letter-spacing:6px;font-size:38px;padding:14px 34px;border-radius:60px}
.hl{display:inline-block;font-weight:900;font-size:150px;line-height:1.05;padding:4px 30px;color:#fff;
  background:linear-gradient(#D8232A,#D8232A) no-repeat left/0% 100%;border-radius:12px}
.sticker{width:260px;height:260px;border-radius:50%;background:#D8232A;color:#fff;border:8px solid #fff;display:flex;flex-direction:column;
  align-items:center;justify-content:center;box-shadow:0 18px 36px rgba(216,35,42,.35)}
.sticker small{font-size:34px;font-weight:900;letter-spacing:4px}.sticker b{font-size:92px;font-weight:900;line-height:1}
.frame{background:#fff;padding:18px;border-radius:10px;box-shadow:0 34px 70px rgba(27,24,29,.28),0 6px 16px rgba(27,24,29,.12)}
.fin{width:100%;height:100%;overflow:hidden;border-radius:4px}.ph{width:100%;height:100%;background-size:cover;background-position:center}
.pill{display:inline-block;background:#fff;color:#1b181d;border-radius:80px;font-weight:800}
.stripes{left:0;width:100%;background:linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96% 100%)}
#bars i{flex:1;background:rgba(27,24,29,.12);border-radius:5px;overflow:hidden}#bars b{display:block;height:100%;width:0;background:#1b181d}
#sdots i{display:inline-block;width:52px;height:52px;border-radius:50%;margin:0 16px;border:5px solid #fff;box-shadow:0 6px 14px rgba(0,0,0,.25)}
.gcell{background:#fff;padding:10px 10px 12px;border-radius:10px;box-shadow:0 14px 30px rgba(27,24,29,.18);text-align:center;color:#1b181d}
.gph{background-size:cover;background-position:center;border-radius:4px}
.gnm{font-weight:900;font-size:26px;letter-spacing:1px;margin-top:10px}.gpr{font-weight:900;font-size:34px;color:#D8232A}"""
def page2(name, cfg):
    open(os.path.join(H, name + '.html'), 'w').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/local.css"><style>'
        + CSS2 + '</style></head><body><script>window.CFG=' + json.dumps(cfg, ensure_ascii=False) + ';</script><script src="ad2.js"></script></body></html>')

B = {i['img']: i for i in AD['beaded']}; ba = AD['beaded']; J = lambda i: i['img'] + '.jpg'
DOT = {'Black & White': '#1b181d', 'Yellow & Blue': '#FFC814', 'Green': '#05B56D', 'Orange': '#F07A1A', 'Blue': '#0350EA'}
page2('beaded-accessories', dict(
    tag='HANDMADE', title1='BEADED', title2='ACCESSORIES', hookSub='NECKLACES · NECK RINGS · SETS', lowest=min(i['price'] for i in ba), shopLine='Shop Beaded Accessories',
    hookPhotos=[J(ba[1]), J(ba[3]), J(ba[6])],
    items=[dict(name='Small', chip='KIDS SIZE', sub='BEADED NECKLACE · 5CM OF BEADS', img=J(ba[0]), price=ba[0]['price']),
           dict(name='Medium', chip='10CM OF BEADS', sub='BEADED NECKLACE', img=J(ba[1]), price=ba[1]['price']),
           dict(name='Large', chip='20CM OF BEADS', sub='BEADED NECKLACE', img=J(ba[2]), price=ba[2]['price']),
           dict(name='Neck Ring & Tie', chip='HANDMADE', sub='BEADED NECK RING WITH TIE', img=J(ba[3]), price=ba[3]['price'])],
    set=dict(kicker='NECKLACE + BANGLE', title='The matching set', price=ba[4]['price'],
             cols=[dict(name=i['name'], img=J(i), dot=DOT[i['name']]) for i in ba[4:]]),
    gridTitle='Complete the look.', gridSub='9 PIECES · FROM R50', gridCols=3, cell=280,
    grid=[dict(name=n, img=J(i), price=i['price']) for n, i in zip(['SMALL', 'MEDIUM', 'LARGE', 'NECK RING', 'BLACK & WHITE SET', 'YELLOW & BLUE SET', 'GREEN SET', 'ORANGE SET', 'BLUE SET'], ba)]))
print('ok')
