# Hebrew (HE-IL) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Hebrew (HE-IL)
**Region:** Israel
**Script direction:** Right-to-left (RTL)
**Last updated:** April 2026

---

## RTL File Integrity — CRITICAL

- Verify string direction tags (dir="rtl") are intact in every file
- Do not alter or remove directionality attributes
- Flag any string where direction tags appear missing or corrupted
- Same RTL caution applies as Arabic — treat with equal priority

---

## Placeholders in RTL Context — CRITICAL

- Placeholders must retain **left-to-right** directionality inside RTL strings
- Do not split a placeholder across two segments
- Use Unicode directional markers if needed: LRM `‎` around placeholders
- Verify placeholder renders correctly in RTL environment before sign-off
- Flag any placeholder that appears visually displaced in RTL context

---

## Nikkud (Vowel Marks)

- Do not add nikkud (niqqud / vowel pointing marks) unless they are present in the source
- Modern Hebrew UI text does not use nikkud — adding them is an error
- If source has nikkud, preserve them exactly

---

## Register

- Modern Hebrew — formal register
- Gender agreement is grammatically required in Hebrew — verify throughout
  - Male vs female forms of verbs and adjectives must match the implied subject
  - UI strings often default to masculine — flag if gender-neutral option exists

---

## Punctuation

- Hebrew uses standard Western punctuation in most digital contexts
- Quotation marks: ״text״ (Hebrew geresh) or "text" — verify per client style
- Period, comma, exclamation, question mark: standard Western characters acceptable

---

## Date and Number Formats

- Date format: `DD/MM/YYYY` — Western format standard for Diligent
- Numbers: Western Arabic numerals (0–9) — standard for Israeli tech UI
- Currency: ₪ symbol (if applicable)

---

## Glossary — Key Diligent Terms (HE-IL)

| English | Hebrew (approved) |
|---------|------------------|
| Board | דירקטוריון |
| Meeting | ישיבה |
| Minutes | פרוטוקול |
| User | משתמש |
| Settings | הגדרות |
| Permissions | הרשאות |
| Notification | התראה |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- String direction tags missing or removed
- Placeholder split across segments in RTL file
- Nikkud added where source has none
- Gender agreement errors — masculine form applied where feminine required
- Western punctuation replaced with incorrect Hebrew variants

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
