"""
placeholder_checker.py
======================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Description:
    Validates placeholder integrity between source and target localisation files.
    Supports .yml, .yaml, .json, .resjson, and .strings formats.
    Any placeholder mismatch is treated as a Critical error — blocks delivery.

Usage:
    python placeholder_checker.py --source en.yml --target de.yml --lang DE
    python placeholder_checker.py --source en.json --target ja.json --lang JA
    python placeholder_checker.py --source en.strings --target fr.strings --lang FR

Placeholder formats checked:
    {variable_name}     — curly brace
    %s %d %1$s %2$d     — printf-style
    [[variable]]        — double bracket
    <b> <br/> <a href>  — HTML inline tags
"""

import re
import sys
import json
import argparse
from pathlib import Path


# ─────────────────────────────────────────
# ANSI colour codes for terminal output
# ─────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─────────────────────────────────────────
# Placeholder regex patterns
# ─────────────────────────────────────────
PLACEHOLDER_PATTERNS = {
    "curly_brace":    r"\{[a-zA-Z_][a-zA-Z0-9_]*\}",
    "printf_style":   r"%(?:\d+\$)?[sd]",
    "double_bracket": r"\[\[[a-zA-Z_][a-zA-Z0-9_]*\]\]",
    "html_tags":      r"<[^>]+>",
}


def extract_placeholders(text: str) -> dict:
    """
    Extract all placeholders from a string.
    Returns a dict of {pattern_name: [list of matches]}.
    """
    results = {}
    for name, pattern in PLACEHOLDER_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            results[name] = matches
    return results


def compare_placeholders(source_text: str, target_text: str) -> list:
    """
    Compare placeholders between source and target strings.
    Returns a list of error dicts if mismatches are found.
    """
    errors = []
    source_ph = extract_placeholders(source_text)
    target_ph = extract_placeholders(target_text)

    all_types = set(list(source_ph.keys()) + list(target_ph.keys()))

    for ph_type in all_types:
        src_list = sorted(source_ph.get(ph_type, []))
        tgt_list = sorted(target_ph.get(ph_type, []))

        if src_list != tgt_list:
            errors.append({
                "type":     ph_type,
                "source":   src_list,
                "target":   tgt_list,
                "missing":  [p for p in src_list if p not in tgt_list],
                "added":    [p for p in tgt_list if p not in src_list],
            })

    return errors


# ─────────────────────────────────────────
# File parsers
# ─────────────────────────────────────────

def parse_yml(filepath: str) -> dict:
    """
    Parse a YAML file and return a flat dict of {key: value}.
    Handles simple key: value pairs only — nested keys joined with dot notation.
    """
    try:
        import yaml
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return flatten_dict(data)
    except ImportError:
        print(f"{RED}ERROR: PyYAML not installed. Run: pip install pyyaml{RESET}")
        sys.exit(1)


def parse_json(filepath: str) -> dict:
    """Parse a JSON or RESJSON file and return a flat dict of {key: value}."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return flatten_dict(data)


def parse_strings(filepath: str) -> dict:
    """
    Parse an iOS .strings file.
    Format: "key" = "value";
    """
    result = {}
    pattern = re.compile(r'^"(.+?)"\s*=\s*"(.+?)"\s*;', re.MULTILINE)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    for match in pattern.finditer(content):
        result[match.group(1)] = match.group(2)
    return result


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dict into dot-notation keys."""
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


def load_file(filepath: str) -> dict:
    """Load a file based on its extension and return a flat key-value dict."""
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
        print(f"Supported types: .yml .yaml .json .resjson .strings")
        sys.exit(1)


# ─────────────────────────────────────────
# Main checker
# ─────────────────────────────────────────

def run_check(source_file: str, target_file: str, lang: str) -> None:
    """
    Run full placeholder integrity check between source and target files.
    Prints results to terminal with colour-coded output.
    """
    print(f"\n{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  Diligent QA — Placeholder Checker{RESET}")
    print(f"{BOLD}  RWS Group | India Revenue Team{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    print(f"  Source : {source_file}")
    print(f"  Target : {target_file}")
    print(f"  Lang   : {lang}\n")

    # Load files
    print(f"  Loading files...")
    source_strings = load_file(source_file)
    target_strings = load_file(target_file)

    print(f"  Source keys : {len(source_strings)}")
    print(f"  Target keys : {len(target_strings)}\n")

    # Check for missing keys in target
    missing_keys = [k for k in source_strings if k not in target_strings]
    extra_keys   = [k for k in target_strings if k not in source_strings]

    if missing_keys:
        print(f"{YELLOW}  ⚠  WARNING — {len(missing_keys)} key(s) in source not found in target:{RESET}")
        for k in missing_keys:
            print(f"     - {k}")
        print()

    if extra_keys:
        print(f"{YELLOW}  ⚠  WARNING — {len(extra_keys)} key(s) in target not found in source:{RESET}")
        for k in extra_keys:
            print(f"     - {k}")
        print()

    # Run placeholder checks on matching keys
    critical_errors = []
    checked         = 0

    for key in source_strings:
        if key not in target_strings:
            continue

        src_text = source_strings[key]
        tgt_text = target_strings[key]
        errors   = compare_placeholders(src_text, tgt_text)
        checked += 1

        if errors:
            critical_errors.append({
                "key":    key,
                "source": src_text,
                "target": tgt_text,
                "errors": errors,
            })

    # ─────────────────────────────────────────
    # Results output
    # ─────────────────────────────────────────

    print(f"  Strings checked : {checked}")
    print(f"  Critical errors : {len(critical_errors)}\n")

    if not critical_errors:
        print(f"{GREEN}  ✅  PASS — No placeholder errors found.{RESET}")
        print(f"{GREEN}  This file is clear for delivery (placeholder check only).{RESET}\n")
        return

    # Print each critical error
    print(f"{RED}{BOLD}  ❌  CRITICAL ERRORS FOUND — DELIVERY BLOCKED{RESET}\n")
    print(f"{RED}  Resolve all items below before releasing files to client.{RESET}\n")

    for i, item in enumerate(critical_errors, start=1):
        print(f"{RED}  [{i:03d}] CRITICAL — Placeholder Mismatch{RESET}")
        print(f"        Key    : {item['key']}")
        print(f"        Source : {item['source']}")
        print(f"        Target : {item['target']}")

        for err in item["errors"]:
            print(f"        Type   : {err['type']}")
            if err["missing"]:
                print(f"        {RED}Missing in target : {err['missing']}{RESET}")
            if err["added"]:
                print(f"        {YELLOW}Added in target   : {err['added']}{RESET}")
        print()

    # Summary
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"  Language          : {lang}")
    print(f"  Strings checked   : {checked}")
    print(f"  Critical errors   : {RED}{len(critical_errors)}{RESET}")
    print(f"  Missing keys      : {YELLOW}{len(missing_keys)}{RESET}")
    print(f"  Status            : {RED}{BOLD}BLOCKED — DO NOT DELIVER{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diligent QA — Placeholder Checker | RWS Group"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to source file (e.g. en.yml)"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path to target file (e.g. de.yml)"
    )
    parser.add_argument(
        "--lang",
        required=True,
        help="Target language code (e.g. DE, JA, FR)"
    )

    args = parser.parse_args()

    run_check(
        source_file=args.source,
        target_file=args.target,
        lang=args.lang.upper(),
    )


if __name__ == "__main__":
    main()
