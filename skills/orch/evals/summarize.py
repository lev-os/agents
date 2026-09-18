"""Aggregate real trial receipts without dropping failures or mixing generations."""
import argparse
from collections import Counter
import json
from pathlib import Path

from run_trials import CASES, SKILL, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home() / '.local/state/lev/evals/orch')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    subject = digest(SKILL / 'SKILL.md')
    evaluator = digest(Path(__file__).with_name('run_trials.py'))
    receipts = []
    for path in sorted(args.root.glob('*/measurement.json')):
        item = json.loads(path.read_text())
        item['receipt'] = str(path)
        receipts.append(item)
    current = [x for x in receipts if x['subject_sha256'] == subject and x['evaluator_sha256'] == evaluator]
    cases = {}
    for case in CASES:
        rows = [x for x in current if x['case'] == case and x['arm'] == 'candidate']
        baseline = [x for x in receipts if x['case'] == case and x['arm'] == 'baseline' and x['evaluator_sha256'] == evaluator]
        cases[case] = {'candidate_counts': dict(Counter(x['status'] for x in rows)),
                       'baseline_counts': dict(Counter(x['status'] for x in baseline)),
                       'qualified': len(rows) >= 2 and all(x['status'] == 'pass' for x in rows),
                       'candidate_receipts': [x['receipt'] for x in rows],
                       'baseline_receipts': [x['receipt'] for x in baseline]}
    qualified = all(x['qualified'] for x in cases.values())
    result = {'status': 'sandbox_qualified' if qualified else 'incomplete',
              'qualification_scope': 'Claude Haiku in synthetic sample projects; no native scheduler or multi-provider claim',
              'subject_sha256': subject, 'evaluator_sha256': evaluator,
              'historical_counts': dict(Counter(x['status'] for x in receipts)),
              'all_receipts': [x['receipt'] for x in receipts], 'cases': cases}
    output = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    print(output)
    return 0 if qualified else 1


if __name__ == '__main__':
    raise SystemExit(main())
