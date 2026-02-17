# Portability Plan

## Core principle
Keep one canonical core (`skills/qchi-r`) and small host adapters.

## Core package
Contains:
- behavior contract
- workflow protocol
- output template
- quality gate checklist
- citation/provenance rules

## Host adapters
- `adapters/openclaw.md`
- `adapters/antigravity.md`
- `adapters/cursor.md`
- `adapters/opencode.md`
- `adapters/generic.md`

Each adapter defines:
- where to place files
- how to trigger behavior
- capability limits
- fallback rules

## Packaging targets
1. OpenClaw `.skill`
2. Generic zip bundle
3. Plain markdown import pack
