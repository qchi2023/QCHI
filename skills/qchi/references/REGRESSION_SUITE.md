# Regression Suite Definition

Run this suite after any QCHI update.

## Baseline v1 cases
1. `oqs-lindblad-trace-preservation`
2. `mbcm-phase-sensitivity-sweep`
3. `qi-channel-capacity-sanity`
4. `paper-repro-mini-arxiv`

## Required logging
- Write per-case outcomes to `skills/qchi/learning/evals.jsonl`
- Write suite decision to `skills/qchi/learning/regressions.jsonl`

## Pass criteria
- no quality-gate failures
- no new critical referee failures
- no CPIS regression below threshold
- no drop in repeated-run stability on baseline v1

If regression fails: revert/update and log failure pattern.
