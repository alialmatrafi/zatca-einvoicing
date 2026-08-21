# Mandatory invoice fields (Article 53(5) / Annex 2)

This is a working checklist, not a substitute for the full ZATCA Data Dictionary — for a field-by-field XML schema mapping, read the official "E-Invoicing Detailed Technical Guideline" PDF linked in `sources.md` before finalizing an XML generator.

## Every invoice (Tax and Simplified)

- Invoice type (Tax Invoice / Simplified Tax Invoice / Credit Note / Debit Note) and, in Phase 2, the correct Invoice Type Code
- Unique, sequential invoice reference number (never reused, gaps must be explainable — e.g. voided invoice still logged)
- Invoice issue date and time
- Seller (supplier) legal name
- Seller VAT registration number
- Seller address
- Line items: description, quantity, unit price, applicable VAT rate/category, line total
- VAT category and rate applied per line (standard 15%, zero-rated, exempt — confirm current standard rate with the user's tax advisor, rates are set by regulation and can change)
- Subtotal (excl. VAT), total VAT amount, grand total (incl. VAT)
- Currency (SAR unless otherwise justified, with exchange rate disclosure if foreign currency)

## Tax Invoice only (B2B/B2G)

- Buyer legal name
- Buyer address
- Buyer VAT registration number (mandatory — a Tax Invoice without the buyer's VAT number is actually a Simplified Tax Invoice by definition, not a defective Tax Invoice)

## Simplified Tax Invoice only (B2C)

- No buyer VAT details required in general
- **Exception**: private healthcare and private education supplied to Saudi nationals — buyer ID (e.g., national ID) must still be captured even though it's a Simplified invoice
- QR code (Base64 TLV) — see `scripts/zatca_qr_tlv.py`

## Credit / Debit Notes

- Must reference the original invoice(s) being adjusted (invoice number and, in Phase 2, the original invoice's hash/UUID reference)
- Follow the same invoice-type rules as the original invoice (a credit note against a Tax Invoice is itself a Tax Invoice type document, and vice versa)
- Reason for adjustment (per Article 54 grounds — return, pricing error, cancellation, etc.)

## Phase 2 additions (all invoice types)

- UUID (128-bit, distinct from the human-readable invoice number)
- Previous Invoice Hash
- Cryptographic Stamp
- (Simplified only) full 9-tag QR — see `phase2-integration.md`

## Anti-patterns that break compliance even when "the invoice looks right"

- Letting a user manually type the invoice number (breaks sequential-integrity checks)
- Allowing an admin UI to edit a submitted invoice's line items after issuance instead of forcing a credit/debit note
- Applying VAT category/rate as a free-text field instead of a constrained enum matching ZATCA's VAT category codes
- Generating the QR code from a template/screenshot instead of from the actual TLV-encoded invoice data (guarantees drift between what's displayed and what's encoded)
