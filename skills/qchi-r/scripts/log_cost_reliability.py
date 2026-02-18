#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Append cost vs reliability entry")
    p.add_argument("--file", default="cost_reliability_log.jsonl")
    p.add_argument("--run-id", required=True)
    p.add_argument("--protocol", required=True)
    p.add_argument("--tokens", type=int, required=True)
    p.add_argument("--seconds", type=float, required=True)
    p.add_argument("--pass-flag", required=True, choices=["true", "false"])
    p.add_argument("--mean-score", type=float, required=True)
    p.add_argument("--cpis", type=float, required=True)
    args = p.parse_args()

    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "run_id": args.run_id,
        "protocol": args.protocol,
        "tokens": args.tokens,
        "seconds": args.seconds,
        "pass": args.pass_flag == "true",
        "mean_score": args.mean_score,
        "cpis": args.cpis,
    }

    path = Path(args.file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    print(path)


if __name__ == "__main__":
    main()
