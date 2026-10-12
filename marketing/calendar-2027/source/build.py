"""Generate Makkie Wholesalers 2027 mini wall calendar variants (same layout as the 2026 print file)."""
import calendar, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = 2027
SOC = "#fff"  # colour of the website/socials/WhatsApp lines
BLANK = True  # leave dates, holidays and school terms empty for the publisher
calendar.setfirstweekday(6)  # Sunday first

HOLIDAYS = {(1, 1), (3, 21), (3, 22), (3, 26), (3, 29), (4, 27), (5, 1), (6, 16),
            (8, 9), (9, 24), (12, 16), (12, 25), (12, 26), (12, 27)}
HOL_COL1 = [("01 JAN", "NEW YEAR'S DAY"), ("21 MAR", "HUMAN RIGHTS DAY"), ("22 MAR", "PUBLIC HOLIDAY"),
            ("26 MAR", "GOOD FRIDAY"), ("29 MAR", "FAMILY DAY"), ("27 APR", "FREEDOM DAY"), ("01 MAY", "WORKERS' DAY")]
HOL_COL2 = [("16 JUN", "YOUTH DAY"), ("09 AUG", "NATIONAL WOMEN'S DAY"), ("24 SEP", "HERITAGE DAY"),
            ("16 DEC", "DAY OF RECONCILIATION"), ("25 DEC", "CHRISTMAS DAY"), ("26 DEC", "DAY OF GOODWILL"),
            ("27 DEC", "PUBLIC HOLIDAY")]
TERMS = [("1", "(11) 13 JANUARY", "19 MARCH"), ("2", "06 APRIL", "25 JUNE"),
         ("3", "20 JULY", "22 SEPTEMBER"), ("4", "05 OCTOBER", "08 (10) DECEMBER")]

THEMES = {
    "gold26": None,
    "gold":  dict(bg="#C0911E", accent="#C79521", dark="#231F20", grid="#F1E5C7", sun="#ECE9E0", fade="#EEDCB3", termtxt="#231F20"),
    "red":   dict(bg="#B8272A", accent="#F2B705", dark="#231F20", grid="#FBEFE0", sun="#EFE6E0", fade="#F3D9D2", termtxt="#231F20"),
    "blue":  dict(bg="#1F4FB4", accent="#FFC814", dark="#14152B", grid="#EAF0FB", sun="#DDE3EE", fade="#D5E0F5", termtxt="#14152B"),
    "green": dict(bg="#128A4F", accent="#FFC814", dark="#1C2420", grid="#EAF5EC", sun="#DCE8DF", fade="#D3EBDB", termtxt="#1C2420"),
}
PHOTOS = {
    "gold26": ["basotho_stack", "hat", "checks", "berets_o", "wedding_shawl", "ndebele_cape",
               "wool", "mohair_o", "sticks_o", "tekkies_o", "beadstrands", "neckrings"],
    "gold":  ["ndebele_women", "chinese", "hero", "chenille", "hat", "kangas",
              "czech", "ndebele_cape", "berets_w", "mink_w", "plastic", "sticks_w"],
    "red":   ["basotho_stack", "polymohair", "neckrings", "tekkies_w", "beadstrands", "haberdash",
              "hero", "wool", "ndebele_women", "mink_o", "czech", "berets_o"],
    "blue":  ["ndebele_cape", "chenille", "hat", "chinese", "sticks_o", "kangas",
              "basotho_stack", "plastic", "tekkies_o", "polymohair", "neckrings", "mink_w"],
    "green": ["hero", "beadstrands", "tekkies_w", "mohair_o", "haberdash", "berets_w",
              "ndebele_women", "checks", "czech", "wool", "sticks_w", "mink_o"],
}
POS = {"tekkies_w": "center 60%", "hero": "center 45%", "ndebele_women": "center 30%", "sticks_w": "center 40%",
       "neckrings": "center 40%", "ndebele_cape": "center 35%"}

def icon(name, color="#fff"):
    svg = open(os.path.join(HERE, "icons", name + ".svg")).read()
    return svg.replace("<svg ", f'<svg fill="{color}" class="ic" ', 1)

def header(theme, logo):
    if logo == "old":
        f = "banner_colour.png" if theme == "gold26" else ("banner.png" if theme == "gold" else "banner_light.png")
        return f'<img id="banner" src="assets/{f}">'
    return '<img id="banner" src="assets/banner_newlogo.png">'

