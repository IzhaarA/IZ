# Black Friday sale (Nov 2026): prices cut ~5% for everyone (no code), old price crossed out + "Save Rxx",
# free gift on orders of R1,000 or more (after sale prices, before delivery). Switches itself off after SALE.end.
# Items already priced the same online as in the shop are left out, so nothing drops below shop retail.
# Usage: python3 patch-promo.py public/index.html   (run after patch-nav.py / patch-track.py)
import sys, re, json
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'const SALE =' in s:
    print('promo already patched'); sys.exit()

SALE = {
    'name': 'BLACK FRIDAY SALE',
    'pct': 5,                                  # never shown to customers; sale prices are rounded UP to whole rands
    'end': '2026-12-01T00:00:00+02:00',        # off from 1 December, SA time
    'gift': 1000,                              # free gift threshold (rand)
    'giftName': 'a free gift',
    # same online as in the shop (Nov 2026 price list): steeltrunks, brass bells, 100m ziela
    'exclude': r'^(STL-|BEL-003|ZLA-00\d-03)',
}

def sub(old, new, count=1):
    global s
    n = s.count(old)
    if n < count: raise SystemExit(f'pattern not found ({n}/{count}): {old[:70]}')
    s = s.replace(old, new)

JS = r'''
/* ---------- Black Friday sale ---------- */
const SALE = %s;
const SALE_ON = Date.now() < Date.parse(SALE.end);
if (SALE_ON) {
  const ex = new RegExp(SALE.exclude);
  PRODUCTS.forEach(p => {
    p.variants.forEach(v => { if (v.price == null || ex.test(v.id)) return; const n = Math.ceil(v.price * (100 - SALE.pct) / 100 - 1e-9); if (n < v.price) { v.was = v.price; v.price = n; } });
    const av = p.variants.filter(v => !v.soldOut), vs = av.length ? av : p.variants, lo = vs.reduce((a, v) => v.price < a.price ? v : a, vs[0]);
    p.minPrice = Math.min(...vs.map(v => v.price)); p.maxPrice = Math.max(...vs.map(v => v.price)); p.wasMin = lo.was || null; p.saveMin = lo.was ? lo.was - lo.price : 0;
  });
}
const PP = p => (p.wasMin && SALE_ON ? `<s class="was">${R(p.wasMin)}</s> ` : '') + (p.minPrice === p.maxPrice ? '' : 'from ') + R(p.minPrice) + (p.wasMin && SALE_ON ? `<span class="save">Save ${R(p.saveMin)}</span>` : '');
function saleRows(ls, sub) {
  if (!SALE_ON || !ls.length) return '';
  const saved = ls.reduce((a, l) => a + (l.v.was ? (l.v.was - l.v.price) * l.qty : 0), 0);
  const left = SALE.gift - sub;
  return (saved ? `<div class="salerow"><span>Black Friday savings</span><b class="num">\u2212${R(saved)}</b></div>` : '')
    + (left <= 0 ? `<div class="giftrow ok">\ud83c\udf81 Your order gets ${SALE.giftName}!</div>`
                 : `<div class="giftrow">\ud83c\udf81 Add ${R(left)} more to get ${SALE.giftName}<i><b style="width:${Math.round(sub / SALE.gift * 100)}%%"></b></i></div>`);
}
''' % json.dumps(SALE)
sub("const tn = u =>", JS + "const tn = u =>")

# prices on product cards, home page, search suggestions
sub("${p.minPrice === p.maxPrice ? R(p.minPrice) : 'from ' + R(p.minPrice)}", "${PP(p)}", 3)
# product pop-up
sub("${R(v.price)}${v.soldOut ? '<span class=\"soldtag\">Sold out</span>' : ''}",
    "${v.was && SALE_ON ? `<s class=\"was\">${R(v.was)}</s> ` : ''}${R(v.price)}${v.was && SALE_ON ? `<span class=\"save big\">You save ${R(v.was - v.price)}</span>` : ''}${v.soldOut ? '<span class=\"soldtag\">Sold out</span>' : ''}")
# basket lines
sub("${esc(vdetail(l.p, l.v))} · ${R(l.v.price)}", "${esc(vdetail(l.p, l.v))} · ${l.v.was && SALE_ON ? `<s class=\"was\">${R(l.v.was)}</s> ` : ''}${R(l.v.price)}")
# basket totals + checkout totals
sub("`<div><span>Subtotal</span><b class=\"num\">${R(sub)}</b></div><div><span>Delivery</span><b class=\"num\">${(s =>",
    "`<div><span>Subtotal</span><b class=\"num\">${R(sub)}</b></div>${saleRows(ls, sub)}<div><span>Delivery</span><b class=\"num\">${(s =>")
sub("`<div><span>Subtotal</span><b class=\"num\">${R(sub)}</b></div>${disc ?",
    "`<div><span>Subtotal</span><b class=\"num\">${R(sub)}</b></div>${saleRows(ls, sub)}${disc ?")
# order message to the shop: remind to pack the gift
sub("\\nSubtotal ${R(o.sub)}", "\\nSubtotal ${R(o.sub)}${SALE_ON && o.sub >= SALE.gift ? '\\n\\ud83c\\udf81 FREE GIFT: yes (Black Friday, order over R' + SALE.gift + ')' : ''}")

BANNER = '''<div class="salebar" id="salebar"><b>BLACK FRIDAY SALE</b><span>Prices cut on almost everything</span><span>\U0001F381 Free gift with orders over R1,000</span><em>Ends 30 November</em></div>
<script>if(Date.now()>=Date.parse("%s"))document.getElementById('salebar').remove()</script>''' % SALE['end']
sub('<body>\n<header class="top">', '<body>\n' + BANNER + '<header class="top">')

CSS = '''
/* ---------- Black Friday sale ---------- */
.salebar{background:#141117;color:#fff;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:4px 18px;padding:9px 14px;font-size:14px;text-align:center}
.salebar b{background:#FFE14F;color:#141117;padding:3px 10px;border-radius:4px;letter-spacing:.06em}.salebar em{font-style:normal;color:#FFE14F;font-weight:700}
s.was{color:#8a837c;font-weight:400;text-decoration-thickness:1.5px;margin-right:2px;font-size:.88em}
.save{display:inline-block;background:#C3312B;color:#fff;font-size:12px;font-weight:700;border-radius:4px;padding:2px 7px;margin-left:6px;vertical-align:middle;letter-spacing:.02em;white-space:nowrap}
.save.big{font-size:14px;padding:4px 10px;margin-left:10px;font-family:var(--body)}
.bigprice s.was{font-size:.6em}
.salerow span,.salerow b{color:#C3312B!important;font-weight:700}
.giftrow{background:#FFF7D6;border:1px solid #F2D36B;border-radius:8px;padding:9px 12px;margin:8px 0;font-size:14px;font-weight:600;color:#5a4500}
.giftrow.ok{background:#E4F2E9;border-color:#9fd0b1;color:#0A5A33}
.giftrow i{display:block;height:5px;background:#f1e3a8;border-radius:4px;margin-top:6px;overflow:hidden}.giftrow i b{display:block;height:100%;background:#C3312B;border-radius:4px}
@media(max-width:700px){.salebar{font-size:12.5px;gap:2px 10px;padding:7px 10px}.salebar span:nth-of-type(1){display:none}}
'''
s = re.sub(r"(</style>\s*</head>)", CSS.replace('\\', '\\\\') + r"\1", s, count=1)
open(P, 'w', encoding='utf-8').write(s)
print('sale patched, ends', SALE['end'])
