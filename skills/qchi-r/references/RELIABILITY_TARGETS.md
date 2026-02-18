# Reliability Targets

QCHI-R target is not "correct once"; it is "hard to get wrong."

## Core KPI
- **Cannot-Play-Incorrectly Score (CPIS)**
  - CPIS = fraction of repeated runs that pass quality gate + correctness threshold.
  - Minimum target for promotion: **CPIS >= 0.90** over at least 10 runs.

## Stability thresholds
- Mean score delta vs baseline must be >= configured `min_delta`.
- Score spread (`max-min`) must be <= configured `max_spread`.
- Score standard deviation must be <= configured `max_stddev`.

## Promotion rule
A behavior change is accepted only if:
1. Mean quality improves vs baseline
2. Stability thresholds pass
3. No critical regression appears in repeated runs

Else revert and log failure pattern.
