"""
untranslated_detector.py
========================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Description:
    Detects untranslated segments in target localisation files by comparing
    source and target strings. Automatically cross-references the approved
    Diligent untranslated terms list to separate genuine misses from
    intentionally untranslated content.

    Directly addresses the "Comment" string escalation pattern where
    untranslated segments were delivered to client undetected.

Usage:
    python untranslated_detector.py --source en.yml --target de.yml --lang DE
    python untranslated_detector.py --source en.json --target zh.json --lang ZH
    python untranslated_detector.py --source en.strings --target fr.strings --lang FR

Supported formats:
    .yml / .yaml / .json / .resjson / .strings

Output:
    RED    = Genuine untranslated segment — must be translated before delivery
    YELLOW = Approved untranslated term — expected, not an error
    GREEN  = All clear — no untranslated segments found
"""

import re
import sys
import json
import argparse
from pathlib import Path


# ─────────────────────────────────────────
# ANSI colour codes
# ─────────────────────────────────────────
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─────────────────────────────────────────
# Diligent approved untranslated terms
# These are intentionally kept in English
# across all 10 target languages
# ─────────────────────────────────────────
APPROVED_UNTRANSLATED = {
    # Product names
    "Diligent Boards",
    "Diligent Entities",
    "Diligent Messenger",
    "Diligent Directors",
    "BoardEffect",
    # Feature names
    "Minutes AI",
    "Insights",
    "Voting",
    "Actions",
    "Annotations",
    # Technical terms
    "Admin",
    "Dashboard",
    "SSO",
    "API",
    "UDF",
    "CRO",
    "PSC",
    "ARD",
    "EF",
    "SLA",
    "ID",
}

# Short strings that are legitimately identical
# in source and target (single chars, symbols, codes)
IGNORE_PATTERNS = [
    r"^\d+$",           # pure numbers
    r"^[^\w]+$",        # pure punctuation/symbols
    r"^\w{1,2}$",       # single or double character codes
    r"^https?://",      # URLs
    r"^[A-Z]{2,5}$",    # acronyms like SLA, API, SSO
]


# ─────────────────────────────────────────
# File parsers
# ─────────────────────────────────────────

def parse_yml(filepath: str) -> dict:
    """Parse a YAML file into a flat key-value dict."""
    try:
        import yaml
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return flatten_dict(data)
    except ImportError:
        print(f"{RED}ERROR: PyYAML not installed. Run: pip install pyyaml{RESET}")
        sys.exit(1)


