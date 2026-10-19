"""Chenille throw codes and colour names (Oct 2026). Safe to re-run.
Usage: python3 patch-chenille.py public/index.html"""
import json, re, sys

CODES = {"CSH-012": "C3", "CSH-014": "C5", "CSH-015": "C14", "CSH-013": "C15"}          # Ivory, Yellow, Purple, Red
NAMES = {"CSH-004": "Terracotta", "CSH-007": "Maroon", "CSH-008": "Charcoal Blue",
         "CSH-009": "Hunter Green", "CSH-010": "Navy Blue"}                              # C7, C10, C13, C16, C17
REMOVE = {"CSH-003"}                                                                     # Honey (C5) is no longer made

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
P = [x for x in P if x["id"] not in REMOVE]
for x in P:
    if x["id"] in CODES: x["code"] = CODES[x["id"]]
    if x["id"] in NAMES:
        x["name"] = NAMES[x["id"]]
        for v in x["variants"]: v["label"] = NAMES[x["id"]]
# chenille throws in code order (C1, C3, C4 ...), in the same place in the list
idx = [i for i, x in enumerate(P) if x["category"] == "Shawls & Throws · Chenille Throws"]
ch = sorted((P[i] for i in idx), key=lambda x: int(re.sub(r"\D", "", x.get("code") or "999") or 999))
for i, x in zip(idx, ch): P[i] = x
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", " ".join(f'{x.get("code")} {x["name"]}' for x in ch))
