"""Shawl & throw photos: show the FRONT photo first and use it as the thumbnail (was the back).
Usage: python3 patch-shawlphotos.py public/index.html   (safe to re-run)
Applies to every product in "Shawls & Throws" that has the two own photos (back, front)."""
import json, sys

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "
s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
n = 0
for prod in P:
    if not prod["category"].startswith("Shawls & Throws"): continue
    for v in prod["variants"]:
        g = v.get("gallery") or []
        img = v.get("img") or ""
        done = img == g[0] or img.endswith("-sq.jpg") or img.endswith("-sqz.jpg") if g else True   # already front-first
        if len(g) == 2 and not done:      # still back-first: img is the back copy, g = [back, front]
            old = v["img"]
            v["gallery"] = [g[1], g[0]]                # front, then back
            v["img"] = g[1]                            # thumbnail = front
            if prod.get("img") == old: prod["img"] = g[1]
            n += 1
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", n, "shawl/throw options now front-first")
