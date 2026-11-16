"""Bangles + haberdashery TikTok ads (Nov 2026) from show-template.html.
Usage: python3 make_show.py <site public folder>   -> copies photos to img/show_*.jpg, writes show-<name>.html
Then: node render.cjs show-<name> full ; ffmpeg ... ../makkies-<name>-tiktok.mp4 (see README)."""
import json, os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); PUB = sys.argv[1]
PH = os.path.join(H, 'img')
def ph(name, f):
    im = Image.open(os.path.join(PUB, 'images', f)).convert('RGB'); im.save(os.path.join(PH, f'show_{name}.jpg'), quality=92); return f'show_{name}'
I = lambda name, f: ph(name, f)
ADS = {
 'bangles': dict(
   H=dict(pill='BANGLES & MATSEKA', t1='COPPER,', t2='BRASS', t3='& SILVER', sub='Shine for every ceremony · from <b style="color:#FFE14F">R10</b>',
          fan=[I('bng_cop', '7985ebc3a34e.jpg'), I('bng_12m', '4b22b41ff7c0.jpg'), I('bng_sl', '7e50c0372313.jpg')]),
   top='BANGLES · MAKKIES', end='Shine for less',
   P=[dict(n='COPPER BANGLES', s='SINGLE R20 · PACK OF 6 R100', pre='ONLY', pr='R20', imgs=['show_bng_cop']),
      dict(n='BRASS BANGLES', s='SINGLE R20 · PACK OF 6 R100', pre='ONLY', pr='R20', imgs=[I('bng_brass', '9b39ac6ce702.jpg')]),
      dict(n='SILVER BANGLES', s='ALUMINIUM · SINGLE OR PACK OF 6', pre='ONLY', pr='R20', imgs=[I('bng_alu', 'df69e52562ba.jpg')]),
      dict(n='MATSEKA 12-PACK', s='STRETCHY · MAROON · SILVER · COPPER', pre='ONLY', pr='R35', imgs=['show_bng_12m', I('bng_12s', '8dec9b719e36.jpg'), I('bng_12c', '42e71acf6d67.jpg')], fan=True),
      dict(n='MATSEKA WIRE', s='LEG RINGS & HAND BANGLES', pre='FROM', pr='R10', imgs=[I('bng_leg', 'fe98fba71b6f.jpg'), I('bng_hand', 'e2b4a78b9984.jpg')], pair=True),
      dict(n='STRETCHY MATSEKA', s='GOLD OR SILVER · SINGLE', pre='ONLY', pr='R15', imgs=[I('bng_sg', '8a4d6508c03c.jpg'), I('bng_ss', '0bde95686b5d.jpg')], pair=True),
      dict(n='SLEEVE HOLDERS', s='GOLD OR SILVER · PER PAIR', pre='ONLY', pr='R25', imgs=['show_bng_sl', I('bng_sls', '718561a80409.jpg')], pair=True)]),
 'beadwork-supplies': dict(
   H=dict(pill='FOR BEADWORK', t1='TWINE,', t2='COTTON', t3='& MORE', sub='Everything for your beadwork · from <b style="color:#FFE14F">R10</b>',
          fan=[I('bw_twine', '31cb78465fc1.jpg'), I('bw_rose', 'ad91495b8319.jpg'), I('bw_cone', '90b4c0279e0a.jpg')]),
   top='BEADWORK SUPPLIES', end='Bead more, spend less',
   P=[dict(n='BEAD TWINE', s='WHITE OR BEIGE · 50G TO 500G', pre='FROM', pr='R12', imgs=[I('bw_tw50', 'd4e20a990189.jpg'), 'show_bw_twine'], pair=True),
      dict(n='ROSE BUD COTTON', s='BEAD HAND COTTON · 200M', pre='ONLY', pr='R15', imgs=['show_bw_rose', I('bw_roseb', '6c03fa14e28c.jpg')], pair=True),
      dict(n='3 PLY BEAD COTTON', s='BLACK OR WHITE', pre='ONLY', pr='R30', imgs=[I('bw_3w', 'f7aa2a4603c6.jpg'), I('bw_3b', 'b8a468d1e03c.jpg')], pair=True),
      dict(n='CROCHET COTTON', s='NO.5 · BIG CONE · BLACK OR WHITE', pre='ONLY', pr='R105', imgs=['show_bw_cone', I('bw_conew', '4043d4b17c27.jpg')], pair=True),
      dict(n='SHIRRING ELASTIC', s='BLACK OR WHITE · 10G OR 30M', pre='FROM', pr='R10', imgs=[I('bw_elb', 'e8fdd3f62195.jpg'), I('bw_elw', '576e6de10787.jpg')], pair=True),
      dict(n='301 COTTON TWINE', s='BEADS COTTON TWINE · 500G', pre='ONLY', pr='R110', imgs=[I('bw_301', '726232288cdf.jpg')])]),
 'sewing-craft': dict(
   H=dict(pill='SEWING & CRAFT', t1='PINS,', t2='NEEDLES', t3='& WOOL', sub='Stock up for less · from <b style="color:#FFE14F">R5</b>',
          fan=[I('sw_wred', '792ab495139a.jpg'), I('sw_gpins', 'c9d249864918.jpg'), I('sw_wblue', '3fc1514951e1.jpg')]),
   top='HABERDASHERY · MAKKIES', end='Stock up & save',
   P=[dict(n='WOOL', s='20 COLOURS', pre='ONLY', pr='R20', imgs=['show_sw_wred', I('sw_wyel', '64a56f347a60.jpg'), 'show_sw_wblue'], fan=True),
      dict(n='SAFETY PINS', s='GOLD OR SILVER · BIG BOXES', pre='ONLY', pr='R90', imgs=['show_sw_gpins', I('sw_spins', '5fe1967f672e.jpg')], pair=True),
      dict(n='PEARL HAT PINS', s='CARD OF 12 · 5 TO 7CM', pre='FROM', pr='R5', imgs=[I('sw_hat', '53103ba8d182.jpg')]),
      dict(n='NEEDLES', s='BEST · ARMY & NAVY · REPAIR SETS', pre='FROM', pr='R10', imgs=[I('sw_n1', '866a59a82c3d.jpg'), I('sw_n2', 'c1aa49b59b50.jpg'), I('sw_n3', '7697d6126a5d.jpg')], fan=True),
      dict(n='BLANKET PINS', s='100 PER PACK · 45 OR 80MM', pre='FROM', pr='R120', imgs=[I('sw_bp', '60153ec0b1df.jpg')]),
      dict(n='CHAIR NAILS', s='GOLD OR SILVER · BOX OF 1000', pre='ONLY', pr='R45', imgs=[I('sw_cg', '9e4cb846571a.jpg'), I('sw_cs', '21c57faa6f02.jpg')], pair=True),
      dict(n='TAPES & HOOKS', s='MEASURING TAPE R10 · CROCHET HOOK R15', pre='FROM', pr='R10', imgs=[I('sw_tape', 'fe990866a387.jpg'), I('sw_hook', 'f4a7881a93d9.jpg')], pair=True)]),
}
# cut-out versions (product on a clean light background, made with rembg: img/show_*_c.jpg); these few cut badly, keep the photo
BAD = {'show_bng_12m', 'show_bng_12s', 'show_bng_12c', 'show_sw_cs', 'show_sw_n1', 'show_sw_n2'}
def cut(n): return n + '_c' if n not in BAD and os.path.exists(os.path.join(PH, n + '_c.jpg')) else n
for c in ADS.values():
    c['H']['fan'] = [cut(n) for n in c['H']['fan']]
    for p in c['P']: p['imgs'] = [cut(n) for n in p['imgs']]
T = open(os.path.join(H, 'show-template.html')).read()
for name, c in ADS.items():
    open(os.path.join(H, f'show-{name}.html'), 'w').write(T.replace('/*CFG*/', json.dumps(c)))
    print(name, len(c['P']), 'products')
