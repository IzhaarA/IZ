# WhatsApp group photo ads, 1080x1350 (no prices). Run: python3 make.py && node render.cjs
import os
D = os.path.dirname(os.path.abspath(__file__))
IMG = '../category-ads-source/img/'
FONTS = open(os.path.join(D, '../homepage-mockups/fonts/fonts.css')).read().replace('url(gf', 'url(../homepage-mockups/fonts/gf')
ADS = [
 ('01-basotho-blankets', 'grid', [('bs_trb-011','Seannamarena'), ('bs_trb-012','Victoria'), ('bs_trb-026','Moshoeshoe')], 'Basotho Blankets', 'Wrapped in tradition',
  'Seannamarena, Victoria, Moshoeshoe and many more designs for weddings, umembeso and every ceremony.'),
 ('02-ndebele-blankets', 'grid', [('pay_ukhamba','Ukhamba'), ('pay_umbhalo','Umbhalo'), ('@ndebele_furpile','Ndebele Furpile')], 'Ndebele Blankets', 'Bold colours, proud heritage',
  'Ukhamba, Umbhalo, Ndebele Furpile and more, in stock now.'),
 ('03-wedding-umembeso', 'quad', [('pay_wedding_shawl','White Wedding Shawl'), ('pay_ziela_gold','Neck Ziela'), ('pay_xhosa_black','Black Stripe Blanket'), ('um_mnk-014','Paris Mink Blanket')], 'Umembeso & Weddings', 'Everything for the big day',
  'Blankets, shawls, neck ziela and gifts for the in-laws, all from one shop.'),
 ('04-czech-beads', 'six', [('pay_czech1','Dark Orange'), ('pay_czech2','Royal Blue'), ('cz_cz-83130','Yellow'), ('pay_czech3','Bright Green'), ('cz_cz-63030','Turquoise'), ('cz_cz-37175','Ceylon Pink')], 'Preciosa Czech Beads', 'Every colour you need',
  'Loose and strung Czech beads for beadwork, crafters and schools. Ask us for a colour list.'),
 ('05-xhosa-blankets', 'grid', [('xh_rug-001','Tivolli Rug'), ('pay_xhosa_black','Black Stripe'), ('xh_stripe_02','Purple Stripe')], 'Xhosa Blankets', 'Classic stripes, made to last',
  'Tribal stripe blankets and traditional rugs in a range of colours.'),
 ('06-ndebele-accessories', 'quad', [('nd_nzl-001','Button Neck Ziela'), ('hat_ndh-002','Ndebele Painted Hat'), ('pay_tekkies','Beetee Painted Tekkies'), ('ba_trd-011','Beaded Necklace')], 'Ndebele Accessories', 'Finish the look',
  'Neck ziela, Ndebele hats, hand-painted tekkies and beaded accessories.'),
 ('07-we-deliver', 'hero', [('bs_trb-024','Mohodu Basotho Blanket')], 'Order from anywhere', 'We deliver across South Africa',
  'Order on WhatsApp or at makkies.co.za. Pay by card, Instant EFT or SnapScan. Courier to your door or PAXI at any PEP.'),
]
def src(n):
    if n.startswith('@'): return 'img/' + n[1:] + '.jpg'
    for ext in ('.jpg', '.png'):
        if os.path.exists(os.path.join(D, IMG + n + ext)): return IMG + n + ext
    raise SystemExit('missing ' + n)
def photos(kind, ims):
    def b(it, cls='', pos='center'):
        n, label = it
        return f'<div class="ph {cls}" style="background-image:url({src(n)});background-position:{pos}"><span class="lb">{label}</span></div>'
    if kind == 'hero': return f'<div class="pics hero">{b(ims[0], pos="50% 40%")}</div>'
    if kind == 'grid': return f'<div class="pics grid">{b(ims[0], "big", "50% 30%")}{b(ims[1])}{b(ims[2])}</div>'
    if kind == 'six': return '<div class="pics six">' + ''.join(b(n) for n in ims) + '</div>'
    return '<div class="pics quad">' + ''.join(b(n) for n in ims) + '</div>'
WA = '<svg width="34" height="34" viewBox="0 0 24 24" fill="#25D366"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>'
CSS = """*{margin:0;padding:0;box-sizing:border-box}@font-face{font-family:'DM Serif Display';src:url(../category-ads-source/fonts/dmserif.woff2)}
body{width:1080px;height:1350px;font-family:Inter,Arial,sans-serif;background:#F6F0E6;color:#1d1b19;overflow:hidden}
.pics{height:880px;display:grid;gap:8px;background:#F6F0E6}.ph{background-size:cover;background-repeat:no-repeat;position:relative}.lb{position:absolute;left:16px;bottom:16px;background:rgba(255,255,255,.94);color:#1d1b19;font-size:25px;font-weight:600;padding:9px 16px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.18);line-height:1.15}.six .lb{font-size:22px;left:12px;bottom:12px;padding:8px 13px}.hero .lb{left:24px;bottom:24px;font-size:28px}
.grid{grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr}.grid .big{grid-row:1/3}.quad{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}.hero .ph{height:880px}.six{grid-template-columns:1fr 1fr 1fr;grid-template-rows:1fr 1fr}
.stripe{height:14px;background:linear-gradient(90deg,#45203F 0 12%,#FFE14F 12% 30%,#0350EA 30% 46%,#FF0141 46% 62%,#05B56D 62% 74%,#FF0141 74% 84%,#FFE14F 84% 96%,#45203F 96%)}
.panel{height:456px;padding:40px 56px 0;position:relative}
.logo{position:absolute;right:52px;top:36px;width:150px}
.eb{font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C3312B}
h1{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:68px;line-height:1.04;margin:12px 0 16px;max-width:770px;text-wrap:balance}
p{font-size:28px;line-height:1.4;color:#4a443e;max-width:770px;text-wrap:pretty}
.foot{position:absolute;left:56px;right:56px;bottom:34px;display:flex;align-items:center;gap:14px;font-size:27px;font-weight:600;border-top:2px solid #e2d9cc;padding-top:22px}
.foot .sep{color:#b9b0a5;font-weight:400}"""
for name, kind, ims, eb, h1, p in ADS:
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body>{photos(kind, ims)}<div class="stripe"></div>
<div class="panel"><img class="logo" src="{IMG}mw_oval.png"><div class="eb">{eb}</div><h1>{h1}</h1><p>{p}</p>
<div class="foot">{WA}<span>072 323 5469</span><span class="sep">|</span><span>makkies.co.za</span><span class="sep">|</span><span>Marabastad, Pretoria</span></div></div></body></html>"""
    open(os.path.join(D, name + '.html'), 'w').write(html)
print(len(ADS), 'ads')
