#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-$HOME/.local/share/opencode/skills/QCHI}"
REPO_URL="${QCHI_REPO_URL:-https://github.com/qchi2023/QCHI.git}"

mkdir -p "$(dirname "$TARGET")"

if [[ -d "$TARGET/.git" ]]; then
  git -C "$TARGET" fetch origin
  git -C "$TARGET" reset --hard origin/main
else
  git clone "$REPO_URL" "$TARGET"
fi

cat > "$TARGET/AGENTS.md" <<'EOF'
# QCHI Agent Bootstrap (OpenCode)

You are running QCHI in OpenCode.

## Mandatory load order
1. Read `skills/qchi/SKILL.md`
2. Read `skills/qchi/adapters/opencode.md`
3. Read `skills/qchi/checklists/QUALITY_GATE.md`
4. Use references under `skills/qchi/references/` as needed

## Operating defaults
- full serious mode by default
- paper reproduction uses multi-agent by default unless explicitly overridden
- direct `.lyx` authoring only
- do not create/update `publishable_draft.lyx` unless explicitly requested

## Learning and persistence
- log learning under `skills/qchi/learning/`
- use project-scoped tracks under `skills/qchi/learning/projects/<project-id>/`
- tracks required: physics, writing, coding-plotting

## Quality and validation
- pass `skills/qchi/checklists/QUALITY_GATE.md` before final output
- run local validators when applicable:
  - `python3 tools/validate_project_learning.py`
  - `python3 tools/run_benchmarks.py`
  - `python3 tools/qchi_lyx_lint.py --root .`

## Git discipline
- commit meaningful changes
EOF

echo "Registered QCHI for OpenCode at: $TARGET"
echo "Launch with: opencode $TARGET"
