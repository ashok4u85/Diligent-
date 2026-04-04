# Global QA Rules — Diligent Account

**Maintained by:** RWS Group — India Revenue Team  
**Last updated:** April 2026  
**Applies to:** All languages, all Diligent file types

---

## File Types in Scope

| Format | Product Area |
|--------|-------------|
| `.yml` / `.yaml` | Web application UI strings |
| `.json` | Frontend component strings |
| `.resjson` | Windows/UWP resource files |
| `.strings` | iOS mobile strings |

---

## Placeholder Rules — CRITICAL

All placeholders must be preserved exactly as they appear in the source.  
Do not translate, reorder, or alter casing unless explicitly instructed by the client.

| Format | Example | Rule |
|--------|---------|------|
| Curly brace | `{variable_name}` | Preserve exactly — most common in YML/JSON |
| Printf-style | `%s`, `%d`, `%1$s`, `%2$d` | Preserve numbering — e.g. `%1$s` cannot become `%s` |
| Double bracket | `[[variable]]` | Preserve as-is — legacy format |
| HTML inline | `<b>`, `<br/>`, `<a href="">` | Preserve tag structure; translate only visible text |

**Any placeholder mismatch = Critical error. Blocks delivery.**

---

## Intentionally Untranslated Terms

The following terms remain in English across all target languages per client agreement.  
Do not flag these as translation errors.

**Product Names**
- Diligent Boards
- Diligent Entities
- Diligent Messenger
- Diligent Directors
- BoardEffect

**Feature Names**
- Minutes AI
- Insights
- Voting
- Actions
- Annotations

**Technical Terms**
- Admin, Dashboard, SSO, API
- UDF, CRO, PSC, ARD, EF

If unsure whether a term is intentionally untranslated — flag for client confirmation. Do not auto-correct.

---

## QA Priority Order

Apply checks in this sequence on every review pass:

1. **Placeholder integrity** — Critical. Any missing, added, or altered placeholder blocks delivery.
2. **Untranslated term compliance** — High. Client-agreed English terms must remain in English.
3. **Accuracy** — Meaning faithfully transferred from source.
4. **Terminology consistency** — Same approved term used throughout the job.
5. **Typographic conventions** — Per language-specific rules (see `language-rules/` folder).
6. **Fluency** — Natural phrasing appropriate to UI context.

---

## Feedback Format (for Danny Wang)

All QA feedback delivered to the client must follow this format:

| Field | Requirement |
|-------|------------|
| Reference | Segment number or string key |
| Issue Type | Accuracy / Terminology / Placeholder / Typo / Style |
| Source | Original source string |
| Current Target | As delivered by linguist |
| Recommended Fix | Corrected target string |
| Comment | Neutral — no blame attribution to linguist |

---

## Recurring Error Patterns (Jobs 038–064)

These issues have appeared repeatedly across Diligent jobs and must be actively checked:

- Missing non-breaking space before French punctuation `: ; !`
- Japanese loanwords rendered in hiragana instead of katakana
- PT-BR strings containing European Portuguese idioms
- Placeholder capitalisation mismatch — `{Count}` instead of `{count}`
- German formal register (Sie) slipping to informal (du) in longer segments
- Mixed simplified and traditional Chinese characters in the same job
- Placeholder segment split in Arabic and Hebrew RTL files

---

## RTL Language Special Rules (AR, HE-IL)

- Verify string direction tags are intact in the file
- Placeholders must remain left-to-right even inside RTL strings
