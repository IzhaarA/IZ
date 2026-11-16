# Printable shop sign + small handout cards with a QR code to the website.
# python3 make_sign.py && node print.cjs   -> makkies-shop-sign-A4.pdf/.png, makkies-qr-cards-A4.pdf/.png
import qrcode, base64, io
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
URL = 'https://makkies.co.za/?src=shop-sign'
def qr_png(url):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=24, border=2); q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color='#1d1b19', back_color='white').convert('RGB')
    lg = Image.open('mw.png').convert('RGBA'); w = im.width // 4; lg.thumbnail((w, w))
    pad = Image.new('RGB', (lg.width + 28, lg.height + 28), 'white')
    x, y = (im.width - pad.width) // 2, (im.height - pad.height) // 2; im.paste(pad, (x, y)); im.paste(lg, (x + 14, y + 14), lg)
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
QR = qr_png(URL); QRC = qr_png('https://makkies.co.za/?src=qr-card')
CSS = open('fonts.css').read() + """
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}body{font-family:Inter,Arial,sans-serif;color:#1d1b19;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.stripe{background:linear-gradient(90deg,#45203F 0 12%,#F2B90D 12% 30%,#1D339E 30% 46%,#DA2C28 46% 62%,#0A7A44 62% 74%,#DA2C28 74% 84%,#F2B90D 84% 96%,#45203F 96%)}
"""
SIGN = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
.page{{width:210mm;height:297mm;position:relative;background:#fff;overflow:hidden;display:flex;flex-direction:column;align-items:center}}
.top{{width:100%;height:9mm;flex:none}}.bot{{position:absolute;left:0;right:0;bottom:0;height:9mm}}
.logo{{width:112mm;margin-top:11mm}}
.eb{{margin-top:7mm;background:#C3312B;color:#fff;font-weight:800;letter-spacing:.18em;font-size:15pt;padding:2.5mm 7mm;border-radius:2mm}}
h1{{font-size:50pt;line-height:1;font-weight:900;letter-spacing:-.02em;margin-top:6mm;text-align:center}}
h1 em{{font-style:normal;color:#C3312B}}
.sub{{font-size:16pt;color:#4a443e;margin-top:4mm;text-align:center}}
.qrbox{{margin-top:7mm;border:2.2mm solid #1d1b19;border-radius:7mm;padding:5mm;background:#fff;position:relative}}
.qrbox img{{width:84mm;height:84mm;display:block}}
.scan{{position:absolute;left:50%;bottom:-6mm;transform:translateX(-50%);background:#1d1b19;color:#fff;font-weight:800;font-size:14pt;letter-spacing:.06em;padding:2mm 6mm;border-radius:10mm;white-space:nowrap}}
.url{{margin-top:11mm;font-size:32pt;font-weight:900;letter-spacing:-.01em}}
.pts{{display:flex;gap:6mm;margin-top:6mm}}.pts div{{border:.6mm solid #e2dbd0;border-radius:4mm;padding:4mm 5mm;width:56mm;text-align:center;font-size:11.5pt;color:#4a443e;line-height:1.35}}
.pts b{{display:block;color:#1d1b19;font-size:13pt;margin-bottom:1mm}}
.wa{{margin-top:6mm;font-size:16pt;font-weight:700}}.wa span{{color:#0A7A44}}
</style></head><body><div class="page"><div class="top stripe"></div>
<img class="logo" src="logo.png"><div class="eb">NEW · SHOP ONLINE 24/7</div>
<h1>Shop from your<br><em>phone</em></h1>
<div class="sub">Blankets, beads &amp; traditional goods, any time</div>
<div class="qrbox"><img src="{QR}"><div class="scan">SCAN WITH YOUR CAMERA</div></div>
<div class="url">makkies.co.za</div>
<div class="pts"><div><b>We deliver</b>Anywhere in South Africa: courier or PAXI</div><div><b>Pay safely</b>Card, Instant EFT or SnapScan</div><div><b>Bulk prices</b>Stock price on 10 pieces or more</div></div>
<div class="wa">Questions? WhatsApp <span>072 323 5469</span></div>
<div class="bot stripe"></div></div></body></html>"""
card = f"""<div class="card"><div class="cs stripe"></div><img class="cl" src="logo.png"><div class="ct">Shop online, any time</div>
<img class="cq" src="{QRC}"><div class="cu">makkies.co.za</div><div class="cd">Delivery across SA · Card, EFT, SnapScan</div><div class="cw">WhatsApp 072 323 5469</div></div>"""
CARDS = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
.page{{width:210mm;height:297mm;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}}
.card{{border:.3mm dashed #b9b0a5;display:flex;flex-direction:column;align-items:center;position:relative;padding-top:9mm}}
.cs{{position:absolute;top:0;left:0;right:0;height:4mm}}.cl{{width:70mm;margin-top:3mm}}.ct{{font-size:17pt;font-weight:900;margin-top:4mm}}
.cq{{width:62mm;height:62mm;margin-top:4mm}}.cu{{font-size:20pt;font-weight:900;margin-top:2mm}}.cd{{font-size:9.5pt;color:#4a443e;margin-top:2mm}}.cw{{font-size:11pt;font-weight:700;color:#0A7A44;margin-top:2mm}}
</style></head><body><div class="page">{card * 4}</div></body></html>"""
open('sign.html', 'w').write(SIGN); open('cards.html', 'w').write(CARDS); print('ok')
