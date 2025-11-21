#!/usr/bin/env python
"""
Render a simple JSON and Markdown index of all profiles for docs/UI.
Usage: python scripts/render_profile_index.py
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"
OUT_JSON = ROOT_DIR / "docs" / "profile_index.json"
OUT_MD = ROOT_DIR / "docs" / "PROFILE_INDEX.md"


def load_profile(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    profiles: List[Dict[str, Any]] = []

    for path in sorted(PROFILES_DIR.glob("*.yaml")):
        data = load_profile(path)
        meta = data.get("metadata", {})
        profiles.append(
            {
                "file": str(path.relative_to(ROOT_DIR)),
                "id": data.get("profile_id"),
                "name": meta.get("title") or data.get("name"),
                "version": data.get("version"),
                "standards": meta.get("standards") or [],
                "tags": meta.get("tags") or [],
                "description": meta.get("description", ""),
            }
        )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(profiles, indent=2), encoding="utf-8")
    print(f"[index] Wrote JSON index to {OUT_JSON}")

    # Simple Markdown index
    lines = [
        "# Profile Index",
        "",
        "| Profile ID | Name | Version | Standards | Tags | File |",
        "|-----------|------|---------|-----------|------|------|",
    ]

    for p in profiles:
        standards = ", ".join(p["standards"])
        tags = ", ".join(p["tags"])
        lines.append(
            f"| {p['id']} | {p['name']} | {p['version']} | "
            f"{standards} | {tags} | `{p['file']}` |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[index] Wrote Markdown index to {OUT_MD}")


if __name__ == "__main__":
    main()
