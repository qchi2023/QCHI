# Cost vs Reliability Policy

Track token/compute cost against reliability gain.

## For each verification protocol run, log:
- run_id
- protocol name
- tokens (or compute proxy)
- wall time
- pass/fail
- mean score
- CPIS

## Decision rule
- Keep expensive protocol only if reliability gain justifies cost.
- Prefer lower-cost protocol when reliability is equivalent.
- Never drop below minimum reliability thresholds to save cost.
