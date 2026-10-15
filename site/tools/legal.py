"""Generate the privacy policy and accessibility statement pages (HE + EN) from the texts below.
Run from the site/ folder: python3 tools/legal.py"""
import os

UPDATED = {'he': '15.10.2026', 'en': '15 October 2026'}

SHELL = '''<title>{title} · PALAMI</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{b}img/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;600;700;800&family=Assistant:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="{b}css/site.css">

<div class="site doc-page" id="top" dir="{dir}" lang="{lang}" data-lang="{lang}" data-base="{b}">
<a class="skip" href="#main">{skip}</a>
<header class="hdr"><div class="in">
  <a class="logo" href="{home}" aria-label="{home_label}"><img class="bv" src="{b}img/mascot-head.webp" alt="" width="44" height="44"><img src="{b}img/wordmark-tagline.svg" alt="PALAMI"></a>
  <a class="back" href="{home}">{back}</a>
  <a class="lang" href="{other}" hreflang="{olang}" lang="{olang}" aria-label="{olabel}">{oshort}</a>
</div></header>

<main id="main" class="doc"><div class="in">
  <h1>{title}</h1>
  <p class="upd">{upd_label} {updated}</p>
{body}
</div></main>

<footer class="ftr"><div class="in">
  <img src="{b}img/logo-full.webp" alt="PALAMI" width="200" height="82">
  <div class="ct">
    <a class="ltr" href="mailto:hello@palami.io">hello@palami.io</a>
    <a class="ltr" href="tel:+972542245627">{phone}</a>
    <a href="privacy.html">{privacy}</a>
    <a href="accessibility.html">{a11y}</a>
    <span>© 2026 PALAMI</span>
  </div>
</div></footer>
</div>
'''

COMMON = {
    'he': dict(dir='rtl', lang='he', b='', home='index.html', home_label='PALAMI, לעמוד הבית', back='חזרה לעמוד הבית',
               olang='en', olabel='English', oshort='EN', skip='דילוג לתוכן', upd_label='עדכון אחרון:',
               phone='054-2245627', privacy='מדיניות פרטיות', a11y='הצהרת נגישות'),
    'en': dict(dir='ltr', lang='en', b='../', home='index.html', home_label='PALAMI, home page', back='Back to the home page',
               olang='he', olabel='עברית', oshort='עב', skip='Skip to content', upd_label='Last updated:',
               phone='+972-54-224-5627', privacy='Privacy policy', a11y='Accessibility statement'),
}

