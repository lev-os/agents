from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_skill_invariants.py"


class CheckSkillInvariantsTest(unittest.TestCase):
    def run_invariant_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )

    def write_exec_repo(self, repo: Path) -> None:
        (repo / "research-results.tsv").write_text(
            "\n".join(
                [
                    "# metric_direction: lower",
                    "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription",
                    "0\tbase123\t10\t0\t-\tbaseline\tbaseline score",
                    "1\tkeep123\t8\t-2\tpass\tkeep\timproved score",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (repo / "autoresearch-lessons.md").write_text("# lessons\n", encoding="utf-8")

    def test_exec_expect_improvement_supports_higher_direction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "research-results.tsv").write_text(
                "\n".join(
                    [
                        "# metric_direction: higher",
                        "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription",
                        "0\tbase123\t10\t0\t-\tbaseline\tbaseline score",
                        "1\tkeep123\t12\t+2\tpass\tkeep\timproved score",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (repo / "autoresearch-lessons.md").write_text("# lessons\n", encoding="utf-8")

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--expect-improvement",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_reject_keep_rows_without_commit_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "research-results.tsv").write_text(
                "\n".join(
                    [
                        "# metric_direction: lower",
                        "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription",
                        "0\tbase123\t10\t0\t-\tbaseline\tbaseline score",
                        "1\t-\t8\t-2\tpass\tkeep\tinvalid keep row",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (repo / "autoresearch-lessons.md").write_text("# lessons\n", encoding="utf-8")

            completed = self.run_invariant_check("exec", "--repo", str(repo))

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("missing a commit hash", completed.stderr)

    def test_exec_invariants_reject_event_logs_without_bundled_helper_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_log = repo / "events.jsonl"
            (repo / "research-results.tsv").write_text(
                "\n".join(
                    [
                        "# metric_direction: lower",
                        "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription",
                        "0\tbase123\t10\t0\t-\tbaseline\tbaseline score",
                        "1\tkeep123\t8\t-2\tpass\tkeep\timproved score",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (repo / "autoresearch-lessons.md").write_text("# lessons\n", encoding="utf-8")
            event_log.write_text(
                'command: python3 scripts/autoresearch_init_run.py\n',
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--event-log",
                str(event_log),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("bundled helper scripts", completed.stderr)

    def test_exec_invariants_accept_bundled_helper_usage_in_event_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_log = repo / "events.jsonl"
            (repo / "research-results.tsv").write_text(
                "\n".join(
                    [
                        "# metric_direction: lower",
                        "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription",
                        "0\tbase123\t10\t0\t-\tbaseline\tbaseline score",
                        "1\tkeep123\t8\t-2\tpass\tkeep\timproved score",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (repo / "autoresearch-lessons.md").write_text("# lessons\n", encoding="utf-8")
            event_log.write_text(
                "\n".join(
                    [
                        'command: python3 .agents/skills/codex-autoresearch/scripts/autoresearch_init_run.py --mode exec',
                        'command: python3 .agents/skills/codex-autoresearch/scripts/autoresearch_record_iteration.py --status keep',
                        'command: python3 .agents/skills/codex-autoresearch/scripts/autoresearch_exec_state.py --cleanup',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--event-log",
                str(event_log),
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_accept_admin_scope_skill_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_log = repo / "events.jsonl"
            self.write_exec_repo(repo)
            event_log.write_text(
                "\n".join(
                    [
                        "command: python3 /etc/codex/skills/codex-autoresearch/scripts/autoresearch_init_run.py --mode exec",
                        "command: python3 /etc/codex/skills/codex-autoresearch/scripts/autoresearch_record_iteration.py --status keep",
                        "command: python3 /etc/codex/skills/codex-autoresearch/scripts/autoresearch_exec_state.py --cleanup",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--event-log",
                str(event_log),
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_accept_user_scope_skill_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_log = repo / "events.jsonl"
            self.write_exec_repo(repo)
            event_log.write_text(
                "\n".join(
                    [
                        "command: python3 /Users/alice/.agents/skills/codex-autoresearch/scripts/autoresearch_init_run.py --mode exec",
                        "command: python3 /Users/alice/.agents/skills/codex-autoresearch/scripts/autoresearch_record_iteration.py --status keep",
                        "command: python3 /Users/alice/.agents/skills/codex-autoresearch/scripts/autoresearch_exec_state.py --cleanup",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--event-log",
                str(event_log),
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_accept_absolute_configured_skill_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_log = repo / "events.jsonl"
            self.write_exec_repo(repo)
            event_log.write_text(
                "\n".join(
                    [
                        "command: python3 /opt/skills/codex-autoresearch/scripts/autoresearch_init_run.py --mode exec",
                        "command: python3 /opt/skills/codex-autoresearch/scripts/autoresearch_record_iteration.py --status keep",
                        "command: python3 /opt/skills/codex-autoresearch/scripts/autoresearch_exec_state.py --cleanup",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--event-log",
                str(event_log),
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_reject_non_json_last_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text("all done\n", encoding="utf-8")

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid JSON", completed.stderr)

    def test_exec_invariants_accept_json_completion_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                '{"status":"completed","baseline":10,"best":8,"best_iteration":1,'
                '"total_iterations":1,"keeps":1,"discards":0,"crashes":0,'
                '"improved":true,"exit_code":0}\n',
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
                "--expect-improvement",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_reject_completion_payload_with_stringified_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                '{"status":"completed","baseline":"10","best":"8","best_iteration":"1",'
                '"total_iterations":"1","keeps":"1","discards":"0","crashes":"0",'
                '"improved":true,"exit_code":0}\n',
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("field baseline must be a number", completed.stderr)

    def test_exec_invariants_reject_completion_payload_with_boolean_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                '{"status":"completed","baseline":10,"best":8,"best_iteration":1,'
                '"total_iterations":1,"keeps":1,"discards":0,"crashes":0,'
                '"improved":true,"exit_code":false}\n',
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("field exit_code must be an integer", completed.stderr)

    def test_exec_invariants_accept_ndjson_completion_stream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                "\n".join(
                    [
                        '{"iteration":1,"commit":"keep123","metric":8,"delta":-2,"guard":"pass","status":"keep","description":"improved score"}',
                        '{"status":"completed","baseline":10,"best":8,"best_iteration":1,"total_iterations":1,"keeps":1,"discards":0,"crashes":0,"improved":true,"exit_code":0}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
                "--expect-improvement",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("exec invariants: OK", completed.stdout)

    def test_exec_invariants_reject_ndjson_with_boolean_iteration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                "\n".join(
                    [
                        '{"iteration":true,"commit":"keep123","metric":8,"delta":-2,"guard":"pass","status":"keep","description":"improved score"}',
                        '{"status":"completed","baseline":10,"best":8,"best_iteration":1,"total_iterations":1,"keeps":1,"discards":0,"crashes":0,"improved":true,"exit_code":0}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("field iteration must be an integer", completed.stderr)

    def test_exec_invariants_reject_ndjson_without_completed_final_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            last_message = repo / "last-message.txt"
            self.write_exec_repo(repo)
            last_message.write_text(
                "\n".join(
                    [
                        '{"iteration":1,"commit":"keep123","metric":8,"delta":-2,"guard":"pass","status":"keep","description":"improved score"}',
                        '{"iteration":2,"commit":"keep456","metric":7,"delta":-1,"guard":"pass","status":"keep","description":"improved score again"}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_invariant_check(
                "exec",
                "--repo",
                str(repo),
                "--last-message-file",
                str(last_message),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("must report status=completed", completed.stderr)


if __name__ == "__main__":
    unittest.main()
