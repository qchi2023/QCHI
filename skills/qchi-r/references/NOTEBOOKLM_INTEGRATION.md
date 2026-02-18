# NotebookLM Integration

## Purpose
Allow QCHI-R workflows to use NotebookLM as a knowledge workspace for source-grounded reasoning.

## Usage model
- Use NotebookLM as an external context/retrieval surface for books, papers, and notes.
- Treat NotebookLM outputs as draft evidence that must still pass QCHI-R quality gates.

## Required workflow
1. Ingest sources into NotebookLM notebooks by topic/domain.
2. Query NotebookLM for summaries, citation trails, and cross-document links.
3. Re-run QCHI-R derivation + validation checks on retrieved claims.
4. Tag claim provenance and record source mapping.

## Guardrails
- Do not accept NotebookLM output without QCHI-R verification checks.
- Preserve claim provenance labels.
- For high-impact claims, require symbolic/numeric verification regardless of NotebookLM confidence.

## Recommended notebook structure
- OQS
- Many-body condensed matter
- Quantum information
- Math methods / techniques
- Reproduction case notebooks
