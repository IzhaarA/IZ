# Site name in Google results (21 Nov 2026). Google showed "makkies.co.za" above results instead of the business name:
# the home page had Store data but no WebSite data, which is what Google uses for the site name. Adds WebSite
# structured data (name Makkie Wholesalers, alternate names Makkies / makkies.co.za) with the site search.
# Usage: python3 patch-sitename.py public/index.html   (always; any order)
import sys, json
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if '"@type": "WebSite"' in s or '"@type":"WebSite"' in s:
    print('site name already patched'); sys.exit()
LD = {"@context": "https://schema.org", "@type": "WebSite", "name": "Makkie Wholesalers",
      "alternateName": ["Makkies", "Makkie Wholesalers Marabastad", "makkies.co.za"], "url": "https://makkies.co.za/",
      "publisher": {"@type": "Organization", "name": "Makkie Wholesalers", "url": "https://makkies.co.za/",
                    "logo": "https://makkies.co.za/apple-touch-180.png"}}
tag = '<script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False) + '</script>\n'
i = s.find('</head>')   # the page's own head (a later '</head>' sits inside the invoice template)
if i < 0: raise SystemExit('</head> not found')
s = s[:i] + tag + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('WebSite site name added')
