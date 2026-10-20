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
  prod("PIN-013", "Thick Needle", PN, "12cm long · 1mm thick", "unit", [("Standard", 7, ph("thick_needle_12cm"))]),
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
# Traditional items (Oct 2026)
TG, TI = "Clothing & Traditional Wear", "Traditional Items"
def ti(id, name, size, unit, variants, desc=None, cat=TI): return prod(id, name, cat, size, unit, variants, desc, TG)
AXE = ph("ndebele_painted_axe_all")
NEW += [
  ti("TRD-001", "Leopard Shell — Large", "", "unit", [("Standard", 30, ph("leopard_shell_large"))]),
  ti("TRD-002", "Leopard Shell — Small", "", "unit", [("Standard", 20, ph("leopard_shell_small"))]),
  ti("TRD-003", "Ndoro Ceramic Disc", "35mm", "unit", [("Standard", 20, ph("Ndoro_ceramic_disc"))]),
  ti("TRD-004", "Cowrie Shells", "100g", "packet", [("Standard", 50, ph("cowrie_shells_1", "cowrie_shells_2"))]),
  ti("TRD-005", "Dimit Coins — Matte Gold", "15mm", "pack of 50", [("Standard", 20, ph("matte_gold_dimit_coins"))]),
  ti("TRD-006", "Dimit Coins — Matte Silver", "15mm", "pack of 50", [("Standard", 20, ph("matte_silver_dimit_coins"))]),
  ti("TRD-007", "Dimit Coins — Shiny Gold", "15mm", "pack of 50", [("Standard", 20, ph("shiny_gold_dimit_coins"))]),
  ti("TRD-008", "Dimit Coins — Shiny Silver", "15mm", "pack of 50", [("Standard", 20, ph("shiny_silver_dimit_coins"))]),
  ti("TRD-009", "Beaded Knob Stick", "30cm", "unit", [("Standard", 75, ph("beaded_knob_stick"))], "Assorted bead colours."),
  ti("TRD-010", "Beaded Necklace — Small", "", "unit", [("Standard", 50, ph("beaded_necklace_small"))]),
  ti("TRD-011", "Beaded Necklace — Medium", "", "unit", [("Standard", 75, ph("beaded_necklace_medium"))]),
  ti("TRD-012", "Beaded Necklace — Large", "", "unit", [("Standard", 150, ph("beaded_necklace_large"))]),
  ti("TRD-013", "Mini Wooden Knob Stick", "40cm", "unit", [("Standard", 30, ph("mini_wooden_knob"))]),
  ti("TRD-014", "Mini Wooden Spear", "40cm", "unit", [("Standard", 30, ph("mini_wooden_spear"))]),
  ti("TRD-015", "Shell Belt Set", "", "set", [("Standard", 100, ph("shell_belt"))]),
  ti("TRD-016", "Ndebele Painted Wooden Axe", "40cm", "unit", [
      ("Stripes", 100, ph("ndebele_painted_axe_1") + AXE), ("Blue & Pink", 100, ph("ndebele_painted_axe_2") + AXE),
      ("Red", 100, ph("ndebele_painted_axe_3") + AXE)]),
  ti("TRD-017", "Poryan Animal Skin", "", "unit", [("Standard", 200, ph("poryan_animal_skin"))]),
  ti("TRD-018", "Mapoto Canvas Apron", "", "unit",
     [(f"Size {z}", 55, ph("mapoto_canvas_apron")) for z in ("14", "14½", "15", "15½", "16", "16½", "17", "17½", "18")]),
  ti("TRD-019", "Animal Fur Headband", "", "unit", [("Standard", 60, ph("animal_fur_headband_2", "animal_fur_headband_1"))]),
  ti("TRD-020", "Plain Wooden Axe", "", "unit", [("Standard", 40, ph("plain_wooden_axe"))]),
  ti("TRD-021", "Matseka Wire Leg Ring — Thick", "", "unit", [("Standard", 15, ph("matseka_wire_leg_thick"))]),
  ti("TRD-022", "Matseka Wire Leg Ring — Thin", "", "unit", [("Standard", 15, ph("matseka_wire_leg_thin"))]),
  ti("TRD-023", "Beaded Neck Ring & Tie", "", "unit", [("Standard", 350, ph("beaded_neck_ring_and_tie_chinese"))]),
  ti("TRD-024", "Matseka Wire Hand Bangle — Thick", "", "unit", [("Standard", 10, ph("matseka_wire_bangle_hand_thick"))]),
  ti("TRD-025", "Matseka Wire Hand Bangle — Thin", "", "unit", [("Standard", 10, ph("matseka_wire_bangle_hand_thin"))]),
  ti("TRD-026", "Stretchy Matseka Bangle — Gold", "", "unit", [("Standard", 15, ph("stretchy_matseka_bangle_gold"))]),
  ti("TRD-027", "Stretchy Matseka Bangle — Silver", "", "unit", [("Standard", 15, ph("stretchy_matseka_bangle_silver"))]),
  ti("TRD-028", "Stretchy Matseka Bangles 12 Pack — Maroon", "", "pack of 12", [("Standard", 35, ph("stretchy_matseka_bangle_12pkt_maroon"))]),
  ti("TRD-029", "Stretchy Matseka Bangles 12 Pack — Silver", "", "pack of 12", [("Standard", 35, ph("stretchy_matseka_bangle_12pkt_silver"))]),
  ti("TRD-030", "Stretchy Matseka Bangles 12 Pack — Copper", "", "pack of 12", [("Standard", 35, ph("stretchy_matseka_bangle_12pkt_copper"))]),
  ti("TRD-031", "Beaded Necklace + Bangle", "", "set", [(c, 75, ph(f"beaded_necklace_bangle_{i}")) for i, c in
      enumerate(("Black & White", "Yellow & Blue", "Green", "Orange", "Blue"), 1)]),
  ti("TRD-032", "Rose Brooch", "", "unit", [(c, 20, ph(f"small_rose_brooch_{i}")) for i, c in
      enumerate(("Lilac", "Blue", "Copper", "Green", "Pink", "Light Pink"), 1)]),
  ti("TRD-033", "Flowers Brooch", "", "unit", [(c, 20, ph(f"small_flowers_brooch_{i}")) for i, c in
      enumerate(("Blue", "Green", "Pink", "Peach", "Blue & Silver", "Light Pink"), 1)]),
  ti("APB-001", "Animal Print Beret — Beige/Black", "", "unit", [("Standard", 85, ph("animal_print_beret_beige_black"))], cat="Berets · Animal Print Berets"),
  ti("APB-002", "Animal Print Beret — White/Black", "", "unit", [("Standard", 85, ph("animal_print_beret_white_black"))], cat="Berets · Animal Print Berets"),
]
NEW[[n["id"] for n in NEW].index("TRD-016")]["img"] = AXE[0]          # card shows all three axes
# product id -> new photos (first one is the card photo)
REPLACE = {
  "PIN-001": ph("blanket_pins_45mm_new"), "PIN-002": ph("blanket_pins_80mm_new"),
  "COT-005": ph("ideel_black_cotton_new"), "COT-004": ph("ideel_white_cotton_new"), "COT-006": ph("ideel_white_cotton_new"),
  "BER-008": ph("new_zcc_green_beret", "new_zcc_green_beret_2"), "WHS-004": ph("police_whistle_new"),
}
AFTER = {"PIN-010": "PIN-009", "TWL-003": "TWL-002", "DCE-001": "DOM-003", "COT-010": "COT-009", "TWN-007": "TWN-006", "TRD-001": "NDJ-003", "APB-001": "BER-007"}  # place next to related items

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
for cat, kg in (("Traditional Items", 0.5), ("Berets \\u00b7 Animal Print Berets", 0.3)):   # delivery weights for the new categories
    if f"'{cat}'" not in h: h = h.replace("'Berets \\u00b7 Lamberets': 0.3,", f"'Berets \\u00b7 Lamberets': 0.3, '{cat}': {kg},", 1)
open(p, "w", encoding="utf-8").write(h)
if len(sys.argv) > 2:
    pub = os.path.dirname(os.path.abspath(p))
    for sub in ("images", "thumbs"):
        os.makedirs(os.path.join(pub, sub), exist_ok=True)
        for f in os.listdir(os.path.join(sys.argv[2], sub)): shutil.copy(os.path.join(sys.argv[2], sub, f), os.path.join(pub, sub, f))
print("patched", p, "-", added, "new products,", len(REPLACE), "products with new photos")
