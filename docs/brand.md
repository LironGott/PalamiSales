# PALAMI brand (brand book v1.2, 2026-10)

> Full source: `docs/reference/brand-book.html` (artifact https://claude.ai/artifact/HBo5hGokUGWzEkyAp3Ujrv). Tokens: `brand/tokens/tokens.css`. Assets: `brand/`.

## Essence
- **Product:** the agency uploads documents, and PALAMI turns them into one digital trip file on the traveler's phone.
- **Slogan:** **כל פרטי הנסיעה בכף ידך**.
- **Mascot:** a beaver, chosen for diligence, building and order. It holds a green suitcase and a phone showing a fully checked list.
- **Values:** מסודר, אמין, חם, פשוט.

## Logo
- **Approved logo:** forest-green wordmark on white. Never change it.
- **Files:**
  - Full logo: `brand/logo/png/logo-full.png`
  - Wordmark: `brand/logo/svg/wordmark.svg`
  - Wordmark with tagline: `brand/logo/svg/wordmark-tagline.svg`
  - Mascot: `brand/mascot/mascot.png`
  - Mascot head: `brand/mascot/mascot-head.png` (favicon, sizes under 48px)
- **The one exception:** `wordmark-on-dark.svg` (white text, copper dot) is used only in the app's dark mode and on the admin dark top stripe.
- **Which version where:**
  - Full logo: splash, login, marketing, email.
  - Wordmark: headers, narrow spots.
  - Mascot: empty states and success.
- **Clear space:** X (the diameter of the copper dot) on every side.
- **Minimum size:** full logo 200px, wordmark with tagline 140px, wordmark 72px, mascot 16px.
- **Don'ts:** stretch, rotate, recolor, add effects, place on busy or green backgrounds, move the dot, regenerate the mascot with AI.

## Color

| Token | Hex | Use |
|---|---|---|
| `--palami-green` | #08402A | primary actions, headings, logo |
| `--palami-copper` | #C37237 | accent, dots, icons |
| `--palami-cream` | #F9E2C5 | soft surfaces, banners |
| `--palami-paper` | #FEFEFC | main background |

- **Usage ratio:** 60% paper and neutrals, 22% green, 10% cream, 6% copper.
- **Primary buttons:** always green. Never use white text on copper (3.6:1 contrast). For copper text, use copper-600 #A85C28.
- **Dark mode:** green becomes #74B590, copper becomes #D4884A.
- **Status colors:** these are not copper (copper hue is 25°; urgent and attention sit at 348° and 42°).

| Meaning | Fill | Tag background | Tag text |
|---|---|---|---|
| ✓ done | #5E9677 | #E6F0EA | #33704F |
| ! attention | #C28A0E | #FBF1D6 | #8A5F00 |
| ✕ urgent | #B91C3C | #FCE8EC | #B91C3C |
| i info | #1D5FA8 | #E4EEF8 | #1D5FA8 |
| ◌ waiting | dashed #A9C7B5 | #F0F2F0 | #5E6862 |

- For travelers, "attention" is soft copper. Red appears only for real emergencies.

## Type
Google Fonts, all with full Hebrew support.

**Families**
- **Rubik 600–800:** display, destination names, big numbers.
- **Assistant 400–700:** body, forms, buttons.
- **IBM Plex Mono 500:** flight numbers, file IDs, booking codes. Wrap Latin and numbers in `dir="ltr"`.

**Scale**

| Step | Size | Family and weight |
|---|---|---|
| 3xl | 44 | Rubik 800 |
| 2xl | 34 | Rubik 700 |
| xl | 28 | Rubik 700 |
| lg | 22 | Rubik 600 |
| md | 18 | Assistant 600 |
| base | 16 | Assistant 400 |
| sm | 14 | Assistant 500 |
| xs | 12 | Assistant 600 |

- Minimum body text on mobile is 16px.
- Line height is 1.6 for running text and 1.2 for headings.

## Systems (`data-product` on `<html>`)

| | Agent | Traveler | Admin |
|---|---|---|---|
| Background | #F4F6F4 | #FBF8F2 | #F4F6F4 + green top stripe |
| Green | primary and nav only | headers, buttons, icons | primary and nav |
| Copper | not in UI | highlights and reminders | not in UI |
| Density | 15px text, 44px rows | 17px text, 48px taps | 40px rows |
| Corners | 6–12px | 16–28px | small |
| Mascot | login and empty states | splash, success, empty states | stripe |
| Motion | fast and minimal | small happy animations (V fills) | none |

## Signature component: trip item row (`.trip-item`)
- **Look:** a cream row (#FBF3E3) with a filled forest-green icon (32px) and a sage V circle (#5E9677, 30px).
- **Size:** min height 64px, radius 14px.
- **RTL layout:** icon on the right, circle on the left.
- **States:** done (V), pending (dashed circle), attention (copper "!").

## UI
- **Radii:** xs 6, sm 10, md 14, lg 20, xl 28. Shadows are soft and green-tinted.
- **Spacing grid:** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64. Mobile gutter 16px.
- **Max widths:** traveler 560px, agent 1280px.
- **Touch targets:** minimum 44px.
- **Icons:** filled, forest green, Material Symbols Rounded (Filled).
- **Breakpoints:** phone ≤639, tablet 640–1023, desktop ≥1024. On phones the agent tables become cards and the sidebar becomes a bottom bar.

## Co-branding
- **Traveler app:** the agency logo is at the top. "מופעל על ידי PALAMI" sits at the bottom, 14px high, not clickable.
- **Agency color:** from v2 it may replace `--brand` in the header and primary button. If it has less than 4.5:1 contrast, fall back to PALAMI green. Status colors never change.
- **Agent system:** PALAMI logo on top, agency logo and name below it.

## Voice
- Short, calm, precise, like a good agent on the phone.
- Prefer gender-neutral phrasing ("אפשר", "כדאי", "מומלץ").
- Examples:
  - ✓ "הטיסה לברצלונה יוצאת מחר ב־06:40. כדאי להגיע לנתב״ג עד 03:40."
  - ✕ "התראה: אירוע טיסה מתקרב (מזהה 4471)."
  - ✓ "הקובץ גדול מדי. אפשר להעלות קובץ עד 20MB, או לצלם שוב."
  - ✕ "שגיאה 413."
- No exclamation-heavy or emoji alarm copy.

## Icons and PWA
- **Home screen and install:** `brand/icons/apple-touch-icon.png` (180), `icon-192`, `icon-maskable-192/512`, `favicon-16/32/48`.
- **Status bar color:** #08402A. Splash background: #FEFEFC.
- **Missing from the repo:** `favicon.ico/svg`, `icon-512`, `icon-monochrome`, `og-image`, the `tokens/*.json`, and the tailwind preset. Request these from the designer if needed.
