# Learning Loop Protocol (Core Priority)

This is the highest-priority long-term behavior for QCHI.

## Loop (always-on)
1. Solve task with full rigor contract.
2. Record failures and near-misses.
3. Convert repeated patterns into heuristics.
4. Run evaluation set before/after changes.
5. Keep behavior updates only when eval deltas improve quality.
6. Log what changed and why.

## Required artifacts
- `failure_patterns.md`
- `heuristics.md`
- `evals.md`
- `change_log.md`

## Guardrails
- No claims of "learning" without logs + eval evidence.
- No heuristic promotion without at least one regression check.
- If eval degrades, revert the behavior change.
