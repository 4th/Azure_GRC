#!/usr/bin/env bash
set -euo pipefail

# Create and initialize a Python virtual environment
# Usage: ./scripts/dev_create_venv.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

echo "[dev] Creating venv at $VENV_DIR using $PYTHON_BIN ..."
$PYTHON_BIN -m venv "$VENV_DIR"

echo "[dev] Activating venv and installing dependencies ..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  pip install -e .
fi

echo "[dev] Done. Activate with: source $VENV_DIR/bin/activate"
