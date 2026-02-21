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
0. Initialize LyX artifacts from template (`tools/init_lyx_artifacts.sh <project-root>`) and verify template opens/exports.
1. Map contribution and target outputs.
2. Build assumption inventory (explicit + inferred).
3. Enumerate all in-scope equations from the paper section set.
4. Re-derive all in-scope equations with intermediate steps.
5. Reproduce computational outputs.
6. Regenerate and compare figures/tables.
7. Run stress/sensitivity tests.
8. Report mismatches and root causes.
9. Mark optional extensions clearly.
10. Attach reproducibility appendix (env, versions, seeds).

## Coverage rule
- "key equations only" is not acceptable for reproduction mode.
- every equation in scope must be listed in the manifest and marked as derived or explicitly blocked with reason.

Claim tags are mandatory for major outputs.
