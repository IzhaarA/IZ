const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  for(const [name,out] of [['lamberets','makkies-lamberets-carousel']]){
    await p.goto('file://'+path.join(__dirname,`ig_${name}.html`));
    await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(500);
    const els=await p.$$('.slide');
    for(let i=0;i<els.length;i++) await els[i].screenshot({path:`/home/user/IZ/marketing/instagram/${out}-${String(i+1).padStart(2,'0')}.jpg`,type:'jpeg',quality:93});
  }
  await b.close();
})();
