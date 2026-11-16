# Visitor tracking (no cookies): adds /t.js + shop hooks to index.html and the private /stats/ page.
# Usage: python3 patch-track.py public/index.html   (run after patch-nav.py; make-seo-pages.py adds /t.js to the Google pages)
# Data: netlify/functions/track.mjs (POST /api/t) and stats.mjs (GET /api/stats?k=KEY). Stats page: /stats/#KEY
import sys, os, shutil
P = sys.argv[1]; s = open(P, encoding='utf-8').read()
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'track'); PUB = os.path.dirname(os.path.abspath(P))
if 'src="/t.js"' not in s:
    hooks = open(os.path.join(H, 'hooks.js')).read()
    i = s.rfind('</body>')
    s = s[:i] + '<script>' + hooks + '</script><script src="/t.js" defer></script>\n' + s[i:]
    open(P, 'w', encoding='utf-8').write(s)
shutil.copy(os.path.join(H, 't.js'), os.path.join(PUB, 't.js'))
os.makedirs(os.path.join(PUB, 'stats'), exist_ok=True)
shutil.copy(os.path.join(H, 'stats.html'), os.path.join(PUB, 'stats', 'index.html'))
print('tracking added')
