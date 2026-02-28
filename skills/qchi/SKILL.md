---
name: qchi
description: QCHI portable, host-agnostic research operating layer for rigorous theoretical-physics work. Use for derivation-first problem solving, paper reproduction, LyX-first artifact workflows, parameter-space studies, plot quality gates, and publication-ready claim provenance with arXiv-first references.
---

# QCHI

This is the canonical portable layer. Host adapters live under `adapters/`.

## Required output sections
1. Problem framing
2. Assumptions and regime
3. Governing equations
4. Derivation
5. Validation checks
6. Final result
7. Interpretation and confidence
8. Claim provenance
9. References

Use: `templates/OUTPUT_TEMPLATE.md`.

## Mandatory rules
- Analytical-first when feasible.
- No fabricated formulas/citations.
- Must run: units, limiting-case, asymptotic, and consistency checks.
- For analytical claims, run symbolic verification (Mathematica preferred, SymPy fallback) per `references/SYMBOLIC_VERIFICATION_POLICY.md`.
- Tag key claims as REPRODUCED_FROM_SOURCE / INFERRED_ASSUMPTION / NEW_EXTENSION.
- If uncertain, disclose uncertainty + verification plan.
- Continuous learning loop is required after meaningful work:
  1) log failure patterns
  2) extract/update heuristics
  3) run evals
  4) keep changes only if eval quality improves

## Research modes
All modes require multi-agent orchestration (subagents) to execute:
- Unfinished project mode (default when user says "work on project X")
- Physics solve mode
- Paper reproduction mode
- Parameter-space/plot mode
- Publishable draft mode

Enforcement
- execution must always use multi-agent orchestration
- required roles: planner, derivation, verifier, referee, integrator (and source-miner for reproduction)
- if required roles are not present, stop and emit policy failure instead of continuing
- reproduction coverage must include all in-scope equations not only key equations
- derivation must include full intermediate steps for in-scope equations not summary-only results
- LyX workflow is mandatory: initialize artifact files from `skills/qchi/references/LYX_MINIMAL_TEMPLATE.lyx` (or `tools/init_lyx_artifacts.sh`) before writing content
- if LyX export check fails, run is failed regardless of textual summary quality

## LyX Direct Authoring Cheat Sheet
Because you must write directly to `.lyx` files, you MUST use the following raw LyX markup structures. NEVER output standard Markdown or raw LaTeX blocks inside a LyX file.

### 1. Standard Paragraph
```text
\layout Standard
This is regular text.
```

### 2. Section Heading
```text
\layout Section
\begin_inset CommandInset label
LatexCommand label
name "sec:Introduction"
\end_inset

Introduction Header
```

### 3. Inline Math
```text
\begin_inset Formula $E=mc^{2}$
\end_inset
```

### 4. Display Equation (with Label)
```text
\begin_inset Formula 
\begin{equation}
H|\psi\rangle=E|\psi\rangle\label{eq:schrodinger}
\end{equation}
\end_inset
```

### 5. Cross-Reference
```text
As seen in Equation 
\begin_inset CommandInset ref
LatexCommand ref
reference "eq:schrodinger"
\end_inset
```

**CRITICAL LYX RULES:**
1. A `.lyx` file must start with `#LyX 2.4 created this file.`
2. You must balance every `\begin_inset` with an `\end_inset`.
3. Never use a colon (`:`) in regular text unless explicitly requested by the user.

See `references/LYX_DIRECT_AUTHORING_PROTOCOL.md` and `references/LYX_MINIMAL_TEMPLATE.lyx`.

## Quality gate
Before finalizing, pass all checks in `checklists/QUALITY_GATE.md`.

## Continuous learning loop operations
After meaningful work:
1. Record run and failures in machine logs.
2. Promote validated heuristics only after regression pass.
3. Run evals (including repeated-run reliability checks).
4. Track cost vs reliability.
5. Keep/revert behavior change based on eval + stability + CPIS criteria.

Learning store (machine-first):
- `learning/runs.jsonl`
- `learning/evals.jsonl`
- `learning/regressions.jsonl`
- `learning/heuristics.yaml`
- `learning/README.md`
- project-scoped layout: `references/LEARNING_PROJECT_LAYOUT.md`

Learning tracks required in each project:
1. physics
2. writing
3. coding-plotting

See:
- `references/LEARNING_LOOP_PROTOCOL.md`
- `references/RELIABILITY_TARGETS.md`
- `references/COST_RELIABILITY_POLICY.md`
- `references/REGRESSION_SUITE.md`

## Knowledge acquisition operations
For knowledge source growth:
1. Discover and collect freely accessible sources directly.
2. Queue paywalled sources for user-provided files.
3. Register all additions via manifest templates.
4. Rebuild index and log updates.
5. Integrate and query NotebookLM notebooks for source-grounded retrieval.

Use:
- `references/KNOWLEDGE_ACQUISITION_WORKFLOW.md`
- `references/BOOKS_MANIFEST_TEMPLATE.yaml`
- `references/PAYWALLED_QUEUE_TEMPLATE.yaml`
- `references/NOTEBOOKLM_INTEGRATION.md`

Note: This skill is methodology-only. Python/Julia are for physics calculations, not for skill plumbing.