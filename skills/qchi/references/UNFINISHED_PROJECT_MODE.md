# Unfinished Project Mode (Default)

## Trigger
When user says: "work on project X" (or equivalent), enter this mode.

## Behavior
- Work diligently on project X end-to-end.
- Continue until completion gate is reached or a true blocker appears.
- Use full multi-agent orchestration (subagents) to decompose and verify tasks.

## Execution contract
1. Load project context/files.
2. Identify missing pieces.
3. Complete missing pieces in practical order.
4. Validate against quality and reliability gates.
5. Produce finished artifacts/draft state.

## Stop conditions
- Completion gate reached.
- Hard blocker requiring user input.

## Reporting style
- Concise progress updates.
- Focus on completed work, blockers, and next concrete step.
