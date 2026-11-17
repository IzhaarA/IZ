# Black Friday WhatsApp Status image (1080x1920). python3 black_friday.py && node render_bf.cjs
import os
D = os.path.dirname(os.path.abspath(__file__)); I = '../category-ads-source/img/'
FONTS = open(os.path.join(D, '../homepage-mockups/fonts/fonts.css')).read().replace('url(gf', 'url(../homepage-mockups/fonts/gf')
ITEMS = [('bs_trb-011.jpg', 'Seannamarena', 'R1,135', 'R1,079', '50% 25%'), ('um_mnk-014.jpg', 'Paris Mink', 'R775', 'R737', '50% 50%'),
         ('pay_ukhamba.jpg', 'Ukhamba', 'R595', 'R566', '50% 30%'), ('bf_khotso.jpg', 'Khotso', 'R625', 'R594', '50% 50%')]
tiles = ''.join(f'''<div class="t"><div class="ph" style="background-image:url({I}{f});background-position:{pos}"></div>
<div class="tag"><s>{w}</s><b>{n}</b></div><div class="lb">{l}</div></div>''' for f, l, w, n, pos in ITEMS)
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
@font-face{{font-family:'DM Serif Display';src:url(../category-ads-source/fonts/dmserif.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(circle at 50% 30%,#3a2140 0%,#141117 60%);color:#fff;font-family:Inter,Arial,sans-serif;position:relative}}
.stripe{{height:16px;background:linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96%)}}
.top{{display:flex;align-items:center;justify-content:center;gap:22px;padding:34px 0 0}}.top img{{width:120px}}.top span{{font-size:30px;font-weight:700;letter-spacing:.18em;color:#e9e3dc}}
.lim{{text-align:center;margin-top:30px}}.lim span{{background:#C3312B;font-weight:800;font-size:30px;letter-spacing:.2em;padding:10px 26px;border-radius:40px}}
h1{{text-align:center;font-weight:900;font-size:128px;line-height:.95;letter-spacing:-1px;margin-top:22px}}
h1 em{{font-style:normal;display:inline-block;background:#FFE14F;color:#141117;padding:6px 30px 14px;border-radius:20px;transform:rotate(-2deg);margin-top:12px;font-size:124px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:0 50px;margin-top:38px}}
.t{{position:relative;height:400px;border-radius:24px;overflow:hidden;border:6px solid #fff;box-shadow:0 24px 50px rgba(0,0,0,.5)}}.ph{{position:absolute;inset:0;background-size:cover}}
.tag{{position:absolute;right:14px;top:14px;width:170px;height:170px;border-radius:50%;background:#FFE14F;color:#141117;display:flex;flex-direction:column;align-items:center;justify-content:center;border:6px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.35)}}
.tag s{{font-size:26px;font-weight:700;color:#6b5a00;text-decoration-thickness:3px;text-decoration-color:#C3312B}}.tag b{{font-size:40px;font-weight:900;line-height:1}}
.lb{{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.95);color:#141117;font-weight:800;font-size:30px;padding:8px 16px;border-radius:10px}}
.gift{{margin:34px 50px 0;background:#fff;color:#141117;border-radius:24px;display:flex;align-items:center;gap:26px;padding:26px 34px}}.gift .g{{font-size:96px;line-height:1}}
.gift b{{display:block;font-size:52px;font-weight:900;color:#C3312B;line-height:1.05}}.gift span{{font-size:32px;font-weight:600}}
.more{{text-align:center;font-size:34px;font-weight:600;color:#e9e3dc;margin-top:24px}}
.url{{text-align:center;margin-top:20px}}.url span{{background:#FFE14F;color:#141117;font-weight:900;font-size:76px;padding:16px 56px;border-radius:70px}}
.end{{text-align:center;margin-top:30px;font-size:32px;font-weight:700}}.end em{{font-style:normal;color:#FFE14F}}
.bot{{position:absolute;left:0;right:0;bottom:0}}
</style></head><body><div class="stripe"></div>
<div class="top"><img src="{I}mw_oval.png"><span>MAKKIE WHOLESALERS</span></div>
<div class="lim"><span>LIMITED TIME</span></div>
<h1>BLACK FRIDAY<br><em>SALE!</em></h1>
<div class="grid">{tiles}</div>
<div class="gift"><div class="g">🎁</div><div><b>FREE GIFT</b><span>with every order over R1,000</span></div></div>
<div class="more">Prices cut on almost everything online</div>
<div class="url"><span>makkies.co.za</span></div>
<div class="end">Ends <em>30 November</em> · WhatsApp 072 323 5469</div>
<div class="stripe bot"></div></body></html>"""
open(os.path.join(D, 'black-friday-status.html'), 'w').write(html); print('ok')
