"""Builds the Makkie Wholesalers price list (A4 PDF) from the live website's product list.
Price = website price; Stock price = website price minus 5%, rounded down to the rand (for shops and resellers who buy stock).
Usage: python3 build_pricelist.py <site index.html> <site images folder> <work folder>
Writes <work>/catalogue.html; make_pdf.cjs turns it into the PDF (same footer as the catalogue)."""
import json, os, re, sys, html, math
from datetime import date
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SITE, IMGS, WORK = sys.argv[1:4]
DISCOUNT = 0.05
h = open(SITE).read(); k = 'const PRODUCTS = '
P = json.JSONDecoder().raw_decode(h[h.index(k) + len(k):])[0]
os.makedirs(os.path.join(WORK, 'img'), exist_ok=True)
GROUPS = ['Beads', 'Blankets & Textiles', 'Clothing & Traditional Wear', 'Haberdashery & General Goods']
e = html.escape

def photo(src):                                  # small website photo for the table
    name = os.path.basename(src); out = os.path.join(WORK, 'img', name)
    if not os.path.exists(out):
        im = Image.open(os.path.join(IMGS, name)).convert('RGB'); im.thumbnail((240, 240)); im.save(out, quality=75, optimize=True)
    return 'img/' + name

def money(x):
    return f'R{x:,.0f}' if abs(x - round(x)) < 0.005 else f'R{x:,.2f}'

def short(l):                                    # "Size 8/0 · ¼kg strung" -> "8/0 strung"
    m = re.match(r'(?:Size )?(.+?) · ¼kg (\w+)', l)
    return f'{m.group(1)} {m.group(2)}' if m else l

def rows(p):
    """One row per price. Same-price colours share a row; blankets, shawls and throws never list colours."""
    labels = [v['label'] for v in p['variants']]
    by = {}
    for v in p['variants']: by.setdefault(v['price'], []).append(v['label'])
    if len(by) == 1:
        opt = ''
        if labels not in (['Standard'], [p['name']]) and p['group'] != 'Blankets & Textiles':
            if all(l.startswith('Size ') or '·' in l for l in labels): opt = ', '.join(short(l) for l in labels)
            elif len(labels) > 1: opt = f'{len(labels)} colours / options'
            elif labels[0] not in (p.get('size'), p['name']): opt = labels[0]
        return [(opt, next(iter(by)))]
    out = []
    for price, ls in sorted(by.items()):
        colourish = p['group'] == 'Blankets & Textiles' and not all(re.search(r'\d+x\d+|bed|pack|single|towel', l, re.I) for l in ls)
        out.append(('Other sizes' if colourish else ', '.join(short(l) for l in ls), price))
    return out

def table(items):
    tr = []
    for p in items:
        rs = rows(p); size = p.get('size') or ''
        sub = ' · '.join(x for x in ['Size ' + size if re.fullmatch(r'\d+', size) else size,
                                      p['unit'] if p['unit'] not in ('unit', 'pair') and p['unit'].lower() not in p['name'].lower() else ''] if x)
        for i, (opt, price) in enumerate(rs):
            first = i == 0
            tr.append('<tr' + (' class="top"' if first else '') + '>'
                      + (f'<td class="ph" rowspan="{len(rs)}"><img src="{photo(p["img"])}"></td><td class="cd" rowspan="{len(rs)}">{e(p["id"])}</td>'
                         f'<td class="nm" rowspan="{len(rs)}"><b>{e(p["name"])}</b>' + (f'<div class="sub">{e(sub)}</div>' if sub else '') + '</td>' if first else '')
                      + f'<td class="op">{e(opt)}</td><td class="pr">{money(price)}</td><td class="sp">{money(math.floor(price * (1 - DISCOUNT) + 1e-9))}</td></tr>')
    return ('<table><thead><tr><th></th><th>Code</th><th>Product</th><th>Size / option</th><th class="pr">Price</th>'
            '<th class="sp">Stock price</th></tr></thead><tbody>' + ''.join(tr) + '</tbody></table>')

sections = []
for g in GROUPS:
    for cat in sorted({p['category'] for p in P if p['group'] == g}, key=str.lower):
        sections.append(f'<section><h2>{e(cat.replace(" · ", " — "))}</h2>{table([p for p in P if p["category"] == cat])}</section>')

logo = os.path.join(H, '..', 'logo', 'makkies-logo.png')
CSS = """@page{size:A4;margin:14mm 12mm 16mm}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,'Liberation Sans',sans-serif;color:#222;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cover{height:262mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;page-break-after:always}
.cover .logo{width:150mm;margin-bottom:14mm}
.cover h1{font-size:24px;margin-bottom:3mm}.cover .date{font-size:13px;color:#666;margin-bottom:8mm}.cover p{font-size:15px;line-height:1.75}
.cover .note{font-size:13px;color:#444;margin-top:8mm;max-width:150mm;line-height:1.7;border:1px solid #ddd;border-radius:8px;padding:10px 14px;text-align:left}
section{margin-bottom:7mm}
h2{background:#1f1c1d;color:#fff;font-size:13px;letter-spacing:2.5px;text-transform:uppercase;padding:7px 10px;border-radius:5px;margin-bottom:4px;break-after:avoid}
table{width:100%;border-collapse:collapse;font-size:10.5px}thead{display:table-header-group}
th{text-align:left;font-size:9.5px;color:#666;font-weight:normal;text-transform:uppercase;letter-spacing:1px;padding:3px 5px;border-bottom:1.5px solid #1f1c1d}
td{padding:2px 5px;vertical-align:middle;border-bottom:1px solid #eee}tr{break-inside:avoid}tr.top td{border-top:1px solid #ccc}
.ph{width:13mm;text-align:center}.ph img{max-width:10mm;max-height:10mm;display:block;margin:auto}
.cd{width:22mm;color:#555;font-size:9.5px}.nm{width:58mm}.sub{font-size:9.5px;color:#777;margin-top:1px}.op{color:#8a2f2a;font-size:9.5px}
.pr,.sp{width:22mm;text-align:right;white-space:nowrap}.pr{font-weight:bold}.sp{font-weight:bold;color:#0a6b3a;background:#eef7f1}
th.sp{color:#0a6b3a}"""
today = date.today()
cover = f'''<div class="cover"><img class="logo" src="file://{os.path.abspath(logo)}"><h1>Price List</h1><div class="date">{today.strftime("%B %Y")}</div>
<p>WhatsApp 072 323 5469 · Tel 012 323 5469<br>
orders@makkies.co.za<br>makkies.co.za</p>
<div class="note"><b>Price</b> is our normal price, the same as on makkies.co.za.<br><b>Stock price</b> is 5% less, for shops and resellers buying stock to sell.<br>
To order, WhatsApp us the product codes and quantities and we'll send you a quote. We deliver anywhere in South Africa: PAXI to any PEP store or courier (delivery is extra), or collect in Marabastad.
Prices may change without notice. Stock and colours are subject to availability.</div></div>'''
open(os.path.join(WORK, 'catalogue.html'), 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><title>Makkie Wholesalers — Price List</title><style>{CSS}</style></head><body>{cover}{"".join(sections)}</body></html>')
print(len(P), 'products,', len(sections), 'sections')
