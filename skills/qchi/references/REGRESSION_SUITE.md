# Regression Suite Definition

Run this suite after any QCHI update.

## Baseline v1 cases
Canonical suite file
- `skills/qchi/learning/benchmarks/baseline_v1.json`

Current baseline includes
1. `oqs-lindblad-trace-preservation`
2. `oqs-complete-positivity-sanity`
3. `mbcm-phase-sensitivity-sweep`
4. `mbcm-noise-robustness-scan`
5. `qi-channel-capacity-sanity`
6. `qi-entropy-bound-check`
7. `paper-repro-mini-arxiv`
8. `writing-technical-clarity-pass`
9. `writing-ref-integrity-pass`
10. `cross-domain-regression-guard`

## Required logging
- Write per-case outcomes to `skills/qchi/learning/evals.jsonl`
- Write suite decision to `skills/qchi/learning/regressions.jsonl`

## Pass criteria
- no quality-gate failures
- no new critical referee failures
- no CPIS regression below threshold
- no drop in repeated-run stability on baseline v1

If regression fails: revert/update and log failure pattern.
