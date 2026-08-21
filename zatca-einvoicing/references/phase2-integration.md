# Phase 2 — Integration (rolling out by waves since 1 January 2023)

Phase 2 adds a live integration between the taxpayer's e-invoicing solution and ZATCA's FATOORA platform. It only applies once the taxpayer's wave has been reached — check `waves-thresholds.md` and always have the user confirm their exact deadline on the FATOORA portal, since ZATCA notifies each taxpayer individually at least 6 months ahead of their wave.

## Format requirement

- Invoices must be produced as **XML** conforming to ZATCA's UBL 2.1-based e-invoicing XML Implementation Standard, **or** as **PDF/A-3 with the XML embedded** inside the PDF.
- The XML must pass ZATCA's structural and business-rule validations (arithmetic accuracy — line totals, VAT totals, and grand totals must reconcile; all mandatory fields present; sequential integrity of invoice counters and hashes).

## CSID onboarding (do this before writing invoice logic)

1. The taxpayer generates a **Cryptographic Stamp Identity (CSID)** through onboarding on the FATOORA portal. This is a manual/portal step, not something you build in application code — but your system needs to securely store and use the resulting credentials.
2. The CSID's private key **must never be exportable** from the signing environment and must never be logged, committed to source control, or transmitted outside the secure onboarding/renewal flow.
3. CSIDs are renewable — build renewal into ops runbooks, not as an afterthought; an expired CSID blocks every invoice from being cleared or reported.

### The onboarding sequence in more technical detail

**Verify this against the current official technical guideline PDF before implementing** — it was reconstructed from third-party integration write-ups during this skill's research, not confirmed line-by-line against ZATCA's primary spec the way the rest of this file was. The shape is very likely right; exact field names, endpoint paths, and the signing curve are worth double-checking.

1. **Generate a CSR** (Certificate Signing Request) that follows ZATCA's specific profile, not a generic CSR — it needs particular Subject/OtherName fields (common name, VAT number, taxpayer/branch name, an EGS — E-invoicing Generation Solution — unit serial number, industry, address/location, and which invoice type(s) the unit supports) and is commonly reported as using the ECDSA secp256k1 curve. A multi-branch or multi-device taxpayer needs a separate CSR (and therefore a separate CSID) per generation unit.
2. **Request a Compliance CSID** by submitting the CSR together with an OTP obtained from the FATOORA portal. This returns a compliance-stage certificate used only for testing.
3. **Pass the Compliance Check** by submitting sample invoices covering every type you'll issue (standard Tax Invoice, Simplified Tax Invoice, credit note, debit note) through ZATCA's compliance-check API. This is where structural/business-rule bugs in your XML generation, hashing, or signing get caught before production.
4. **Request a Production CSID (PCSID)** once compliance checks pass. This is the certificate actually used for live clearance/reporting, and it has a limited validity period — plan renewal as a recurring operational task, not a one-time setup step.
5. There are generally **three environments** to design around: a sandbox/developer environment for early development, a simulation environment that mirrors production for final testing, and production itself. Don't let a compliance-stage (sandbox/simulation) certificate end up used for live production traffic by accident — validate which environment a CSID belongs to before using it.

If you're building a multi-tenant SaaS (one system serving many taxpayers), each tenant needs its own isolated CSID and private key — never a shared signing key across tenants — and ideally keys live in an HSM or a secrets manager (e.g. cloud KMS/Vault) with per-tenant access boundaries, since a leaked key lets someone forge invoices under that taxpayer's identity.

## Cryptographic stamp

An electronic stamp created via cryptographic algorithms that proves authenticity of origin and integrity of content.

- **Tax Invoices**: the stamp is applied by **ZATCA** during the clearance step, not by the taxpayer's system.
- **Simplified Tax Invoices**: the stamp is applied by the **taxpayer's own solution**, using its CSID, before the invoice is shared with the buyer.

## Clearance vs. reporting — the key Phase 2 workflow difference

| | Tax Invoice (B2B/B2G) | Simplified Tax Invoice (B2C, or B2B < SAR 1,000) |
|---|---|---|
| Flow | **Clearance**: submit XML to ZATCA, wait for real-time approval + ZATCA-applied cryptographic stamp, *then* share with the buyer | **Reporting**: taxpayer stamps and issues the invoice to the buyer immediately, then reports it to ZATCA within **24 hours** |
| Who stamps it | ZATCA | The taxpayer's solution (via CSID) |
| Failure mode | Buyer never receives an invoice that hasn't cleared | Buyer already has the invoice; reporting failure is a backend problem to fix, not a customer-facing blocker |

