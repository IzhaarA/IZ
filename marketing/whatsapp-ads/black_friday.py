# Black Friday WhatsApp Status image (1080x1920), same products and look as the TikTok video (bf2.html).
# python3 black_friday.py && node render_bf.cjs
import os
D = os.path.dirname(os.path.abspath(__file__)); I = '../category-ads-source/img/'
FONTS = open(os.path.join(D, '../homepage-mockups/fonts/fonts.css')).read().replace('url(gf', 'url(../homepage-mockups/fonts/gf')
ITEMS = [('Seannamarena', 'Basotho blanket', 'R1,135', 'R1,056', 'R79', 'bs_trb-011', '50% 25%'),
 ('Paris Mink', '2 ply · in box', 'R775', 'R721', 'R54', 'um_mnk-014', '50% 55%'),
 ('Khotso', 'Basotho blanket', 'R625', 'R582', 'R43', 'bf_khotso', '50% 50%'),
 ('Ukhamba', 'Ndebele blanket', 'R595', 'R554', 'R41', 'pay_ukhamba', '50% 30%'),
 ('Umbhalo', 'Ndebele blanket', 'R595', 'R554', 'R41', 'pay_umbhalo', '50% 50%'),
 ('Elizabeth', 'Basotho blanket', 'R305', 'R284', 'R21', 'pay_elizabeth', '50% 50%'),
 ('Tribal Stripe', 'Xhosa blanket', 'R300', 'R279', 'R21', 'pay_xhosa_black', '50% 50%'),
 ('Beaded Neck Ring', 'Ndebele beadwork', 'R350', 'R326', 'R24', 'bf_neckring_c', '50% 50%'),
 ('Neck Ziela', 'Button · gold', 'R150', 'R140', 'R10', 'bf_ziela_c', '50% 50%'),
 ('ZCC Green Beret', 'Lambswool', 'R105', 'R98', 'R7', 'bf_beret_c', '50% 50%')]
cards = ''.join(f'''<div class="c"><div class="ph" style="background-image:url({I}{im}.jpg);background-position:{pos}"></div>
<div class="tx"><b>{n}</b><small>{s}</small><div class="pr"><s>{w}</s><em>{now}</em></div><span class="sv">SAVE {sv}</span></div></div>''' for n, s, w, now, sv, im, pos in ITEMS)
tape = 'BLACK FRIDAY ★ SALE ★ ' * 6
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1920px;overflow:hidden;background:#0b0b0c;color:#fff;font-family:Archivo,Arial,sans-serif;position:relative}}
.cond{{font-family:Oswald,Impact,sans-serif;text-transform:uppercase}}
.tape{{position:absolute;left:-200px;width:1500px;height:86px;display:flex;align-items:center;white-space:nowrap;overflow:hidden;font-family:Oswald,Impact,sans-serif;font-weight:700;font-size:46px;letter-spacing:5px}}
.ty{{background:#FFE14F;color:#0b0b0c;top:28px;transform:rotate(-3deg)}}.tr{{background:#E1251B;color:#fff;bottom:24px;transform:rotate(2deg)}}
.hd{{position:absolute;top:150px;left:0;right:0;text-align:center}}
.hd .lg{{display:flex;align-items:center;justify-content:center;gap:16px;font-weight:700;font-size:26px;letter-spacing:.2em;color:#cfc9c2}}.hd img{{width:84px}}
.hd h1{{font-family:Oswald,Impact,sans-serif;font-weight:700;font-size:112px;white-space:nowrap;line-height:1;margin-top:10px;letter-spacing:-1px}}
.hd h1 span{{background:#FFE14F;color:#0b0b0c;padding:0 22px 4px;border-radius:10px;display:inline-block;transform:rotate(-2deg)}}
.hd p{{font-weight:700;font-size:30px;margin-top:10px;color:#FFE14F;letter-spacing:.06em}}
.grid{{position:absolute;top:470px;left:40px;right:40px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.c{{display:flex;height:206px;background:#1b1a1c;border-radius:18px;overflow:hidden;position:relative;border:2px solid #2c2a2e}}
.ph{{width:190px;flex:none;background-size:cover;background-color:#F4EFE8}}
.tx{{padding:16px 16px 0 18px;min-width:0}}.tx b{{display:block;font-family:Oswald,Impact,sans-serif;font-size:33px;font-weight:700;text-transform:uppercase;line-height:1.05;white-space:nowrap}}
.tx small{{display:block;font-size:20px;color:#a9a39c;margin-top:2px}}
.pr{{margin-top:8px;white-space:nowrap}}.pr s{{font-size:24px;font-weight:700;color:#a9a39c;text-decoration-color:#E1251B;text-decoration-thickness:4px}}
.pr em{{display:inline-block;font-style:normal;background:#FFE14F;color:#0b0b0c;font-weight:900;font-size:40px;padding:0 10px 3px;border-radius:8px;margin-left:6px}}
.sv{{position:absolute;right:12px;bottom:12px;background:#E1251B;font-weight:800;font-size:20px;letter-spacing:.06em;padding:5px 10px;border-radius:6px}}
.ft{{position:absolute;top:1590px;left:40px;right:40px;display:flex;align-items:center;gap:20px;background:#FFE14F;color:#0b0b0c;border-radius:20px;padding:16px 26px}}
.ft .g{{font-size:76px;line-height:1}}.ft b{{display:block;font-family:Oswald,Impact,sans-serif;font-size:50px;text-transform:uppercase;line-height:1}}.ft span{{font-size:26px;font-weight:700}}
.ft .u{{margin-left:auto;text-align:right}}.ft .u b{{font-family:Archivo,Arial,sans-serif;font-weight:900;font-size:46px;text-transform:none;letter-spacing:-1px}}
.end{{position:absolute;top:1740px;left:0;right:0;text-align:center;font-weight:700;font-size:28px;color:#cfc9c2}}
</style></head><body>
<div class="tape ty">{tape}</div>
<div class="hd"><div class="lg"><img src="{I}mw_oval.png">MAKKIE WHOLESALERS</div><h1>BLACK FRIDAY <span>SALE</span></h1><p>LIMITED TIME · ENDS 30 NOVEMBER</p></div>
<div class="grid">{cards}</div>
<div class="ft"><div class="g">🎁</div><div><b>Free gift</b><span>with orders over R1,000</span></div><div class="u"><b>makkies.co.za</b><span>WhatsApp 072 323 5469</span></div></div>
<div class="end">Prices cut on almost everything online · Delivery across SA</div>
<div class="tape tr">{'SAVE NOW ★ FREE GIFT OVER R1,000 ★ ' * 4}</div>
</body></html>"""
open(os.path.join(D, 'black-friday-status.html'), 'w').write(html); print('ok')
