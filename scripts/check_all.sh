#!/usr/bin/env bash
set -euo pipefail

# Run pre-commit, tests, and typechecks
# Usage: ./scripts/check_all.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[check] Running pre-commit hooks on all files..."
pre-commit run --all-files

echo "[check] Running unit + integration tests..."
pytest

echo "[check] Running mypy..."
mypy policyengine services agents functions

echo "[check] All checks passed ✅"
