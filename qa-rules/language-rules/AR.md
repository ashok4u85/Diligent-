# Arabic (AR) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Arabic (AR)
**Region:** Middle East
**Script direction:** Right-to-left (RTL)
**Last updated:** April 2026

---

## RTL File Integrity — CRITICAL

- Verify string direction tags (dir="rtl") are intact in every file
- Do not alter or remove directionality attributes
- Flag any string where direction tags appear missing or corrupted

---

## Placeholders in RTL Context — CRITICAL

This is a known high-risk area for Arabic files:

- Placeholders must retain **left-to-right** directionality inside RTL strings
- Do not split a placeholder across two segments — this breaks rendering
- Use Unicode directional markers if needed: LRM `‎` around placeholders
- Test: verify the placeholder renders correctly in an RTL environment before sign-off
- Flag any placeholder that appears visually displaced in RTL context

---

## Numeric Formatting

- Do not alter numeric formatting unless explicitly instructed by client
- Western Arabic numerals (0–9) are standard for Diligent UI
- Eastern Arabic numerals (٠١٢٣٤٥٦٧٨٩) — use only if client specifies

---

## Register

- Modern Standard Arabic (MSA) — not dialect
- Formal register throughout
- Do not use colloquial dialect terms from any specific Arabic-speaking region

---

## Punctuation

- Arabic period: ـ or . — verify per client style
- Arabic comma: ، (U+060C) — not standard comma ,
- Arabic question mark: ؟ (U+061F) — not standard ?
- Quotation marks: «نص» — guillemets acceptable

---

## Date and Number Formats

- Date format: `DD/MM/YYYY` — Western format is standard for Diligent
- Time format: verify 12-hour vs 24-hour per client instruction

---

## Glossary — Key Diligent Terms (AR)

| English | Arabic (approved) |
|---------|------------------|
| Board | مجلس الإدارة |
| Meeting | اجتماع |
| Minutes | محضر الاجتماع |
| User | مستخدم |
| Settings | الإعدادات |
| Permissions | الأذونات |
| Notification | إشعار |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- String direction tags missing or removed
- Placeholder split across segments in RTL file
- Placeholder rendered out of position in RTL context
- Dialect terms used instead of MSA
- Arabic comma ، replaced with standard comma ,

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
