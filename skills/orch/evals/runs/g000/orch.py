#!/usr/bin/env python3
"""Small stdlib-only state machine for the orch skill POC."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATUSES = {"ready", "running", "blocked", "complete", "paused"}
BRANCH_STATUSES = {"pending", "running", "blocked", "complete", "deferred"}
OUTCOMES = {"progress", "no_change", "blocked", "decision_needed", "complete"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"state not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON state: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("state root must be an object")
    return value


def save(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def validate(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("version", "goal", "root", "mode", "status", "branches", "scheduler"):
        if key not in state:
            errors.append(f"missing {key}")
    if state.get("version") != 1:
        errors.append("version must be 1")
    if not isinstance(state.get("goal"), str) or not state.get("goal", "").strip():
        errors.append("goal must be non-empty text")
    if state.get("status") not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")
    branches = state.get("branches")
    if not isinstance(branches, list) or not branches:
        errors.append("branches must be a non-empty list")
    else:
        ids: list[str] = []
        for index, branch in enumerate(branches):
            if not isinstance(branch, dict):
                errors.append(f"branch {index} must be an object")
                continue
            branch_id = branch.get("id")
            if not isinstance(branch_id, str) or not branch_id:
                errors.append(f"branch {index} has no id")
            elif branch_id in ids:
                errors.append(f"duplicate branch id: {branch_id}")
            else:
                ids.append(branch_id)
            if branch.get("status") not in BRANCH_STATUSES:
                errors.append(f"branch {branch_id or index} has invalid status")
            if not isinstance(branch.get("owner"), str) or not branch.get("owner"):
                errors.append(f"branch {branch_id or index} has no owner")
        known = set(ids)
        for branch in branches:
            if isinstance(branch, dict):
                for dependency in branch.get("needs", []) or []:
                    if dependency not in known:
                        errors.append(f"branch {branch.get('id', '?')} needs unknown branch {dependency}")
    scheduler = state.get("scheduler")
    if not isinstance(scheduler, dict):
        errors.append("scheduler must be an object")
    elif not re.fullmatch(r"(?:[1-9][0-9]*)(?:m|h)", str(scheduler.get("northstar_interval", ""))):
        errors.append("scheduler.northstar_interval must look like 30m or 1h")
    return errors


def cmd_plan(args: argparse.Namespace) -> int:
    routes = args.route or ["skill://lev"]
    branches = [
        {
            "id": "root" if len(routes) == 1 else f"route-{index + 1}",
            "outcome": args.goal if len(routes) == 1 else f"{args.goal} ({route})",
            "owner": route,
            "needs": [],
            "effects": ["read"],
            "verifier": "controller inspection",
            "stop": "failed gate, named decision, or verified completion",
            "status": "pending",
        }
        for index, route in enumerate(routes)
    ]
    by_id = {branch["id"]: branch for branch in branches}
    for declaration in args.need:
        branch_id, separator, dependencies = declaration.partition("=")
        if not separator or branch_id not in by_id:
            print(f"invalid --need: {declaration}", file=sys.stderr)
            return 2
        by_id[branch_id]["needs"] = [item for item in dependencies.split(",") if item]
    state = {
        "version": 1,
        "goal": args.goal,
        "root": str(Path(args.root).expanduser().resolve()),
        "mode": args.mode,
        "status": "ready",
        "branches": branches,
        "scheduler": {
            "northstar_interval": args.interval,
            "orchestrator_interval": None,
            "dedupe_key": f"{args.goal}:{args.mode}",
        },
        "blockers": [],
        "decisions": [],
        "evidence": [],
        "tick": 0,
        "created_at": now(),
        "updated_at": now(),
    }
    errors = validate(state)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    save(Path(args.state).expanduser(), state)
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


def cmd_tick(args: argparse.Namespace) -> int:
    path = Path(args.state).expanduser()
    state = load(path)
    errors = validate(state)
    if errors:
        print("invalid state: " + "; ".join(errors), file=sys.stderr)
        return 2
    branch = next((item for item in state["branches"] if item["id"] == args.branch), None)
    if branch is None:
        print(f"unknown branch: {args.branch}", file=sys.stderr)
        return 2
    outcome = args.outcome
    branch["status"] = {
        "progress": "complete" if args.complete else "running",
        "no_change": "running",
        "blocked": "blocked",
        "decision_needed": "deferred",
        "complete": "complete",
    }[outcome]
    event = {"at": now(), "branch": args.branch, "outcome": outcome, "note": args.note or ""}
    state.setdefault("evidence", []).append(event)
    if outcome == "blocked":
        state.setdefault("blockers", []).append({"branch": args.branch, "note": args.note or ""})
        state["status"] = "blocked"
    elif outcome == "decision_needed":
        state.setdefault("decisions", []).append({"branch": args.branch, "question": args.note or ""})
        state["status"] = "paused"
    elif outcome == "complete" or args.complete:
        if all(item["status"] in {"complete", "deferred"} for item in state["branches"]):
            state["status"] = "complete"
        else:
            state["status"] = "running"
    else:
        state["status"] = "running"
    state["tick"] += 1
    state["updated_at"] = now()
    save(path, state)
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = load(Path(args.state).expanduser())
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate(load(Path(args.state).expanduser()))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("valid")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="orch", description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--goal", required=True)
    plan.add_argument("--root", default=".")
    plan.add_argument("--mode", choices=("plan", "auto", "execute", "monitor"), default="plan")
    plan.add_argument("--route", action="append")
    plan.add_argument("--need", action="append", default=[], help="branch=dependency[,dependency]")
    plan.add_argument("--interval", default="30m")
    plan.add_argument("--state", default=".lev/orch-state.json")
    plan.set_defaults(func=cmd_plan)
    tick = sub.add_parser("tick")
    tick.add_argument("--state", required=True)
    tick.add_argument("--branch", required=True)
    tick.add_argument("--outcome", choices=sorted(OUTCOMES), required=True)
    tick.add_argument("--note")
    tick.add_argument("--complete", action="store_true")
    tick.set_defaults(func=cmd_tick)
    status = sub.add_parser("status")
    status.add_argument("--state", required=True)
    status.set_defaults(func=cmd_status)
    check = sub.add_parser("validate")
    check.add_argument("--state", required=True)
    check.set_defaults(func=cmd_validate)
    return root


if __name__ == "__main__":
    parsed = parser().parse_args()
    raise SystemExit(parsed.func(parsed))
