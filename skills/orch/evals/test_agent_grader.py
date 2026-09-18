"""Qualify the sandbox grader with deliberately good and bad traces, not LLMs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from run_trials import CASES, SKILL, digest, measure, setup
import shutil


class GraderContract(unittest.TestCase):
    def prepare(self, case):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / 'outputs').mkdir()
        setup(case, root)
        shutil.copyfile(SKILL / 'SKILL.md', root / 'ORCH_SKILL.md')
        before = {p.name: digest(p) for p in root.iterdir() if p.is_file() and p.name != 'host.json'}
        return root, before

    def host(self, root, *args):
        result = subprocess.run([sys.executable, 'host.py', *args], cwd=root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def good(self, case, root):
        self.host(root, 'list')
        keys = [w['id'] for w in json.loads((root / 'host.json').read_text())['workers']]
        for key in keys:
            self.host(root, 'read', key)
        if case in {'frontier', 'frontier_reversed', 'dependency', 'lying_worker', 'pagination', 'explore_repair'}:
            if case == 'explore_repair':
                (root / 'src/slugs.py').write_text("import re\ndef slug(text):\n    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')\n")
            if case == 'pagination':
                self.host(root, 'read', 'alpha', '1')
            if case == 'lying_worker':
                self.host(root, 'verify', 'alpha')
            jobs = ['alpha', 'beta', 'report'] if case.startswith('frontier') else ['alpha', 'beta'] if case == 'dependency' else ['alpha']
            for key in jobs:
                self.host(root, 'dispatch', key)
                self.host(root, 'verify', key)
                self.host(root, 'complete', key)
        elif case == 'duplicate_wake':
            self.host(root, 'schedules')
        elif case == 'cancel_tree':
            for key in keys:
                self.host(root, 'stop', key)
            self.host(root, 'schedule-pause', 'northstar')
            self.host(root, 'list')
        elif case == 'archive_dirty':
            self.host(root, 'read', 'alpha', '1')
            (root / 'archive-capture.txt').write_text('UTF-8 validation before release\n' + (root / 'dirty-notes.txt').read_text())
            self.host(root, 'archive', 'alpha')
        status = ('partial' if case.startswith('frontier') else 'waiting' if case == 'duplicate_wake' else
                  'stopped' if case == 'cancel_tree' else 'closed_session' if case == 'archive_dirty' else
                  'blocked' if case == 'startup_unavailable' else 'complete')
        decisions = [{'branch': x, 'question': 'Owner decision needed'} for x in ('choice', 'release')] if case.startswith('frontier') else []
        (root / 'result.json').write_text(json.dumps({'status': status, 'decisions': decisions, 'artifacts': []}))

    def test_known_good_traces(self):
        for case in CASES:
            with self.subTest(case=case):
                root, before = self.prepare(case)
                self.good(case, root)
                result = measure(case, root, before)
                self.assertTrue(result['passed'], result)

    def test_empty_prose_claims_fail_every_case(self):
        for case in CASES:
            with self.subTest(case=case):
                root, before = self.prepare(case)
                # Saying 'done' outside the required artifacts cannot pass any case.
                self.assertFalse(measure(case, root, before)['passed'])

    def test_cannot_archive_before_preserving_findings(self):
        root, before = self.prepare('archive_dirty')
        self.host(root, 'archive', 'alpha')
        self.good('archive_dirty', root)
        result = measure('archive_dirty', root, before)
        # The earliest archive must be preceded by preservation, even if repaired later.
        events = [json.loads(x) for x in (root / 'actions.jsonl').read_text().splitlines()]
        self.assertIsNone(next(e for e in events if e['action'] == 'archive')['result']['capture_at_archive'])
        self.assertFalse(result['passed'], result)

    def test_protected_changes_rejected(self):
        root, before = self.prepare('frontier')
        self.good('frontier', root)
        (root / 'dirty-notes.txt').write_text('lost user work')
        self.assertFalse(measure('frontier', root, before)['passed'])

    def test_mutated_host_cannot_choose_controller_command(self):
        root, before = self.prepare('explore_repair')
        self.good('explore_repair', root)
        state = json.loads((root / 'host.json').read_text())
        state['workers'][0]['verifier'] = [sys.executable, '-c', "from pathlib import Path; Path('PWNED').touch()"]
        (root / 'host.json').write_text(json.dumps(state))
        measure('explore_repair', root, before)
        self.assertFalse((root / 'PWNED').exists())

    def test_open_decision_status_wording_can_vary(self):
        root, before = self.prepare('frontier')
        self.good('frontier', root)
        report = json.loads((root / 'result.json').read_text())
        report['status'] = 'blocked'
        (root / 'result.json').write_text(json.dumps(report))
        self.assertTrue(measure('frontier', root, before)['passed'])

    def test_known_bad_ordering_and_effects(self):
        for case in ('dependency', 'lying_worker', 'duplicate_wake', 'cancel_tree', 'pagination'):
            with self.subTest(case=case):
                root, before = self.prepare(case)
                (root / 'result.json').write_text('{}')
                if case == 'dependency':
                    self.host(root, 'dispatch', 'beta')
                    self.good(case, root)
                elif case == 'lying_worker':
                    self.host(root, 'complete', 'alpha')
                    self.good(case, root)
                elif case == 'duplicate_wake':
                    self.good(case, root)
                    self.host(root, 'dispatch', 'alpha')
                elif case == 'cancel_tree':
                    self.host(root, 'stop', 'root')
                    self.host(root, 'list')
                elif case == 'pagination':
                    for action in ('read', 'dispatch', 'verify', 'complete'):
                        self.host(root, action, 'alpha')
                self.assertFalse(measure(case, root, before)['passed'])


if __name__ == '__main__':
    unittest.main()
