"""Photos for the 'we now accept online payment' TikTok ad (Oct 2026) -> ../instagram/source/ph/pay_*.jpg.
Usage: python3 pay_collect.py <site index.html> <site images folder> <full-size photo folder>
Uses the suppliers' full-size photos where the website only keeps a small copy (Umbhalo: the Mini Umbhalo photo,
same design, because the Umbhalo photo is only 363px)."""
import json, sys, os, re, hashlib, subprocess
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); PH = os.path.join(H, '..', 'instagram', 'source', 'ph')
h = open(sys.argv[1]).read(); k = 'const PRODUCTS = '; by = {p['id']: p for p in json.JSONDecoder().raw_decode(h[h.index(k) + len(k):])[0]}
IMGS, HI = sys.argv[2], sys.argv[3]
def full(url):
    url = re.sub(r'_\d+x(\.\w+)(\?|$)', r'\1\2', url)
    out = os.path.join(HI, hashlib.md5(url.encode()).hexdigest()[:12] + '.jpg')
    if not os.path.exists(out): subprocess.run(['curl', '-sSf', '-m', '60', '-o', out, url], check=True)
    return out
def take(name, pid, label=None, photo=None):     # photo: one of the website's photos of the product, by file name
    p = by[pid]; v = next(x for x in p['variants'] if label is None or x['label'] == label)
    src = os.path.join(IMGS, photo) if photo else full(v['url']) if v.get('url') else os.path.join(IMGS, os.path.basename(v['img']))
    im = Image.open(src).convert('RGB'); im.save(os.path.join(PH, f'pay_{name}.jpg'), quality=92)
    return dict(name=name, id=pid, title=p['name'], price=min(x['price'] for x in p['variants']), size=im.size)
OUT = [take('czech1', 'CZ-93140'), take('czech2', 'CZ-33060'), take('czech3', 'CZ-53250'),
       take('wedding_shawl', 'SHW-011', photo='e23966438394.jpg'),          # our own photo, full (not the square card crop)
       take('xhosa_black', 'TRB-029', 'Black Stripe'),
       take('ziela_gold', 'NZL-001'), take('ziela_silver', 'NZL-002'),
       take('tekkies', 'TEK-002'), take('ukhamba', 'TRB-003'), take('umbhalo', 'TRB-001'), take('elizabeth', 'TRB-022', 'Red')]
for o in OUT: print(o)
