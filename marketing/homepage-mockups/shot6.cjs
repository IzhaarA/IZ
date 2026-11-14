const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch();
  const u='file:///tmp/claude-0/-home-user-IZ/2fe381b0-b6e5-5442-ac73-431a50475247/scratchpad/home/look-g.html';
  let p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await p.goto(u); await p.waitForTimeout(600); await p.addStyleTag({ content: 'header{position:relative!important}' });
  await p.screenshot({ path: 'phone-g-full.png', fullPage: true }); await p.close();
  p = await b.newPage({ viewport: { width: 1366, height: 900 } }); await p.goto(u); await p.waitForTimeout(600);
  await p.addStyleTag({ content: 'header{position:relative!important}' });
  await p.screenshot({ path: 'desk-g.png', fullPage: true }); await b.close(); })();
