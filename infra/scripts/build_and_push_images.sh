#!/usr/bin/env bash
set -euo pipefail

# build_and_push_images.sh
# -----------------------------------------------------------------------------
# Build and push 4th.GRC container images (PolicyEngine, Scorecard, etc.)
#
# Usage (from repo root):
#   bash infra/scripts/build_and_push_images.sh policyengine-svc myregistry.azurecr.io dev
#   bash infra/scripts/build_and_push_images.sh scorecard-app     myregistry.azurecr.io dev
#   bash infra/scripts/build_and_push_images.sh all               myregistry.azurecr.io dev
#
# This script is designed to run on:
#   - Linux / macOS
#   - Windows (Git Bash) with Docker Desktop
#
# It does NOT perform 'docker login' itself. CI/CD (GitHub Actions, AzDO) or
# you locally must login beforehand:
#   docker login myregistry.azurecr.io
# -----------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") <service|all> <registry> <tag>

Examples:
  $(basename "$0") policyengine-svc myregistry.azurecr.io dev
  $(basename "$0") scorecard-app   myregistry.azurecr.io v0.1.0
  $(basename "$0") all             myregistry.azurecr.io ${TAG:-dev}

Services:
  policyengine-svc   FastAPI PolicyEngine service
  scorecard-app      TrustOps Scorecard (Streamlit)
  all                Build & push all of the above
EOF
  exit 1
}

if [ "$#" -ne 3 ]; then
  usage
fi

SERVICE="$1"
REGISTRY="$2"
TAG="$3"

if [ -z "$REGISTRY" ] || [ -z "$TAG" ]; then
  echo "[error] REGISTRY and TAG must not be empty."
  usage
fi

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

build_and_push() {
  local name="$1"
  local dockerfile="$2"
  local context="$3"

  local image="${REGISTRY}/${name}:${TAG}"

  echo
  echo "============================================================"
  echo "[build] Service       : ${name}"
  echo "[build] Dockerfile    : ${dockerfile}"
  echo "[build] Context       : ${context}"
  echo "[build] Target image  : ${image}"
  echo "============================================================"

  if [ ! -f "${dockerfile}" ]; then
    echo "[error] Dockerfile not found: ${dockerfile}"
    exit 1
  fi

  pushd "${ROOT_DIR}" >/dev/null

  echo "[build] docker build ..."
  docker build \
    -t "${image}" \
    -f "${dockerfile}" \
    "${context}"

  echo "[push] docker push ${image} ..."
  docker push "${image}"

  popd >/dev/null
  echo "[ok] Done: ${image}"
}

# -----------------------------------------------------------------------------
# Service definitions
# -----------------------------------------------------------------------------

build_policyengine() {
  build_and_push \
    "policyengine-svc" \
    "infra/container-images/policyengine-svc/Dockerfile" \
    "."
}

build_scorecard() {
  build_and_push \
    "scorecard-app" \
    "infra/container-images/scorecard-app/Dockerfile" \
    "."
}

# -----------------------------------------------------------------------------
# Dispatch
# -----------------------------------------------------------------------------

case "${SERVICE}" in
  policyengine-svc)
    build_policyengine
    ;;

  scorecard-app)
    build_scorecard
    ;;

  all)
    build_policyengine
    build_scorecard
    ;;

  *)
    echo "[error] Unknown service: ${SERVICE}"
    echo "Supported: policyengine-svc | scorecard-app | all"
    exit 1
    ;;
esac

echo
echo "[done] All requested images built and pushed successfully."
