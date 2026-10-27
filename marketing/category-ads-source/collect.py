"""Collects the website photos and product details for the category ads into ../instagram/source/ph and ads.json.
Usage: python3 collect.py <site index.html> <site images folder>"""
import json, sys, os, re, colorsys
from PIL import Image, ImageDraw, ImageFilter
H = os.path.dirname(os.path.abspath(__file__)); PH = os.path.join(H, '..', 'instagram', 'source', 'ph')
h = open(sys.argv[1]).read(); k = 'const PRODUCTS = '; P = json.JSONDecoder().raw_decode(h[h.index(k) + len(k):])[0]
SOLD = set(json.loads(re.search(r'SOLD_OUT\s*=\s*(\[[^\]]*\])', h).group(1)))
by = {p['id']: p for p in P}

def img(src, name, pad=False):               # site photo -> ph/<name>.jpg; pad=True makes a tall photo square so the frame doesn't crop it
    im = Image.open(os.path.join(sys.argv[2], os.path.basename(src))).convert('RGB')
    w, hh = im.size
    if pad and abs(w - hh) > max(w, hh) * .1:  # tall or wide photo: stretch its own edges (softly blurred) to make it square
        n = max(w, hh); sq = Image.new('RGB', (n, n)); x0, y0 = (n - w) // 2, (n - hh) // 2; e = max(6, min(w, hh) // 40)
        if x0:
            sq.paste(im.crop((0, 0, e, hh)).resize((x0, hh)).filter(ImageFilter.GaussianBlur(10)), (0, 0))
            sq.paste(im.crop((w - e, 0, w, hh)).resize((n - w - x0, hh)).filter(ImageFilter.GaussianBlur(10)), (x0 + w, 0))
        if y0:
            sq.paste(im.crop((0, 0, w, e)).resize((w, y0)).filter(ImageFilter.GaussianBlur(10)), (0, 0))
            sq.paste(im.crop((0, hh - e, w, hh)).resize((w, n - hh - y0)).filter(ImageFilter.GaussianBlur(10)), (0, y0 + hh))
        sq.paste(im, (x0, y0)); im = sq
    im.save(os.path.join(PH, name + '.jpg'), quality=90); return im
