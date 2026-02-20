#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_learning_dashboard.py
PORT="${1:-8787}"
echo "Serving dashboard at http://127.0.0.1:${PORT}/dashboard/"
python3 -m http.server "$PORT"
