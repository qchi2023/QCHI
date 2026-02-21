# Register QCHI in OpenCode

OpenCode does not auto-register GitHub "skills" the same way OpenClaw does.

In OpenCode, registration means:
1. put the QCHI repo in a known local path
2. ensure project bootstrap instructions exist in `AGENTS.md`
3. open that project path in OpenCode

## One-command registration
```bash
bash scripts/register_opencode_qchi.sh
```

Default install path:
- `~/.local/share/opencode/skills/QCHI`

## After registration
Launch OpenCode on the registered path
```bash
opencode ~/.local/share/opencode/skills/QCHI
```

OpenCode should then follow project instructions from `AGENTS.md` and `skills/qchi/*`.

## Important note about "no skills installed"
That message refers to OpenCode's internal skill registry.
QCHI still works via project instructions even if that registry says none.

## Optional branch for testing
```bash
cd ~/.local/share/opencode/skills/QCHI
git checkout -B testing/opencode-v1
```
