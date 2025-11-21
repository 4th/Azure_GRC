#!/usr/bin/env bash
set -euo pipefail

# Simple release tagging helper
# Usage: ./scripts/tag_release.sh v0.3.0

if [ $# -ne 1 ]; then
  echo "Usage: $0 vX.Y.Z"
  exit 1
fi

VERSION="$1"

if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.1.0"
  exit 1
fi

echo "[release] Tagging $VERSION ..."
git tag -a "$VERSION" -m "Release $VERSION"
git push origin "$VERSION"

echo "[release] Done."
