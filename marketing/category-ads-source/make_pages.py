"""Writes one TikTok page per category (<name>.html) from ads.json. The animation is in ad2.js; render with render.cjs.
Each page has its own look (palette, border, opening layout, how the photos come in, sticker shape) so the videos differ."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); AD = json.load(open(os.path.join(H, 'ads.json')))

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
.sticker.tag{width:290px;height:200px;border-radius:28px}
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
IGCSS = """body{width:1080px;height:auto;overflow:visible;background:#777;color:#1b181d}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;color:#1b181d}.pat{inset:0;opacity:.05}
.cdots{top:22px;display:flex;justify-content:center;gap:9px}.cdots i{width:10px;height:10px;border-radius:50%;background:#1b181d;opacity:.22}.cdots i.on{opacity:1}
.foot{bottom:30px;font-size:24px;font-weight:600;letter-spacing:1px;color:#6b625a}"""
def page2(name, cfg):
    """Writes the TikTok page <name>.html and the Instagram carousel page <name>-ig.html from the same settings."""
    open(os.path.join(H, name + '-ig.html'), 'w').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/local.css"><style>'
        + CSS2 + IGCSS + '</style></head><body><script>window.CFG=' + json.dumps(cfg, ensure_ascii=False) + ';</script><script src="carousel.js"></script></body></html>')
    open(os.path.join(H, name + '.html'), 'w').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/local.css"><style>'
        + CSS2 + '</style></head><body><script>window.CFG=' + json.dumps(cfg, ensure_ascii=False) + ';</script><script src="ad2.js"></script></body></html>')

ba = AD['beaded']; J = lambda i: i['img'] + '.jpg'
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

def items(key, idx, chip, sub, name=lambda i: i['name']):
    return [dict(name=name(AD[key][n]), chip=chip(AD[key][n]), sub=sub(AD[key][n]), img=J(AD[key][n]), price=AD[key][n]['price']) for n in idx]
def grid(key, short=lambda i: i['name'].upper(), ptxt=None):
    return [dict(name=short(i), img=J(i), price=i['price'], **({'ptxt': ptxt} if ptxt else {})) for i in AD[key]]
low = lambda key: min(i['price'] for i in AD[key])

hats = AD['hats']; HN = ['White Cap', 'Beige', 'Black', 'Brown', 'White', "Women's Hat", 'Brown Pattern']
page2('ndebele-hats', dict(
    tag='HAND-PAINTED', title1='NDEBELE', title2='HATS', hookSub='7 STYLES · SIZE 58', lowest=low('hats'), shopLine='Shop Ndebele Hats',
    hookPhotos=[J(hats[n]) for n in (1, 6, 0, 3)],
    items=[dict(name=HN[n], chip='PAINTED CAP' if n == 0 else 'PAINTED HAT', sub='HAND-PAINTED · SIZE ' + hats[n]['size'].upper(), img=J(hats[n]), price=hats[n]['price']) for n in range(7)],
    gridTitle='Pick your style.', gridSub='HAND-PAINTED · FROM R150', gridCols=4, cell=215, grid=[dict(name=HN[n].upper(), img=J(h), price=h['price']) for n, h in enumerate(hats)],
    look=dict(band='ndebele', hook='mosaic', enter='up', sticker='tag', hl='#0350EA', tilt=12,
              pal=[{'bg': '#F4E9DA', 'acc': '#B5562B'}, {'bg': '#EAEFE4', 'acc': '#4E7A3A'}, {'bg': '#F3E4E1', 'acc': '#A33A3A'}, {'bg': '#E6EAF0', 'acc': '#2F4E8A'}])))

page2('cloudsoft-shawls', dict(
    tag='SOFT AS A CLOUD', title1='CLOUDSOFT', title2='SHAWLS', hookSub='7 COLOURS · 130 × 130 CM', lowest=low('cloudsoft'), shopLine='Shop Cloudsoft Shawls', hookPre='ONLY',
    hookPhotos=[J(AD['cloudsoft'][3])],
    items=items('cloudsoft', range(7), lambda i: '130 × 130 CM', lambda i: 'CLOUDSOFT SHAWL · 100% POLYESTER'),
    gridTitle='7 colours.', gridSub='R175 EACH · 130 × 130 CM', gridCols=4, cell=215, grid=grid('cloudsoft'),
    look=dict(band='shawl', hook='hero', enter='zoom', sticker='circle', hl='#2F6FD6', tilt=-10,
              pal=[{'bg': '#E8EEF8', 'acc': '#2F6FD6'}, {'bg': '#EFEAF6', 'acc': '#6C4FA3'}, {'bg': '#E6F2F1', 'acc': '#1F8A84'}, {'bg': '#F6ECEE', 'acc': '#C04A64'}])))

page2('chenille-throws', dict(
    tag='WARM & SOFT', title1='CHENILLE', title2='THROWS', hookSub='14 COLOURS · 130 × 180 CM', lowest=low('chenille'), shopLine='Shop Chenille Throws', hookPre='ONLY',
    hookPhotos=[J(AD['chenille'][n]) for n in (6, 2, 12)],
    items=items('chenille', (0, 1, 2, 4, 6, 7, 9, 11), lambda i: '130 × 180 CM', lambda i: 'PLAIN CHENILLE THROW'),
    citems=items('chenille', range(14), lambda i: '130 × 180 CM', lambda i: 'PLAIN CHENILLE THROW'),
    gridTitle='14 colours.', gridSub='R175 EACH · 130 × 180 CM', gridCols=5, cell=170, grid=grid('chenille'),
    look=dict(band='shawl', hook='fan', enter='left', sticker='tag', hl='#8A3B2B', tilt=16,
              pal=[{'bg': '#F5E8DE', 'acc': '#A24A2A'}, {'bg': '#F2E6EA', 'acc': '#8A2F4A'}, {'bg': '#F4EEDD', 'acc': '#9A7414'}, {'bg': '#E9E7F1', 'acc': '#4B4790'}])))

page2('plain-shawls', dict(
    tag='ONE PRICE', title1='PLAIN', title2='SHAWLS', hookSub='29 COLOURS · ALL R95', lowest=low('plainsh'), shopLine='Shop Plain Shawls', hookPre='ONLY',
    hookPhotos=[J(AD['plainsh'][n]) for n in (14, 22, 26, 20)],
    items=items('plainsh', (14, 9, 26, 15, 20, 22, 6), lambda i: '120 × 120 CM', lambda i: 'PLAIN SHAWL · 29 COLOURS'),
    citems=items('plainsh', (14, 9, 26, 15, 20, 22, 6, 12, 0, 28), lambda i: '120 × 120 CM', lambda i: 'PLAIN SHAWL · 29 COLOURS'),
    gridTitle='29 colours.', gridSub='ALL R95 · 120 × 120 CM', gridCols=6, cell=150, grid=grid('plainsh'),
    look=dict(band='shawl', hook='mosaic', enter='right', sticker='circle', hl='#D8232A', tilt=-18,
              pal=[{'bg': '#E3F1E9', 'acc': '#0E8A55'}, {'bg': '#ECECEC', 'acc': '#1b181d'}, {'bg': '#E4EAF8', 'acc': '#2347C4'}, {'bg': '#F8E4E4', 'acc': '#D02A2A'},
                   {'bg': '#FAF2D6', 'acc': '#B88A00'}, {'bg': '#F6E3EF', 'acc': '#B0277A'}, {'bg': '#F5E8E8', 'acc': '#B0607A'}])))

page2('wool', dict(
    tag='DOUBLE KNIT', title1='ROSEBUD', title2='WOOL', hookSub='20 COLOURS · 100G BALLS', lowest=low('wool'), shopLine='Shop Rosebud Wool',
    hookPhotos=[J(AD['wool'][13])],
    items=items('wool', (1, 3, 9, 5, 12, 13, 18, 11), lambda i: '100G BALL', lambda i: 'OR R95 FOR A PACKET OF 5'),
    gridTitle='20 colours.', gridSub='R20 A BALL · 5 FOR R95', gridCols=5, cell=165, grid=grid('wool'),
    look=dict(band='straw', hook='hero', enter='up', sticker='tag', hl='#7A3FA0', tilt=10,
              pal=[{'bg': '#F7E5E5', 'acc': '#C2312F'}, {'bg': '#E7F2E2', 'acc': '#3F9A2E'}, {'bg': '#E5EAF7', 'acc': '#2850C8'}, {'bg': '#FAF3D8', 'acc': '#C79A00'},
                   {'bg': '#FBEADF', 'acc': '#D9641E'}, {'bg': '#F6E2F0', 'acc': '#B21E7D'}, {'bg': '#EEE4F4', 'acc': '#6B2FA0'}, {'bg': '#ECECEC', 'acc': '#1b181d'}])))

tw = AD['towels']
page2('towels', dict(
    tag='BATH & GUEST', title1='FRESH', title2='TOWELS', hookSub='BATH · HAND · GUEST · FACE', lowest=low('towels'), shopLine='Shop Towels',
    hookPhotos=[J(tw[n]) for n in (3, 1, 2)],
    items=[dict(name='Bath Sheet', chip='90 × 150 CM', sub='BRISTOL WHITE BATH SHEET', img=J(tw[1]), price=tw[1]['price']),
           dict(name='Hand Towel', chip='50 × 90 CM', sub='BLOCK HAND TOWEL', img=J(tw[2]), price=tw[2]['price']),
           dict(name='Face Cloths', chip='10 PER PACK', sub='30 × 45 CM R60 · 37 × 55 CM R70', img=J(tw[0]), price=tw[0]['price'], pre='FROM')],
    set=dict(kicker='COLIBRI GUEST TOWELS', title='Pick a colour', price=tw[3]['price'], sub='30 × 50 CM · R35 EACH OR 10 FOR R300',
             cols=[dict(name=i['name'].split('· ')[-1], img=J(i), dot=d) for i, d in zip(tw[3:], ('#3A5BA8', '#B4502C', '#B05A78'))]),
    gridTitle='Pick your towel.', gridSub='FROM R35', gridCols=3, cell=270,
    grid=[dict(name=n, img=J(tw[k]), price=tw[k]['price'], ptxt=p) for n, k, p in (('BATH SHEET', 1, 'R150'), ('HAND TOWEL', 2, 'R75'), ('FACE CLOTHS', 0, 'from R60'),
          ('GUEST · BLUE', 3, 'R35'), ('GUEST · RUST', 4, 'R35'), ('GUEST · ROSE', 5, 'R35'))],
    look=dict(band='straw', hook='fan', enter='zoom', sticker='circle', hl='#0E7C86', tilt=-12,
              pal=[{'bg': '#E4F2F3', 'acc': '#0E7C86'}, {'bg': '#F4EEE4', 'acc': '#9A6A2E'}, {'bg': '#EAF0F6', 'acc': '#3A5BA8'}, {'bg': '#F5E9EC', 'acc': '#B05A78'}])))
print('ok')
