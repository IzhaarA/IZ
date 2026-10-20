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

page('beaded-accessories', 'beaded', 'BEADED', 'ACCESSORIES', 'HANDMADE', 'NECKLACES · SETS · FROM R50', 'Shop Beaded Accessories',
     lambda i: ('KIDS SIZE · ' if i['id'] == 'TRD-010' else '') + (i['size'].upper() or 'HANDMADE'), [4, 0, 3, 2, 6, 1, 8],
     gridTitle='Complete the look.', gridSub='NECKLACES · NECK RINGS · SETS')
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
print('ok')
