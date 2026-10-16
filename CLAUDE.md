# PALAMI: project memory for Claude

**PALAMI** (palami.io) is a B2B SaaS for Israeli travel agencies. The agency drags booking documents (PDF or images) into a trip file. An AI engine classifies them, extracts the fields, names each file and files it automatically. The traveler gets one link to a mobile web app (PWA) that holds the whole trip: schedule, documents, emergency info, chat with the agent, notifications. It works offline.
Slogan: **"כל פרטי הנסיעה בכף ידך"**. Mascot: a beaver (הבונה). UI language: **Hebrew, RTL**.

The repo name "PalamiSales" is historical; the product is PALAMI.

## Read these before building anything
| File | What |
|---|---|
| `docs/spec-summary.md` | Distilled logical spec (draft 0.9): vision, three systems, ingestion model, statuses, data model, fields, rules BR-xx, MVP scope, build order, screens |
| `docs/brand.md` | Brand book: logo usage, colors, type, per-system look, voice |
| `brand/tokens/tokens.css` | Design tokens; set `<html data-product="traveler|agent|admin" dir="rtl" lang="he">` |
| `docs/prototypes/traveler.md` | Blueprint of the clickable traveler prototype (every screen, flow, sample data, CSS components) |
| `docs/prototypes/agent.md` | Blueprint of the agent prototype |
| `docs/prototypes/admin.md` | Blueprint of the admin prototype (**out of scope for now**) |
| `docs/reference/*` | Original sources, the ground truth: `spec.html`/`spec.txt` (full spec, 28 chapters), `brand-book.html`, `prototype-*.html` (open in a browser to click through) |
| `brand/` | Logo (png/svg), mascot, app icons |

Original artifacts on claude.ai (owner: the user):
- Brand book: https://claude.ai/artifact/HBo5hGokUGWzEkyAp3Ujrv
- Spec: https://claude.ai/artifact/QEa9EhST9oHB7SiDfPTHtE
- Traveler prototype: https://claude.ai/artifact/As9pjqQKDaz4zRjXPf13Pj
- Agent prototype: https://claude.ai/artifact/W7xw6yQtf1r94evC5LdTE5
- Admin prototype: https://claude.ai/artifact/DNPd741xZ4J3GCzZJHtUTi (not in scope yet)

If the user says the spec or prototypes changed, re-read the artifact with the Artifact tool (`action: read`) and update `docs/`.

## Three systems (one DB, one brand, different look)
- **Agent** `app.palami.io`: desktop-first, also on phones. Professional, quiet, dense. Green only for primary actions and navigation; no copper.
- **Traveler** `trip.palami.io`: phone-first PWA opened from a link. Warm paper background, cream item rows with a sage V check, the beaver in the right moments. Agency logo on top; "מופעל על ידי PALAMI" at the bottom.
- **Admin** `admin.palami.io`: PALAMI staff. Agent look plus a green top stripe and an ADMIN badge.

## Non-negotiables (from the spec and brand book)
**Ingestion and data**
- "The agent only drags." Filing is automatic. The agent acts only on:
  - an uncertain field (confidence <0.9 goes to "לטיפול")
  - an update to an existing event (before/after, approve or reject)
  - the first publish (costs 1 credit)
- Documents go only into a specific trip; there is no global drop zone.
- No passports are stored in v1.
- Every time is stored with an IANA time zone and shown with a label ("שעון ברצלונה").
- Trip ID format `HDR-2609-0031`: agency code, YYMM, then a running number. It never changes.

**Display rules**
- Status colors carry one meaning everywhere: crimson urgent, honey attention, sage done, blue updated, grey waiting. Always show an icon and a word, never color alone. Never color a whole row.
- Dates:
  - Agent and admin: `DD.MM.YYYY`, ranges `12.11.2026 – 19.11.2026`.
  - Traveler: month names ("12–19 בנובמבר").
  - Never "12–19/11".
- Latin text and numbers inside Hebrew go in `dir="ltr"` / `unicode-bidi:isolate`.

**Accessibility**
- IS 5568 / WCAG 2.2 AA.
- Touch targets ≥44px (traveler 48px). Body text ≥16px (traveler 17px). Big-text mode.
- Respect reduced motion.

**Copy**
- No comma before a word starting with the conjunction "ו" (user rule, 2026-10-15).
- Spell "הכל" without vav (not "הכול") (user, 2026-10-15).
- Website term for what the agent drags: "מסמכים" (not "הזמנות" or "אישורים"); keep it consistent sitewide (user, 2026-10-15).
- Gender-neutral Hebrew ("אפשר", "כדאי"). The prototypes use feminine forms; neutralize them.
- Short, calm, human ("הטיסה יוצאת בעוד 3 ימים", not "סטטוס: פורסם"). No jargon like PNR or OCR toward travelers.

