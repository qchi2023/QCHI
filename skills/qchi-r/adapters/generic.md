# Generic Adapter

For any chat/model host:
1. Set system prompt from `templates/SYSTEM_PROMPT.md`.
2. Paste output contract from `templates/OUTPUT_TEMPLATE.md`.
3. Draft response in markdown.
4. Validate response sections:
   - `python3 scripts/quality_gate_check.py --input <response.md>`
5. After accepted work, run learning loop update scripts.
