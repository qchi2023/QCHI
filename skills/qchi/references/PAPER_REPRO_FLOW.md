# Paper Reproduction Flow

## Enforcement
- default execution is multi-agent
- required roles
  1) source-miner
  2) derivation
  3) verifier
  4) referee
- if role set is incomplete and user did not explicitly request single-agent, stop with policy failure

## Flow
1. Map contribution and target outputs.
2. Build assumption inventory (explicit + inferred).
3. Re-derive key equations with intermediate steps.
4. Reproduce computational outputs.
5. Regenerate and compare figures/tables.
6. Run stress/sensitivity tests.
7. Report mismatches and root causes.
8. Mark optional extensions clearly.
9. Attach reproducibility appendix (env, versions, seeds).

Claim tags are mandatory for major outputs.
