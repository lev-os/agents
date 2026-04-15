#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "command failed")
    return result.stdout


def try_run(cmd: list[str], cwd: Path) -> str | None:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout


def git_tags(repo: Path) -> list[dict[str, str]]:
    out = run(
        [
            "git",
            "for-each-ref",
            "refs/tags",
            "--sort=creatordate",
            "--format=%(refname:short)\t%(creatordate:short)\t%(subject)",
        ],
        repo,
    )
    tags: list[dict[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        tags.append({"tag": parts[0], "date": parts[1], "subject": parts[2]})
    return tags


def github_repo_url(repo: Path) -> str | None:
    gh_out = try_run(["gh", "repo", "view", "--json", "url"], repo)
    if gh_out:
        try:
            return json.loads(gh_out)["url"]
        except Exception:
            pass

    remote = try_run(["git", "remote", "get-url", "origin"], repo)
    if not remote:
        return None

    remote = remote.strip()
    if remote.startswith("git@github.com:"):
        slug = remote.removeprefix("git@github.com:").removesuffix(".git")
        return f"https://github.com/{slug}"
    if remote.startswith("https://github.com/"):
        return remote.removesuffix(".git")
    return None


def github_repo_slug(repo: Path) -> str | None:
    gh_out = try_run(["gh", "repo", "view", "--json", "nameWithOwner"], repo)
    if gh_out:
        try:
            return json.loads(gh_out)["nameWithOwner"]
        except Exception:
            pass

    url = github_repo_url(repo)
    if url and url.startswith("https://github.com/"):
        return url.removeprefix("https://github.com/")
    return None


def github_releases(repo: Path) -> dict[str, dict[str, str]]:
    slug = github_repo_slug(repo)
    if not slug:
        return {}

    out = try_run(["gh", "api", f"repos/{slug}/releases?per_page=100"], repo)
    if not out:
        return {}

    try:
        rows = json.loads(out)
    except Exception:
        return {}

    releases: dict[str, dict[str, str]] = {}
    for row in rows:
        tag = row.get("tag_name") or row.get("tagName")
        if not tag:
            continue
        releases[tag] = {
            "date": (row.get("published_at") or row.get("publishedAt") or "")[:10],
            "url": row.get("html_url") or row.get("url") or "",
            "kind": "Draft release" if (row.get("draft") or row.get("isDraft")) else "Release",
            "name": row.get("name") or "",
        }
    return releases


def build_rows(repo: Path) -> list[dict[str, str]]:
    tags = git_tags(repo)
    releases = github_releases(repo)
    base_url = github_repo_url(repo)

    rows: list[dict[str, str]] = []
    for tag in tags:
        release = releases.get(tag["tag"])
        if release:
            row = {
                "version": tag["tag"],
                "kind": release["kind"],
                "date": release["date"] or tag["date"],
                "summary": tag["subject"] or release["name"],
                "url": release["url"],
            }
        else:
            url = f"{base_url}/tree/{tag['tag']}" if base_url else ""
            row = {
                "version": tag["tag"],
                "kind": "Tag",
                "date": tag["date"],
                "summary": tag["subject"],
                "url": url,
            }
        rows.append(row)
    rows.sort(key=lambda row: (row["date"], row["version"]))
    rows.reverse()
    return rows


def markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "## Version Timeline",
        "",
        "`Kind` distinguishes a published release from a plain git tag.",
        "",
        "| Version | Kind | Date | Summary |",
        "|---------|------|------|---------|",
    ]
    for row in rows:
        label = f"[`{row['version']}`]({row['url']})" if row["url"] else f"`{row['version']}`"
        lines.append(
            f"| {label} | {row['kind']} | {row['date']} | {row['summary']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="repository path")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="output format",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    rows = build_rows(repo)

    if args.format == "json":
        print(json.dumps(rows, indent=2))
    else:
        print(markdown(rows), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
