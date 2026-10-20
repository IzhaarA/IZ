"""New products (Oct 2026) and replacement photos. Safe to re-run.
Usage: python3 patch-new-products.py public/index.html [new-products-folder]
With the folder given, the cropped photos (new-products/images + thumbs) are copied into public/ too."""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PH = json.load(open(os.path.join(HERE, "new-products", "photos.json")))
def ph(*names): return [PH[n] for n in names]
HG = "Haberdashery & General Goods"

def prod(id, name, cat, size, unit, variants, desc=None, group=HG):
    p = {"id": id, "name": name, "category": cat, "group": group, "size": size, "unit": unit}
    if desc: p["desc"] = desc
    vs = []
    for i, (label, price, photos) in enumerate(variants, 1):
        v = {"id": f"{id}-{'STD' if len(variants) == 1 else str(i).zfill(2)}", "label": label, "price": price, "img": photos[0]}
        if len(photos) > 1: v["gallery"] = photos
        vs.append(v)
    p["variants"] = vs; p["img"] = vs[0]["img"]
    pr = [v["price"] for v in vs]; p["minPrice"], p["maxPrice"] = min(pr), max(pr)
    return p

PN, CT = "Haberdashery · Pins & Needles", "Haberdashery · Cotton & Twine"
NEW = [
  prod("PIN-010", "Army & Navy Needles", PN, "19 needles", "book", [("Standard", 10, ph("army_navy_needles_1", "army_navy_needles_2"))], "Needle book with assorted hand-sewing needles."),
  prod("PIN-011", "Upholstery Needles", PN, "Sizes 5, 6, 7 & 10", "pack of 4", [("Standard", 30, ph("upholstery_needles"))], "Curved and straight upholstery needles."),
  prod("PIN-012", "Measuring Tape", PN, "150cm", "unit", [("Standard", 10, ph("measuring_tape"))], "Soft sewing tape measure, cm and inches."),
  prod("PIN-013", "Thick Needle", PN, "12cm", "unit", [("Standard", 7, ph("thick_needle_12cm"))]),
  prod("TWL-003", "Block Hand Towel", "Towels", "50x90cm", "unit", [("Standard", 75, ph("block_hand_towel"))]),
  prod("TWL-004", "Colibri Guest Towel", "Towels", "30x50cm", "unit", [
      ("Single towel", 35, ph("colibri_guest_towel_1", "colibri_guset_towel_2", "colibri_guset_towel_3")),
      ("Pack of 10", 300, ph("colibri_guest_towel_1", "colibri_guset_towel_2", "colibri_guset_towel_3"))], "Assorted designs."),
  prod("DCE-001", "Dice 100 Pack — 5mm", "Dice & Dominoes", "5mm", "pack of 100", [("Standard", 50, ph("dice_100pkt_5mm"))]),
  prod("DCE-002", "Dice 100 Pack — 9mm", "Dice & Dominoes", "9mm", "pack of 100", [("Standard", 50, ph("dice_100pkt_9mm"))]),
  prod("DCE-003", "Dice 20 Pack — Colour Dots", "Dice & Dominoes", "14mm", "pack of 20", [("Standard", 30, ph("dice_20pkt"))], "Red and blue dots."),
  prod("COT-010", "Shirring Elastic 10g — Black", CT, "10g", "reel", [("Standard", 10, ph("shirring_elastic_black_10g"))], "0.6mm shirring elastic."),
  prod("COT-012", "Shirring Elastic 10g — White", CT, "10g", "reel", [("Standard", 10, ph("shirring_elastic_white_10g"))], "0.6mm shirring elastic."),
  prod("COT-013", "Shirring Elastic 30m — Black", CT, "30m", "reel", [("Standard", 50, ph("shirring_elastic_black_30m"))], "0.8mm shirring elastic."),
  prod("COT-014", "Shirring Elastic 30m — White", CT, "30m", "reel", [("Standard", 50, ph("shirring_elastic_white_30m_1", "shirring_elastic_white_30m_2"))], "0.8mm shirring elastic."),
  prod("TWN-007", "Sisal Dry Twine", CT, "500g", "unit", [("Standard", 95, ph("sisal_dry_twine", "sisal_dry_twine_2"))], "100% natural fibre."),
  prod("COT-011", "Crochet Cotton no.5 Spring Time — Black", CT, "500g", "cone", [("Standard", 105, ph("springtime_black_500g", "springtime_black_500g_2"))]),
  prod("COT-015", "Crochet Cotton no.5 Spring Time — White", CT, "500g", "cone", [("Standard", 105, ph("springtime_white_500g", "springtime_white_500g_2"))]),
  prod("PIP-001", "Smoking Pipe", "Smoking Pipes", "", "unit", [("Standard", 40, ph("smoking_pipe_1", "smoking_pipe_2"))], "Comes in a gift tray."),
]
# product id -> new photos (first one is the card photo)
REPLACE = {
  "PIN-001": ph("blanket_pins_45mm_new"), "PIN-002": ph("blanket_pins_80mm_new"),
  "COT-005": ph("ideel_black_cotton_new"), "COT-004": ph("ideel_white_cotton_new"), "COT-006": ph("ideel_white_cotton_new"),
  "BER-008": ph("new_zcc_green_beret", "new_zcc_green_beret_2"), "WHS-004": ph("police_whistle_new"),
}
AFTER = {"PIN-010": "PIN-009", "TWL-003": "TWL-002", "DCE-001": "DOM-003", "COT-010": "COT-009", "TWN-007": "TWN-006"}  # place next to related items

p = sys.argv[1]
h = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = h.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(h[s:])
have = {x["id"] for x in P}
added = 0
anchor = None
for n in NEW:
    if n["id"] in have: continue
    a = AFTER.get(n["id"]) or anchor
    ids = [x["id"] for x in P]
    P.insert(ids.index(a) + 1 if a in ids else len(P), n); anchor = n["id"]; added += 1
for x in P:
    if x["id"] in REPLACE:
        photos = REPLACE[x["id"]]
        for v in x["variants"]:
            v["img"] = photos[0]; v.pop("url", None)
            if len(photos) > 1: v["gallery"] = photos
            else: v.pop("gallery", None)
        x["img"] = photos[0]
h = h[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + h[s + end:]
open(p, "w", encoding="utf-8").write(h)
if len(sys.argv) > 2:
    pub = os.path.dirname(os.path.abspath(p))
    for sub in ("images", "thumbs"):
        os.makedirs(os.path.join(pub, sub), exist_ok=True)
        for f in os.listdir(os.path.join(sys.argv[2], sub)): shutil.copy(os.path.join(sys.argv[2], sub, f), os.path.join(pub, sub, f))
print("patched", p, "-", added, "new products,", len(REPLACE), "products with new photos")
