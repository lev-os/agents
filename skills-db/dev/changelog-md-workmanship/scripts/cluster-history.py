#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


THEMES: dict[str, tuple[str, list[str]]] = {
    "sync": ("Sync, import/export, and merge behavior", ["sync", "jsonl", "import", "export", "merge", "flush", "conflict"]),
    "storage": ("Storage, schema, and database behavior", ["storage", "sqlite", "schema", "database", "db", "cache", "fsqlite"]),
    "cli": ("CLI command surface and workflow behavior", ["cli", "command", "list", "show", "close", "update", "ready", "blocked", "count", "stats"]),
    "testing": ("Testing, conformance, and benchmark coverage", ["test", "e2e", "conformance", "benchmark", "fixture", "harness"]),
    "output": ("Output modes, formatting, and serialization", ["output", "json", "toon", "format", "rich", "quiet", "markdown"]),
    "routing": ("Routing, MCP, and cross-project coordination", ["routing", "redirect", "external", "mcp", "agent", "id resolution"]),
    "reliability": ("Reliability, recovery, and workspace health", ["doctor", "recovery", "workspace", "quarantine", "snapshot", "failure", "health"]),
    "concurrency": ("Concurrency, contention, and blocked-cache correctness", ["concurrency", "lock", "blocked-cache", "contention", "busy", "stale"]),
    "performance": ("Performance and throughput work", ["perf", "optimiz", "throughput", "alloc", "lazy", "checkpoint"]),
    "release": ("Release, install, and CI plumbing", ["release", "workflow", "ci", "install", "binary", "checksum", "bump version"]),
    "docs": ("Docs, README, AGENTS, and changelog work", ["docs", "readme", "agents", "changelog"]),
}


def git_log(repo: Path, extra: list[str]) -> list[dict[str, str]]:
    cmd = ["git", "log", "--date=short", "--pretty=format:%H\t%ad\t%s", "--no-merges", *extra]
    result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git log failed")

    rows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        sha, date, subject = line.split("\t", 2)
        rows.append({"sha": sha, "date": date, "subject": subject})
    return rows


def classify(subject: str) -> str:
    lowered = subject.lower()
    best_theme = "general"
    best_score = 0
    for theme, (_, keywords) in THEMES.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        if score > best_score:
            best_theme = theme
            best_score = score
    return best_theme


def bucket_key(date_str: str, window: str) -> str:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if window == "month":
        return date.strftime("%Y-%m")
    return date.strftime("%Y-%m")


def cluster(rows: list[dict[str, str]], window: str) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        theme = classify(row["subject"])
        if theme == "general":
            continue
        buckets[(bucket_key(row["date"], window), theme)].append(row)

    clusters: list[dict[str, object]] = []
    for (bucket, theme), commits in buckets.items():
        if len(commits) < 2:
            continue
        commits.sort(key=lambda row: row["date"])
        title = THEMES[theme][0]
        clusters.append(
            {
                "bucket": bucket,
                "theme": theme,
                "title": title,
                "commit_count": len(commits),
                "start_date": commits[0]["date"],
                "end_date": commits[-1]["date"],
                "representative_commits": commits[-5:],
            }
        )
    clusters.sort(key=lambda row: (row["end_date"], row["commit_count"]), reverse=True)
    return clusters


def markdown(clusters: list[dict[str, object]]) -> str:
    lines = ["## Candidate Capability Waves", ""]
    for idx, cluster in enumerate(clusters, start=1):
        lines.append(
            f"### {idx}) {cluster['title']} ({cluster['bucket']}, {cluster['commit_count']} commits)"
        )
        lines.append("")
        lines.append(f"- Window: {cluster['start_date']} to {cluster['end_date']}")
        lines.append(f"- Suggested section title: {cluster['title']}")
        lines.append("- Representative commits:")
        for row in cluster["representative_commits"]:
            lines.append(f"  - `{row['sha'][:7]}` — {row['subject']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--range")
    parser.add_argument("--max-commits", type=int, default=300)
    parser.add_argument("--window", choices=["month"], default="month")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    extra: list[str] = []
    if args.range:
        extra.append(args.range)
    if args.since:
        extra.extend(["--since", args.since])
    if args.until:
        extra.extend(["--until", args.until])
    extra.extend(["-n", str(args.max_commits)])

    rows = git_log(repo, extra)
    clusters = cluster(rows, args.window)

    if args.format == "json":
        print(json.dumps(clusters, indent=2))
    else:
        print(markdown(clusters))
    return 0


if __name__ == "__main__":
    sys.exit(main())
