const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage();
  for(const t of process.argv.slice(2)){
    await p.goto('file://'+path.join(__dirname,`cal_${t}.html`));
    await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
    await p.pdf({path:path.join(__dirname,`raw_${t}.pdf`),preferCSSPageSize:true,printBackground:true});
  }
  await b.close();
})();