**Traveler app**
- Four tabs: בית, לו״ז, מסמכים, מידע.
- The bell and the "חירום" button are in every header. The emergency screen works offline.

## Status of the work
- 2026-10: Knowledge captured: spec, brand and prototypes saved into `docs/` and `brand/`. No application code yet.
- Next: the user will send a dedicated prompt for building a **website**. Follow it, and use the docs above as the source of truth for content, design and behavior.

## Working conventions
- Develop on the branch the session specifies; commit with clear messages and push.
- Keep `CLAUDE.md` and `docs/` updated when decisions change.

## Marketing website project (palami.io), started 2026-10
- Brief: a small, bilingual (HE RTL / EN LTR) one-page marketing site for agencies, for AWS Activate / Founders Club. Sections: Hero, How it works, Value, Product peek, Demo request form. No CRM, no invented claims, no publishing or DNS changes without approval. All communication with the user in Hebrew.
- Homepage design draft v1 (concept E, full page, HE): https://claude.ai/artifact/XrnMu93fqebrtuckHTCDA2, source in `site/`. Hero headline now "ראש שקט לסוכן. נסיעה מסודרת לנוסע." with a "ping-pong" section (traveler questions vs answers in the app).
- Stage 1–2 done: analysis, competitors, messaging and 4 design concepts. Published at https://claude.ai/artifact/6LFttB6EeWZ9st5nu8m6Ni (source: `docs/website/concepts/`). Research notes: `docs/website/competitors.md`, `docs/website/aws.md`. Prototype screenshots: `docs/website/screenshots/`.
- Origin pain (user, 2026-10-15): PALAMI was born to solve scattered trip documents (some in WhatsApp, some in email, some with the agent, some with each spouse). It is NOT a CRM for agents; never let the site read like one. The buyer is the agency (it buys the traveler subscriptions), so the hero shows agent side + traveler side (real dashboard + phone) with an agency-first lead. The animated "drag documents → AI files → traveler phone" visual lives in the "איך זה עובד" section, placed right after the hero.
- Positioning (user clarification): PALAMI is a B2B SaaS with a B2B2C experience. Two value pillars: (1) the agency workspace and management system (dashboard, trip statuses, missing items, control, customers, documents) as the primary pillar; (2) the digital trip experience for travelers. Do not present it as only a traveler app.
- Recommendation v2 awaiting approval: concept E "מרכז הבקרה של הסוכנות" (dashboard-first), with "how it works" from A and the V-row from D on mobile. Headline: "כל הנסיעות של הסוכנות, תחת שליטה. כל פרטי הנסיעה, בכף היד של הנוסע." Agency-side capabilities verified by the user (2026-10-15): all listed management features exist in the developed system (dashboard, statuses, missing items, urgency, trip file, ingestion with exceptions and approval, customers, chat, publish, notification policy, roles, simple view, history) EXCEPT basic reports, which must not be claimed. Traveler app status still to confirm.
- AWS: apply with an email on @palami.io; site must be fully functioning and public.

## Website: files, build and launch (2026-10-15)
- Source in `site/`: `index.html` (HE), `en/index.html` (EN), shared `css/site.css` + `js/site.js` (HE/EN strings for peek, form, menu), self-hosted `fonts/`. Legal pages generated by `site/tools/legal.py` (privacy + accessibility, HE/EN).
- When changing Hebrew copy, update `en/index.html` (and `js/site.js` strings) too.
- Build: `python3 site/tools/build.py` → `site/dist/` (full HTML docs, canonical/hreflang/OG, robots, sitemap, 404, favicon.ico). `--preview` → `site/.preview/` for the artifact. `FORM_ENDPOINT=...` connects the form. See `site/DEPLOY.md`.
- The artifact preview is published from `site/index.html` with `url` = the homepage artifact, plus the files from `site/.preview/`.
- Measurement (user approved 2026-10-15): no analytics tool and no cookies at launch. The demo form sends a `source` field (UTM tags or referrer, else "direct"); Google Search Console after launch; Plausible only when paid campaigns start. See `site/DEPLOY.md`.
- Decisions (user, 2026-10-15): AWS Amplify hosting; Formspree for the form; domain palami.io at GoDaddy (DNS stays there, www.palami.io is the main address, palami.io forwards); mailbox info@palami.io (replaces hello@); the user is the accessibility coordinator (statement lists info@ and phone, approved); keep form data 24 months; company not registered yet ("PALAMI" for now); a lawyer will review the legal pages.
- Launch runbook and Amplify settings: `site/DEPLOY.md`, `site/amplify/`. Formspree endpoint https://formspree.io/f/mwlvwbjn (default in build.py). **LIVE since 2026-10-15 at https://www.palami.io** (Amplify app palami-site, branch main, eu-north-1; temp URL main.derxdl2rg7k45.amplifyapp.com). Updates: rebuild, zip `site/dist/` contents, Amplify > main > Deploy updates.

