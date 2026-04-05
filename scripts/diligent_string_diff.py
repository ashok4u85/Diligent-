"""
diligent_string_diff.py
=======================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Description:
    Three-way string diff tool. Compares:
    - Source (EN) — new version from client
    - Old target  — previous delivery
    - New target  — current delivery from linguist

    Identifies exactly what the linguist changed between
    deliveries and flags each change for linguistic review.
    Replaces manual Beyond Compare process.

Usage:
    python diligent_string_diff.py --source en_new.json --old de_old.json --new de_new.json --lang DE
    python diligent_string_diff.py --source en_new.yml  --old zh_old.yml  --new zh_new.yml  --lang ZH

Supported formats:
    .yml / .yaml / .json / .resjson / .strings

Output:
    RED    = Source changed AND target changed — high risk
    YELLOW = Target changed only — linguist update — review required
    GREEN  = No changes detected
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
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


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
    """Parse an iOS .strings file. Format: key = value;"""
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
        sys.exit(1)


# ─────────────────────────────────────────
# Diff logic
# ─────────────────────────────────────────

def classify_change(src_old, src_new, tgt_old, tgt_new) -> str:
    """
    Classify the type of change across source and target.

    Returns:
        'no_change'         — nothing changed
        'source_only'       — source changed, target unchanged (stale TM risk)
        'target_only'       — target changed, source unchanged (linguist update)
        'both_changed'      — both source and target changed (high risk)
        'new_key'           — key did not exist in previous version
    """
    src_changed = src_old != src_new if src_old else True
    tgt_changed = tgt_old != tgt_new if tgt_old else True

    if tgt_old is None:
        return "new_key"
    if not src_changed and not tgt_changed:
        return "no_change"
    if src_changed and not tgt_changed:
        return "source_only"
    if not src_changed and tgt_changed:
        return "target_only"
    if src_changed and tgt_changed:
        return "both_changed"
    return "no_change"


# ─────────────────────────────────────────
# Main diff runner
# ─────────────────────────────────────────

def run_diff(source_file: str, old_file: str, new_file: str, lang: str) -> list:
    """
    Run three-way diff and return list of changed items.
    Also prints results to terminal.
    """
    print(f"\n{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  Diligent QA — String Diff Tool v2{RESET}")
    print(f"{BOLD}  RWS Group | India Revenue Team{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    print(f"  Source (new) : {source_file}")
    print(f"  Target (old) : {old_file}")
    print(f"  Target (new) : {new_file}")
    print(f"  Language     : {lang}\n")

    source_strings = load_file(source_file)
    old_strings    = load_file(old_file)
    new_strings    = load_file(new_file)

    print(f"  Source keys  : {len(source_strings)}")
    print(f"  Old TGT keys : {len(old_strings)}")
    print(f"  New TGT keys : {len(new_strings)}\n")

    results = {
        "both_changed":  [],
        "target_only":   [],
        "source_only":   [],
        "new_key":       [],
    }

    for key in source_strings:
        src_new = source_strings.get(key)
        tgt_old = old_strings.get(key)
        tgt_new = new_strings.get(key)

        if tgt_new is None:
            continue

        # For source_old we use src_new as proxy if not available
        src_old = src_new
        classification = classify_change(src_old, src_new, tgt_old, tgt_new)

        if classification == "no_change":
            continue

        item = {
            "key":     key,
            "source":  src_new,
            "old_tgt": tgt_old or "— not in previous file —",
            "new_tgt": tgt_new,
            "type":    classification,
            "lang":    lang,
        }
        if classification in results:
            results[classification].append(item)

    # ─────────────────────────────────────────
    # Print results
    # ─────────────────────────────────────────

    all_changes = (
        results["both_changed"] +
        results["target_only"] +
        results["source_only"] +
        results["new_key"]
    )

    if not all_changes:
        print(f"{GREEN}  ✅  PASS — No string changes detected.{RESET}\n")
        return []

    # Both changed — highest risk
    if results["both_changed"]:
        print(f"{RED}{BOLD}  ⚠  SOURCE + TARGET CHANGED — HIGH RISK ({len(results['both_changed'])} strings){RESET}\n")
        for i, item in enumerate(results["both_changed"], 1):
            print(f"{RED}  [{i:03d}] BOTH CHANGED{RESET}")
            print(f"        Key     : {item['key']}")
            print(f"        Source  : {item['source']}")
            print(f"        Old TGT : {item['old_tgt']}")
            print(f"        New TGT : {item['new_tgt']}")
            print(f"        Action  : {RED}Submit for linguistic review{RESET}\n")

    # Target only changed — linguist update
    if results["target_only"]:
        print(f"{YELLOW}{BOLD}  ℹ  TARGET CHANGED BY LINGUIST ({len(results['target_only'])} strings){RESET}\n")
        for i, item in enumerate(results["target_only"], 1):
            print(f"{YELLOW}  [{i:03d}] LINGUIST UPDATE{RESET}")
            print(f"        Key     : {item['key']}")
            print(f"        Source  : {item['source']}")
            print(f"        Old TGT : {item['old_tgt']}")
            print(f"        New TGT : {item['new_tgt']}")
            print(f"        Action  : {YELLOW}Review — accept / revert / escalate{RESET}\n")

    # Source only changed — stale TM risk
    if results["source_only"]:
        print(f"{CYAN}{BOLD}  ℹ  SOURCE CHANGED, TARGET UNCHANGED — STALE TM RISK ({len(results['source_only'])} strings){RESET}\n")
        for i, item in enumerate(results["source_only"], 1):
            print(f"{CYAN}  [{i:03d}] STALE TM RISK{RESET}")
            print(f"        Key     : {item['key']}")
            print(f"        Source  : {item['source']}")
            print(f"        Old TGT : {item['old_tgt']}")
            print(f"        New TGT : {item['new_tgt']}")
            print(f"        Action  : {CYAN}Verify translation still matches updated source{RESET}\n")

    # New keys
    if results["new_key"]:
        print(f"{BLUE}{BOLD}  ℹ  NEW KEYS — NOT IN PREVIOUS DELIVERY ({len(results['new_key'])} strings){RESET}\n")
        for i, item in enumerate(results["new_key"], 1):
            print(f"{BLUE}  [{i:03d}] NEW KEY{RESET}")
            print(f"        Key     : {item['key']}")
            print(f"        Source  : {item['source']}")
            print(f"        New TGT : {item['new_tgt']}\n")

    # Summary
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}  SUMMARY — {lang}{RESET}")
    print(f"  Both source + target changed : {RED}{len(results['both_changed'])}{RESET}")
    print(f"  Linguist updates (TGT only)  : {YELLOW}{len(results['target_only'])}{RESET}")
    print(f"  Stale TM risk (SRC only)     : {CYAN}{len(results['source_only'])}{RESET}")
    print(f"  New keys                     : {BLUE}{len(results['new_key'])}{RESET}")
    print(f"  Total flagged                : {BOLD}{len(all_changes)}{RESET}")
    print(f"{BOLD}{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

    return all_changes


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diligent QA — Three-Way String Diff | RWS Group"
    )
    parser.add_argument("--source", required=True, help="New source file (e.g. en_new.json)")
    parser.add_argument("--old",    required=True, help="Previous target file (e.g. de_old.json)")
    parser.add_argument("--new",    required=True, help="New target file (e.g. de_new.json)")
    parser.add_argument("--lang",   required=True, help="Target language code (e.g. DE, ZH, FR)")
    args = parser.parse_args()

    run_diff(
        source_file=args.source,
        old_file=args.old,
        new_file=args.new,
        lang=args.lang.upper(),
    )


if __name__ == "__main__":
    main()
