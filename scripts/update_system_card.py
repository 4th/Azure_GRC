#!/usr/bin/env python
"""
Update SYSTEM_CARD.md from a JSON config and/or evaluation result.
Usage: python scripts/update_system_card.py config.json eval_result.json
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict


ROOT_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT_DIR / "docs" / "SYSTEM_CARD_TEMPLATE.md"
OUT = ROOT_DIR / "docs" / "SYSTEM_CARD.md"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: update_system_card.py config.json [eval_result.json]")
        return 1

    config = load_json(Path(argv[1]))
    eval_data: Dict[str, Any] = {}
    if len(argv) >= 3:
        eval_data = load_json(Path(argv[2]))

    template = TEMPLATE.read_text(encoding="utf-8")

    # Simple placeholder replacement
    replacements = {
        "{{SYSTEM_NAME}}": config.get("system_name", "Unknown System"),
        "{{OWNER}}": config.get("owner", "N/A"),
        "{{PROFILE_ID}}": eval_data.get("profile_id", config.get("profile_id", "N/A")),
        "{{SCORE}}": str(eval_data.get("summary", {}).get("score", "N/A")),
        "{{VERDICT}}": eval_data.get("summary", {}).get("verdict", "N/A"),
        "{{DESCRIPTION}}": config.get("description", ""),
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, str(value))

    OUT.write_text(template, encoding="utf-8")
    print(f"[system-card] Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
