#!/usr/bin/env bash
set -euo pipefail

# Run basic security/static analysis scans
# Usage: ./scripts/scan_security.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[sec] Running bandit (Python security scan)..."
bandit -r policyengine services agents functions -q || true

echo "[sec] Running yamllint on profiles/ and rules/..."
yamllint profiles rules || true

echo "[sec] (Optional) Running detect-secrets if installed..."
if command -v detect-secrets >/dev/null 2>&1; then
  detect-secrets scan || true
else
  echo "[sec] detect-secrets not installed; skipping."
fi

echo "[sec] Security scan completed (non-blocking)."
