/* PALAMI marketing site: shared behaviour for the Hebrew and English pages. */
(function(){
  var root=document.querySelector('.site');
  var LANG=root.getAttribute('data-lang')||'he', BASE=root.getAttribute('data-base')||'';

  var T={
    he:{
      menuOpen:'תפריט', menuClose:'סגירת התפריט',
      pause:'השהיית האנימציה', play:'הפעלת האנימציה', prevS:'המסך הקודם', nextS:'המסך הבא',
      errName:'צריך למלא שם מלא', errEmail:'האימייל לא נראה תקין. כדאי לבדוק שוב', errPhone:'מספר הטלפון לא נראה תקין',
      thanks:'תודה, ', sentDraft:'בגרסת העיצוב הטופס עוד לא מחובר. באתר האמיתי הפנייה תגיע אלינו ונחזור אליכם בקרוב.',
      sent:'קיבלנו את הפרטים ונחזור אליכם בקרוב.', sending:'שולחים…', failed:'משהו השתבש בשליחה. אפשר לנסות שוב או לכתוב לנו ל־info@palami.io'
    },
    en:{
      menuOpen:'Menu', menuClose:'Close menu',
      pause:'Pause animation', play:'Play animation', prevS:'Previous screen', nextS:'Next screen',
      errName:'Please enter your full name', errEmail:'That email doesn’t look right. Please check it', errPhone:'That phone number doesn’t look right',
      thanks:'Thank you, ', sentDraft:'This is a design draft, so the form is not connected yet. On the live site your request will reach us and we’ll get back to you soon.',
      sent:'We got your details and will get back to you soon.', sending:'Sending…', failed:'Something went wrong. Please try again or email us at info@palami.io'
    }
  }[LANG];

  var DATA={
    he:{
      agent:[
        ['דשבורד','מה דחוף היום, ביטוח חסר ומה מוכן לפרסום','r-dash.webp','desk','app.palami.io/home'],
        ['תיקי נסיעה','כל התיקים, עם סטטוס, חוסרים וסינון','r-trips.webp','desk','app.palami.io/trips'],
        ['יומן','כל ההמראות והנחיתות של הסוכנות','r-calendar.webp','desk','app.palami.io/calendar'],
        ['מסמכים והעלאה','גוררים את המסמכים והם נכנסים לתיק','r-trip-docs.webp','desk','app.palami.io/trips/HDR-2609-0031'],
        ['ביטוח','מה יש בתיק ואם חסר ביטוח','r-trip-overview.webp','desk','app.palami.io/trips/HDR-2609-0031'],
        ['לקוחות','כל לקוח, עם כל הנסיעות שלו','r-customers.webp','desk','app.palami.io/customers']
      ],
      trav:[
        ['מסך הבית','ספירה לאחור, מסמכים חשובים והאירוע הבא. מתעדכן לבד לפי שלב הנסיעה.','t-home-before.webp','phone',[['t-home-before.webp','לפני הנסיעה'],['t-home-during.webp','במהלך הנסיעה'],['t-home-after.webp','אחרי החזרה']]],
        ['לו״ז','כל יום בנסיעה, לפי השעה המקומית','t-schedule.webp','phone'],
        ['מסמכים','כל הכרטיסים והשוברים, שמורים בטלפון','t-docs.webp','phone'],
        ['התראות','כל העדכונים והתזכורות על הנסיעה, במקום אחד','t-notifs.webp','phone'],
        ['מידע','כל המידע החשוב ליעד: מזג אוויר, השעה ביעד, טיפים מהסוכן ורשימת אריזה','t-info.webp','phone'],
        ['צ\'אט עם הסוכן','שואלים את הסוכן ישירות מהאפליקציה, בלי לחפש מספר','t-chat.webp','phone'],
        ['חירום','מספרים מקומיים, ביטוח והסוכנות, גם בלי אינטרנט','t-emergency.webp','phone']
      ]
    },
    en:{
      agent:[
        ['Dashboard','What’s urgent today, missing insurance and what’s ready to publish','r-dash.webp','desk','app.palami.io/home'],
        ['Trip files','Every trip file, with status, missing items and filters','r-trips.webp','desk','app.palami.io/trips'],
        ['Calendar','All of the agency’s departures and landings','r-calendar.webp','desk','app.palami.io/calendar'],
        ['Documents & upload','Drag the documents in and they’re filed into the trip','r-trip-docs.webp','desk','app.palami.io/trips/HDR-2609-0031'],
        ['Insurance','What’s in the file and whether insurance is missing','r-trip-overview.webp','desk','app.palami.io/trips/HDR-2609-0031'],
        ['Customers','Every customer, with all of their trips','r-customers.webp','desk','app.palami.io/customers']
      ],
      trav:[
        ['Home','Countdown, key documents and what’s next. Updates itself with each stage of the trip.','t-home-before.webp','phone',[['t-home-before.webp','Before the trip'],['t-home-during.webp','During the trip'],['t-home-after.webp','After returning']]],
        ['Schedule','Every day of the trip, in local time','t-schedule.webp','phone'],
        ['Documents','All tickets and vouchers, saved on the phone','t-docs.webp','phone'],
        ['Notifications','Every trip update and reminder, in one place','t-notifs.webp','phone'],
        ['Info','Everything that matters at the destination: weather, local time, tips from the agent and a packing list','t-info.webp','phone'],
        ['Chat with the agent','Ask the agent right from the app, no need to look for a number','t-chat.webp','phone'],
        ['Emergency','Local numbers, insurance and the agency, even offline','t-emergency.webp','phone']
      ]
    }
  }[LANG];

  /* product peek */
  var side='agent', idx=0, list=document.getElementById('pk-list'), stage=document.getElementById('pk-stage');
  function esc(t){ return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function render(){
    var L=DATA[side];
    list.innerHTML=L.map(function(s,i){return '<button type="button" aria-pressed="'+(i===idx)+'" data-i="'+i+'"><b>'+esc(s[0])+'</b><span>'+esc(s[1])+'</span></button>';}).join('');
    var s=L[idx], src=BASE+'img/'+s[2], alt=esc(s[0]+': '+s[1]);
    stopSlides();
    if(s[3]==='phone' && s[4]){ slides(s, alt); return; }
    stage.innerHTML = s[3]==='desk'
      ? '<div class="browser"><img src="'+src+'" alt="'+alt+'"></div>'
      : '<div class="phone"><img src="'+src+'" alt="'+alt+'"></div>';
  }
  /* a screen with stages (traveler home): the phone changes by itself while in view; arrows, dots and swipe (touch or mouse drag) take over */
  var slideT=null, slideIO=null;
  function stopSlides(){ if(slideT){ clearInterval(slideT); slideT=null; } if(slideIO){ slideIO.disconnect(); slideIO=null; } }
  function slides(s, alt){
    var st=s[4], cur=0, held=false, rtl=root.getAttribute('dir')==='rtl';
    stage.innerHTML='<div class="sw"><button type="button" class="sarr" data-d="-1" aria-label="'+T.prevS+'">'+(rtl?'→':'←')+'</button>'
      +'<div class="phone slides" role="img" aria-label="'+alt+'">'+st.map(function(x,i){ return '<img src="'+BASE+'img/'+x[0]+'" alt="" draggable="false"'+(i?'':' class="on"')+'>'; }).join('')+'</div>'
      +'<button type="button" class="sarr" data-d="1" aria-label="'+T.nextS+'">'+(rtl?'←':'→')+'</button></div>'
      +'<p class="scap">'+esc(st[0][1])+'</p><div class="sdots">'+st.map(function(x,i){ return '<button type="button" data-s="'+i+'" aria-pressed="'+(i===0)+'"><span>'+esc(x[1])+'</span></button>'; }).join('')+'</div>';
    var sw=stage.querySelector('.sw'), cap=stage.querySelector('.scap'), ph=stage.querySelector('.slides'), imgs=ph.querySelectorAll('img'), dots=stage.querySelectorAll('[data-s]');
    var show=function(i){ cur=(i+st.length)%st.length; cap.textContent=st[cur][1];
      Array.prototype.forEach.call(imgs,function(im,k){ im.classList.toggle('on',k===cur); });
      Array.prototype.forEach.call(dots,function(d,k){ d.setAttribute('aria-pressed',String(k===cur)); }); };
    var take=function(i){ held=true; stopSlides(); show(i); };
    Array.prototype.forEach.call(dots,function(d){ d.addEventListener('click',function(){ take(+d.getAttribute('data-s')); }); });
    sw.querySelectorAll('.sarr').forEach(function(b){ b.addEventListener('click',function(){ take(cur+(+b.getAttribute('data-d'))); }); });
    var x0=null;
    ph.addEventListener('pointerdown',function(e){ x0=e.clientX; });
    ph.addEventListener('pointerup',function(e){ if(x0===null) return; var dx=e.clientX-x0; x0=null;
      if(Math.abs(dx)>30) take(cur+((dx<0)!==rtl?1:-1)); });
    if(window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var run=function(){ if(!slideT && !held) slideT=setInterval(function(){ show(cur+1); },3500); };
    var pause=function(){ if(slideT){ clearInterval(slideT); slideT=null; } };
    sw.addEventListener('mouseenter',pause); sw.addEventListener('mouseleave',run);
    sw.addEventListener('focusin',pause); sw.addEventListener('focusout',run);
    if('IntersectionObserver' in window){
      slideIO=new IntersectionObserver(function(es){ if(es[0].isIntersecting) run(); else pause(); },{threshold:.5});
      slideIO.observe(ph);
    } else run();
  }
  if(list && stage){
    document.querySelectorAll('[data-side]').forEach(function(b){
      b.addEventListener('click',function(){ side=b.getAttribute('data-side'); idx=0;
        document.querySelectorAll('[data-side]').forEach(function(x){x.setAttribute('aria-selected',String(x===b));}); render(); });
    });
    list.addEventListener('click',function(e){ var b=e.target.closest('[data-i]'); if(!b) return; idx=+b.getAttribute('data-i'); render();
      var cur=list.querySelector('[data-i="'+idx+'"]'); if(cur && cur.scrollIntoView) cur.scrollIntoView({block:'nearest',inline:'nearest',behavior:'smooth'}); });
    render();
    /* mobile: one scrollable row; fade + arrow show there are more screens */
    var wrap=list.parentNode, more=wrap.querySelector('.more'), rtl=root.getAttribute('dir')==='rtl';
    if(more){
      more.textContent=rtl?'←':'→';
      var edges=function(){ var max=list.scrollWidth-list.clientWidth, pos=Math.abs(list.scrollLeft);
        var scrolls=max>4; wrap.classList.toggle('scrolls',scrolls);
        wrap.classList.toggle('at-start',pos<4); wrap.classList.toggle('at-end',pos>max-4);
        more.hidden=!scrolls || pos>max-4; };
      list.addEventListener('scroll',edges,{passive:true}); window.addEventListener('resize',edges);
      document.querySelectorAll('[data-side]').forEach(function(b){ b.addEventListener('click',function(){ list.scrollLeft=0; edges(); }); });
      more.addEventListener('click',function(){ list.scrollBy({left:(rtl?-1:1)*list.clientWidth*0.6,behavior:'smooth'}); });
      edges();
    }
  }

  /* hero visual: clicking the agent screen or the phone opens that side in the product peek */
  var peek=document.getElementById('peek');
  document.querySelectorAll('[data-peek]').forEach(function(a){
    a.addEventListener('click',function(){ var tab=document.querySelector('[data-side="'+a.getAttribute('data-peek')+'"]'); if(tab && tab.getAttribute('aria-selected')!=='true') tab.click(); });
  });
  document.querySelectorAll('.hero .art, .hero .mdash').forEach(function(el){
    el.addEventListener('click',function(e){
      var want=e.target.closest('.phone, .k3, .mphl')?'trav':'agent', tab=document.querySelector('[data-side="'+want+'"]');
      if(tab && tab.getAttribute('aria-selected')!=='true') tab.click();
      if(peek) peek.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
    });
  });

  /* benefits: always open, on every screen size (the explanation is part of the message) */
  document.querySelectorAll('details.bi summary').forEach(function(su){
    su.addEventListener('click',function(e){ e.preventDefault(); });
    su.setAttribute('tabindex','-1');
  });

  /* how-it-works animation: scale to column, pause control */
  var art=document.querySelector('.hvw');
  if(art){
    var fitHv=function(){ var k=Math.min(1,art.clientWidth/480); art.style.setProperty('--k',k); art.style.height=(524*k)+'px'; };
    window.addEventListener('resize',fitHv); fitHv();
    var pb=art.querySelector('.hv-pause'), steps=document.querySelector('.howg');
    if(pb){
      pb.addEventListener('click',function(){
        var p=!art.classList.contains('paused');
        art.classList.toggle('paused',p); if(steps) steps.classList.toggle('paused',p);
        pb.setAttribute('aria-pressed',String(p));
        pb.querySelector('span').textContent=p?T.play:T.pause;
      });
    }
  }

  /* mobile menu */
  var hdr=document.querySelector('.hdr'), mb=hdr&&hdr.querySelector('.menu');
  if(mb){
    var setMenu=function(o){ hdr.classList.toggle('open',o); mb.setAttribute('aria-expanded',String(o)); mb.setAttribute('aria-label',o?T.menuClose:T.menuOpen); };
    mb.addEventListener('click',function(){ setMenu(!hdr.classList.contains('open')); });
    hdr.querySelectorAll('nav a').forEach(function(a){ a.addEventListener('click',function(){ setMenu(false); }); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape' && hdr.classList.contains('open')){ setMenu(false); mb.focus(); } });
  }

  /* highlight the current section in the nav */
  var navA=[].slice.call(document.querySelectorAll('.hdr nav a[href^="#"]'));
  if(navA.length){
    var spy=function(){ var y=window.innerHeight*0.4, cur=''; navA.forEach(function(a){ var s=document.querySelector(a.getAttribute('href')); if(!s) return; var r=s.getBoundingClientRect(); if(r.top<=y && r.bottom>y) cur=s.id; });
      navA.forEach(function(a){ if(cur && a.getAttribute('href')==='#'+cur) a.setAttribute('aria-current','true'); else a.removeAttribute('aria-current'); }); };
    window.addEventListener('scroll',spy,{passive:true}); window.addEventListener('resize',spy); spy();
  }

  /* demo request form. When the form has a real action URL it is sent with fetch; otherwise it shows the design-draft message. */
  var f=document.getElementById('demo-form'), err=document.getElementById('f-err');
  if(f){
    /* where the visitor came from (UTM tags or the referring site), sent with the form. No cookies or storage. */
    var src=f.querySelector('input[name="source"]');
    if(src){
      var q=new URLSearchParams(location.search), parts=[];
      ['utm_source','utm_medium','utm_campaign'].forEach(function(k){ var v=q.get(k); if(v) parts.push(k.slice(4)+'='+v.slice(0,60)); });
      try{ if(document.referrer){ var h=new URL(document.referrer).hostname; if(h && h!==location.hostname) parts.push('ref='+h); } }catch(x){}
      src.value=parts.join('; ')||'direct';
    }
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var bad=[], n=f.name.value.trim(), m=f.email.value.trim(), p=f.phone.value.replace(/[\s()-]/g,'');
      [['name',!n],['email',!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(m)],['phone',!/^\+?\d{9,15}$/.test(p)]].forEach(function(x){ f[x[0]].setAttribute('aria-invalid',String(x[1])); if(x[1]) bad.push(x[0]); });
      if(bad.length){ err.hidden=false; err.textContent= bad.indexOf('name')>=0?T.errName: bad.indexOf('email')>=0?T.errEmail:T.errPhone; f[bad[0]].focus(); return; }
      err.hidden=true;
      var first=esc(n.split(' ')[0]);
      var done=function(msg){ f.innerHTML='<div class="okmsg" role="status" tabindex="-1"><img src="'+BASE+'img/mascot.webp" alt=""><b>'+T.thanks+first+'!</b><span>'+msg+'</span></div>'; var o=f.querySelector('.okmsg'); if(o) o.focus(); };
      var action=f.getAttribute('action');
      if(!action || action==='#'){ done(T.sentDraft); return; }
      if(f.website && f.website.value){ done(T.sent); return; } /* honeypot: bots fill the hidden field */
      var btn=f.querySelector('button[type="submit"]'); if(btn){ btn.disabled=true; btn.textContent=T.sending; }
      fetch(action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
        .then(function(r){ if(!r.ok) throw new Error(r.status); done(T.sent); })
        .catch(function(){ err.hidden=false; err.textContent=T.failed; if(btn){ btn.disabled=false; btn.textContent=btn.getAttribute('data-label')||btn.textContent; } });
    });
  }
  /* lock screen notifications: drop in once when the section scrolls into view */
  var locks=document.querySelectorAll('.lock');
  if(locks.length && 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion:reduce)').matches){
    var lo=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('go'); lo.unobserve(e.target); } }); },{threshold:.4});
    Array.prototype.forEach.call(locks,function(l){ l.classList.add('anim'); lo.observe(l); });
  }
})();
