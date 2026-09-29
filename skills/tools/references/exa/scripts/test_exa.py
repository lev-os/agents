#!/usr/bin/env python3
"""Offline transport and payload checks: python3 test_exa.py."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

script = Path(__file__).with_name('exa.sh').resolve()
with tempfile.TemporaryDirectory(prefix='exa-test-') as directory:
    root = Path(directory)
    fake = root / 'curl'
    fake.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
Path(os.environ['EXA_TEST_LOG']).write_text(json.dumps(args))
status = os.environ.get('EXA_TEST_STATUS', '200')
if status == 'transport': sys.exit(28)
if '-w' in args:
    print('{}\\n' + status)
elif status != '200':
    sys.exit(22)
else:
    print('{"results":[],"answer":"fixture"}')
''')
    fake.chmod(0o700)
    envfile = root / 'env'
    envfile.write_text('EXA_API_KEY=file-key\n')
    env = {key: value for key, value in os.environ.items() if not key.startswith('EXA_')}
    env.update(PATH=str(root) + os.pathsep + os.environ['PATH'],
               EXA_ENV_FILE=str(envfile), EXA_CREDENTIALS_FILE=str(root / 'missing'),
               EXA_TEST_LOG=str(root / 'request.json'), EXA_CONNECT_TIMEOUT='2',
               EXA_MAX_TIME='5')

    def run(*args, overrides=None, success=True):
        result = subprocess.run(['bash', str(script), *args], cwd=root,
                                env=env | (overrides or {}), capture_output=True,
                                text=True, timeout=10)
        assert (result.returncode == 0) == success, (args, result.stderr)
        return result

    def request():
        return json.loads((root / 'request.json').read_text())

    def payload():
        args = request()
        return json.loads(args[args.index('-d') + 1])

    run('status', overrides={'EXA_API_KEY': 'explicit'})
    args = request()
    assert 'x-api-key: explicit' in args and 'x-api-key: file-key' not in args
    assert args[args.index('--connect-timeout') + 1] == '2'
    assert args[args.index('--max-time') + 1] == '5'
    run('status')
    assert 'x-api-key: file-key' in request()
    for status in ('401', '403', '429', '500', 'transport'):
        result = run('status', overrides={'EXA_TEST_STATUS': status}, success=False)
        assert 'api: ok' not in result.stdout
    run('search', 'quote " and $ shell', '--num', '2', '--no-summary')
    assert payload()['query'] == 'quote " and $ shell'
    assert payload()['numResults'] == 2 and 'userLocation' not in payload()
    assert 'summary' not in payload()['contents']
    run('search', 'q', '--location', 'CA', '--domains', 'a.test,b.test',
        '--since', '2026-09-01', '--until', '2026-09-21', '--no-text', '--no-summary')
    assert payload()['userLocation'] == 'CA'
    assert payload()['includeDomains'] == ['a.test', 'b.test']
    assert payload()['startPublishedDate'] == '2026-09-01T00:00:00.000Z'
    assert 'contents' not in payload()
    run('contents', 'https://example.com/a', '--max-chars', '100', '--no-summary')
    assert payload()['urls'] == ['https://example.com/a']
    assert payload()['text']['maxCharacters'] == 100 and 'summary' not in payload()
    output = root / 'answer.json'
    run('answer', 'question', '--no-text', '--output', str(output))
    assert payload() == {'query': 'question'} and json.loads(output.read_text())['answer'] == 'fixture'
    output.write_text('preserve')
    run('answer', 'q', '--output', str(output), overrides={'EXA_TEST_STATUS': '500'}, success=False)
    assert output.read_text() == 'preserve'
    for args in [('search', 'q', '--num', '0'), ('search', 'q', '--num'),
                 ('contents',), ('contents', '--unknown'), ('contents', 'file:///tmp/x'),
                 ('answer', 'q', '--unknown')]:
        (root / 'request.json').unlink(missing_ok=True)
        run(*args, success=False)
        assert not (root / 'request.json').exists(), args
print('Exa offline transport, payload, validation, and output checks passed')
