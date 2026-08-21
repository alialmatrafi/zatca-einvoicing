---
name: zatca-einvoicing
description: Guidance for making any invoicing, billing, POS, ERP, or freelance-invoicing feature compliant with Saudi Arabia's ZATCA e-invoicing system (Fatoora / الفوترة الإلكترونية). Covers Phase 1 (Generation) and Phase 2 (Integration/waves), Tax vs Simplified invoice rules, mandatory fields, QR/TLV codes, XML/UBL 2.1 structure, cryptographic stamps and CSID onboarding, VAT registration thresholds, and penalties. Determines whether a company, sole establishment, or freelancer (فريلانسر / عمل حر) operating inside Saudi Arabia is even in scope, and which phase/wave applies. Use this skill whenever the user mentions ZATCA, Fatoora, الفوترة الإلكترونية, VAT invoices in Saudi Arabia, e-invoicing compliance, or is building/reviewing a billing, checkout, POS, ERP, or invoicing feature for a business or freelancer based in KSA — even if they never say the word "compliance" or "ZATCA" explicitly, e.g. "I'm adding an invoice PDF to my Saudi SaaS app" or "how do I bill my Saudi clients as a freelancer."
---

# ZATCA E-Invoicing Compliance

## Why this exists

Saudi Arabia's Zakat, Tax and Customs Authority (ZATCA) legally requires every VAT-registered taxable person resident in KSA — companies, sole establishments, and freelancers operating under a commercial or freelance license alike — to issue invoices electronically through the Fatoora system. Non-compliance carries escalating fines (see `references/penalties.md`), and Phase 2 integration is being rolled out in waves that already cover most VAT-registered taxpayers as of mid-2026. Developers building or reviewing any feature that issues an invoice, receipt, or credit/debit note for a KSA-based business need to get this right the first time, because retrofitting cryptographic stamping and clearance flows after launch is expensive.

**This skill is engineering guidance distilled from ZATCA's published rules, not legal or tax advice.** Regulations, wave thresholds, and deadlines change — always confirm current requirements against the official sources in `references/sources.md` (especially the live wave schedule and the technical guideline PDFs) and recommend the user's tax advisor or a ZATCA-accredited e-invoicing solution provider sign off before go-live, particularly for Phase 2 clearance flows.

## Step 1 — Establish applicability before writing any code

Don't assume the user's business is in scope. Walk through this before recommending an implementation:

1. **Is the entity VAT-registered in KSA?** If not, and their annual taxable revenue is below SAR 375,000, they are **not currently subject to e-invoicing** — mandatory VAT registration kicks in at SAR 375,000/year, voluntary registration is allowed from SAR 187,500/year. A freelancer working under Saudi Arabia's "Freelance Business License" (رخصة العمل الحر) or Wathq/Maroof registration follows the exact same thresholds as any other taxable person — there is no freelancer-specific exemption once they cross the threshold or opt into voluntary registration.
2. **If VAT-registered:** they are already subject to **Phase 1 (Generation)** — this has applied to every VAT-registered taxpayer since 4 December 2021, no exceptions, no waves.
3. **Is the entity also in scope for Phase 2 (Integration)?** ZATCA notifies each taxpayer at least 6 months ahead of their integration wave. Waves are announced from the highest revenue down to the lowest — see `references/waves-thresholds.md` for the schedule and, critically, tell the user to verify their exact wave/deadline on the FATOORA portal or ZATCA's current wave announcement, since new waves are published periodically and thresholds keep dropping (by mid-2026 waves already reach businesses around SAR 375k–187.5k in annual revenue).
4. **Non-residents** issuing invoices for KSA-taxed supplies are explicitly exempt from the e-invoicing obligation.

Only once you know whether the user needs Phase 1 only, or Phase 1 + Phase 2, should you scope the implementation work.

## Step 2 — Know the two invoice types

Everything downstream (fields, QR rules, clearance vs. reporting) depends on knowing which invoice type applies:

- **Tax Invoice** — B2B/B2G, or any transaction where the buyer is also VAT-registered. Requires full buyer details (name, address, VAT number). In Phase 2, must be **cleared** by ZATCA in real time before it reaches the buyer.
- **Simplified Tax Invoice** — B2C, or B2B transactions under SAR 1,000. No buyer VAT details required (exception: private healthcare/education supplied to Saudi nationals must still capture buyer ID). Must carry a QR code. In Phase 2, the taxpayer's own system stamps it and it is **reported** to ZATCA within 24 hours (not pre-cleared).
- **Credit/Debit Notes** follow the type of the invoice they adjust and must reference the original invoice.

Read `references/invoice-fields.md` for the full mandatory field list (Article 53(5) / Annex 2) for each type — get this wrong and every invoice generated is non-compliant, not just the UI.

