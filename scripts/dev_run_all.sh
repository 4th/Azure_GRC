#!/usr/bin/env bash
set -euo pipefail

# Start PolicyEngine and Scorecard together in separate terminals
# Usage: ./scripts/dev_run_all.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
fi

export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"

echo "[dev] Starting PolicyEngine on :8080 ..."
uvicorn services.policyengine_svc.main:app \
  --host 0.0.0.0 \
  --port 8080 \
  --reload \
  &

PE_PID=$!

echo "[dev] Starting TrustOps Scorecard on :8501 ..."
streamlit run apps/scorecard/streamlit_app.py &
SC_PID=$!

echo "[dev] PolicyEngine PID: $PE_PID"
echo "[dev] Scorecard PID:   $SC_PID"
echo "[dev] Press Ctrl+C to stop both."

wait
