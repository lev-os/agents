#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def try_run(cmd: list[str], cwd: Path) -> str | None:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout


def normalize_labels(labels: object) -> list[str]:
    if isinstance(labels, list):
        out: list[str] = []
        for item in labels:
            if isinstance(item, dict):
                name = item.get("name")
                if name:
                    out.append(str(name))
            elif isinstance(item, str):
                out.append(item)
        return out
    return []


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def best_beads_timestamp(obj: dict[str, object]) -> str:
    for key in ("closed_at", "updated_at", "created_at"):
        value = obj.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def beads_rows(repo: Path) -> list[dict[str, object]]:
    path = repo / ".beads" / "issues.jsonl"
    if not path.exists():
        return []
    rows_by_id: dict[str, tuple[dict[str, object], tuple[str, int]]] = {}
    malformed_lines = 0
    conflict_marker_lines = 0
    anonymous_rows: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        if line.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            conflict_marker_lines += 1
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            malformed_lines += 1
            continue

        row = {
            "id": obj.get("id") or "",
            "title": obj.get("title") or "",
            "status": obj.get("status") or "",
            "closed_at": obj.get("closed_at") or obj.get("updated_at") or "",
            "kind": obj.get("issue_type") or "",
            "url": "",
            "labels": obj.get("labels") or [],
            "source": "beads",
        }
        issue_id = str(row["id"])
        if not issue_id:
            anonymous_rows.append(row)
            continue

        candidate_key = (best_beads_timestamp(obj), line_number)
        existing = rows_by_id.get(issue_id)
        if existing is None or candidate_key >= existing[1]:
            rows_by_id[issue_id] = (row, candidate_key)

    if conflict_marker_lines:
        warn(
            f"skipped {conflict_marker_lines} merge-conflict marker lines while parsing {path}"
        )
    if malformed_lines:
        warn(f"skipped {malformed_lines} malformed JSONL lines while parsing {path}")

    rows = [row for row, _ in rows_by_id.values()]
    rows.sort(
        key=lambda row: (
            str(row.get("closed_at") or ""),
            str(row.get("id") or ""),
        ),
        reverse=True,
    )
    return rows + anonymous_rows


def github_rows(repo: Path, state: str, limit: int) -> list[dict[str, object]]:
    out = try_run(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "all" if state == "all" else state,
            "--limit",
            str(limit),
            "--json",
            "number,title,state,closedAt,labels,url",
        ],
        repo,
    )
    if not out:
        return []
    raw = json.loads(out)
    rows: list[dict[str, object]] = []
    for item in raw:
        rows.append(
            {
                "id": f"#{item.get('number')}",
                "title": item.get("title") or "",
                "status": item.get("state") or "",
                "closed_at": item.get("closedAt") or "",
                "kind": "issue",
                "url": item.get("url") or "",
                "labels": normalize_labels(item.get("labels")),
                "source": "github",
            }
        )
    return rows


def linear_rows(path: Path) -> list[dict[str, object]]:
    raw = json.loads(path.read_text())
    items = raw if isinstance(raw, list) else raw.get("issues") or raw.get("nodes") or []
    rows: list[dict[str, object]] = []
    for item in items:
        state = item.get("state")
        labels = item.get("labels")
        if isinstance(labels, dict):
            labels = labels.get("nodes")
        rows.append(
            {
                "id": item.get("identifier") or item.get("id") or "",
                "title": item.get("title") or item.get("name") or "",
                "status": state.get("name") if isinstance(state, dict) else state or "",
                "closed_at": item.get("completedAt") or item.get("canceledAt") or item.get("updatedAt") or "",
                "kind": "linear",
                "url": item.get("url") or "",
                "labels": normalize_labels(labels),
                "source": "linear",
            }
        )
    return rows


