# zatca-einvoicing — a Claude Skill for Saudi ZATCA e-invoicing compliance

A [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills) that gives Claude (Claude Code, Cowork, claude.ai) working knowledge of Saudi Arabia's ZATCA e-invoicing system (Fatoora / الفوترة الإلكترونية), so it can help developers build or review any invoicing, billing, POS, ERP, or freelance-invoicing feature correctly — for a registered company, a sole establishment, or a freelancer (فريلانسر / عمل حر) operating inside KSA.

It answers, in order: *is this business even in scope?* → *which invoice type applies?* → *what does Phase 1 / Phase 2 actually require?* → *what are the common ways to get it wrong?* — backed by reference files for each ZATCA topic area and a working script for the QR/TLV code every Simplified Tax Invoice needs.

## What's in the box

```
zatca-einvoicing/
├── SKILL.md                              # entry point Claude reads first
├── references/
│   ├── phase1-generation.md              # Phase 1 (effective 4 Dec 2021) requirements
│   ├── phase2-integration.md             # Phase 2 (rolling waves) requirements: XML/UBL, CSID, clearance vs reporting
│   ├── invoice-fields.md                 # mandatory field checklist per invoice type
│   ├── waves-thresholds.md               # Phase 2 wave/threshold schedule + how to keep it current
│   ├── penalties.md                      # violation → fine reference
│   ├── freelancer-applicability.md       # how freelance licensing interacts with VAT/e-invoicing scope
│   └── sources.md                        # authoritative ZATCA sources to re-verify anything time-sensitive
└── scripts/
    └── zatca_qr_tlv.py                   # builds the Base64 TLV QR payload (Phase 1: 5 tags, Phase 2: 9 tags)
```

`zatca-einvoicing.skill` (in this repo's [Releases](../../releases), or built locally per below) is the same content packaged as an installable `.skill` archive.

## Install

**Claude Code / Cowork:** drop the `zatca-einvoicing/` folder into your skills directory (or install the packaged `.skill` file if your setup supports one-click skill install), then just talk about ZATCA, Fatoora, e-invoicing in Saudi Arabia, or building a billing/POS/invoicing feature for a KSA-based business or freelancer — the skill triggers on context, you don't need to name it explicitly.

**claude.ai:** upload `SKILL.md` (and the `references/` and `scripts/` folders) as a custom skill, if your workspace supports it.

## ⚠️ Not legal or tax advice

This skill distills ZATCA's *published* rules into engineering guidance. Regulations, VAT rates, wave deadlines, and fine amounts change over time, and some figures here (notably the Phase 2 wave table and penalty amounts) were sourced from third-party compliance trackers rather than a single official ZATCA tariff page — see `references/sources.md` for exactly what's official vs. secondary. Always confirm current requirements on [zatca.gov.sa](https://zatca.gov.sa) / the FATOORA portal, and have a licensed tax advisor or ZATCA-accredited e-invoicing solution provider sign off before going live, especially for Phase 2 clearance integration.

## Sources this skill was built from

- [ZATCA — Rules & Regulations](https://zatca.gov.sa/ar/RulesRegulations/Pages/rules.aspx)
- [ZATCA — Service Level Agreement](https://zatca.gov.sa/ar/AboutUs/Pages/ZATCA-SLA.aspx)
- [ZATCA — Customer Charter](https://zatca.gov.sa/ar/AboutUs/Pages/Customer-Charter.aspx)
- [ZATCA — Disclaimer Policy](https://zatca.gov.sa/ar/Pages/Disclaimer-Policy.aspx)
- [ZATCA — Information Security Policy](https://zatca.gov.sa/ar/AboutUs/Pages/Information-Security-Policy.aspx)
- [ZATCA — E-Invoicing](https://zatca.gov.sa/ar/E-Invoicing/Pages/default.aspx)
- [ZATCA — E-Invoicing Detailed Guideline (PDF)](https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf)
- [ZATCA — E-Invoicing Detailed Technical Guideline (PDF)](https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-invoicing-Detailed-Technical-Guideline.pdf)

## Contributing

Corrections are especially welcome for `references/waves-thresholds.md` and `references/penalties.md` — those are the two files most likely to drift from ZATCA's current position. If you find a stale figure, open a PR with a link to the current official source.

## License

MIT — see [LICENSE](LICENSE). Use, fork, and redistribute freely; no warranty, and see the disclaimer above.
