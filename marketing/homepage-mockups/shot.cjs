const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [url, out, w, h, full] = process.argv.slice(2);
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  await p.screenshot({ path: out, fullPage: full === '1' }); await b.close(); })();
