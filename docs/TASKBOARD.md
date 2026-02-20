# TASKBOARD

## In Progress
- [ ] Run first full regression sweep on real paper set provided by user
- [ ] Tune CPIS thresholds after baseline results

## Next
- [ ] Add richer adapter compliance test corpus
- [ ] Add auto-generated release notes from learning logs
- [ ] Add chart view to local dashboard (trend lines by project/track)

## Done
- [x] Consolidated on canonical `qchi` skill
- [x] Removed duplicate `qchi-top-layer` skill variant
- [x] Hardened knowledge source policy and license/access gates
- [x] Enforced LyX writing rules including no `:` default
- [x] Added mandatory label + `\ref` guidance for LyX artifacts
- [x] Added machine-first learning store (`learning/*.jsonl`, `heuristics.yaml`)
- [x] Added Rust `qchi-lint` scaffold and CI workflow
- [x] Added adapter contract reference
- [x] Added benchmark suite scaffold and CI validation (`tools/run_benchmarks.py`)
- [x] Added LyX lint engine and CI hook (`tools/qchi_lyx_lint.py`)
- [x] Added local learning dashboard (`dashboard/`, `scripts/run_learning_dashboard.sh`)
- [x] Added host helper scripts/docs (`scripts/host_help.sh`, `docs/HOST_COMMANDS.md`)
