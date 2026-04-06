"""
validate_files.py
=================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Validates JSON and YAML structure of all delivery files.
Checks every file in the New Translated folder recursively.

Usage:
    python validate_files.py --folder "C:\\path\\to\\New Translated"
    python validate_files.py --folder "C:\\path\\to\\New Translated" --report validate_report.txt
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def validate_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            return False, "File is empty"
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON error at line {e.lineno}, col {e.colno}: {e.msg}"
    except UnicodeDecodeError as e:
        return False, f"Encoding error: {e}"
    except Exception as e:
        return False, str(e)


def validate_yaml(path):
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            return False, "File is empty"
        yaml.safe_load(content)
        return True, None
    except ImportError:
        try:
            with open(path, "r", encoding="utf-8") as f:
                f.read()
            return True, "YAML not installed — encoding check only"
        except Exception as e:
            return False, str(e)
    except Exception as e:
        return False, f"YAML error: {e}"


def validate_strings(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            return True, None
        lines = content.split("\n")
        errors = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("/*"):
                continue
            if not re.match(r'^".*"\s*=\s*".*"\s*;', line):
                errors.append(f"Line {i}: {line[:60]}")
        if errors:
            return False, " | ".join(errors[:3])
        return True, None
    except Exception as e:
        return False, str(e)


def get_file_size(path):
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f}KB"
    else:
        return f"{size/1024/1024:.1f}MB"


def validate_folder(base_folder, report_file=None):
    base = Path(base_folder)
    if not base.exists():
        print(f"{RED}ERROR: Folder not found: {base_folder}{RESET}")
        return

    SUPPORTED = {
        ".json":    validate_json,
        ".resjson": validate_json,
        ".yml":     validate_yaml,
        ".yaml":    validate_yaml,
        ".strings": validate_strings,
    }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_lines = []

    def log(line="", colour=""):
        text = f"{colour}{line}{RESET}" if colour else line
        print(text)
        report_lines.append(re.sub(r'\033\[\d+m', '', line))

    log(f"\n{'━'*58}", BOLD+BLUE)
    log(f"  FILE VALIDATION REPORT", BOLD)
    log(f"  RWS Group | India Revenue Team | Ashok Poojary", BOLD)
    log(f"  Run date : {timestamp}", BOLD)
    log(f"  Folder   : {base_folder}", BOLD)
    log(f"{'━'*58}\n", BOLD+BLUE)

    all_files = []
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            all_files.append(path)

    log(f"  Files found: {len(all_files)}\n")

    results = {"valid": [], "invalid": [], "warning": []}
    current_lang = None

    for path in all_files:
        try:
            rel = path.relative_to(base)
            lang = rel.parts[0] if len(rel.parts) > 1 else "root"
        except ValueError:
            lang = "unknown"

        if lang != current_lang:
            log(f"\n  {'─'*50}")
            log(f"  {lang}", BOLD+CYAN)
            current_lang = lang

        ext = path.suffix.lower()
        validator = SUPPORTED[ext]
        ok, error = validator(str(path))

        rel_path = str(path.relative_to(base))
        size = get_file_size(str(path))

        if ok:
            if error:
                log(f"  ⚠️  {YELLOW}WARN{RESET}  {rel_path:60} {size}")
                results["warning"].append((rel_path, error))
            else:
                log(f"  ✅ {GREEN}VALID{RESET} {rel_path:60} {size}")
                results["valid"].append(rel_path)
        else:
            log(f"  ❌ {RED}FAIL{RESET}  {rel_path:60} {size}")
            log(f"       {RED}{error}{RESET}")
            results["invalid"].append((rel_path, error))

    log(f"\n{'━'*58}", BOLD+BLUE)
    log(f"  SUMMARY", BOLD)
    log(f"{'━'*58}", BOLD+BLUE)
    log(f"  Total files checked : {len(all_files)}")
    log(f"  Valid               : {GREEN}{len(results['valid'])}{RESET}")
    log(f"  Warnings            : {YELLOW}{len(results['warning'])}{RESET}")
    log(f"  Invalid             : {RED}{len(results['invalid'])}{RESET}")

    if results["invalid"]:
        log(f"\n  {RED}{BOLD}INVALID FILES — fix before delivery:{RESET}")
        for path, error in results["invalid"]:
            log(f"    ✗ {path}")
            log(f"      {RED}{error}{RESET}")
        log(f"\n  {RED}{BOLD}OVERALL: FAIL — do not deliver until errors are fixed{RESET}")
    elif results["warning"]:
        log(f"\n  {YELLOW}OVERALL: PASS WITH WARNINGS{RESET}")
    else:
        log(f"\n  {GREEN}{BOLD}OVERALL: ALL FILES VALID — safe to deliver{RESET}")

    log(f"{'━'*58}\n", BOLD+BLUE)

    if report_file:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"{GREEN}  Report saved: {report_file}{RESET}\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Delivery File Validator | RWS Group Diligent QA"
    )
    parser.add_argument("--folder", required=True,
                        help="Path to New Translated folder")
    parser.add_argument("--report", default=None,
                        help="Save report to file e.g. validate_report.txt")
    args = parser.parse_args()
    validate_folder(args.folder, args.report)


if __name__ == "__main__":
    main()
