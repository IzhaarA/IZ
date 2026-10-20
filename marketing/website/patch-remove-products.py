"""Products taken off the site (Oct 2026). Safe to re-run.
Usage: python3 patch-remove-products.py public/index.html"""
import json, sys

REMOVE = {
    "MNK-013": "Beverly 1ply double bed size mink",
}
TEXT = [  # chat assistant wording that depends on the removed products
    ("<b>mink blankets</b> (from R375)", "<b>mink blankets</b> (from R395)"),
]

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
n = len(P)
P = [x for x in P if x["id"] not in REMOVE]
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
for old, new in TEXT: h = h.replace(old, new)
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", n - len(P), "products removed")
