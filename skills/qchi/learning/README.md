# QCHI Learning Store

Machine-first persistence for continuous learning.

## Files
- `runs.jsonl` one record per execution run
- `evals.jsonl` one record per evaluated test case
- `regressions.jsonl` one record per suite-level regression decision
- `heuristics.yaml` curated promoted heuristics and status

## JSONL conventions
- UTF-8
- One valid JSON object per line
- No trailing comments
- Append-only, never rewrite historical lines
- Use ISO-8601 UTC timestamps

## Minimal run record
```json
{"run_id":"run-2026-02-20T19:10:00Z-001","ts":"2026-02-20T19:10:00Z","mode":"paper_reproduction","domain":"OQS","task_id":"arxiv:1234.5678v2:eq_12","quality_gate_pass":true,"cpis":0.93,"cost_tokens":4210,"status":"completed"}
```

## Minimal eval record
```json
{"eval_id":"eval-2026-02-20T19:12:00Z-001","ts":"2026-02-20T19:12:00Z","run_id":"run-2026-02-20T19:10:00Z-001","suite":"baseline-v1","case_id":"oqs-lindblad-trace-preservation","score":0.92,"pass":true,"regression":false}
```

## Minimal regression record
```json
{"regression_id":"reg-2026-02-20T19:15:00Z-001","ts":"2026-02-20T19:15:00Z","suite":"baseline-v1","before_commit":"abc1234","after_commit":"def5678","pass":true,"critical_failures":0,"decision":"promote"}
```
