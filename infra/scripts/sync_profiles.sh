#!/usr/bin/env bash
set -euo pipefail

# sync_profiles.sh
# -----------------------------------------------------------------------------
# Thin wrapper around scripts/sync_profiles_to_blob.py
# to sync profiles/ -> Azure Blob Storage / ADLS Gen2
#
# Usage (from repo root):
#   bash infra/scripts/sync_profiles.sh
#
# Required environment variables:
#   PROFILES_BLOB_ACCOUNT_URL   e.g. https://4thgrcdev.blob.core.windows.net
#   PROFILES_BLOB_CONTAINER     e.g. policy-profiles   (default in script)
#   PROFILES_BLOB_PREFIX        e.g. profiles/         (optional)
#
# Works on:
#   - Linux / macOS
#   - Windows (Git Bash) with Python installed
# -----------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY_SCRIPT="${ROOT_DIR}/scripts/sync_profiles_to_blob.py"

usage() {
  cat <<EOF
Usage:
  $(basename "$0")

This script expects the Python helper:
  scripts/sync_profiles_to_blob.py

And these environment variables:

  PROFILES_BLOB_ACCOUNT_URL   (required)
  PROFILES_BLOB_CONTAINER     (optional, default: policy-profiles)
  PROFILES_BLOB_PREFIX        (optional, default: profiles/)

Example:

  export PROFILES_BLOB_ACCOUNT_URL="https://4thgrcdev.blob.core.windows.net"
  export PROFILES_BLOB_CONTAINER="policy-profiles"
  export PROFILES_BLOB_PREFIX="profiles/"

  bash infra/scripts/sync_profiles.sh
EOF
  exit 1
}

if [ ! -f "${PY_SCRIPT}" ]; then
  echo "[error] Python helper not found: ${PY_SCRIPT}"
  echo "       Make sure scripts/sync_profiles_to_blob.py exists."
  exit 1
fi

if [ "${1-}" = "-h" ] || [ "${1-}" = "--help" ]; then
  usage
fi

if [ -z "${PROFILES_BLOB_ACCOUNT_URL:-}" ]; then
  echo "[error] PROFILES_BLOB_ACCOUNT_URL is not set."
  echo "        Set it to your Blob endpoint, e.g.:"
  echo "        export PROFILES_BLOB_ACCOUNT_URL=\"https://<account>.blob.core.windows.net\""
  exit 1
fi

echo "================================================================="
echo "[sync]  4th.GRC profiles -> Azure Blob / ADLS Gen2"
echo "[sync]  ROOT_DIR                  : ${ROOT_DIR}"
echo "[sync]  PROFILES_BLOB_ACCOUNT_URL : ${PROFILES_BLOB_ACCOUNT_URL}"
echo "[sync]  PROFILES_BLOB_CONTAINER   : ${PROFILES_BLOB_CONTAINER:-policy-profiles}"
echo "[sync]  PROFILES_BLOB_PREFIX      : ${PROFILES_BLOB_PREFIX:-profiles/}"
echo "================================================================="

# Prefer venv python if active
if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "[error] No python or python3 found in PATH."
  exit 1
fi

pushd "${ROOT_DIR}" >/dev/null

echo "[sync] Running Python sync script..."
"${PYTHON_BIN}" "${PY_SCRIPT}"

popd >/dev/null

echo "[sync] Done."
