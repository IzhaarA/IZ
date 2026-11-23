# Real pack photos for Czech (Preciosa) seed bead colours that only had a thin colour strip (23 Nov 2026).
# PHOTOS: option code -> photo in new-products/photos/. That option, and the product's card picture, use the photo.
# Usage: python3 patch-czphotos.py public/index.html   (after the catalogue patches, before make-seo-pages.py)
import json, os, sys, shutil
from PIL import Image
PHOTOS = {'CZ-46112-8/0-L': 'cz-46112-8-0-loose.jpg'}   # Shell Yellow/Brown Luster (cream), 8/0 loose, 23 Nov 2026
P = sys.argv[1]; PUB = os.path.dirname(os.path.abspath(P)); H = os.path.dirname(os.path.abspath(__file__))
h = open(P, encoding='utf-8').read()
key = 'const PRODUCTS = '; s = h.index(key) + len(key)
PR, end = json.JSONDecoder().raw_decode(h[s:])
n = 0
for prod in PR:
    for v in prod['variants']:
        f = PHOTOS.get(v['id'])
        if not f: continue
        name = 'images/' + os.path.splitext(f)[0] + '.jpg'
        shutil.copy(os.path.join(H, 'new-products', 'photos', f), os.path.join(PUB, name))
        t = Image.open(os.path.join(PUB, name)); t.thumbnail((360, 360)); t.save(os.path.join(PUB, 'thumbs', os.path.basename(name)), quality=85)
        v['img'] = name; v['gallery'] = [name] + [g for g in v.get('gallery', []) if g != name]
        prod['img'] = name; n += 1
h = h[:s] + json.dumps(PR, ensure_ascii=False, separators=(',', ':')) + h[s + end:]
open(P, 'w', encoding='utf-8').write(h)
print('pack photos set:', n)
