"""Independent artifact/transport audit for current-subject trial receipts."""
import argparse
import hashlib
import json
from pathlib import Path

from run_trials import SKILL, digest


def audit(path):
    manifest = json.loads((path / 'manifest.json').read_text())
    receipt = json.loads((path / 'measurement.json').read_text())
    records = [json.loads(x) for x in (path / 'events.jsonl').read_text().splitlines()]
    calls = {block['id']: block for r in records if r.get('type') == 'assistant'
             for block in r.get('message', {}).get('content', []) if block.get('type') == 'tool_use'}
    successful_reads = {}
    for r in records:
        if r.get('type') != 'user':
            continue
        for block in r.get('message', {}).get('content', []):
            call = calls.get(block.get('tool_use_id'))
            if block.get('type') != 'tool_result' or block.get('is_error') or not call or call['name'] != 'mcp__sample__read_file':
                continue
            content = block.get('content', [])
            text = content if isinstance(content, str) else ''.join(c.get('text', '') for c in content)
            successful_reads[call['input']['path']] = hashlib.sha256(text.encode()).hexdigest()
    checked = {'terminal_pass': receipt['status'] == 'pass',
               'only_scoped_tools': set(c['name'] for c in calls.values()) <= {'mcp__sample__read_file', 'mcp__sample__write_file', 'mcp__sample__host', 'mcp__sample__resolve_invocation'},
               'project_bytes_delivered': successful_reads.get('PROJECT.md') == digest(path / 'project/PROJECT.md'),
               'subject_preserved': manifest['subject_sha256'] == digest(path / 'skill.snapshot.txt'),
               'allowed_model': receipt['models'] == ['claude-haiku-4-5-20251001'],
               'fixture_generation_matches': manifest['fixture_sha256'] == digest(Path(__file__).with_name('sample_host.py')),
               'transport_generation_matches': manifest.get('mcp_sha256') == digest(Path(__file__).with_name('sample_mcp.py'))}
    if manifest['arm'] == 'candidate':
        checked['skill_bytes_delivered'] = successful_reads.get('ORCH_SKILL.md') == manifest['subject_sha256']
    return {'path': str(path), 'case': receipt['case'], 'arm': receipt['arm'], 'checks': checked, 'passed': all(checked.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home() / '.local/state/lev/evals/orch')
    args = parser.parse_args()
    current = digest(SKILL / 'SKILL.md')
    rows = []
    for path in sorted(args.root.glob('*/measurement.json')):
        receipt = json.loads(path.read_text())
        if receipt['subject_sha256'] == current and receipt['arm'] == 'candidate':
            rows.append(audit(path.parent))
    print(json.dumps({'audits': rows, 'passed': bool(rows) and all(r['passed'] for r in rows)}, indent=2))
    return 0 if rows and all(r['passed'] for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
