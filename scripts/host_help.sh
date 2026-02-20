#!/usr/bin/env bash
set -euo pipefail

host="${1:-all}"

show_common() {
  cat <<'EOF'
Common setup
------------
git clone git@github.com:qchi2023/QCHI.git
cd QCHI
bash tools/check_env.sh
python3 tools/validate_project_learning.py

Always load
- skills/qchi/SKILL.md
- skills/qchi/references/
EOF
}

show_openclaw() {
  cat <<'EOF'
OpenClaw
--------
openclaw gateway status
openclaw gateway start
openclaw gateway restart
openclaw help
openclaw gateway --help
Adapter: skills/qchi/adapters/openclaw.md
EOF
}

show_opencode() {
  cat <<'EOF'
OpenCode
--------
bash scripts/bootstrap_opencode_ubuntu.sh
Adapter: skills/qchi/adapters/opencode.md
EOF
}

show_cursor() {
  cat <<'EOF'
Cursor or VS Code flow
----------------------
Use host instruction/context panel and load
- skills/qchi/SKILL.md
- skills/qchi/adapters/cursor.md
- needed files under skills/qchi/references/
EOF
}

show_antigravity() {
  cat <<'EOF'
Antigravity
-----------
Use host instruction/context panel and load
- skills/qchi/SKILL.md
- skills/qchi/adapters/antigravity.md
EOF
}

show_codex() {
  cat <<'EOF'
Codex or other generic hosts
----------------------------
Use host instruction/context panel and load
- skills/qchi/SKILL.md
- skills/qchi/adapters/generic.md
- relevant files under skills/qchi/references/
EOF
}

show_lint() {
  cat <<'EOF'
Optional local lint
-------------------
cargo build --manifest-path tools/qchi-lint/Cargo.toml --release
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind runs --file skills/qchi/learning/runs.jsonl
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind evals --file skills/qchi/learning/evals.jsonl
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind regressions --file skills/qchi/learning/regressions.jsonl
EOF
}

case "$host" in
  all)
    show_common
    echo
    show_openclaw
    echo
    show_opencode
    echo
    show_cursor
    echo
    show_antigravity
    echo
    show_codex
    echo
    show_lint
    ;;
  openclaw) show_common; echo; show_openclaw ;;
  opencode) show_common; echo; show_opencode ;;
  cursor|vscode) show_common; echo; show_cursor ;;
  antigravity) show_common; echo; show_antigravity ;;
  codex|generic|other) show_common; echo; show_codex ;;
  lint) show_lint ;;
  *)
    echo "Unknown host: $host"
    echo "Usage: bash scripts/host_help.sh [all|openclaw|opencode|cursor|vscode|antigravity|codex|generic|lint]"
    exit 1
    ;;
esac