Design your system so a clearance failure blocks nothing customer-facing for Simplified invoices, but *does* block invoice delivery for Tax Invoices until ZATCA responds — don't fake a "cleared" state client-side.

## Required technical fields beyond Phase 1

- **UUID** — a 128-bit unique identifier per invoice, separate from the human-readable sequential invoice number.
- **Previous Invoice Hash** — each invoice's XML includes a hash reference to the immediately preceding invoice, forming a hash chain that lets ZATCA detect gaps or reordering. The very first invoice in a sequence uses a defined seed/zero hash per ZATCA's spec. The hash is computed (commonly reported as SHA-256) over a **canonicalized** form of the XML — don't hash whatever byte-for-byte XML string your library happens to produce; use the standard's canonicalization rules (XML-C14N is the commonly referenced approach) so that harmless formatting differences (attribute order, whitespace) don't change the hash and break the chain.
- **Cryptographic Stamp** field, populated per the clearance/reporting flow above.

## QR code — 9-tag TLV (Phase 2)

Phase 2 extends the Phase 1 5-tag QR to 9 Base64 TLV-encoded tags for Simplified Tax Invoices:

1. Seller name
2. Seller VAT registration number
3. Invoice timestamp
4. Invoice total (with VAT)
5. VAT amount
6. Invoice XML hash
7. ECDSA cryptographic stamp
8. Seller's ECDSA public key
9. ECDSA signature of the public key stamp (certificate signature)

Use `scripts/zatca_qr_tlv.py` — it supports both the 5-tag (Phase 1) and 9-tag (Phase 2) modes. Don't hand-roll TLV/Base64 encoding; malformed tag length/value pairs are a common cause of clearance rejection and of ZATCA's mobile app failing to verify the QR.

**The single most common TLV bug: measuring length in characters instead of bytes.** The TLV length byte must be the value's length in UTF-8 *bytes*, not characters. This is easy to get right for English text and easy to get wrong for Arabic (or any non-ASCII) text, because most Arabic characters take 2 bytes in UTF-8 — if your code does `len(seller_name)` instead of `len(seller_name.encode("utf-8"))`, an Arabic seller name will silently produce a corrupted, unreadable QR. `scripts/zatca_qr_tlv.py` handles this correctly (it encodes to UTF-8 first, then measures length), but if you ever reimplement TLV encoding elsewhere in a codebase, flag this explicitly in code review — it's the kind of bug that passes every test written with English sample data and fails the moment a real Arabic business name goes through it.

**Physical/print requirements**, since this QR ends up on a real receipt: keep it at roughly 2×2 cm or larger with adequate quiet-zone margin around it, use a medium-or-higher error-correction level (so smudged thermal printing still scans), and generate it fresh from the actual invoice data at print time — never from a static template or screenshot, since any drift between what's printed and what's encoded is itself a compliance problem. If you're printing from a thermal POS printer, most send QR content via ESC/POS commands rather than rendering a bitmap — make sure the printer receives the exact Base64 TLV string as the QR *data*, not a pre-rendered image that could get re-encoded incorrectly.

## Outage / failure handling

- If ZATCA's platform is unavailable: the taxpayer may continue issuing invoices manually/uncleared temporarily, but must notify ZATCA via the dedicated incident form and retry clearance/reporting regularly.
- If the taxpayer's own device/solution fails: manual invoices are permitted during the outage; once restored, re-issue or back-report compliant invoices.
- **Extended outages**: Tax Invoices can be cleared retroactively within 15 days of the supply month's end; Simplified Tax Invoices must still be reported within 24 hours of restoration.
- Invoices that never get cleared/reported are not eligible for input VAT deduction on the buyer's side — this is a real financial consequence for the user's customers, worth surfacing explicitly.

## Advance payments and special cases

- Advance/prepayment invoices use Invoice Type Code `386` and the `PrepaidAmount` KSA extension fields.
- Private healthcare/education supplied to Saudi nationals: even though it's zero-rated, Simplified Tax Invoices for these must still capture buyer ID details — don't drop buyer capture just because the invoice type is "Simplified."
- Supplies "not subject to VAT" don't require an invoice at all under this system, and don't need to preserve counter/hash sequence continuity if issued from the same solution as VAT-subject invoices.
