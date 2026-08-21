# Phase 2 wave / threshold schedule

ZATCA rolls out Phase 2 integration in successive waves, ordered from taxpayers with the **highest** VAT-taxable annual revenue down to the lowest. Each taxpayer is notified individually by ZATCA at least 6 months before their wave's effective date, and waves keep being announced as thresholds decrease — **this table will go stale**. Treat it as "the shape of the rollout" for building applicability logic, not as a hardcoded deadline to ship against.

## Known waves as of this skill's last research pass (August 2026)

| Wave | Revenue threshold (annual VAT-taxable supplies) | Deadline |
|---|---|---|
| 23 | > SAR 750,000 | 31 March 2026 |
| 24 | > SAR 375,000 | 30 June 2026 |
| 25 | > SAR 187,500 | ~1 February 2027 (verify — reported but not yet fully confirmed at research time) |

Earlier waves (1–22) progressively brought in taxpayers from >SAR 3 billion down to >SAR 750,000; by wave 24 the rollout already reaches the SAR 375,000 mandatory-VAT-registration threshold, meaning essentially every mandatorily VAT-registered business is now (mid-2026) in scope or about to be. Voluntarily-registered taxpayers (SAR 187,500–375,000) are being brought in around wave 25.

## How to use this in an application

Don't hardcode "if revenue > X, show Phase 2 features" with the numbers above baked in permanently. Instead:

1. Build the applicability check as a **configurable threshold + effective date**, sourced from a value the user can update (a config row, not a constant in code) — because ZATCA will keep adding waves below SAR 187,500 is unlikely (that's the voluntary registration floor) but wave deadlines and grouping can still shift.
2. Tell the user explicitly: *"Confirm your exact wave and deadline via the FATOORA portal notification or ZATCA's current wave announcement — don't rely on a hardcoded table in code, including this one."*
3. If the user doesn't know their revenue tier or wave, ask them rather than guessing — an incorrect assumption here changes the whole scope of what needs to be built (Phase 1 only vs. full Phase 2 integration).

## Source to re-check

ZATCA's e-invoicing page and periodic wave-announcement press releases are the authoritative source — see `sources.md`. Third-party compliance-software blogs (Wafeq, Origami, Jaicome, etc.) often track the wave table faster than ZATCA's own site updates, but treat them as secondary confirmation, not the source of truth.
