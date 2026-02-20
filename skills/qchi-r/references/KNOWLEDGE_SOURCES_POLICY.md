# Knowledge Sources Policy

QCHI-R knowledge should come from both:
1. Continuous learning loop (failures/heuristics/evals)
2. Curated external sources (including books)

## Book Acquisition Rule
- Download books/materials that you found on internet.
- Prefer:
  - open textbooks
  - public-domain books
  - institution-licensed access
  - user-provided files/links
- Do NOT use pirated sources.

## Access & License Gate (mandatory)
For every source, record:
- `access_mode`: `open_web` | `public_domain` | `institutional` | `user_provided` | `unknown`
- `license_status`: `open` | `restricted` | `unknown`

Policy enforcement:
- If `access_mode=unknown` or `license_status=unknown`, queue for review before use.
- Do not use restricted content unless access is valid (institutional or user-provided file).

## Source Priority
1. arXiv and primary papers
2. authoritative textbooks/monographs
3. review articles

## Knowledge Ingestion Requirements
For each new source, record:
- title, author, edition/year
- source URL/path
- topic tags
- confidence/use scope
- access_mode
- license_status

### Source Record Template
```yaml
source_id: SRC-YYYYMMDD-001
title: "..."
authors: ["..."]
year: 20XX
edition: "..."
url_or_path: "..."
topic_tags: ["...", "..."]
use_scope: "background | derivation | validation"
confidence: "high | medium | low"
access_mode: "open_web | public_domain | institutional | user_provided | unknown"
license_status: "open | restricted | unknown"
provenance_tag: "REPRODUCED_FROM_SOURCE | INFERRED_ASSUMPTION | NEW_EXTENSION"
```

## Quality Guardrails
- Never elevate a claim from a single weak source.
- Cross-check key formulas/results against at least one independent source when possible.
- Mark uncertain or conflicting sources explicitly.

## CI/Review Guardrails
- Block merges if forbidden text appears (e.g., "Do use pirated sources").
- Block merges when required source metadata fields are missing.
- Require at least one provenance-tagged source record for non-trivial claims.
