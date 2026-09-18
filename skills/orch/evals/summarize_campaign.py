"""Bounded campaign verdict across core and invocation cases; retains every attempt."""
import argparse
import json
import re
from pathlib import Path

from audit_receipts import audit
from run_trials import CASES, SKILL, digest
from invocation_cases import INVOCATIONS


def same_except_budget(previous, current):
    pattern = r"state\['limit'\] not in \([0-9, ]+\)"
    return (len(re.findall(pattern, previous)) == len(re.findall(pattern, current)) == 1
            and re.sub(pattern, 'AUTHORIZED_CAPS', previous) == re.sub(pattern, 'AUTHORIZED_CAPS', current))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('campaign', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--subject', type=Path, default=SKILL / 'SKILL.md')
    parser.add_argument('--evaluator', type=Path, default=Path(__file__).with_name('run_trials.py'))
    parser.add_argument('--compatible-evaluator', type=Path, action='append', default=[], help='Previous snapshot differing ONLY in the authorized-cap tuple')
    args = parser.parse_args()
    campaign = json.loads(args.campaign.read_text())
    current = digest(args.subject)
    evaluator = digest(args.evaluator)
    evaluators = {evaluator}
    for previous in args.compatible_evaluator:
        if not same_except_budget(previous.read_text(), args.evaluator.read_text()):
            parser.error('Compatible evaluator differs outside the authorized-cap tuple')
        evaluators.add(digest(previous))
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
        if row['subject_sha256'] == current and row['evaluator_sha256'] in evaluators:
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
              'compatible_evaluator_sha256': sorted(evaluators - {evaluator}),
              'cases': cases, 'attempts': attempts}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
