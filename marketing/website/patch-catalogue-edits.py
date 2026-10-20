"""Catalogue edits (20 Oct 2026): split products, renames, sizes, photo order. Safe to re-run.
Usage: python3 patch-catalogue-edits.py public/index.html"""
import json, sys

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
by = {x["id"]: x for x in P}

def split(pid, parts):
    """One product per option. parts = [(new product id, name suffix, size or None)] in option order.
    The option codes stay the same, so baskets saved earlier keep working."""
    if pid not in by or len(by[pid]["variants"]) == 1: return
    src = by[pid]; base = src["name"]; at = P.index(src)
    new = []
    for v, (nid, suffix, size) in zip(src["variants"], parts):
        x = {k: val for k, val in src.items() if k != "variants"}
        x["id"] = nid; x["name"] = f"{base} — {suffix}"
        if size is not None: x["size"] = size
        v = dict(v); v["label"] = "Standard"
        x["variants"] = [v]; x["img"] = v["img"]; x["minPrice"] = x["maxPrice"] = v["price"]
        new.append(x)
    P[at:at + 1] = new
    for x in new: by[x["id"]] = x

split("HNK-002", [("HNK-002", "Plain White", None), ("HNK-003", "Light Checks", None), ("HNK-004", "Dark Checks", None)])
split("BNG-004", [("BNG-004", "Gold", None), ("BNG-005", "Silver", None)])
split("SKA-001", [("SKA-001", "15cm", "15cm"), ("SKA-004", "20cm", "20cm")])
split("BEL-001", [("BEL-001", "Gold", None), ("BEL-005", "Silver", None)])
# Colibri guest towel: one product per design, each sold single or as a 10 pack
if "TWL-004" in by and "TWL-005" not in by:
    src = by["TWL-004"]; at = P.index(src); photos = src["variants"][0].get("gallery") or [src["img"]]
    towels = []
    for n, (pid, colour) in enumerate([("TWL-004", "Blue"), ("TWL-005", "Rust"), ("TWL-006", "Rose")]):
        x = {k: val for k, val in src.items() if k not in ("variants", "desc")}
        x["id"] = pid; x["name"] = f"Colibri Guest Towel — {colour}"; x["img"] = photos[n]
        x["variants"] = [{"id": f"{pid}-01", "label": "Single towel", "price": 35, "img": photos[n]},
                         {"id": f"{pid}-02", "label": "Pack of 10", "price": 300, "img": photos[n]}]
        towels.append(x)
    P[at:at + 1] = towels
    for x in towels: by[x["id"]] = x
# Copper, brass and aluminium bangles: single R20 or pack of 6 R100
for pid in ("BNG-001", "BNG-002", "BNG-003"):
    x = by[pid]; img = x["img"]
    x["variants"] = [{"id": f"{pid}-1", "label": "Single bangle", "price": 20, "img": img},
                     {"id": f"{pid}-STD", "label": "Pack of 6", "price": 100, "img": img}]   # pack keeps its old code
    x["unit"] = "unit"; x["desc"] = "sold single or in a pack of 6"
for i in ("BNG-004", "BNG-005"): by[i]["desc"] = "sold per pair"
for i in ("BEL-001", "BEL-005"): by[i]["desc"] = "jingle bells"

def setp(pid, **kw):
    for k, val in kw.items(): by[pid][k] = val

for v in by["TEK-004"]["variants"]: v["price"] = 60                    # White Ladies Canvas Tekkies
setp("WIR-004", name="711 Copper Wire")
if "TRD-016" in by:                                                     # Ndebele painted axe colour names
    for v in by["TRD-016"]["variants"]:
        v["label"] = {"Stripes": "Ndebele Stripe", "Red": "Black & Red"}.get(v["label"], v["label"])
for pid, sz, d in (("TRD-010", "5cm of beads", "Kids size."), ("TRD-011", "10cm of beads", None), ("TRD-012", "20cm of beads", None)):
    if pid in by: setp(pid, size=sz, **({"desc": d} if d else {}))      # beaded necklaces: depth of the beadwork
if "TRD-015" in by: setp("TRD-015", size="65cm & 35cm", desc="2-piece set: one 65cm belt and one 35cm belt.")
setp("WHS-001", name="Plastic 2 Pipe Ndebele Whistle", desc="2-pipe plastic whistle")
setp("WHS-006", size="9cm")                                            # 3 Pipe Metal Whistle
setp("WHS-005", size="12cm")                                           # 2 Pipe Metal Whistle
SIZES = {"BEL-002": ["10cm", "12cm", "20cm"], "BEL-004": ["10cm", "12cm", "20cm"], "BEL-003": ["12cm", "24cm", "26cm"]}
for pid, sz in SIZES.items():
    for v, s_ in zip(by[pid]["variants"], sz):
        v["label"] = v["label"].split(" · ")[0] + " · " + s_            # Small · 10cm
