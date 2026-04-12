#!/usr/bin/env python3
"""
Mine session history for ritual patterns (prompts repeated 10+ times).

Usage:
    ./mine_rituals.py --workspace /data/projects/PROJECT
    ./mine_rituals.py --workspace /data/projects/PROJECT --min-count 5
    ./mine_rituals.py --workspace /data/projects/PROJECT --output rituals.json
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def run_cass_search(workspace: str, limit: int = 500) -> dict:
    """Run cass search and return JSON results."""
    cmd = [
        "cass", "search", "*",
        "--workspace", workspace,
        "--json",
        "--fields", "minimal",
        "--limit", str(limit)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running cass: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    return json.loads(result.stdout)


def extract_user_prompts(hits: list) -> list[str]:
    """Filter to user prompts (lines 1-3) and extract titles."""
    prompts = []
    for hit in hits:
        if hit.get("line_number", 999) <= 3:
            title = hit.get("title", "")[:80]  # Truncate for grouping
            if title:
                prompts.append(title)
    return prompts


def find_rituals(prompts: list[str], min_count: int = 10) -> list[dict]:
    """Find repeated prompts and return sorted by frequency."""
    counts = Counter(prompts)
    rituals = [
        {"prompt": prompt, "count": count}
        for prompt, count in counts.items()
        if count >= min_count
    ]
    return sorted(rituals, key=lambda x: -x["count"])


def main():
    parser = argparse.ArgumentParser(
        description="Mine session history for ritual patterns"
    )
    parser.add_argument(
        "--workspace", "-w",
        required=True,
        help="Workspace path to search"
    )
    parser.add_argument(
        "--min-count", "-m",
        type=int,
        default=10,
        help="Minimum occurrences to be considered a ritual (default: 10)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=500,
        help="Max sessions to search (default: 500)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for JSON results (default: stdout)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Searching {args.workspace}...", file=sys.stderr)

    # Run search
    results = run_cass_search(args.workspace, args.limit)
    hits = results.get("hits", [])
    total = results.get("total_matches", 0)

    if args.verbose:
        print(f"Found {total} total matches, processing {len(hits)}...", file=sys.stderr)

    # Extract and analyze
    prompts = extract_user_prompts(hits)
    rituals = find_rituals(prompts, args.min_count)

    # Output
    output = {
        "workspace": args.workspace,
        "total_sessions_searched": len(hits),
        "min_count_threshold": args.min_count,
        "rituals_found": len(rituals),
        "rituals": rituals
    }

    if args.output:
        Path(args.output).write_text(json.dumps(output, indent=2))
        print(f"Wrote {len(rituals)} rituals to {args.output}")
    else:
        print(json.dumps(output, indent=2))

    # Summary to stderr
    if args.verbose or not args.output:
        print("\n--- RITUAL SUMMARY ---", file=sys.stderr)
        print(f"Total rituals found: {len(rituals)}", file=sys.stderr)
        if rituals:
            print("\nTop 5 rituals:", file=sys.stderr)
            for r in rituals[:5]:
                print(f"  [{r['count']:3d}x] {r['prompt']}", file=sys.stderr)


if __name__ == "__main__":
    main()
