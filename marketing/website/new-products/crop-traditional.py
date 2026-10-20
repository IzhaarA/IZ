import sys, json
from PIL import Image, ImageFilter, ImageDraw
# name: (centre x as fraction of width, centre y as fraction of height, square side as fraction of width)
CROPS = {
 'leopard_shell_large': (.52,.49,.68), 'leopard_shell_small': (.515,.52,.66), 'Ndoro_ceramic_disc': (.53,.54,.62),
 'cowrie_shells_1': (.55,.44,1.0), 'cowrie_shells_2': (.49,.475,1.14),
 'matte_gold_dimit_coins': (.565,.565,.62), 'matte_silver_dimit_coins': (.535,.55,.6),
 'shiny_gold_dimit_coins': (.6,.55,.5), 'shiny_silver_dimit_coins': (.6,.57,.58),
 'beaded_knob_stick': (.57,.47,.84), 'beaded_necklace_large': (.51,.5,1.02), 'beaded_necklace_medium': (.55,.52,.85),
 'beaded_necklace_small': (.5,.48,.78), 'mini_wooden_knob': (.5,.5,1.36), 'mini_wooden_spear': (.53,.51,1.36),
 'shell_belt': (.51,.51,1.3), 'ndebele_painted_axe_all': (.47,.44,1.12), 'ndebele_painted_axe_1': (.47,.43,.95),
 'ndebele_painted_axe_2': (.48,.41,.95), 'ndebele_painted_axe_3': (.48,.5,.96), 'poryan_animal_skin': (.55,.5,1.3),
 'mapoto_canvas_apron': (.5,.5,1.16), 'animal_fur_headband_1': (.5,.55,.74), 'animal_fur_headband_2': (.5,.51,1.18),
 'plain_wooden_axe': (.48,.46,.96), 'matseka_wire_leg_thick': (.55,.49,.74), 'matseka_wire_leg_thin': (.53,.42,.75),
 'animal_print_beret_beige_black': (.515,.44,.95), 'animal_print_beret_white_black': (.505,.415,.93),
 'beaded_neck_ring_and_tie_chinese': (.5,.52,1.26),
 'matseka_wire_bangle_hand_thick': (.57,.48,.78), 'matseka_wire_bangle_hand_thin': (.55,.475,.76),
 'stretchy_matseka_bangle_12pkt_maroon': (.5,.42,.82), 'stretchy_matseka_bangle_gold': (.56,.455,.72), 'stretchy_matseka_bangle_silver': (.565,.45,.72),
}
# dark table edges in the photo: (side, width fraction) replaced by the plain background next to them
CLEAN = {'shell_belt': [('l', .05), ('r', .1)], 'poryan_animal_skin': [('l', .1), ('r', .08)], 'mapoto_canvas_apron': [('l', .05)], 'beaded_neck_ring_and_tie_chinese': [('l', .04), ('r', .07)]}
ROT = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
def clean(im, edges):
    W, H = im.size
    for side, f in edges:
        w = int(f * W); e = max(6, W // 40)
        if side == 'l': im.paste(im.crop((w, 0, w + e, H)).resize((w, H)).filter(ImageFilter.GaussianBlur(8)), (0, 0))
        else: im.paste(im.crop((W - w - e, 0, W - w, H)).resize((w, H)).filter(ImageFilter.GaussianBlur(8)), (W - w, 0))
    return im
def crop(im, cx, cy, side):
    W, H = im.size; s = int(side * W); x0 = int(cx * W - s / 2); y0 = int(cy * H - s / 2)
    pl, pt, pr, pb = max(0, -x0), max(0, -y0), max(0, x0 + s - W), max(0, y0 + s - H)
    if pl or pt or pr or pb:
        big = Image.new('RGB', (W + pl + pr, H + pt + pb)); big.paste(im, (pl, pt))
        e = max(6, W // 40)
        if pl: big.paste(im.crop((0, 0, e, H)).resize((pl, H)).filter(ImageFilter.GaussianBlur(8)), (0, pt))
        if pr: big.paste(im.crop((W - e, 0, W, H)).resize((pr, H)).filter(ImageFilter.GaussianBlur(8)), (pl + W, pt))
        if pt: big.paste(big.crop((0, pt, big.width, pt + e)).resize((big.width, pt)).filter(ImageFilter.GaussianBlur(8)), (0, 0))
        if pb: big.paste(big.crop((0, pt + H - e, big.width, pt + H)).resize((big.width, pb)).filter(ImageFilter.GaussianBlur(8)), (0, pt + H))
        im = big; x0 += pl; y0 += pt
    return im.crop((x0, y0, x0 + s, y0 + s))
src, out = sys.argv[1], sys.argv[2]
order = open(f'{src}/../order.txt').read().split()
for n in order:
    cx, cy, side = CROPS[n]
    im = Image.open(f'{src}/{n}.jpg').convert('RGB')
    if n in CLEAN: im = clean(im, CLEAN[n])
    c = crop(im, cx, cy, side).resize((1000, 1000), Image.LANCZOS)
    if n in ROT: c = c.rotate(-ROT[n], expand=False)
    c.save(f'{out}/{n}.jpg', quality=90)
# numbered sheets, 15 per sheet
for k in range(0, len(order), 15):
    sh = Image.new('RGB', (5 * 250 + 60, 3 * 280 + 20), 'white'); d = ImageDraw.Draw(sh)
    for i, n in enumerate(order[k:k + 15]):
        t = Image.open(f'{out}/{n}.jpg').resize((240, 240)); x, y = 10 + (i % 5) * 260, 10 + (i // 5) * 280
        sh.paste(t, (x, y)); d.rectangle([x, y, x + 34, y + 24], fill='black'); d.text((x + 6, y + 6), str(k + i + 1), fill='white')
        d.text((x, y + 246), n.replace('_', ' ')[:38], fill='black')
    rows = (len(order[k:k + 15]) + 4) // 5; sh = sh.crop((0, 0, sh.width, rows * 280 + 20))
    sh.save(f'{out}/../crops-{k // 15 + 1}.jpg', quality=88)