PRIVACY = {
'he': dict(title='מדיניות פרטיות', desc='מדיניות הפרטיות של האתר palami.io.', body='''
  <p>המדיניות הזאת מסבירה איזה מידע אנחנו מקבלים דרך האתר palami.io ומה אנחנו עושים איתו. היא חלה על האתר בלבד. למערכת PALAMI ולאפליקציית הנוסע יש תנאים נפרדים.</p>
  <h2>מי אנחנו</h2>
  <p>האתר מופעל על ידי PALAMI <span class="todo">[שם החברה הרשום ומספר החברה יעודכנו]</span>. לכל שאלה: <a class="ltr" href="mailto:hello@palami.io">hello@palami.io</a> או <a class="ltr" href="tel:+972542245627">054-2245627</a>.</p>
  <h2>איזה מידע אנחנו אוספים</h2>
  <p>רק את מה שממלאים בטופס בקשת ההדגמה: שם מלא, אימייל, טלפון ושם הסוכנות (לא חובה). אין חובה למסור את הפרטים, אבל בלעדיהם לא נוכל לחזור אליכם.</p>
  <p>האתר לא משתמש בעוגיות לפרסום או למעקב ולא בכלי ניתוח של צד שלישי. כמו בכל אתר, ספק האחסון שומר רישומים טכניים (כמו כתובת IP וסוג דפדפן) לצורכי אבטחה ותפעול.</p>
  <h2>למה אנחנו משתמשים במידע</h2>
  <p>כדי לחזור אליכם, לתאם את ההדגמה ולענות על שאלות. לא נשלח אליכם דיוור שיווקי בלי הסכמה מפורשת, ולא נמכור או נשכיר את הפרטים.</p>
  <h2>עם מי המידע משותף</h2>
  <p>רק עם ספקי שירות שעוזרים לנו להפעיל את האתר ולקבל את הפניות (אחסון האתר ושירות הטפסים והדואר), ורק לצורך הזה. <span class="todo">[שמות הספקים יעודכנו לפני העלאה]</span> המידע יכול להישמר בשרתים מחוץ לישראל.</p>
  <h2>כמה זמן נשמור את המידע</h2>
  <p>כל עוד צריך לטפל בפנייה ובקשר העסקי, ולא יותר מ־24 חודשים מהפנייה האחרונה, אלא אם החוק מחייב אחרת.</p>
  <h2>הזכויות שלכם</h2>
  <p>אפשר לבקש לעיין במידע שלכם, לתקן אותו או למחוק אותו. פונים אלינו ב־<a class="ltr" href="mailto:hello@palami.io">hello@palami.io</a> ונטפל בבקשה בהקדם.</p>
  <h2>אבטחה</h2>
  <p>האתר מוצפן ב־HTTPS והגישה לפניות מוגבלת לאנשים שמטפלים בהן.</p>
  <h2>שינויים במדיניות</h2>
  <p>אם נעדכן את המדיניות, הגרסה החדשה תופיע בעמוד הזה עם תאריך העדכון.</p>
'''),
'en': dict(title='Privacy policy', desc='Privacy policy for the palami.io website.', body='''
  <p>This policy explains what information we receive through the palami.io website and what we do with it. It covers the website only. The PALAMI system and the traveler app have separate terms.</p>
  <h2>Who we are</h2>
  <p>The website is operated by PALAMI <span class="todo">[registered company name and number to be added]</span>. For any question: <a href="mailto:hello@palami.io">hello@palami.io</a> or <a href="tel:+972542245627">+972-54-224-5627</a>.</p>
  <h2>What we collect</h2>
  <p>Only what you enter in the demo request form: full name, email, phone and agency name (optional). You don’t have to give us these details, but without them we can’t get back to you.</p>
  <p>The website does not use advertising or tracking cookies or third-party analytics. As with any website, the hosting provider keeps technical logs (such as IP address and browser type) for security and operation.</p>
  <h2>How we use it</h2>
  <p>To get back to you, schedule the demo and answer your questions. We won’t send you marketing emails without your explicit consent and we won’t sell or rent your details.</p>
  <h2>Who we share it with</h2>
  <p>Only service providers that help us run the website and receive requests (website hosting and the form and email service), and only for that purpose. <span class="todo">[provider names to be added before launch]</span> The information may be stored on servers outside Israel.</p>
  <h2>How long we keep it</h2>
  <p>For as long as needed to handle your request and our business relationship, and no longer than 24 months after your last contact, unless the law requires otherwise.</p>
  <h2>Your rights</h2>
  <p>You can ask to see, correct or delete your information. Email us at <a href="mailto:hello@palami.io">hello@palami.io</a> and we’ll handle it promptly.</p>
  <h2>Security</h2>
  <p>The website is served over HTTPS and access to requests is limited to the people who handle them.</p>
  <h2>Changes</h2>
  <p>If we update this policy, the new version will appear on this page with the date of the update.</p>
'''),
}

