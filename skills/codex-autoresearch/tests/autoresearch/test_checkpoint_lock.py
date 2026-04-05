from __future__ import annotations

import tempfile
from pathlib import Path

from .base import AutoresearchScriptsTestBase


class AutoresearchCheckpointLockTest(AutoresearchScriptsTestBase):
    maxDiff = None

    def test_checkpoint_lock_acquire_status_release_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            acquired = self.run_script(
                "autoresearch_checkpoint_lock.py",
                "acquire",
                "--repo",
                str(repo),
                "--run-tag",
                "run-a",
                "--pid",
                "12345",
            )
            self.assertEqual(acquired["status"], "acquired")

            status = self.run_script(
                "autoresearch_checkpoint_lock.py",
                "status",
                "--repo",
                str(repo),
            )
            self.assertEqual(status["status"], "stale")
            self.assertEqual(status["payload"]["run_tag"], "run-a")

            reacquired = self.run_script(
                "autoresearch_checkpoint_lock.py",
                "acquire",
                "--repo",
                str(repo),
                "--run-tag",
                "run-b",
                "--pid",
                str(Path(__file__).stat().st_ino),
            )
            self.assertEqual(reacquired["status"], "acquired")
            self.assertEqual(reacquired["payload"]["run_tag"], "run-b")

            released = self.run_script(
                "autoresearch_checkpoint_lock.py",
                "release",
                "--repo",
                str(repo),
                "--run-tag",
                "run-b",
            )
            self.assertEqual(released["status"], "released")

            final_status = self.run_script(
                "autoresearch_checkpoint_lock.py",
                "status",
                "--repo",
                str(repo),
            )
            self.assertEqual(final_status["status"], "free")
