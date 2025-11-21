#!/usr/bin/env bash
set -euo pipefail

# Run formatting, linting, and type checking
# Usage: ./scripts/lint_and_typecheck.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[lint] black ..."
black policyengine services agents functions apps tests

echo "[lint] isort ..."
isort policyengine services agents functions apps tests

echo "[lint] flake8 ..."
flake8 policyengine services agents functions apps tests

echo "[type] mypy ..."
mypy policyengine services agents functions
