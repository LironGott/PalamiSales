/* PALAMI landing page (/demo/): audience variants for ad message match, form, sticky bar, gentle reveal. No cookies or storage. */
(function(){
  var root=document.querySelector('.lp'), BASE=root.getAttribute('data-base')||'';
  var q=new URLSearchParams(location.search);
  var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var WA='https://wa.me/972542245627?text=%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A9%D7%9E%D7%95%D7%A2%20%D7%A2%D7%9C%20PALAMI';
  var T={
    errName:'צריך למלא שם מלא', errPhone:'מספר הטלפון לא נראה תקין. כדאי לבדוק שוב',
    thanks:'תודה, ', sent:'קיבלנו את הפרטים ונחזור אליכם בקרוב לתיאום ההדגמה.',
    sentDraft:'בגרסת התצוגה הטופס לא שולח. באתר החי הפנייה תגיע אלינו ונחזור אליכם בקרוב.',
    sending:'שולחים…', failed:'משהו השתבש בשליחה. אפשר לנסות שוב או לכתוב לנו ב־WhatsApp', now:'רוצים לדבר כבר עכשיו?'
  };

  /* message match: ?for=solo or ?for=agency (use it in the ad URL) tunes the eyebrow, the lead and the preselected business type */
  var V={
    solo:{eyebrow:'לסוכנים עצמאיים', lead:'גוררים את המסמכים של הנסיעה, PALAMI מתייקת הכל אוטומטית והנוסע מקבל את כל הנסיעה בטלפון, עם הלוגו שלכם. כמו סוכנות גדולה, גם כשעובדים לבד.'},
    agency:{eyebrow:'לסוכנויות נסיעות', lead:'כל התיקים של כל הסוכנים במסך אחד. גוררים את המסמכים, PALAMI מתייקת הכל אוטומטית והנוסע מקבל את כל הנסיעה בטלפון, במיתוג הסוכנות.'}
  };
  var who=q.get('for');
  if(V[who]){
    Object.keys(V[who]).forEach(function(k){ var el=document.querySelector('[data-v="'+k+'"]'); if(el) el.textContent=V[who][k]; });
    var r=document.querySelector('input[name="business"][value="'+who+'"]'); if(r) r.checked=true;
    var c=document.querySelector('.wcard[data-seg="'+who+'"]'); if(c) c.classList.add('hl');
  }

  /* header shadow once the page scrolls */
  var hdr=document.querySelector('.hdr');
  var onScroll=function(){ hdr.classList.toggle('scrolled',window.scrollY>8); };
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();

  /* every CTA goes to the form and puts the cursor in the first field */
  var f=document.getElementById('demo-form'), lead=document.getElementById('lead');
  document.querySelectorAll('[data-go="lead"]').forEach(function(a){
    a.addEventListener('click',function(e){
      e.preventDefault();
      lead.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
      var first=f && f.querySelector('#f-name'); if(first) setTimeout(function(){ first.focus({preventScroll:true}); },reduce?0:450);
    });
  });

  /* phone sticky bar: hidden while the form is on screen */
  var mbar=document.querySelector('.mbar');
  if(mbar && 'IntersectionObserver' in window){
    new IntersectionObserver(function(es){ es.forEach(function(e){ mbar.classList.toggle('away',e.isIntersecting); }); },{threshold:.25}).observe(lead);
  }

  /* gentle reveal of sections */
  if(!reduce && 'IntersectionObserver' in window){
    var els=document.querySelectorAll('.step,.filed,.tile,.wcard,.path li,.phonechat,.fbox');
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); io.unobserve(e.target); } }); },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    Array.prototype.forEach.call(els,function(el,i){ el.classList.add('rv'); el.style.transitionDelay=((i%3)*70)+'ms'; io.observe(el); });
  }

  /* form */
  var err=document.getElementById('f-err');
  if(!f) return;
  var src=f.querySelector('input[name="source"]');
  if(src){
    var parts=[];
    ['utm_source','utm_medium','utm_campaign','utm_content','for'].forEach(function(k){ var v=q.get(k); if(v) parts.push(k.replace('utm_','')+'='+v.slice(0,60)); });
    try{ if(document.referrer){ var h=new URL(document.referrer).hostname; if(h && h!==location.hostname) parts.push('ref='+h); } }catch(x){}
    src.value=parts.join('; ')||'direct';
  }
  function esc(t){ return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  /* clear the error mark as soon as the field is fixed */
  ['name','phone'].forEach(function(n){ f[n].addEventListener('input',function(){ if(f[n].getAttribute('aria-invalid')==='true'){ f[n].setAttribute('aria-invalid','false'); err.hidden=true; } }); });
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var n=f.name.value.trim(), p=f.phone.value.replace(/[\s().-]/g,'');
    var badN=n.length<2, badP=!/^(\+?972|0)\d{8,9}$/.test(p) && !/^\+\d{9,15}$/.test(p);
    f.name.setAttribute('aria-invalid',String(badN)); f.phone.setAttribute('aria-invalid',String(badP));
    if(badN||badP){ err.hidden=false; err.textContent=badN?T.errName:T.errPhone; (badN?f.name:f.phone).focus(); return; }
    err.hidden=true;
    var first=esc(n.split(' ')[0]);
    var done=function(msg){
      lead.classList.add('done');
      f.innerHTML='<div class="okmsg" role="status" tabindex="-1"><img src="'+BASE+'img/mascot.webp" alt=""><b>'+T.thanks+first+'!</b><span>'+msg+'</span><span class="alt">'+T.now+' <a class="wa" href="'+WA+'" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a></span></div>';
      var o=f.querySelector('.okmsg'); if(o) o.focus();
    };
    var action=f.getAttribute('action');
    if(!action || action==='#'){ done(T.sentDraft); return; }
    if(f.website && f.website.value){ done(T.sent); return; } /* honeypot */
    var btn=f.querySelector('button[type="submit"]'); btn.disabled=true; btn.textContent=T.sending;
    fetch(action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
      .then(function(r){ if(!r.ok) throw new Error(r.status); done(T.sent); })
      .catch(function(){ err.hidden=false; err.textContent=T.failed; btn.disabled=false; btn.textContent=btn.getAttribute('data-label'); });
  });
})();
