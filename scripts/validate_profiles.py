#!/usr/bin/env python
"""
Validate all profiles and rules under profiles/ and rules/ using policyengine validators.
Usage: python scripts/validate_profiles.py
"""

import sys
from pathlib import Path
from typing import List

import yaml

from policyengine.validators import validate_profile
from policyengine.schema import PolicyProfile  # or your equivalent model


ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_profile_file(path: Path) -> List[str]:
    data = load_yaml(path)
    errors: List[str] = []

    try:
        # Structural validation (custom)
        validate_profile(data)
        # Schema validation (pydantic)
        PolicyProfile.model_validate(data)
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    return errors


def main() -> int:
    if not PROFILES_DIR.exists():
        print(f"[ERROR] Profiles directory not found: {PROFILES_DIR}")
        return 1

    failures = 0
    for path in sorted(PROFILES_DIR.glob("*.yaml")):
        rel = path.relative_to(ROOT_DIR)
        errors = validate_profile_file(path)
        if errors:
            failures += 1
            print(f"[FAIL] {rel}")
            for err in errors:
                print(f"       - {err}")
        else:
            print(f"[OK]   {rel}")

    if failures:
        print(f"\n[SUMMARY] {failures} profile(s) failed validation ❌")
        return 1

    print("\n[SUMMARY] All profiles valid ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
