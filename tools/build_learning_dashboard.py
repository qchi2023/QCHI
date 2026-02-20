#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
LEARNING = ROOT / "skills" / "qchi" / "learning"
OUTDIR = ROOT / "dashboard"
OUTDIR.mkdir(exist_ok=True)


def read_jsonl(path: Path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            rows.append({"_parse_error": True, "raw": line})
    return rows


def load_yaml_like(path: Path):
    # keep dependency-free; return raw text for now
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def project_summary(project_dir: Path):
    tracks = {}
    for track in ["physics", "writing", "coding-plotting"]:
        tdir = project_dir / track
        tracks[track] = {
            "runs": read_jsonl(tdir / "runs.jsonl"),
            "evals": read_jsonl(tdir / "evals.jsonl"),
            "regressions": read_jsonl(tdir / "regressions.jsonl"),
            "heuristics_yaml": load_yaml_like(tdir / "heuristics.yaml"),
        }
    return tracks


data = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "global": {
        "runs": read_jsonl(LEARNING / "runs.jsonl"),
        "evals": read_jsonl(LEARNING / "evals.jsonl"),
        "regressions": read_jsonl(LEARNING / "regressions.jsonl"),
        "heuristics_yaml": load_yaml_like(LEARNING / "heuristics.yaml"),
    },
    "projects": {},
}

projects_root = LEARNING / "projects"
if projects_root.exists():
    for p in sorted(projects_root.iterdir()):
        if not p.is_dir() or p.name.startswith("."):
            continue
        data["projects"][p.name] = project_summary(p)

(OUTDIR / "learning_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Wrote {(OUTDIR / 'learning_data.json')}")
