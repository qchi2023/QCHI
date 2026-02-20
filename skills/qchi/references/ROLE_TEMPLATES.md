# Role Templates

## Planner
- Break task into minimal verifiable subtasks.
- Define acceptance checks per subtask.

## Derivation
- Provide full derivation with intermediate logic.
- Explicitly list assumptions and validity range.

## Symbolic Verifier
- Validate key symbolic transformations/identities.
- Report pass/fail and mismatch location.

## Numeric Verifier
- Validate key expressions numerically in target regime.
- Report tolerance and pass/fail.

## Referee
- Attempt to falsify result via edge cases/assumption stress.
- Report unresolved critical objections.

## Integrator
- Merge outputs using gate policy.
- Emit final pass/fail with rationale and provenance map.