for x in P:                                                            # wool: drop the shared second photo
    if x["category"] == "Haberdashery · Wool":
        for v in x["variants"]:
            if v.get("gallery") and len(v["gallery"]) > 1: v["gallery"] = v["gallery"][:1]
setp("COT-007", size="1.5mm · 100g")                                   # Kite/Khozo cord
FIRST = {"BAC-003": "images/6c659f89f09a.jpg", "BAC-004": "images/4a50565238fe.jpg", "BAC-005": "images/57635af1a30d.jpg"}
for pid, first in FIRST.items():                                       # fishing lines: the (old) second photo goes first
    for v in by[pid]["variants"]:
        g = v.get("gallery") or []
        if first in g: v["gallery"] = [first] + [x for x in g if x != first]; v["img"] = first
    by[pid]["img"] = by[pid]["variants"][0]["img"]
setp("PIN-009", size="3mm & 4mm", desc="Double-ended: 3.0mm hook on one end, 4.0mm on the other.")
for x in P:                                                            # Berets: every beret except the lamberets -> "Plain Berets"
    if x["category"] == "Berets": x["category"] = "Berets · Plain Berets"
ids = [x["id"] for x in P]                                             # ZCC green beret first among the plain berets
if ids.index("BER-008") > ids.index("BER-001"):
    P.insert(ids.index("BER-001"), P.pop(ids.index("BER-008")))
MATSEKA = ["TRD-021", "TRD-022", "TRD-024", "TRD-025", "TRD-026", "TRD-027", "TRD-028", "TRD-029", "TRD-030"]   # matseka leg rings and bangles -> Bangles
for pid in [m for m in MATSEKA if m in by and by[m]["category"] != "Bangles"]:
    by[pid]["category"] = "Bangles"; P.remove(by[pid])
    last = max(i for i, x in enumerate(P) if x["category"] == "Bangles"); P.insert(last + 1, by[pid])
for pid in [d for d in ("TRD-005", "TRD-006", "TRD-007", "TRD-008") if d in by and by[d]["category"] != "Dimit Coins"]:
    by[pid].update(category="Dimit Coins", group="Beads"); P.remove(by[pid])   # dimit coins: own category under Beads
    last = max(i for i, x in enumerate(P) if x["group"] == "Beads"); P.insert(last + 1, by[pid])
for pid in [b for b in ("TRD-009", "TRD-010", "TRD-011", "TRD-012", "TRD-023", "TRD-031")   # beaded items -> Beads · Beaded Accessories
            if b in by and by[b]["category"] != "Beaded Accessories"]:
    by[pid].update(category="Beaded Accessories", group="Beads"); P.remove(by[pid])
    last = max(i for i, x in enumerate(P) if x["group"] == "Beads"); P.insert(last + 1, by[pid])
ska = by["SKA-003"]                                                    # painted and plain wooden axes -> Scissors, Knives & Axes
for pid in [a for a in ("TRD-016", "TRD-020") if a in by and by[a]["category"] != ska["category"]]:
    by[pid].update(category=ska["category"], group=ska["group"]); P.remove(by[pid])
    last = max(i for i, x in enumerate(P) if x["category"] == ska["category"]); P.insert(last + 1, by[pid])
for pid in [b for b in ("TRD-032", "TRD-033") if b in by and by[b]["category"] != "Haberdashery · Brooches"]:   # brooches
    by[pid].update(category="Haberdashery · Brooches", group="Haberdashery & General Goods"); P.remove(by[pid])
    last = max(i for i, x in enumerate(P) if x["category"].startswith("Haberdashery · ")); P.insert(last + 1, by[pid])
for pid in [b for b in ("TRD-001", "TRD-002", "TRD-004") if b in by and by[b]["category"] != "Shells"]:   # leopard & cowrie shells -> Beads · Shells
    by[pid].update(category="Shells", group="Beads"); P.remove(by[pid])
    last = max(i for i, x in enumerate(P) if x["group"] == "Beads"); P.insert(last + 1, by[pid])
for x in P:
    pr = [v["price"] for v in x["variants"]]; x["minPrice"], x["maxPrice"] = min(pr), max(pr)

h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
if "'Berets \\u00b7 Plain Berets'" not in h:                          # delivery weight for the new subcategory
    h = h.replace("'Berets \\u00b7 Lamberets': 0.3,", "'Berets \\u00b7 Lamberets': 0.3, 'Berets \\u00b7 Plain Berets': 0.3,", 1)
if "'Haberdashery \\u00b7 Brooches'" not in h:
    h = h.replace("'Haberdashery \\u00b7 Pins & Needles': 0.1,", "'Haberdashery \\u00b7 Pins & Needles': 0.1, 'Haberdashery \\u00b7 Brooches': 0.1,", 1)
if "'Dimit Coins'" not in h:
    h = h.replace("'Beading Accessories': 0.2,", "'Beading Accessories': 0.2, 'Dimit Coins': 0.2, 'Beaded Accessories': 0.4, 'Shells': 0.2,", 1)
open(p, "w", encoding="utf-8").write(h)
print("patched", p, "-", len(P), "products")
