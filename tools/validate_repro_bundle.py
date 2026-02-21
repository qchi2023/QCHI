#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

REQ_ROLE_FILES = [
    "roles/source-miner.md",
    "roles/derivation.md",
    "roles/verifier.md",
    "roles/referee.md",
]

TRACKS = ["physics", "writing", "coding-plotting"]


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--project-id", required=True)
    args = ap.parse_args()

    root = Path(args.project_root)
    pid = args.project_id
    errors = []

    notes = root / "artifacts" / "lyx" / "notes.lyx"
    plots = root / "artifacts" / "lyx" / "systematics_plots.lyx"
    if not notes.exists():
        errors.append("missing artifacts/lyx/notes.lyx")
    if not plots.exists():
        errors.append("missing artifacts/lyx/systematics_plots.lyx")

    reports = root / "artifacts" / "reports"
    compliance = reports / "compliance.json"
    repro_manifest = reports / "repro_manifest.json"

    if not compliance.exists():
        errors.append("missing artifacts/reports/compliance.json")
    else:
        cj = load_json(compliance)
        if not cj:
            errors.append("invalid JSON in compliance.json")
        else:
            if str(cj.get("status", "")).lower() != "pass":
                errors.append("compliance.json status is not pass")

    if not repro_manifest.exists():
        errors.append("missing artifacts/reports/repro_manifest.json")
    else:
        rj = load_json(repro_manifest)
        if not rj:
            errors.append("invalid JSON in repro_manifest.json")
        else:
            mappings = rj.get("equation_source_mappings", [])
            if not isinstance(mappings, list) or len(mappings) == 0:
                errors.append("repro_manifest missing equation_source_mappings")

    for rel in REQ_ROLE_FILES:
        p = reports / rel
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"missing or empty artifacts/reports/{rel}")

    learn_root = root / "skills" / "qchi" / "learning" / "projects" / pid
    for t in TRACKS:
        tdir = learn_root / t
        if not tdir.exists():
            errors.append(f"missing learning track dir: {tdir}")
            continue
        for f in ["runs.jsonl", "heuristics.yaml"]:
            fp = tdir / f
            if not fp.exists():
                errors.append(f"missing learning file: {fp}")

    if errors:
        print("FAIL conformance bundle")
        for e in errors:
            print(f"- {e}")
        return 1

    print("PASS conformance bundle")
    return 0


if __name__ == "__main__":
    sys.exit(main())
