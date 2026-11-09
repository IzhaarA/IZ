# Big first-post "welcome" ad for the WhatsApp groups, 1080x1920 (no prices). Run: python3 welcome.py && node render.cjs
import os
D = os.path.dirname(os.path.abspath(__file__))
I = '../category-ads-source/img/'
FONTS = open(os.path.join(D, '../homepage-mockups/fonts/fonts.css')).read().replace('url(gf', 'url(../homepage-mockups/fonts/gf')
BIG = [('bs_trb-011.jpg', 'Seannamarena', '50% 25%'), ('pay_ukhamba.jpg', 'Ukhamba', '50% 30%')]
SMALL = [('pay_czech2.jpg', 'Czech Beads'), ('hat_ndh-002.jpg', 'Ndebele Hats'), ('nd_nzl-001.jpg', 'Neck Ziela'), ('pay_wedding_shawl.jpg', 'Wedding Shawls'), ('pay_umbhalo.jpg', 'Umbhalo'),
         ('xh_rug-001.jpg', 'Xhosa Rugs'), ('kg_kng-008.jpg', 'Kangas'), ('ba_trd-011.jpg', 'Beadwork'), ('um_mnk-014.jpg', 'Mink Blankets'), ('pay_tekkies.jpg', 'Beetee Painted Tekkies')]
ic = lambda p: f'<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFE14F" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
TRUCK = ic('<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>')
CARD = ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/>')
SHOP = ic('<path d="M4 10v10h16V10M3 6l2-3h14l2 3v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0z"/>')
WA = '<svg width="46" height="46" viewBox="0 0 24 24" fill="#25D366"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>'
CSS = """*{margin:0;padding:0;box-sizing:border-box}@font-face{font-family:'DM Serif Display';src:url(../category-ads-source/fonts/dmserif.woff2)}
body{width:1080px;height:1920px;background:#1b1714;color:#F6F0E6;font-family:Inter,Arial,sans-serif;overflow:hidden}
.stripe{height:16px;background:linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96%)}
.top{display:flex;align-items:center;gap:26px;padding:34px 48px 30px}.top img{width:150px}
.top b{display:block;font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:58px;line-height:1}.top span{display:block;font-size:24px;letter-spacing:.2em;text-transform:uppercase;color:#FFE14F;margin-top:10px;font-weight:600}
.mos{display:grid;grid-template-columns:repeat(20,1fr);grid-template-rows:470px 240px 240px;gap:8px;padding:0 8px}
.ph{position:relative;background-size:cover;background-position:center;border-radius:6px}.ph{grid-column:span 4}.ph.big{grid-column:span 10}
.lb{position:absolute;left:10px;bottom:10px;max-width:calc(100% - 20px);line-height:1.2;background:rgba(255,255,255,.95);color:#1d1b19;font-size:20px;font-weight:600;padding:6px 11px;border-radius:7px;box-shadow:0 2px 10px rgba(0,0,0,.25)}
.big .lb{font-size:26px;left:18px;bottom:18px;padding:9px 16px}
.more{text-align:center;font-family:'DM Serif Display',Georgia,serif;font-style:italic;font-size:44px;color:#FFE14F;padding:18px 0 0}.txt{padding:22px 52px 0}
.eb{display:inline-block;background:#FFE14F;color:#1b1714;font-weight:800;font-size:24px;letter-spacing:.14em;text-transform:uppercase;padding:9px 16px;border-radius:6px}
h1{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:88px;line-height:1.02;letter-spacing:-.5px;margin-top:18px;text-wrap:balance}
h1 em{font-style:normal;color:#FFE14F}
p.sub{font-size:29px;line-height:1.42;color:#d9cfc2;margin-top:16px;max-width:960px}
.pts{display:flex;justify-content:space-between;padding:26px 52px 0;font-size:24px;color:#d9cfc2}.pts div{display:flex;align-items:center;gap:12px}.pts b{color:#fff;font-weight:600}
.shop{position:absolute;left:52px;right:52px;bottom:150px;background:#fff;color:#1b1714;border-radius:16px;display:flex;align-items:center;justify-content:center;text-align:center;padding:22px 34px}
.shop small{display:block;font-size:24px;font-weight:600;color:#C3312B;letter-spacing:.08em;text-transform:uppercase}.shop b{display:block;font-size:66px;font-weight:800;letter-spacing:-1px;line-height:1.05}
.shop .go{background:#1b1714;color:#fff;font-size:28px;font-weight:700;border-radius:12px;padding:20px 26px;white-space:nowrap}
.cta{position:absolute;left:52px;right:52px;bottom:52px;display:flex;align-items:center;justify-content:center;gap:16px;font-size:30px;color:#d9cfc2}.cta b{color:#fff;font-size:34px}
.bot{position:absolute;left:0;right:0;bottom:0}"""
big = ''.join(f'<div class="ph big" style="background-image:url({I}{f});background-position:{pos}"><span class="lb">{l}</span></div>' for f, l, pos in BIG)
small = ''.join(f'<div class="ph" style="background-image:url({I}{f})"><span class="lb">{l}</span></div>' for f, l in SMALL)
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body><div class="stripe"></div>
<div class="top"><img src="{I}mw_oval.png"><div><b>Makkie Wholesalers</b><span>Blankets · Beads · Traditional Goods</span></div></div>
<div class="mos">{big}{small}</div><div class="more">...and much more!</div>
<div class="txt"><span class="eb">New · Shop online 24/7</span><h1>You can now <em>shop online!</em></h1>
<p class="sub">Browse our blankets, beads and traditional goods on your phone, order any time and pay by card, Instant EFT or SnapScan.</p></div>
<div class="pts"><div>{TRUCK}<b>Delivery across SA</b></div><div>{CARD}<b>Safe online payment</b></div><div>{SHOP}<b>Or visit our shop</b></div></div>
<div class="shop"><div><small>Shop online at</small><b>makkies.co.za</b></div></div>
<div class="cta">{WA}<span>Questions? WhatsApp <b>072 323 5469</b></span></div>
<div class="bot stripe"></div></body></html>"""
open(os.path.join(D, '00-welcome.html'), 'w').write(html)
print('ok')
