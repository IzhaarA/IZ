"""Square card photos for the shawls & throws (front photo, whole shawl in frame).
Usage: python3 make-shawl-thumbs.py public            (run inside the deploy folder after the photos are downloaded)
For every shawl/throw whose card photo is its front photo (images/X.jpg), writes
  public/images/X-sq.jpg  (900x900)  and  public/thumbs/X-sq.jpg (360x360)
and points the product's card photo at it. The product page still shows the full photos.
Safe to re-run."""
import json, os, sys
from PIL import Image, ImageFilter

pub = sys.argv[1]
TOP, BOTTOM = 0.04, 0.93          # keep from just above the stand's head to below the hem (fractions of photo height)
# Photos taken from further away get a closer crop: product id -> (top, bottom, centre x), fractions of the photo
CLOSER = {
    "CSH-001": (0.115, 0.785, 0.487),   # C1 Black chenille throw
}

def square(src, top=TOP, bottom=BOTTOM, cx=0.5):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    y0, y1 = int(H * top), int(H * bottom)
    band = im.crop((0, y0, W, y1)); h = y1 - y0
    if W >= h:                                   # wide enough: crop around the stand
        x0 = min(max(0, int(W * cx - h / 2)), W - h); return band.crop((x0, 0, x0 + h, h))
    pad = (h - W + 1) // 2
    out = Image.new("RGB", (W + 2 * pad, h))
    out.paste(band, (pad, 0))
    # extend the wall/floor sideways: stretch the outer 3% of each side, softly blurred
    e = max(4, W // 33)
    left = band.crop((0, 0, e, h)).resize((pad, h)).filter(ImageFilter.GaussianBlur(6))
    right = band.crop((W - e, 0, W, h)).resize((pad, h)).filter(ImageFilter.GaussianBlur(6))
    out.paste(left, (0, 0)); out.paste(right, (W + pad, 0))
    return out.crop((0, 0, h, h))

p = os.path.join(pub, "index.html")
html = open(p, encoding="utf-8").read()
key = "const PRODUCTS = "; s = html.index(key) + len(key)
P, end = json.JSONDecoder().raw_decode(html[s:])
made = 0
for prod in P:
    if not prod["category"].startswith("Shawls & Throws"): continue
    for v in prod["variants"]:
        g = v.get("gallery") or []
        if len(g) != 2: continue
        front = g[0]
        if v.get("img") not in (front, front[:-4] + "-sq.jpg", front[:-4] + "-sqz.jpg"): continue      # only our own front-first photos
        close = CLOSER.get(prod["id"])
        sq = front[:-4] + ("-sqz.jpg" if close else "-sq.jpg")
        src = os.path.join(pub, front)
        if not os.path.exists(os.path.join(pub, sq)):
            img = square(src, *close) if close else square(src)
            img.resize((900, 900), Image.LANCZOS).save(os.path.join(pub, sq), quality=84, optimize=True)
            os.makedirs(os.path.join(pub, "thumbs"), exist_ok=True)
            img.resize((360, 360), Image.LANCZOS).save(os.path.join(pub, "thumbs", sq[7:]), quality=82, optimize=True)
        if prod.get("img") == v["img"]: prod["img"] = sq
        v["img"] = sq; made += 1
html = html[:s] + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + html[s + end:]
open(p, "w", encoding="utf-8").write(html)
print("shawl card photos:", made)
