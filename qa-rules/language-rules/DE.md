# German (DE) — Language-Specific QA Rules

**Account:** Diligent Corporation  
**Language:** German (DE)  
**Region:** Germany  
**Register:** Formal (Sie)  
**Last updated:** April 2026

---

## Register

- Always use **Sie** (formal) — never **du** (informal)
- This applies to all UI strings, tooltips, error messages, and button labels
- Watch for register slip in longer paragraph-style strings — linguists occasionally
  drift to du mid-paragraph
- If source English uses "you" ambiguously, default to Sie

---

## Compound Nouns

- German compounds must follow the established Diligent glossary
- Do not split compound nouns arbitrarily with spaces or hyphens unless the glossary confirms it
- Examples of correct compounds to verify:
  - Benutzereinstellungen (not Benutzer Einstellungen)
  - Vorstandssitzung (not Vorstand-Sitzung)
- When a new compound is not in the glossary — flag for client confirmation, do not invent

---

## UI Truncation Risk

- German strings consistently run 20–35% longer than English source
- Flag any string where the German translation may exceed visible UI space
- Pay particular attention to:
  - Button labels (short English = very short space)
  - Navigation menu items
  - Column headers in table views
  - Modal dialog titles
- Format your truncation flag as: `[TRUNCATION RISK] String key: {key_name}`

---

## Punctuation

- Use typographic quotes: „German quote" — not "English quotes"
- Ellipsis: use the single ellipsis character `…` not three dots `...`
- No space before colon, semicolon, or exclamation mark (unlike French)
- Decimal separator: comma `,` not period `.` — e.g. `1,5` not `1.5`
- Thousands separator: period `.` — e.g. `1.000` not `1,000`

---

## Capitalisation

- German nouns are always capitalised — verify this is applied consistently
- Watch for nouns incorrectly written in lowercase in translated strings
- Adjectives derived from proper nouns: lowercase — e.g. `diligente Lösung` not `Diligente Lösung`
- Product names and feature names follow the intentionally untranslated list — do not capitalise
  differently based on German grammar rules

---

## Placeholders in German Context

- Placeholder position may shift due to German sentence structure (verb-final)
- Verify the translated string still makes grammatical sense with the placeholder in its position
- Example issue: `{username} hat die Datei gelöscht` — placeholder must stay at sentence start
  if that is where it appears in source
- Flag any case where placeholder reordering changes meaning

---

## Date and Number Formats

- Date format: `TT.MM.JJJJ` (e.g. `04.04.2026`)
- Time format: 24-hour clock — `14:30` not `2:30 PM`
- Currency: if EUR appears, format as `1.234,56 €` (period thousands, comma decimal, symbol after)

---

## Glossary — Key Diligent Terms (DE)

| English | German (approved) | Notes |
|---------|------------------|-------|
| Board | Vorstand / Board | Use Board when referring to Diligent Boards product |
| Meeting | Sitzung | Preferred over Besprechung for board context |
| Minutes | Protokoll | Not Minuten |
| Voting | Abstimmung | Feature name Voting stays in English |
| Actions | Maßnahmen | Feature name Actions stays in English |
| Dashboard | Dashboard | Intentionally untranslated |
| Admin | Admin | Intentionally untranslated |
| User | Benutzer | Not Nutzer |
| Settings | Einstellungen | |
| Permissions | Berechtigungen | |
| Notification | Benachrichtigung | |

---

## Common Errors Logged (Diligent Job History)

- Register slip from Sie to du in longer help text strings
- Compound noun split incorrectly — e.g. `Benutzer Einstellungen` instead of `Benutzereinstellungen`
- English-style quotes used instead of „German quotes"
- Truncation not flagged on button labels
- Placeholder reordered without grammatical verification

---

*Global rules always apply in addition to these language-specific rules.*  
*Refer to `qa-rules/global-rules.md` for placeholder, untranslated terms, and feedback format standards.*
