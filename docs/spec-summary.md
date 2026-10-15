# PALAMI: spec summary (from "אפיון לוגי", draft 0.9, Oct 2026)

> Full source: `docs/reference/spec.html` (artifact https://claude.ai/artifact/QEa9EhST9oHB7SiDfPTHtE), plain text in `docs/reference/spec.txt`.
> IDs: FR-xxx is a customer requirement · F-x.x a feature (ch. 6) · BP-xx a business process · BR-xx a business rule (enforced server-side) · SCR-Axx/Txx/Mxx a screen (agent/traveler/admin).
> Open question for partner (איילי): the agency payment model (ch. 25). Everything else is approved.

## 1. Vision
- **What it is:** a digital trip file for travel agencies, sold B2B to agencies.
- **How it works:** the agency uploads the documents once. The traveler gets one link with everything, at the right time, even offline.
- **Slogan:** "כל פרטי הנסיעה בכף ידך". Domain: palami.io.
- **Pilot KPIs:**
  - ≥70% of travelers open the link.
  - <3 minutes from the first drop to publish.
  - ≥80% of documents filed with no agent touch.
  - −30% repeat questions to the agent.
  - ≥80% of agencies publish another trip.
- **Not:** a booking system, a GDS/CRM replacement, or check-in on the traveler's behalf. No passports or medical data in v1. No real-time flight status without an integration.
- **UX target:**
  - A 70-year-old traveler at the airport finds the boarding pass in 2 taps.
  - An agent with 40 open files sets up a file in minutes.

## 2. Three systems (shared DB and brand, different look)

| | Agent `app.palami.io` | Traveler `trip.palami.io` (PWA via link) | Admin `admin.palami.io` |
|---|---|---|---|
| Users | agents + agency managers (incl. older agents) | main customer + trip companions | PALAMI staff |
| Feel | professional, quiet, dense; tables | fun, warm, inviting; big cards, V rows, beaver | functional |
| Density | 15px text, 44px rows, big-text mode | 17px text, 48px taps | 40px rows |
| Colour | grey-white; green only for primary action/nav; no copper | warm paper, green, copper accents | agent look + green top stripe + beaver + ADMIN badge |
| Branding | PALAMI on top, agency name and logo below | agency in the centre, "מופעל על ידי PALAMI" at the bottom | PALAMI only |

- Phone and desktop in all three from the MVP. Dedicated tablet design comes in v1.1.
- Breakpoints: ≤639 / 640–1023 / ≥1024. On phones the agent tables become cards and the sidebar becomes a bottom bar.
- Each system has its own separate login.

**Status colours** (same meaning everywhere; always shown with an icon and a word):
- ✕ urgent: crimson.
- ! attention: honey in the agent system, soft copper for the traveler.
- ✓ done: sage.
- i updated: blue.
- ◌ waiting: grey dashed.

Rules for colouring:
- Never colour a whole row. Use a thin side bar, a tag and a counter.
- Dashboard order: red first, then honey, then by departure date.
- When nothing is open, the dashboard shows "הכול בשליטה" ✓ instead of zero counters.

**Agent dashboard row colour (the most severe item in the file wins):**
- **Red (BR-48..51):**
  - No travel insurance and ≤2 days to departure.
  - No cancellation insurance and 6 days have passed since booking.
  - An update awaiting approval with the event ≤72h away.
  - A client message unanswered for 2h within working hours.
  - A document that cancels a flight or trip.
  - A file blocked as malicious.
- **Honey (BR-52):**
  - An open "לטיפול" item.
  - No travel insurance with 3–30 days to departure.
  - No cancellation insurance on days 3–5 after booking.
  - An update awaiting approval with the event >72h away.
  - Check-in not marked 6h before the flight.
  - Ready to publish with ≤14 days to departure.
- **Green, blue, grey (BR-53):**
  - Green: published or active, with nothing open.
  - Blue: something auto-filed or published in the last 24h.
  - Grey: draft, processing, or waiting on the traveler.

## 3. Core model: "the agent only drags" (ch. 4–5)
- The agent opens a file and drags PDFs and images into it, any number at any time. There is no global drop zone; every document goes into a specific file (BR-26).
- Pipeline: validate → OCR → classify → extract fields with confidence → match the file (names and dates ±3 days) → file it (create or update events, link travelers, attach the file).
- Outcomes:
  - **Auto-filed:** most documents.
  - **"לטיפול":** one uncertain field (confidence <0.9), or the document looks like it belongs to another file (move it there, or confirm manually).
  - **Update awaiting approval:** a new document changes an existing event. The agent sees before and after, then approves, rejects or chooses "later" (BR-05). Values that only add information are filed automatically.
- Mandatory fields per type (BR-73). If one is not read with certainty, the item stops and does not reach travelers.
  - Agent upload: the item goes to לטיפול with the source snippet.
  - Traveler upload: the traveler is asked to fill in one field. The agent gets no notification.

| Type | Mandatory fields |
|---|---|
| Flight (per segment) | airline, flight number, departure date+time+TZ, arrival date+time+TZ, origin, destination, PNR, passenger names |
| Hotel | name, address, check-in, check-out, confirmation number, booker or guests |
| Rental car | company, booking number, pickup place, pickup date+time, return place, return date+time, main driver |
| Transfer | meeting point, time, destination |
| Train | operator, origin, destination, date+time |
| Insurance | type (cancellation / travel), company, policy number, validity, insured; emergency 24/7 number is material for travel insurance |
| Restaurant / show / attraction / tour / other | name, date, start time, location |

- Unknown document types: extract the key facts. If there is a date, create an "אחר" event; otherwise store the document with a summary.
- Document types are configurable data (`DOC_TYPE`), not code.
- **14 upload checks, in order:**
  1. Permission.
  2. Type: PDF, JPG, PNG, HEIC or WEBP.
  3. Size: ≤20MB per file, ≤20 files per upload, ≤30 pages.
  4. Not corrupt.
  5. Virus scan.
  6. Password-protected PDF: ask once.
  7. Duplicate hash: skip.
  8. Readability (blur, darkness).
  9. Recognised as one of the 11 categories.
  10. Belongs to the trip.
  11. Mandatory fields read with ≥0.9 confidence.
  12. Logic: landing after takeoff, checkout after check-in, policy covers the trip.
  13. Changes an existing event.
  14. Sensitive data: passports are not stored; card numbers are masked to the last 4 digits.
  - Each failure is shown in plain language with what to do. One failing file does not stop the others.
- **Content-based file names:** examples "טיסה LY395 · תל אביב–ברצלונה · 12.11.2026", "מלון Casa Bonay · 12–19.11.2026".
  - Personal documents end with the traveler's name. Max 80 chars. Duplicates get "(2)".
  - The original name is kept in history.
- **Traveler uploads:** always on, with no agency toggle.
  - The traveler chooses who sees it: all / only me / chosen travelers. Default comes from the names in the document, and the field is shown only when more than one person is on the trip (BR-74).
  - Tickets also create a schedule event; insurance stays as a document only.
  - Tagged "הוסף על ידי X". The agent gets no notification (BR-44).
  - Changing an agent-created event always waits for agent approval.
- **Traveler document display (BR-79):**
  - Title: type · name, ≤35 chars, no date or name.
  - Second line: when · for whom · extra (for example "ה׳ 12 בנוב׳ · 06:10 · רק לך").
  - Sorted by date, with whole-trip documents first.
  - Filters, shown only when non-empty and in this order: הכול, טיסות, לינה, אטרקציות, רכב, ביטוח, אחר.

## 4. Statuses (ch. 11)
- **Trip:**
  - טיוטה → ממתינה להשלמה (something missing) ⇄ טיוטה → מוכנה לפרסום → פורסמה (first publish uses 1 credit).
  - Publishing is also allowed from ממתינה להשלמה.
  - פורסמה → יש עדכונים לפרסום (new documents while auto-update is off) → פורסמה (no credit).
  - פורסמה → בנסיעה (start date) → הסתיימה (end date) → נמחקה (end of retention).
  - בוטלה from a draft (no charge) or after publish. Travelers see "הנסיעה בוטלה" for 7 days.
  - Status is automatic. The agent manually triggers only publish and cancel.
- **Upload:** התקבל → בעיבוד → (נחסם | שובץ אוטומטית | לטיפול | עדכון ממתין לאישור) → גלוי לנוסע → הוחלף. A לטיפול item can also end as נדחה.
- **Insurance:** ייבדק → (30 days before departure with no policy) אין ביטוח → יש פוליסה | הנוסע סגר עצמאית | לא נדרש. From "self", uploading a policy moves it to יש פוליסה.
- **Alert:** scheduled → quiet-hours hold → open → snoozed / done / not relevant / cancelled on recalculation.
- **Missing items (BR-58):** missing insurance, an update awaiting approval, a field to check, a traveler without phone or email, fewer travelers than declared. They are shown in the "חוסרים" column.

## 5. Data model (ch. 9, logical)
Every entity except AGENCY carries an agency id (BR-01).

**Agency and staff**
- **AGENCY:** name, status, package, auto-publish rule, retention 6–24 months (default 12), hours, emergency 24/7 phone, post-return message, legal fields, privacy policy (template or link).
- **BRANDING:** logo (wide + square). Agency colour comes in v2.
- **USER:** name, email, photo, hours, emergency phone (all optional), role (agency manager / agent), MFA, view scope (own trips / whole agency), display prefs (simple view, text size).

**Customers and travelers**
- **CUSTOMER:** id `HDR-C-00123`, name, mobile (unique within the agency; it is the username), email, password hash, language, consents.
- **TRAVELER** (a customer on a trip): role (main / companion), group, head of group, escort, adult or child, `via` adult.
- **TRAVEL_UNIT:** a group inside the trip (family, couple, room).

**Trips, events and documents**
- **TRIP:** id `HDR-2609-0031` (agency code-YYMM-running number; immutable, never reused; BR-35), main customer, destinations, dates (mandatory), type (יחיד / זוג / משפחה / חברים / קבוצה מאורגנת), sharing mode, status, cancellation-insurance and travel-insurance status, responsible agent, first publish date, pending changes, internal note.
- **UPLOAD:** file, uploader, original name, display name, check results, processing status, suggested trip.
- **EVENT:** category, title, start and end with IANA time zone, supplier, booking number, category fields, travelers, source, filed auto or manual, last updated by.
- **LOCATION:** address, coordinates, verification status.
- **DOCUMENT / DOC_VERSION:** type, display name, belongs to (all or a subset), shared with (for traveler uploads), uploaded by, sensitivity. Each version holds the encrypted file, hash, scan status and processing status.
- **EXTRACTION / EXTRACTED_FIELD:** for each field, the value, confidence, source location, whether it is material, and how it was accepted (auto / approved / corrected).
- **CONFLICT:** before and after values, source document, status, approver.

**Notifications, access and offline**
- **NOTIFICATION_POLICY:** at agency level, with trip-level overrides that store only the differences.
- **NOTIFICATION_PREF:** customer's channels, quiet hours, types turned off.
- **ALERT:** the bell notifications, with read flag and deep link.
- **CHECKIN_RULE**.
- **SHARE_LINK / ACCESS_SESSION:** token stored as a hash, ≥128 bits.
- **OFFLINE_SNAPSHOT**.

**Messaging, emergency and billing**
- **CONVERSATION / MESSAGE:** one per trip.
- **COUNTRY / EMERGENCY_NUMBER:** maintained by the agency.
- **LEGAL_DOC_VERSION, CONSENT_RECORD:** immutable, kept 7 years.
- **USAGE_RECORD, CREDIT_TXN:** a ledger kept 7 years.
- **AUDIT_EVENT:** append-only, kept 24 months.

## 6. Fields (ch. 10)
Three levels: mandatory · mandatory-to-publish · optional. Anything the documents can provide is never typed by hand.

- **Customer:**
  - Mandatory: first and last name (Hebrew), mobile (international format), email.
  - Password: ≥6 chars with no complexity rules; common passwords are blocked; 5 failures lock the account for 15 minutes.
  - Channels default to email + Push; WhatsApp after consent.
  - Marketing consent is off by default and logged with who, when and how.
- **Trip:**
  - Mandatory: main customer, destination, type (default couple), traveler count (incl. children), sharing mode, start and end dates.
  - Optional: name (auto "ברצלונה · משפחת כהן"), internal note (never shown to travelers).
- **Traveler:**
  - Mandatory: name, role, group, adult or child.
  - Mandatory to publish: phone or email, for adults.
  - A child needs a `via` adult from the same group.
- **Agency setup:**
  - Mandatory: name, 3-letter code, logo (wide + square), phone, email, hours, emergency 24/7 phone.
  - Optional: chat on/off, post-return message, retention, "שומרים על קשר" text and days (default 14).
  - Mandatory to publish: legal details, emergency numbers per destination.
- **Agent:**
  - Mandatory: name, email, mobile (for 2FA), role, view scope.
  - Optional: photo ≤5MB, availability hours, personal emergency phone.

## 7. Travelers, groups, multiple trips (ch. 13–14)
- **Traveler login:** the link leads to the trip but does not open it.
  - Sign in with mobile (or email) and password.
  - First time, or a new device: OTP by WhatsApp or SMS, then choose a password.
  - The device stays logged in for 90 days, or until the end of the last trip.
  - Forgot password: OTP. Lost phone: the agent clicks "ניתוק כל המכשירים".
  - Sensitive documents open after login with no extra code (they are logged).
- **On publish:** each traveler is matched to a user by phone or email. An existing user gets the trip added; otherwise a new user is created.
- **Hierarchy:** trip › main customer (exactly 1) › groups › travelers › children via an adult. The head of a group sees the whole group's documents.
- **Sharing:**
  - "כולם רואים הכול" is the default for solo, couple and family.
  - "כל נוסע רואה את המשותף ואת שלו" is the default for friends and organized groups. Organized groups can have an escort.
- **Document ownership:** all, or any subset (≥1 traveler). The AI proposes it from the names. Removing a traveler revokes access immediately, including the offline copy.
- **Multiple trips:** one login shows all of the customer's trips at that agency. Each trip is isolated. Order: active trip, then upcoming by date, then ended. Only published or ended trips are visible to travelers (BR-69).
- **Organized group of 20+:**
  - Import travelers from Excel, or create them from tickets.
  - One publish sends every traveler a personal link.
  - Track who opened the link; resend only to those who didn't.

## 8. Insurance (ch. 15)
- Insurance is the only completeness check, because nothing else is known about the booking.

| | Cancellation insurance | Travel insurance |
|---|---|---|
| When bought | within ~1 week of booking | by departure |
| Agent alerts | day 3 and day 6 after booking (booking date from the flight document, or the file open date) | 7 days and 2 days before departure |

- Agent actions: upload a policy · "הנוסע סגר עצמאית" (the traveler gets an optional request to upload) · "לא נדרש".
- A combined policy closes both checks.
- The traveler sees only the upload request. The insurance emergency number appears on the traveler's emergency screen.

## 9. Notifications (ch. 16)
- **Bell everywhere:** unread count and a single blink on arrival.
  - Newest first, unread in bold. Each item deep-links to its target. "סמן הכול כנקרא".
  - Items are deleted after 60 days.
  - Every Push, WhatsApp or email message also appears in the bell (BR-46).
- **Four layers:** system defaults → agency (SCR-A15) → trip override (SCR-A25) → traveler preferences (SCR-T12). Critical notifications are locked on.
- **Traveler defaults:**
  - Trip ready (on publish).
  - Pre-trip summary 3 days before.
  - Check-in by airline rule, otherwise 24h before, worded as a recommendation (BR-13); repeat reminder 6h before unless marked done.
  - Leave for the airport 3h before an international flight, 2h before a domestic one.
  - Morning brief at 08:00 local time.
  - Event reminder 2h before.
  - Car return 3h before; hotel check-out at 08:00.
  - "Something changed": immediately, critical.
  - Agent replied in chat.
  - Document requested, plus a reminder after 2 days.
  - "שומרים על קשר" 14 days after return: marketing, opt-in only.
- **Agent alerts:**
  - Insurance (see ch. 15).
  - Update awaiting approval: popup immediately, reminder after 4h.
  - Open exception: reminder after 24h.
  - Departing tomorrow: summary at 17:00.
  - New chat message.
  - Unanswered for 2h: escalate to the manager.
  - Low credits (<5) and credits expiring in 30 days: notify the manager.
- **Scheduling rules:**
  - Timing is relative to the event, in the event's time zone. Changing an event recalculates its notifications (BR-14).
  - Quiet hours are 22:00–07:00, in the traveler's location that day. Critical notifications pass through.
  - If a notification's time has already passed at publish: send now if the event hasn't happened, otherwise skip.
  - Notifications within 15 minutes are merged. At most 4 non-critical per day.

## 10. Emergency, chat, assistant (ch. 17)
- **Emergency (SCR-T14):**
  - The button is in every header, works offline, and is cached automatically.
  - Order on the screen:
    1. Local emergency numbers for the country of today.
    2. Insurance 24/7 line and policy number.
    3. Agency 24/7 line, then the agent's personal phone (only if given, only during the trip; BR-55).
    4. Israeli embassy or consulate.
    5. Tonight's hotel, with a taxi address card in the local language and an English toggle (BR-75).
  - Numbers are maintained by the agency per country, each with "עודכן ע״י הסוכנות" and a date.
- **Chat:**
  - Enabled per agency. When off, travelers get phone, email and WhatsApp buttons instead.
  - Family: one conversation per trip. Organized group: personal conversations plus a broadcast.
  - Messages written offline are queued.
  - Outside hours: auto-reply with the expected reply time and emergency numbers.
  - The agent can add an attached file to the file with one click. Quick replies are available.
- **Smart assistant (LLM): v1.1.** Answers only from the trip data, with a source; never invents. "Don't know" hands over to the agent. No answers to medical, legal or urgent questions.

## 11. Key business rules (ch. 18; full list BR-01..82 in the spec)
**Isolation, access and security**
- BR-01: isolate every request by agency.
- BR-02: an agent sees only assigned trips unless widened by the manager.
- BR-10/11: personal documents are visible only to their owner and the agency. They are cached offline encrypted, and every view is logged.
- BR-12: link token ≥128 bits, stored as a hash.
- BR-19: the audit log is append-only.
- BR-22: support access needs manager approval and lasts 24h.
- BR-41: traveler login with phone and password; the device stays logged in 90 days.
- BR-70: agent sessions. "Stay logged in" is off by default; idle timeout is 30 minutes with a warning 1 minute before; ticking it keeps the session 14 days. Logout clears local data.

**Filing documents**
- BR-03/04: confidence ≥0.9 is auto-filed; below that the field goes to לטיפול. Material fields are defined per category.
- BR-05: an existing value never changes without approval.
- BR-24: duplicate hash is skipped.
- BR-35: file ID format, shown everywhere next to the trip name.
- BR-45: ownership subsets.

**Time and location**
- BR-08: every time is stored with an IANA time zone and shown with a label such as "שעון ברצלונה".
- BR-09: an unverified location gets no pin and no distance.
- BR-23: "next event" is the first event that hasn't ended; during an ongoing event show "now" and "next".

**Publishing and credits**
- BR-06/07: 1 credit per trip, on the first publish only. The first publish is always manual. Later updates auto-publish only if the agency enabled auto-update; changes to existing events always need approval.
- BR-71: the agent is the final approver. One line in the publish dialog, no checkbox.
- Credits: up to 6 travelers = 1 credit, 7–20 = 2, more than 20 = group package. Nearest-expiry credits are used first.

**Display and wording**
- BR-68: agent and admin dates are `DD.MM.YYYY` and ranges "12.11.2026 – 19.11.2026" (LTR). Travelers see month names ("12–19 בנובמבר"). Never "12–19/11".
- BR-76: the green home card changes by phase: countdown before the trip; during it, a day board (day X of Y with a continuous bar, local time vs Israel, weather, currency vs ₪ with a calculator); after return, the agency message.

**Travelers and lists**
- BR-56: the packing list is shared; "ארזתי" is personal.
- BR-57: navigation is one button that opens the device's app. On iPhone the traveler chooses Waze, Google or Apple Maps once and the choice is remembered. Always offer "copy address" too.
- BR-60: calendar export is a one-way subscription feed.

**Roles**
- BR-77: the agency manager (Supervisor) can do everything an agent can, plus agency settings. An agent sees only "my settings".

**Legal and privacy**
- BR-61: the agency is the data controller; PALAMI is the processor.
- BR-62: one agreement (service + DPA), uploaded scanned before activation.
- BR-63/80: no checkbox for travelers. One line at password creation. The version the traveler saw is stored, and a material change shows a one-time "עדכנו את התנאים" notice.
- BR-64: marketing only with consent, prefixed "פרסומת", with one-click removal.
- BR-67: essential cookies only, so no cookie banner.
- BR-72: at most 2 marketing messages per month, none during the trip, none between 21:00 and 09:00.
- BR-78: legal documents are set at agency level.
- BR-82: retention 12 months after return (6–24 configurable), then deletion including backups within 30 days; logs 24 months, billing 7 years.

## 12. Permissions (ch. 19, short)
- **Agency manager:** everything, including agency settings, legal, and chat and emergency setup.
- **Agent:** assigned trips; opens files, uploads, resolves exceptions, publishes, edits trip notifications, edits emergency numbers.
- **Main customer:** sees according to the sharing mode. Adds documents, attractions and packing items. Can propose edits to agent events.
- **Companion:** like the main customer, but adds for themselves only.
- **Support:** temporary access only.

## 13. MVP scope and build order (ch. 7)
**MVP (must-have):**
- Agency isolation, auth, audit, file protection.
- Admin: agencies, onboarding wizard, employees, agreement, credits, support access, health, audit, tickets.
- Agent: simple view, help, big text, undo; customers and files; statuses; travelers and groups.
- Ingestion engine and checks; schedule; insurance check.
- Publishing.
- Traveler app: home, my trips, documents, offline, emergency, navigation links, info, my agent, traveler uploads and activities.
- Notifications engine with WhatsApp, email and bell.
- Legal minimum, roles, phone + desktop, accessibility (IS 5568, WCAG 2.2 AA).

**MVP "important" (can slip to 1.1):** file-match check, basic reports, "שומרים על קשר", calendar export, Push, chat, auto-update, post-return message.

**v1.1:**
- In-app map and daily route.
- Last-visit tracking.
- Export before deletion.
- Tablet design.
- Self-service employee management.
- LLM assistant.
- Ingestion by email forwarding (`hdr-2609-0031@in.palami.io`).
- Version restore, trip templates.
- Complementary offer from the agent ("מעוניין").

**v2:** marketing campaigns, discounts, supplier integrations and live flight status, feedback, store apps and Wallet, English, agency colour, CRM/GDS API, tasks per file, avatars.

**v3:** private continued use, B2C, white label, more languages.

**Build order:**
1. Infrastructure and the responsive, accessible skeleton with brand tokens.
2. Admin basics.
3. Customers and files.
4. Ingestion.
5. Schedule and insurance.
6. Publishing and the traveler app.
7. Notifications.
8. Agent UX and support.
9. Billing.
10. MVP "important" items.

## 14. Screens
- **Agent:**
  - A00 simple view, A01 login, A02 dashboard.
  - A03 new customer + file (one screen, two columns), A04 trip file with tabs: מסמכים והעלאה / סקירה וביטוח / לו״ז / נוסעים / מידע לנוסע / התראות לנסיעה / שיחה / היסטוריה.
  - A05 upload, A06 לטיפול, A07 update approval, A08 publish, A09 links, A10 bell, A11 history.
  - A12 branding (v2), A13 employees, A14 credits, A15 notification policy, A16 trips without insurance.
  - A17 customer card, A18 chats, A19 customers.
  - A20 my profile, A21 report a bug, A22 legal, A23 user menu, A24 settings (mine / agency), A25 trip notifications.
- **Traveler:**
  - T01 login, T02 home (3 phases), T03 schedule (day / week), T04 event details, T05 documents.
  - T06 map (v1.1), T07 info, T08 offline, T09 check-in, T10 your agent.
  - T12 notifications and settings, T13 my trips, T14 emergency, T15 chat, T16 assistant (v1.1), T17 bell.
  - T18 add document, T19 add to schedule, T20 privacy and accessibility, T21 terms updated.
  - Four tabs: בית, לו״ז, מסמכים, מידע. "עוד" sits in the header menu.
- **Admin:** M01–M14 (see `docs/prototypes/admin.md`).

## 15. Metrics events (ch. 26)
- doc_auto_filed / doc_needs_look / doc_conflict
- link_opened
- first_drop → trip_published
- field_corrected
- customer_trip_added
- emergency_opened / emergency_call_tap
- chat_message_sent / chat_first_reply
- agent_active / simple_view_on
- agent_contact_tap

## 16. Not covered by the spec yet
Technical architecture, a backlog with acceptance criteria, and a test plan.
