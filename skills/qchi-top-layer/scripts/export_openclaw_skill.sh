#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${1:-$ROOT/../../dist}"
mkdir -p "$OUT_DIR"

cd "$ROOT/.."
zip -r "$OUT_DIR/qchi-top-layer.skill" qchi-top-layer \
  -x "*/__pycache__/*" "*.pyc"

echo "Created: $OUT_DIR/qchi-top-layer.skill"
