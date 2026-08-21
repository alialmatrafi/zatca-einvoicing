# Freelancers and sole establishments — how they fit in

There is **no separate legal category** for "freelancer" in ZATCA's e-invoicing rules — the obligation attaches to VAT registration status, not to business structure or size. A freelancer registered under Saudi Arabia's Freelance Business License (رخصة العمل الحر, obtained via Wathq/Maroof or the "Freelancers Portal") is a "taxable person" exactly like a registered company once they cross the VAT threshold or opt into voluntary registration.

## Practical decision logic to give the user

1. **Annual taxable revenue < SAR 187,500**: not required or eligible to register for VAT in the usual case → not subject to e-invoicing. (Edge cases in VAT eligibility exist; don't treat this as exhaustive tax advice.)
2. **SAR 187,500 – 375,000**: eligible for **voluntary** VAT registration. If they register voluntarily, they become subject to e-invoicing (Phase 1 immediately, Phase 2 once their wave arrives). If they don't register, they're out of scope for now — but should design their invoicing feature so it's not painful to add compliance later, since many freelancers cross this band as they grow.
3. **Above SAR 375,000**: **mandatory** VAT registration → mandatory e-invoicing, same as any company.

## If they're not VAT-registered, say so explicitly in the invoice design

This is easy to overlook: a freelancer under the threshold who isn't VAT-registered must **not** charge VAT, print a VAT registration number, or label the document a "tax invoice" — doing so is itself a compliance problem, separate from (and in a sense the mirror image of) the e-invoicing obligation. If you're designing an invoice template for a not-yet-registered freelancer, make the VAT/tax fields genuinely absent or zero rather than present-but-unused, and consider a plain label like "commercial invoice" or an explicit note that it's not VAT-subject, so nothing on the document could mislead a client into thinking they can reclaim input VAT on it.

## What this means for a product built for freelancers (e.g., an invoicing SaaS, marketplace payout tool, etc.)

- Don't assume all users are out of scope just because they're individuals rather than registered companies — ask for VAT registration status, not just "are you a freelancer."
- Don't assume all users are in scope either — plenty of freelancers stay under SAR 187,500 and have no VAT/e-invoicing obligation at all; forcing QR codes and cryptographic stamps on them is unnecessary complexity and cost.
- If the product serves a mix (some VAT-registered, some not), the invoicing feature needs a per-user compliance mode, not a single global switch — the simplest correct model is: capture VAT registration status and number per user, and only apply Phase 1 (and later Phase 2, once past their wave date) generation rules when that's set.
- If the user is building a platform where non-residents supply KSA customers, remember non-residents are exempt from the e-invoicing obligation for KSA-taxed supplies — don't force compliance flows onto suppliers who aren't KSA tax residents.
