const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const dir=process.argv[2], mode=process.argv[3];
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.join(dir,'ad_insta.html'));
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(500);
  const times = mode==='preview' ? [1.7,5.9,9.5,11.0,12.0,13.5,15.9,16.4,17.8,21.5] : [...Array(660).keys()].map(i=>i/30);
  let i=0;
  for(const t of times){
    await p.evaluate(t=>render(t),t);
    await p.screenshot({path:path.join(dir, mode==='preview'?'prev':'frames_insta', (mode==='preview'?'p':'f')+String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:94});
    i++;
  }
  await b.close();
})();
