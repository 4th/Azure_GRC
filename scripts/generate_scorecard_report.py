#!/usr/bin/env python
"""
Generate a Markdown scorecard report from a PolicyEngine evaluation result.
Usage: python scripts/generate_scorecard_report.py path/to/eval_result.json
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

from datetime import datetime


def load_eval(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: generate_scorecard_report.py eval_result.json")
        return 1

    in_path = Path(argv[1])
    data = load_eval(in_path)

    profile_id = data.get("profile_id", "unknown-profile")
    summary = data.get("summary", {})
    score = summary.get("score")
    verdict = summary.get("verdict")
    findings = data.get("findings", [])

    ts = datetime.utcnow().isoformat() + "Z"
    out_path = in_path.with_suffix(".md")

    lines: list[str] = [
        f"# Governance Scorecard – {profile_id}",
        "",
        f"- Generated at: `{ts}`",
        f"- Overall score: **{score}**",
        f"- Verdict: **{verdict}**",
        "",
        "## Findings",
        "",
        "| ID | Title | Severity | Status | Message |",
        "|----|-------|----------|--------|---------|",
    ]

    for f in findings:
        fid = f.get("id")
        title = f.get("title", "")
        severity = f.get("severity", "")
        status = f.get("status", "")
        message = f.get("message", "").replace("\n", " ")
        lines.append(
            f"| {fid} | {title} | {severity} | {status} | {message} |"
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[report] Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
