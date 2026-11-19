const { chromium } = require('playwright');
const path=require('path');
(async()=>{
  const [page,times]=[process.argv[2],process.argv[3].split(',').map(Number)];
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.join(__dirname,page+'.html')); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
  const D=await p.evaluate(()=>window.DURATION);
  const shots=[];
  for(const t of times){ await p.evaluate(t=>render(t),t); shots.push(await p.screenshot({type:'jpeg',quality:70})); }
  // contact sheet
  await p.setViewportSize({width:1080*Math.min(4,shots.length)/3,height:1920*Math.ceil(shots.length/4)/3});
  await p.setContent('<body style="margin:0;display:flex;flex-wrap:wrap;background:#888">'+shots.map(s=>`<img style="width:360px;height:640px" src="data:image/jpeg;base64,${s.toString('base64')}">`).join('')+'</body>');
  await p.waitForTimeout(300);
  await p.screenshot({path:'/tmp/claude-0/-home-user-IZ/2fe381b0-b6e5-5442-ac73-431a50475247/scratchpad/prev-'+page+'.jpg',type:'jpeg',quality:80});
  console.log(page,'duration',D.toFixed(1),'errors',errs); await b.close();
})();
