#!/usr/bin/env bash
set -euo pipefail

# Run only unit tests
# Usage: ./scripts/run_unit_tests.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

pytest tests/unit -q