A11Y = {
'he': dict(title='הצהרת נגישות', desc='הצהרת הנגישות של האתר palami.io.', body='''
  <p>חשוב לנו שכל אחד ואחת יוכלו להשתמש באתר בקלות, כולל אנשים עם מוגבלות. השקענו בהנגשת האתר ונמשיך לשפר אותו.</p>
  <h2>רמת הנגישות</h2>
  <p>האתר נבנה בהתאם לתקן הישראלי ת״י 5568 ולהנחיות WCAG 2.2 ברמה AA.</p>
  <h2>מה עשינו באתר</h2>
  <ul>
    <li>אפשר לנווט בכל האתר במקלדת, עם סימון ברור של המיקום וקישור "דילוג לתוכן".</li>
    <li>מבנה כותרות ותגיות שקוראי מסך מבינים, וטקסט חלופי לתמונות שיש בהן מידע.</li>
    <li>ניגודיות צבעים מספקת, ומידע לא מועבר רק באמצעות צבע.</li>
    <li>האתר מותאם לנייד, ואפשר להגדיל את הטקסט עד 200% בלי לאבד תוכן.</li>
    <li>לאנימציה יש כפתור השהיה, והאתר מכבד את ההגדרה "הפחתת תנועה" במכשיר.</li>
    <li>לכל שדה בטופס יש תווית, והודעות השגיאה מוקראות ומסבירות מה לתקן.</li>
  </ul>
  <h2>מגבלות ידועות</h2>
  <p>צילומי המסך של המערכת מוצגים כתמונות בעברית, עם תיאור טקסטואלי של מה שמוצג בהם. אם משהו באתר לא נגיש לכם, נשמח לשמוע ולתקן.</p>
  <h2>איך בדקנו</h2>
  <p>האתר נבדק בכלי בדיקה אוטומטי (axe) ובבדיקה ידנית של ניווט במקלדת, בדפדפן Chrome במחשב ובגודל מסך של נייד.</p>
  <h2>פנייה בנושא נגישות</h2>
  <p>רכז/ת הנגישות: <span class="todo">[שם יעודכן]</span><br>אימייל: <a class="ltr" href="mailto:hello@palami.io">hello@palami.io</a><br>טלפון: <a class="ltr" href="tel:+972542245627">054-2245627</a></p>
  <p>כדי שנוכל לעזור מהר, כדאי לציין באיזה עמוד הבעיה ומה ניסיתם לעשות.</p>
'''),
'en': dict(title='Accessibility statement', desc='Accessibility statement for the palami.io website.', body='''
  <p>We want everyone to be able to use this website easily, including people with disabilities. We have worked to make it accessible and will keep improving it.</p>
  <h2>Accessibility level</h2>
  <p>The website was built to meet Israeli Standard IS 5568 and the WCAG 2.2 guidelines at level AA.</p>
  <h2>What we did</h2>
  <ul>
    <li>The whole site can be used with a keyboard, with a clear focus indicator and a “Skip to content” link.</li>
    <li>Headings and landmarks that screen readers understand, and alternative text for informative images.</li>
    <li>Sufficient color contrast, and information is never conveyed by color alone.</li>
    <li>The site adapts to mobile, and text can be enlarged up to 200% without losing content.</li>
    <li>The animation has a pause button and the site respects the device’s “reduce motion” setting.</li>
    <li>Every form field has a label, and error messages are announced and explain what to fix.</li>
  </ul>
  <h2>Known limitations</h2>
  <p>Screenshots of the system are images in Hebrew, with a text description of what they show. If anything on the site is not accessible to you, we’d like to hear about it and fix it.</p>
  <h2>How we tested</h2>
  <p>The site was tested with an automated checker (axe) and manual keyboard navigation, in Chrome on desktop and at mobile screen size.</p>
  <h2>Contact us about accessibility</h2>
  <p>Accessibility coordinator: <span class="todo">[name to be added]</span><br>Email: <a href="mailto:hello@palami.io">hello@palami.io</a><br>Phone: <a href="tel:+972542245627">+972-54-224-5627</a></p>
  <p>To help us respond quickly, please tell us which page the problem is on and what you were trying to do.</p>
'''),
}

def page(lang, d, name):
    c = dict(COMMON[lang])
    c['other'] = ('en/' if lang == 'he' else '../') + name
    c.update(d)
    c['updated'] = UPDATED[lang]
    return SHELL.format(**c)

for lang in ('he', 'en'):
    out = '' if lang == 'he' else 'en/'
    os.makedirs(out or '.', exist_ok=True)
    open(out + 'privacy.html', 'w', encoding='utf-8').write(page(lang, PRIVACY[lang], 'privacy.html'))
    open(out + 'accessibility.html', 'w', encoding='utf-8').write(page(lang, A11Y[lang], 'accessibility.html'))
print('ok')
