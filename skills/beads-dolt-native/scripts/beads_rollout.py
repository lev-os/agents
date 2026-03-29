#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SHARED_PORT = "3308"
SHARED_HOST = "127.0.0.1"


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=check,
        env={**os.environ, "BEADS_DOLT_SHARED_SERVER": "1"},
    )


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "repo"


def discover_repos(roots: list[Path]) -> list[Path]:
    repos: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for meta in root.glob("**/.beads/metadata.json"):
            repo = meta.parent.parent
            repos.add(repo.resolve())
    return sorted(repos)


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def git_remote(repo: Path) -> str:
    proc = run(["git", "config", "--get", "remote.origin.url"], cwd=repo, check=False)
    return proc.stdout.strip()


def derive_db_name(repo: Path) -> str:
    remote = git_remote(repo)
    basis = remote or str(repo)
    base = slugify(Path(remote.rstrip("/")).stem if remote else repo.name)
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:6]
    return f"beads_{base}_{digest}"


def upsert_line(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    needle = f"{key}:"
    replaced = False
    for idx, line in enumerate(lines):
        if line.strip().startswith(needle):
            lines[idx] = f"{key}: {value}"
            replaced = True
    if not replaced:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"{key}: {value}")
    return "\n".join(lines).rstrip() + "\n"


def patch_config(repo: Path) -> None:
    config_path = repo / ".beads" / "config.yaml"
    text = config_path.read_text() if config_path.exists() else ""
    text = upsert_line(text, "dolt.mode", "server")
    text = upsert_line(text, "dolt.shared-server", "true")
    text = upsert_line(text, "dolt.host", SHARED_HOST)
    text = upsert_line(text, "dolt.port", SHARED_PORT)
    config_path.write_text(text)


def apply_repo(repo: Path, *, sync_mode: str) -> dict[str, Any]:
    db_name = derive_db_name(repo)
    patch_config(repo)
    steps: list[dict[str, Any]] = []

    for cmd in (
        ["bd", "dolt", "set", "database", db_name, "--update-config"],
        ["bd", "dolt", "set", "host", SHARED_HOST, "--update-config"],
        ["bd", "dolt", "set", "port", SHARED_PORT, "--update-config"],
        ["bd", "dolt", "start"],
    ):
        proc = run(cmd, cwd=repo, check=False)
        steps.append({"cmd": cmd, "code": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})

    if sync_mode == "push":
        proc = run(["bd", "dolt", "push"], cwd=repo, check=False)
        steps.append({"cmd": ["bd", "dolt", "push"], "code": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})
    elif sync_mode == "pull":
        proc = run(["bd", "dolt", "pull"], cwd=repo, check=False)
        steps.append({"cmd": ["bd", "dolt", "pull"], "code": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})

    show = run(["bd", "dolt", "show", "--json"], cwd=repo, check=False)
    ready = run(["bd", "ready", "--json"], cwd=repo, check=False)
    return {
        "repo": str(repo),
        "database": db_name,
        "sync_mode": sync_mode,
        "steps": steps,
        "show_ok": show.returncode == 0,
        "show": show.stdout.strip() or show.stderr.strip(),
        "ready_ok": ready.returncode == 0,
        "ready_excerpt": (ready.stdout.strip() or ready.stderr.strip())[:1200],
    }


def scan_repo(repo: Path) -> dict[str, Any]:
    meta = read_json(repo / ".beads" / "metadata.json")
    cfg = (repo / ".beads" / "config.yaml").read_text() if (repo / ".beads" / "config.yaml").exists() else ""
    return {
        "repo": str(repo),
        "remote": git_remote(repo),
        "current_database": meta.get("dolt_database"),
        "current_port": meta.get("dolt_server_port"),
        "target_database": derive_db_name(repo),
        "has_shared_server_flag": "dolt.shared-server: true" in cfg,
        "has_shared_port": f"dolt.port: {SHARED_PORT}" in cfg,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Roll out one Beads Dolt-native playbook across many repos.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("scan", "apply"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--roots", nargs="+", required=True)
        if name == "apply":
            sub.add_argument("--sync", choices=["none", "push", "pull"], default="none")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    roots = [Path(root).expanduser().resolve() for root in args.roots]
    repos = discover_repos(roots)

    if args.command == "scan":
        print(json.dumps({"count": len(repos), "repos": [scan_repo(repo) for repo in repos]}, indent=2))
        return 0

    results = [apply_repo(repo, sync_mode=args.sync) for repo in repos]
    print(json.dumps({"count": len(results), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
