#!/usr/bin/env bash
set -euo pipefail

# Run the TrustOps Scorecard Streamlit app
# Usage: ./scripts/dev_run_scorecard.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"

if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
fi

echo "[dev] Starting TrustOps Scorecard on http://localhost:8501 ..."
streamlit run apps/scorecard/streamlit_app.py
