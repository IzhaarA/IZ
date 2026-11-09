const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, '00-welcome.html')); await p.waitForTimeout(600);
  await p.screenshot({ path: path.join(__dirname, 'out', '00-welcome.jpg'), type: 'jpeg', quality: 92 }); await b.close(); })();
