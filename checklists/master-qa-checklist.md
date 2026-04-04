# Master QA Checklist — Diligent Account

**Maintained by:** RWS Group — India Revenue Team  
**Programme Manager:** Ashok Poojary  
**Source:** Consolidated from Danny Wang feedback — Jobs 038–064  
**Total Items:** 128  
**Last updated:** April 2026

---

## How to Use This Checklist

- Work through each section in order — sections follow the QA priority sequence
- Mark each item: ✅ Pass | ❌ Fail | ⚠️ Flag for review | N/A Not applicable
- Any ❌ on a Section 1 (Placeholder) item = delivery blocked until resolved
- Log all ❌ and ⚠️ items in the per-job checklist under `checklists/per-job/`

---

## Section 1 — Placeholder Integrity (Critical)

These checks must pass before any other review proceeds.

- [ ] 1.01 All `{variable_name}` placeholders present in target — none missing
- [ ] 1.02 All `{variable_name}` placeholders unaltered — casing matches source exactly
- [ ] 1.03 All `%s`, `%d` printf placeholders present and unaltered
- [ ] 1.04 Numbered printf placeholders (`%1$s`, `%2$d`) retain correct numbering
- [ ] 1.05 All `[[variable]]` double-bracket placeholders present and unaltered
- [ ] 1.06 No placeholder has been translated or paraphrased
- [ ] 1.07 No additional placeholder has been introduced that does not exist in source
- [ ] 1.08 HTML tag `<b>` preserved where present in source
- [ ] 1.09 HTML tag `<br/>` preserved where present in source
- [ ] 1.10 HTML tag `<a href="">` structure preserved — only visible text translated
- [ ] 1.11 No placeholder split across two segments in RTL files (AR, HE-IL)
- [ ] 1.12 Placeholder retains LTR directionality inside RTL strings (AR, HE-IL)
- [ ] 1.13 Placeholder position shift (due to target language grammar) verified for meaning
- [ ] 1.14 No space inserted inside placeholder brackets — `{ variable }` is incorrect
- [ ] 1.15 Placeholder capitalisation matches source — `{count}` not `{Count}`

---

## Section 2 — Untranslated Term Compliance (High)

- [ ] 2.01 "Diligent Boards" left in English across all languages
- [ ] 2.02 "Diligent Entities" left in English across all languages
- [ ] 2.03 "Diligent Messenger" left in English across all languages
- [ ] 2.04 "Diligent Directors" left in English across all languages
- [ ] 2.05 "BoardEffect" left in English across all languages
- [ ] 2.06 "Minutes AI" left in English across all languages
- [ ] 2.07 "Insights" left in English across all languages
- [ ] 2.08 "Voting" left in English across all languages
- [ ] 2.09 "Actions" left in English across all languages
- [ ] 2.10 "Annotations" left in English across all languages
- [ ] 2.11 "Admin" left in English across all languages
- [ ] 2.12 "Dashboard" left in English across all languages
- [ ] 2.13 "SSO" left in English across all languages
- [ ] 2.14 "API" left in English across all languages
- [ ] 2.15 "UDF" left in English across all languages
- [ ] 2.16 "CRO" left in English across all languages
- [ ] 2.17 "PSC" left in English across all languages
- [ ] 2.18 "ARD" left in English across all languages
- [ ] 2.19 "EF" left in English across all languages
- [ ] 2.20 Any new untranslated term candidate flagged for client confirmation before actioning

---

## Section 3 — Accuracy

- [ ] 3.01 Source meaning faithfully transferred — no omissions
- [ ] 3.02 Source meaning faithfully transferred — no additions not implied by source
- [ ] 3.03 No mistranslation of UI action verbs (Save, Delete, Cancel, Submit, Approve)
- [ ] 3.04 No mistranslation of role names (Owner, Member, Guest, Admin)
- [ ] 3.05 No mistranslation of status labels (Active, Inactive, Pending, Archived)
- [ ] 3.06 Conditional strings (if/then logic implied by source) translated with correct logic
- [ ] 3.07 Plural forms handled correctly per target language rules
- [ ] 3.08 Error messages retain the correct implied urgency — not softened or amplified
- [ ] 3.09 Tooltip text accurately reflects the function it describes
- [ ] 3.10 Help text accurately reflects the process it describes
- [ ] 3.11 Numbers, dates, and percentages in source reproduced correctly in target
- [ ] 3.12 No back-translation ambiguity — target string maps clearly back to source intent

---

## Section 4 — Terminology Consistency

- [ ] 4.01 Same approved term used for the same concept throughout the job
- [ ] 4.02 Glossary terms applied — no unapproved synonyms introduced
- [ ] 4.03 "Board" / "Vorstand" / equivalent used consistently per language glossary
- [ ] 4.04 "Meeting" / "Sitzung" / equivalent used consistently per language glossary
- [ ] 4.05 "Minutes" / "Protokoll" / equivalent used consistently per language glossary
- [ ] 4.06 "User" / "Benutzer" / equivalent used consistently — not mixed with informal variants
- [ ] 4.07 "Settings" / "Einstellungen" / equivalent consistent throughout
- [ ] 4.08 "Permissions" / "Berechtigungen" / equivalent consistent throughout
- [ ] 4.09 "Notification" equivalent consistent throughout
- [ ] 4.10 Any new term not in glossary flagged before a translation choice is locked
- [ ] 4.11 TM leverage strings verified — context match does not introduce stale terminology
- [ ] 4.12 Repeated strings translated identically across the job

