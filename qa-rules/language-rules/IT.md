# Italian (IT) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Italian (IT)
**Region:** Italy
**Register:** Formal (Lei)
**Last updated:** April 2026

---

## Register

- Always use **Lei** (formal third person) — never **tu** (informal)
- Lei takes third-person singular verb forms — verify verb agreement throughout
- Watch for register slip in longer help text strings

---

## Apostrophe Usage

Italian uses elision apostrophes extensively. Flag if missing:

| Incorrect | Correct |
|-----------|---------|
| dell | dell' |
| nell | nell' |
| sull | sull' |
| all | all' |
| dall | dall' |

---

## YAML Double Apostrophe Artifact

A known processing issue causes double apostrophes in YAML files:
- `dell''amministratore` instead of `dell'amministratore`
- Flag any double apostrophe as a file processing artifact — do not pass through to delivery

---

## Punctuation

- Quotation marks: «testo» or "testo" — both acceptable per Diligent style
- Ellipsis: single character `…` not three dots `...`
- No space before colon, semicolon, or exclamation mark

---

## Date and Number Formats

- Date format: `GG/MM/AAAA` (e.g. `04/04/2026`)
- Decimal separator: comma — `1,5` not `1.5`
- Thousands separator: period — `1.000` not `1,000`

---

## Glossary — Key Diligent Terms (IT)

| English | Italian (approved) |
|---------|-------------------|
| Board | Consiglio di amministrazione / Board |
| Meeting | Riunione |
| Minutes | Verbale |
| User | Utente |
| Settings | Impostazioni |
| Permissions | Autorizzazioni |
| Notification | Notifica |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- Missing apostrophe in elisions: dell, nell, sull
- Double apostrophe YAML artifact passed through to delivery
- tu used instead of Lei
- Gender agreement errors on adjectives

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
