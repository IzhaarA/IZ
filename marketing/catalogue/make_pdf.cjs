// Prints <work>/catalogue.html to the catalogue PDF with the MW oval and page numbers in the footer.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [work, out] = process.argv.slice(2);
  const oval = fs.readFileSync(path.join(__dirname, '..', 'logo', 'makkies-mw-oval-300.png')).toString('base64');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(work, 'catalogue.html'), { waitUntil: 'load' });
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font-family:Arial;font-size:7.5px;color:#777;padding:0 12mm;display:flex;align-items:center;justify-content:space-between">
      <span style="display:flex;align-items:center;gap:6px;letter-spacing:1px"><img src="data:image/png;base64,${oval}" style="height:15px">MAKKIE WHOLESALERS · makkies.co.za</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>` });
  await b.close();
})();
