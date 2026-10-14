const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path'), fs=require('fs');
(async()=>{
  const dir=__dirname, mode=process.argv[2]||'full';
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.join(dir,'ad.html'));
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(600);
  const out=path.join(dir, mode==='preview'?'prev':'frames'); fs.mkdirSync(out,{recursive:true});
  const times = mode==='preview' ? [1.9,4.95,6.4,9.6,12.7,15.8,19.0] : [...Array(600).keys()].map(i=>i/30);
  let i=0;
  for(const t of times){ await p.evaluate(t=>render(t),t);
    await p.screenshot({path:path.join(out,(mode==='preview'?'p':'f')+String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:93}); i++; }
  await b.close();
})();