## Website: copy decisions (2026-10-15)
- Hero eyebrow "העוזר האישי של סוכן הנסיעות" (EN "The travel agent’s personal assistant"); H1 unchanged; bold lead "כל מסמכי הנסיעה של הלקוחות, מסודרים אוטומטית ובכף היד של הנוסע." then "גוררים את המסמכים, מערכת AI מתייקת הכל ואתם יודעים בכל רגע מה עוד חסר בכל תיק."; hero CTAs: demo + how it works (demo hidden on phones, the sticky bar has it).
- Page title/description start in Hebrew (no "PALAMI:" prefix, it breaks RTL in share previews); never "מערכת לניהול נסיעות" (sounds like CRM).
- Motion: only the how-it-works animation, the traveler lock-screen notifications (drop in once) and the peek home screen cycling before/during/after (pauses on hover, arrows/drag/dots). No hero phone rotation, no auto-playing peek tabs, no scroll arrows in filter rows.

- Idea (user, 2026-10-15): later, a separate site for private travelers who want to use PALAMI directly. Not planned yet; brand-level assets (slogan "כל פרטי הנסיעה בכף ידך") should stay neutral between agencies and consumers.
- B2C layout options (2026-10-15, not decided): https://claude.ai/artifact/VsMDRaM7iYnHntEMGrTLxd, source `docs/website/b2c/`. A toggle, B split homepage, C traveler-first, D keep agency homepage + strip + /travelers page. Recommended: D for the first month, B later.

## Website: confirmed details and open reminders
- Contact (approved 2026-10-15): email info@palami.io (being created by the user), phone 054-2245627.
- TODO (reminder): registered company name not decided yet. Site uses "PALAMI" as placeholder in footer and privacy policy; replace once the company is registered.
- Real agent-system screenshots (work in progress, from the user, 2026-10-15) are in `site/img/r-*.webp` and used for the agent side. Traveler screens still from the prototype. Real system also has: two filter rows (trip status, publish status), "only trips without active agent" toggle, trip actions (republish, view as traveler, edit trip, cancel trip). TODO: user will give system access later. Traveler app is specified (not yet developed): present without promising availability.
- Technical questions (hosting, form provider, DNS) postponed by the user until design is final.

## Agent calendar and trip sharing (spec 1.0, 12.10.2026; in development)
- Spec: https://claude.ai/artifact/TgteZe9s616ZngiTruwLLv (`docs/reference/spec-calendar-sharing.html`), prototype: https://claude.ai/artifact/K2rQnoKuWBWBqtVfrbwPEf (`docs/reference/prototype-calendar.html`).
- Calendar tab (SCR-A26): monthly/weekly view of all departures and landings (agency-wide for managers, filter by agent), status marks on cards. Sharing a trip with another agent (SCR-A27): "החלפה" (full work + notifications) or "שיתוף מידע" (view only), optional end date. Absence cover plans (SCR-A28): split active trips between substitutes for a period. View-permission levels per agent (BR-90).
- Calendar and sharing will be available when the website launches (user, 2026-10-15): present them as existing, no "coming soon" tag.
- Website uses: calendar card + calendar screenshot (`site/img/r-calendar.webp`, from the prototype), "teamwork, even on vacation" card. Also added: traveler Push notifications, agency-scheduled reminders, contact after return, "ראש פנוי לנסיעה הבאה" band.

## Service agreements for agencies (2026-10-16)
- Two versions (agency, independent agent) built from one source in `docs/legal/agreements/` (see its README). PDF in `out/`. Preview: https://claude.ai/artifact/CxjDJwZN85PNCRi7ovxP8L
- One signed document = agreement + pricing annex + data-processing annex (reg. 15) + sub-processors (spec BR-62). Pricing model not final (spec ch. 25): Annex A is a fill-in form, with the trip bank as default.
- Tone: short, fair, plain Hebrew with a non-binding "בקצרה" box. Needs lawyer review and the company details before sending.
