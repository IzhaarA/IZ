const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path'), fs=require('fs');
(async()=>{
  const page=process.argv[2], mode=process.argv[3]||'full', dir=__dirname;
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.join(dir,page+'.html')); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(700);
  const D=await p.evaluate(()=>window.DURATION);
  const out=path.join(dir,(mode==='preview'?'prev-':'frames-')+page); fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true});
  const times= mode==='preview' ? (process.argv[4]||'2.3,4.9,6.6,9.6,'+(D-5.2)+','+(D-1.2)).split(',').map(Number) : [...Array(Math.round(D*30)).keys()].map(i=>i/30);
  let i=0; for(const t of times){ await p.evaluate(t=>render(t),t); await p.screenshot({path:path.join(out,'f'+String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:93}); i++; }
  console.log(page,'duration',D,'frames',i,'errors',errs); await b.close();
})();
