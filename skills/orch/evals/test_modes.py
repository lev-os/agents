import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('mode', Path(__file__).resolve().parents[1] / 'scripts/mode.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Modes(unittest.TestCase):
    def test_resolution(self):
        caps = {'scheduler_available': True, 'supported_intervals': ['20m', '30m']}
        for command, mode, limit, goal in [('$orch', 'discover', 0, False), ('$orch auto', 'auto', None, True),
                                          ('$orch --until=human', 'auto', None, True), ('$orch --once', 'once', 1, False)]:
            with self.subTest(command=command):
                result = module.resolve(command, caps)
                self.assertTrue(result['valid'])
                self.assertEqual((result['mode'], result['unit_limit'], result['goal_required']), (mode, limit, goal))
        for command in ('$orch --once auto', '$orch --until=no', '$orch --watch=0m', '$orch auto --watch=1h'):
            self.assertFalse(module.resolve(command, caps)['valid'])
        unavailable = module.resolve('$orch auto --watch=20m', {'scheduler_available': False})
        self.assertFalse(unavailable['mode_allows_execution'])
        self.assertFalse(unavailable['goal_required'])
        self.assertTrue(unavailable['report_required'])


if __name__ == '__main__':
    unittest.main()
