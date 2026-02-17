#!/usr/bin/env python3
import argparse
from pathlib import Path

REQUIRED_HEADERS = [
    "problem framing",
    "assumptions and regime",
    "governing equations",
    "derivation",
    "validation checks",
    "final result",
    "interpretation and confidence",
    "claim provenance",
    "references",
]


def main():
    p = argparse.ArgumentParser(description="Validate required QCHI-R output sections")
    p.add_argument("--input", required=True, help="markdown file to validate")
    args = p.parse_args()

    text = Path(args.input).read_text().lower()
    missing = [h for h in REQUIRED_HEADERS if h not in text]
    if missing:
        print("MISSING:" + ",".join(missing))
        raise SystemExit(2)
    print("PASS")


if __name__ == "__main__":
    main()
