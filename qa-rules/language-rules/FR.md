# French (FR) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** French (FR)
**Region:** France
**Register:** Formal (vous)
**Last updated:** April 2026

---

## Register

- Always use **vous** (formal) — never **tu** (informal)
- Applies to all UI strings, tooltips, error messages, and button labels
- Watch for register slip in longer paragraph strings

---

## Punctuation — CRITICAL FOR FRENCH

French typography requires a non-breaking space before certain punctuation marks.
This is a recurring error in Diligent jobs and must be actively checked.

| Punctuation | Rule |
|-------------|------|
| Colon `:` | Non-breaking space before — `texte :` |
| Semicolon `;` | Non-breaking space before — `texte ;` |
| Exclamation `!` | Non-breaking space before — `texte !` |
| Question `?` | Non-breaking space before — `texte ?` |

**Flag any string where these spaces are missing.**

---

## Quotation Marks

- Use guillemets: **« text »**
- Not English-style double quotes: ~~"text"~~
- Space inside guillemets is acceptable per French convention

---

## Date and Number Formats

- Date format: `JJ/MM/AAAA` (e.g. `04/04/2026`)
- Time format: 24-hour — `14h30` or `14:30`
- Decimal separator: comma — `1,5` not `1.5`
- Thousands separator: non-breaking space — `1 000` not `1,000`

---

## Glossary — Key Diligent Terms (FR)

| English | French (approved) |
|---------|------------------|
| Board | Conseil d'administration / Board |
| Meeting | Réunion |
| Minutes | Procès-verbal |
| User | Utilisateur |
| Settings | Paramètres |
| Permissions | Autorisations |
| Notification | Notification |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- Missing non-breaking space before `:` `;` `!` `?`
- English quotes used instead of guillemets « »
- tu used instead of vous in shorter UI strings
- European number formatting instead of French convention

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
