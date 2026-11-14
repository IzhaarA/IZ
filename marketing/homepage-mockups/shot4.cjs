const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch();
  let p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await p.goto('http://localhost:8788/look-g.html', { waitUntil: 'load' }); await p.waitForTimeout(600);
  for (const [i, y] of [[1,0],[2,800],[3,1700],[4,3200]]) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(200); await p.screenshot({ path: `phone-g-${i}.png` }); }
  await p.screenshot({ path: 'phone-g-full.png', fullPage: true }); await p.close();
  p = await b.newPage({ viewport: { width: 1366, height: 900 } });
  await p.goto('http://localhost:8788/look-g.html', { waitUntil: 'load' }); await p.waitForTimeout(600);
  await p.screenshot({ path: 'desk-g.png', fullPage: true }); await b.close(); })();
