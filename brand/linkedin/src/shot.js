const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const s of [1,2]){const p=await b.newPage({viewport:{width:1584,height:396},deviceScaleFactor:s});
await p.goto('file://'+__dirname+'/personal-banner.html');await p.waitForTimeout(600);
await p.screenshot({path:__dirname+'/../palami-linkedin-personal-banner-1584x396'+(s==2?'@2x':'')+'.png'});}
await b.close();})();
