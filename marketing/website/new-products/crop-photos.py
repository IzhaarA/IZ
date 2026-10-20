import sys, json
from PIL import Image, ImageFilter
# name: (centre x as fraction of width, centre y as fraction of height, square side as fraction of width)
CROPS = {
 'army_navy_needles_1': (.55,.44,.89), 'army_navy_needles_2': (.56,.495,1.27), 'upholstery_needles': (.5,.49,1.0),
 'measuring_tape': (.51,.43,.98), 'thick_needle_12cm': (.56,.43,.82), 'block_hand_towel': (.545,.505,1.32),
 'colibri_guest_towel_1': (.5625,.49,.88), 'colibri_guset_towel_2': (.525,.47,.98), 'colibri_guset_towel_3': (.525,.415,.93),
 'dice_100pkt_5mm': (.565,.405,.82), 'dice_100pkt_9mm': (.54,.435,.82), 'dice_20pkt': (.56,.405,.68),
 'shirring_elastic_black_10g': (.485,.47,.68), 'shirring_elastic_white_10g': (.535,.475,.6), 'shirring_elastic_black_30m': (.475,.435,.56),
 'shirring_elastic_white_30m_1': (.51,.475,.66), 'shirring_elastic_white_30m_2': (.41,.385,.66), 'sisal_dry_twine': (.435,.425,.98),
 'sisal_dry_twine_2': (.5,.4,.97), 'springtime_black_500g': (.525,.465,1.06), 'springtime_black_500g_2': (.5,.54,.94),
 'springtime_white_500g': (.515,.435,1.16), 'springtime_white_500g_2': (.49,.365,.9), 'smoking_pipe_1': (.51,.435,1.0),
 'smoking_pipe_2': (.485,.455,1.22), 'blanket_pins_45mm_new': (.51,.48,1.05), 'blanket_pins_80mm_new': (.51,.47,.99),
 'ideel_black_cotton_new': (.515,.485,1.12), 'ideel_white_cotton_new': (.5,.485,1.08), 'new_zcc_green_beret': (.505,.5,1.06),
 'new_zcc_green_beret_2': (.505,.42,1.0), 'police_whistle_new': (.565,.47,.78),
}
ROT = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
def crop(im, cx, cy, side):
    W, H = im.size; s = int(side * W); x0 = int(cx * W - s / 2); y0 = int(cy * H - s / 2)
    pl, pt, pr, pb = max(0, -x0), max(0, -y0), max(0, x0 + s - W), max(0, y0 + s - H)
    if pl or pt or pr or pb:                       # extend the plain background by stretching the edges, softly blurred
        big = Image.new('RGB', (W + pl + pr, H + pt + pb)); big.paste(im, (pl, pt))
        e = max(6, W // 40)
        if pl: big.paste(im.crop((0, 0, e, H)).resize((pl, H)).filter(ImageFilter.GaussianBlur(8)), (0, pt))
        if pr: big.paste(im.crop((W - e, 0, W, H)).resize((pr, H)).filter(ImageFilter.GaussianBlur(8)), (pl + W, pt))
        if pt: big.paste(big.crop((0, pt, big.width, pt + e)).resize((big.width, pt)).filter(ImageFilter.GaussianBlur(8)), (0, 0))
        if pb: big.paste(big.crop((0, pt + H - e, big.width, pt + H)).resize((big.width, pb)).filter(ImageFilter.GaussianBlur(8)), (0, pt + H))
        im = big; x0 += pl; y0 += pt
    return im.crop((x0, y0, x0 + s, y0 + s))
src, out = sys.argv[1], sys.argv[2]
for n, (cx, cy, side) in CROPS.items():
    im = Image.open(f'{src}/{n.rstrip("_")}.jpg').convert('RGB')
    c = crop(im, cx, cy, side).resize((1000, 1000), Image.LANCZOS)
    if n in ROT: c = c.rotate(-ROT[n], expand=False)
    c.save(f'{out}/{n.rstrip("_")}.jpg', quality=90)