def tones(im):                               # page tint and text colour taken from the middle of the photo
    w, hh = im.size; c = im.crop((w * 3 // 10, hh * 3 // 10, w * 7 // 10, hh * 7 // 10)).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    hh_, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c])
    tint = colorsys.hls_to_rgb(hh_, .88, min(s, .45)); ink = colorsys.hls_to_rgb(hh_, .22, min(.9, s + .15))
    hx = lambda t: '#%02x%02x%02x' % tuple(int(x * 255) for x in t); return hx(tint), hx(ink)
def fan(names, out, card=380):               # fanned photo cards for the carousel cover
    n = len(names); W = card + (n - 1) * int(card * .55) + 260; cv = Image.new('RGBA', (W, card + 300), (0, 0, 0, 0))
    for i, nm in enumerate(names):
        ph = Image.open(os.path.join(PH, nm + '.jpg')).convert('RGB').resize((card, card), Image.LANCZOS)
        fr = Image.new('RGBA', (card + 24, card + 24), (255, 255, 255, 255)); fr.paste(ph, (12, 12))
        m = Image.new('L', fr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fr.width - 1, fr.height - 1), 26, fill=255); fr.putalpha(m)
        r = (i - (n - 1) / 2) * -7; fr = fr.rotate(r, expand=True, resample=Image.BICUBIC)
        sh = Image.new('RGBA', fr.size, (0, 0, 0, 0)); sh.putalpha(fr.getchannel('A').point(lambda a: a * .35)); sh = sh.filter(ImageFilter.GaussianBlur(16))
        x = 130 + i * int(card * .55) - (fr.width - card) // 2; y = 120 + int(abs(i - (n - 1) / 2) ** 1.6 * 14) - (fr.height - card) // 2
        cv.alpha_composite(Image.composite(Image.new('RGBA', sh.size, (0, 0, 0, 255)), Image.new('RGBA', sh.size, (0, 0, 0, 0)), sh.getchannel('A')), (x + 10, y + 24))
        cv.alpha_composite(fr, (x, y))
    cv.crop(cv.getbbox()).save(os.path.join(PH, out + '.png'))

ADS = {}
PHOTO = {'CH-49': 'images/fd6771443e59.jpg',          # Black Chinese beads: the 8/0 packet photo looks better
         'TRB-011': 'images/c0b051ba921c.jpg', 'TRB-012': 'images/7a9886a68352.jpg'}   # Seanamarena, Victoria: worn, not the flat design
def add(key, items, fan_names):
    for it in items: it['tint'], it['ink'] = tones(Image.open(os.path.join(PH, it['img'] + '.jpg')))
    fan(fan_names, key + '_fan'); ADS[key] = items

def simple(key, ids, label=lambda p: p['name'], pad=False):
    out = []
    for pid in ids:
        p = by[pid]
        if pid in SOLD: continue
        v = p['variants'][0]; nm = f"{key}_{pid.lower()}"; img(PHOTO.get(pid, v['img']), nm, pad)
        out.append(dict(id=pid, name=label(p), img=nm, price=min(x['price'] for x in p['variants']),
                        size=p.get('size') or '', multi=len(p['variants']) > 1, desc=p.get('desc', ''), labels=[x['label'] for x in p['variants']], varies=len({x['price'] for x in p['variants']}) > 1))
    return out

cat = lambda c: [p['id'] for p in P if p['category'] == c]
# beaded accessories: each necklace + the 5 colours of the necklace & bangle set
ba = simple('ba', ['TRD-010', 'TRD-011', 'TRD-012', 'TRD-023'], lambda p: p['name'].replace('Beaded Necklace — ', '').replace('Beaded ', ''))
for v in by['TRD-031']['variants']:
    nm = 'ba_set_' + v['id'].split('-')[-1]; img(v['img'], nm)
    ba.append(dict(id='TRD-031', name=v['label'], img=nm, price=v['price'], size='Necklace + bangle', set=True))
add('beaded', ba, [ba[i]['img'] for i in (4, 0, 3, 2, 6)])
hats = simple('hat', [i for i in cat('Hats · Ndebele Hats') if i != 'NDH-006'],   # the hats video was made while the beaded hat was sold out
             lambda p: p['name'].replace('Ndebele Painted ', 'Painted ').replace('Ndebele ', ''))
add('hats', hats, [x['img'] for x in hats[:6]])
for key, c in (('cloudsoft', 'Shawls & Throws · Cloudsoft Shawls'), ('chenille', 'Shawls & Throws · Chenille Throws'), ('plainsh', 'Shawls & Throws · Plain Shawls')):
    its = simple(key, cat(c)); add(key, its, [x['img'] for x in its[:7]])
wool = simple('wool', cat('Haberdashery · Wool')); add('wool', wool, [x['img'] for x in wool[::3][:7]])
TOWEL = {'TWL-001': 'Face Cloths', 'TWL-002': 'White Bath Sheet', 'TWL-003': 'Block Bath Towel'}
tw = simple('towel', cat('Towels'), lambda p: TOWEL.get(p['id'], p['name'].replace('Colibri Guest Towel — ', 'Guest Towel · '))); add('towels', tw, [x['img'] for x in (tw[3], tw[2], tw[1], tw[4], tw[5])])
nd = simple('nd', cat('Traditional Ndebele Accessories'))
for v in by['TRD-016']['variants']:                     # painted axe colours for the colour set
    nm = 'nd_axe_' + v['id'].split('-')[-1]; img(v['img'], nm); nd.append(dict(id='TRD-016', name=v['label'], img=nm, price=v['price'], size='40cm', set=True))
add('ndebele', nd, [nd[i]['img'] for i in (4, 7, 2, 9, 11, 6)])
bg = simple('bg', cat('Bangles'), pad=True); add('bangles', bg, [bg[i]['img'] for i in (0, 9, 5, 3, 13, 1)])
ct = simple('ct', cat('Haberdashery · Cotton & Twine')); add('cotton', ct, [ct[i]['img'] for i in (6, 7, 4, 9, 16, 15)])
mk = simple('mk', cat('Mink Blankets')); add('mink', mk, [mk[i]['img'] for i in (0, 3, 6, 11, 13, 15)])
pref = lambda c: [p['id'] for p in P if p['category'].startswith(c)]
ch = simple('ch', pref('Chinese Glass')); add('chinese', ch, [ch[i]['img'] for i in (4, 12, 18, 25, 30, 36)])
cz = simple('cz', pref('Czech Glass')); add('czech', cz, [cz[i]['img'] for i in range(0, 42, 7)])
p3 = simple('p3', cat('Plastic Beads · 3mm Round')); add('plastic3', p3, [p3[i]['img'] for i in (4, 3, 7, 8, 0)])
p6 = simple('p6', cat('Plastic Beads · 6mm Round')); add('plastic6', p6, [p6[i]['img'] for i in (6, 7, 5, 10, 2, 33)])
po = simple('po', cat('Plastic Beads · 8mm Oval')); add('plasticoval', po, [po[i]['img'] for i in (1, 4, 3, 8, 0)])
# December ceremonies (27 Oct 2026)
bs = simple('bs', cat('Tribal Blankets · Basotho')); add('basotho', bs, [bs[i]['img'] for i in (4, 6, 7, 10, 11, 13)])
um = simple('um', ['MNK-014', 'MNK-011', 'TRB-027', 'TRB-023', 'SHW-011', 'SHW-015', 'CSH-001', 'PSH-021'])
add('umembeso', um, [um[i]['img'] for i in (0, 2, 4, 3, 1)])
xh = simple('xh', ['RUG-002', 'RUG-001', 'RUG-003'])
for v in by['TRB-029']['variants']:                   # Xhosa stripe blanket colours for the colour set
    nm = 'xh_stripe_' + v['id'].split('-')[-1]; img(v['img'], nm); xh.append(dict(id='TRB-029', name=v['label'], img=nm, price=v['price'], size='', set=True))
add('xhosa', xh, [xh[i]['img'] for i in (3, 0, 4, 1, 5)])
kg = simple('kg', [i for i in cat('Kangas') if i not in ('KNG-001', 'KNG-002', 'KNG-004', 'KNG-011')], pad=True)
add('kangas', kg, [kg[i]['img'] for i in (1, 3, 8, 4, 12)])
json.dump(ADS, open(os.path.join(H, 'ads.json'), 'w'), indent=1, ensure_ascii=False)
print({k: len(v) for k, v in ADS.items()})
