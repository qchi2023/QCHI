# Adapter Contract (v1)

All host adapters must satisfy this contract.

## Input contract
- receive user task verbatim
- preserve QCHI mode selection
- pass through required constraints

## Output contract
Must emit these sections in order
1. Problem framing
2. Assumptions and regime
3. Governing equations
4. Derivation
5. Validation checks
6. Final result
7. Interpretation and confidence
8. Claim provenance
9. References

## Failure contract
- if a required capability is unavailable, state limitation explicitly
- do not fabricate formulas or references
- include fallback verification plan

## Compliance checklist
- [ ] required sections present
- [ ] provenance tags present
- [ ] uncertainty handling present when needed
- [ ] no host-specific leakage in final artifact
