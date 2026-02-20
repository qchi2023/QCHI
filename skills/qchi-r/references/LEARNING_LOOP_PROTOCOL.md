# Learning Loop Protocol (Core Priority)

This is the highest-priority long-term behavior for QCHI.

## Loop (always-on)
1. Solve task with full rigor contract.
2. Record failures and near-misses.
3. Convert repeated patterns into heuristics.
4. Run evaluation set before/after changes.
5. Run repeated-eval stability checks and compute CPIS.
6. Track cost vs reliability gain for the protocol used.
7. Keep behavior updates only when eval/stability/CPIS criteria pass.
8. Log what changed and why.

## Required artifacts
Machine-first store
- `skills/qchi-r/learning/runs.jsonl`
- `skills/qchi-r/learning/evals.jsonl`
- `skills/qchi-r/learning/regressions.jsonl`
- `skills/qchi-r/learning/heuristics.yaml`

Optional human summaries
- `failure_patterns.md`
- `change_log.md`

## Guardrails
- No claims of "learning" without logs + eval evidence.
- No heuristic promotion without at least one regression check.
- If eval degrades, revert the behavior change.
