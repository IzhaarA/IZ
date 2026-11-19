"""Three extra TikTok videos to run alongside the Black Friday video (Nov 2026).
  trio-basket  : "What does R1,000 get you?" basket fills up, free gift unlocks
  trio-wedding : December wedding season / umembeso gift list
  trio-beads   : "Pick your colour": oval bead necklace rainbow, then plastic and glass seed beads
Must include (owner's request): Umbhalo, ZCC green beret, plain shawl, white wedding shawl.
Usage: python3 make_trio.py <site public folder>  -> copies photos to img/t_*.jpg, writes trio-*.html (from trio-*.src.html) with sale prices
Then:  node render.cjs trio-<name> full ; ffmpeg (see README) -> ../makkies-<name>-tiktok.mp4"""
import json, math, os, re, sys
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); PUB = sys.argv[1]; PH = os.path.join(H, 'img')
s = open(os.path.join(PUB, 'index.html'), encoding='utf-8').read()
i = s.index('[', s.index('const PRODUCTS')); d = 0
for k in range(i, len(s)):
    d += {'[': 1, ']': -1}.get(s[k], 0)
    if d == 0: break
BY = {p['id']: p for p in json.loads(s[i:k + 1])}
K5 = re.compile(r'^(SHW-002|TRB-005|MNK-003|MNK-005|CHS-001)'); EX = re.compile(r'^(STL-|BEL-003|ZLA-00\d-03)')
def price(pid, vi=0):   # (sale price, old price), worked out the same way as the website (7%, 5% on a few, rounded up)
    v = BY[pid]['variants'][vi]
    if EX.match(v['id']): return v['price'], None
    n = math.ceil(v['price'] * (100 - (5 if K5.match(v['id']) else 7)) / 100 - 1e-9)
    return (n, v['price']) if n < v['price'] else (v['price'], None)
R = lambda x: 'R{:,}'.format(int(round(x)))
def pic(name, pid, vi=0):
    im = Image.open(os.path.join(PUB, BY[pid]['variants'][vi]['img'])).convert('RGB')
    im.save(os.path.join(PH, f't_{name}.jpg'), quality=92); return f't_{name}'
def neck(pid):   # oval necklaces: cut-outs on white from cut_necklaces.py (img/t_n_<id>_c.jpg) if made, else lift the grey card to white
    if os.path.exists(os.path.join(PH, f't_n_{pid.lower()}_c.jpg')): return f't_n_{pid.lower()}_c'
    a = np.asarray(Image.open(os.path.join(PUB, BY[pid]['variants'][0]['img'])).convert('RGB')).astype(float)
    bg = np.median(np.concatenate([a[:25, :25].reshape(-1, 3), a[:25, -25:].reshape(-1, 3)]), axis=0)
    a = np.clip(a * (255 / np.maximum(bg - 6, 1)), 0, 255); a[a.min(-1) > 228] = 255
    Image.fromarray(a.astype('uint8')).save(os.path.join(PH, f't_n_{pid.lower()}.jpg'), quality=92)
    return f't_n_{pid.lower()}'
def vidx(pid, label):   # index of the variant whose label contains `label`
    return next(k for k, v in enumerate(BY[pid]['variants']) if label in v['label'])
def vpic(name, pid, label): return pic(name, pid, vidx(pid, label))
def item(pid, name, sub, photo, mode='cover', pos='50% 50%', vi=0):
    n, w = price(pid, vi); return dict(id=pid, n=name, s=sub, now=R(n), was=R(w) if w else '', v=n, img=photo, mode=mode, pos=pos)

