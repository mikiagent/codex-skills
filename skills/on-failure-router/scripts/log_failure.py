#!/usr/bin/env python3
"""Append a structured failure record to a JSONL feedback log."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append one Codex Skill failure record to JSONL.")
    parser.add_argument("--log", default=".codex-skill-feedback/failures.jsonl")
    parser.add_argument("--complaint", required=True)
    parser.add_argument("--task", default="")
    parser.add_argument("--skills", default="", help="Comma-separated Skill names")
    parser.add_argument("--observed", default="")
    parser.add_argument("--expected", default="")
    parser.add_argument("--cause", default="")
    parser.add_argument("--owner", default="")
    parser.add_argument("--changed", default="", help="Comma-separated changed files")
    parser.add_argument("--validation", default="")
    parser.add_argument("--outcome", default="open", choices=["open", "fixed", "partial", "unresolved"])
    return parser.parse_args()


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    args = parse_args()
    path = Path(args.log).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "complaint": args.complaint,
        "task": args.task,
        "skills": split_csv(args.skills),
        "observed_failure": args.observed,
        "expected_behavior": args.expected,
        "verified_cause": args.cause,
        "owning_layer": args.owner,
        "changed_files": split_csv(args.changed),
        "validation": args.validation,
        "outcome": args.outcome,
    }

    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Logged failure record to {path}")


if __name__ == "__main__":
    main()
