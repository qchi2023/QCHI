#!/usr/bin/env bash
set -euo pipefail

missing=0

check_cmd() {
  local cmd="$1"
  local label="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[OK] $label ($cmd)"
  else
    echo "[MISSING] $label ($cmd)"
    missing=1
  fi
}

echo "QCHI environment check"
echo "----------------------"

check_cmd git "Version control"
check_cmd python3 "Python runtime"
check_cmd lyx "LyX editor (direct .lyx workflow)"
check_cmd cargo "Rust package manager (qchi-lint)"
check_cmd rustc "Rust compiler (qchi-lint)"

# Optional host runtime indicators (informational)
echo
echo "Host runtimes (informational)"
for cmd in openclaw codex claude cursor; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[FOUND] $cmd"
  fi
done

echo
if [[ $missing -eq 1 ]]; then
  echo "Result: FAIL (missing required tools)"
  echo "See docs/INSTALL_PREREQS.md for install commands."
  exit 1
else
  echo "Result: PASS"
fi
