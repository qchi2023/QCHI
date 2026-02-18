# Symbolic Verification Policy

For analytical physics work, symbolic verification is mandatory when feasible.

## Preferred verifier
1. Mathematica (preferred for symbolic checks)
2. SymPy (fallback)

## Required flow
1. Produce analytical derivation in QCHI-R format.
2. Verify key symbolic steps/identities with Mathematica when available.
3. If Mathematica unavailable, use SymPy and mark verifier used.
4. For numerically relevant claims, run Python/Julia cross-checks.
5. Record verifier outputs and discrepancies in provenance notes.

## Acceptance rule
A high-impact analytical claim is accepted only if:
- symbolic verification passes, and
- no unresolved contradiction remains with numeric checks.

If mismatch exists:
- block claim promotion,
- log failure pattern,
- add heuristic only after resolved.
