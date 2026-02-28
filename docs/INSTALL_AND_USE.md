# Install and Use QCHI

This repo contains a portable skill core at `skills/qchi/`.

## Required programs
- See also `docs/INSTALL_PREREQS.md` for OS install commands.

Minimum
- `git`
- `python3` (for validators and utility scripts)

Recommended
- `rust` + `cargo` (to build `tools/qchi-lint`)
- `LyX` (for direct `.lyx` authoring workflow)

Host runtime (choose one)
- OpenClaw
- Codex
- Claude Code
- Cursor
- Antigravity
- OpenCode

## A) OpenClaw install

1. Package status
- This repo currently has prebuilt skill artifacts under `dist/`
- Canonical source is `skills/qchi/`
- If you need a fresh `.skill` artifact, use your OpenClaw packaging workflow/tooling on `skills/qchi/`

2. Install in OpenClaw
- Import a `.skill` artifact in OpenClaw, or install from the `skills/qchi/` source according to your OpenClaw setup

3. Use
- Ask tasks that match the skill scope, for example
  - "work on unfinished project X"
  - "reproduce arXiv:XXXX.XXXXX"
  - "run parameter-space analysis for ..."

## Quick bootstrap for Ubuntu + OpenCode

```bash
bash scripts/bootstrap_opencode_ubuntu.sh
```

See `docs/HOST_COMMANDS.md` for host-by-host quick commands.

## QCHI CLI usage
Run the orchestrator directly from this repo:

```bash
python3 bin/qchi doctor --host gemini
python3 bin/qchi run --host gemini --mode physics_solve --task "derive harmonic oscillator normalization"
python3 bin/qchi lint report --file templates/OUTPUT_TEMPLATE.md
python3 bin/qchi version
```

By default, `qchi run` writes run artifacts to `.qchi/runs/<task_id>/` (role outputs, attempt logs, final summary).
Set `--run-artifacts-dir <path>` or `QCHI_RUN_ARTIFACTS_DIR` to change the artifact root.

Legacy compatibility: `python3 bin/qchi --mode ... --task ...` is still accepted and maps to `qchi run`.

## B) Generic host use (Codex, Claude Code, Cursor, Antigravity)

1. Use canonical instructions from
- `skills/qchi/SKILL.md`
- `skills/qchi/references/`

2. Apply host adapter notes from
- `skills/qchi/adapters/openclaw.md`
- `skills/qchi/adapters/cursor.md`
- `skills/qchi/adapters/antigravity.md`
- `skills/qchi/adapters/opencode.md`
- `skills/qchi/adapters/generic.md`

3. Keep learning logs in
- `skills/qchi/learning/`
- `skills/qchi/learning/projects/<project-id>/...`

## C) Expected behavior defaults
- Full serious mode by default
- Paper reproduction defaults to multi-agent unless user asks single-agent
- `publishable_draft.lyx` only when explicitly requested
- Direct `.lyx` writing workflow only

## D) Verification
- CI workflow: `.github/workflows/qchi-lint.yml`
- Rust lint scaffold: `tools/qchi-lint/`
- Project-learning layout validator: `tools/validate_project_learning.py`
- Benchmark suite validator: `tools/run_benchmarks.py`
- LyX lint engine: `tools/qchi_lyx_lint.py`

## E) Learning visibility
Local dashboard
```bash
bash scripts/run_learning_dashboard.sh
```
Then open `http://127.0.0.1:8787/dashboard/`
