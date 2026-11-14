const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await p.goto('file:///tmp/claude-0/-home-user-IZ/2fe381b0-b6e5-5442-ac73-431a50475247/scratchpad/home/look-g.html', { waitUntil: 'load' }); await p.waitForTimeout(600);
  await p.addStyleTag({ content: 'header{position:relative!important}' });
  await p.screenshot({ path: 'phone-g-full.png', fullPage: true }); await b.close(); })();
