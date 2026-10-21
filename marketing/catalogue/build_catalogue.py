"""Builds the Makkie Wholesalers product catalogue (A4 PDF) from the live website's product list.
Usage: python3 build_catalogue.py <site index.html> <site images folder> <work folder>
Writes <work>/catalogue.html with resized photos in <work>/img; make_pdf.cjs turns it into the PDF."""
import json, os, re, sys, html
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SITE, IMGS, WORK = sys.argv[1:4]
h = open(SITE).read(); k = 'const PRODUCTS = '
P = json.JSONDecoder().raw_decode(h[h.index(k) + len(k):])[0]
os.makedirs(os.path.join(WORK, 'img'), exist_ok=True)
GROUPS = ['Beads', 'Blankets & Textiles', 'Clothing & Traditional Wear', 'Haberdashery & General Goods']
e = html.escape

def photo(src):                                  # website photo, resized for print
    name = os.path.basename(src); out = os.path.join(WORK, 'img', name)
    if not os.path.exists(out):
        im = Image.open(os.path.join(IMGS, name)).convert('RGB'); im.thumbnail((480, 480)); im.save(out, quality=78, optimize=True)
    return 'img/' + name

def czech(labels):                               # "Size 8/0 · ¼kg strung", "Size 8/0 · ¼kg loose" -> "8/0 (strung, loose)"
    sizes = {}
    for l in labels:
        m = re.match(r'(?:Size )?(.+?) · ¼kg (\w+)', l)
        if m: sizes.setdefault(m.group(1), []).append(m.group(2))
    return 'Sizes: ' + ' · '.join(f"{s} ({', '.join(w)})" for s, w in sizes.items())

def variations(p):
    labels = [v['label'] for v in p['variants']]
    if labels in (['Standard'], [p['name']]): return ''
    if p['group'] == 'Blankets & Textiles':      # no colour counts or colour lists for blankets, shawls and throws
        sized = [l for l in labels if re.search(r'\d+x\d+|bed', l, re.I)]
        return 'Sizes: ' + ', '.join(sized) if sized and len(sized) == len(labels) else ''
    if p['category'].startswith('Czech'): return czech(labels)
    if re.search(r'[–-]', p.get('size') or '') and len(labels) > 3: return ''   # size range already shown (tekkies, overcoats)
    if all(l.startswith('Size ') for l in labels):
        return ('Sizes: ' if len(labels) > 1 else 'Size ') + ' · '.join(l[5:] for l in labels)
    if len(labels) == 1: return '' if labels[0] in (p.get('size'), p['name']) else labels[0]
    if all(re.search(r'\d(mm|cm|m)\b', l) for l in labels): return 'Sizes: ' + ', '.join(labels)
    return 'Options: ' + ', '.join(labels)

def card(p):
    size = p.get('size') or ''
    bits = [e('Size ' + size if re.fullmatch(r'\d+', size) else size)] if size else []
    if p['unit'] not in ('unit', 'pair') and p['unit'].lower() not in p['name'].lower(): bits.append(e(p['unit']))
    bits.append('Code ' + e(p['id']))
    var = variations(p)
    return (f'<div class="card"><div class="ph"><img src="{photo(p["img"])}"></div><div class="nm">{e(p["name"])}</div>'
            f'<div class="sub">{" · ".join(bits)}</div>' + (f'<div class="var">{e(var)}</div>' if var else '') + '</div>')

sections = []
for g in GROUPS:
    for cat in sorted({p['category'] for p in P if p['group'] == g}, key=str.lower):
        items = [p for p in P if p['category'] == cat]
        cols = 3 if len(items) > 6 else 2
        sections.append(f'<section class="c{cols}"><h2>{e(cat.replace(" · ", " — "))}</h2><div class="grid">{"".join(card(p) for p in items)}</div></section>')

logo = os.path.join(H, '..', 'logo', 'makkies-logo-outline.png')   # outlined lettering, like the shop's note pads
CSS = """@page{size:A4;margin:14mm 12mm 16mm}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,'Liberation Sans',sans-serif;color:#222;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cover{height:262mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;page-break-after:always}
.cover .logo{width:150mm}.bar{width:140mm;height:7px;margin:12mm 0 9mm;background:linear-gradient(90deg,#45203F 0 12%,#FFC814 12% 30%,#1E3FA8 30% 46%,#C3312B 46% 62%,#0A7F48 62% 74%,#C3312B 74% 84%,#FFC814 84% 100%)}
.cover h1{font-size:22px;margin-bottom:8mm}.cover p{font-size:15px;line-height:1.75}.cover .note{font-size:12.5px;color:#666;margin-top:8mm;max-width:140mm;line-height:1.7}
section{page-break-before:always}section:first-of-type{page-break-before:auto}
h2{background:#1f1c1d;color:#fff;font-size:15px;letter-spacing:3px;text-transform:uppercase;padding:9px 12px;border-radius:6px;margin-bottom:8px}
.grid{display:grid;gap:8px}.c2 .grid{grid-template-columns:1fr 1fr}.c3 .grid{grid-template-columns:1fr 1fr 1fr}
.card{border:1px dashed #bbb;border-radius:6px;padding:7px 8px 8px;text-align:center;break-inside:avoid}
.ph{display:flex;align-items:center;justify-content:center}.c2 .ph{height:64mm}.c3 .ph{height:41mm}
.ph img{max-width:100%;max-height:100%}
.nm{font-weight:bold;font-size:14.5px;margin-top:5px}.c3 .nm{font-size:12.5px}
.sub{font-size:11.5px;color:#666;margin-top:2px}.c3 .sub{font-size:10.5px}
.var{font-size:11px;color:#8a2f2a;margin-top:2px;line-height:1.35}.c3 .var{font-size:10px}"""
cover = f'''<div class="cover"><img class="logo" src="file://{os.path.abspath(logo)}"><div class="bar"></div><h1>Product Catalogue</h1>
<p>Unit D4, Pretoria Oriental Complex, Entrance 6, 7th Street<br>Marabastad, Pretoria<br>WhatsApp 072 323 5469 · Tel 012 323 5469<br>
orders@makkies.co.za · blankets@yebo.co.za<br>makkies.co.za</p>
<p class="note">Wholesale and retail pricing on request — send us the product codes on WhatsApp and we'll quote you. Stock and colours are subject to availability.</p></div>'''
open(os.path.join(WORK, 'catalogue.html'), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Makkie Wholesalers — Product Catalogue</title><style>{CSS}</style></head><body>{cover}{"".join(sections)}</body></html>')
print(len(P), 'products,', len(sections), 'sections')
