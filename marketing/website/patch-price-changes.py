"""Price changes (option code -> new price). Safe to re-run; add new changes at the bottom.
Usage: python3 patch-price-changes.py public/index.html   (run before patch-prices.py so card prices follow)"""
import json, sys

PRICES = {}
def setp(codes, price):
    for c in codes: PRICES[c] = price

# 19 Oct 2026
setp([f"SHW-012-0{i}" for i in range(1, 7)], 250)                 # Scotch Throw (all colours)
setp([f"SHW-014-0{i}" for i in range(1, 9)], 150)                 # Plaid Throw (all colours)
setp(["TRB-006-02", "TRB-007-02"], 250)                           # Ndebele + Beetee Furpile, 150x160cm
setp([f"MNK-010-0{i}" for i in range(1, 8)], 500)                 # Colourful 1ply in bag (all colours)
setp(["BUD-001-01"], 215)                                         # Boxer Grey by Aranda
setp(["WHS-002-1"], 30)                                           # Plastic Referee Whistles
setp(["BEL-002-1", "BEL-004-1"], 60)                              # Tea bells, small (gold + silver)
setp(["BEL-002-2", "BEL-004-2"], 70)                              # Tea bells, medium
setp(["BEL-002-3", "BEL-004-3"], 90)                              # Tea bells, large
setp(["BAC-004-STD"], 40)                                         # Elastic Fishing Line 0.8mm, 100m

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
seen, changed = set(), []
for prod in P:
    for v in prod["variants"]:
        if v["id"] in PRICES:
            seen.add(v["id"])
            if v["price"] != PRICES[v["id"]]:
                changed.append(f'{prod["name"]} {v["label"]}: R{v["price"]:g} -> R{PRICES[v["id"]]}')
                v["price"] = PRICES[v["id"]]
    pr = [v["price"] for v in prod["variants"]]
    prod["minPrice"], prod["maxPrice"] = min(pr), max(pr)
missing = set(PRICES) - seen
if missing: sys.exit("unknown option codes: " + ", ".join(sorted(missing)))
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", len(changed), "prices changed")
for c in changed: print("  ", c)
