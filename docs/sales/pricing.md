# PALAMI pricing and dynamic quote (draft, 2026-10-16)

> Status: a proposal for the user's approval. All the numbers are placeholders and live in one place: `PRICING` at the top of the script in `sales/quote/quote.src.html`.

## What the spec says (source of the model)
- Chapter 25 ("חיוב ונתוני שימוש"): the payment model is not decided yet. The system collects data for four candidate models: a trip bank (credit per published trip), payment per traveler, a monthly subscription by tiers, and paid add-ons (WhatsApp/SMS, storage, AI assistant).
- Business goals: "הכנסה חוזרת מדמי פלטפורמה ובנק נסיעות. קרדיט נצרך רק כשנסיעה מתפרסמת ללקוח."
- F11.1: the trip bank is the default. BR-06: a credit is used once per trip, on the first publish.
- BP-12: credits are priced by trip type and traveler count (up to 6 = 1, 7–20 = 2, over 20 = group package). The credits closest to expiry are used first. The manager is alerted when the balance runs low.
- Admin: packages בסיס / Pro / קבוצות. Credits are loaded with an expiry date (end of year, one year, half a year).
- Chapter 25 also notes that SMS and WhatsApp messages cost money and add up in big groups.

## The model in the quote
**Monthly system fee + a yearly traveler bank.** It is the "platform fee + bank" hybrid from the spec, with the traveler as the unit the agency buys (the user's request: "בנק נוסעים").
- A traveler is counted once, when the trip is first sent to them (same moment as BR-06). Drafts and trips cancelled before publish are not counted.
- Groups need no separate package: every traveler counts once. This replaces the 1/2/package credit table with one simple rule.
- The bank is valid for 12 months. Top-ups at the same price per traveler.
- Volume tiers (all-units). The bank size picks the tier automatically:

| Tier | Travelers per year | Per traveler | System fee per month | Users |
|---|---|---|---|---|
| בסיס | 100–399 | ₪12 | ₪149 | up to 3 |
| מקצועי | 400–1,199 | ₪9.50 | ₪249 | up to 8 |
| מתקדם | 1,200–3,999 | ₪7.50 | ₪449 | up to 20 |
| ארגוני | 4,000+ | ₪6 | ₪690 | unlimited |

- Monthly price = system fee + (bank × price per traveler) / 12. Extra user ₪39/month. Optional: special discount (5–20%) and 10% off for paying the year upfront. Prices exclude VAT. Quote valid 30 days.
- Examples: 500 travelers ≈ ₪645/month; 1,000 ≈ ₪1,041; 2,000 ≈ ₪1,699.
- The tiers are tuned so that the jump at the bottom of each tier is small (1,199 → ₪1,198, 1,200 → ₪1,199). The builder shows a hint like "at 1,200 travelers you move up to מתקדם" to help upsell.

**Open decisions for the user:** the numbers; whether WhatsApp/SMS are included or billed as add-ons (chapter 25 suggests counting them); a setup fee (none in the draft); a pilot benefit (use the free-text line in the builder); whether to keep the spec's trip credits internally (1 traveler-unit = 1 traveler, so the ledger stays in the spirit of BP-12).

## Market survey: how to build such a quote
**Competitors (travel-agent tools, priced per seat, not per traveler):**
- Travefy: about $31 per user per month billed yearly, $39 monthly ([Capterra](https://www.capterra.com/p/148927/Travefy-Agent/), [Software Advice](https://www.softwareadvice.com/travel-management/travefy-agent-profile/)).
- Tern: $49 per seat per month monthly, $35 quarterly or yearly ([tern.travel/pricing](https://tern.travel/pricing)).
- AXUS: from $35 per seat per month ([TrustRadius](https://www.trustradius.com/products/axus-travel-app)).
- Umapped: from about $25 per month, 10% off yearly ([TrustRadius](https://www.trustradius.com/compare-products/umapped)).
- Takeaway: the market anchor is about ₪100–180 per agent per month for itinerary tools without a full traveler app and without automatic filing. PALAMI charges by travelers served (the value metric). Seats stay cheap, so the whole team can work in it, and the traveler app is the differentiator.

**Pricing-page and proposal practices applied:**
- Three or four tiers, with the customer's tier marked ("ההצעה שלכם"); showing all the tiers gives transparency and anchoring ([PayPro checklist](https://payproglobal.com/wp-content/uploads/2025/11/SaaS-Pricing-Page-Optimization-Checklist.pdf), [Monetizely on anchoring](https://www.getmonetizely.com/articles/the-anchoring-effect-in-saas-pricing-using-high-prices-to-drive-sales)).
- One value metric (travelers), with few pricing dimensions ([River guide](https://rivereditor.com/guides/how-to-design-saas-pricing-pages-2026)).
- Yearly-payment discount of 10–20%; above 25% sets a discount expectation ([Fungies](https://fungies.io/?p=36581)). The draft uses 10%.
- Prepaid credit or bank: volume price per unit, a clear expiry (12 months is common) with reminders before it expires, and a clear mapping of what one unit is ([Monetizely on credits](https://www.getmonetizely.com/articles/credit-based-pricing-systems-flexibility-without-complexity), [Lago](https://getlago.com/blog/credit-based-pricing), [Bunny](https://bunny.com/glossary/prepaid-credits/)). Do not hard-stop when the bank runs out (publishing is critical); top up or bill the overage.
- The monthly price is the hero number; the yearly total and the breakdown sit beside it. Short lists of what the customer gets, no feature dump. A quote number, a date and a validity date. VAT stated (Israeli B2B convention: prices exclude VAT).

## The tool
- Source `sales/quote/quote.src.html`. Build: `python3 sales/quote/build.py` writes `sales/quote/offer/index.html`, to upload to `www.palami.io/offer/` (noindex). Not deployed; it needs the user's approval.
- Builder: agency name, email or mobile, traveler bank (slider, number, presets). Optional settings: users, discount, yearly prepay, a personal line. Send: email (mailto) or WhatsApp (wa.me) with a ready message and a link; copy link; save as PDF (A4 print).
- The client link holds the quote in the query string (`?a=&n=&id=&dt=...`) and opens a clean proposal view with "שמירה כ־PDF". Quote IDs: `PAL-YYMM-NNN` (counter kept in the browser).
- Preview artifact: https://claude.ai/artifact/Cf8Ho4dBNL7KLiPkVvFUoc (inside the artifact, the client link points at www.palami.io/offer and PDF saving is turned off).
- Agency-side features listed in the quote come from the verified list in CLAUDE.md (no reports). The traveler app is specified, not built yet: check before sending to customers.