umbhalo = item('TRB-002', 'UMBHALO', 'NDEBELE BLANKET', 'pay_umbhalo')
wedding = item('SHW-011', 'WHITE WEDDING SHAWL', 'FOR THE BRIDE', pic('wedding', 'SHW-011'), pos='50% 35%')
plain = item('PSH-016', 'PLAIN SHAWL', '29 COLOURS', pic('plain_red', 'PSH-016'), pos='50% 35%')
beret = item('BER-008', 'ZCC GREEN BERET', 'LAMBSWOOL BERET', 'bf_beret_c', 'cut')
ziela = item('NZL-001', 'NECK ZIELA', 'BUTTON NECK ZIELA · GOLD', 'bf_ziela_c', 'cut')
GIFTS = [dict(n='10 blanket pins', img=pic('g_pins', 'PIN-001')), dict(n='2 flag whistles', img=pic('g_whistle', 'WHS-001')),
         dict(n='Beaded oval necklace', img=neck('PBN-E29'))]
ORDER = ['PBN-04', 'PBN-E23', 'PBN-E66', 'PBN-E66CL', 'PBN-E17', 'PBN-E68CL', 'PBN-E15', 'PBN-E67CL', 'PBN-E09', 'PBN-13', 'PBN-E77',
         'PBN-E36', 'PBN-E37', 'PBN-05', 'PBN-E29', 'PBN-08', 'PBN-E06', 'PBN-E61', 'PBN-E64', 'PBN-07', 'PBN-E78']   # rainbow order
NECKS = [x for x in ORDER if x in BY and not BY[x]['variants'][0].get('soldOut')]
CFG = {
  'basket': dict(P=[umbhalo, wedding, plain, beret, ziela], G=GIFTS),
  'wedding': dict(P=[
      dict(item('MNK-014', 'PARIS MINK', '2 PLY · IN A GIFT BOX', 'um_mnk-014'), who='For Mama'),
      dict(umbhalo, who='For Baba'),
      dict(wedding, who='For the bride'),
      dict(item('PSH-007', 'PLAIN SHAWLS', '29 COLOURS', pic('plain_pink', 'PSH-007'), pos='50% 35%'), who='For the aunties'),
      dict(beret, who='For church'),
      dict(item('KNG-005', 'KANGAS', 'MANY PRINTS', pic('kanga', 'KNG-005'), 'cut'), who='For everyone'),
      dict(item('TWL-003', 'BATH TOWELS', 'SOFT & THICK', pic('towel', 'TWL-003'), 'cut'), who='For the home')]),
  'beads': dict(N=[dict(id=x, n=BY[x]['name'], img=neck(x)) for x in NECKS], now=R(price('PBN-E29')[0]), was=R(price('PBN-E29')[1]),
                P=[dict(item('CZ-63030', 'CZECH GLASS SEED BEADS', 'PRECIOSA · ¼KG · SIZE 8/0 · 59 COLOURS', 'x', vi=vidx('CZ-63030', '8/0 · ¼kg strung')),
                        imgs=[vpic('cz1', 'CZ-63030', '8/0 · ¼kg strung'), vpic('cz2', 'CZ-33060', '8/0 · ¼kg strung'), vpic('cz3', 'CZ-53250', '8/0 · ¼kg strung')]),
                   dict(item('CH-28', 'CHINESE GLASS SEED BEADS', '450G PACKET · 40+ COLOURS', 'x'),
                        imgs=[pic('ch1', 'CH-42B'), pic('ch2', 'CH-5009'), pic('ch', 'CH-28')]),
                   dict(item('PB6-E23', '6MM PLASTIC BEADS', '250G PACKET · 37 COLOURS', 'x'),
                        imgs=[pic('pb6', 'PB6-E23'), pic('pb6b', 'PB6-E17'), pic('pb6c', 'PB6-E29')])]),
}
for name, c in CFG.items():
    t = open(os.path.join(H, f'trio-{name}.src.html'), encoding='utf-8').read()
    open(os.path.join(H, f'trio-{name}.html'), 'w', encoding='utf-8').write(t.replace('/*CFG*/{}', json.dumps(c, ensure_ascii=False)))
    print(name, [(x.get('n'), x.get('now')) for x in c['P']])
print('basket total', sum(x['v'] for x in CFG['basket']['P']), '| necklaces', len(NECKS))
