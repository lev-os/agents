"""Known-good and intentionally wrong invocation traces; no model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from invocation_cases import INVOCATIONS, setup_invocation, measure_invocation
from run_trials import setup, worker, write, measure, digest, reserve_campaign


class InvocationOracle(unittest.TestCase):
    def case(self, name):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / 'outputs').mkdir()
        setup_invocation(name, root, setup, worker, write)
        before = {p.name: digest(p) for p in root.iterdir() if p.is_file() and p.name != 'host.json'}
        return root, before

    def host(self, root, *args):
        result = subprocess.run([sys.executable, 'host.py', *args], cwd=root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def prepare_good(self, case, root):
        self.host(root, 'list')
        state = json.loads((root / 'host.json').read_text())
        for job in state['workers']:
            self.host(root, 'read', job['id'])
        report = {'status': 'partial', 'decisions': [], 'artifacts': []}
        if case == 'mode_bare':
            write(root / 'outputs/graph.json', {'branches': [{'id': w['id'], 'needs': w['needs']} for w in state['workers']]})
            report['recommendation'] = 'Run auto after preparation.'
        elif case in {'mode_conflict', 'mode_watch_unavailable'}:
            report.update(status='blocked', decisions=[{'branch': 'startup', 'question': 'Resolve required capability or conflicting mode'}])
        elif case == 'mode_watch':
            self.host(root, 'goals')
            self.host(root, 'schedules')
            self.host(root, 'schedule-update', 'existing-watch', '20m')
            report['status'] = 'waiting'
        else:
            if case != 'mode_once':
                self.host(root, 'goals')
                if case != 'mode_until':
                    self.host(root, 'goal-create', 'created-goal')
            if case == 'mode_watch_new':
                self.host(root, 'schedules')
                self.host(root, 'schedule-create', 'watch', '20m')
            for key in (['alpha'] if case == 'mode_once' else ['alpha', 'beta']):
                if not (case == 'mode_until' and key == 'alpha'):
                    self.host(root, 'dispatch', key)
                self.host(root, 'verify', key)
                self.host(root, 'complete', key)
            if case != 'mode_once':
                report['decisions'] = [{'branch': 'choice', 'question': 'Monthly or annual?'}]
        write(root / 'result.json', report)

    def test_positive_controls(self):
        for case in INVOCATIONS:
            with self.subTest(case=case):
                root, before = self.case(case)
                self.prepare_good(case, root)
                result = measure_invocation(case, root, before, measure)
                self.assertTrue(result['passed'], result)

    def test_empty_claim_cannot_pass(self):
        for case in INVOCATIONS:
            with self.subTest(case=case):
                root, before = self.case(case)
                write(root / 'result.json', {'status': 'complete'})
                self.assertFalse(measure_invocation(case, root, before, measure)['passed'])

    def test_bare_must_not_execute(self):
        root, before = self.case('mode_bare')
        self.prepare_good('mode_bare', root)
        self.host(root, 'dispatch', 'alpha')
        self.assertFalse(measure_invocation('mode_bare', root, before, measure)['passed'])

    def test_once_must_stop_after_one_unit(self):
        root, before = self.case('mode_once')
        self.prepare_good('mode_once', root)
        self.host(root, 'dispatch', 'beta')
        self.assertFalse(measure_invocation('mode_once', root, before, measure)['passed'])

    def test_budget_cannot_reset_on_revision(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'campaign.json'
            for n in range(20):
                self.assertEqual(reserve_campaign(path, {'case': 'test', 'subject_sha256': str(n)}, Path(folder)), n+1)
            with self.assertRaises(SystemExit):
                reserve_campaign(path, {'case': 'test', 'subject_sha256': 'new-revision'}, Path(folder))
            self.assertEqual(len(json.loads(path.read_text())['runs']), 20)


if __name__ == '__main__':
    unittest.main()
