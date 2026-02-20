#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

TRACKS = ["physics", "writing", "coding-plotting"]
REQUIRED = ["runs.jsonl", "evals.jsonl", "regressions.jsonl", "heuristics.yaml"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="skills/qchi/learning/projects")
    args = p.parse_args()

    root = Path(args.root)
    if not root.exists():
      print(f"missing root: {root}")
      return 1

    projects = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if not projects:
      print("no project dirs yet; PASS bootstrap")
      return 0

    errors = []
    for proj in projects:
      for track in TRACKS:
        tdir = proj / track
        if not tdir.exists():
          errors.append(f"{proj}: missing track {track}")
          continue
        for f in REQUIRED:
          fp = tdir / f
          if not fp.exists():
            errors.append(f"{proj}/{track}: missing {f}")

    if errors:
      print("FAIL project learning layout")
      for e in errors:
        print(f"- {e}")
      return 1

    print("PASS project learning layout")
    return 0


if __name__ == "__main__":
    sys.exit(main())
