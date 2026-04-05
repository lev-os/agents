#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

from autoresearch_helpers import (
    AutoresearchError,
    default_checkpoint_lock_path,
    resolve_repo_path,
    utc_now,
)
from autoresearch_launch_gate import pid_is_alive


def read_lock_payload(lock_path: Path) -> dict[str, Any] | None:
    if not lock_path.exists():
        return None
    try:
        payload = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AutoresearchError(f"Invalid checkpoint lock JSON in {lock_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AutoresearchError(f"Invalid checkpoint lock payload in {lock_path}: expected an object")
    return payload


def lock_status(lock_path: Path) -> dict[str, Any]:
    payload = read_lock_payload(lock_path)
    if payload is None:
        return {"status": "free", "lock_path": str(lock_path)}
    pid = payload.get("pid")
    stale = isinstance(pid, int) and not pid_is_alive(pid)
    return {
        "status": "stale" if stale else "held",
        "lock_path": str(lock_path),
        "payload": payload,
    }


def acquire_lock(
    *,
    lock_path: Path,
    run_tag: str,
    pid: int,
    wait_seconds: float,
    poll_seconds: float,
) -> dict[str, Any]:
    deadline = time.time() + max(wait_seconds, 0.0)
    payload = {
        "run_tag": run_tag,
        "pid": pid,
        "created_at": utc_now(),
    }

    while True:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            status = lock_status(lock_path)
            current = status.get("payload", {})
            if status["status"] == "stale":
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                continue
            if current.get("run_tag") == run_tag and current.get("pid") == pid:
                return {
                    "status": "already-held",
                    "lock_path": str(lock_path),
                    "payload": current,
                }
            if time.time() >= deadline:
                return {
                    "status": "busy",
                    "lock_path": str(lock_path),
                    "payload": current,
                }
            time.sleep(max(poll_seconds, 0.1))
            continue

        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        return {
            "status": "acquired",
            "lock_path": str(lock_path),
            "payload": payload,
        }


def release_lock(
    *,
    lock_path: Path,
    run_tag: str | None,
    force: bool,
) -> dict[str, Any]:
    payload = read_lock_payload(lock_path)
    if payload is None:
        return {"status": "free", "lock_path": str(lock_path)}
    if not force and run_tag and payload.get("run_tag") not in {run_tag, ""}:
        return {
            "status": "owned-by-other",
            "lock_path": str(lock_path),
            "payload": payload,
        }
    lock_path.unlink(missing_ok=True)
    return {
        "status": "released",
        "lock_path": str(lock_path),
        "payload": payload,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coordinate git checkpointing across multiple autoresearch runs in one repo."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--repo", required=True)
    shared.add_argument("--lock-path")

    status = subparsers.add_parser("status", parents=[shared])

    acquire = subparsers.add_parser("acquire", parents=[shared])
    acquire.add_argument("--run-tag", required=True)
    acquire.add_argument("--pid", type=int, default=os.getpid())
    acquire.add_argument("--wait-seconds", type=float, default=0.0)
    acquire.add_argument("--poll-seconds", type=float, default=2.0)

    release = subparsers.add_parser("release", parents=[shared])
    release.add_argument("--run-tag")
    release.add_argument("--force", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo = resolve_repo_path(args.repo)
    lock_path = Path(args.lock_path).resolve() if args.lock_path else default_checkpoint_lock_path(repo)

    if args.command == "status":
        print(json.dumps(lock_status(lock_path), indent=2, sort_keys=True))
        return 0
    if args.command == "acquire":
        result = acquire_lock(
            lock_path=lock_path,
            run_tag=args.run_tag,
            pid=args.pid,
            wait_seconds=args.wait_seconds,
            poll_seconds=args.poll_seconds,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] in {"acquired", "already-held"} else 2
    if args.command == "release":
        print(
            json.dumps(
                release_lock(
                    lock_path=lock_path,
                    run_tag=args.run_tag,
                    force=args.force,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    raise AutoresearchError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AutoresearchError as exc:
        raise SystemExit(f"error: {exc}")
