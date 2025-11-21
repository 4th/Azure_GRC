#!/usr/bin/env bash
set -euo pipefail

# Run only integration tests (requires Azure/Cosmos env vars)
# Usage: ./scripts/run_integration_tests.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[tests] Running integration tests (ensure env vars are set)..."
pytest tests/integration -q
