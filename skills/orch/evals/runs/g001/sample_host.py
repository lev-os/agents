"""Sandbox-only worker/scheduler fixture. This is NOT a real provider adapter.

Commands: list, read ID [PAGE], dispatch ID, verify ID, complete ID,
stop ID, archive ID, schedules, schedule-create, schedule-pause ID.
Operations deliberately allow incorrect ordering; the controller grades the log.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'host.json'


def main():
    args = sys.argv[1:]
    if not args or args[0] in {'-h', '--help'}:
        print(__doc__)
        return
    state = json.loads(STATE.read_text())
    action = args[0]
    key = args[1] if len(args) > 1 else None
    item = next((x for x in state['workers'] if x['id'] == key), None)
    result = {}
    if action == 'list':
        result = [{'id': x['id'], 'status': x['status'], 'parent': x.get('parent'), 'needs': x['needs']} for x in state['workers']]
    elif action == 'read' and item:
        page = int(args[2]) if len(args) > 2 else 0
        pages = item['pages']
        result = {'text': pages[page], 'next_page': page + 1 if page + 1 < len(pages) else None}
    elif action == 'dispatch' and item:
        result = {'handle': key, 'status': 'completed'}
        if item.get('command'):
            proc = subprocess.run(item['command'], cwd=ROOT, text=True, capture_output=True)
            result.update(exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
        item['status'] = 'completed'
    elif action == 'verify' and item:
        proc = subprocess.run(item['verifier'], cwd=ROOT, text=True, capture_output=True)
        result = {'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    elif action == 'complete' and item:
        item['status'] = 'accepted'
        result = {'status': 'accepted'}
    elif action == 'stop' and item:
        item['status'] = 'interrupted'
        result = {'status': 'interrupted', 'children_stopped': False}
    elif action == 'archive' and item:
        item['status'] = 'archived'
        capture = ROOT / 'archive-capture.txt'
        result = {'archived': True, 'capture_at_archive': capture.read_text() if capture.exists() else None}
    elif action == 'schedules':
        result = state['schedules']
    elif action == 'schedule-create':
        state['schedules'].append({'id': 'duplicate-timer', 'status': 'active'})
        result = state['schedules'][-1]
    elif action == 'schedule-pause':
        timer = next(x for x in state['schedules'] if x['id'] == key)
        timer['status'] = 'paused'
        result = timer
    else:
        raise SystemExit('unsupported fixture command; use --help')
    STATE.write_text(json.dumps(state, indent=2) + '\n')
    with (ROOT / 'actions.jsonl').open('a') as log:
        log.write(json.dumps({'action': action, 'id': key, 'args': args[1:], 'result': result}) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
