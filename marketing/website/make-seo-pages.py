"""Search-engine pages for makkies.co.za, built from the products in public/index.html.
Usage: python3 make-seo-pages.py public        (run last, after the patches; safe to re-run)

Writes into public/:
  p/<name>-<code>/index.html   one real page per product (title, photo, prices, options, Product schema)
  c/<category>/index.html      one page per category, listing its products
  products/index.html          every category and product on one page (linked from the shop footer)
  returns/, terms/, privacy/   the shop's Delivery & returns, Terms and Privacy pages as real pages
  sitemap.xml, robots.txt      tell Google/Bing which pages exist
  google-products.xml          Google Merchant Center feed (free Shopping listings), one item per option
  llms.txt                     short plain-text summary for AI assistants
The shop itself is unchanged: every page's "Buy online" button opens the product in the shop (/#p/<code>)."""
import json, os, re, sys, html
from urllib.parse import quote
from datetime import date
from xml.sax.saxutils import escape as xesc

PUB = sys.argv[1]
SITE = 'https://makkies.co.za'
WA = '27723235469'
TODAY = date.today().isoformat()
h = open(os.path.join(PUB, 'index.html'), encoding='utf-8').read()
k = 'const PRODUCTS = '
P = json.JSONDecoder().raw_decode(h[h.index(k) + len(k):])[0]
m = re.search(r'const SOLD_OUT = (\[.*?\]);', h)
SOLD = set(json.loads(m.group(1))) if m else set()
for p in P:
    for v in p['variants']: v['soldOut'] = p['id'] in SOLD or v['id'] in SOLD
    p['soldOut'] = all(v['soldOut'] for v in p['variants'])
e = html.escape
GROUPS = ['Blankets & Textiles', 'Beads', 'Clothing & Traditional Wear', 'Haberdashery & General Goods']

def slug(s):
    s = s.lower().replace('&', ' and ').replace('¼', 'quarter')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def money(x): return f'R{x:,.0f}' if x == int(x) else f'R{x:,.2f}'

def leaf(cat): return cat.split(' · ')[-1]

CATNAME = {'Basotho': 'Basotho Blankets', 'Ndebele': 'Ndebele Blankets', 'Xhosa': 'Xhosa Blankets', '100% Acrylic': '100% Acrylic Shawls & Throws',
           '3mm Round': '3mm Round Plastic Beads', '6mm Round': '6mm Round Plastic Beads', '8mm Oval': '8mm Oval Plastic Beads',
           'Oval Necklaces': 'Plastic Bead Oval Necklaces', 'Mens Pacino Hats': "Men's Pacino Hats"}
def cname(cat): return CATNAME.get(leaf(cat), leaf(cat))   # page name for a category, e.g. "Tribal Blankets · Basotho" -> "Basotho Blankets"

SUFFIX = {   # what each category adds to a short product name ("Coral" -> "Coral Plain Shawl"); '' adds nothing
    '100% Acrylic': 'Acrylic Shawl', 'Chenille Throws': 'Chenille Throw', 'Cloudsoft Shawls': 'Cloudsoft Shawl', 'Lema Shawls': 'Lema Shawl',
    'Plaid and Scotch Throws': 'Throw', 'Plain Shawls': 'Plain Shawl', 'Polymohair Shawls': 'Polymohair Shawl', 'Small Check Shawls': 'Small Check Shawl',
    'Small Plain Shawls': 'Small Plain Shawl', 'Small Wooly Shawls': 'Small Wooly Shawl', 'Soft Touch Shawls': 'Soft Touch Shawl', 'Wedding Shawls': 'Wedding Shawl',
    'Basotho': 'Basotho Blanket', 'Ndebele': 'Ndebele Blanket', 'Xhosa': 'Xhosa Blanket', 'Mink Blankets': 'Mink Blanket', 'Hotel Blankets': 'Hotel Blanket',
    'Budget/Charity Blankets': 'Blanket', 'Baby Blankets': 'Baby Blanket', 'Travelling Rugs': 'Travelling Rug', 'Towels': 'Towel', 'Kangas': 'Kanga',
    'Czech Glass Seed Beads': 'Czech Glass Seed Beads', 'Chinese Glass Seed Beads': 'Chinese Glass Seed Beads', '3mm Round': '3mm Round Plastic Beads',
    '6mm Round': '6mm Round Plastic Beads', '8mm Oval': '8mm Oval Plastic Beads', 'Oval Necklaces': 'Plastic Bead Oval Necklace', 'Wooden Beads': 'Wooden Beads',
    'Pearl Beads': 'Pearl Beads', 'Wool': 'Wool', 'Chair Nails': 'Chair Nails', 'Steeltrunks': 'Steel Trunk', 'Scarves': 'Scarf', 'Overcoats': 'Overcoat',
    'Mens Pacino Hats': 'Pacino Hat', 'Straw Hats': 'Straw Hat', 'Lamberets': 'Lamberet', 'Brooches': 'Brooch', 'Whistles': 'Whistle', 'Mirrors': 'Mirror',
    'Bells': 'Bell', 'Handkerchiefs': 'Handkerchief', 'Smoking Pipes': 'Smoking Pipe', 'Bangles': 'Bangle'}

