// PDF final: aplana (hornea) los degradados oscuros sobre las imágenes para que ningún visor los reinterprete.
const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:1200,height:1400},deviceScaleFactor:2});
 const p=await ctx.newPage();
 await p.goto('file:///home/claude/ebook/index.html?final'); await p.waitForTimeout(1500);
 await p.evaluate(()=>document.fonts.ready);
 const TXT='.ct,.tag,.logo,.qt,.bt,.num,.cap,.chead';
 const n=await p.evaluate(()=>{
   document.querySelectorAll('.cover,.quote,.back,.opener-img').forEach((el,i)=>el.setAttribute('data-flat',i));
   return document.querySelectorAll('[data-flat]').length;});
 for(let i=0;i<n;i++){
   const h=await p.$(`[data-flat="${i}"]`);
   await p.evaluate(([i,TXT])=>{const e=document.querySelector(`[data-flat="${i}"]`);
     e.querySelectorAll(TXT).forEach(t=>t.style.visibility='hidden');},[i,TXT]);
   const buf=await h.screenshot({type:'jpeg',quality:93});
   await p.evaluate(([i,TXT,d])=>{const e=document.querySelector(`[data-flat="${i}"]`);
     e.classList.add('flat'); e.style.backgroundImage=`url(data:image/jpeg;base64,${d})`; e.style.backgroundSize='100% 100%';
     e.querySelectorAll(TXT).forEach(t=>t.style.visibility='');},[i,TXT,buf.toString('base64')]);
 }
 await p.addStyleTag({content:`.flat::after,.flat::before{display:none!important}.flat>.bg,.flat>.photo-bg,.flat>figure,.flat>.ph{display:none!important}`});
 await p.pdf({path:'/home/claude/ebook/E-Book_Johanna-Daza_Sanando-la-desconexion-emocional-en-pareja.pdf',width:'8.5in',height:'11in',printBackground:true,margin:{top:0,right:0,bottom:0,left:0},preferCSSPageSize:true});
 await b.close(); console.log('flat elements',n);
})();
