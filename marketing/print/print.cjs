const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  for (const [f, out] of [['sign.html', 'makkies-shop-sign-A4'], ['cards.html', 'makkies-qr-cards-A4']]) {
    await p.goto('file://' + path.join(__dirname, f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    await p.pdf({ path: out + '.pdf', format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    await p.screenshot({ path: out + '.png', fullPage: true }); }
  await b.close(); })();
