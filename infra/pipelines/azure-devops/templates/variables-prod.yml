#!/usr/bin/env bash
set -euo pipefail

# teardown_environment.sh
# -----------------------------------------------------------------------------
# Convenience script to tear down (destroy) a 4th.GRC environment using Terraform.
#
# Works on:
#   - Linux / macOS
#   - Windows (Git Bash) with Terraform + Azure CLI installed
#
# Usage:
#   bash infra/scripts/teardown_environment.sh dev
#   bash infra/scripts/teardown_environment.sh test
#   bash infra/scripts/teardown_environment.sh prod
#
# Options:
#   --auto-approve   Skip interactive confirmation and run `terraform destroy -auto-approve`
#
# Example:
#   bash infra/scripts/teardown_environment.sh dev --auto-approve
# -----------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") <environment> [--auto-approve]

Examples:
  $(basename "$0") dev
  $(basename "$0") dev --auto-approve

Environments map to:
  infra/terraform/environments/<environment>/
EOF
  exit 1
}

if [ "$#" -lt 1 ]; then
  usage
fi

ENV_NAME="$1"
shift || true

AUTO_APPROVE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --auto-approve)
      AUTO_APPROVE=1
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "[error] Unknown option: $1"
      usage
      ;;
  esac
  shift || true
done

TF_WORKING_DIR="${ROOT_DIR}/infra/terraform/environments/${ENV_NAME}"

if [ ! -d "${TF_WORKING_DIR}" ]; then
  echo "[error] Terraform environment directory not found:"
  echo "       ${TF_WORKING_DIR}"
  exit 1
fi

echo "================================================================="
echo "[env]  Tearing down environment: ${ENV_NAME}"
echo "[env]  Terraform directory     : ${TF_WORKING_DIR}"
echo "[env]  Auto-approve?           : ${AUTO_APPROVE}"
echo "================================================================="

# Optional: sanity check Azure login
if command -v az >/dev/null 2>&1; then
  echo "[azure] Checking Azure CLI login (az account show)..."
  if ! az account show >/dev/null 2>&1; then
    echo "[azure] Not logged in. Run: az login"
  else
    echo "[azure] Azure CLI is logged in."
  fi
else
  echo "[warn] Azure CLI (az) not found in PATH. Skipping login check."
fi

cd "${TF_WORKING_DIR}"

echo
echo "-----------------------------------------------------------------"
echo "[tf] terraform init"
echo "-----------------------------------------------------------------"
terraform init

TFVARS_FILE="${ENV_NAME}.tfvars"

DESTROY_CMD="terraform destroy"
if [ -f "${TFVARS_FILE}" ]; then
  DESTROY_CMD="${DESTROY_CMD} -var-file=\"${TFVARS_FILE}\""
else
  echo "[warn] No ${TFVARS_FILE} found in ${TF_WORKING_DIR}."
  echo "       terraform destroy will run without -var-file."
fi

if [ "${AUTO_APPROVE}" -eq 1 ]; then
  DESTROY_CMD="${DESTROY_CMD} -auto-approve"
fi

echo
echo "-----------------------------------------------------------------"
echo "[tf] terraform destroy (env=${ENV_NAME})"
echo "-----------------------------------------------------------------"

if [ "${AUTO_APPROVE}" -eq 0 ]; then
  echo
  read -r -p "Destroy ALL resources for environment '${ENV_NAME}'? [y/N]: " CONFIRM
  case "${CONFIRM}" in
    y|Y|yes|YES)
      ;;
    *)
      echo "[tf] Destroy cancelled by user."
      exit 0
      ;;
  esac
fi

# shellcheck disable=SC2086
eval "${DESTROY_CMD}"

echo
echo "[done] Environment '${ENV_NAME}' destroyed successfully."
