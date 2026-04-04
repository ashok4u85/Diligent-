# Diligent Localisation QA Repository

**Maintained by:** RWS Group — India Revenue Team  
**Account:** Diligent Corporation  
**Scope:** UI Localisation Quality Assurance across 10 languages  
**Programme Manager:** Ashok Poojary

---

## Overview

This repository contains QA scripts, rules, checklists, and reference materials used by the RWS delivery team to manage localisation quality for Diligent Corporation's software products — including **Diligent Boards**, **BoardEffect (BE)**, and related platform modules.

All QA processes documented here are specific to Diligent's file formats, glossary conventions, placeholder standards, and language requirements. The repository supports both human QA review and automated script-based checks.

---

## Supported Languages

| Code | Language | Region |
|------|----------|--------|
| DE | German | Germany |
| ES-419 | Spanish | Latin America |
| FR | French | France |
| IT | Italian | Italy |
| JA | Japanese | Japan |
| NL | Dutch | Netherlands |
| PT-BR | Portuguese | Brazil |
| ZH | Chinese | Simplified |
| AR | Arabic | Middle East |
| HE-IL | Hebrew | Israel |

---

## Repository Structure

```
Diligent-/
│
├── README.md                        ← This file
│
├── qa-rules/
│   ├── global-rules.md              ← Placeholder formats, untranslated terms, file type rules
│   └── language-rules/
│       ├── DE.md
│       ├── ES-419.md
│       ├── FR.md
│       ├── IT.md
│       ├── JA.md
│       ├── NL.md
│       ├── PT-BR.md
│       ├── ZH.md
│       ├── AR.md
│       └── HE-IL.md
│
├── scripts/
│   ├── diligent_string_diff.py      ← String diff tool (replaces Beyond Compare manual review)
│   ├── placeholder_checker.py       ← Validates placeholder integrity across all formats
│   └── untranslated_detector.py     ← Flags untranslated segments against approved exceptions
│
├── checklists/
│   ├── master-qa-checklist.md       ← 128-item consolidated QA checklist (from client feedback)
│   └── per-job/                     ← Job-specific QA logs and sign-off records
│
├── samples/
│   └── anonymised/                  ← Sanitised file samples used to test scripts
│
└── .cursor/
    └── rules                        ← Cursor AI context rules for this repository
```

---

## File Formats in Scope

| Format | Product Area |
|--------|-------------|
| `.yml` / `.yaml` | Web application UI strings |
| `.json` | Frontend component strings |
| `.resjson` | Windows/UWP resource files |
| `.strings` | iOS mobile strings |

---

## Placeholder Standards

Diligent files use multiple placeholder formats. All must be preserved exactly — do not translate, reorder without justification, or alter casing.

| Format | Example | Notes |
|--------|---------|-------|
| Curly brace | `{variable_name}` | Most common in YML/JSON |
| Printf-style | `%s`, `%d`, `%1$s` | Preserve numbering |
| Double bracket | `[[variable]]` | Legacy format |
| HTML inline | `<b>`, `<br/>` | Preserve tag structure |

---

## Intentionally Untranslated Terms

The following terms remain in English across all target languages per client agreement:

**Product Names:** Diligent Boards, Diligent Entities, Diligent Messenger, Diligent Directors, BoardEffect  
**Feature Names:** Minutes AI, Insights, Voting, Actions, Annotations  
**Technical Terms:** Admin, Dashboard, SSO, API, UDF, CRO, PSC, ARD, EF

Do not flag these as errors during QA review.

---

## Recurring QA Patterns (from Client Feedback History)

These issues have been logged across Jobs 038–064 and are actively monitored:

- Missing non-breaking space before French punctuation (`: ; !`)
- Japanese loanwords rendered in hiragana instead of katakana
- PT-BR strings containing European Portuguese idioms
- Placeholder capitalisation mismatch (`{Count}` instead of `{count}`)
- German formal register (Sie) slipping to informal (du) in longer segments
- Mixed simplified and traditional Chinese characters in the same job
- Placeholder segment split in Arabic/Hebrew RTL files

---

## QA Priority Order

When conducting a review pass, apply checks in this sequence:

1. **Placeholder integrity** — Critical; any error blocks delivery
2. **Untranslated term compliance** — High; client-agreed exceptions must be respected
3. **Accuracy** — Meaning faithfully transferred from source
4. **Terminology consistency** — Same approved term used throughout
5. **Typographic conventions** — Per language-specific rules
6. **Fluency** — Natural phrasing appropriate to UI context

---

## Scripts — Quick Reference

### `diligent_string_diff.py`
Compares source and target string files to surface missing, added, or structurally altered segments. Designed to replace manual Beyond Compare reviews for large file sets.

```bash
python scripts/diligent_string_diff.py --source en.yml --target de.yml
```

### `placeholder_checker.py`
Validates that all placeholders in source strings are present and unaltered in target strings.

```bash
python scripts/placeholder_checker.py --file de.yml --lang DE
```

### `untranslated_detector.py`
Identifies segments where the target string appears to be identical to the source, and cross-references against the approved untranslated terms list to separate false positives from genuine misses.

```bash
python scripts/untranslated_detector.py --file ja.yml --lang JA
```

---

## Contacts

| Role | Name |
|------|------|
| Programme Manager (RWS) | Ashok Poojary |
| Delivery Lead (RWS) | Radhakrishnan Kumar |
| Client QA Contact (Diligent) | Danny Wang |

---

## Versioning

Job-level QA logs are stored under `checklists/per-job/` and named using the convention `job-[number]-[product]-[lang].md`.

Example: `job-064-BE-ZH.md`

---

*This repository is maintained by RWS Group for internal QA process management on the Diligent account. File samples are anonymised before upload. No client-confidential content is committed to this repository.*