---

## Section 5 — Typographic Conventions

### General
- [ ] 5.01 Correct quote marks used per language (not generic "English quotes" everywhere)
- [ ] 5.02 Ellipsis uses single character `…` not three dots `...` where required
- [ ] 5.03 No double spaces anywhere in the target string
- [ ] 5.04 No leading or trailing spaces in target string
- [ ] 5.05 Sentence-final punctuation present where source has it
- [ ] 5.06 Sentence-final punctuation absent where source omits it (UI labels often unpunctuated)

### German (DE)
- [ ] 5.07 Typographic quotes used: „text" not "text"
- [ ] 5.08 No space before colon, semicolon, or exclamation mark
- [ ] 5.09 Decimal separator is comma: `1,5` not `1.5`
- [ ] 5.10 Nouns capitalised correctly throughout

### French (FR)
- [ ] 5.11 Non-breaking space inserted before `:` `;` `!` `?`
- [ ] 5.12 Guillemets used: « text » not "text"
- [ ] 5.13 No space after opening guillemet or before closing guillemet (or consistent per style)

### Spanish (ES-419)
- [ ] 5.14 Inverted question mark `¿` at sentence start where required
- [ ] 5.15 Inverted exclamation mark `¡` at sentence start where required

### Italian (IT)
- [ ] 5.16 Apostrophe usage correct: dall', nell', sull' — not dall, nell, sull
- [ ] 5.17 No double apostrophe artifact from YAML processing

### Japanese (JA)
- [ ] 5.18 Full-width punctuation used: 。、「」— not half-width equivalents
- [ ] 5.19 No mixing of full-width and half-width punctuation in same string
- [ ] 5.20 No line break introduced within a segment unless source has one

### Chinese (ZH)
- [ ] 5.21 Full-width punctuation used: ，。！？
- [ ] 5.22 No space between Chinese characters and adjacent punctuation
- [ ] 5.23 Simplified characters only — no traditional characters present
- [ ] 5.24 Ellipsis rendered as `……` (double ellipsis) per ZH convention

### Arabic (AR)
- [ ] 5.25 String direction tags intact in file
- [ ] 5.26 Numeric formatting unaltered unless instructed

### Hebrew (HE-IL)
- [ ] 5.27 String direction tags intact in file
- [ ] 5.28 No nikkud (vowel marks) added unless present in source

---

## Section 6 — Fluency and Register

- [ ] 6.01 Formal register maintained throughout (Sie / vous / usted / Lei / u / você as applicable)
- [ ] 6.02 No register slip mid-string or mid-paragraph
- [ ] 6.03 Phrasing natural for UI context — not literal word-for-word translation
- [ ] 6.04 No awkward calques (direct structural copies from English that read unnaturally)
- [ ] 6.05 Action verbs in UI buttons sound natural as commands in target language
- [ ] 6.06 Error messages sound natural — not robotic or over-literal
- [ ] 6.07 Help text reads as native-language guidance — not translated instruction manual prose
- [ ] 6.08 No untranslated English words other than approved exceptions
- [ ] 6.09 No machine translation artefacts (unnatural word order, missing articles, wrong gender)
- [ ] 6.10 Gender agreement correct where applicable (DE, FR, ES, IT)
- [ ] 6.11 Number agreement correct — singular/plural forms applied appropriately
- [ ] 6.12 Loanwords in Japanese rendered in katakana — not hiragana or romaji

---

## Section 7 — File Integrity

- [ ] 7.01 File structure intact — no segments deleted or reordered
- [ ] 7.02 Segment count matches source file — no missing segments
- [ ] 7.03 String keys / IDs unaltered — only target text changed
- [ ] 7.04 No metadata or header content altered
- [ ] 7.05 YAML indentation preserved — no indentation errors introduced
- [ ] 7.06 JSON structure valid — no broken brackets, missing commas, or quote errors
- [ ] 7.07 `.strings` format intact — key = "value"; pattern preserved
- [ ] 7.08 `.resjson` format intact — JSON-compliant with comments preserved
- [ ] 7.09 No BOM (Byte Order Mark) issues introduced in UTF-8 files
- [ ] 7.10 File encoding matches source — UTF-8 throughout

---

## Section 8 — TM and Leverage Verification

- [ ] 8.01 Context Match (101%) segments verified — not assumed correct without review
- [ ] 8.02 Repetitions translated consistently with the first instance in the job
- [ ] 8.03 Fuzzy match segments (75–99%) reviewed for accuracy — not accepted blindly
- [ ] 8.04 TM leverage from previous jobs verified against current glossary version
- [ ] 8.05 Stale TM terminology flagged and updated where glossary has changed
- [ ] 8.06 MT segments reviewed for accuracy and fluency — not delivered as-is
- [ ] 8.07 New segments (0% match) confirmed as fully translated — no source text left in target

---

## Section 9 — Delivery Readiness

- [ ] 9.01 All Critical errors (Section 1) resolved before delivery
- [ ] 9.02 All High errors (Section 2) resolved or client-confirmed before delivery
- [ ] 9.03 Per-job QA log completed and saved under `checklists/per-job/`
- [ ] 9.04 Feedback summary prepared in Danny Wang format if errors were found
- [ ] 9.05 File naming convention confirmed — matches client delivery specification
- [ ] 9.06 Delivery package contains correct file set — no extra or missing files
- [ ] 9.07 PM sign-off completed before files leave RWS

---

## Per-Job Log Template

Copy this block into a new file under `checklists/per-job/` for each job.
