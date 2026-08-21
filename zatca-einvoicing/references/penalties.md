# Violations and penalties

ZATCA generally applies a **progressive penalty structure**: a warning for a first-time minor violation, then escalating fines for repeat or more serious violations. Treat the specific SAR amounts below as the commonly-reported ranges (sourced from third-party compliance guides, not a single ZATCA tariff table found during research) — confirm current amounts with the user's tax advisor before using them in anything customer-facing like a risk memo, since fine schedules are exactly the kind of thing that gets revised.

| Violation | Reported range |
|---|---|
| Not issuing an e-invoice at all (e.g., handwritten/non-compliant document) | SAR 5,000 – 50,000, depending on severity/repetition |
| Missing QR code on a Simplified Tax Invoice | Progressive: SAR 1,000 → 5,000 → 10,000 → 40,000 across repeat violations |
| Deleting or modifying an invoice after issuance (instead of issuing a credit/debit note) | SAR 10,000 up to 50,000 — treated as a serious integrity violation |
| Missing buyer VAT number on a Tax Invoice (B2B) | Progressive, same warning → escalating structure as above |
| Failing to integrate by the assigned Phase 2 wave deadline | Up to SAR 50,000; each non-compliant invoice issued after the deadline can be treated as a separate violation |
| Not reporting a system malfunction / clearance-reporting outage to ZATCA | Progressive, warning → escalating structure |

## Why this matters for implementation decisions

- The "deleting/modifying after issuance" penalty is a strong argument for making invoice records genuinely immutable at the data layer (append-only, credit/debit notes for corrections) rather than relying on "we just don't expose an edit button in the UI" — direct DB access or a future engineer without this context can undo that.
- The per-invoice framing on integration failures ("each non-integrated invoice... may constitute a separate violation") means a Phase 2 outage that silently keeps issuing invoices without reporting/clearing them can compound quickly — surface outages loudly in ops monitoring, don't let them fail silently.
- There has periodically been a **penalty exemption / amnesty initiative** covering some past violations (tax return and principal-amount settlement, not covering deliberate evasion) — if the user asks about cleaning up historical non-compliance, tell them to check ZATCA's current initiative status rather than assuming one is active, since these have specific windows.
