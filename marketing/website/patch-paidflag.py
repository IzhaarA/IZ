# Card sales were not counted (22 Nov 2026). Coming back from PayFast, the page clears '#paid' from the address
# before the Google tag (patch-gtag.py) and the visitor counter (t.js) look for it, so neither saw the sale:
# Google Ads reported no conversions and the stats page showed 0 orders. Now the '#paid' return is remembered
# at the very start of the page (window.MK_PAID) and both check that instead.
# Usage: python3 patch-paidflag.py public/index.html   (after patch-track.py and patch-gtag.py; also copies the fixed t.js)
import sys, os, shutil
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'window.MK_PAID' in s:
    print('paid flag already patched'); sys.exit()
FLAG = "<script>window.MK_PAID = location.hash === '#paid';</script>\n"
i = s.find('<head>')
if i < 0: raise SystemExit('<head> not found')
s = s[:i + 6] + '\n' + FLAG + s[i + 6:]
old = "if (location.hash === '#paid') { try { const o = JSON.parse(localStorage.getItem('makkie_gpay')"
if s.count(old) != 1: raise SystemExit('gtag #paid check not found')
s = s.replace(old, "if (window.MK_PAID || location.hash === '#paid') { try { const o = JSON.parse(localStorage.getItem('makkie_gpay')")
open(P, 'w', encoding='utf-8').write(s)
H = os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(H, 'track', 't.js'), os.path.join(os.path.dirname(os.path.abspath(P)), 't.js'))
print('card sales now reach Google Ads and the stats page')
