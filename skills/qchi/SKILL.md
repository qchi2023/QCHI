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
- Unfinished project mode (default when user says "work on project X")
- Physics solve mode
- Paper reproduction mode (mandatory multi-agent by default)
- Parameter-space/plot mode
- Publishable draft mode
- Multi-agent orchestration mode

Paper reproduction enforcement
- paper reproduction must use multi-agent orchestration unless user explicitly requests single-agent
- required roles: source-miner, derivation, verifier, referee
- if required roles are not present, stop and emit policy failure instead of continuing

See `references/WORKFLOW_MODES.md` and `references/PAPER_REPRO_FLOW.md`.
For reliability and verification enforcement, also use:
- `references/RELIABILITY_TARGETS.md`
- `references/MULTI_PATH_VERIFICATION.md`
- `references/COST_RELIABILITY_POLICY.md`
- `references/KNOWLEDGE_SOURCES_POLICY.md`
- `references/KNOWLEDGE_ACQUISITION_WORKFLOW.md`
- `references/NOTEBOOKLM_INTEGRATION.md`
- `references/MULTI_AGENT_ORCHESTRATION.md`
- `references/AGENT_MESSAGE_SCHEMA.yaml`
- `references/ROLE_TEMPLATES.md`
- `references/EQUATION_PROVENANCE_LEDGER.md`
- `references/ASSUMPTION_DEBT_TRACKER.md`
- `references/REPRO_MANIFEST_SCHEMA.md`
- `references/REFEREE_RUBRIC.md`
- `references/DOMAIN_PLAYBOOK_OQS.md`
- `references/DOMAIN_PLAYBOOK_MBCM.md`
- `references/DOMAIN_PLAYBOOK_QI.md`
- `references/NOTEBOOKLM_SOURCE_MAPPING.md`
- `references/PROMOTION_GATES.md`
- `references/REGRESSION_SUITE.md`
- `references/UNFINISHED_PROJECT_MODE.md`
- `references/ADAPTER_CONTRACT.md`
- `references/LYX_DIRECT_AUTHORING_PROTOCOL.md`
- `references/LYX_DOCS_INDEX.md`
- `references/PROJECT_ARTIFACT_LAYOUT.md`.

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