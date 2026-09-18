"""Behavioral regressions for the bundled CLI, independent of skill wording."""
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CLI = Path(__file__).resolve().parents[1] / 'scripts/orch.py'


class ChainContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / 'state.json'

    def call(self, *args):
        return subprocess.run([sys.executable, str(CLI), *args, '--state', str(self.state)],
                              text=True, capture_output=True)

    def plan(self, dependency=False):
        args = ['plan', '--goal', 'Repair sample project', '--root', self.tmp.name,
                '--mode', 'auto', '--route', 'skill://coder', '--route', 'skill://research']
        if dependency:
            args += ['--need', 'route-2=route-1']
        result = self.call(*args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def tick(self, branch, outcome):
        return self.call('tick', '--branch', branch, '--outcome', outcome,
                         '--note', 'controller-observed sample result')

    def read(self):
        return json.loads(self.state.read_text())

    def test_blocked_branch_does_not_stop_independent_work(self):
        for blocked in ('route-1', 'route-2'):
            with self.subTest(blocked=blocked):
                if self.state.exists():
                    self.state.unlink()
                self.plan()
                self.assertEqual(self.tick(blocked, 'blocked').returncode, 0)
                self.assertNotIn(self.read()['status'], ('blocked', 'paused', 'complete'))

    def test_decision_does_not_stop_independent_work(self):
        self.plan()
        self.tick('route-1', 'decision_needed')
        self.assertNotIn(self.read()['status'], ('blocked', 'paused', 'complete'))

    def test_no_false_completion_with_unanswered_decision(self):
        self.plan()
        self.tick('route-1', 'decision_needed')
        self.tick('route-2', 'complete')
        self.assertNotEqual(self.read()['status'], 'complete')
        self.assertEqual(len(self.read()['decisions']), 1)

    def test_all_outcome_orders_preserve_open_branches(self):
        for a, b in itertools.product(('complete', 'blocked', 'decision_needed'), repeat=2):
            with self.subTest(a=a, b=b):
                if self.state.exists():
                    self.state.unlink()
                self.plan()
                self.tick('route-1', a)
                self.tick('route-2', b)
                self.assertEqual(self.read()['status'] == 'complete', a == b == 'complete')

    def test_dependency_blocks_early_completion_without_mutation(self):
        self.plan(dependency=True)
        before = self.state.read_bytes()
        self.assertNotEqual(self.tick('route-2', 'complete').returncode, 0)
        self.assertEqual(self.state.read_bytes(), before)

    def test_dependency_becomes_ready_after_completion(self):
        self.plan(dependency=True)
        self.assertEqual(self.tick('route-1', 'complete').returncode, 0)
        self.assertEqual(self.tick('route-2', 'complete').returncode, 0)
        self.assertEqual(self.read()['status'], 'complete')

    def test_reject_cycle_and_self_dependency(self):
        for needs in (['route-1=route-1'], ['route-1=route-2', 'route-2=route-1']):
            args = ['plan', '--goal', 'cycle', '--route', 'skill://coder', '--route', 'skill://research']
            for need in needs:
                args += ['--need', need]
            self.assertNotEqual(self.call(*args).returncode, 0)
            self.assertFalse(self.state.exists())

    def test_plan_never_overwrites_existing_chain(self):
        self.plan()
        before = self.state.read_bytes()
        self.assertNotEqual(self.call('plan', '--goal', 'replacement').returncode, 0)
        self.assertEqual(self.state.read_bytes(), before)

    def test_terminal_chain_does_not_restart(self):
        self.plan()
        self.tick('route-1', 'complete')
        self.tick('route-2', 'complete')
        before = self.state.read_bytes()
        self.assertNotEqual(self.tick('route-1', 'progress').returncode, 0)
        self.assertEqual(self.state.read_bytes(), before)

    def test_decision_requires_explicit_resolution(self):
        self.plan()
        self.tick('route-1', 'decision_needed')
        before = self.state.read_bytes()
        self.assertNotEqual(self.tick('route-1', 'complete').returncode, 0)
        self.assertEqual(self.state.read_bytes(), before)

    def test_malformed_state_fails_without_traceback_or_mutation(self):
        self.plan()
        data = self.read()
        data['branches'][0]['needs'] = 123
        self.state.write_text(json.dumps(data))
        before = self.state.read_bytes()
        result = self.call('validate')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(self.state.read_bytes(), before)

    def test_duplicate_wake_is_idempotent(self):
        self.plan()
        args = ['tick', '--branch', 'route-1', '--outcome', 'progress',
                '--note', 'verified wake', '--event-id', 'wake-1']
        first = self.call(*args)
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.state.read_bytes()
        self.assertEqual(self.call(*args).returncode, 0)
        self.assertEqual(self.state.read_bytes(), before)
        different = self.call('tick', '--branch', 'route-2', '--outcome', 'complete',
                              '--note', 'conflicting replay', '--event-id', 'wake-1')
        self.assertNotEqual(different.returncode, 0)


if __name__ == '__main__':
    unittest.main()
