# CHANGELOG

## 2026-02-20
- Consolidated on `qchi` as canonical skill.
- Removed deprecated `skills/qchi-top-layer` variant.
- Hardened `KNOWLEDGE_SOURCES_POLICY.md` with license/access gates and source-record template.
- Added LyX policy constraints:
  - no `:` in `.lyx` output by default
  - mandatory labels for equation/figure/table/section
  - mandatory `\ref` usage for internal references
- Added machine-first learning store:
  - `skills/qchi/learning/runs.jsonl`
  - `skills/qchi/learning/evals.jsonl`
  - `skills/qchi/learning/regressions.jsonl`
  - `skills/qchi/learning/heuristics.yaml`
- Added Rust lint scaffold `tools/qchi-lint` and CI workflow `.github/workflows/qchi-lint.yml`.
- Added adapter compliance reference `references/ADAPTER_CONTRACT.md`.

## 2026-02-17
- Initialized portable top-layer repo structure.
- Added baseline README and workflow rules.
- Added canonical spec and template placeholders.
- Refactored QCHI to methodology-only skill model (removed non-physics Python tooling from skill package).
