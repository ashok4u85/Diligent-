# Diligent QA Workflow — Team Operating Procedure

**Account:** Diligent Corporation
**Team:** Ashok Poojary, Krish, Suraj
**Last updated:** April 2026

---

## Overview

This document is the step-by-step operating procedure for running QA
on every Diligent delivery. Follow it in order for every job.
Do not skip steps.

```
Step 1 — Download from FTP
Step 2 — Set up local job folder
Step 3 — Run placeholder check
Step 4 — Run untranslated detector
Step 5 — Run batch QA (all languages, all files)
Step 6 — Paste changed strings to Claude
Step 7 — Save per-job log to GitHub
Step 8 — Deliver to Diligent
```

---

## Before You Start

Make sure you have these installed on your machine:

```
Python 3.10+        → python --version
Git                 → git --version
PyYAML              → pip install pyyaml
Requests            → pip install requests
```

Your local clone of this repo must be up to date:

```
cd "C:\Users\apoojary\Downloads\archive (1)\DTX\_Cursor\Diligent-"
git pull origin main
```

---

## Step 1 — Download From Danny's FTP

Danny uploads job files to the RWS FTP at:

```
Home → _TO_RWS → _2026 → Source for translation → [Program_name + Date]
```

Examples:
- `D1P_UI_20260211`
- `BE_active_UI_20260310`

Download the full zipped folder to your local machine and extract it.

Inside you will find:

```
[Program_name + Date]/
├── _Latest version/
│   └── To Translate/         ← NEW source files (files to translate)
├── _Previous version/
│   └── To Translate/         ← OLD source files (previous version)
└── _Previous version/
    └── Translated/
        ├── DE/               ← OLD target files per language
        ├── FR/
        ├── ZH/
        └── (all languages)
```

---

## Step 2 — Set Up Local Job Folder

Create a new job folder inside your local `Diligent-` repo clone under a
`jobs/` folder. Use the job name and date as the folder name.

Example for job `D1P_UI_20260211`:

```
Diligent-/
└── jobs/
    └── D1P_UI_20260211/
        ├── source/           ← copy files from _Latest version/To Translate/
        ├── source_old/       ← copy files from _Previous version/To Translate/
        ├── DE/
        │   ├── new/          ← new translated files (from tech team post-processing)
        │   └── old/          ← copy files from _Previous version/Translated/DE/
        ├── FR/
        │   ├── new/
        │   └── old/
        ├── ZH/
        │   ├── new/
        │   └── old/
        └── (ES, IT, PT-BR, JA, NL, AR, HE-IL as applicable)
```

### Important Rules

- `source/` = new English source from Danny — files to be translated
- `source_old/` = previous English source — used for delta comparison
- `[LANG]/new/` = translated files received from tech team after post-processing
- `[LANG]/old/` = previous translated files from Danny's FTP

**Do not rename the files themselves** — keep Danny's original filenames
so the script can match source to target automatically.

---

## Step 3 — Run Placeholder Check (Single File Test)

Before running the full batch, test one file pair first to confirm
the setup is correct.

```
cd "C:\Users\apoojary\Downloads\archive (1)\DTX\_Cursor\Diligent-"

python scripts/placeholder_checker.py \
  --source jobs/D1P_UI_20260211/source/issues_en.json \
  --target jobs/D1P_UI_20260211/DE/new/issues_de.json \
  --lang DE
```

**What to look for:**

| Output | Meaning | Action |
|--------|---------|--------|
| ✅ PASS | No placeholder errors | Continue to Step 4 |
| ❌ CRITICAL | Placeholder missing or altered | Stop — send back to tech team |

**If blocked:** Do not proceed. Email the tech team with the specific
key and placeholder error. Do not deliver until resolved.

---

## Step 4 — Run Untranslated Detector (Single File Test)

```
python scripts/untranslated_detector.py \
  --source jobs/D1P_UI_20260211/source/issues_en.json \
  --target jobs/D1P_UI_20260211/DE/new/issues_de.json \
  --lang DE
```

**What to look for:**

| Output | Meaning | Action |
|--------|---------|--------|
| ✅ PASS | No untranslated segments | Continue to Step 5 |
| ℹ APPROVED | Known untranslated terms | Expected — not an error |
| ❌ BLOCKED | Source text left untranslated | Stop — send back to linguist |

**If blocked:** Note the string key and send to the linguist for
translation. This is the pattern behind the Diligent "Comment"
string escalation — catch it here before it reaches Danny Wang.

---

## Step 5 — Run Full Batch QA (All Languages, All Files)

This is the main command. It processes every language folder and
every file in one run.

```
python scripts/batch_qa_runner.py --job jobs/D1P_UI_20260211
```

To save the report to a file at the same time:

```
python scripts/batch_qa_runner.py \
  --job jobs/D1P_UI_20260211 \
  --report jobs/D1P_UI_20260211/qa_report.txt
```

To run specific languages only:

```
python scripts/batch_qa_runner.py \
  --job jobs/D1P_UI_20260211 \
  --langs DE FR ZH IT
```

### Reading the Batch Output