def stem(w): return re.sub(r'(es|s)$', '', w) if len(w) > 3 else w

def title(p):                                    # adds the category words the name is missing, e.g. "Pitseng" -> "Pitseng Basotho Blanket"
    n = p['name']; have = {stem(w) for w in re.findall(r'[a-z0-9%]+', n.lower())}
    suf = SUFFIX.get(leaf(p['category']), '')
    if stem(suf.replace(' ', '').lower()) in {stem(w) for w in re.findall(r'[a-z]+', n.lower())}: suf = ''   # "Steeltrunk" already says "Steel Trunk"
    add = [w for w in suf.split() if stem(w.lower()) not in have]
    return n + (' ' + ' '.join(add) if add else '')

def prices(p):
    pr = [v['price'] for v in p['variants'] if v.get('price') is not None and not v['soldOut']] or \
         [v['price'] for v in p['variants'] if v.get('price') is not None]
    return min(pr), max(pr)

def img_url(src): return SITE + '/' + src.lstrip('/')

def describe(p, t):
    if p.get('desc'): return p['desc']
    lo, hi = prices(p); size = p.get('size') or ''
    n = len(p['variants'])
    bits = [f"{t}{' (' + size + ')' if size else ''} from Makkie Wholesalers in Marabastad, Pretoria",
            f"{'from ' if lo != hi else ''}{money(lo)}" + (f" per {p['unit']}" if p['unit'] not in ('unit', 'pair') else '')]
    if n > 1: bits.append(f'{n} colours/options available' if p['group'] != 'Blankets & Textiles' else 'several colours available')
    return ', '.join(bits) + '. Wholesale and retail, delivered anywhere in South Africa by PAXI or courier.'

for p in P: p['t'] = title(p)
seen = {}
for p in P: seen.setdefault(p['t'], []).append(p)
for same in seen.values():                        # same title twice (e.g. steel trunks in 4 sizes): add the size, else the code
    if len(same) > 1:
        for p in same: p['t'] += f" {(p.get('size') or '').split(' · ')[-1] or p['id']}"
for p in P:
    p['url'] = f"/p/{slug(p['t'])}-{slug(p['id'])}/"
    p['d'] = describe(p, p['t'])
cats = {}
for p in P: cats.setdefault(p['category'], []).append(p)
CURL = {c: f'/c/{slug(c.replace(" · ", " "))}/' for c in cats}

