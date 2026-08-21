# zatca-einvoicing — a Claude Skill for Saudi ZATCA e-invoicing compliance

*[بالعربي ⬇️](#النسخة-العربية) — النسخة العربية بالأسفل.*

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

---

## النسخة العربية

### وش هذا؟

**zatca-einvoicing** هو [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills) — ملف تعليمات يعطي Claude (سواء بـ Claude Code، Cowork، أو claude.ai) معرفة عملية بمنظومة الفوترة الإلكترونية السعودية التابعة لهيئة الزكاة والضريبة والجمارك (زاتكا / فاتورة)، عشان يقدر يساعد المطورين يبنون أو يراجعون أي فيتشر فوترة أو فواتير أو نقاط بيع (POS) أو ERP بشكل صحيح — سواء كانت منشأة مسجّلة، مؤسسة فردية، أو فريلانسر (عمل حر) داخل السعودية.

الترتيب اللي يتبعه: *هل هذا النشاط أصلاً يخضع للنظام؟* ← *أي نوع فاتورة ينطبق؟* ← *وش تتطلبه المرحلة الأولى / الثانية فعليًا؟* ← *وش أكثر الأخطاء الشائعة؟* — مدعوم بملفات مرجعية لكل موضوع من مواضيع زاتكا، وسكربت جاهز وشغّال لتوليد رمز QR (TLV) اللي تحتاجه كل فاتورة مبسّطة.

### محتويات المجلد

```
zatca-einvoicing/
├── SKILL.md                              # الملف الرئيسي اللي يقرأه Claude أول شي
├── references/
│   ├── phase1-generation.md              # متطلبات المرحلة الأولى (سارية من 4 ديسمبر 2021)
│   ├── phase2-integration.md             # متطلبات المرحلة الثانية (موجات): XML/UBL، CSID، الفرق بين الاعتماد والإبلاغ
│   ├── invoice-fields.md                 # قائمة الحقول الإلزامية لكل نوع فاتورة
│   ├── waves-thresholds.md               # جدول موجات المرحلة الثانية وكيف تتأكد إنه محدّث
│   ├── penalties.md                      # جدول المخالفات والغرامات
│   ├── freelancer-applicability.md       # علاقة ترخيص العمل الحر بالتسجيل الضريبي ونطاق الفوترة الإلكترونية
│   └── sources.md                        # مصادر زاتكا الرسمية للتحقق من أي معلومة حساسة بالوقت
└── scripts/
    └── zatca_qr_tlv.py                   # يبني QR بصيغة Base64 TLV (5 حقول للمرحلة الأولى، 9 للمرحلة الثانية)
```

ملف `zatca-einvoicing.skill` (بقسم [Releases](../../releases) بهذا المستودع، أو مبني محليًا حسب التعليمات تحت) هو نفس المحتوى بس مضغوط كملف تنصيب مباشر.

### طريقة التنصيب

**Claude Code / Cowork:** حط مجلد `zatca-einvoicing/` داخل مجلد الـ skills حق بيئتك (أو نصّب ملف `.skill` مباشرة لو بيئتك تدعم التنصيب بضغطة وحدة)، وبعدها بس تكلم عن زاتكا، فاتورة، الفوترة الإلكترونية بالسعودية، أو أي فيتشر فوترة/POS/ERP لمنشأة أو فريلانسر بالسعودية — الـ Skill يشتغل تلقائيًا حسب السياق، ما تحتاج تسميه صراحة.

**claude.ai:** ارفع `SKILL.md` (مع مجلدي `references/` و`scripts/`) كـ custom skill، إذا مساحة عملك تدعم هالخاصية.

### ⚠️ هذا مو استشارة قانونية أو ضريبية

هذا الـ Skill يلخّص القواعد *المنشورة* من زاتكا بصيغة توجيه هندسي للمطورين. الأنظمة، نسب الضريبة، مواعيد الموجات، وقيم الغرامات تتغيّر مع الوقت — وبعض الأرقام هنا (خصوصًا جدول موجات المرحلة الثانية وقيم الغرامات) مصدرها مواقع متابعة امتثال خارجية (third-party) مو صفحة تعرفة رسمية واحدة من زاتكا — راجع `references/sources.md` لمعرفة أي معلومة رسمية مؤكدة وأيها من مصدر ثانوي. تأكد دايمًا من المتطلبات الحالية عبر [zatca.gov.sa](https://zatca.gov.sa) أو بوابة فاتورة، وخلّي مستشار ضريبي مرخّص أو مزوّد حل فوترة إلكترونية معتمد من زاتكا يراجع الحل قبل الإطلاق الفعلي، خصوصًا لتدفقات الاعتماد (Clearance) بالمرحلة الثانية.

### المصادر اللي بُني عليها هذا الـ Skill

- [زاتكا — الأنظمة واللوائح](https://zatca.gov.sa/ar/RulesRegulations/Pages/rules.aspx)
- [زاتكا — اتفاقية مستوى الخدمة](https://zatca.gov.sa/ar/AboutUs/Pages/ZATCA-SLA.aspx)
- [زاتكا — ميثاق المتعاملين](https://zatca.gov.sa/ar/AboutUs/Pages/Customer-Charter.aspx)
- [زاتكا — سياسة إخلاء المسؤولية](https://zatca.gov.sa/ar/Pages/Disclaimer-Policy.aspx)
- [زاتكا — سياسة أمن المعلومات](https://zatca.gov.sa/ar/AboutUs/Pages/Information-Security-Policy.aspx)
- [زاتكا — الفوترة الإلكترونية](https://zatca.gov.sa/ar/E-Invoicing/Pages/default.aspx)
- [زاتكا — الدليل الإرشادي التفصيلي للفوترة الإلكترونية (PDF)](https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-Invoicing_Detailed__Guideline.pdf)
- [زاتكا — الدليل الفني التفصيلي للفوترة الإلكترونية (PDF)](https://zatca.gov.sa/en/E-Invoicing/Introduction/Guidelines/Documents/E-invoicing-Detailed-Technical-Guideline.pdf)

### المساهمة

التصحيحات مرحّب فيها بالذات لملفي `references/waves-thresholds.md` و`references/penalties.md` — هذولا أكثر ملفين متوقع يصير فيهم انحراف عن وضع زاتكا الحالي مع الوقت. إذا لقيت رقم قديم أو غير دقيق، افتح Pull Request مع رابط للمصدر الرسمي الحالي.

### الرخصة

MIT — راجع ملف [LICENSE](LICENSE). استخدام وتعديل وإعادة توزيع حر بالكامل؛ بدون أي ضمان، وراجع التنويه أعلاه.