## Step 3 — Implement per phase

Read the relevant reference file in full before writing implementation code — don't guess at the technical details from memory, they are precise and audited.

- **Phase 1 only** → `references/phase1-generation.md`. Core requirements: generate invoices electronically (never scan/photocopy a paper original), any electronic format is fine (XML not yet mandatory), tamper-evident sequencing (locked invoice counter, protected timestamp, no silent deletion), and a QR code on every Simplified Tax Invoice.
- **Phase 1 + Phase 2** → also read `references/phase2-integration.md`. Core requirements: XML per the UBL 2.1-based ZATCA standard (or PDF/A-3 with embedded XML), a Cryptographic Stamp Identity (CSID) issued through onboarding on the FATOORA portal, a hash chain linking each invoice to the previous one, a UUID per invoice, real-time clearance for Tax Invoices, 24-hour reporting for Simplified Tax Invoices, and a 9-tag TLV QR code on every Simplified Tax Invoice (use `scripts/zatca_qr_tlv.py`, don't hand-roll the TLV/base64 encoding).

## Step 4 — QR code generation

For both phases, Simplified Tax Invoices need a Base64 TLV-encoded QR code. Phase 1 needs the basic 5 tags; Phase 2 extends this to 9 tags (adds hash, cryptographic stamp, and public key info). Use the bundled script rather than re-implementing TLV encoding by hand — it's a common source of clearance rejections:

```bash
python3 scripts/zatca_qr_tlv.py --help
```

See the script's docstring and `references/phase2-integration.md` for what each tag means and which are Phase 1 vs Phase 2 only.

## Step 5 — Security, archiving, and operational requirements

ZATCA's Information Security Policy expects e-invoicing solutions to treat taxpayer/buyer data and cryptographic material with ISO/IEC 27001-aligned controls and to follow National Cybersecurity Authority (NCA) baseline controls. In practice this means, at minimum: the CSID private key must never be exportable or logged; invoices must be archived per VAT record-retention rules with a traceable naming convention (VAT number + timestamp + reference); and any outage that prevents clearance/reporting must be logged and reported to ZATCA, with invoices cleared/reported retroactively once service is restored (Tax Invoices within 15 days of month-end, Simplified within 24 hours). Don't design a "silent failure" path where an invoice is issued to a customer but never makes it to ZATCA.

## Step 6 — Common pitfalls to flag for the user

- Treating e-invoicing as a "generate a PDF" problem — Phase 2 is fundamentally an integration/API problem (clearance and reporting calls, retries, CSID renewal).
- Missing the QR code on Simplified Tax Invoices, or encoding it as plain text instead of TLV/Base64.
- Allowing invoices to be edited or deleted after issuance instead of forcing a credit/debit note — this is one of the more heavily fined violations.
- Assuming a freelancer or small business is automatically exempt — check VAT registration status and revenue, not company size or "freelancer" status alone.
- Hardcoding a wave deadline into code or docs without a note to re-verify it — ZATCA has issued 24+ waves and keeps adding more as thresholds drop; see `references/waves-thresholds.md` for how to word this so it doesn't go stale.
- Forgetting non-resident suppliers are exempt, which can lead to over-building compliance flows for entities that don't need them.

For fine amounts by violation type, see `references/penalties.md` — useful when the user asks "what happens if we ship without this."

## Step 7 — Wrap up with a compliance summary, not just code

When you finish helping implement or review an invoicing feature, give the user a short compliance summary: which phase(s) apply to them, which invoice types they issue, what's implemented vs. still open (e.g., "CSID onboarding still needs to happen on the live FATOORA portal, that's a manual step outside code"), and a reminder to validate against ZATCA's sandbox/testing environment before going live. Don't present the implementation as fully certified — ZATCA compliance ultimately requires using an accredited/registered e-invoicing solution and passing their validation.

## Reference files

- `references/phase1-generation.md` — full Phase 1 technical + legal requirements
- `references/phase2-integration.md` — full Phase 2 technical requirements (XML/UBL, clearance, CSID, hash chain, QR TLV tags)
- `references/invoice-fields.md` — mandatory field checklist per invoice type
- `references/waves-thresholds.md` — Phase 2 wave/threshold schedule and how to keep it current
- `references/penalties.md` — violation → fine table
- `references/freelancer-applicability.md` — how KSA freelance licensing interacts with VAT/e-invoicing
- `references/sources.md` — authoritative ZATCA sources to re-verify anything time-sensitive
- `scripts/zatca_qr_tlv.py` — generates the Base64 TLV QR payload for Simplified Tax Invoices (Phase 1 and Phase 2 tag sets)
