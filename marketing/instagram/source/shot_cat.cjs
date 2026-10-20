// Screenshots the Oct 2026 category carousels (built by build_ig.py) into ../makkies-<name>-carousel-NN.jpg
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');
const NAMES = ['beaded-accessories', 'ndebele-hats', 'cloudsoft-shawls', 'chenille-throws', 'plain-shawls', 'wool', 'towels'];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const name of process.argv.slice(2).length ? process.argv.slice(2) : NAMES) {
    const out = path.join(__dirname, '..');
    for (const f of fs.readdirSync(out)) if (f.startsWith(`makkies-${name}-carousel-`)) fs.unlinkSync(path.join(out, f));
    await p.goto('file://' + path.join(__dirname, `ig_${name}.html`));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    const els = await p.$$('.slide');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(out, `makkies-${name}-carousel-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 93 });
    console.log(name, els.length);
  }
  await b.close();
})();
