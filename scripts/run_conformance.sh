#!/usr/bin/env bash
set -euo pipefail

project_root="${1:?usage: run_conformance.sh <project-root> <project-id>}"
project_id="${2:?usage: run_conformance.sh <project-root> <project-id>}"

repo_root="$(cd "$(dirname "$0")/.." && pwd)"

python3 "$repo_root/tools/qchi_lyx_lint.py" --root "$project_root/artifacts/lyx"
python3 "$repo_root/tools/validate_repro_bundle.py" --project-root "$project_root" --project-id "$project_id"

echo "PASS full conformance checks"
