const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => { const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
  for (const f of fs.readdirSync(__dirname).filter(f => /^\d\d-.*\.html$/.test(f))) {
    await p.goto('file://' + path.join(__dirname, f)); await p.waitForTimeout(500);
    await p.screenshot({ path: path.join(__dirname, 'out', f.replace('.html', '.jpg')), type: 'jpeg', quality: 92 }); }
  await b.close(); })();
