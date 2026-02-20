# Learning Project Layout

Use project-scoped learning stores.

## Structure
- `skills/qchi/learning/projects/<project-id>/physics/`
- `skills/qchi/learning/projects/<project-id>/writing/`
- `skills/qchi/learning/projects/<project-id>/coding-plotting/`

Each track directory should contain
- `runs.jsonl`
- `evals.jsonl`
- `regressions.jsonl`
- `heuristics.yaml`

## Scope rules
- keep reusable domain-agnostic heuristics in shared core only after promotion gates pass
- keep project-specific heuristics inside the relevant project track
- do not mix unrelated projects in one log file

## Naming
- project id format: `proj-<short-name>-<yyyy>`
- run id format: `run-<utc>-<seq>`
- eval id format: `eval-<utc>-<seq>`
