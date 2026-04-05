"""
batch_qa_runner.py
==================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Description:
    Batch QA runner. Processes all files across all languages
    in a single command. Runs three checks on every file pair:
    1. Placeholder integrity (placeholder_checker.py logic)
    2. Untranslated segment detection (untranslated_detector.py logic)
    3. Three-way string diff (diligent_string_diff.py logic)

    Designed for jobs with 3 files per language across 8 languages
    (24 file pairs total) — processed in one run with one consolidated report.

Expected folder structure:
    job-064/
    ├── source/
    │   ├── file1_en.json
    │   ├── file2_en.json
    │   └── file3_en.json
    ├── DE/
    │   ├── new/
    │   │   ├── file1_de.json
    │   │   ├── file2_de.json
    │   │   └── file3_de.json
    │   └── old/
    │       ├── file1_de.json
    │       ├── file2_de.json
    │       └── file3_de.json
    ├── FR/
    │   ├── new/
    │   └── old/
    └── (ZH, ES, IT, PT-BR, JA, NL ...)

Usage:
    python batch_qa_runner.py --job job-064
    python batch_qa_runner.py --job job-064 --langs DE FR ZH
    python batch_qa_runner.py --job job-064 --report report_job064.txt

Output:
    Terminal: colour-coded per file per language
    File:     consolidated report saved to --report path
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────
# ANSI colour codes
# ─────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─────────────────────────────────────────
# Supported languages
# ─────────────────────────────────────────
ALL_LANGUAGES = ["DE", "ES", "ES-419", "FR", "IT", "JA", "NL", "PT-BR", "ZH", "AR", "HE-IL"]


# ─────────────────────────────────────────
# Approved untranslated terms
# ─────────────────────────────────────────
APPROVED_UNTRANSLATED = {
    "Diligent Boards", "Diligent Entities", "Diligent Messenger",
    "Diligent Directors", "BoardEffect", "Minutes AI", "Insights",
    "Voting", "Actions", "Annotations", "Admin", "Dashboard",
    "SSO", "API", "UDF", "CRO", "PSC", "ARD", "EF", "SLA", "ID",
}

PLACEHOLDER_PATTERNS = {
    "curly_brace":    r"\{[a-zA-Z_][a-zA-Z0-9_]*\}",
    "printf_style":   r"%(?:\d+\$)?[sd]",
    "double_bracket": r"\[\[[a-zA-Z_][a-zA-Z0-9_]*\]\]",
    "html_tags":      r"<[^>]+>",
}

IGNORE_PATTERNS = [
    r"^\d+$",
    r"^[^\w]+$",
    r"^\w{1,2}$",
    r"^https?://",
    r"^[A-Z]{2,5}$",
]


# ─────────────────────────────────────────
# File parsers
# ─────────────────────────────────────────

def parse_yml(filepath):
    try:
        import yaml
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return flatten_dict(data)
    except ImportError:
        print(f"{RED}ERROR: PyYAML not installed. Run: pip install pyyaml{RESET}")
        sys.exit(1)


def parse_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return flatten_dict(data)


def parse_strings(filepath):
    result  = {}
    pattern = re.compile(r'^"(.+?)"\s*=\s*"(.+?)"\s*;', re.MULTILINE)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    for match in pattern.finditer(content):
        result[match.group(1)] = match.group(2)
    return result


def flatten_dict(d, parent_key="", sep="."):
    items = {}
    if not isinstance(d, dict):
        return items
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        elif isinstance(v, str):
            items[new_key] = v
    return items


def load_file(filepath):
    path = Path(filepath)
    ext  = path.suffix.lower()
    if ext in [".yml", ".yaml"]:
        return parse_yml(filepath)
    elif ext in [".json", ".resjson"]:
        return parse_json(filepath)
    elif ext == ".strings":
        return parse_strings(filepath)
    else:
        print(f"{RED}ERROR: Unsupported file type: {ext}{RESET}")
        return {}


# ─────────────────────────────────────────
# Check functions
# ─────────────────────────────────────────

def check_placeholders(source_strings, target_strings):
    """Check placeholder integrity between source and target."""
    errors = []
    for key in source_strings:
        if key not in target_strings:
            continue
        src = source_strings[key]
        tgt = target_strings[key]
        for name, pattern in PLACEHOLDER_PATTERNS.items():
            src_matches = sorted(re.findall(pattern, src))
            tgt_matches = sorted(re.findall(pattern, tgt))
            if src_matches != tgt_matches:
                errors.append({
                    "key":     key,
                    "type":    "PLACEHOLDER",
                    "source":  src,
                    "target":  tgt,
                    "missing": [p for p in src_matches if p not in tgt_matches],
                    "added":   [p for p in tgt_matches if p not in src_matches],
                })
    return errors


def check_untranslated(source_strings, target_strings):
    """Detect untranslated segments."""
    genuine = []
    approved = []
    for key in source_strings:
        if key not in target_strings:
            continue
        src = source_strings[key].strip()
        tgt = target_strings[key].strip()
        if src != tgt:
            continue
        # Check ignore patterns
        ignore = any(re.match(p, src) for p in IGNORE_PATTERNS)
        if ignore:
            continue
        # Check approved
        if src in APPROVED_UNTRANSLATED or src.lower() in {t.lower() for t in APPROVED_UNTRANSLATED}:
            approved.append({"key": key, "value": src})
        else:
            genuine.append({"key": key, "source": src, "target": tgt})
    return genuine, approved


def check_string_diff(source_strings, old_strings, new_strings):
    """Three-way diff between source, old target, and new target."""
    changes = []
    for key in source_strings:
        src_new = source_strings.get(key, "")
        tgt_old = old_strings.get(key)
        tgt_new = new_strings.get(key)
        if tgt_new is None or tgt_old is None:
            continue
        if tgt_old == tgt_new:
            continue
        changes.append({
            "key":     key,
            "source":  src_new,
            "old_tgt": tgt_old,
            "new_tgt": tgt_new,
        })
    return changes


# ─────────────────────────────────────────
# File pair matcher
# ─────────────────────────────────────────

def find_file_pairs(job_path, lang):
    """
    Find matching source, old target, new target file triplets
    for a given language folder.
    Returns list of (source_file, old_file, new_file, filename) tuples.
    """
    source_dir = job_path / "source"
    old_dir    = job_path / lang / "old"
    new_dir    = job_path / lang / "new"

    if not source_dir.exists():
        print(f"{RED}  ERROR: source/ folder not found in {job_path}{RESET}")
        return []
    if not new_dir.exists():
        print(f"{YELLOW}  WARNING: {lang}/new/ folder not found — skipping{RESET}")
        return []

    pairs = []
    source_files = list(source_dir.iterdir())

    for src_file in source_files:
        if src_file.suffix.lower() not in [".json", ".yml", ".yaml", ".resjson", ".strings"]:
            continue

        # Find matching target file by stem (without language suffix)
        stem = src_file.stem

        # Try exact name first, then strip language code suffix
        new_file = None
        for f in new_dir.iterdir():
            if f.suffix == src_file.suffix:
                if f.stem == stem or stem in f.stem or f.stem in stem:
                    new_file = f
                    break

        if new_file is None:
            # Try first file with same extension as fallback
            candidates = [f for f in new_dir.iterdir() if f.suffix == src_file.suffix]
            if len(candidates) == 1:
                new_file = candidates[0]

        if new_file is None:
            print(f"{YELLOW}  WARNING: No matching target file for {src_file.name} in {lang}/new/{RESET}")
            continue

        # Find old file
        old_file = None
        if old_dir.exists():
            for f in old_dir.iterdir():
                if f.suffix == src_file.suffix:
                    if f.stem == new_file.stem or new_file.stem in f.stem or f.stem in new_file.stem:
                        old_file = f
                        break

        pairs.append((src_file, old_file, new_file, new_file.name))

    return pairs


# ─────────────────────────────────────────
# Main batch runner
# ─────────────────────────────────────────

def run_batch(job_folder: str, langs: list, report_file: str = None) -> None:
    """
    Run full QA batch across all languages and files in the job folder.
    """
    job_path = Path(job_folder)
    if not job_path.exists():
        print(f"{RED}ERROR: Job folder not found: {job_folder}{RESET}")
        sys.exit(1)

    # Auto-detect languages if not specified
    if not langs:
        langs = [
            d.name for d in job_path.iterdir()
            if d.is_dir() and d.name.upper() in [l.upper() for l in ALL_LANGUAGES]
        ]
        if not langs:
            langs = [
                d.name for d in job_path.iterdir()
                if d.is_dir() and d.name not in ["source"]
            ]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    job_name  = job_path.name

    # Report storage
    report_lines = []
    grand_summary = {
        "files_processed":    0,
        "placeholder_errors": 0,
        "untranslated":       0,
        "string_changes":     0,
        "blocked_files":      [],
        "review_files":       [],
        "clean_files":        [],
        "all_changes":        [],
    }

    def log(line="", colour=""):
        print(f"{colour}{line}{RESET}" if colour else line)
        report_lines.append(re.sub(r'\033\[\d+m', '', line))

    log(f"\n{'━'*55}", BOLD+BLUE)
    log(f"  BATCH QA REPORT — {job_name}", BOLD)
    log(f"  RWS Group | India Revenue Team", BOLD)
    log(f"  Run date : {timestamp}", BOLD)
    log(f"  Languages: {', '.join(langs)}", BOLD)
    log(f"{'━'*55}\n", BOLD+BLUE)

    for lang in langs:
        lang_upper = lang.upper()
        log(f"\n  {'─'*45}")
        log(f"  LANGUAGE: {lang_upper}", BOLD+CYAN)
        log(f"  {'─'*45}")

        pairs = find_file_pairs(job_path, lang)

        if not pairs:
            log(f"  No file pairs found for {lang_upper} — skipping", YELLOW)
            continue

        for src_file, old_file, new_file, filename in pairs:
            grand_summary["files_processed"] += 1
            file_blocked = False
            file_changes = []

            log(f"\n  File: {filename}", BOLD)

            # Load files
            source_strings = load_file(str(src_file))
            new_strings    = load_file(str(new_file))
            old_strings    = load_file(str(old_file)) if old_file else {}

            # ── Check 1: Placeholders ──
            ph_errors = check_placeholders(source_strings, new_strings)
            if ph_errors:
                file_blocked = True
                grand_summary["placeholder_errors"] += len(ph_errors)
                log(f"  ❌ Placeholders : {len(ph_errors)} CRITICAL error(s)", RED)
                for err in ph_errors:
                    log(f"     [{err['key']}]", RED)
                    if err.get("missing"):
                        log(f"       Missing : {err['missing']}", RED)
                    if err.get("added"):
                        log(f"       Added   : {err['added']}", YELLOW)
            else:
                log(f"  ✅ Placeholders : PASS", GREEN)

            # ── Check 2: Untranslated ──
            genuine, approved = check_untranslated(source_strings, new_strings)
            if genuine:
                file_blocked = True
                grand_summary["untranslated"] += len(genuine)
                log(f"  ❌ Untranslated : {len(genuine)} segment(s) — BLOCKED", RED)
                for item in genuine:
                    log(f"     [{item['key']}] = \"{item['source']}\"", RED)
            else:
                if approved:
                    log(f"  ✅ Untranslated : PASS ({len(approved)} approved term(s))", GREEN)
                else:
                    log(f"  ✅ Untranslated : PASS", GREEN)

            # ── Check 3: String diff ──
            if old_strings:
                changes = check_string_diff(source_strings, old_strings, new_strings)
                if changes:
                    grand_summary["string_changes"] += len(changes)
                    log(f"  ⚠️  String diff  : {len(changes)} change(s) — review required", YELLOW)
                    for item in changes:
                        log(f"     [{item['key']}]", YELLOW)
                        log(f"       SRC : {item['source']}", "")
                        log(f"       OLD : {item['old_tgt']}", "")
                        log(f"       NEW : {item['new_tgt']}", YELLOW)
                        file_changes.append({**item, "lang": lang_upper, "file": filename})
                else:
                    log(f"  ✅ String diff  : No changes detected", GREEN)
            else:
                log(f"  ℹ️  String diff  : No previous file — skipping diff check", CYAN)

            # File status
            if file_blocked:
                grand_summary["blocked_files"].append(f"{lang_upper}/{filename}")
                log(f"  STATUS: BLOCKED — do not deliver", RED+BOLD)
            elif file_changes:
                grand_summary["review_files"].append(f"{lang_upper}/{filename}")
                grand_summary["all_changes"].extend(file_changes)
                log(f"  STATUS: REVIEW REQUIRED before delivery", YELLOW+BOLD)
            else:
                grand_summary["clean_files"].append(f"{lang_upper}/{filename}")
                log(f"  STATUS: CLEAN — ready for delivery", GREEN+BOLD)

    # ─────────────────────────────────────────
    # Grand summary
    # ─────────────────────────────────────────
    log(f"\n{'━'*55}", BOLD+BLUE)
    log(f"  GRAND SUMMARY — {job_name}", BOLD)
    log(f"{'━'*55}", BOLD+BLUE)
    log(f"  Files processed      : {grand_summary['files_processed']}")
    log(f"  Placeholder errors   : {grand_summary['placeholder_errors']}", RED if grand_summary['placeholder_errors'] else GREEN)
    log(f"  Untranslated segs    : {grand_summary['untranslated']}", RED if grand_summary['untranslated'] else GREEN)
    log(f"  String changes       : {grand_summary['string_changes']}", YELLOW if grand_summary['string_changes'] else GREEN)
    log(f"  Clean files          : {len(grand_summary['clean_files'])}", GREEN)
    log(f"  Review required      : {len(grand_summary['review_files'])}", YELLOW)
    log(f"  Blocked files        : {len(grand_summary['blocked_files'])}", RED if grand_summary['blocked_files'] else GREEN)

    if grand_summary["blocked_files"]:
        log(f"\n  BLOCKED — resolve before delivery:", RED+BOLD)
        for f in grand_summary["blocked_files"]:
            log(f"    ✗ {f}", RED)

    if grand_summary["review_files"]:
        log(f"\n  REVIEW REQUIRED — paste into Claude for verdict:", YELLOW+BOLD)
        for f in grand_summary["review_files"]:
            log(f"    ⚠ {f}", YELLOW)

    if grand_summary["all_changes"]:
        log(f"\n  CHANGED STRINGS FOR CLAUDE REVIEW ({len(grand_summary['all_changes'])} total):", YELLOW+BOLD)
        log(f"  Copy everything below and paste into Claude:\n", YELLOW)
        log(f"  {'─'*45}")
        for item in grand_summary["all_changes"]:
            log(f"  Lang: {item['lang']} | File: {item['file']}")
            log(f"  Key : {item['key']}")
            log(f"  SRC : {item['source']}")
            log(f"  OLD : {item['old_tgt']}")
            log(f"  NEW : {item['new_tgt']}")
            log(f"  {'─'*45}")

    overall = "BLOCKED" if grand_summary["blocked_files"] else \
              "REVIEW REQUIRED" if grand_summary["review_files"] else "CLEAN"
    colour  = RED if overall == "BLOCKED" else YELLOW if overall == "REVIEW REQUIRED" else GREEN
    log(f"\n  OVERALL STATUS : {overall}", colour+BOLD)
    log(f"{'━'*55}\n", BOLD+BLUE)

    # Save report
    if report_file:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"{GREEN}  Report saved to: {report_file}{RESET}\n")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diligent QA — Batch Runner | RWS Group"
    )
    parser.add_argument(
        "--job",
        required=True,
        help="Path to job folder (e.g. job-064)"
    )
    parser.add_argument(
        "--langs",
        nargs="*",
        default=[],
        help="Languages to process (e.g. DE FR ZH). Auto-detects if not specified."
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Optional: save report to a text file (e.g. report_job064.txt)"
    )
    args = parser.parse_args()

    run_batch(
        job_folder=args.job,
        langs=[l.upper() for l in args.langs] if args.langs else [],
        report_file=args.report,
    )


if __name__ == "__main__":
    main()
