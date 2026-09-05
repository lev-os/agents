#!/usr/bin/env python3
"""Compile auto-enrich depth flags and validate companion session traces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


POLICIES = {
    "simple": {
        "mode": "simple",
        "companion_required": False,
        "max_interview_turns": 0,
        "review_cycles": 0,
        "hard_max_cycles": 0,
        "semantic_review": "host_once",
    },
    "standard": {
        "mode": "standard",
        "companion_required": True,
        "max_interview_turns": 1,
        "review_cycles": 1,
        "hard_max_cycles": 1,
        "semantic_review": "companion",
    },
    "deep": {
        "mode": "deep",
        "companion_required": True,
        "max_interview_turns": 12,
        "review_cycles": 2,
        "hard_max_cycles": 5,
        "semantic_review": "companion",
    },
}


def compile_policy(
    mode: str,
    cycles: int | None = None,
    interview_turns: int | None = None,
    max_cycles: int | None = None,
) -> dict[str, object]:
    policy = dict(POLICIES[mode])
    if max_cycles is not None:
        minimum = 0 if mode == "simple" else 1
        if max_cycles < minimum or max_cycles > int(policy["hard_max_cycles"]):
            raise ValueError(f"max cycles must be between {minimum} and {policy['hard_max_cycles']} for {mode}")
        policy["hard_max_cycles"] = max_cycles
    if cycles is not None:
        if mode == "simple" and cycles != 0:
            raise ValueError("simple mode forbids companion review cycles")
        minimum = 0 if mode == "simple" else 1
        if cycles < minimum or cycles > int(policy["hard_max_cycles"]):
            raise ValueError(f"cycles must be between {minimum} and {policy['hard_max_cycles']} for {mode}")
        policy["review_cycles"] = cycles
    if int(policy["review_cycles"]) > int(policy["hard_max_cycles"]):
        raise ValueError("review cycles cannot exceed max cycles")
    if interview_turns is not None:
        if interview_turns < 0 or interview_turns > int(policy["max_interview_turns"]):
            raise ValueError(f"interview turns must be between 0 and {policy['max_interview_turns']} for {mode}")
        policy["max_interview_turns"] = interview_turns
    return policy


def validate_trace(policy: dict[str, object], trace_path: Path) -> dict[str, object]:
    events = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()] if trace_path.exists() else []
    companion = [event for event in events if event.get("kind") == "companion_invocation"]
    session_ids = {event.get("session_id") for event in companion if event.get("session_id")}
    required = bool(policy["companion_required"])
    checks = {
        "simple_has_zero_companion_invocations": required or len(companion) == 0,
        "companion_invoked_when_required": (not required) or len(companion) >= 1,
        "one_explicit_session": (not required) or len(session_ids) == 1,
        "every_invocation_has_session": all(event.get("session_id") for event in companion),
    }
    return {
        "mode": policy["mode"],
        "passed": all(checks.values()),
        "checks": checks,
        "companion_invocations": len(companion),
        "session_ids": sorted(session_ids),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=sorted(POLICIES), default="standard")
    parser.add_argument("--cycles", type=int)
    parser.add_argument("--max-cycles", type=int)
    parser.add_argument("--max-interview-turns", type=int)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    try:
        policy = compile_policy(args.mode, args.cycles, args.max_interview_turns, args.max_cycles)
    except ValueError as error:
        print(json.dumps({"error": str(error), "mode": args.mode}))
        return 2
    result = {"policy": policy}
    if args.trace is not None:
        result["trace_validation"] = validate_trace(policy, args.trace)
    print(json.dumps(result, indent=2))
    return 0 if result.get("trace_validation", {}).get("passed", True) else 1


if __name__ == "__main__":
    sys.exit(main())
