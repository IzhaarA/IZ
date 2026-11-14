const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch();
  for (const l of ['d','e','f']) {
    let p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await p.goto(`http://localhost:8788/look-${l}.html`, { waitUntil: 'load' }); await p.waitForTimeout(600);
    await p.screenshot({ path: `phone-${l}.png` });                       // first screen as a customer sees it
    await p.evaluate(() => window.scrollTo(0, 760)); await p.waitForTimeout(200);
    await p.screenshot({ path: `phone-${l}-2.png` }); await p.close();
    p = await b.newPage({ viewport: { width: 1366, height: 900 } });
    await p.goto(`http://localhost:8788/look-${l}.html`, { waitUntil: 'load' }); await p.waitForTimeout(600);
    await p.screenshot({ path: `desk-${l}.png`, fullPage: true }); await p.close(); }
  await b.close(); })();