def jira_rows(path: Path) -> list[dict[str, object]]:
    raw = json.loads(path.read_text())
    items = raw.get("issues") if isinstance(raw, dict) else raw
    rows: list[dict[str, object]] = []
    for item in items:
        fields = item.get("fields", {}) if isinstance(item, dict) else {}
        status = fields.get("status", {})
        rows.append(
            {
                "id": item.get("key") or item.get("id") or "",
                "title": fields.get("summary") or item.get("title") or "",
                "status": status.get("name") if isinstance(status, dict) else status or "",
                "closed_at": fields.get("resolutiondate") or fields.get("updated") or "",
                "kind": "jira",
                "url": item.get("self") or "",
                "labels": normalize_labels(fields.get("labels")),
                "source": "jira",
            }
        )
    return rows


def milestone_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current = "unsectioned"
    for idx, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        bullet = re.match(r"^\s*[-*]\s+(?:\[(x|X| )\]\s+)?(.+)$", line)
        if not bullet:
            continue
        done = bullet.group(1)
        title = bullet.group(2).strip()
        rows.append(
            {
                "id": f"{path.stem}:{idx}",
                "title": title,
                "status": "closed" if done and done.lower() == "x" else "open",
                "closed_at": "",
                "kind": current,
                "url": "",
                "labels": [],
                "source": "milestones",
            }
        )
    return rows


def auto_kind(repo: Path, input_path: Path | None) -> str:
    if input_path:
        if input_path.suffix.lower() == ".md":
            return "milestones"
        if input_path.suffix.lower() == ".json":
            text = input_path.read_text()
            if '"identifier"' in text or '"completedAt"' in text:
                return "linear"
            if '"fields"' in text and '"resolutiondate"' in text:
                return "jira"
    if (repo / ".beads" / "issues.jsonl").exists():
        return "beads"
    if try_run(["gh", "repo", "view", "--json", "nameWithOwner"], repo):
        return "github"
    return "unknown"


def filter_rows(rows: list[dict[str, object]], state: str) -> list[dict[str, object]]:
    if state == "all":
        return rows
    want = state.lower()
    out = []
    for row in rows:
        status = str(row.get("status") or "").lower()
        if want == "closed" and status in {"closed", "done", "completed"}:
            out.append(row)
        elif want == "open" and status not in {"closed", "done", "completed"}:
            out.append(row)
    return out


def markdown(rows: list[dict[str, object]]) -> str:
    lines = ["## Workstreams", ""]
    for row in rows:
        label = f"[`{row['id']}`]({row['url']})" if row.get("url") else f"`{row['id']}`"
        suffix = f" — {row['closed_at']}" if row.get("closed_at") else ""
        lines.append(f"- {label} {row['title']} [{row['source']}] {suffix}".rstrip())
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--input", help="path to tracker export file")
    parser.add_argument("--kind", default="auto", choices=["auto", "beads", "github", "linear", "jira", "milestones"])
    parser.add_argument("--state", default="closed", choices=["closed", "open", "all"])
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--format", default="json", choices=["json", "markdown"])
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    input_path = Path(args.input).resolve() if args.input else None
    kind = args.kind if args.kind != "auto" else auto_kind(repo, input_path)

    if kind == "beads":
        rows = beads_rows(repo)
    elif kind == "github":
        rows = github_rows(repo, args.state, args.limit)
    elif kind == "linear":
        if not input_path:
            raise SystemExit("--input is required for linear exports")
        rows = linear_rows(input_path)
    elif kind == "jira":
        if not input_path:
            raise SystemExit("--input is required for jira exports")
        rows = jira_rows(input_path)
    elif kind == "milestones":
        if not input_path:
            raise SystemExit("--input is required for milestone markdown")
        rows = milestone_rows(input_path)
    else:
        raise SystemExit("could not determine tracker kind; pass --kind explicitly")

    rows = filter_rows(rows, args.state)
    rows = rows[: args.limit]

    if args.format == "markdown":
        print(markdown(rows), end="")
    else:
        print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
