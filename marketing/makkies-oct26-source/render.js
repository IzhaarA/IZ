const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const dir=process.argv[2], mode=process.argv[3];
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.join(dir,'ad.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(500);
  const times = mode==='preview' ? [0.3,1.0,1.7,2.7,3.7,4.7,5.7,6.6,7.5,9.0,10.5,13.5] : [...Array(450).keys()].map(i=>i/30);
  let i=0;
  for(const t of times){
    await p.evaluate(t=>render(t),t);
    await p.screenshot({path:path.join(dir, mode==='preview'?'prev':'frames', (mode==='preview'?'p':'f')+String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:94});
    i++;
  }
  await b.close();
})();
