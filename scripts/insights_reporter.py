insights_reporter.py
====================
Diligent Account — RWS Group India Revenue Team
Maintained by: Ashok Poojary

Description:
    QA Insights Reporter. Analyses QA batch output across multiple jobs
    to surface error patterns, language health trends, and recurring issues.

    Reads saved report files (produced by batch_qa_runner.py --report)
    and generates a consolidated insights summary covering:
      - Job health trend (CLEAN / REVIEW / BLOCKED per job)
      - Aggregate totals across all analysed jobs
      - Per-language health scores and error rates
      - Error category breakdown (placeholder / untranslated / string diff)
      - Actionable recommendations

Usage:
    python insights_reporter.py --reports report_job062.txt report_job063.txt report_job064.txt
    python insights_reporter.py --reports-dir ./reports/
    python insights_reporter.py --reports-dir ./reports/ --output insights_summary.txt

Output:
    Terminal: colour-coded insights report
    File:     optional consolidated summary saved to --output path
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


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
# Report parser
# ─────────────────────────────────────────

def parse_report(filepath: Path) -> dict:
    """
    Parse a batch QA report text file produced by batch_qa_runner.py --report.
    Returns structured dict with per-job and per-language findings.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    findings = {
        "job":      filepath.stem,
        "filepath": str(filepath),
        "languages": defaultdict(lambda: {
            "placeholder_errors": 0,
            "untranslated":       0,
            "string_changes":     0,
            "blocked":            0,
            "review":             0,
            "clean":              0,
            "files":              [],
        }),
        "totals": {
            "files_processed":    0,
            "placeholder_errors": 0,
            "untranslated":       0,
            "string_changes":     0,
            "blocked":            0,
            "review":             0,
            "clean":              0,
        },
    }

    # Grand summary extraction
    for field, pattern in [
        ("files_processed",    r"Files processed\s*:\s*(\d+)"),
        ("placeholder_errors", r"Placeholder errors\s*:\s*(\d+)"),
        ("untranslated",       r"Untranslated segs\s*:\s*(\d+)"),
        ("string_changes",     r"String changes\s*:\s*(\d+)"),
        ("clean",              r"Clean files\s*:\s*(\d+)"),
        ("review",             r"Review required\s*:\s*(\d+)"),
        ("blocked",            r"Blocked files\s*:\s*(\d+)"),
    ]:
        m = re.search(pattern, content)
        if m:
            findings["totals"][field] = int(m.group(1))

    overall_m = re.search(r"OVERALL STATUS\s*:\s*(\w[\w ]+)", content)
    findings["overall_status"] = overall_m.group(1).strip() if overall_m else "UNKNOWN"

    # Per-language extraction — split on LANGUAGE: <code> markers
    lang_sections = re.split(r"LANGUAGE:\s*([A-Z]{2,6}(?:-[A-Z]{2,4})?)", content)
    for i in range(1, len(lang_sections), 2):
        lang = lang_sections[i].strip()
        if i + 1 >= len(lang_sections):
            break
        section = lang_sections[i + 1]

        findings["languages"][lang]["placeholder_errors"] += len(
            re.findall(r"Placeholders\s*:.*?CRITICAL", section)
        )
        findings["languages"][lang]["untranslated"] += len(
            re.findall(r"Untranslated\s*:.*?BLOCKED", section)
        )
        findings["languages"][lang]["string_changes"] += len(
            re.findall(r"String diff\s*:.*?change\(s\)", section)
        )
        findings["languages"][lang]["blocked"] += len(re.findall(r"STATUS: BLOCKED", section))
        findings["languages"][lang]["review"]  += len(re.findall(r"STATUS: REVIEW REQUIRED", section))
        findings["languages"][lang]["clean"]   += len(re.findall(r"STATUS: CLEAN", section))
        findings["languages"][lang]["files"].extend(re.findall(r"File:\s*(\S+)", section))

    return findings


# ─────────────────────────────────────────
# Aggregator
# ─────────────────────────────────────────

def aggregate(reports: list) -> dict:
    """Aggregate stats from a list of parsed report dicts."""
    agg = {
        "jobs_analysed": len(reports),
        "languages": defaultdict(lambda: {
            "placeholder_errors": 0,
            "untranslated":       0,
            "string_changes":     0,
            "blocked":            0,
            "review":             0,
            "clean":              0,
            "files_total":        0,
            "error_rate":         0.0,
        }),
        "job_statuses": [],
        "totals": {
            "files_processed":    0,
            "placeholder_errors": 0,
            "untranslated":       0,
            "string_changes":     0,
            "blocked":            0,
            "review":             0,
            "clean":              0,
        },
    }

    for r in reports:
        agg["job_statuses"].append({
            "job":    r["job"],
            "status": r["overall_status"],
            "files":  r["totals"]["files_processed"],
        })
        for key in agg["totals"]:
            agg["totals"][key] += r["totals"].get(key, 0)
        for lang, stats in r["languages"].items():
            for key in ["placeholder_errors", "untranslated", "string_changes", "blocked", "review", "clean"]:
                agg["languages"][lang][key] += stats[key]
            agg["languages"][lang]["files_total"] += len(stats["files"])

    for lang, stats in agg["languages"].items():
        total = stats["files_total"]
        if total > 0:
            stats["error_rate"] = round((stats["blocked"] + stats["review"]) / total * 100, 1)

    return agg


# ─────────────────────────────────────────
# Health scoring
# ─────────────────────────────────────────

def health_score(stats: dict) -> tuple:
    """Returns (score 0–100, label) based on clean-file ratio."""
    total = stats["files_total"]
    if total == 0:
        return 100, "N/A"
    score = round(stats["clean"] / total * 100)
    if score >= 90:
        label = "EXCELLENT"
    elif score >= 70:
        label = "GOOD"
    elif score >= 50:
        label = "FAIR"
    else:
        label = "POOR"
    return score, label


# ─────────────────────────────────────────
# Renderer
# ─────────────────────────────────────────

def render_insights(agg: dict, output_file: str = None) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    def log(line="", colour=""):
        print(f"{colour}{line}{RESET}" if colour else line)
        lines.append(re.sub(r'\033\[\d+m', '', line))

    log(f"\n{'━'*60}", BOLD + BLUE)
    log(f"  QA INSIGHTS REPORT — RWS Group | Diligent Account", BOLD)
    log(f"  Generated : {timestamp}", BOLD)
    log(f"  Jobs analysed : {agg['jobs_analysed']}", BOLD)
    log(f"{'━'*60}\n", BOLD + BLUE)

    # ── 1. Job health trend ──────────────────────────────────
    log(f"  {'─'*50}")
    log(f"  1. JOB HEALTH TREND", BOLD + CYAN)
    log(f"  {'─'*50}")
    for job in agg["job_statuses"]:
        status = job["status"]
        colour = GREEN if status == "CLEAN" else YELLOW if "REVIEW" in status else RED
        log(f"  {job['job']:<32} {status}", colour)
    log()

    # ── 2. Aggregate totals ──────────────────────────────────
    t = agg["totals"]
    log(f"  {'─'*50}")
    log(f"  2. AGGREGATE TOTALS ({agg['jobs_analysed']} job(s))", BOLD + CYAN)
    log(f"  {'─'*50}")
    log(f"  Files processed      : {t['files_processed']}")
    log(f"  Placeholder errors   : {t['placeholder_errors']}",
        RED if t['placeholder_errors'] else GREEN)
    log(f"  Untranslated segs    : {t['untranslated']}",
        RED if t['untranslated'] else GREEN)
    log(f"  String changes       : {t['string_changes']}",
        YELLOW if t['string_changes'] else GREEN)
    log(f"  Clean files          : {t['clean']}", GREEN)
    log(f"  Review required      : {t['review']}",
        YELLOW if t['review'] else GREEN)
    log(f"  Blocked files        : {t['blocked']}",
        RED if t['blocked'] else GREEN)
    log()

    # ── 3. Per-language health scores ────────────────────────
    log(f"  {'─'*50}")
    log(f"  3. PER-LANGUAGE HEALTH SCORES", BOLD + CYAN)
    log(f"  {'─'*50}")
    log(f"  {'Lang':<12} {'Score':>6} {'Label':<12} {'Blocked':>8} {'Review':>8} {'Clean':>7} {'ErrRate':>8}")
    log(f"  {'-'*12} {'-'*6} {'-'*12} {'-'*8} {'-'*8} {'-'*7} {'-'*8}")

    sorted_langs = sorted(
        agg["languages"].items(),
        key=lambda x: health_score(x[1])[0]
    )
    for lang, stats in sorted_langs:
        score, label = health_score(stats)
        colour = GREEN if score >= 90 else YELLOW if score >= 50 else RED
        log(
            f"  {lang:<12} {score:>5}% {label:<12} {stats['blocked']:>8} "
            f"{stats['review']:>8} {stats['clean']:>7} {stats['error_rate']:>7}%",
            colour,
        )
    log()

    # ── 4. Error category breakdown ──────────────────────────
    total_ph = sum(s["placeholder_errors"] for s in agg["languages"].values())
    total_ut = sum(s["untranslated"]       for s in agg["languages"].values())
    total_ch = sum(s["string_changes"]     for s in agg["languages"].values())

    log(f"  {'─'*50}")
    log(f"  4. ERROR CATEGORY BREAKDOWN", BOLD + CYAN)
    log(f"  {'─'*50}")
    log(f"  Placeholder errors (CRITICAL) : {total_ph}",
        RED if total_ph else GREEN)
    log(f"  Untranslated segments         : {total_ut}",
        RED if total_ut else GREEN)
    log(f"  String changes (review)       : {total_ch}",
        YELLOW if total_ch else GREEN)
    log()

    # ── 5. Recommendations ───────────────────────────────────
    log(f"  {'─'*50}")
    log(f"  5. RECOMMENDATIONS", BOLD + CYAN)
    log(f"  {'─'*50}")

    recommendations = []

    if total_ph > 0:
        worst = max(agg["languages"].items(), key=lambda x: x[1]["placeholder_errors"])
        recommendations.append((
            RED,
            f"  [!] Placeholder errors detected — prioritise {worst[0]} "
            f"({worst[1]['placeholder_errors']} error(s)). Block delivery until resolved.",
        ))

    if total_ut > 0:
        worst = max(agg["languages"].items(), key=lambda x: x[1]["untranslated"])
        recommendations.append((
            RED,
            f"  [!] Untranslated segments — highest in {worst[0]} "
            f"({worst[1]['untranslated']} segment(s)). Return to linguist for rework.",
        ))

    poor_langs = [l for l, s in agg["languages"].items() if health_score(s)[1] == "POOR"]
    if poor_langs:
        recommendations.append((
            YELLOW,
            f"  [~] Languages with POOR health: {', '.join(poor_langs)} — "
            f"escalate to PM for review.",
        ))

    excellent_langs = [l for l, s in agg["languages"].items() if health_score(s)[1] == "EXCELLENT"]
    if excellent_langs:
        recommendations.append((
            GREEN,
            f"  [OK] High-performing languages: {', '.join(excellent_langs)} — "
            f"maintain current QA process.",
        ))

    if total_ch > 0 and total_ph == 0 and total_ut == 0:
        recommendations.append((
            YELLOW,
            f"  [~] {total_ch} string change(s) pending Claude review — "
            f"paste flagged strings into Claude before delivering.",
        ))

    if not recommendations:
        log(f"  [OK] No critical issues detected across all analysed jobs. "
            f"Current QA process is effective.", GREEN)
    else:
        for colour, rec in recommendations:
            log(rec, colour)

    log()
    log(f"{'━'*60}\n", BOLD + BLUE)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{GREEN}  Insights saved to: {output_file}{RESET}\n")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diligent QA — Insights Reporter | RWS Group"
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--reports",
        nargs="+",
        metavar="FILE",
        help="One or more .txt report files produced by batch_qa_runner.py --report",
    )
    source_group.add_argument(
        "--reports-dir",
        metavar="DIR",
        help="Directory containing .txt report files (all matched automatically)",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help="Optional: save insights report to a file (e.g. insights_summary.txt)",
    )
    args = parser.parse_args()

    if args.reports_dir:
        reports_dir = Path(args.reports_dir)
        if not reports_dir.exists():
            print(f"{RED}ERROR: Reports directory not found: {reports_dir}{RESET}")
            sys.exit(1)
        report_files = sorted(reports_dir.glob("*.txt"))
        if not report_files:
            print(f"{RED}ERROR: No .txt report files found in {reports_dir}{RESET}")
            sys.exit(1)
    else:
        report_files = [Path(p) for p in args.reports]

    parsed = []
    for rf in report_files:
        if not rf.exists():
            print(f"{YELLOW}WARNING: File not found — skipping: {rf}{RESET}")
            continue
        try:
            parsed.append(parse_report(rf))
            print(f"{GREEN}  Loaded: {rf}{RESET}")
        except Exception as exc:
            print(f"{YELLOW}WARNING: Could not parse {rf}: {exc}{RESET}")

    if not parsed:
        print(f"{RED}ERROR: No valid reports to analyse.{RESET}")
        sys.exit(1)

    agg = aggregate(parsed)
    render_insights(agg, output_file=args.output)


if __name__ == "__main__":
    main()