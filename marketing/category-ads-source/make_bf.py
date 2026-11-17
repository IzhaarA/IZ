"""Black Friday 2026 TikTok ad from bf-template.html -> bf-sale.html. Render: node render.cjs bf-sale full, then ffmpeg."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
P = [  # name, sub line, was, now, save, photo   (sale prices = website prices during the sale)
 ('SEANNAMARENA', 'BASOTHO BLANKET', 'R1,135', 'R1,056', 'R79', 'bs_trb-011', True),
 ('PARIS MINK', '2 PLY · QUEEN / KING · IN BOX', 'R775', 'R721', 'R54', 'um_mnk-014', True),
 ('KHOTSO', 'BASOTHO BLANKET', 'R625', 'R582', 'R43', 'bf_khotso', True),
 ('UKHAMBA', 'NDEBELE BLANKET', 'R595', 'R554', 'R41', 'pay_ukhamba', True),
 ('UMBHALO', 'NDEBELE BLANKET', 'R595', 'R554', 'R41', 'pay_umbhalo', True),
 ('ELIZABETH', 'BASOTHO BLANKET · 5 COLOURS', 'R305', 'R284', 'R21', 'pay_elizabeth', True),
 ('TRIBAL STRIPE', 'XHOSA BLANKET', 'R300', 'R279', 'R21', 'pay_xhosa_black', True),
 ('BEETEE TEKKIES', 'HAND-PAINTED · UK3 – UK8', 'R250', 'R233', 'R17', 'pay_tekkies', False),
 ('BEADED NECK RING', 'NECK RING & TIE · NDEBELE BEADWORK', 'R350', 'R326', 'R24', 'bf_neckring_c', False),
 ('NECK ZIELA', 'BUTTON NECK ZIELA · GOLD', 'R150', 'R140', 'R10', 'bf_ziela_c', False),
 ('ZCC GREEN BERET', 'LAMBSWOOL BERET', 'R105', 'R98', 'R7', 'bf_beret_c', False),
]
C = dict(H=dict(pill='LIMITED TIME · ENDS 30 NOV', t1='BLACK', t2='FRIDAY', t3='SALE!', sub='Prices cut + <b style="color:#FFE14F">free gift</b> over R1,000',
               fan=['pay_ukhamba', 'bs_trb-011', 'pay_umbhalo']),
         top='BLACK FRIDAY SALE', end='Black Friday Sale',
         P=[dict(n=n, s=s, was=w, pr=p, save=sv, imgs=[im], cover=cv) for n, s, w, p, sv, im, cv in P])
T = open(os.path.join(H, 'bf-template.html')).read()
open(os.path.join(H, 'bf-sale.html'), 'w').write(T.replace('/*CFG*/', json.dumps(C)))
print('ok', len(P))