def month_block(m, th):
    weeks = calendar.monthcalendar(YEAR, m)
    if len(weeks) == 6:  # wrap 6th week into first row, as on the 2026 calendar
        extra = weeks.pop()
        weeks[0] = [e if e else f for f, e in zip(weeks[0], extra)]
    cells = []
    for r, wk in enumerate([] if BLANK else weeks):
        for c, d in enumerate(wk):
            if not d:
                continue
            cls = "red" if (c == 0 or (m, d) in HOLIDAYS) else ("sat" if c == 6 else "")
            cells.append(f'<span class="d {cls}" style="left:{c*20.82:.2f}pt;top:{r*16.4:.2f}pt">{d}</span>')
    names = "".join(f'<span style="left:{i*20.82:.2f}pt">{n}</span>' for i, n in enumerate(["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]))
    return f'''<div class="mb">
  <div class="mh"><svg class="mhsvg" viewBox="0 0 145.7 19" preserveAspectRatio="none">
    <polygon points="0,0 106,0 112,19 0,19" fill="{th['dark']}"/>
    <polygon points="9,0 13,0 19,19 15,19" fill="{th['accent']}"/>
    <polygon points="106,0 145.7,0 145.7,19 112,19" fill="{th['dark']}"/>
    <polyline points="104,1.2 145.7,1.2" stroke="{th['accent']}" stroke-width="1.1" fill="none"/>
    <polyline points="104,1.2 110.5,18.5" stroke="{th['accent']}" stroke-width="1.1" fill="none"/>
  </svg>
  <div class="mn">{calendar.month_name[m].upper()}</div><div class="my">{YEAR}</div></div>
  <div class="dn">{names}</div>
  <div class="gr"><div class="sunc"></div>{''.join(cells)}</div>
</div>'''

def build(theme, logo="old"):
    th = THEMES[theme] or THEMES["gold"]
    photos = PHOTOS[theme]
    rows = [186.4, 286.5, 644.5, 744.5]
    ph = []
    for i, p in enumerate(photos):
        r, c = divmod(i, 3)
        pos = POS.get(p, "center")
        cap = '<div class="cap">Wedding Shawl</div>' if p == "wedding_shawl" else ""
        ph.append(f'<div class="ph" style="left:{54.3+c*157.67:.2f}pt;top:{rows[r]}pt;background-image:url(assets/{p}.jpg);background-position:{pos}">{cap}</div>')
    mrows, mcols = [386.6, 515.5, 844.6, 973.5], [54.3, 218.0, 381.7]
    months = []
    for i in range(12):
        r, c = divmod(i, 3)
        months.append(f'<div style="position:absolute;left:{mcols[c]}pt;top:{mrows[r]}pt">{month_block(i+1, th)}</div>')
    hol = lambda col: "".join(f'<div class="hr"><span class="hd">{d}</span><span class="hdash">-</span><span>{n}</span></div>' for d, n in col)
    terms = "".join(f'<div class="tr"><span class="tn">{n}</span><span class="ts">{a}</span><span class="hdash">-</span><span>{b}</span></div>' for n, a, b in TERMS)
    logos = [("aranda", 54.3, 91.0, 36.0), ("preciosa", 160.7, 76.9, 41.1), ("lamberet", 254.5, 57.6, 43.6),
             ("indulge", 323.0, 90.8, 45.0), ("sesli", 423.6, 103.7, 35.0)]
    logo_html = "".join(f'<img class="lg" src="assets/{n}.png" style="left:{x}pt;top:1187.4pt;width:{w}pt;height:{h}pt">' for n, x, w, h in logos)
    marks = []
    for x in (0, 583.937):
        for y in (0, 1250.079):
            sx = -1 if x == 0 else 1
            sy = -1 if y == 0 else 1
            marks.append(f'<div class="cm" style="left:{45+min(x+sx*12, x+sx*32):.3f}pt;top:{45+y-0.125:.3f}pt;width:20pt;height:0.25pt"></div>')
            marks.append(f'<div class="cm" style="left:{45+x-0.125:.3f}pt;top:{45+min(y+sy*12, y+sy*32):.3f}pt;width:0.25pt;height:20pt"></div>')
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/local.css">
<style>
@page {{ size: 673.937pt 1340.079pt; margin: 0 }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:673.937pt;height:1340.079pt;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
#trim{{position:absolute;left:45pt;top:45pt;width:583.937pt;height:1250.079pt;font-family:Montserrat,sans-serif;color:{th['dark']}}}
#bg{{position:absolute;left:-9pt;top:-9pt;right:-9pt;bottom:-9pt;background:linear-gradient(180deg,{th['bg']} 0%,{th['bg']} 80.5%,{th['fade']} 88%,#fff 95%,#fff 100%)}}
#panel{{position:absolute;left:33.65pt;top:24.29pt;width:515.4pt;height:1240pt;border:3pt solid #fff;border-bottom:none}}
.cm{{position:absolute;background:#000}}
#banner{{position:absolute;left:35.7pt;top:27.6pt;width:512.4pt;height:93.6pt}}
#addr{{position:absolute;left:45.7pt;top:135pt;font-family:Tinos,serif;font-weight:700;font-size:12.6pt;line-height:13.4pt;color:#fff}} #addr .wa{{color:{SOC}}}
#year{{position:absolute;left:190pt;width:172pt;top:117pt;text-align:center;font-family:Fredoka,sans-serif;font-weight:700;font-size:62pt;line-height:1;color:#fff;-webkit-text-stroke:3.2pt #231F20;paint-order:stroke fill;letter-spacing:1pt}}
#soc{{position:absolute;left:363pt;top:128pt;font-family:Tinos,serif;font-weight:700;font-size:12.6pt;line-height:14pt;color:{SOC}}}
#soc div{{display:flex;align-items:center;gap:3.2pt;white-space:nowrap;margin-bottom:3pt}}
.ic{{width:10.5pt;height:10.5pt;flex:none}}
#addr .ic{{width:10pt;height:10pt;vertical-align:-1.2pt;margin-right:2pt}}
.ph{{position:absolute;width:157.67pt;height:91.7pt;background-size:cover;background-repeat:no-repeat}}
.mb{{position:relative;width:145.7pt;height:114.8pt}}
.mh{{position:absolute;left:0;top:2.9pt;width:145.7pt;height:19pt}}
.mhsvg{{position:absolute;inset:0;width:100%;height:100%}}
.mn{{position:absolute;left:14pt;width:92pt;top:0;height:19pt;line-height:19.5pt;text-align:center;color:#fff;font-weight:800;font-size:10.6pt;letter-spacing:.4pt}}
.my{{position:absolute;left:110pt;width:35.7pt;top:0;height:19pt;line-height:20pt;text-align:center;color:{th['accent']};font-weight:800;font-size:10.6pt}}
.dn{{position:absolute;left:0;top:21.4pt;width:145.7pt;height:11.6pt;background:{th['grid']};border-bottom:.6pt solid {th['dark']}}}
.dn span{{position:absolute;top:0;width:20.82pt;text-align:center;font-size:6.3pt;line-height:11.4pt;font-weight:500}}
.gr{{position:absolute;left:0;top:33pt;width:145.7pt;height:81.8pt;background:{th['grid']}}}
.sunc{{position:absolute;left:0;top:0;width:20.82pt;height:100%;background:{th['sun']}}}
.d{{position:absolute;width:20.82pt;height:16.4pt;line-height:16.4pt;padding-top:1.4pt;text-align:center;font-size:10.4pt;font-weight:700;color:#231F20}}
.d.red{{color:#E1251B}} .d.sat{{color:#6E6B67}}
#hb{{position:absolute;left:54.3pt;top:1106.2pt;width:473pt;height:72.9pt}}
#hbsvg{{position:absolute;inset:0;width:100%;height:100%}}
#ht{{position:absolute;left:62pt;width:200pt;top:4pt;text-align:center;color:#fff;font-weight:700;font-size:9.4pt;letter-spacing:.3pt}}
.hc{{position:absolute;top:17.5pt;color:#fff;font-size:5pt;line-height:6.6pt;font-weight:500}}
.hr{{display:flex;white-space:nowrap}} .hd{{display:inline-block;width:19pt;text-align:right}} .hdash{{display:inline-block;width:8pt;text-align:center}}
#tt{{position:absolute;left:283pt;width:190pt;top:2.5pt;text-align:center;color:{th['termtxt']};font-weight:700;font-size:9.4pt}}
#ts{{position:absolute;left:283pt;width:190pt;top:14.5pt;text-align:center;color:{th['termtxt']};font-weight:700;font-size:6.2pt}}
#terms{{position:absolute;left:300pt;top:26.5pt;color:{th['termtxt']};font-size:5.9pt;line-height:7.5pt;font-weight:600}}
.tr{{display:flex;white-space:nowrap}} .tn{{display:inline-block;width:12pt}} .ts{{display:inline-block;width:62pt}}
#fp1{{position:absolute;left:62pt;width:200pt;top:64.6pt;text-align:center;color:#fff;font-size:3.3pt;font-weight:500}}
#fp2{{position:absolute;left:283pt;width:190pt;top:64.6pt;text-align:center;color:#fff;font-size:3.3pt;font-weight:600}}
.lg{{position:absolute;object-fit:contain}}
.cap{{position:absolute;left:26%;width:50%;top:31%;text-align:center;font-family:'Great Vibes',cursive;font-size:13pt;line-height:1;color:#7A5A0C;text-shadow:0 0 1.5pt #fff;white-space:nowrap}}
#nh{{position:absolute;left:35.7pt;top:27.6pt;width:512.4pt;height:93.6pt;display:flex;align-items:center;justify-content:center;gap:14pt}}
#nh .nl{{height:70pt;width:auto;filter:drop-shadow(0 1.5pt 2pt rgba(0,0,0,.35))}}
#nh .nn{{font-family:'DM Serif Display',serif;font-size:36pt;line-height:1;white-space:nowrap;color:#fff;-webkit-text-stroke:3.4pt #000;paint-order:stroke fill;letter-spacing:.5pt}}
#nh .ns{{display:flex;height:3.2pt;margin:5pt 0 5pt 2pt;width:100%}} #nh .ns i{{flex:1}}
#nh .ntag{{font-family:Montserrat,sans-serif;font-weight:800;font-size:10.5pt;letter-spacing:5pt;white-space:nowrap;color:#231F20;margin-left:2pt}}
</style></head><body>
{''.join(marks)}
<div id="trim">
 <div id="bg"></div><div id="panel"></div>
 {header(theme, logo)}
 <div id="addr">Shop No. D4<br>Pretoria Oriental Complex<br>Marabastad, Pretoria</div>
 <div id="year">{YEAR}</div>
 <div id="soc">
   <div>{icon('globe', SOC)}<span>www.makkies.co.za</span></div>
   <div>{icon('tiktok', SOC)}{icon('instagram', SOC)}{icon('facebook', SOC)}<span>@makkiewholesalers</span></div>
   <div>{icon('whatsapp', SOC)}<span>072 323 5469</span></div>
 </div>
 {''.join(ph)}
 {''.join(months)}
 <div id="hb">
  <svg id="hbsvg" viewBox="0 0 473 72.9" preserveAspectRatio="none">
   <polygon points="0,0 20,0 36,62 0,62" fill="{th['accent']}"/>
   <polygon points="20,0 23.5,0 39.5,62 36,62" fill="#F3E7C9"/>
   <polygon points="23.5,0 270,0 286,62 39.5,62" fill="{th['dark']}"/>
   <polygon points="270,0 273.5,0 289.5,62 286,62" fill="#F3E7C9"/>
   <polygon points="273.5,0 473,0 473,56 289.5,56" fill="{th['accent']}"/>
   <rect x="34" y="62" width="439" height="10.9" fill="{th['dark']}"/>
   <polygon points="289.5,56 473,56 473,62 291,62" fill="{th['dark']}"/>
  </svg>
  <div id="ht">PUBLIC HOLIDAYS</div>
  <div class="hc" style="left:42pt">{"" if BLANK else hol(HOL_COL1)}</div>
  <div class="hc" style="left:152pt">{"" if BLANK else hol(HOL_COL2)}</div>
  <div id="tt">SCHOOL TERMS</div><div id="ts">INLAND &amp; COASTAL PROVINCES</div>
  <div id="terms">{"" if BLANK else terms}</div>
  <div id="fp1">At the time of going to press, all information, dates &amp; school terms were correct</div>
  <div id="fp2">DESIGNED &amp; PRINTED BY ZIPPY PRESS - www.zippypress.co.za - Tel: 012 666 7093</div>
 </div>
 {logo_html}
</div></body></html>'''

if __name__ == "__main__":
    for arg in (sys.argv[1:] or THEMES):
        t, _, logo = arg.partition(":")
        name = f"{t}_{logo}" if logo else t
        open(os.path.join(HERE, f"cal_{name}.html"), "w").write(build(t, logo or "old"))
        print("wrote", name)
