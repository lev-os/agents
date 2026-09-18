"""Bounded campaign verdict across core and invocation cases; retains every attempt."""
import argparse
import json
from pathlib import Path

from audit_receipts import audit
from run_trials import CASES, SKILL, digest
from invocation_cases import INVOCATIONS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('campaign', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--subject', type=Path, default=SKILL / 'SKILL.md')
    parser.add_argument('--evaluator', type=Path, default=Path(__file__).with_name('run_trials.py'))
    args = parser.parse_args()
    campaign = json.loads(args.campaign.read_text())
    current = digest(args.subject)
    evaluator = digest(args.evaluator)
    attempts = []
    current_rows = []
    for entry in campaign['runs']:
        path = Path(entry['path'])
        measurement = path / 'measurement.json'
        if not measurement.exists():
            attempts.append({'case': entry['case'], 'status': 'pending', 'path': str(path)})
            continue
        row = json.loads(measurement.read_text())
        attempts.append({'case': row['case'], 'status': row['status'], 'subject_sha256': row['subject_sha256'], 'path': str(path)})
        if row['subject_sha256'] == current and row['evaluator_sha256'] == evaluator:
            current_rows.append((row, audit(path)))
    cases = {}
    for case in CASES + INVOCATIONS:
        rows = [(r, a) for r, a in current_rows if r['case'] == case]
        cases[case] = {'runs': len(rows), 'passed': bool(rows) and all(r['status'] == 'pass' and a['passed'] for r, a in rows),
                       'failed_checks': sorted({k for r, a in rows for k, v in {**(r.get('measurements') or {}).get('checks', {}), **a['checks']}.items() if not v})}
    passed = len(attempts) <= campaign['limit'] and all(c['passed'] for c in cases.values()) and not any(a['status'] == 'pending' for a in attempts)
    result = {'status': 'sandbox_qualified' if passed else 'incomplete_or_failed',
              'scope': 'Haiku via restricted MCP on synthetic goal/scheduler fixtures and real sandboxed job artifacts',
              'launches': len(attempts), 'limit': campaign['limit'], 'subject_sha256': current, 'evaluator_sha256': evaluator,
              'cases': cases, 'attempts': attempts}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
