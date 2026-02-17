#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/../../" && pwd)"
DIST="$REPO_ROOT/dist"
mkdir -p "$DIST"

cd "$ROOT/.."
zip -r "$DIST/qchi-r.skill" qchi-r -x "*/__pycache__/*" "*.pyc"
zip -r "$DIST/qchi-r-portable.zip" qchi-r -x "*/__pycache__/*" "*.pyc"

echo "Built: $DIST/qchi-r.skill"
echo "Built: $DIST/qchi-r-portable.zip"
