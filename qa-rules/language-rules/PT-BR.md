# Portuguese Brazil (PT-BR) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Portuguese (PT-BR)
**Region:** Brazil
**Register:** Formal (você)
**Last updated:** April 2026

---

## Register

- Always use **você** (formal Brazilian) — never **tu** unless source specifies
- Never use **vós** — this is archaic and not used in Brazilian Portuguese
- Applies to all UI strings, tooltips, error messages, and button labels

---

## Brazilian vs European Portuguese — CRITICAL

This is a recurring error in Diligent jobs. European Portuguese is not accepted.

Flag these European Portuguese patterns immediately:

| European PT (incorrect) | Brazilian PT (correct) |
|------------------------|----------------------|
| utilizador | usuário |
| computador portátil | notebook / laptop |
| telemóvel | celular |
| autocarro | ônibus |
| ecrã | tela |
| ficheiro | arquivo |
| janela (window) | janela ✅ (acceptable in both) |

---

## Punctuation

- Quotation marks: "texto" — standard double quotes acceptable in PT-BR
- Ellipsis: single character `…` not three dots `...`
- No space before colon or semicolon

---

## Date and Number Formats

- Date format: `DD/MM/AAAA` (e.g. `04/04/2026`)
- Decimal separator: comma — `1,5` not `1.5`
- Thousands separator: period — `1.000` not `1,000`
- Currency: R$ symbol before amount — `R$ 1.234,56`

---

## Glossary — Key Diligent Terms (PT-BR)

| English | Portuguese BR (approved) |
|---------|------------------------|
| Board | Conselho de administração / Board |
| Meeting | Reunião |
| Minutes | Ata |
| User | Usuário |
| Settings | Configurações |
| Permissions | Permissões |
| Notification | Notificação |
| Admin | Admin (untranslated) |
| Dashboard | Dashboard (untranslated) |

---

## Common Errors (Diligent Job History)

- European Portuguese terms used instead of Brazilian variants
- utilizador instead of usuário
- ecrã instead of tela
- tu used instead of você

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