def parse_json(filepath: str) -> dict:
    """Parse a JSON or RESJSON file into a flat key-value dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return flatten_dict(data)


def parse_strings(filepath: str) -> dict:
    """Parse an iOS .strings file. Format: "key" = "value";"""
    result  = {}
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
    """Load a file based on its extension."""
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
        print(f"Supported: .yml .yaml .json .resjson .strings")
        sys.exit(1)


# ─────────────────────────────────────────
# Detection logic
# ─────────────────────────────────────────

def should_ignore(text: str) -> bool:
    """
    Returns True if the string is expected to be identical
    in source and target — e.g. numbers, symbols, short codes.
    """
    text = text.strip()
    for pattern in IGNORE_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def is_approved_untranslated(text: str) -> bool:
    """
    Returns True if the string is an approved Diligent
    untranslated term that should remain in English.
    """
    text_stripped = text.strip()
    # Exact match
    if text_stripped in APPROVED_UNTRANSLATED:
        return True
    # Contains an approved term as the full value
    for term in APPROVED_UNTRANSLATED:
        if text_stripped.lower() == term.lower():
            return True
    return False


def is_untranslated(source: str, target: str) -> bool:
    """
    Returns True if the target string appears to be
    identical to the source — indicating a missed translation.
    Strips whitespace and is case-sensitive.
    """
    return source.strip() == target.strip()


def classify_match(source: str, target: str) -> str:
    """
    Classify why source and target match.
    Returns: 'ignore' | 'approved' | 'untranslated'
    """
    if should_ignore(source):
        return "ignore"
    if is_approved_untranslated(source):
        return "approved"
    if is_untranslated(source, target):
        return "untranslated"
    return "ok"


# ─────────────────────────────────────────
# Main checker
# ─────────────────────────────────────────

def run_check(source_file: str, target_file: str, lang: str) -> None:
    """
    Run full untranslated segment detection between source and target.
    Prints colour-coded results to terminal.
    """
    print(f"\n{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  Diligent QA — Untranslated Detector{RESET}")
    print(f"{BOLD}  RWS Group | India Revenue Team{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    print(f"  Source : {source_file}")
    print(f"  Target : {target_file}")
    print(f"  Lang   : {lang}\n")

    # Load files
    source_strings = load_file(source_file)
    target_strings = load_file(target_file)

    print(f"  Source keys : {len(source_strings)}")
    print(f"  Target keys : {len(target_strings)}\n")

    # Check for missing keys
    missing_keys = [k for k in source_strings if k not in target_strings]
    if missing_keys:
        print(f"{YELLOW}  ⚠  WARNING — {len(missing_keys)} source key(s) missing from target:{RESET}")
        for k in missing_keys:
            print(f"     - {k}")
        print()

    # Run detection
    genuine_untranslated = []
    approved_matches     = []
    ignored              = []
    checked              = 0

    for key in source_strings:
        if key not in target_strings:
            continue

        src = source_strings[key]
        tgt = target_strings[key]
        checked += 1

        if not is_untranslated(src, tgt):
            continue

        classification = classify_match(src, tgt)

        if classification == "ignore":
            ignored.append({"key": key, "value": src})
        elif classification == "approved":
            approved_matches.append({"key": key, "value": src})
        elif classification == "untranslated":
            genuine_untranslated.append({
                "key":    key,
                "source": src,
                "target": tgt,
            })

    # ─────────────────────────────────────────
    # Results
    # ─────────────────────────────────────────

    print(f"  Strings checked          : {checked}")
    print(f"  Genuine untranslated     : {RED}{len(genuine_untranslated)}{RESET}")
    print(f"  Approved untranslated    : {YELLOW}{len(approved_matches)}{RESET}")
    print(f"  Ignored (symbols/codes)  : {len(ignored)}\n")

    # Approved terms — informational
    if approved_matches:
        print(f"{YELLOW}  ℹ  APPROVED UNTRANSLATED TERMS (expected — not errors):{RESET}")
        for item in approved_matches:
            print(f"     ✓ [{item['key']}] = \"{item['value']}\"")
        print()

    # Clean pass
    if not genuine_untranslated:
        print(f"{GREEN}  ✅  PASS — No untranslated segments found.{RESET}")
        print(f"{GREEN}  This file is clear for delivery (untranslated check only).{RESET}\n")
        return

    # Genuine errors
    print(f"{RED}{BOLD}  ❌  UNTRANSLATED SEGMENTS FOUND — DELIVERY BLOCKED{RESET}\n")
    print(f"{RED}  These segments must be translated before releasing to client.{RESET}\n")
    print(f"{RED}  Root cause of the Diligent 'Comment' string escalation —{RESET}")
    print(f"{RED}  do not deliver until all items below are resolved.{RESET}\n")

    for i, item in enumerate(genuine_untranslated, start=1):
        print(f"{RED}  [{i:03d}] UNTRANSLATED — Must Fix{RESET}")
        print(f"        Key    : {item['key']}")
        print(f"        Source : {item['source']}")
        print(f"        Target : {item['target']}  {RED}← identical to source{RESET}")
        print()

    # Summary
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"  Language                 : {lang}")
    print(f"  Strings checked          : {checked}")
    print(f"  Genuine untranslated     : {RED}{len(genuine_untranslated)}{RESET}")
    print(f"  Approved untranslated    : {YELLOW}{len(approved_matches)}{RESET}")
    print(f"  Missing keys             : {YELLOW}{len(missing_keys)}{RESET}")
    print(f"  Status                   : {RED}{BOLD}BLOCKED — DO NOT DELIVER{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diligent QA — Untranslated Segment Detector | RWS Group"
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
        help="Target language code (e.g. DE, JA, ZH, FR)"
    )

    args = parser.parse_args()

    run_check(
        source_file=args.source,
        target_file=args.target,
        lang=args.lang.upper(),
    )


if __name__ == "__main__":
    main()
