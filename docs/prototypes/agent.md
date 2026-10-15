> Source: `docs/reference/prototype-agent.html` (artifact https://claude.ai/artifact/W7xw6yQtf1r94evC5LdTE5). Condensed blueprint. When in doubt, open the original prototype and the spec (`docs/reference/spec.txt`, ch. 23).

# PALAMI Agent App (סוכן): blueprint from the prototype

The prototype is a single-file vanilla JS app in Hebrew RTL. It has one global state `S`, and `render()` rebuilds `#root`. Clicks are delegated through `data-act`, `data-go`, `data-trip` and `data-tab`. Theme: agent tokens (`brand/tokens/tokens.css`, `data-product="agent"`). Green is used only for primary actions and navigation. There is no copper. Status signals follow BR-48..53.

## Shell
- **Desktop:** a 232px sticky sidebar on the right and a main column. The main column has a sticky top bar and content up to 1180px wide.
- **Sidebar:**
  - PALAMI wordmark, then the agency logo with "מסעות הדרים / רונית לוי · {role}". Clicking it opens the user menu.
  - Nav: דשבורד · נסיעות · לטיפול (warn count) · שיחות (red unread count) · לקוחות · הגדרות.
  - Credit box at the bottom: "בנק נסיעות · 38 קרדיטים · 12 פגים ב־31/12".
- **Top bar:** bell (unread dot), עזרה (help boxes per view, from the `HELP` map), דיווח על תקלה, טקסט גדול (font 16→18.5px), תצוגה פשוטה. `simple` and `big` persist in localStorage.
- **User menu:** name, email, role pill, הפרופיל שלי, יציאה מהחשבון. Closes on Esc or an outside click.
- **Toasts:** one at a time. Undo actions show "בטל" and stay 10s; others stay 3.5s.
- **Modals:** one at a time. Close on Esc or a backdrop click.
- **Mobile (≤860px):**
  - The sidebar becomes a bottom tab bar and top-bar buttons become icon-only.
  - Tiles stay 4 compact columns. Tables turn into trip cards with a colored side bar.
  - Chat shows the list first, then the thread full-screen with a back button.

## Views
- **login**
  - Fields: email, password, and "להישאר מחובר במחשב הזה" (unchecked; hint "לא לסמן במחשב שסוכנים אחרים משתמשים בו"). Plus שכחתי סיסמה.
  - After logout: "יצאת מהחשבון: המחשב פנוי…".
- **dash**
  - Greeting, a search box under it (client, destination, file ID, booking number), and "+ פתיחת תיק נסיעה".
  - Four clickable tiles:
    - Urgent (red top bar), or "הכול בשליטה" ✓ when nothing is urgent.
    - ביטוח חסר (honey).
    - מסמכים לטיפול.
    - מוכנות לפרסום.
  - Status filter chips: הכול / ממתינה להשלמה / טיוטה / מוכנה לפרסום / פורסמה / יש עדכונים לפרסום / בנסיעה.
  - Sortable table: מזהה תיק, יעד, לקוח, מי נוסע, תאריכים, יציאה, נוסעים, סטטוס, חוסרים.
    - Sorting cycles asc → desc → off. Off means urgency order: red rows first, then honey, then the rest.
  - Missing cell:
    - "✓ אין" when nothing is missing.
    - Otherwise a pill "N חוסרים ▾", red if any item is urgent. It expands an inline row listing each missing item with its own action.
- **simpleHome**
  - Three large cards: תיק נסיעה חדש · מה מחכה לי (count of insurance + exceptions + unread chats) · כניסה לתיק קיים.
- **trips**: search plus a sortable table of all trips, with the same row signals and missing rows.
- **trip** (file)
  - Header: back, name, ID pill, then dates · pax · status · trip type.
  - Header actions: "איך זה נראה ללקוח", "פרסום ושליחה ללקוח" (drafts), "פרסום N עדכונים" (when pending > 0).
  - Tabs:
    - **מסמכים והעלאה**
      - Drop zone and "בחירת קבצים".
      - Processing feed: each file gets a status, a summary and a "why" explanation.
      - "מסמכים בתיק" list:
        - Each row shows the content-based name, the original filename (mono), and a "הוסף על ידי X" pill when a traveler uploaded it.
        - Ownership button "שייך ל…": checkboxes for all or per passenger, plus "לפי קבוצה" chips. At least one passenger is required. Undo is available.
    - **סקירה וביטוח**: insurance block (upload policy / הנוסע סגר עצמאית / לא נדרש) and "מה יש בתיק" pills. Its note: "מה שהועלה זה מה שיש".
    - **לו״ז**: table with מתי (local time and time-zone label), אירוע, and מקור (auto / your decision / added by a traveler).
    - **נוסעים**:
      - Hierarchy breadcrumb, then one card per group.
      - Adult rows have children indented under them. Badges: לקוח ראשי / ראש קבוצה / ילד/ה.
      - A missing phone shows the warn pill "חסר נייד, נדרש לפרסום".
      - Clicking a name opens the edit modal. "+ הוספת נוסע" opens the add modal.
      - Organized group (23 pax): who opened the link, "שליחה שוב ל־6 שלא פתחו", "הודעה לכל הקבוצה", "ייבוא נוסעים מאקסל".
    - **מידע לנוסע**:
      - Tips textarea (option "לשמור גם כטיפים קבועים ל{dest}").
      - Shared packing list: add and remove, each item showing "הצעה אוטומטית" or "נוסף ע״י X". "ארזתי" is per traveler and never shown to the agent.
    - **שיחה**: link to the chat.
    - **התראות לנסיעה**: per-trip notification table (see Notifications).
- **exc** (לטיפול): one question at a time ("1 מתוך N").
  - `look`: missing mandatory field (for example the car return time).
    - Shows an OCR snippet with the uncertain part highlighted, plus an input.
    - Buttons: אישור (creates the reminder) and אחר כך (the item stays held from travelers).
  - `flight`: update conflict card (see Flows).
- **missing** (ביטוח חסר): items grouped by trip (name, ID, dates, pax, "יציאה בעוד N"), each with the 3 insurance actions.
- **custlist**: sortable table with לקוח (and a tag such as "מתעניינת בנסיעה הבאה"), נייד, נסיעה קרובה, נסיעות, ערוצים.
- **cust** (customer card)
  - Header: name, ID `HDR-C-00123` with copy, "ניתוק כל המכשירים" (undo), contacts.
  - Channel toggles: Push / WhatsApp / אימייל.
  - Marketing consent toggle, with an audit line ("סומן על ידי רונית · 3.9.2026 · בטופס ההזמנה").
  - Terms version: "גרסה 1.0 · אושרו בכניסה ב־2.10.2026".
  - "+ נסיעה חדשה לדנה" (prefilled), and a trips table with Dana's role in each trip.
- **chat**
  - Conversation list: initials, name, "dest · ID", preview, unread dot.
  - Thread:
    - Header has a לתיק button.
    - A file attached to a message can be added with "הוסיפי לתיק"; it is then auto-ingested and closes the related missing item.
    - Quick replies, composer.
- **settings**
  - **ההגדרות שלי** (everyone):
    - Profile photo (≤5MB, optional; initials when absent).
    - Availability: same as the agency, or own days and hours.
    - Personal emergency phone: shown only during an active trip.
    - My support tickets, with "דיווח על תקלה".
    - Logout.
  - **הגדרות הסוכנות** (supervisor only; an agent sees "מנוהלות על ידי {manager}"):
    - Employees: list, and "+ בקשה להוספת עובד" (sends a request to the PALAMI team in MVP).
    - Chat on/off.
    - Post-return message, with placeholders `[שם הסוכן]` and `[טלפון הסוכנות]` and a live preview.
    - Retention: 6/12/18/24 months.
    - Legal card (fields listed below, plus three documents with preview).
    - Traveler notification defaults.

## Flows
- **New trip modal** (`openNewTrip`)
  - Customer: first and last name, mobile (required; it is the customer key), email.
  - Trip: destination, trip type (יחיד / זוג (default) / משפחה / חברים / קבוצה מאורגנת), departure and return dates (required, return not before departure), pax count (≥1).
  - Shows "מזהה התיק: HDR-2610-00NN".
  - On create: a draft trip with insurance status `later`, the main customer as the first passenger in a default group "משפחת {last}". Opens the docs tab.
- **Upload**
  - Accepted: pdf, jpg, png, heic, webp. Anything else is blocked with a hint to save as PDF.
  - Processing is async; the agent can keep working.
  - Result statuses: `p` בעיבוד · `ok` שובץ · `w` לטיפול · `b`/`upd` ממתין לאישור · `m` "תיק אחר?" · `x` נחסם.
  - `m` (wrong file) offers "העבר לתיק ההוא" or "אשר ידנית: שייך לתיק הזה".
  - Each file is renamed by its content; the original name is kept.
  - An insurance document sets insurance to ok and clears the missing item.
- **Flight update** (`flightCard`, also opened as a popup alertdialog)
  - Compare grid: שדה / עכשיו בתיק / במסמך החדש. Only changed values are highlighted.
  - Checkbox: "לעדכן את 4 הנוסעים אחרי האישור". Note that check-in and airport reminders will be recalculated.
  - Buttons:
    - אשרי: makes the trip "יש עדכונים לפרסום".
    - דחי: keeps the old value.
    - אחר כך: re-queues the item in exc.
- **Publish modal**
  - Summary: recipients (passengers with contact), documents, credits ("1 קרדיט · יישארו 37"; updates cost 0).
  - Banner "מה הנוסעים יראו".
  - Non-blocking warnings: passengers with no contact, no insurance.
  - Channel: by each traveler's preference, or copy links only.
  - Statement line without a checkbox: "בפרסום את מאשרת שבדקת…" (BR-71).
  - On confirm: credit −1 on first publish, status pub, pending updates reset to 0.
- **Passengers**
  - Add modal: name, adult or "ילד/ה בלי טלפון".
    - Adult: phone or email, optional "head of group".
    - Child: "מקבל/ת דרך" (an adult from the trip) is required.
    - Group: pick an existing one, or "+ קבוצה חדשה" with a name.
  - Rules:
    - Duplicate name shows a warning.
    - Only one head per group; the first adult in a new group becomes head.
    - Renaming an adult updates children who receive through them.
    - Changing a phone after publish sends a new link and stops the old number from logging in.
  - Missing items generated: "הוזנו X מתוך N נוסעים", and "ל{name} אין נייד או אימייל".
  - Sharing mode by trip type: "separate" (each sees shared + own) for friends and organized groups; "all see all" for every other type.
- **Notifications**
  - Agency defaults `NR` (setting / options / default):

    | Setting | Options | Default |
    |---|---|---|
    | שומרים על קשר | 14/7/30 days after return (marketing; opt-in only) | 14 |
    | סיכום לפני יציאה | 3/2/5 days before | 3 |
    | צ'ק-אין, when the airline has no rule | 24/48h before | 24 |
    | תזכורת צ'ק-אין | 6/3/12h before | 6 |
    | יציאה לשדה | 3/2/4h before | 3 |
    | תדריך בוקר | 08:00/07:00/09:00 | 08:00 |
    | תזכורת לאירוע | 2/1/4h before | 2 |
    | משהו השתנה | (locked, critical) | always on |

  - Per-trip table:
    - Each row is "כמו בסוכנות" or "שונה לנסיעה הזו", with a reset per row and a reset for the whole table (both undoable).
    - Overrides are stored as diffs only.
    - The "when" select is disabled while a rule is off.
- **Bell**
  - Unread count; rings when a new item arrives. Panel has "סמני הכול כנקרא".
  - Each item shows trip name · ID · time and deep-links to a view, a trip tab, or the flight popup.
- **Support ticket** ("דיווח על תקלה")
  - Text (required), optional screenshot. Screen, browser, user and trip ID are attached automatically.
  - Ticket numbers start at #1043. Statuses: חדשה / בטיפול / נסגרה.
- **Legal fields** (supervisor)
  - שם משפטי, ח.פ., כתובת, אימייל לפניות פרטיות.
  - רכז נגישות (only required for agencies with 25 or more employees).
  - ממונה הגנת פרטיות (optional; hidden if empty).
  - הסדרי נגישות במשרד.
  - Privacy policy: the PALAMI template, or the agency's own link.
  - Agreement status: "✓ נחתם · 3.9.2026".

## Status computation
```
ST = { draft:'טיוטה', incomplete:'ממתינה להשלמה', ready:'מוכנה לפרסום', pub:'פורסמה',
       pend:'יש עדכונים לפרסום', act:'בנסיעה', done:'הסתיימה', cancel:'בוטלה' }
stored: draft | pub | act | done | cancel
stOf(t): draft && missing>0 → incomplete; draft && all ready → ready; pub && pend>0 → pend; else stored
missingOf(trip) = pending flight update (urgent) + insurance items + unclear fields
                  + pax count shortfall + adults without phone/email
signal: red if urgent item, honey if any missing, else none
```

## Data model (implied)
- **Trip**
  - Fields: `{type, id 'HDR-YYMM-NNNN', name 'dest · customer', dates, pax, paxN, st, ins: ok|miss|self|na|later, ready:[filled,total], pend, cust}`.
  - Dates are shown as `DD.MM.YYYY – DD.MM.YYYY` (LTR).
- **Passenger:** `{name, role main|companion, contact, docsSummary, lastLogin, group, adult|child, viaAdult, isHead}`.
- **Trip document:** `{displayName, owners: 'all' | [names], addedBy, originalFilename}`.
- **Inbox item:** `{trip, name, orig, st, res, why, by, suggestedTrip}`.
- **Missing insurance:** `{trip, type ביטול|נסיעות, what, note, st ''|req}`.
- **Exception:** `{type field_unclear|update_conflict, trip, doc, field, ocrSnippet, current, proposed}`.
- **Notification:** `{t, trip, at, unread, icon, action/view/tab}`.
- **Customer:** `{id HDR-C-NNNNN, name, phone (unique key), email, channels, marketingConsent + audit, termsVersion, trips[{role}]}`.
- **Conversation:** one per trip. Messages are `{me, text, at, file?, added?}`.
- **Ticket:** `{n, text, trip, status, at, answer}`.
- **Agent:** `{name, email, role sup|agent, photo, hours (own or agency), emergencyPhone + on}`.
- **Agency:** `{name, logo, phone, email, hours, emergency24, retentionMonths, chatOn, postReturnMsg, notifDefaults, legal fields, credits}`.

## Gaps in the prototype (decide in real build)
- Hard-coded schedule.
- The "ready" tile opens one fixed trip instead of filtering.
- Only Dana's customer card is live.
- Search covers only the file ID and the name; the spec also requires customer and booking number.
- The notification engine is not implemented; only its settings are.
