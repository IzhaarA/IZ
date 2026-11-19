# Product photos in the shop grid (19 Nov 2026).
# A customer browsing from TikTok's in-app browser saw grey boxes instead of the mirror photos: the grid only
# loaded photos when scrolled near ("lazy"), which some in-app browsers on slow data do late or not at all.
# Now the first 8 cards load their photo straight away, and a photo that fails is retried once (full-size photo).
# Usage: python3 patch-images.py public/index.html
import sys
P = sys.argv[1]
s = open(P, encoding='utf-8').read()
if 'function imgRetry(' in s:
    print('images already patched'); sys.exit()
def sub(old, new):
    global s
    if s.count(old) != 1: raise SystemExit(f'pattern found {s.count(old)} times: ' + old[:80])
    s = s.replace(old, new)
sub("document.getElementById('grid').innerHTML = shown.map(p => `<article",
    "document.getElementById('grid').innerHTML = shown.map((p, gi) => `<article")
sub("<img loading=\"lazy\" decoding=\"async\" src=\"${tn(p.img)}\" alt=\"${esc(p.name)}\"",
    "<img loading=\"${gi < 8 ? 'eager' : 'lazy'}\" decoding=\"async\" src=\"${tn(p.img)}\" alt=\"${esc(p.name)}\" onerror=\"imgRetry(this,'${p.img}')\"")
sub("function hi(img, url) {",
    "function imgRetry(img, full) { if (img.dataset.retry) return; img.dataset.retry = 1; img.loading = 'eager'; setTimeout(() => { img.src = full + (full.includes('?') ? '&' : '?') + 'r=1'; }, 400); }\nfunction hi(img, url) {")
open(P, 'w', encoding='utf-8').write(s)
print('grid photos: first 8 load straight away, failed photos retried')
