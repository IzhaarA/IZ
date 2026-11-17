"""Black Friday 2026 TikTok ad from bf-template.html -> bf-sale.html. Render: node render.cjs bf-sale full, then ffmpeg."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
P = [  # name, sub line, was, now, save, photo   (sale prices = website prices during the sale)
 ('SEANNAMARENA', 'BASOTHO BLANKET', 'R1,135', 'R1,079', 'R56', 'bs_trb-011', True),
 ('PARIS MINK', '2 PLY · QUEEN / KING · IN BOX', 'R775', 'R737', 'R38', 'um_mnk-014', True),
 ('KHOTSO', 'BASOTHO BLANKET', 'R625', 'R594', 'R31', 'bf_khotso', True),
 ('UKHAMBA', 'NDEBELE BLANKET', 'R595', 'R566', 'R29', 'pay_ukhamba', True),
 ('UMBHALO', 'NDEBELE BLANKET', 'R595', 'R566', 'R29', 'pay_umbhalo', True),
 ('ELIZABETH', 'BASOTHO BLANKET · 5 COLOURS', 'R305', 'R290', 'R15', 'pay_elizabeth', True),
 ('TRIBAL STRIPE', 'XHOSA BLANKET', 'R300', 'R285', 'R15', 'pay_xhosa_black', True),
 ('BEETEE TEKKIES', 'HAND-PAINTED · UK3 – UK8', 'R250', 'R238', 'R12', 'pay_tekkies', False),
]
C = dict(H=dict(pill='LIMITED TIME · ENDS 30 NOV', t1='BLACK', t2='FRIDAY', t3='SALE!', sub='Prices cut + <b style="color:#FFE14F">free gift</b> over R1,000',
               fan=['pay_ukhamba', 'bs_trb-011', 'pay_umbhalo']),
         top='BLACK FRIDAY SALE', end='Black Friday Sale',
         P=[dict(n=n, s=s, was=w, pr=p, save=sv, imgs=[im], cover=cv) for n, s, w, p, sv, im, cv in P])
T = open(os.path.join(H, 'bf-template.html')).read()
open(os.path.join(H, 'bf-sale.html'), 'w').write(T.replace('/*CFG*/', json.dumps(C)))
print('ok', len(P))
