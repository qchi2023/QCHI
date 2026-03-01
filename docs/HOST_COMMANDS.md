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

## 2b) QCHI CLI (multi-agent orchestrator)
```bash
python3 bin/qchi doctor --host gemini
python3 bin/qchi run --host gemini --mode physics_solve --task "your task here"
python3 bin/qchi lint report --file templates/OUTPUT_TEMPLATE.md
python3 bin/qchi regression sweep --suite skills/qchi/learning/benchmarks/baseline_v1.json
python3 bin/qchi dashboard build
python3 bin/qchi dashboard serve --port 8787
python3 bin/qchi version
```

Run artifacts are saved by default under `.qchi/runs/<task_id>/`.
Override artifact root with `--run-artifacts-dir <path>` or `QCHI_RUN_ARTIFACTS_DIR`.
Use `--host-timeout-sec <seconds>` to prevent stalled host subprocess calls from blocking forever.
Learning runs are appended by default to `skills/qchi/learning/runs.jsonl`.
Use `--project-id` and optional `--learning-track` for project-scoped run logs.
Use `qchi regression sweep --results-file <json>` for full-suite scoring from recorded case results, or `--execute` to run cases through the orchestrator.

## 3) OpenClaw
OpenClaw CLI commands
```bash
openclaw gateway status
openclaw gateway start
openclaw gateway restart
```

Install QCHI skill into OpenClaw workspace
```bash
mkdir -p ~/.openclaw/workspace/skills
rsync -a skills/qchi/ ~/.openclaw/workspace/skills/qchi/
openclaw skills check
openclaw skills list --eligible
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
python3 tools/run_benchmarks.py --results-file /path/to/sweep_results.json --min-runs 10
python3 tools/qchi_lyx_lint.py --root .
```

## 6) Conformance checks (host-agnostic)
```bash
bash scripts/run_conformance.sh ~/Documents/QCHI-Projects/<project-id> <project-id>
```

## 7) Local learning dashboard
```bash
python3 bin/qchi dashboard serve --port 8787
```
Open `http://127.0.0.1:8787/dashboard/`
Use the Track Trends controls to switch metric and 14/30/90-day rolling windows for each project track.
