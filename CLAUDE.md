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
- Stage 1–2 done: analysis, competitors, messaging and 4 design concepts. Published at https://claude.ai/artifact/6LFttB6EeWZ9st5nu8m6Ni (source: `docs/website/concepts/`). Research notes: `docs/website/competitors.md`, `docs/website/aws.md`. Prototype screenshots: `docs/website/screenshots/`.
- Positioning (user clarification): PALAMI is a B2B SaaS with a B2B2C experience. Two value pillars: (1) the agency workspace and management system (dashboard, trip statuses, missing items, control, customers, documents) as the primary pillar; (2) the digital trip experience for travelers. Do not present it as only a traveler app.
- Recommendation v2 awaiting approval: concept E "מרכז הבקרה של הסוכנות" (dashboard-first), with "how it works" from A and the V-row from D on mobile. Headline: "כל הנסיעות של הסוכנות, תחת שליטה. כל פרטי הנסיעה, בכף היד של הנוסע." Agency-side capabilities verified by the user (2026-10-15): all listed management features exist in the developed system (dashboard, statuses, missing items, urgency, trip file, ingestion with exceptions and approval, customers, chat, publish, notification policy, roles, simple view, history) EXCEPT basic reports, which must not be claimed. Traveler app status still to confirm.
- AWS: apply with an email on @palami.io; site must be fully functioning and public.
