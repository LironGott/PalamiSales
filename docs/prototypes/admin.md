> Source: docs/reference/prototype-admin.html (artifact https://claude.ai/artifact/DNPd741xZ4J3GCzZJHtUTi). The admin system is out of scope for now.

## Technical summary: PALAMI Admin prototype (`PALAMI · ניהול`)

**File:** /root/.claude/projects/-home-user-PalamiSales/3936a2d6-96a6-531f-b24a-0a41a5fbcfc8/tool-results/artifact-642a3985-1791389144-8f15.html (337 lines, read in full)

### Overview
- It is a single-file vanilla JS prototype. The UI is Hebrew RTL (`dir="rtl" lang="he"`).
- Rendering: one global state `S`, a `render()` function that rebuilds the whole `#root` from string templates, and event handlers on `document` that dispatch on attributes (`data-act`, `data-go`, `data-ag`, `data-tk`, `data-tkf`, `data-step`, `data-agtab`, `data-w`, etc.).
- Theme ("theme-admin.css" tokens): light and dark modes, a brand-green top stripe (`#08402a`) with the mascot head, the wordmark and a gold **ADMIN** badge. A CSS comment says status colours follow **BR-48..53**.
- Responsive: below 860px the side nav becomes a 3-column grid.
- Fonts: Rubik, Assistant and IBM Plex Mono.
- The logged-in staff member is always **נועה · הקמה ותמיכה** (noa@palami.io). Other staff: דן, עידו.

### Global chrome
- **Top stripe**
  - Bell button with an unread count; its popover lists notifications, with "סמני הכול כנקרא".
  - User menu: "הפרופיל שלי" (toast says the real app has details, password and 2FA) and "יציאה מהחשבון".
- **Login view** (`כניסה למערכת הניהול`)
  - Fields: email, password, and a 6-digit TOTP "קוד אימות (מאפליקציית האימות)".
  - Validation: email and password are required, and the code must match `^\d{6}$`.
  - After logout the banner reads "יצאת מהחשבון – המחשב פנוי לאיש צוות אחר". A demo button logs in as נועה.
- **Side nav:** סוכנויות · תמיכה · קרדיטים וחיוב · כניסה לחשבון סוכנות · תקינות המערכת · היסטוריית פעולות.
  - תמיכה shows a red badge with the open-ticket count when a late new ticket exists.
  - כניסה לחשבון סוכנות shows a warning badge when an access request is pending.
  - תקינות המערכת always shows a red "1".
- **Notifications** (`NOTIFS`: t, s, go, un). Each one deep-links to a view; a tickets notification also sets the filter to `late`. Examples:
  - new ticket #1042 unanswered for 5h
  - מסעות הדרים approved account access until 14:30
  - שמש נופשים payment 19 days late
  - גלובוס טורס agreement sent for signature
- **Feedback:** toasts (3.8s) and modals (close on Esc or a backdrop click).

### Views

**1. סוכנויות (agency list)**
- Four KPI tiles:
  - תשלום באיחור של יותר מ־14 יום (red when above 0)
  - הקמה לא הושלמה (amber)
  - סוכנויות פעילות (every agency not in setup)
  - נסיעות שפורסמו החודש (static 1,284)
- Table columns: סוכנות, קוד, עובדים, נסיעות פעילות, קרדיטים, הסכם, סטטוס, action.
- Sorting by urgency: late (red side bar) first, then setup or low (amber side bar), then the rest.
- Row click: an agency in setup reopens the wizard at its saved step; any other opens agency detail.
- Button "+ סוכנות חדשה" starts a fresh wizard.

**2. Agency detail**
- Header: logo placeholder, name, code, "חבילת X" and a status pill.
- Actions:
  - "בקשת כניסה לחשבון"
  - "השהיה" (toast only): agents cannot log in, but travelers keep seeing their trips
- Tabs (chips):
  - **עובדים**
    - Table: name, email, phone, role (pill when the role is מנהל), status.
    - Statuses: פעיל / מושבת / "הוזמן, עוד לא נכנס".
    - Row actions: השבתה ↔ החזרה (both write to the audit log), and שליחה מחדש for invites.
    - Note: "כל עובד מקבל מייל להגדרת סיסמה. מנהל רואה את כל נסיעות הסוכנות".
    - "+ עובד" modal: name, email, phone, role סוכן/מנהל. It runs the same validation, then adds the employee as invited and shows "ההזמנה נשלחה".
    - "העלאת קובץ CSV" modal: the demo adds 2 employees and sends invites.
  - **פרטים ולוגו:** איש קשר, אימייל, טלפון, שעות פעילות, טלפון חירום 24/7, קוד לתיקים (example `HDR-2610-0001`). Wide logo for traveler screens, square logo for the agent system; agency colour is planned for v2.
  - **קרדיטים ושימוש:** balance, package, "12 פגים ב־31/12", monthly usage (נסיעות שפורסמו, נוסעים, קבוצות (מעל 20)), "טעינת קרדיטים", ייצוא לאקסל.
  - **הסכם**
    - A single document, "הסכם השירות ונספח עיבוד המידע", with one signature. Version 1.0 · 9.2026.
    - States: none → "סימון: נשלח לחתימה" → sent ("תזכורת לחתימה") → signed.
    - Signing happens by uploading the scan (PDF or image, ≤10MB), which marks the agreement signed with today's date.
    - The file is stored encrypted, and every view is audit-logged.
    - **"סוכנות מופעלת רק אחרי שההסכם החתום נשמר כאן."**
  - **הגדרות** (read-only): צ'אט עם לקוחות, מספרי חירום לכל יעד (entered by the agency), מדיניות התראות (PALAMI defaults). "הוספת מסמכים על ידי נוסעים תמיד פעילה, ואין לה מתג."

**3. Onboarding wizard (6 steps)**
- Steps: פרטים · קוד לתיקים · לוגו · עובדים · ברירות מחדל · חבילה והפעלה.
- Progress: step pills, with completed steps shown as ✓. You can jump back to any step up to the current one. The header says "נשמר אוטומטית".
- The המשך button validates each step:
  1. **פרטים**
     - Required: name, contact, email, phone, emergency phone 24/7 ("מוצג לנוסעים במסך החירום").
     - Hours is optional; default "א׳–ה׳ 9:00–18:00".
     - "מילוי לדוגמה" fills demo data.
  2. **קוד לתיקים**
     - Exactly 3 English letters (`^[A-Z]{3}$`), uppercased automatically.
     - Must be unique across agencies; the agency being resumed is excluded from the check.
     - "נכנס לכל מזהה תיק ולא משתנה אחר כך."
     - Live preview: `CODE-2610-0001`.
  3. **לוגו**
     - Wide logo: SVG or transparent PNG, ≤2MB.
     - Square logo for the agent system; if none is given, it is auto-cropped from the wide one.
     - Phone mockup of the traveler view, with a "מופעל על ידי PALAMI" footer.
     - MVP branding is logo-only; colour comes in v2.
  4. **עובדים**
     - Toggle between העלאת קובץ CSV and הוספה ידנית.
     - Invites are sent only at activation.
     - Validated table with inline fixes and row delete (details under Employees CSV below).
  5. **ברירות מחדל**
     - צ'אט עם לקוחות toggle, default on. When off, clients see only phone, email and WhatsApp.
     - התראות לנוסעים uses PALAMI defaults: סיכום 3 ימים לפני, צ'ק-אין, תדריך בוקר 08:00.
     - נוסעים מוסיפים מסמכים: always on, no toggle.
     - "הסוכנות יכולה לשנות את כל אלה בעצמה אחר כך."
  6. **חבילה והפעלה**
     - Package: בסיס / Pro / קבוצות. Opening credits default 20.
     - Summary banner.
     - **Signed agreement upload is required.** Without it activation is blocked ("ההקמה נשמרה, ואפשר לחזור אליה").
     - Button "הפעלת הסוכנות ושליחת הזמנות" creates or updates the agency: status active, agreement signed, and every employee set to "הוזמן, עוד לא נכנס".
     - Activation writes to the audit log and navigates to agency detail.

**Employees CSV (parsing and validation)**
- Columns in order: שם מלא, אימייל, נייד, תפקיד (מנהל או סוכן).
- Parsing:
  - Delimiter can be `,`, `;` or tab; quotes are trimmed.
  - A row needs at least 3 columns.
  - Rows whose first cell matches שם or name are skipped as headers.
  - Role defaults to סוכן.
- Validation:
  - Email must match `^[^\s@]+@[^\s@]+\.[^\s@]+$`.
  - Mobile, after stripping spaces and dashes, must match `^0\d{8,9}$`.
  - Emails must be unique (case-insensitive).
- Errors, in priority order: אימייל לא תקין › נייד לא תקין › אימייל כפול.
- Row display: errors get an amber row and are fixed inline. Counters show תקינים / לתיקון, plus "צריך לפחות מנהל אחד".
- Header-row copy button: "העתקת שורת הכותרות".
- The wizard demo includes one bad email (`orna@globus`).

**4. תמיכה (support tickets)**
- Header note: "התראה לצוות בפעמון ובאימייל על כל קריאה חדשה".
- Filter tiles (click toggles the filter):
  - לא נענו 4 שעות (late and new)
  - פתוחות
  - בטיפול
  - נסגרו השבוע · ממוצע 3.5 שעות (11 plus the closed tickets)
- Default list shows all open tickets.
- Split layout: list on one side (#, agency · agent, time, subject, 📎 for a screenshot, status) and detail on the other.
- Detail pane:
  - Body text and the screenshot placeholder.
  - "נשלח לבד" auto-captured environment (browser · OS · screen) and the linked trip ID.
  - אחראי select (נועה/דן/עידו) and status select.
  - Message thread.
  - Reply box: "תשובה לסוכן – מגיעה אליו בפעמון ובאימייל".
  - Buttons: שליחה, בקשת כניסה לחשבון, סגירת הקריאה.
- Statuses (`TKST`): new=חדשה (red), work=בטיפול (amber), agent=ממתינה לסוכן, closed=נסגרה (green).
- Rules:
  - Replying to a new ticket moves it to work, clears late, and auto-assigns נועה if it has no owner.
  - Any status change away from new clears late.
  - Status change and close notify the agent.

**5. כניסה לחשבון סוכנות (account access)**
- Policy text: used when a ticket cannot be understood without seeing the agent's screen.
  - The agency manager approves.
  - Access is read-only, time-limited (up to 24 hours) and audit-logged.
  - **Travelers' personal documents (passport, policy) never open.**
- Table: agency, who, ticket, state.
  - active: "פעילה עד HH:MM" plus a countdown timer; buttons סיום עכשיו and כניסה.
  - pending: "ממתינה לאישור המנהל"; button תזכורת למנהל.
  - done: הסתיימה.
- Requesting access creates at most one non-done request per agency and writes to the audit log. Ending access writes to the audit log.

**6. תקינות המערכת (system health)**
- Purpose: "לגלות תקלה לפני שסוכן מתקשר".
- Cards with ok/warn/bad dots; bad and warn cards link to the related ticket:
  - קליטת מסמכים (bad): a PDF stuck "בעיבוד" for 61 minutes
  - WhatsApp (warn): a number without a country prefix, ticket #1041
  - קבצים שנחסמו כחשודים
  - זמן עיבוד ממוצע: 14 seconds, target under 60
  - אימיילים: 99.8% delivered
  - Push

**7. היסטוריית פעולות (audit log)**
- Every staff action, recorded as מתי / מי / מה.
- "לא ניתן למחוק או לערוך. נדרש לאבטחה ולחוק הגנת הפרטיות."
- Filter chips: הכול, לפי איש צוות, לפי סוכנות. Only הכול works in the prototype.
- Logged events:
  - access entry, request and end
  - credit loads
  - setup start and stop
  - employee disable and enable
  - agreement upload and marking it sent
  - agency activation

**8. קרדיטים וחיוב (credits and billing)**
- Table covers agencies not in setup: package, balance (with a נמוך pill), used this month, payment (שולם, or באיחור N ימים), and טעינה.
- Load-credits modal:
  - Amount, default 20.
  - **Expiry date is required.** Presets: סוף השנה, שנה מהיום, חצי שנה.
  - Saving adds the amount to the balance. A low agency returns to active when its balance reaches 10 or more. Writes to the audit log with the expiry date.
- Note: "מודל התשלום עוד לא נקבע. המערכת אוספת את הנתונים לכל מודל". Excel export is a stub.

### Data model (in-memory)
- **Agency:** `{id, name, code(3 letters), st: active|setup|low|late, step (setup only), emp, trips, credits, days (late), contact, email, phone, hours, emerg, pkg: בסיס|Pro|קבוצות, agr:{st: none|sent|signed, date, file}}`.
  - Seed data: שמש נופשים SMS (late 19d), גלובוס טורס GLB (setup, step 3, agreement sent), אופק תיירות OFK (low, 3 credits), מסעות הדרים HDR (active, 38 credits).
- **Employee** (per agency): `[name, email, phone, role מנהל/ת|סוכן/ת, status פעיל|מושבת|הוזמן, עוד לא נכנס]`.
- **Ticket:** `{n, ag, who, t (subject), body, st, at, late, shot, trip, env, owner, msgs:[{me, t, at}]}`.
- **Access request:** `{ag, who, tk, st: pending|active|done, until, left}`.
- **Audit entry:** `[when, who, what]`, prepended on each action.
- **Notification:** `{t, s, go, un}`.
- **Wizard draft:** `{step, name, code, contact, email, phone, hours, emerg, logo, sq, mode, rows[], chat, pkg, credits, agr, from}`.
- **Trip/file ID format:** `CODE-YYMM-NNNN` (e.g. `HDR-2610-0041`).

### Key business rules
1. An agency cannot be activated without an uploaded signed agreement (service agreement and DPA, one signature). Setup can be saved and resumed.
2. The agency code is 3 English letters, unique, and immutable because it is embedded in every file ID.
3. An agency needs at least one manager. All employee rows must be valid before continuing. Invites go out only at activation.
4. A manager sees all of the agency's trips. Disabled employees cannot log in.
5. Pausing an agency blocks agents, but travelers still see their trips.
6. Account access requires manager approval, is read-only, lasts at most 24h, is audit-logged, and never exposes traveler personal documents.
7. The audit log is immutable (privacy law).
8. Ticket SLA: a new ticket unanswered for 4 hours is flagged late.
9. A payment more than 14 days late is flagged red. Credits below 10 count as low.
10. Credit loads require an expiry date.
11. Cancelling a trip before publish deducts no credit; publishing a trip consumes credits.
12. Traveler document upload is always on. Chat with clients is on by default and the agency can change it.
13. MVP branding is logo-only, with agency colour in v2.
14. The billing model is still undecided.
