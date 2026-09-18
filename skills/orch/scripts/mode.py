"""Resolve orch invocation controls without dispatching or changing any state."""
import argparse
import json
import re
import shlex
from pathlib import Path


def resolve(invocation, capabilities):
    words = shlex.split(invocation)
    if words and words[0] in {'$orch', 'orch', '/orch'}:
        words = words[1:]
    auto = any(w in {'auto', '--until=human'} for w in words)
    once = '--once' in words
    watches = [w.partition('=')[2] for w in words if w.startswith('--watch=')]
    unknown = [w for w in words if w not in {'auto', '--until=human', '--once'} and not w.startswith('--watch=')]
    reasons = []
    if unknown or (once and auto) or len(watches) > 1:
        reasons.append('Conflicting or unsupported invocation controls')
    watch = watches[0] if watches else None
    if watch is not None and not re.fullmatch(r'[1-9][0-9]*[mh]', watch):
        reasons.append('Watch needs a positive duration such as 20m')
    if watch and capabilities.get('scheduler_available') is not True:
        reasons.append('Required scheduling capability is unavailable; repair/admit an adapter before execution')
    supported = capabilities.get('supported_intervals')
    if watch and supported and watch not in supported:
        reasons.append('Requested watch interval is unsupported by the host')
    mode = 'once' if once else 'auto' if auto else 'discover'
    return {'mode': mode, 'valid': not reasons, 'blocked_reasons': reasons,
            'goal_required': mode == 'auto' and not reasons,
            'goal_operations': ['inspect_existing', 'reuse_matching_or_create'] if mode == 'auto' and not reasons else [],
            'watch_interval': watch, 'mode_allows_execution': mode != 'discover' and not reasons,
            'branch_authorization': 'unknown_until_full_branch_instructions_read',
            'next_action': 'list_then_read_every_branch_including_continuation_pages',
            'unit_limit': 1 if mode == 'once' else 0 if mode == 'discover' else None,
            'unit_operations': ['execute', 'verify', 'accept'],
            'acceptance_requires': 'a separate successful verifier invocation after execution; dispatch success and reading output do not count',
            'after_unit': 'report_and_stop' if mode == 'once' else 'recompute_ready_branches',
            'report_status_scope': 'whole branch graph, not just this invocation; remaining branches mean partial/waiting/blocked, never complete',
            'report_required': True,
            'exit_operations': ['write_project_report_file', 'read_back_report_file', 'final_response']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('invocation')
    parser.add_argument('--capabilities', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(resolve(args.invocation, json.loads(args.capabilities.read_text())), indent=2))