| Status | Colour | Meaning | Action |
|--------|--------|---------|--------|
| CLEAN | Green | No issues found | Ready for delivery |
| REVIEW REQUIRED | Yellow | Linguist made changes | Paste to Claude — Step 6 |
| BLOCKED | Red | Critical errors found | Stop — fix before delivery |

### At the End of the Report

The batch runner prints a ready-to-paste block of all changed strings:

```
CHANGED STRINGS FOR CLAUDE REVIEW (47 total):
Copy everything below and paste into Claude:
─────────────────────────────────────────────
Lang: DE | File: issues_de.json
Key : issues.status.inProgress
SRC : In progress
OLD : 進行中
NEW : 処理中
─────────────────────────────────────────────
```

Copy this entire block — you will use it in Step 6.

---

## Step 6 — Paste Changed Strings to Claude for Verdict

Open Claude at claude.ai and paste the changed strings block.

Tell Claude:

```
These are changed strings from Diligent job [job name].
Please review each one and tell me:
- ACCEPT if the new translation is better or equivalent
- REVERT if the old translation was correct
- FLAG if you are not sure and it needs linguist confirmation
Apply our Diligent account rules for each language.
```

Claude will return a verdict for every changed string:

```
[001] Lang: DE | Key: issues.status.inProgress
      Source : In progress
      Old    : 進行中
      New    : 処理中
      Verdict: REVERT — 進行中 is the approved Diligent glossary term
      Reason : 処理中 means "processing" — wrong context for UI status

[002] Lang: ZH | Key: issues.severity.critical
      Source : Critical
      Old    : 关键
      New    : 严重
      Verdict: ACCEPT — 严重 is more accurate for severity level
      Reason : 关键 means "key/important" — 严重 correctly conveys severity
```

### Acting on Verdicts

| Verdict | Action |
|---------|--------|
| ACCEPT | Keep new translation — no change needed |
| REVERT | Restore old translation in the file |
| FLAG | Send to linguist with specific query |

---

## Step 7 — Save Per-Job Log to GitHub

After QA is complete, save a job log under `checklists/per-job/`.

Create a new file named: `job-[name]-[lang].md`

Example: `checklists/per-job/D1P_20260211_ALL.md`

Copy this template and fill it in:

```
# QA Log — D1P_UI_20260211

Job        : D1P_UI_20260211
Product    : D1P
Languages  : DE, FR, ZH, IT, ES, PT-BR, JA, NL
Reviewer   : [Your name]
Review date: [Date]
Files      : [Number of files per language]

## Results

| Language | Placeholders | Untranslated | String Changes | Status |
|----------|-------------|--------------|----------------|--------|
| DE       | PASS        | PASS         | 3 reviewed     | CLEAN  |
| FR       | PASS        | PASS         | 5 reviewed     | CLEAN  |
| ZH       | PASS        | 1 fixed      | 7 reviewed     | CLEAN  |
| IT       | PASS        | PASS         | 2 reviewed     | CLEAN  |

## Issues Found

[List all items that were reverted or flagged with key and reason]

## Sign-off

PM sign-off   : Ashok Poojary
Delivered to  : Danny Wang
Delivery date : [Date]
```

Push to GitHub:

```
git add checklists/per-job/D1P_20260211_ALL.md
git commit -m "QA log D1P_UI_20260211 all languages"
git push
```

---

## Step 8 — Deliver to Diligent

Once all checks pass and all REVERT items are corrected:

1. Confirm no BLOCKED files remain
2. Confirm all REVERT verdicts have been applied to the target files
3. Confirm all FLAG items have been resolved by the linguist
4. Deliver files to Danny Wang on FTP

---

## Quick Reference — Script Commands

| Script | Purpose | Command |
|--------|---------|---------|
| `placeholder_checker.py` | Single file — placeholder check | `python scripts/placeholder_checker.py --source [src] --target [tgt] --lang [XX]` |
| `untranslated_detector.py` | Single file — untranslated check | `python scripts/untranslated_detector.py --source [src] --target [tgt] --lang [XX]` |
| `diligent_string_diff.py` | Single file — three-way diff | `python scripts/diligent_string_diff.py --source [src] --old [old] --new [new] --lang [XX]` |
| `batch_qa_runner.py` | All files — full batch QA | `python scripts/batch_qa_runner.py --job [job-folder]` |

---

## Escalation Rules

| Situation | Who to contact | What to say |
|-----------|---------------|-------------|
| Placeholder error | Tech team | Share key, source string, and specific placeholder missing |
| Untranslated segment | Linguist | Share key and source string — request translation |
| FLAG verdict from Claude | Linguist | Share source, old translation, new translation — request confirmation |
| Client escalation from Danny | Ashok | Share QA log and Claude verdicts as evidence |

---

## Notes for Krish and Suraj

- Always run the batch QA **before** delivery — never skip
- If in doubt about a Claude verdict — escalate to Ashok
- Keep the per-job log updated — this is our audit trail with the client
- If Danny flags an issue after delivery — check the QA log first
  to see if it was reviewed and what verdict was given
- Any new recurring error pattern should be reported to Ashok
  so it can be added to the language rule files in `qa-rules/`

---

*This workflow is maintained by Ashok Poojary, RWS Group India Revenue Team.*
*Raise any process questions or updates via the GitHub Issues tab on this repo.*
