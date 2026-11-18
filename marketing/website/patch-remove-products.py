"""Products taken off the site (Oct 2026). Safe to re-run.
Usage: python3 patch-remove-products.py public/index.html"""
import json, sys

REMOVE = {
    "MNK-013": "Beverly 1ply double bed size mink",
    "CZ-98190": "Opaque Dark Red Coral Sfinx (Czech beads, removed 9 Nov 2026)",
}
# TEMPORARILY OFF THE SITE (18 Nov 2026, owner's request): Cloudsoft Shawl "G" (GSH-) and Plain Chenille Throw "C" (CSH-).
# To bring them back: empty this list and upload.
HIDE_PREFIXES = ["GSH-", "CSH-"]
TEXT = [  # chat assistant wording that depends on the removed products
    ("<b>mink blankets</b> (from R375)", "<b>mink blankets</b> (from R395)"),
]

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
n = len(P)
P = [x for x in P if x["id"] not in REMOVE and not x["id"].startswith(tuple(HIDE_PREFIXES))]
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
for old, new in TEXT: h = h.replace(old, new)
if "CSH-" in HIDE_PREFIXES:   # chat assistant: point winter questions at the Aranda Chenille instead of the hidden plain chenille
    for old, new in [("<b>chenille throws</b>, <b>overcoats</b>", "<b>Aranda chenille throws</b>, <b>overcoats</b>"),
                     ("['MNK-002', 'CSH-001', 'OVC-001', 'PMS-001'], ['Mink Blankets', 'Chenille Throws', 'Overcoats'",
                      "['MNK-002', 'SHW-008', 'OVC-001', 'PMS-001'], ['Mink Blankets', 'Shawls & Throws', 'Overcoats'")]:
        h = h.replace(old, new)
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", n - len(P), "products removed")
