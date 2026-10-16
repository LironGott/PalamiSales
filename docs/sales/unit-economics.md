# PALAMI unit economics (estimate, 2026-10-16)

> Estimates for deciding on prices, not measurements. Replace them with real numbers once the pilot runs (chapter 26 metrics + usage report F11.2). The same assumptions are in `COSTS` in `sales/quote/quote.src.html`, which shows the margin of every quote in the builder (internal only).

## Variable cost per traveler (≈ ₪1.2, with buffer)
Assumptions: about 8 documents per trip, 2.6 travelers per trip, $1 ≈ ₪3.6.

| Item | Assumption | ₪ per traveler |
|---|---|---|
| AI filing | Claude Sonnet 5.5 at $2 / $10 per million tokens; a 2-page document ≈ 7K input + 0.8K output tokens ≈ $0.02–0.03; 8 documents per trip. Haiku 5.5 ($0.10 / $0.50) would cost about 20× less, if quality holds | ≈ 0.25 |
| WhatsApp | Utility template ≈ $0.0053 per message in Israel (Meta changed to per-message pricing in 7/2025); about 12 messages per traveler per trip; free inside an open service window | ≈ 0.25 |
| SMS | Login code and fallback, about 5 per traveler, about ₪0.06 each (no verified 2026 price: get quotes from local providers) | ≈ 0.3 |
| Storage, email, push | S3 + SES, about 20MB per trip kept for 12 months | < 0.05 |
| Buffer | Retries, re-processing, updates | ≈ 0.35 |

Card clearing and invoicing: about 1.5% of revenue.

## Cost per agency per month (support and account care)
סולו ₪40 (self-serve onboarding), בסיס ₪120, מקצועי ₪200, מתקדם ₪300, ארגוני ₪500. That is about 1–3 hours a month at ₪150 an hour, plus setup spread over the year.

## Contribution per quote (from the builder)
| Travelers | Tier | Price per month | Costs | Left for us |
|---|---|---|---|---|
| 70 | סולו | ₪155 | ₪49 | ₪106 (68%) |
| 200 | בסיס | ₪332 | ₪145 | ₪187 (56%) |
| 500 | מקצועי | ₪645 | ₪260 | ₪385 (60%) |
| 1,000 | מקצועי | ₪1,041 | ₪316 | ₪725 (70%) |
| 2,000 | מתקדם | ₪1,699 | ₪525 | ₪1,174 (69%) |
| 4,000 | ארגוני | ₪2,690 | ₪940 | ₪1,750 (65%) |

The cost per traveler is low (about 10–15% of the price per traveler). The real cost is human support per agency. That is why small agencies get a low fee only with self-serve onboarding.

## Fixed costs and break-even (the open question)
Not known yet: team salaries, the actual AWS bill, a WhatsApp BSP fee, accounting and legal. Rough scenarios, at an average contribution of about ₪350 per agency per month:

| Fixed monthly cost | Example | Agencies needed |
|---|---|---|
| ₪5,000 | Infrastructure and tools only, founders without salary | ≈ 15 |
| ₪30,000 | + one developer part-time | ≈ 85 |
| ₪80,000 | Two developers + support person | ≈ 230 |

Market: about 750 travel agencies in Israel, about 94% of them single-owner ([Rentech Digital, 4/2026](https://rentechdigital.com/smartscraper/business-report-details/list-of-travel-agencies-in-israel); vendor figures vary a lot). So most customers will be small (סולו/בסיס). Covering a full team needs a large share of the Israeli market, larger agencies and groups, or growth beyond (B2C, abroad, add-ons).

## Market fit
- Competitors charge per agent: about $25–49 per agent per month (≈ ₪90–180), without automatic filing and with a weaker traveler app. A one-person agency on סולו with 70–150 travelers pays ₪155–242, close to one competitor seat, with the traveler app included.
- ₪6–13 per traveler is a small share of what an agency earns on a trip. Validate this in pilot interviews.

## Sources
- Claude API prices: Anthropic pricing (claude-api reference, cached 2026-10-06).
- WhatsApp Israel rates: [SleekFlow](https://sleekflow.io/blog/whatsapp-business-api-pricing-updates-2025), [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing), [hon.co.il](https://www.hon.co.il/?p=280241).
- SMS: [consumers.org.il](https://www.consumers.org.il/category/reduce-the-price-of-sms) (marginal cost ≤ ₪0.05; not a commercial price).
- Agencies in Israel: [Rentech Digital](https://rentechdigital.com/smartscraper/business-report-details/list-of-travel-agencies-in-israel), [Infobel](https://www.infobelpro.com/companies/israel/travel-agencies).

## Interactive model
`sales/model/` (build: `python3 sales/model/build.py`, it reads PRICING and COSTS from the quote source). Preview: https://claude.ai/artifact/BH7d45qhFkcvpRqPrEe2CG. Inputs: number of agencies by size (and travelers per year for each size) and fixed monthly costs (three scenarios). Output: monthly and yearly profit, a bridge from revenue to profit, break-even and a profit-by-agency-count chart. Example mix (25 solo, 15 small, 7 mid, 2 large = 49 agencies): about ₪13.8K left per month. That is ≈ +₪6.5K with the lean scenario and ≈ −₪21.7K with one developer, whose break-even is about 126 agencies.
