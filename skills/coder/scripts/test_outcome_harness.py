#!/usr/bin/env python3
"""Prove coder outcome oracles reject bad fixtures and accept good outcomes."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("run_outcome_eval.py")
SPEC = importlib.util.spec_from_file_location("coder_outcome_eval", MODULE_PATH)
assert SPEC and SPEC.loader
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)


class OutcomeHarnessTest(unittest.TestCase):
    def fixture(self, case: str):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        artifact_root = Path(temporary.name)
        root = artifact_root / "repo"
        root.mkdir()
        EVAL.init_repo(root)
        _, baseline = EVAL.SETUPS[case](root)
        EVAL.commit_fixture(root)
        output = artifact_root / "final.txt"
        return root, baseline, output

    def assert_red_then_green(self, case: str, solution: str) -> None:
        root, baseline, output = self.fixture(case)
        self.assertFalse(EVAL.oracle(case, root, baseline, output)["passed"])
        target = "slug.py" if case == "direct_slug" else "ports.py" if case == "project_rules" else "backoff.py"
        EVAL.write(root / target, solution)
        if case.startswith("sdd_"):
            EVAL.write(output, '{"coder_session":"c1","reviewer_session":"r1","review":"APPROVED"}\n')
        self.assertTrue(EVAL.oracle(case, root, baseline, output)["passed"])

    def test_direct_slug_red_then_green(self) -> None:
        self.assert_red_then_green(
            "direct_slug",
            "import re\n\ndef slug(value):\n    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')\n",
        )

    def test_project_rules_red_then_green(self) -> None:
        self.assert_red_then_green(
            "project_rules",
            "def parse_port(value):\n    try:\n        port = int(value)\n    except (TypeError, ValueError):\n        raise ValueError('invalid port')\n    if not 1 <= port <= 65535:\n        raise ValueError('invalid port')\n    return port\n",
        )

    def test_sdd_modes_red_then_green(self) -> None:
        solution = "def capped_backoff(attempt, base=2, cap=30):\n    if attempt < 0:\n        raise ValueError('attempt must be non-negative')\n    return min(base ** attempt, cap)\n"
        for case in ("sdd_checkpoint", "sdd_pair"):
            with self.subTest(case=case):
                self.assert_red_then_green(case, solution)

    def test_blocked_cases_require_typed_attention_and_clean_repo(self) -> None:
        for case in ("dead_account", "fable_unavailable"):
            with self.subTest(case=case):
                root, baseline, output = self.fixture(case)
                self.assertFalse(EVAL.oracle(case, root, baseline, output)["passed"])
                EVAL.write(output, '{"provider":"requested","profile":"unavailable","failure":"capacity","action":"human login"}\n')
                self.assertTrue(EVAL.oracle(case, root, baseline, output)["passed"])
                EVAL.write(root / "unexpected.txt", "mutation\n")
                self.assertFalse(EVAL.oracle(case, root, baseline, output)["passed"])


if __name__ == "__main__":
    unittest.main()
