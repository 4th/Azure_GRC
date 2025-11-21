#!/usr/bin/env bash
set -euo pipefail

# Build local Docker images for PolicyEngine svc and Scorecard
# Usage: ./scripts/build_docker_images.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

REGISTRY="${REGISTRY:-local}"
TAG="${TAG:-dev}"

echo "[docker] Building policyengine-svc..."
docker build \
  -t "${REGISTRY}/policyengine-svc:${TAG}" \
  -f services/policyengine_svc/Dockerfile \
  .

echo "[docker] Building scorecard-app..."
docker build \
  -t "${REGISTRY}/scorecard-app:${TAG}" \
  -f apps/scorecard/Dockerfile \
  .

echo "[docker] Images built:"
docker images | grep -E "policyengine-svc|scorecard-app" || true
