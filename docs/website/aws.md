# AWS Activate and AWS Founders Club Tel Aviv: website and email requirements

**Method caveat:** I could not open any of the pages directly. WebFetch and curl to aws.amazon.com, startups.aws.com, aws-experience.com, repost.aws and web.archive.org were all blocked: the DNS lookup failed, or the proxy returned 403. Everything below comes from search-engine extracts of those official pages. The text in quotation marks is the page text as the search tool returned it. It is close to verbatim, but I could not check it word for word against the live pages. Re-check on the live pages before anyone relies on the exact wording.

## (a) Official eligibility requirements

**AWS Activate Credits page** (https://aws.amazon.com/startups/credits/)
- Both tiers: the startup must be **pre-Series B** and **founded in the last 10 years**. It must have **"a company website or company profile"** and be new to Activate credits, or be asking for more than it got before.
- Some versions of the page also require an **"AWS Account on Paid Tier Plan"**. Third-party guides say new accounts start on a Free plan that cannot receive credits. I could not verify that claim against an AWS page.
- **Founders tier:** for self-funded startups with no Activate Provider. The credits page says "Up to $5,000 USD in Activate Credits, starting with $1,000". The step-by-step guide says Founders gives $1,000, and "select startups may qualify for up to $5,000 over time".
- **Portfolio tier:** needs an **Organization ID (Org ID)** from an Activate Provider such as an accelerator or VC. The current page says "Up to $200,000 USD". Older and landing pages say up to $100,000, so the pages conflict. One page says the most recent funding round must be "within the last 12 months, if applicable". Without an Org ID, you are "initially eligible for the Founders Package".

**Step-by-step guide** (https://aws.amazon.com/aws-startups/learn/applying-for-aws-activate-credits-a-step-by-step-guide/)
- Founders requirements: **"have a fully functioning website"**, be founded in the past 10 years, be new to Activate credits, and be self-funded or pre-Series B.

**Activate Terms & Conditions** (https://aws.amazon.com/activate/terms/, last updated 22 Jan 2026)
- Section 1.1: "By providing your website URL, you authorize us to use automated means to collect publicly available information from your website to evaluate your credit application."
- AWS "may accept or reject any such application in our sole discretion". This wording also appears at https://aws.amazon.com/activate/portfolio-detail/requirements/.
- Government entities cannot take part. You need a valid AWS account and must complete registration.

**AWS Founders Club Tel Aviv** (https://aws-experience.com/emea/tel-aviv/program/aws-founders-club)
- The page describes the club only in general terms: it is for "founders of early stage startups who are looking to build and expand their network, meet investors and benefit from what AWS has to offer".
- Benefits: it is free, with a co-working space on Floor28, a monthly business event, 1:1 technical meetings, and "up to $10,000 in AWS Credits" (Activate).
- **Not verified:** I found no published eligibility criteria for Tel Aviv. The page lists no website, email, funding or stage rules. The $10K figure is higher than the $5K Founders cap, which suggests it is club-specific or a Portfolio-style Org ID route. The KSA Founders Club page (a different region) says "applications are evaluated to determine fit". Tel Aviv likely works the same way, but that is not confirmed.

## (b) What AWS says about the company website and email

**Website (official):**
- The credits page requires "a company website or company profile". The step-by-step guide requires "a fully functioning website".
- The Terms say the website is crawled automatically to evaluate the application. In practice, the site must be public and readable, and its content is part of the review.
- **Not found on any official page:** an explicit "not under construction" rule, a "must describe the product" rule, or a LinkedIn requirement. Those are inferences from "fully functioning" and the automated crawl, not stated rules. The word "profile" in the credits page may mean a public company profile such as LinkedIn or Crunchbase, but AWS does not say which.

**Email domain (official, from the step-by-step guide). This matters for Palami:**
- Use **"your business email address (matching your startup's domain)"** for **both the AWS Activate profile and the credit application**.
- Consistent domain information "helps validate your application and confirm your startup's credentials".
- When creating a new AWS account, use the business email for consistent domain information. When linking an existing account, check that its contact info uses the business email.
- Exception: the **AWS Builder ID** is personal. The guide says to create it with a personal email, because it follows you across jobs.

For Palami this means: apply from an address such as name@palami.io, list https://palami.io as the website, and make sure the linked AWS account's contact email is also @palami.io. A Gmail address on the application is not banned outright, but it goes against AWS's own guidance.

## (c) Rejection reasons stated by AWS or seen on re:Post

**Official (FAQ at https://aws.amazon.com/startups/faq):**
- AWS Activate "was unable to confirm my association with my AWS Activate Provider" (Portfolio).
- Wrong AWS account selected, or wrong information such as the wrong email address.
- Account-linking errors, for example an account already linked to another Builder ID.
- AWS keeps sole discretion and gives no detailed reasons. The standard rejection notice says the application "does not meet one or more internal requirements".

**Community answers on re:Post (not official AWS policy; many look AI-generated, 1-2 years old):**
- A user was rejected three times after entering a **product URL rather than the corporate website**. The reply said "even small discrepancies between your application, company website, and public records can trigger rejection". (https://repost.aws/questions/QUVuZGx6GyQ2SvJte7KaHalg/)
- A generic "internal requirements" rejection; suggestions were a live website, a valid billing profile and consistent business data. (https://repost.aws/questions/QUh20KPcOWTZ24LmmStPIa3g/)
- Repeated Founders rejections: AWS doesn't explain them, and support sometimes asks for incorporation documents and a use-case justification. A prior Founders grant blocks a repeat Founders grant, even if those credits went unused. (https://repost.aws/questions/QUq-hqNzjaTq-9-IBFvxdhlg/)
- Escalation route: the Activate contact form at https://aws.amazon.com/activate/contact-us/, or your Activate Provider for Portfolio.

## (d) Official requirements vs. quality recommendations

**Official (AWS pages):**
1. Pre-Series B, founded within 10 years, and new to Activate credits (or asking for more than before).
2. A company website or company profile, described as a "fully functioning website" in the guide, which AWS crawls automatically.
3. A business email matching the startup's domain on the Activate profile and the application (guide). The Builder ID uses a personal email.
4. An AWS account on the Paid Tier plan (some page versions).
5. Portfolio only: a valid Org ID from an Activate Provider, and provider affiliation must be confirmable.
6. AWS decides at its sole discretion.

**Quality recommendations (community or inferred, not stated by AWS):**
- The site should be live on its own domain, not a placeholder or "coming soon" page.
- It should clearly name the company and describe the product.
- The company name should be the same on the application, the website footer or about page, LinkedIn and registry records.
- Use the corporate site rather than a product subdomain or app URL.
- Have a matching LinkedIn company page.
- Keep billing details valid.

**Could not verify:**
- Exact current wording and credit amounts on the live pages ($100K vs. $200K Portfolio).
- Any Tel Aviv Founders Club eligibility rules.
- Whether a non-matching email domain is an automatic rejection or just a negative signal.
- Any explicit LinkedIn or "under construction" rule.
