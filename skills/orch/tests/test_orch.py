#!/usr/bin/env python3
"""Minimal behavioral checks for the orch POC CLI."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "orch.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        check=False,
        text=True,
        capture_output=True,
    )


def main() -> int:
    skill = (ROOT / "SKILL.md").read_text()
    for phrase in (
        "startup_blocker",
        "The worker that changes an artifact does not certify it",
        "Use scheduling tools available in the environment",
        "skill://coder",
        "skill://lev",
        "skill://eval-builder",
    ):
        assert phrase in skill, f"missing contract: {phrase}"
    with tempfile.TemporaryDirectory() as directory:
        state = Path(directory) / "state.json"
        planned = run(
            "plan",
            "--goal",
            "prove routing",
            "--root",
            directory,
            "--mode",
            "auto",
            "--route",
            "skill://research",
            "--route",
            "skill://lev-plan",
            "--need",
            "route-2=route-1",
            "--state",
            str(state),
        )
        assert planned.returncode == 0, planned.stderr
        assert run("validate", "--state", str(state)).stdout.strip() == "valid"
        ticked = run(
            "tick",
            "--state",
            str(state),
            "--branch",
            "route-1",
            "--outcome",
            "decision_needed",
            "--note",
            "choose owner",
        )
        assert ticked.returncode == 0, ticked.stderr
        data = json.loads(state.read_text())
        assert data["status"] == "paused"
        assert data["decisions"][0]["question"] == "choose owner"
        assert data["branches"][1]["needs"] == ["route-1"]
    print("orch POC checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
