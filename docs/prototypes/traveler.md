> Source: docs/reference/prototype-traveler.html (artifact https://claude.ai/artifact/As9pjqQKDaz4zRjXPf13Pj)

# PALAMI traveler (נוסע) prototype: technical blueprint

Source file: /root/.claude/projects/-home-user-PalamiSales/3936a2d6-96a6-531f-b24a-0a41a5fbcfc8/tool-results/artifact-4fe2dfb4-1791471851-068e.html. It is one HTML file in vanilla JS (an IIFE). All state lives in one object `S`. Navigation is a string stack. `render()` rebuilds `#app` with innerHTML, and one delegated click listener handles every interaction. The page is Hebrew RTL (`dir="rtl" lang="he"`). Sample persona: דנה כהן, with agent רונית לוי at the fictional agency "מסעות הדרים". Trip: Barcelona, 12–19 Nov 2026, 4 passengers.

## 0. Shell and architecture

- **Desktop layout:** `.stage` shows a left guide panel ("מה רואה הנוסע"), a list of "נסו" deep links, and a 390×800 phone frame (`.device`, 10px border, 44px radius). At ≤760px the guide is hidden and the app fills the screen (100dvh).
- **Status bar:** a fake bar shows `9:41` and either `5G ▮▮▮` or `✈ מצב טיסה` when offline.
- **Offline bar (`.offbar`):** "אין חיבור. מוצג המידע ששמרת היום ב־09:12". It shows when `S.offline`, on every view except emergency.
- **Routing:** `S.stack` holds route strings, some with a parameter (`event:f1`, `doc:d2`, `ldoc:privacy`, `dgroup:tix`).
  - `go(v)`: the tab routes (`home`, `schedule`, `docs`, `info`) reset the stack to `[v]`. Any other route is pushed.
  - `back()` pops the stack.
  - `render()` looks up `V[route](param)`. If `!S.logged` it shows `login`. An unknown route falls back to home.
- **Font scale:** `--fs` is 16px, or 19.5px when `S.big` (big text).
- **Persistence:** only `S.big` is saved, to `localStorage['proto-trav']`.
- **Toast:** `toast(msg, undo?)` shows a snackbar for 3.2s. It can carry a "בטל" undo button (used for check-in). It uses role=status and sits above the tab bar (bottom 96px).
- **Placeholder actions:** many buttons only show a toast describing what the real app will do (call, WhatsApp, navigate, download, open airline site). A real build should implement the actions those toasts name: `tel:` links, `wa.me`, map deep links, file download, `.ics`.
- **Timers:**
  - Countdown refreshes every 1s (`#cd`).
  - Local-time element `#lt` refreshes every 15s.
  - After render, the view auto-scrolls the chat to the bottom, focuses the first OTP box or the password field, and scrolls the selected doc filter chip into view.

### Header variants (`top(kind, title)`)

- **Home:** the agency logo on the start side (a composite SVG: orange circle plus "מסעות הדרים / סוכנות לדוגמה"), then the SOS pill "חירום", the bell, and a menu icon button that goes to `more`.
- **Other views:** a back button (when stack >1), the title in h2, the bell (omitted for kind `nobell`), and the SOS pill. Both SOS and bell are always reachable.
- **Bell (`bellBtn`):** a round icon with a red count badge for unread notifications. The aria-label reads "התראות, N חדשות". `addNotif()` adds an item and plays a one-time ring animation (class `ring`, 0.8s).

### Tab bar (`tabs(active)`)

Four columns. Every tab resets the stack.

| Route | Icon | Label |
|---|---|---|
| `home` | home | בית |
| `schedule` | cal | לו״ז |
| `docs` | doc | מסמכים |
| `info` | info | מידע |

- The active tab gets `aria-current="page"`, the brand color and bold text.
- The bar appears on home, schedule, docs, info, dgroup (as home), notifs (no active tab), add (as docs) and addev (as schedule).
- It is absent on event, doc, otp, taxi, emergency, chat, legal, ldoc, more, offline, settings, agent, trips and cal.
- (Code also has a `map` route that uses `tabs('map')`, but no tab or link reaches it. It is dead code.)

### Global overlay: terms-update sheet (`.tsheet`)

Shows when `S.termsNotice`, on every view except ldoc and emergency.
- Bottom sheet, title "עדכנו את מדיניות הפרטיות". Body: "מה השתנה: הוספנו ספק חדש לשליחת הודעות WhatsApp. אין שום דבר שצריך לעשות."
- Link "לקריאת המדיניות המעודכנת" goes to `ldoc:privacy`.
- Button "הבנתי" (`termsok`): clears the notice, sets `S.ver={terms:'1.0', privacy:'1.1', at:'היום · אחרי "הבנתי"'}`, and toasts "תודה. נשמר".
- Footnote: "ההודעה מופיעה פעם אחת, ונשמרת גם בפעמון."
- Demo trigger `termsdemo`: sets the notice, resets the stack to home, and adds the notification "עדכנו את מדיניות הפרטיות" (go `ldoc:privacy`).

## 1. Screens

### login (shown when `!S.logged`)

Three steps via `S.lstep`.

**`login` step**
- Logo, mascot image (`brand/mascot/mascot.png`, alt "הבונה של PALAMI מחזיק מזוודה וטלפון").
- Headline "ברצלונה מחכה לך" (the next trip name), subline "כניסה כדי לראות את הנסיעה".
- Field "מספר נייד" (tel, mono, prefilled 050-555-4417, autocomplete username).
- Field "סיסמה" (password, placeholder "הסיסמה שלך").
- Button "כניסה": an empty password toasts "צריך להקליד סיסמה". Otherwise it logs in, sets stack to home, and toasts "ברוכה הבאה, דנה. נשארת מחוברת במכשיר הזה".
- Text "✓ אשאר מחובר במכשיר הזה" and a "שכחתי סיסמה" button (goes to the code step).
- `.first` card: "פעם ראשונה כאן?" / "נשלח קוד ב־WhatsApp, ותבחרי סיסמה" with button "שלחו לי קוד", which goes to the code step.

**`code` step**
- "שלחנו קוד ב־WhatsApp" / "למספר שמסתיים ב־4417".
- Six single-digit OTP inputs, LTR. Each strips non-digits and auto-advances. When all six are filled and the user is not logged in, it goes to `setpw`. The demo accepts any code.

**`setpw` step**
- "בחרי סיסמה" / "6 תווים לפחות. בפעמים הבאות: נייד וסיסמה". Field "סיסמה חדשה".
- Button "שמירה וכניסה" validates:
  - fewer than 6 chars: "צריך לפחות 6 תווים"
  - repeated single digit, or starts with 123456 or 654321: "הסיסמה הזו נפוצה מדי. נסי אחרת"
  - On success: logs in and toasts "הסיסמה נשמרה. ברוכה הבאה".
- `<details class="legal-note">` with summary "בכניסה את מסכימה ל<u>תנאי השימוש ולמדיניות הפרטיות</u>", which expands to a short privacy blurb. This is consent at first login, versioned in `S.ver` as `at:'2.10.2026 · בכניסה הראשונה'`.

The footer "מופעל על ידי [PALAMI wordmark]" appears on all three steps.

### home

- **Row:** "בוקר טוב, דנה" plus a trip switcher button (`.ttog`, ghost, trip name and caret, aria-haspopup listbox). It toggles `S.tripDD`, a dropdown `.tdd` built by `tripPicker()`:
  - Lists only trips that are `live` or `ended`. Each shows name and dates.
  - The current trip gets a check icon. Ended trips get "הסתיימה" and muted text.
  - Footnote: "נסיעות שרונית עוד מכינה יופיעו כאן כשהן מוכנות".
  - Picking a trip sets `S.trip`, resets to home, and toasts "עברת לנסיעה: X".
  - Clicking outside closes it.
- **Trip not live (`notLive()`):**
  - Ended trip: mascot, "name · dates", "הנסיעה הסתיימה. המסמכים והלו״ז נשארים כאן לצפייה.", and a button "חזרה לברצלונה".
  - In-preparation trip: "רונית עדיין מכינה את הנסיעה הזו. כשהיא תהיה מוכנה תקבלי הודעה, והכול יופיע כאן." and a button "שאלה לרונית" (goes to chat).
  - Schedule and docs use the same notLive() view.

**Phase `before` (default)**
1. Brand countdown card (`.card.brand.cdc`): label "עד ההמראה". A live countdown shows four boxes for days, hours, minutes and seconds, with Hebrew singular/plural ("יום/ימים", "שעה/שעות", "דקה/דקות", "שנייה/שניות"), role=timer. The target is now + 3d 4h 22m 45s. Below it: `t.when` = "יום ה׳, 12 בנובמבר · 06:10 שעון ישראל".
2. Important documents (`qdocs()`, see below).
3. "האירוע הבא" card (goes to `event:f1`): plane icon, "טיסה לברצלונה", "LY 395 · טרמינל 3 · 4 נוסעים". A kv list: המראה 06:10 שעון ישראל; נחיתה 10:05 שעון ברצלונה; הזמנה X7KQ2P (mono). Footnote "עודכן לפני יומיים ע״י רונית".
4. Primary full button "הצג את כרטיס הטיסה" (goes to `doc:d2`).
5. Check-in card:
   - Info-tinted plane icon, "צ'ק-אין לטיסה", "ייפתח מחר ב־06:10, לפי כלל של חברת התעופה".
   - Buttons "לאתר החברה" (toast) and "ביצעתי צ'ק-אין". The latter sets `S.checkin` and toasts "מעולה. לא נשלח לך עוד תזכורת" with undo.
   - After check-in: "סימנת שביצעת. נתראה בשדה!" and a `.vk` check with "בוצע".

**Phase `during`**
1. Day board (`dboard()`, brand card):
   - "יום 3 מתוך 8" and "שבת 14.11". A progress bar at 37.5% (role=progressbar).
   - Three tiles:
     - "עכשיו": live Barcelona time via `Intl` Europe/Madrid, plus the offset text with "מישראל" stripped ("שעה פחות" etc.).
     - "היום 22° שמשי".
     - A button "1 אירו / 4.05 ₪ / מחשבון|סגירה" that toggles `S.fx`.
   - Currency converter (shown when open): `.fxrow` with an input labeled אירו (inputmode decimal, default 10) "=" and a live ₪ result: `round(n*4.05, 2)` in he-IL locale, accepting a comma as decimal point. Note: "שער יציג של בנק ישראל · עודכן היום 09:00".
   - Footer: "מחר 19° וגשם קל. כדאי מטרייה."
2. "האירוע הבא" (`nextDuring`): the car pickup c1, "היום · 10:00 שעון ברצלונה" and its sub.
3. qdocs.

**Phase `after`**
1. Brand card "הנסיעה הסתיימה" / "מקווים שנהניתם בברצלונה!" / "להזמנת הטיול הבא, צרו קשר: רונית לוי · 03-555-0142".
   - Buttons "התקשרות" (`.acb`, white) and "WhatsApp" (`.acg`, translucent).
   - Note "הנוסח נקבע על ידי מסעות הדרים", meaning the agency configures the copy.
2. qdocs.

**Always on home**
- Chat card (`.chatrow`): agent avatar, "שאלה לרונית?" / "צ'אט עם הסוכנת שלך · עונה בדרך כלל תוך שעתיים", chat icon. Goes to chat.
- Demo phase switcher: segmented control "הדמיה: שלב הנסיעה" with לפני / במהלך / אחרי. It sets the phase, forces the trip to bcn, closes the dropdown and fx, and scrolls to top.
- Footer "מופעל על ידי PALAMI".

**qdocs ("מסמכים חשובים") card**
- Header link "לכל המסמכים (N) ‹" goes to docs.
- A 3-column grid of tiles. Each item is either a doc id (goes to `doc:id`) or a group `g:tix` / `g:fl` (goes to `dgroup:x`, with a count badge `.qn` showing the number of docs in that category).
- Contents vary by phase:
  - before: כרטיס טיסה (d2), מלון (d3), ביטוח (d4), רכב (d5), הסעה (d7), אטרקציות (g:tix)
  - during: מלון, רכב, ביטוח, אטרקציות, הסעה, טיסה הביתה (d1)
  - after: טיסות (g:fl), מלון, ביטוח, רכב, אטרקציות, הסעה

### dgroup:{tix|fl}

- Title "אטרקציות" or "טיסות". Text: "N {title} בנסיעה הזו, לפי התאריך. לחיצה פותחת את המסמך."
- Rows (`.trow`):
  - A date block parsed from sort key `k` (YYYYMMDDhhmm), showing the day and the Hebrew month abbreviation from `MON`.
  - Title and docMeta.
  - A time pill (`tm`) when present.
- Ghost button "לכל המסמכים" at the bottom.

### trips ("הנסיעות שלי", reached from the more menu)

- "הקרובה": trip row bcn with pill "עוד 3 ימים" (brand).
- "הסתיימו": ath with pill "הסתיימה".
- The current trip is outlined and its date block filled with the brand color.
- Info banner: "כאן מופיעות נסיעות שרונית כבר שלחה לך, ונסיעות שהסתיימו. נסיעה שעוד בהכנה תופיע כשתהיה מוכנה."
- Clicking a row switches the trip.

### schedule ("לוח זמנים")

- Top row:
  - Segmented "יום" / "שבוע" (`S.week`).
  - Primary small button "+ הוספה ללו״ז" (goes to addev).
  - `.offnote` button (goes to cal): "הוספה ליומן הטלפון" / "הלו״ז ייכנס ליומן ויתעדכן לבד". When connected it reads "הלו״ז ביומן הטלפון שלך" / "מתעדכן לבד · {provider}".
- **Day mode:**
  - Day chips for 12–19, each showing the weekday letter and number (ה׳ 12 … ה׳ 19).
  - Note "השעות לפי המקום שבו מתקיים האירוע".
  - A timeline (`.tl`) of the day's events, built by `evRow`: a time column, a vertical line with a dot, and a clickable card with the title, an "עודכן" warn pill when `upd`, a "הוסף על ידי X" badge when `by`, and "tz · sub" (warn-colored when `unv`).
  - Empty day: sun icon and "יום חופשי. אין אירועים מתוכננים."
- **Week mode:**
  - "12–19 בנובמבר · גוללים לצדדים · לחיצה על יום פותחת אותו".
  - A horizontal scroll-snap row of 104px columns. Each column has a header (`.wch`, weekday and big date) that opens that day in day mode, plus event chips (`.wcb`: mono time and the first part of the title before " · ", warn background when updated), or "חופשי" when empty.

### cal ("יומן הטלפון")

- Explainer: "הלו״ז שלך ביומן של הטלפון". Subscribe once and events auto-update. Sync is one-way, from PALAMI to the phone calendar.
- When connected: banner "מחובר ל{X}" with button "הפסקת הסנכרון". This toasts "הסנכרון הופסק והאירועים יימחקו מ{X}".
- Menu with "יומן אייפון (Apple)", "Google Calendar", "Outlook". Picking one sets `S.calOn` and toasts "הלו״ז נוסף ל… ויתעדכן לבד".
- Note: per-event add is also available from "פרטי האירוע". The real build would use a webcal/ICS subscription feed.

### event:{id}

- Card: icon, title, "t tz". kv list of `e.kv`; if `addr` exists and no כתובת row, a כתובת row is appended (styled `.addr`).
- Banners:
  - `upd`: warn "השתנה אתמול / שעת האיסוף עודכנה מ־10:45 ל־11:00."
  - `unv`: warn "הכתובת לא אומתה / אפשר לשאול את רונית."
  - `by`: info "הוסף על ידי X / רונית רואה את זה בתיק. אפשר לערוך או למחוק."
- `doc`: primary button "פתחי את המסמך" (goes to `doc:id`).
- If addr exists and is verified, a two-button row:
  - "ניווט": if `S.navApp` is set, it is a direct link. Otherwise it toggles a 3-tile picker (Waze #33ccff, Google Maps #1a73e8, Apple Maps #333) with the prompt "באיזו אפליקציה לנווט? נזכור את הבחירה. באנדרואיד הטלפון שואל בעצמו". Picking saves `S.navApp` and toasts "נזכור את הבחירה. אפשר לשנות בהגדרות". Once set, a note reads "הניווט נפתח ב־X. אפשר לשנות בהגדרות".
  - "העתקת כתובת": clipboard copy and toast "הכתובת הועתקה".
- Deep links:
  - Waze: `https://waze.com/ul?q=…&navigate=yes`
  - Google: `https://www.google.com/maps/dir/?api=1&destination=…`
  - Apple: `https://maps.apple.com/?daddr=…`
- Ghost button "הוספת האירוע ליומן" (single-event ICS).
- Footer: "מקור: {src}", for example "אישור-הזמנת-טיסה.pdf · שובץ אוטומטית · 2 באוק׳". This shows provenance.

### docs ("מסמכים")

- `.offnote` with a vk check: "כל המסמכים שמורים בטלפון" (offline: "אין רשת עכשיו. הכול זמין מהטלפון") / "עובד גם בלי אינטרנט · איך זה עובד". Goes to offline.
- Primary "+ הוספת מסמך" (goes to add). Note "הזמנתם משהו לבד? מעלים כאן, והכול נשאר במקום אחד."
- Swipeable filter chips: הכול, טיסות(flight), לינה(hotel), אטרקציות(tix), רכב(car), ביטוח(ins), אחר(other). Only categories that have docs are shown.
- List sorted by `k` ascending (insurance has k "0", so it comes first).
- Each `.doc` row has:
  - an icon
  - title `t`
  - small meta "dt · who · x"
  - a "הוספת בעצמך" badge when `by`
  - a tail: a warn pill with `neu` text ("עודכן", "חדש", "להשלמה"), or a lock icon when `lock && !unlocked`, or a `.vk` check ("שמור בטלפון")
- Empty filter: "אין מסמכים מהסוג הזה בנסיעה."
- Footer note: "לפי התאריך. בכל שורה: מה זה, מתי, ולמי."

### doc:{id}

- If the doc is locked and not unlocked, the route is replaced with otp. (No sample doc has `lock` set, but the OTP flow targets d4, the insurance policy.)
- `.paper` mock preview, LTR mono with grey skeleton lines. Header depends on category: "SECURITAS TRAVEL · POLICY", "HOTEL MAR BLAU · VOUCHER", "BOOKING CONFIRMATION · X7KQ2P" or "VOUCHER". Body shows "COHEN / DANA" and the dates.
- Buttons "הורדה" (primary) and "שמור בטלפון ✓" (cloud icon; toast "המסמך כבר שמור בטלפון. הוא זמין גם בלי אינטרנט").
- docMeta text, then "שם הקובץ בהורדה: {name}", a human-readable download filename such as "כרטיס טיסה · LY395 · דנה כהן".

### otp ("מסמך מוגן")

- Lock icon, "כדי לפתוח את פוליסת הביטוח", "שלחנו קוד בן 6 ספרות למספר שמסתיים ב־4417".
- Six inputs. When complete: `S.unlocked=true`, the route is replaced with `doc:d4`, and a toast "אומת".
- Button "שלחו לי קוד חדש".

### emergency ("חירום · ספרד")

- Red header (`--bad`) with a white pill "עובד בלי אינטרנט". The offline bar is suppressed here.
- `.ecard` list, each with a label, a big mono number, a subline and a "התקשר" button:
  1. "חירום מקומי: משטרה, אמבולנס, כיבוי": 112 (2.2em, red, danger button). Subline "מספר החירום באיחוד האירופי".
  2. "מוקד הביטוח 24/7": +972-3-555-0170, "Securitas Travel · פוליסה TRV-4482-1190".
  3. "הסוכנות שלך 24/7": 03-555-0199, "מסעות הדרים · קו חירום".
  4. Only when `agentEPhone`: "הסוכנת שלך · נייד אישי" 054-555-0186, "רונית לוי".
  5. "נציגות ישראל בספרד": "מהמאגר", "שגרירות ישראל במדריד · נבדק 9/2026".
  6. "המלון של הלילה": +34 93 555 0142, "Hotel Mar Blau".
- Doc row "פוליסת הביטוח שלך / Securitas · TRV-4482-1190 · שמורה בטלפון" (goes to doc:d4).
- Button "הכתובת של המלון לנהג מונית" (goes to taxi).
- Note "המספרים במסך לדוגמה, חוץ מ־112."

### taxi ("כתובת לנהג")

- Large LTR card in the local language (Spanish), with a `lang` attribute. Toggle to English (`S.taxiEn`).
  - Spanish line: "Por favor, lléveme a esta dirección:" / English: "Please take me to this address:"
  - **Hotel Mar Blau** (2em, weight 800), "Carrer de Pujades 145", "08005 Barcelona", "Tel. +34 93 555 0142".
- Hebrew explainer: "מראים את המסך לנהג. כתוב בספרדית, כי המלון של הלילה בספרד: "בבקשה, קחו אותי לכתובת הזו". עובד גם בלי אינטרנט." The language button reads "English" or "Español".
- Primary "ניווט לכתובת" uses the same nav-app picker logic.
- Buttons "העתקת כתובת" and "התקשרות למלון".

### chat

- Custom header: back, avatar, "רונית · מסעות הדרים", "עונה בדרך כלל תוך שעתיים, א׳–ה׳ 9:00–17:00", SOS.
- Note "שיחה על {trip} · גלויה לכל הנוסעים בנסיעה". The chat is per trip and shared with all passengers.
- Bubbles:
  - Mine (`.msg.me`): brand color, aligned to the start side, which is the right side in RTL.
  - Agent (`.them`): white with shadow, aligned to the end side, with "רונית · time" under each.
- Composer form: attach button (toast), input "כתבי הודעה…", "שלחי".
  - Offline: the message is queued with time "ממתינה לרשת".
  - Online: the message is added with "עכשיו", and after 1.4s an auto-reply arrives: "קיבלתי, תודה! בודקת ועונה בהקדם".

### more ("עוד")

- Menu: הנסיעות שלי (trips), שימוש בלי אינטרנט (offline), התראות ותצוגה (settings), הסוכנת שלך (agent), פרטיות ונגישות (legal).
- Ghost button "יציאה מהחשבון": logs out and returns to the login step.

### notifs ("התראות", no bell in header)

- "N לא נקראו" and "סמני הכול כנקרא".
- Rows (`.nrow`): unread rows get a 4px brand border on the start side and bold text. Each shows an icon, text, and "{trip name} · at".
- Clicking marks the item read, resets the stack to `['home', go]`, and deep-links to the target. Back then returns to home.
- Footnote "גם מה שנשלח אלייך ב־WhatsApp או באימייל מופיע כאן." The in-app inbox mirrors all channels.

### add ("הוספת מסמך", nobell)

- If `!S.travUp` (agency disabled traveler uploads): empty state "רוצים להוסיף מסמך? … שלחו את המסמך לרונית" with a "שליחה לרונית" button.
- **Share box ("עם מי לשתף?"):** radio chips כל הנוסעים / רק אני (default `me`) / נוסעים שבחרת.
  - "pick" reveals toggle chips for the other passengers in `PAXN` (אורי כהן, יואב כהן, נועה כהן).
  - Note: "מופיע כי בנסיעה 4 נוסעים. כשנוסעים לבד, לא צריך לבחור. רונית תמיד רואה, ואפשר לשנות גם אחר כך, מפרטי המסמך."
- **Pickers:**
  - "📷 צילום": file input, accept image/*, capture=environment.
  - "📎 קובץ": multiple files.
  - Chosen files go to `S.pend`.
  - Demo button "הדמיה: בחירת 4 קבצים לדוגמה" adds IMG_5520.jpg, policy_2026.pdf, sixt-voucher.pdf, scan_blurry.jpg.
- **Pending card:**
  - "נבחר קובץ אחד" or "נבחרו N קבצים". Each file is listed with an × remove button.
  - "משותף עם: {label}".
  - Primary "הוספה למסמכים" (`addconfirm`) calls `upload()`. Ghost "ביטול" clears the list.
- **Processing (`upload`):** each file gets state `p` ("קורא את הקובץ…") and resolves after 1200 + j×700 ms:
  - Extension not pdf/jpg/jpeg/png/heic/webp: state `x`, banner "אי אפשר להוסיף את "name"" / "אפשר להוסיף PDF או תמונה."
  - Name contains "sixt": state `need`. A copper-outlined card (`.vk.attn` "!") titled "רכב שכור · Europcar": "לא הצלחנו לקרוא בוודאות את **שעת החזרת הרכב**, ולכן הרכב עוד לא נוסף ללו״ז. מה כתוב בשובר?" A time field labeled "שעת החזרה, 18/11" and "שמירה". Saving:
    - creates event (day 16, 09:00, "איסוף רכב · Europcar", sub "תחנת Sants · החזרה 18/11 ב־{t}")
    - creates doc (neu "חדש")
    - sets the message "תודה! הרכב נוסף ללו״ז: … התזכורת להחזרה תגיע בזמן" and toasts "נשמר. הרכב בלו״ז"
  - Name contains "blur": state `x`, "התמונה לא ברורה" / "לא הצלחנו לקרוא את … נסי לצלם שוב, באור טוב ובלי צל."
  - Otherwise: cycles through mock classification results `RES`:
    1. Picasso museum ticket (tix). It becomes an event plus a doc, with message "זה אירוע, אז הוא נוסף לבד גם ללו״ז, ביום ב׳ 16/11 ב־10:00".
    2. Cancellation insurance הפניקס (ins). Doc only: "נשמר במסמכים. זה מסמך בלבד, בלי אירוע, ולכן לא נוסף ללו״ז".
    3. Sixt car (other). Event plus doc.
    - Each success pushes a doc (`neu:'חדש'`, `by:'דנה'`, `who` from `whoLbl()`) and a notification "המסמך נקלט: …" that links to the event or doc.
- **Success card:** vk check, name, "הועלה בשם {orig}" (mono), the message, "משותף: {label}", and "לאירוע בלו״ז" when an event was created.
- **Finish:** "סיום וחזרה למסמכים" appears when nothing is still processing.
  - Unresolved `need` items become docs with neu "להשלמה" and dt "16–18 בנוב׳ · חסרה שעת ההחזרה".
  - Navigates to docs and toasts "N מסמכים נשמרו במסמכים" (or "לא נוספו מסמכים").
  - Hint when items are unresolved: "אפשר להשלים את הפרט החסר גם אחר כך, מפרטי המסמך."
- **Info banner:** "מעלים רק את המסמך: אם זה כרטיס או הזמנה (הופעה, מסעדה, רכב), המערכת תוסיף לבד גם אירוע ללו״ז. אם זה מסמך בלבד, כמו ביטוח, הוא נשמר במסמכים וזהו."

### addev ("הוספה ללו״ז")

- Also gated by `travUp`.
- Fields:
  - "מה *" (default פארק גואל)
  - "יום *" (select of DAYS, default `S.day` or 15)
  - "שעת התחלה *" (10:00) and "שעת סיום" (12:00), side by side
  - "מקום (לא חובה)" (placeholder "כתובת או שם המקום")
- Optional document row: "מסמך (לא חובה)" / "למשל כרטיס כניסה או אישור הזמנה" with a "📎 צירוף" file input. When attached it shows "מצורף: name" and "הסרה". Demo button "הדמיה: צירוף כרטיס לדוגמה" attaches IMG_7781.jpg.
- Submit "הוספה ללו״ז":
  - Validates that a name exists ("מה מוסיפים? צריך שם") and that end > start ("שעת הסיום לפני שעת ההתחלה").
  - Creates EV `{by:'דנה', ic:'walk', kv:[['מתי'],['שעות'],['כתובת'?]]}`. With an attachment it also creates a doc (cat other).
  - Switches to schedule day view on that day and toasts "נוסף ללו״ז ביום X/11. רונית רואה את זה בתיק".
- Note: "יופיע בלו״ז עם התגית "הוסף על ידי דנה"… לשנות טיסה או מלון שרונית הזמינה אפשר רק דרכה."

### info ("מידע שימושי")

- **Weather card:** "מזג אוויר בברצלונה", big 19°, "בהיר חלקית · 12–19 בנובמבר: 13°–20°", source line. Below a divider: "השעה עכשיו בברצלונה", the offset text ("שעה פחות מישראל"), and the live time.
- **Tips card:** "טיפים מרונית" (free text: metro, T-casual card, dinner after 20:30), "רונית כתבה את זה בתיק הנסיעה · עודכן אתמול".
- **Packing list ("רשימת אריזה"):** "משותפת לך ולרונית: שתיכן יכולות להוסיף ולמחוק. הסימון "ארזתי" הוא רק שלך".
  - Each row: text, source line ("הצעה אוטומטית לפי היעד והעונה" or "נוסף ע״י X"), a toggle for packed state (per user), and an × delete button (toast "הוסר מהרשימה").
  - Add input "להוסיף פריט" with "הוספה". Empty input toasts "מה להוסיף?". A new item gets source דנה and toasts "נוסף לרשימה. רונית רואה את זה בתיק".

### offline ("בלי אינטרנט")

- "הכול שמור בטלפון / עודכן לבד היום ב־09:12".
- Banner "לא צריך לעשות כלום". Everything is cached whenever the trip opens online: schedule, addresses, phones, booking numbers, emergency screen, all documents including the policy.
- Toggle "הדמיית מצב טיסה" (`S.offline`).
- "מה נשמר": "הכול: N מסמכים, הלו״ז, מסך החירום ופרטי הסוכנת. המידע מוצפן בטלפון ונמחק לבד אם מתנתקים מהחשבון."

### settings ("התראות ותצוגה")

- **ניווט:** select "אפליקציית ניווט" with לפי הטלפון / Waze / Google Maps / Apple Maps. Note "באנדרואיד: לפי הטלפון. באייפון: נבחרת בפעם הראשונה".
- **איך לעדכן אותי (channels):** toggles for "התראה בטלפון (Push)", "WhatsApp", "אימייל". At least one must stay on: turning off the last one forces mail back on and toasts "צריך לפחות ערוץ אחד. השארנו אימייל".
- **מה לשלוח לי:**
  - Locked toggle "שינויים בטיסות ובמסמכים / תמיד נשלח, חשוב לביטחון שלך". Opacity 0.6; clicking toasts "התראה קריטית. אי אפשר לכבות אותה".
  - "תזכורות צ'ק-אין ויציאה לשדה" (checkin)
  - "תדריך בוקר ב־08:00 / מה מחכה היום: האירועים, השעות ומזג האוויר" (morning)
  - "תזכורת לפני אירועים" (events)
  - "הצעות לנסיעות הבאות / פרסומת מהסוכנות. נשלח רק אם הפעלת" (offers, marketing opt-in). Toggling it toasts the consent status.
- **שעות שקט:** "לא להעיר אותי בין 22:00–07:00", "לפי השעה במקום שבו את נמצאת" (display only).
- **טקסט גדול:** toggle "מגדיל את כל הטקסט באפליקציה", persisted.

### agent ("הסוכנת שלך")

- Large avatar (an SVG illustration, or initials "רל" when there is no photo), "רונית לוי", "מסעות הדרים", pill "● זמינה עכשיו", "א׳–ה׳ 9:00–17:00 · עונה בדרך כלל תוך שעתיים".
- Buttons: "צ'אט עם רונית" (primary), "התקשרי · 03-555-0142", "WhatsApp".
- When `agentEPhone`: ecard "בחירום, בזמן הנסיעה" 054-555-0186, "הנייד האישי של רונית. מוצג רק עד סוף הנסיעה".
- Demo toggles: no photo (falls back to initials) and the emergency phone on or off.

### legal ("פרטיות ונגישות") and ldoc:{privacy|terms|access}

- legal:
  - Version line: "הגרסה שראית: תנאי שימוש {ver.terms} · מדיניות פרטיות {ver.privacy} · {ver.at}".
  - Card "המידע שלך, בקצרה".
  - Card "לעיין, לתקן או למחוק" / "רונית מטפלת בזה בשבילך" with button "כתיבה לרונית".
  - Menu: מדיניות הפרטיות המלאה, תנאי שימוש, הצהרת נגישות.
- ldoc: info banner "טיוטה לבדיקה משפטית" (highlighted placeholders are filled once by the agency admin), then `<article class="ldoc">` with the full HTML.
  - `.sum` "בקצרה" box (cream).
  - `.fill` spans (warn-soft highlight) mark agency-specific placeholders: agency name, ח.פ., address, privacy email, retention "12 חודשים", accessibility coordinator, etc.
- Key policy facts to carry over:
  - The agency is the data controller; PALAMI is the processor.
  - Retention is 12 months after return. Then data is deleted, and deleted from backups within 30 days.
  - Audit logs are kept 24 months. Consent records are kept 7 years.
  - Documents are not used to train AI models.
  - No GPS, contacts or payment data is collected.
  - A new device requires password plus OTP.
  - Children without phones are linked to an adult.
  - The accessibility target is WCAG 2.2 AA (ת״י 5568). The policy says reduced motion is respected and there is no flashing.

## 2. Data model

### S (app state)

- **Session:** `logged:false`, `lstep:'login'|'code'|'setpw'`, `unlocked` (secure-doc OTP passed).
- **Navigation:** `stack:['home']`, `trip:'bcn'`, `tripDD`, `day:'12'`, `week:false`, `docf:'all'`, `navOpen`, `navApp:null|'waze'|'google'|'apple'`.
- **Phase / demo:** `phase:'before'|'during'|'after'`, `offline`, `big`, `checkin`, `fx`, `fxv`, `taxiEn`, `calOn:null|'Google Calendar'…`.
- **Agency configuration flags:**
  - `agentPhoto:true`
  - `agentEPhone:true`
  - `travUp:true`: the traveler may upload documents and add events.
- **Notifications:** `notifs[] {id, t, at, un, go, ic}`. Samples:
  - t1 "הטיסה LY 395: איסוף ההסעה עודכן ל־11:00" (go event:t1, ic bus)
  - t2 "הצ'ק־אין לטיסה LY 395 ייפתח מחר ב־06:10" (home, plane)
  - t3 "רונית ענתה לך בצ'אט" (chat)
  - t4 "כרטיס הטיסה שלך עודכן" (doc:d2)
  - `ring` (bell animation flag)
- **Preferences:** `notif:{checkin:true, morning:true, events:false, offers:true}` and `chan:{push:true, wa:true, mail:false}`.
- **Chat:** `chat[] {me:bool, t, at}`. Three seed messages about a stroller on the airport shuttle and self-bought insurance.
- **Packing:** `packing:{pass:true, adapt:false, umb:false, meds:true}` holds per-user packed state. `packList[[id, text, source]]` holds the shared items; source is `'auto'` or a name. Seeds: דרכונים בתוקף; מתאם חשמל (תקע אירופאי); מטרייה קטנה; תרופות קבועות; נעליים נוחות להליכה בעיר (רונית).
- **Upload flow:**
  - `share:'all'|'me'|'pick'`, `sharePick:{ori, yoav, noa}`
  - `pend[]` (file names)
  - `adds[] {orig, st:'p'|'ok'|'need'|'x', sh, name, fn, who, m, t, ev}`
  - `evFile`
- **Legal:** `termsNotice`, `ver:{terms:'1.0', privacy:'1.0', at:'2.10.2026 · בכניסה הראשונה'}`.

### TRIPS (map keyed by id)

Fields: `{name, dates, pax, live, ended?, d, m, count?, when?}`. `d` and `m` are the day number and month abbreviation for the date block.

| id | name | dates | pax | status |
|---|---|---|---|---|
| bcn | ברצלונה | 12–19 בנובמבר 2026 | 4 | live; count "עוד 3 ימים"; when "יום ה׳, 12 בנובמבר · 06:10 שעון ישראל" |
| rom | רומא ופירנצה | 4–11 במרץ 2027 | 2 | not live (in prep, hidden from the picker) |
| cre | כרתים | 9–16 באוגוסט 2027 | 5 | not live |
| ath | אתונה | 18–23 במאי 2026 | 2 | ended |

Visibility rule: a trip is shown only when it has been sent (live) or has ended.

### DAYS

`[['12','ה׳'],['13','ו׳'],['14','ש׳'],['15','א׳'],['16','ב׳'],['17','ג׳'],['18','ד׳'],['19','ה׳']]`

### EV (events keyed by id)

Fields:
- `day`, `t` ("HH:MM"), `tz` (for example "שעון ישראל" or "שעון ברצלונה"; times are shown in local time)
- `ic`, `title`, `sub`
- `kv[[label, value]]`
- `addr?`, `doc?` (doc id)
- `src` (provenance string)
- `upd?` (updated flag), `unv?` (address unverified), `by?` (added by a traveler)

| id | day | time | title | key details |
|---|---|---|---|---|
| f1 | 12 | 06:10 | המראה · LY 395 | TLV T3 to BCN T1, landing 10:05, booking X7KQ2P, 23 kg baggage, doc d1, addr נמל התעופה בן גוריון, טרמינל 3 |
| f2 | 12 | 10:05 | נחיתה בברצלונה | |
| t1 | 12 | 11:00 | הסעה למלון | upd (was 10:45); meet in arrivals hall, sign "כהן"; driver +34 611 220 118; "4 + עגלה"; doc d7 |
| h1 | 12 | 15:00 | צ'ק-אין · Hotel Mar Blau | Carrer de Pujades 145; confirmation 88412; 2 family rooms; breakfast; crib request; checkout 19/11 11:00; doc d3 |
| r1 | 12 | 20:30 | ארוחת ערב · El Pati | by דנה; unv (no address) |
| g1 | 13 | 09:45 | סיור מודרך ברובע הגותי | Plaça Nova 5; 09:45–12:45; Hebrew guide; TR-5521; doc d8 |
| l1 | 13 | 13:00 | ארוחת צהריים | Carrer del Bisbe 8; "הוזן ע״י רונית"; no doc |
| c1 | 14 | 10:00 | איסוף רכב שכור | El Prat T1; return 19/11 12:30; family car; driver דנה כהן; doc d5 |
| m1 | 14 | 21:00 | משחק כדורגל | Camp Nou; gates open 19:30; gate 9; row 12, 4 seats; doc d6 |
| o1 | 19 | 11:00 | צ'ק-אאוט מהמלון | |
| f3 | 19 | 16:20 | טיסה הביתה · LY 396 | lands 21:05 Israel time |

`MAPDAY` lists route stops per day for the unused map route.

### DOCS (array)

Fields:
- `id`
- `cat`: flight / hotel / tix / car / ins / other
- `ic`
- `t` (display title), `dt` (human date string), `who` (share label), `x?` (extra, for example "3 מושבים")
- `k`: sort key "YYYYMMDDhhmm", or "0" for whole-trip docs
- `tm?` (time pill)
- `neu?` (status pill text)
- `by?` (uploaded by traveler)
- `off` (available offline)
- `name` (download filename)
- `lock?` (requires OTP)

| id | cat | title | dt | who | other |
|---|---|---|---|---|---|
| d4 | ins | ביטוח נסיעות · Securitas | כל הנסיעה | רק לך | by דנה |
| d1 | flight | טיסות הלוך וחזור · LY 395 | 12–19 בנוב׳ | לכל הנוסעים | |
| d2 | flight | כרטיס טיסה הלוך · LY 395 | ה׳ 12 בנוב׳ · 06:10 | רק לך | neu "עודכן" |
| d7 | other | הסעה · שדה התעופה–המלון | 11:00 | | neu "עודכן" |
| d3 | hotel | מלון Hotel Mar Blau | 12–19 בנוב׳ · 7 לילות | | |
| d8 | tix | סיור מודרך · הרובע הגותי | | | |
| d9 | tix | הופעה · פאלאו דה לה מוזיקה | ו׳ 13 בנוב׳ · 20:30 | רק לך | by דנה |
| d5 | car | רכב שכור · Sixt | | | |
| d6 | tix | כדורגל · ברצלונה–ריאל מדריד | ש׳ 14 בנוב׳ · 21:00 | לך, לאורי וליואב | x "3 מושבים" |

**Sharing labels (`whoLbl()`):**
- "לכל הנוסעים"
- "רק לך"
- "לך, לאורי וליואב": built with the Hebrew ל prefix and ו before the last name.

`shareLbl()` is a second variant used in the upload cards ("כל הנוסעים", "רק את", "את ואורי, יואב").

### Other constants

- **PAXN:** `[['ori','אורי כהן'],['yoav','יואב כהן'],['noa','נועה כהן']]`. These are the other passengers, excluding the current user.
- **QD / DG:** per-phase quick-document tiles and the groups (`tix` אטרקציות, `fl` טיסות).
- **FX:** 4.05 (EUR to ILS).
- **MON:** Hebrew month abbreviations.
- **LEGAL:** `{privacy, terms, access}`, each `{t, h (html)}`.
- **RES:** mock classifier outputs: `{cat, ic, t, dt, k, tm, name, m (message), ev?{day, t, ic, title, sub}}`.

### Domain concepts a real backend needs

- Trip, with a status lifecycle: draft, sent/live, ended.
- Passengers.
- Agent: photo, phones, hours, optional emergency phone.
- Agency: logo, brand copy, legal placeholders.
- Event: local time zone, provenance, update history (old value), verification flag, creator.
- Document: category, sharing scope, offline flag, lock, status badge, creator, download filename, linked event.
- Notification: deep-link target and read state, mirrored across channels.
- Chat: per trip, visible to all passengers, with an offline queue.
- Packing item: shared items with a per-user packed flag.
- User preferences: channels, notification types, nav app, big text, quiet hours.
- Legal version acceptance: version plus timestamp.
- Calendar subscription.
- Emergency contacts: per country, with a checked date.

## 3. Design tokens and reusable CSS

**Fonts:** Rubik 500–800 (display, `--f-d`), Assistant 400–700 (body, `--f-b`). `--f-m` is also Rubik and is used for numbers, LTR and tabular figures. Base `--fs` is 16px, or 19.5px for big text. Line height 1.45.

### Light palette

| Token | Value |
|---|---|
| --bg | #fbf8f2 |
| --surface | #fff |
| --surface-2 | #f4efe6 |
| --ink | #16241d |
| --muted | #5c5951 |
| --line | #e7e1d6 |
| --brand | #08402a (deep green) |
| --brand-ink | #fff |
| --brand-soft | #eef6f1 |
| --ok / --ok-fill / --ok-soft | #33704f / #5e9677 (sage V) / #e6f0ea |
| --warn / --warn-soft | #a85c28 / #fcf4ec |
| --bad / --bad-soft | #b91c3c / #fce8ec |
| --info / --info-soft | #1d5fa8 / #e4eef8 |
| --copper | #c37237 (attention, focus ring) |
| --item | #fbf3e3 (cream item rows) |
| --wait-line | #a9c7b5 |
| --shadow | 0 1px 2px rgb(8 64 42/.06), 0 6px 18px rgb(8 64 42/.07) |
| page / frame | #e9efe9 / #08402a |

### Dark palette

Applied via `prefers-color-scheme` (unless `data-theme=light`) and via `[data-theme=dark]`.

| Token | Value |
|---|---|
| bg | #0c1712 |
| surface | #13211a |
| surface-2 | #1a2b22 |
| ink | #e8ede9 |
| muted | #9aa79f |
| line | #26392f |
| brand | #74b590 |
| brand-ink | #021209 |
| brand-soft | #14291f |
| ok | #7fbf9a |
| warn | #e5a570 |
| bad | #f27a8c |
| info | #7fb2e8 |
| copper | #d4884a |
| item | #1f2a21 |
| wait-line | #3f5a4b |

### Radii

- Cards 20px; trow 18px; item rows and qa 16px.
- Ready, qd tiles and offnote 14px; buttons 13px (small 10px); chips and seg 12px.
- Pills 999px; bottom sheet 22px at the top.
- Tap targets: buttons min 46px (small 36px), icon buttons 42px circles, inputs 48px.

### Components

- **`.vk` check circle:** 28px circle in `--ok-fill`, with a white CSS-drawn check (an 11×6 border-left/bottom box rotated −45°). It pops in with `vkpop` (0.45s overshoot cubic-bezier(.34,1.4,.64,1)) unless reduced motion is on.
  - `.vk.wait`: transparent, 2.4px dashed `--wait-line`, no check.
  - `.vk.attn`: copper with a white "!".
  - Small variants: 20–22px.
- **`.doc` item row:** grid 42px / 1fr / auto, cream `--item` background, 16px radius, no shadow. Icon at 28px in brand color. Title bold, meta muted .8em. Tail is a pill, lock or vk. `.byme` badge (info-soft pill "הוספת בעצמך").
- **`.card`:** white, 20px radius, 14px padding, grid gap 8.
  - `.card.brand`: green background, white text. Translucent white tiles inside (`rgb(255 255 255/.14–.22)`).
  - `.card.click`: the card as a button.
  - `.k`: a small bold muted eyebrow label.
- **`.btn`** variants: `.pri` (brand), `.ghost` (surface-2), `.danger` (bad), `.s`, `.full`. Brand-card buttons: `.acb` (white on brand) and `.acg` (translucent).
- **`.pill`** variants: ok / warn / bad / info / br.
- **`.chip`:** pressed state uses inverted ink. `.chips.swipe` is a full-bleed horizontal scroller with no scrollbar.
- **`.seg`:** segmented control on surface-2. The pressed button is white with a shadow.
- **`.tog`:** switch, 48×28, knob animates via `inset-inline-start`. On is brand. `.lock` is 0.6 opacity. Uses role=switch with aria-checked.
- **`.qd-g` tiles:** cream, 3 columns, min-height 64, icon 26px brand color. `.qn` count badge (brand circle) at the top end corner.
- **Timeline `.tli`:** 52px time column (mono, LTR), a 14px rail with a 2px line and a 10px brand dot with a bg-colored ring, then the card.
- **Week view:** `.wc` columns 104px, scroll-snap. `.wcb` event chips in brand-soft, `.upd` in warn-soft. `.wcf` free day uses a dashed border.
- **`.ecard`:** emergency contact, number 1.6em mono, aligned right in LTR.
- **`.taxi`:** big LTR address card, name 2em weight 800.
- **`.nrow.un`:** 4px brand border on the start side.
- **`.msg.me`:** brand bubble with a 4px corner at `border-end-start`. `.msg.them`: white bubble with the 4px corner at `border-end-end`.
- **`.tsheet`:** bottom sheet with shadow `0 -12px 32px`.
- **`.toast`:** ink background, bg-colored text, 14px radius, bottom 96px.
- **`.offnote`:** 3-column (icon / text plus small / chevron) bordered row button. The chevron is the "back" icon flipped with scaleX(-1).
- **`.menuitem`:** icon / label / chevron, with a bottom border.
- **`.setrow`:** icon / label / control.
- **`.trow`:** list row with a 54×58 date block; the current trip gets a brand outline and a filled block.
- **`.paper`:** document preview mock.
- **`.otp`:** six 42×52 boxes, LTR.
- **`.fld`:** a label wrapping an input or select (48px, 12px radius). Focus is a 3px `--focus` outline.
- **Focus-visible:** a 3px copper outline with 2px offset on every interactive element.
- **`.mono`:** LTR, `unicode-bidi:isolate`, tabular numbers. Used for phones, booking codes, times and filenames inside RTL text.
- **`.legal-note`:** details/summary with no marker. The expanded part is a cream box.

**Icons:** an inline SVG sprite of `<symbol>`s at 24×24, using currentColor: plane, bed, doc, cal, map, home, menu, back (chevron, flipped for RTL), shield, sos, user, cloud (cloud with check), lock, check, alert, car, food, ticket, bus, walk, chat, phone, bell, sun, text, swap, down, send, heart, info, logo. They render through `ic(name)` as `<svg><use href="#name">`.

**Brand assets referenced (missing from the file):** `brand/logo/svg/wordmark.svg` (PALAMI wordmark, used in the "מופעל על ידי" footer) and `brand/mascot/mascot.png` (the beaver "הבונה" mascot, used on login and empty states). The CSS comment names a theme file, brand/tokens/theme-traveler.css: "warm paper, sage V, cream item rows, beaver moments".

**UX conventions to keep:**
- Hebrew copy is written in the feminine form, addressed to דנה (שלחי, כתבי, התקשרי); the real app needs gendered or neutral variants.
- Every item shows its provenance ("שובץ אוטומטית", "עודכן ע״י רונית").
- Updated items get an "עודכן" pill and a banner with old and new values.
- Unverified addresses get a warning and no navigation.
- Traveler-added items carry a "הוסף על ידי" badge, and the agent can see them.
- Critical change notifications cannot be disabled.
- Marketing requires opt-in.
- At least one notification channel stays on.
- Times are shown in the event's local time zone.
- The whole app works offline.
- Emergency and SOS are reachable from every header.
