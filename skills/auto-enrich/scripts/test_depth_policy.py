#!/usr/bin/env python3
"""Outcome tests for auto-enrich depth and companion persistence policy."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from depth_policy import compile_policy, validate_trace


FAKE_CODER = """#!/usr/bin/env python3
import json, pathlib, sys
trace = pathlib.Path(sys.argv[1])
action = sys.argv[2]
session = "companion-session-1" if action == "start" else sys.argv[3]
with trace.open("a") as handle:
    handle.write(json.dumps({"kind":"companion_invocation","action":action,"session_id":session}) + "\\n")
print(session)
"""


def exercise(policy: dict[str, object], turns: int) -> tuple[Path, tempfile.TemporaryDirectory]:
    temporary = tempfile.TemporaryDirectory()
    root = Path(temporary.name)
    runner = root / "coder"
    runner.write_text(FAKE_CODER)
    runner.chmod(0o755)
    trace = root / "trace.jsonl"
    if policy["companion_required"]:
        session = subprocess.check_output([str(runner), str(trace), "start"], text=True).strip()
        for _ in range(max(0, turns - 1)):
            resumed = subprocess.check_output([str(runner), str(trace), "resume", session], text=True).strip()
            if resumed != session:
                raise AssertionError("fake coder changed companion session")
    return trace, temporary


class DepthPolicyOutcomeTest(unittest.TestCase):
    def test_skill_routes_transport_to_coder_without_launch_recipes(self) -> None:
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        text = skill.read_text()
        for required in (
            "--simple", "--standard", "--deep", "skill://coder",
            "one explicit session id reused", "Read-only Companion Transport",
        ):
            self.assertIn(required, text)
        self.assertNotIn("## Companion Launch Forms", text)
        self.assertNotIn("claude --safe-mode --print", text)
        self.assertNotIn("codex exec --ignore-user-config", text)

        coder = Path(__file__).resolve().parents[2] / "coder/SKILL.md"
        coder_text = coder.read_text()
        for required in (
            "## Read-only Companion Transport", "umask 077", "unique `mktemp -d`",
            "PTY for Codex", "no PTY for Claude", "exit 124 is failure",
            "verify no child remains", "remove temporary", "Never use recency",
        ):
            self.assertIn(required, coder_text)

    def test_simple_launches_no_companion(self) -> None:
        for options in ({}, {"cycles": 0}, {"max_cycles": 0}, {"interview_turns": 0}, {"cycles": 0, "max_cycles": 0, "interview_turns": 0}):
            with self.subTest(options=options):
                policy = compile_policy("simple", **options)
                trace, temporary = exercise(policy, turns=3)
                self.addCleanup(temporary.cleanup)
                result = validate_trace(policy, trace)
                self.assertTrue(result["passed"])
                self.assertEqual(result["companion_invocations"], 0)

    def test_standard_reuses_one_session(self) -> None:
        policy = compile_policy("standard")
        trace, temporary = exercise(policy, turns=2)
        self.addCleanup(temporary.cleanup)
        result = validate_trace(policy, trace)
        self.assertTrue(result["passed"])
        self.assertEqual(result["session_ids"], ["companion-session-1"])

    def test_deep_reuses_one_session_across_many_turns(self) -> None:
        policy = compile_policy("deep")
        trace, temporary = exercise(policy, turns=5)
        self.addCleanup(temporary.cleanup)
        result = validate_trace(policy, trace)
        self.assertTrue(result["passed"])
        self.assertEqual(result["companion_invocations"], 5)
        self.assertEqual(result["session_ids"], ["companion-session-1"])

    def test_trace_rejects_session_replacement(self) -> None:
        policy = compile_policy("deep")
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("\n".join([
                json.dumps({"kind": "companion_invocation", "session_id": "one"}),
                json.dumps({"kind": "companion_invocation", "session_id": "two"}),
            ]) + "\n")
            self.assertFalse(validate_trace(policy, trace)["passed"])

    def test_simple_rejects_companion_budget(self) -> None:
        with self.assertRaises(ValueError):
            compile_policy("simple", cycles=1)
        with self.assertRaises(ValueError):
            compile_policy("simple", max_cycles=1)
        with self.assertRaises(ValueError):
            compile_policy("simple", interview_turns=1)

    def test_companion_modes_require_at_least_one_cycle(self) -> None:
        for mode in ("standard", "deep"):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                compile_policy(mode, cycles=0)

    def test_deep_max_cycles_bounds_review_cycles(self) -> None:
        self.assertEqual(compile_policy("deep", cycles=3, max_cycles=3)["hard_max_cycles"], 3)
        with self.assertRaises(ValueError):
            compile_policy("deep", cycles=3, max_cycles=2)


if __name__ == "__main__":
    unittest.main()
