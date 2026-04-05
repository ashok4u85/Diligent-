# Dutch (NL) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Dutch (NL)
**Region:** Netherlands
**Register:** Formal (u)
**Last updated:** April 2026

---

## Register

- Always use **u** (formal) — never **jij** or **je** (informal)
- Applies to all UI strings, tooltips, error messages, and button labels

---

## Compound Words

- Dutch uses compound nouns extensively — verify spacing and hyphenation
- Do not add spaces inside compounds that should be written as one word
- Examples:

| Incorrect | Correct |
|-----------|---------|
| gebruiker instellingen | gebruikersinstellingen |
| systeem beheer | systeembeheer |
| toegangs rechten | toegangsrechten |

- When a new compound is not in the glossary — flag for client confirmation

---

## Punctuation

- Quotation marks: „tekst" or 'tekst' — verify per Diligent style guide
- Ellipsis: single character `…` not three dots `...`
- No space before colon or semicolon

---

## Date and Number Formats

- Date format: `DD-MM-JJJJ` (e.g. `04-04-2026`)
- Decimal separator: comma — `1,5` not `1.5`
- Thousands separator: period — `1.000` not `1,000`

---

## Glossary — Key Diligent Terms (NL)

| English | Dutch (approved) |
|---------|-----------------|
| Board | Raad van bestuur / Board |
| Meeting | Vergadering |
| Minutes | Notulen |
| User | Gebruiker |
| Settings | Instellingen |
| Permissions | Machtigingen |
| Notification | Melding |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- Compound nouns incorrectly split with spaces
- jij or je used instead of u
- Incorrect hyphenation of compounds

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
