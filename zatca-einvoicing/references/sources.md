# Authoritative sources — re-verify time-sensitive details here

Anything involving a date, threshold, fine amount, or wave number in this skill can change. These are the sources to check before relying on a number in production-facing work:

- ZATCA e-invoicing hub: https://zatca.gov.sa/ar/E-Invoicing/Pages/default.aspx (and the English mirror under `/en/E-Invoicing/`)
- ZATCA Rules & Regulations index: https://zatca.gov.sa/ar/RulesRegulations/Pages/rules.aspx
- ZATCA Service Level Agreement (registration/processing timelines): https://zatca.gov.sa/ar/AboutUs/Pages/ZATCA-SLA.aspx
- ZATCA Customer Charter: https://zatca.gov.sa/ar/AboutUs/Pages/Customer-Charter.aspx
- ZATCA Disclaimer Policy: https://zatca.gov.sa/ar/Pages/Disclaimer-Policy.aspx
- ZATCA Information Security Policy: https://zatca.gov.sa/ar/AboutUs/Pages/Information-Security-Policy.aspx
- **E-Invoicing Detailed Guideline (PDF, primary technical/legal reference used to build this skill)**: https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf
- **E-Invoicing Detailed Technical Guideline (PDF, XML/UBL schema and field-level detail)**: https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-invoicing-Detailed-Technical-Guideline.pdf
- FATOORA portal (CSID onboarding, wave notifications, sandbox): accessible via the ZATCA e-invoicing hub above

## What this skill did NOT get from an official ZATCA source

The current wave table (`waves-thresholds.md`) and the penalty amounts (`penalties.md`) were sourced from third-party compliance-industry write-ups (e.g., Wafeq, Origami, Jaicome — all e-invoicing solution vendors who track ZATCA announcements closely) because ZATCA's own pages returned as general policy/navigation pages rather than the live wave table during this skill's research. Flag this explicitly to users who need precise, current numbers — point them to the FATOORA portal or their ZATCA account, which shows their actual assigned wave and deadline.