CSS = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,'Liberation Sans',sans-serif;background:#F8F5EF;color:#221F1D;line-height:1.5}
a{color:#1D339E}header{background:#fff;border-bottom:1px solid #DFDACF}header .w{display:flex;align-items:center;justify-content:space-between;gap:12px}
header img{height:44px;width:auto;display:block}header nav a{color:#221F1D;text-decoration:none;font-size:14px;margin-left:14px}
.w{max-width:1080px;margin:0 auto;padding:12px 16px}.crumbs{font-size:13px;color:#6F6A63;margin:8px 0 14px}.crumbs a{color:#6F6A63}
.prod{display:grid;grid-template-columns:1fr 1fr;gap:28px;background:#fff;border:1px solid #DFDACF;border-radius:12px;padding:20px}
.prod img.main{width:100%;height:auto;border-radius:8px;background:#f2efe9}.thumbs{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.thumbs img{width:56px;height:56px;object-fit:cover;border-radius:6px}
h1{font-size:26px;line-height:1.2;margin-bottom:6px}.code{color:#6F6A63;font-size:13px}.price{font-size:26px;font-weight:bold;margin:12px 0 4px}
.so{display:inline-block;background:#FBE7E4;color:#C3312B;border-radius:20px;padding:2px 10px;font-size:13px;font-weight:bold}.ins{color:#1F7A3A;font-weight:bold;font-size:14px}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}.btn{display:inline-block;padding:11px 18px;border-radius:8px;text-decoration:none;font-weight:bold}
.buy{background:#221F1D;color:#fff}.wa{background:#0A7A44;color:#fff}table{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}
td,th{text-align:left;padding:6px 8px;border-bottom:1px solid #eee}th{font-size:12px;color:#6F6A63;text-transform:uppercase;letter-spacing:1px}
.desc{margin-top:12px;font-size:15px}.note{margin-top:10px;font-size:13px;color:#6F6A63}h2{font-size:20px;margin:26px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.card{background:#fff;border:1px solid #DFDACF;border-radius:10px;padding:8px;text-decoration:none;color:#221F1D}
.card img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:6px;background:#f2efe9}.card b{display:block;font-size:14px;margin-top:6px}.card span{font-size:13px;color:#6F6A63}
.intro{font-size:15px;max-width:760px}.policy h3{margin:16px 0 6px}.policy p,.policy ul{margin-bottom:10px}.policy li{margin:0 0 6px 20px}.cats{columns:3 220px;font-size:15px}.cats li{margin:3px 0;list-style:none}
footer{margin-top:36px;background:#24211F;color:#ddd;font-size:14px}footer a{color:#F2B90D}footer .w{padding:22px 16px}
@media(max-width:720px){.prod{grid-template-columns:1fr}h1{font-size:22px}header nav{display:none}}"""

def page(path, ttl, desc, body, ld=(), canonical=None, img=None):
    canonical = canonical or SITE + path
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(ttl)}</title><meta name="description" content="{e(desc[:300])}"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Makkie Wholesalers"><meta property="og:title" content="{e(ttl)}">
<meta property="og:description" content="{e(desc[:300])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{img or SITE + '/og.jpg'}">
<link rel="icon" href="/favicon-64.png"><style>{CSS}</style>{lds}</head><body>
<header><div class="w"><a href="/"><img src="/logo-header.png" alt="Makkie Wholesalers – Blankets • Beads • Traditional Goods" width="258" height="44"></a>
<nav><a href="/">Shop</a><a href="/products/">All products</a><a href="https://wa.me/{WA}">WhatsApp 072 323 5469</a></nav></div></header>
<main class="w">{body}</main>
<footer><div class="w"><b>Makkie Wholesalers</b> · Unit D4, Pretoria Oriental Complex, Entrance 6, 7th Street, Marabastad, Pretoria<br>
WhatsApp <a href="https://wa.me/{WA}">072 323 5469</a> · Tel 012 323 5469 · <a href="mailto:orders@makkies.co.za">orders@makkies.co.za</a><br>
Wholesale and retail. Prices include 15% VAT. Delivery anywhere in South Africa by PAXI or courier, or collect in Marabastad.<br>
<a href="/">Shop online</a> · <a href="/products/">All products</a> · <a href="/returns/">Delivery &amp; returns</a> · <a href="/terms/">Terms</a> · <a href="/privacy/">Privacy</a></div></footer></body></html>"""
    out = os.path.join(PUB, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)

def crumbs(items):
    html_ = ' › '.join(f'<a href="{u}">{e(n)}</a>' if u else e(n) for n, u in items)
    ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, **({'item': SITE + u} if u else {})} for i, (n, u) in enumerate(items)]}
    return f'<div class="crumbs">{html_}</div>', ld

def card(p):
    lo, hi = prices(p)
    pr = ('From ' if lo != hi else '') + money(lo)
    return (f'<a class="card" href="{p["url"]}"><img src="/{p["img"].lstrip("/")}" alt="{e(p["t"])}" loading="lazy">'
            f'<b>{e(p["t"])}</b><span>{pr}{" · Sold out" if p["soldOut"] else ""}</span></a>')

STORE = {'@type': 'Store', 'name': 'Makkie Wholesalers', 'url': SITE + '/'}

# ---------- product pages ----------
for p in P:
    lo, hi = prices(p); t = p['t']
    imgs = []
    for v in p['variants']:
        for s in [v.get('img')] + list(v.get('gallery') or []):
            if s and s not in imgs: imgs.append(s)
    if p['img'] in imgs: imgs.remove(p['img'])
    imgs = [p['img']] + imgs
    show_opts = not (len(p['variants']) == 1 and p['variants'][0]['label'] in ('Standard', p['name']))
    rows = ''.join(f'<tr><td>{e(v["label"])}</td><td>{money(v["price"])}</td><td>{"<span class=so>Sold out</span>" if v["soldOut"] else "In stock"}</td></tr>'
                   for v in p['variants'] if v.get('price') is not None) if show_opts else ''
    size = p.get('size') or ''
    facts = ' · '.join(x for x in [('Size ' + size) if size else '', p['unit'] if p['unit'] not in ('unit', 'pair') else '', 'Code ' + p['id']] if x)
    cb, cld = crumbs([('Home', '/'), (p['group'], None), (cname(p['category']), CURL[p['category']]), (t, None)])
    buy = f'{SITE}/#p/{quote(p["id"])}'
    wa = f'https://wa.me/{WA}?text=' + quote(f"Hi, I'd like to order {t} ({p['id']})")
    others = [x for x in cats[p['category']] if x is not p][:8]
    body = (cb + f'<div class="prod"><div><img class="main" src="/{imgs[0].lstrip("/")}" alt="{e(t)}">'
            + (f'<div class="thumbs">' + ''.join(f'<img src="/{s.lstrip("/")}" alt="{e(t)}" loading="lazy">' for s in imgs[1:9]) + '</div>' if len(imgs) > 1 else '')
            + f'</div><div><h1>{e(t)}</h1><div class="code">{e(facts)}</div>'
            + f'<div class="price">{"From " if lo != hi else ""}{money(lo)}</div>'
            + ('<span class="so">Sold out</span>' if p['soldOut'] else '<span class="ins">In stock · delivery anywhere in South Africa</span>')
            + f'<div class="btns"><a class="btn buy" href="{buy}">Buy online</a><a class="btn wa" href="{wa}">Order on WhatsApp</a></div>'
            + f'<div class="desc">{e(p["d"])}</div>'
            + (f'<table><tr><th>Option</th><th>Price</th><th>Stock</th></tr>{rows}</table>' if rows else '')
            + (f'<div class="note">{e(p["note"])}</div>' if p.get('note') else '')
            + '<div class="note">Bulk and trade buyers: WhatsApp us for wholesale pricing. Prices include 15% VAT.</div></div></div>'
            + (f'<h2>More {e(cname(p["category"]))}</h2><div class="grid">{"".join(card(x) for x in others)}</div>' if others else ''))
    offers = [{'@type': 'Offer', 'sku': v['id'], 'name': v['label'], 'price': f'{v["price"]:.2f}', 'priceCurrency': 'ZAR',
               'availability': 'https://schema.org/' + ('OutOfStock' if v['soldOut'] else 'InStock'), 'url': SITE + p['url'],
               'itemCondition': 'https://schema.org/NewCondition', 'seller': STORE} for v in p['variants'] if v.get('price') is not None]
    prod = {'@context': 'https://schema.org', '@type': 'Product', 'name': t, 'sku': p['id'], 'description': p['d'],
            'image': [img_url(s) for s in imgs[:6]], 'category': p['category'].replace(' · ', ' > '), 'url': SITE + p['url'],
            'offers': offers[0] if len(offers) == 1 else {'@type': 'AggregateOffer', 'priceCurrency': 'ZAR', 'lowPrice': f'{lo:.2f}',
                      'highPrice': f'{hi:.2f}', 'offerCount': len(offers), 'offers': offers}}
    page(p['url'], f'{t} – {money(lo)}{"+" if lo != hi else ""} | Makkie Wholesalers', p['d'], body, [prod, cld], img=img_url(imgs[0]))

# ---------- category pages ----------
for c, items in cats.items():
    lo = min(prices(x)[0] for x in items); nm = cname(c)
    parent = c.split(' · ')[0] if ' · ' in c else None
    cb, cld = crumbs([('Home', '/'), (items[0]['group'], None)] + ([(parent, None)] if parent else []) + [(nm, None)])
    intro = (f'{len(items)} {nm} from {money(lo)} at Makkie Wholesalers, Marabastad, Pretoria. '
             'Wholesale and retail, with delivery anywhere in South Africa by PAXI to any PEP store or courier, or collect from our shop.')
    body = (cb + f'<h1>{e(nm)}</h1><p class="intro">{e(intro)}</p><div class="btns"><a class="btn buy" href="{SITE}/#c/{quote(c)}">Shop {e(nm)} online</a></div>'
            f'<div class="grid">{"".join(card(x) for x in items)}</div>')
    lst = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': nm,
           'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + x['url'], 'name': x['t']} for i, x in enumerate(items)]}
    page(CURL[c], f'{nm} – from {money(lo)} | Makkie Wholesalers, Pretoria', intro, body, [lst, cld], img=img_url(items[0]['img']))

# ---------- all products page ----------
body = '<h1>All products</h1><p class="intro">Everything we stock at Makkie Wholesalers in Marabastad, Pretoria: blankets, shawls, beads and traditional goods. Wholesale and retail, delivered anywhere in South Africa.</p>'
for g in GROUPS:
    gc = sorted([c for c in cats if cats[c][0]['group'] == g], key=str.lower)
    body += f'<h2>{e(g)}</h2><ul class="cats">' + ''.join(f'<li><a href="{CURL[c]}">{e(c.replace(" · ", " – "))}</a> ({len(cats[c])})</li>' for c in gc) + '</ul>'
for g in GROUPS:
    for c in sorted([c for c in cats if cats[c][0]['group'] == g], key=str.lower):
        body += f'<h2>{e(c.replace(" · ", " – "))}</h2><ul class="cats">' + ''.join(f'<li><a href="{x["url"]}">{e(x["t"])}</a></li>' for x in cats[c]) + '</ul>'
page('/products/', 'All products | Makkie Wholesalers – Blankets, Beads & Traditional Goods, Pretoria',
     'Every product at Makkie Wholesalers: Basotho, Ndebele and mink blankets, shawls, Czech and Chinese seed beads, traditional goods. Wholesale and retail, Marabastad, Pretoria.', body)

# ---------- policy pages (same text as the shop's Delivery & returns / Terms / Privacy pop-ups) ----------
cfg = h[h.index('const CONFIG = {'):]
def cval(key): return re.search(key + r":\s*'([^']*)'", cfg).group(1)
def cnum(key): return re.search(key + r":\s*([0-9.]+)", cfg).group(1)
SUBS = {'${CONFIG.business}': cval('business'), '${esc(CONFIG.address)}': cval('address'), '${CONFIG.email}': cval('email'),
        '${R(CONFIG.shipping.band1)}': 'R' + cnum('band1'), '${CONFIG.shipping.quoteOverKg}': cnum('quoteOverKg')}
POLICY = {'delivery': '/returns/', 'terms': '/terms/', 'privacy': '/privacy/'}
for pid, path in POLICY.items():
    m = re.search(pid + r": \{t: '([^']*)', h: \(\) => `(.*?)`\}", h, re.S)
    if not m: sys.exit('page not found: ' + pid)
    ttl, txt = m.group(1), m.group(2)
    for a, b in SUBS.items(): txt = txt.replace(a, e(b))
    if '${' in txt: sys.exit(f'unknown value in {pid} page: ' + txt[txt.index('${'):][:60])
    page(path, f'{ttl} | Makkie Wholesalers', re.sub(r'<[^>]+>|\s+', ' ', txt).strip()[:300],
         f'<div class="prod" style="display:block"><h1>{e(ttl)}</h1><div class="desc policy">{txt}</div></div>')

# ---------- sitemap, robots, feed, llms.txt ----------
urls = ['/', '/products/', '/returns/', '/terms/', '/privacy/'] + list(CURL.values()) + [p['url'] for p in P]
open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(PUB, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')

GPC = {'Blankets & Textiles': 'Home & Garden > Linens & Bedding > Bedding > Blankets', 'Beads': 'Arts & Entertainment > Hobbies & Creative Arts > Arts & Crafts > Art & Crafting Materials > Embellishments & Trims > Beads'}
items = []
for p in P:
    for v in p['variants']:
        if v.get('price') is None: continue
        lab = '' if v['label'] in ('Standard', p['name']) else ' – ' + v['label']
        items.append('<item>' + ''.join(f'<{t}>{xesc(str(x))}</{t}>' for t, x in [
            ('g:id', v['id']), ('g:item_group_id', p['id']), ('title', (p['t'] + lab)[:150]), ('description', p['d'][:5000]),
            ('link', SITE + p['url']), ('g:image_link', img_url(v.get('img') or p['img'])),
            ('g:availability', 'out_of_stock' if v['soldOut'] else 'in_stock'), ('g:price', f'{v["price"]:.2f} ZAR'),
            ('g:condition', 'new'), ('g:identifier_exists', 'no'), ('g:brand', 'Makkie Wholesalers'),
            ('g:product_type', p['category'].replace(' · ', ' > '))] + ([('g:google_product_category', GPC[p['group']])] if p['group'] in GPC else [])) + '</item>')
open(os.path.join(PUB, 'google-products.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0"><channel>'
    f'<title>Makkie Wholesalers</title><link>{SITE}/</link><description>Blankets, beads and traditional goods</description>\n' + '\n'.join(items) + '\n</channel></rss>\n')

llms = ['# Makkie Wholesalers', '',
        '> Wholesale and retail shop in Marabastad, Pretoria, South Africa, selling blankets (Basotho, Ndebele, Xhosa, mink, hotel and budget blankets), '
        'shawls and throws, Czech and Chinese glass seed beads, plastic beads, traditional and Ndebele goods, berets, hats, kangas and haberdashery. '
        'Online shop at https://makkies.co.za with delivery anywhere in South Africa (PAXI to any PEP store, or courier), or collect in store.', '',
        'Address: Unit D4, Pretoria Oriental Complex, Entrance 6, 7th Street, Marabastad, Pretoria. WhatsApp 072 323 5469 (+27 72 323 5469). '
        'Tel 012 323 5469. Email orders@makkies.co.za. Prices in South African rand, including 15% VAT. Bulk and trade buyers get wholesale pricing on request.', '',
        '## Categories', ''] + [f'- [{c.replace(" · ", " – ")}]({SITE}{CURL[c]}): {len(cats[c])} products from {money(min(prices(x)[0] for x in cats[c]))}'
                                for g in GROUPS for c in sorted([c for c in cats if cats[c][0]['group'] == g], key=str.lower)] + \
       ['', '## More', '', f'- [All products]({SITE}/products/)', f'- [Sitemap]({SITE}/sitemap.xml)', '']
open(os.path.join(PUB, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms))

# ---------- shop footer: crawlable link to the product list ----------
LINK = '<li><a class="flink" href="/products/">All products (list)</a></li>'
if LINK not in h:
    old = """<li><button class="flink" onclick="openPage('about')">About us</button></li>"""
    if h.count(old) != 1: sys.exit('footer not found')
    h = h.replace(old, old + '\n      ' + LINK)
    open(os.path.join(PUB, 'index.html'), 'w', encoding='utf-8').write(h)
print(f'{len(P)} product pages, {len(cats)} category pages, {len(urls)} sitemap URLs, {len(items)} feed items')
