"""Exercise the actual sandbox restrictions before any further agent trials."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from sample_host import run_job


class TrialBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'outputs').mkdir()

    def run_code(self, code):
        return run_job([sys.executable, '-c', code], root=self.root)

    def test_authorized_output_write(self):
        result = self.run_code("from pathlib import Path; Path('outputs/ok').write_text('ok')")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_parent_cannot_be_signalled(self):
        result = self.run_code('import os; os.kill(os.getppid(), 0)')
        self.assertNotEqual(result.returncode, 0)

    def test_network_is_denied(self):
        result = self.run_code("import socket; socket.create_connection(('example.com', 80), 1)")
        self.assertNotEqual(result.returncode, 0)

    def test_write_outside_outputs_denied(self):
        result = self.run_code("from pathlib import Path; Path('outside').write_text('bad')")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'outside').exists())

    def test_other_executable_denied(self):
        result = self.run_code("import subprocess; subprocess.run(['/usr/bin/true'], check=True)")
        self.assertNotEqual(result.returncode, 0)

    def test_home_read_denied(self):
        # Read a harmless known-present file rather than actual credentials.
        path = str(Path.home() / '.agents/skills/orch/SKILL.md')
        result = self.run_code('from pathlib import Path; Path(' + repr(path) + ').read_text()')
        self.assertNotEqual(result.returncode, 0)

    def test_mcp_has_no_shell_and_rejects_path_escape(self):
        commands = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'write_file', 'arguments': {'path': '../escape.txt', 'content': 'bad'}}},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'host', 'arguments': {'action': 'killall'}}},
        ]
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('sample_mcp.py')), str(self.root)],
                                input='\n'.join(json.dumps(x) for x in commands)+'\n', text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [json.loads(x) for x in result.stdout.splitlines()]
        self.assertEqual({t['name'] for t in rows[0]['result']['tools']}, {'read_file', 'write_file', 'host', 'resolve_invocation'})
        self.assertTrue(rows[1]['result']['isError'])
        self.assertTrue(rows[2]['result']['isError'])


if __name__ == '__main__':
    unittest.main()
