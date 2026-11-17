const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'black-friday-status.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await p.screenshot({ path: path.join(__dirname, 'out', 'black-friday-status.jpg'), type: 'jpeg', quality: 92 }); await b.close(); })();
