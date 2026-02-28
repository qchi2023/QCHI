#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${1:-8787}"
python3 bin/qchi dashboard serve --port "$PORT"
