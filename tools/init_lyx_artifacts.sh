#!/usr/bin/env bash
set -euo pipefail
proj_root="${1:?usage: init_lyx_artifacts.sh <project-root>}"
mkdir -p "$proj_root/artifacts/lyx"
tpl="$(cd "$(dirname "$0")/.." && pwd)/skills/qchi/references/LYX_MINIMAL_TEMPLATE.lyx"
cp "$tpl" "$proj_root/artifacts/lyx/notes.lyx"
cp "$tpl" "$proj_root/artifacts/lyx/systematics_plots.lyx"
echo "Initialized LyX artifacts in $proj_root/artifacts/lyx"
