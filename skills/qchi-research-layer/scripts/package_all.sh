#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/../../" && pwd)"
DIST="$REPO_ROOT/dist"
mkdir -p "$DIST"

cd "$ROOT/.."
zip -r "$DIST/qchi-research-layer.skill" qchi-research-layer -x "*/__pycache__/*" "*.pyc"
zip -r "$DIST/qchi-research-layer-portable.zip" qchi-research-layer -x "*/__pycache__/*" "*.pyc"

echo "Built: $DIST/qchi-research-layer.skill"
echo "Built: $DIST/qchi-research-layer-portable.zip"
