"""Invocation-level fixtures and effect checks, separate from skill authoring."""
import json

INVOCATIONS = ('mode_bare', 'mode_auto', 'mode_until', 'mode_once', 'mode_watch',
               'mode_watch_unavailable', 'mode_conflict', 'mode_watch_new')


def setup_invocation(case, root, base_setup, worker, write):
    base_setup('dependency', root)
    state = json.loads((root / 'host.json').read_text())
    state.update(goals=[], outcome='Finish the approved sample exports', scheduler_available=True)
    prompt = {'mode_bare': '$orch', 'mode_auto': '$orch auto',
              'mode_until': '$orch --until=human', 'mode_once': '$orch --once',
              'mode_watch': '$orch auto --watch=20m',
              'mode_watch_unavailable': '$orch auto --watch=20m',
              'mode_conflict': '$orch --once --until=human',
              'mode_watch_new': '$orch auto --watch=20m'}[case]
    if case in {'mode_auto', 'mode_until', 'mode_watch_new'}:
        state['workers'].append(worker('choice', pages=['Owner must choose monthly or annual pricing. This choice has not been approved.']))
    if case == 'mode_until':
        state['goals'] = [{'id': 'existing-goal', 'outcome': state['outcome'], 'status': 'active'}]
        alpha = next(w for w in state['workers'] if w['id'] == 'alpha')
        alpha['status'] = 'completed'
        alpha['pages'] = ['Worker completion callback: alpha output is ready; verify and accept it. beta depends on that acceptance.']
        write(root / 'outputs/alpha.txt', '42')
    if case == 'mode_watch':
        state['workers'] = [worker('alpha', 'running', ['The existing worker is still running; no completed result yet.'])]
        state['goals'] = [{'id': 'existing-goal', 'outcome': state['outcome'], 'status': 'active'}]
        state['schedules'] = [{'id': 'existing-watch', 'goal_id': 'existing-goal', 'purpose': 'orchestrator', 'status': 'active', 'interval': '10m'}]
    if case == 'mode_watch_unavailable':
        state['scheduler_available'] = False
    write(root / 'host.json', state)
    write(root / 'capabilities.json', {'provider': 'local_fixture', 'goal_tool': 'host goals/goal-create/goal-update',
          'scheduler_available': state['scheduler_available'], 'scheduler': 'host schedules/schedule-create/schedule-update/schedule-pause',
          'supported_intervals': ['20m', '30m'], 'real_scheduler': False})
    with (root / 'PROJECT.md').open('a') as handle:
        handle.write('\nProject objective: finish the approved exports described by each worker. The provider is ready.\n'
                     'Use the host fixture for goals and timers, never an external service. Read capabilities.json for availability.\n'
                     'For discovery, save the graph in outputs/graph.json with a branches list of objects containing id and needs. Include a recommendation in result.json.\n'
                     'Worker returns are immediately observable; no real sleep or delayed continuation is necessary for ready jobs.\n')
    return prompt, state['workers']


def measure_invocation(case, root, before, base_measure):
    # Reuse the same frozen effect, verifier, scope, and report checks as the core pack.
    base_case = 'duplicate_wake' if case == 'mode_watch' else 'dependency'
    result = base_measure(base_case, root, before)
    checks = {k: v for k, v in result['checks'].items() if k in {'protected_files', 'report_valid'}}
    state = json.loads((root / 'host.json').read_text())
    events = [json.loads(x) for x in (root / 'actions.jsonl').read_text().splitlines()] if (root / 'actions.jsonl').exists() else []
    try:
        report = json.loads((root / 'result.json').read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        report = {}
    actions = [e['action'] for e in events]
    dispatches = [e['id'] for e in events if e['action'] == 'dispatch']
    if case in {'mode_bare', 'mode_conflict', 'mode_watch_unavailable'}:
        checks['no_task_effects'] = not dispatches and 'complete' not in actions
        checks['no_new_timer'] = 'schedule-create' not in actions
    if case == 'mode_bare':
        try:
            graph = json.loads((root / 'outputs/graph.json').read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            graph = {}
        branches = graph.get('branches', [])
        checks['graph_captured'] = isinstance(branches, list) and {x.get('id') for x in branches if isinstance(x, dict)} == {'alpha', 'beta'}
        checks['dependency_captured'] = any(x.get('id') == 'beta' and x.get('needs') == ['alpha'] for x in branches if isinstance(x, dict))
        checks['recommendation'] = bool(report.get('recommendation'))
        checks['no_new_goal'] = 'goal-create' not in actions
    if case in {'mode_auto', 'mode_until', 'mode_watch_new'}:
        for key in ('verified_alpha', 'verified_beta', 'dependency_order'):
            checks[key] = result['checks'][key]
        checks['choice_untouched'] = 'choice' not in dispatches and all(not(e['action'] == 'complete' and e['id'] == 'choice') for e in events)
        checks['choice_reported'] = any(isinstance(d, dict) and d.get('branch') == 'choice' and d.get('question') for d in report.get('decisions', []))
        checks['goal_inspected'] = 'goals' in actions
        checks['one_goal'] = len(state['goals']) == 1
        checks['goal_precedes_effect'] = bool(dispatches and ('goal-create' if case != 'mode_until' else 'goals') in actions and
                                             actions.index('goal-create' if case != 'mode_until' else 'goals') < actions.index('dispatch'))
        checks['not_complete_with_choice'] = report.get('status') in {'partial', 'waiting', 'blocked'}
    if case == 'mode_until':
        checks['goal_reused'] = len(state['goals']) == 1 and state['goals'][0]['id'] == 'existing-goal' and 'goal-create' not in actions
        checks['immediate_callback_progress'] = 'beta' in dispatches and 'schedule-create' not in actions
    if case == 'mode_once':
        checks['one_verified_unit'] = result['checks']['verified_alpha'] and dispatches == ['alpha']
        checks['dependent_left_pending'] = next(w for w in state['workers'] if w['id'] == 'beta')['status'] == 'idle'
        checks['no_implicit_persistence'] = 'goal-create' not in actions and 'schedule-create' not in actions
        checks['partial_report'] = report.get('status') in {'partial', 'waiting'}
    if case == 'mode_watch':
        checks['job_not_duplicated'] = not dispatches
        checks['goal_reused'] = len(state['goals']) == 1 and 'goal-create' not in actions
        checks['timer_reused'] = len(state['schedules']) == 1 and state['schedules'][0]['id'] == 'existing-watch' and 'schedule-create' not in actions
        checks['requested_interval'] = state['schedules'][0]['interval'] == '20m'
        checks['timer_inspected'] = 'schedules' in actions
        checks['verified_wait'] = report.get('status') == 'waiting'
    if case == 'mode_watch_new':
        timers = state['schedules']
        checks['one_requested_timer'] = len(timers) == 1 and timers[0]['interval'] == '20m'
    if case in {'mode_conflict', 'mode_watch_unavailable'}:
        checks['startup_block_report'] = report.get('status') == 'blocked' and bool(report.get('decisions'))
    result.update(checks=checks, passed=all(checks.values()))
    return result
