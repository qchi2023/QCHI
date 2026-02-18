# Multi-Path Verification Policy

For high-impact outputs, require at least two independent verification paths.

## Required paths (choose two or more)
1. Independent analytical derivation path
2. Numerical verification path (Python/Julia)
3. Symbolic checker path (SymPy/Mathematica-like tool)
4. Constraint/symmetry sanity path

## Acceptance
- Final claim is accepted only when paths agree within tolerance.
- If paths diverge, report mismatch and block claim promotion.
- Mismatch root-cause must be logged in failure patterns.
