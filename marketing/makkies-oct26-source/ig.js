const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  await p.goto('file://'+path.join(__dirname,'ig.html'));
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(500);
  for(let i=1;i<=5;i++){
    const el=await p.$('#s'+i);
    await el.screenshot({path:`/home/user/IZ/marketing/instagram/makkies-oct26-carousel-${i}.jpg`,type:'jpeg',quality:93});
  }
  await b.close();
})();
