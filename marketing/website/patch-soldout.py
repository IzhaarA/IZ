"""Sold-out products for makkies.co.za.
Usage: python3 patch-soldout.py public/index.html   (safe to re-run; it rewrites the sold-out list each time)

Edit SOLD_OUT below. A product code (e.g. CH-5009) marks every colour/size of that product sold out;
an option code (e.g. CH-5009-02) marks only that option. Find codes on the product page ("Code ...")."""
import sys

SOLD_OUT = [
    "CH-5009",       # Cerise Pink, Chinese Glass Seed Beads (all sizes)
    "CH-44-8/0",     # Opaque Light Green 44, size 8/0
    "CH-5003-6/0",   # Pearly White 5003, size 6/0
    "CH-5004-8/0",   # Cream Pearl 5004, size 8/0
]

p = sys.argv[1]
h = open(p, encoding="utf-8").read()

def one(old, new, count=1):
    global h
    n = h.count(old)
    if n != count: sys.exit(f"expected {count} match(es), found {n}: {old[:80]!r}")
    h = h.replace(old, new)

LIST = "const SOLD_OUT = " + repr(SOLD_OUT).replace("'", '"') + ";   // sold-out product or option codes (see patch-soldout.py)\n"
if "const SOLD_OUT = " in h:
    s = h.index("const SOLD_OUT = "); e = h.index("\n", s) + 1
    h = h[:s] + LIST + h[e:]
    open(p, "w", encoding="utf-8").write(h); print("updated sold-out list", p, SOLD_OUT); sys.exit(0)

# 1) the list, applied before card prices are worked out (prices come from options still in stock)
INIT = LIST + ("PRODUCTS.forEach(p => { p.variants.forEach(v => { v.soldOut = SOLD_OUT.includes(p.id) || SOLD_OUT.includes(v.id); }); "
               "p.soldOut = p.variants.every(v => v.soldOut); });\n")
one("PRODUCTS.forEach(p => { const pr = p.variants.map(v => v.price).filter(x => x != null);",
    INIT + "PRODUCTS.forEach(p => { const av = p.variants.filter(v => !v.soldOut), pr = (av.length ? av : p.variants).map(v => v.price).filter(x => x != null);")

# 2) cards: grey photo + "Sold out" label (shop grid and home-page featured cards)
one("""<article class="card" onclick="openProduct('${p.id}')\"""",
    """<article class="card${p.soldOut ? ' soldout' : ''}" onclick="openProduct('${p.id}')\"""", 2)
one("""<div class="ph ${fitContain(p) ? 'bead' : ''}">""",
    """<div class="ph ${fitContain(p) ? 'bead' : ''}">${p.soldOut ? '<span class="sold">Sold out</span>' : ''}""", 2)

# 3) sold-out products go to the end of every list
one("  return list;\n}\nfunction renderGrid", "  return list.filter(p => !p.soldOut).concat(list.filter(p => p.soldOut));\n}\nfunction renderGrid")

# 4) product page: open on the cheapest option in stock; grey out sold-out options; WhatsApp instead of Add to basket
one("cur = {p, v: p.variants.reduce((a, x) => x.price < a.price ? x : a), qty: 1, gi: 0};",
    "cur = {p, v: (p.variants.filter(x => !x.soldOut).length ? p.variants.filter(x => !x.soldOut) : p.variants).reduce((a, x) => x.price < a.price ? x : a), qty: 1, gi: 0};")
one("""<button class="var ${x === v ? 'on' : ''}" onclick=""", """<button class="var ${x === v ? 'on' : ''}${x.soldOut ? ' so' : ''}" onclick=""")
one("""alt="">` : ''}${esc(x.label)}</button>`).join('')}""",
    """alt="">` : ''}${esc(x.label)}${x.soldOut ? '<small>sold out</small>' : ''}</button>`).join('')}""")
one("""<div class="bigprice num">${R(v.price)}</div>""",
    """<div class="bigprice num${v.soldOut ? ' so' : ''}">${R(v.price)}${v.soldOut ? '<span class="soldtag">Sold out</span>' : ''}</div>""")
s = h.index("""      <div class="row"><div class="qty"><button onclick="cur.qty=Math.max(1,cur.qty-1)""")
e = h.index("""Add to basket</button></div>""", s) + len("""Add to basket</button></div>""")
buy = h[s:e]
h = h[:s] + ("""      ${v.soldOut ? `<div class="soldbox"><b>${p.soldOut ? 'This product is sold out' : 'This option is sold out'}</b><span>${p.soldOut ? 'We’re waiting on new stock.' : 'Choose another option above, or ask us when it’s back.'}</span>"""
             """<a class="btn" href="https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent('Hi, please let me know when ' + fullName(p) + (!p.soldOut && p.variants.length > 1 ? ' (' + v.label + ')' : '') + ' is back in stock. ' + productURL(p.id))}" target="_blank" rel="noopener">WhatsApp us when it’s back</a></div>` : `"""
             + buy.strip() + "`}") + h[e:]

# 5) never let a sold-out option into the basket (also clears it from baskets saved earlier)
one("function addToCart(id, qty) {",
    "function addToCart(id, qty) { const so = PRODUCTS.some(p => p.variants.some(v => v.id === id && v.soldOut)); if (so) { toast('Sorry, that’s sold out'); return; }")
one("buildNav(); renderCart(); renderGrid();",
    "{ const n = state.cart.length; state.cart = state.cart.filter(l => !PRODUCTS.some(p => p.variants.some(v => v.id === l.id && v.soldOut))); if (state.cart.length < n) { save(); setTimeout(() => toast('Something in your basket has sold out and was removed'), 800); } }\n"
    "buildNav(); renderCart(); renderGrid();")

# 6) styles
CSS = """<style id="soldout-style">
.card.soldout .ph img{opacity:.5}
.card.soldout .tag{display:none}
.card.soldout .price b{color:var(--muted)}
.card .sold{position:absolute;right:10px;top:10px;z-index:2;background:var(--ink);color:#fff;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 9px;border-radius:4px}
.var.so{color:var(--muted);background:#F4F2EE;border-style:dashed}
.var.so img{filter:grayscale(1);opacity:.6}
.var small{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--scarlet);margin-left:2px}
.bigprice.so{color:var(--muted);display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.soldtag{font-family:'Source Sans 3',system-ui,sans-serif;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:#fff;padding:5px 10px;border-radius:5px}
.soldbox{margin-top:12px;padding:14px 16px;border:1px solid var(--line);border-radius:10px;background:var(--bg);display:flex;flex-direction:column;gap:4px}
.soldbox b{color:var(--ink);font-size:15.5px}
.soldbox span{font-size:14px;color:var(--muted)}
.soldbox .btn{margin-top:10px;align-self:flex-start;background:#1F7A3A;color:#fff;text-decoration:none}
</style>
"""
h = h.replace("</head>", CSS + "</head>", 1)

open(p, "w", encoding="utf-8").write(h)
print("patched", p, SOLD_OUT)
