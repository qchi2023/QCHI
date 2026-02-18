# Knowledge Acquisition Workflow

## Objective
Continuously expand QCHI-R knowledge sources with minimal user friction.

## Source collection behavior
1. Skill/agent actively searches for high-value sources in target domains.
2. If a source is accessible without paywall, download and register it directly.
3. If a source is behind paywall, add it to a paywalled queue for user-provided file ingestion.

## Division of work
- Agent/skill:
  - discover sources
  - collect freely accessible files
  - draft metadata entries
  - keep source index updated
- User:
  - provide files for paywalled items only

## Intake folders
- `knowledge/books/inbox/` for new files
- `knowledge/books/processed/` for normalized files
- `knowledge/books/paywalled_queue.yaml` for missing paywalled items

## Metadata fields (required)
- id
- title
- author
- year
- topic_tags
- source_url_or_path
- access_type (`free` | `paywalled_user_provided`)
- status (`inbox` | `processed` | `indexed`)

## Update cycle
1. Discover new sources
2. Download free sources
3. Register paywalled queue items
4. Ingest user-provided paywalled files
5. Rebuild knowledge index
6. Log additions in change log
