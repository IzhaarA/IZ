"""Makes the price on product cards match the product page everywhere.
Usage: python3 patch-prices.py public/index.html   (safe to re-run)
- recalculates every product's minPrice/maxPrice from its options' real prices
- the site also recalculates them when it loads, so a price edit can never leave a stale card price
- a product page opens on its cheapest option, so "from R40" on the card shows R40 when opened
- corrects prices the chat assistant quotes from memory"""
import json, re, sys

p = sys.argv[1]
h = open(p, encoding="utf-8").read()

def one(old, new, optional=False):
    global h
    n = h.count(old)
    if n == 0 and optional: return
    if n != 1: sys.exit(f"expected 1 match, found {n}: {old[:70]!r}")
    h = h.replace(old, new)

# 1) stored card prices
key = "const PRODUCTS = "
s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
fixed = []
for prod in P:
    pr = [v["price"] for v in prod["variants"] if v.get("price") is not None]
    if pr and (prod.get("minPrice") != min(pr) or prod.get("maxPrice") != max(pr)):
        fixed.append(f'{prod["id"]} {prod["name"]}: R{prod.get("minPrice")} -> R{min(pr)}')
        prod["minPrice"], prod["maxPrice"] = min(pr), max(pr)
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]

# 2) always recalculate on load
RECALC = "PRODUCTS.forEach(p => { const pr = p.variants.map(v => v.price).filter(x => x != null); if (pr.length) { p.minPrice = Math.min(...pr); p.maxPrice = Math.max(...pr); } });   // card prices always match the options\n"
if RECALC not in h:
    one("const tn = u =>", RECALC + "const tn = u =>")

# 3) product page opens on the cheapest option
one("const p = byId[id]; cur = {p, v: p.variants[0], qty: 1, gi: 0}; drawModal();",
    "const p = byId[id]; cur = {p, v: p.variants.reduce((a, x) => x.price < a.price ? x : a), qty: 1, gi: 0}; drawModal();",
    optional="p.variants.reduce((a, x) => x.price < a.price ? x : a)" in h)

# 4) chat assistant
one("<b>Elizabeth Basotho</b> comes in 8 colours at R275", "<b>Elizabeth Basotho</b> comes in 5 colours at R305", optional=True)
one("<b>Metal Church Stick</b> (R100)", "<b>Metal Church Stick</b> (from R100)", optional=True)
one("bracelets and belts (R40–R150)", "bracelets and belts (from R40)", optional=True)

open(p, "w", encoding="utf-8").write(h)
print("patched", p, f"- {len(fixed)} card prices corrected")
for f in fixed: print("  ", f)
