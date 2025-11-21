#!/usr/bin/env bash
set -euo pipefail

# Run the PolicyEngine FastAPI service locally
# Usage: ./scripts/dev_run_policyengine.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"

# Load local env if present
if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
fi

echo "[dev] Starting PolicyEngine service on http://127.0.0.1:8080 ..."
uvicorn services.policyengine_svc.main:app \
  --host 0.0.0.0 \
  --port 8080 \
  --reload
