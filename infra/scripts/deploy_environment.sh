#!/usr/bin/env bash
set -euo pipefail

# deploy_environment.sh
# -----------------------------------------------------------------------------
# Convenience script to deploy a 4th.GRC environment using Terraform.
#
# Works on:
#   - Linux / macOS
#   - Windows (Git Bash) with Terraform + Azure CLI installed
#
# Usage:
#   bash infra/scripts/deploy_environment.sh dev
#   bash infra/scripts/deploy_environment.sh test
#   bash infra/scripts/deploy_environment.sh prod
#
# Options:
#   --plan-only    Run init/validate/plan but do NOT apply
#   --auto-approve Skip interactive confirmation and run `terraform apply -auto-approve`
#
# Example:
#   bash infra/scripts/deploy_environment.sh dev --auto-approve
# -----------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") <environment> [--plan-only] [--auto-approve]

Examples:
  $(basename "$0") dev
  $(basename "$0") dev --plan-only
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

PLAN_ONLY=0
AUTO_APPROVE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan-only)
      PLAN_ONLY=1
      ;;
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
echo "[env]  Deploying environment: ${ENV_NAME}"
echo "[env]  Terraform directory  : ${TF_WORKING_DIR}"
echo "[env]  Plan only?           : ${PLAN_ONLY}"
echo "[env]  Auto-approve?        : ${AUTO_APPROVE}"
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

echo
echo "-----------------------------------------------------------------"
echo "[tf] terraform validate"
echo "-----------------------------------------------------------------"
terraform validate

PLAN_FILE="tfplan-${ENV_NAME}.bin"
TFVARS_FILE="${ENV_NAME}.tfvars"

if [ ! -f "${TFVARS_FILE}" ]; then
  echo "[warn] No ${TFVARS_FILE} found in ${TF_WORKING_DIR}."
  echo "       Terraform will run without -var-file, or you can create:"
  echo "       ${TFVARS_FILE}"
  PLAN_CMD="terraform plan -out=${PLAN_FILE}"
else
  PLAN_CMD="terraform plan -var-file=\"${TFVARS_FILE}\" -out=${PLAN_FILE}"
fi

echo
echo "-----------------------------------------------------------------"
echo "[tf] terraform plan (env=${ENV_NAME})"
echo "-----------------------------------------------------------------"
# shellcheck disable=SC2086
eval "${PLAN_CMD}"

if [ "${PLAN_ONLY}" -eq 1 ]; then
  echo
  echo "[tf] Plan-only mode enabled. Skipping apply."
  echo "     Saved plan file: ${TF_WORKING_DIR}/${PLAN_FILE}"
  exit 0
fi

echo
echo "-----------------------------------------------------------------"
echo "[tf] terraform apply (env=${ENV_NAME})"
echo "-----------------------------------------------------------------"

if [ "${AUTO_APPROVE}" -eq 1 ]; then
  terraform apply -auto-approve "${PLAN_FILE}"
else
  echo
  read -r -p "Apply this plan to environment '${ENV_NAME}'? [y/N]: " CONFIRM
  case "${CONFIRM}" in
    y|Y|yes|YES)
      terraform apply "${PLAN_FILE}"
      ;;
    *)
      echo "[tf] Apply cancelled by user."
      exit 0
      ;;
  esac
fi

echo
echo "[done] Environment '${ENV_NAME}' deployed successfully."
