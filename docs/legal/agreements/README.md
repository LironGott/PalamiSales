# PALAMI service agreements (agency + independent agent)

Two versions from one source, so they stay in sync:
- `out/palami-agreement-agency.pdf`: travel agencies (multi-user; signed once by the agency manager).
- `out/palami-agreement-independent.pdf`: independent travel agent (sole proprietor).

Each is one document (spec BR-62): the agreement, Annex A (plan and price, filled in before signing), Annex B (data processing under reg. 15 of the Data Security Regulations 2017), Annex C (sub-processors), and signatures.

- Texts: `content.py` (`V("agency", "independent")` for text that differs). Layout: `build.py`. PDF footer: `print.cjs`.
- Build: `python3 docs/legal/agreements/build.py` (HTML + PDF; `--no-pdf` for HTML only).
- Word for legal review: `cd docs/legal/agreements && python3 export_json.py && node docx.cjs` → `out/*-legal-review.docx`.
  Track changes is on, and the first page lists the open questions for the lawyer (`REVIEW_NOTES` in `content.py`; delete that page before sending).
  If the lawyer edits the Word file, bring the accepted wording back into `content.py` and rebuild, so the PDF and Word stay the same.
- Preview artifact: https://claude.ai/artifact/CxjDJwZN85PNCRi7ovxP8L (published from `out/preview.html` + both HTML files).

Status (16.10.2026): version 1.0, based on research, not a legal opinion. **A lawyer must review it before it is sent.**
Open items: company name and number (company not registered yet; clause 12.4 lets PALAMI assign to it), final pricing model (spec ch. 25),
sub-processor names and locations (Annex C), support hours, the liability floor (₪5,000 agency / ₪2,000 independent), and whether the
company needs a privacy protection officer under Amendment 13.

Key positions (chosen to be fair and not intimidating): no minimum term (agency 30 days' notice, independent 14 days; PALAMI 60 days);
price changes need 30 days' notice and purchased credits keep their value; late payment stops only new publishing, so published trips and
the emergency screen keep working; liability capped at 12 months of fees with a floor (×3 for privacy/confidentiality breaches; no cap for
intent, gross negligence or bodily injury); unused credits stay valid until they expire, refunded pro rata if PALAMI ends the agreement or
the customer leaves over a change; 30 days to export after termination; a trip in progress stays available until 7 days after return;
no use of documents to train models; logo used outside the app only with consent; Israeli law, Tel Aviv–Jaffa courts.
