# Host Commands Quickstart

Use these commands on a fresh machine.

Quick helper
```bash
bash scripts/host_help.sh all
bash scripts/host_help.sh codex
bash scripts/host_help.sh openclaw
```

## 1) Clone and bootstrap
```bash
git clone git@github.com:qchi2023/QCHI.git
cd QCHI
bash scripts/bootstrap_opencode_ubuntu.sh
```

If you do not want full bootstrap, run minimum checks
```bash
bash tools/check_env.sh
python3 tools/validate_project_learning.py
```

## 2) Canonical skill files to load (all hosts)
Always load these first
- `skills/qchi/SKILL.md`
- `skills/qchi/references/`

Host-specific adapter to load
- OpenClaw: `skills/qchi/adapters/openclaw.md`
- OpenCode: `skills/qchi/adapters/opencode.md`
- Cursor or VS Code flow: `skills/qchi/adapters/cursor.md`
- Antigravity: `skills/qchi/adapters/antigravity.md`
- Generic fallback (Codex or others): `skills/qchi/adapters/generic.md`

## 3) OpenClaw
OpenClaw CLI commands
```bash
openclaw gateway status
openclaw gateway start
openclaw gateway restart
```

For OpenClaw-specific options use
```bash
openclaw help
openclaw gateway --help
```

## 4) OpenCode registration and launch
```bash
bash scripts/register_opencode_qchi.sh
opencode ~/.local/share/opencode/skills/QCHI
```

Guide
- `docs/OPENCODE_REGISTER.md`

## 5) Codex / Claude Code / Cursor / VS Code / Antigravity / others
I do not hardcode undocumented CLI commands here.

Use the host's native way to set system instructions/context and point it to
- `skills/qchi/SKILL.md`
- one adapter file from `skills/qchi/adapters/`
- relevant references under `skills/qchi/references/`

Then keep learning logs in
- `skills/qchi/learning/`
- `skills/qchi/learning/projects/<project-id>/...`

## 5) Optional local lint
```bash
cargo build --manifest-path tools/qchi-lint/Cargo.toml --release
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind runs --file skills/qchi/learning/runs.jsonl
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind evals --file skills/qchi/learning/evals.jsonl
cargo run --manifest-path tools/qchi-lint/Cargo.toml -- jsonl --kind regressions --file skills/qchi/learning/regressions.jsonl
python3 tools/run_benchmarks.py
python3 tools/qchi_lyx_lint.py --root .
```

## 6) Conformance checks (host-agnostic)
```bash
bash scripts/run_conformance.sh ~/Documents/QCHI-Projects/<project-id> <project-id>
```

## 7) Local learning dashboard
```bash
bash scripts/run_learning_dashboard.sh
```
Open `http://127.0.0.1:8787/dashboard/`
