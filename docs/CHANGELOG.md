# CHANGELOG

## 2026-02-20
- Consolidated on `qchi` as canonical skill and removed deprecated `skills/qchi-top-layer` variant.
- Hardened `KNOWLEDGE_SOURCES_POLICY.md` with license/access gates and source-record template.
- Added LyX policy constraints:
  - no `:` in `.lyx` output by default
  - mandatory labels for equation/figure/table/section
  - mandatory `\ref` usage for internal references
  - direct `.lyx` authoring protocol
- Added local LyX manuals for grounding under `skills/qchi/references/lyx-docs/`.
- Added machine-first learning store:
  - `skills/qchi/learning/runs.jsonl`
  - `skills/qchi/learning/evals.jsonl`
  - `skills/qchi/learning/regressions.jsonl`
  - `skills/qchi/learning/heuristics.yaml`
- Added project-scoped learning layout with required tracks:
  - `physics`
  - `writing`
  - `coding-plotting`
- Added validators and CI gates:
  - `tools/validate_project_learning.py`
  - `tools/run_benchmarks.py`
  - `tools/qchi_lyx_lint.py`
  - `.github/workflows/qchi-lint.yml`
- Added benchmark suite scaffold: `skills/qchi/learning/benchmarks/baseline_v1.json`.
- Added local learning dashboard:
  - `tools/build_learning_dashboard.py`
  - `scripts/run_learning_dashboard.sh`
  - `dashboard/index.html`
- Added installation and host operations docs:
  - `docs/INSTALL_AND_USE.md`
  - `docs/INSTALL_PREREQS.md`
  - `docs/HOST_COMMANDS.md`
- Added bootstrap and helper scripts:
  - `scripts/bootstrap_opencode_ubuntu.sh`
  - `scripts/host_help.sh`
  - `tools/check_env.sh`

## 2026-02-17
- Initialized portable top-layer repo structure.
- Added baseline README and workflow rules.
- Added canonical spec and template placeholders.
- Refactored QCHI to methodology-only skill model (removed non-physics Python tooling from skill package).
