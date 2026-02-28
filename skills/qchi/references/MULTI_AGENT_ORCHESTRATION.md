# Multi-Agent Orchestration Protocol

## Objective
Enable QCHI workflows to decompose hard physics tasks across specialized agents and merge results with strict verification gates.

## Agent roles
1. Planner Agent
   - decomposes task into subproblems
   - defines required checks and outputs
2. Derivation Agent
   - produces analytical derivation candidate
3. Symbolic Verifier Agent
   - checks symbolic steps (Mathematica preferred, SymPy fallback)
4. Numeric Verifier Agent
   - checks numeric consistency (Python/Julia)
5. Referee Agent
   - challenges assumptions/logic; tries to break result
6. Integrator Agent
   - merges outputs and decides pass/fail against gates

## Message contract (agent-to-agent)
Each handoff payload should include:
- task_id
- subtask_id
- assumptions
- required_outputs
- result_summary
- verification_status
- confidence
- provenance_tags
- blockers

## Gate policy
Integrator can promote a final result only if:
- derivation exists and is complete,
- symbolic verifier passes (or explicit justified defer),
- numeric verifier passes when applicable,
- referee reports no unresolved critical issue,
- quality gate checklist passes.

## Failure policy
If any critical gate fails:
- block promotion,
- log failure pattern,
- queue heuristic update candidate,
- require re-run before acceptance.

## Host adaptation note
All hosts (including Gemini CLI, Codex CLI, etc.) must utilize true sub-agents to enforce these roles. Sequential simulation in a single thread is no longer permitted; the task must be delegated to specialized sub-agents.
