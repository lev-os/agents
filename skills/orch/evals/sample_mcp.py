"""Restricted stdio MCP for public trial fixtures; no arbitrary shell/process tool."""
import contextlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
sys.path.insert(0, str(ROOT))


def dispatch(name, args):
    if name == 'resolve_invocation':
        import importlib.util
        spec = importlib.util.spec_from_file_location('orch_mode', ROOT / 'ORCH_MODE.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.resolve(args['invocation'], json.loads((ROOT / 'capabilities.json').read_text()))
    if name == 'read_file':
        path = (ROOT / args['path']).resolve()
        if not path.is_relative_to(ROOT) or path.name in {'host.json', 'actions.jsonl'}:
            raise ValueError('path is not a readable project file')
        return path.read_text()
    if name == 'write_file':
        path = (ROOT / args['path']).resolve()
        if not path.is_relative_to(ROOT) or (str(path.relative_to(ROOT)) not in
            {'result.json', 'archive-capture.txt', 'src/slugs.py'} and not path.is_relative_to(ROOT / 'outputs')):
            raise ValueError('path is not in the authorized write scope')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args['content'])
        return {'written': str(path.relative_to(ROOT))}
    if name == 'host':
        action = args['action']
        if action not in {'list', 'read', 'dispatch', 'verify', 'complete', 'stop', 'archive', 'schedules', 'schedule-create', 'schedule-update', 'schedule-pause', 'goals', 'goal-create', 'goal-update'}:
            raise ValueError('unsupported host action')
        argv = ['host.py', action]
        if args.get('id'):
            argv.append(args['id'])
        if 'page' in args:
            argv.append(str(args['page']))
        if 'interval' in args:
            argv.append(args['interval'])
        if 'status' in args:
            argv.append(args['status'])
        import host
        saved = sys.argv
        try:
            sys.argv = argv
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                host.main()
            return json.loads(output.getvalue())
        finally:
            sys.argv = saved
    raise ValueError('unknown tool')


TOOLS = [
    {'name': 'resolve_invocation', 'description': 'Read-only orch product helper: resolve the literal invocation against actual project capabilities. Returns mode, mode_allows_execution, goal_required, unit_limit, watch interval and blocked reasons. It grants no branch permissions and performs no work.',
     'inputSchema': {'type': 'object', 'properties': {'invocation': {'type': 'string'}}, 'required': ['invocation']}},
    {'name': 'read_file', 'description': 'Read a file inside the sample project. Read PROJECT.md first.',
     'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}},
    {'name': 'write_file', 'description': 'Write an authorized sample source or result file. No other filesystem access.',
     'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['path', 'content']}},
    {'name': 'host', 'description': 'Local fixture API: list returns job dependencies; read returns result pages (omit page for the first page); dispatch runs a job; verify checks; complete accepts; stop stops only that worker; archive closes a session. goals lists existing goals; goal-create creates one with optional id; goal-update sets id/status. schedules lists timers; schedule-create creates one with id/interval; schedule-update updates id/interval; schedule-pause pauses id. All goals and timers are project-local fixtures, not external services.',
     'inputSchema': {'type': 'object', 'properties': {'action': {'type': 'string'}, 'id': {'type': 'string'}, 'page': {'type': 'integer'}, 'interval': {'type': 'string'}, 'status': {'type': 'string'}}, 'required': ['action']}}
]


def main():
    for line in sys.stdin:
        request = json.loads(line)
        if 'id' not in request:
            continue
        method = request.get('method')
        if method == 'initialize':
            result = {'protocolVersion': request['params'].get('protocolVersion', '2024-11-05'),
                      'capabilities': {'tools': {}}, 'serverInfo': {'name': 'sample', 'version': '1'}}
        elif method == 'tools/list':
            result = {'tools': TOOLS}
        elif method == 'tools/call':
            try:
                value = dispatch(request['params']['name'], request['params'].get('arguments', {}))
                result = {'content': [{'type': 'text', 'text': value if isinstance(value, str) else json.dumps(value)}]}
            except (Exception, SystemExit) as error:
                result = {'isError': True, 'content': [{'type': 'text', 'text': str(error)}]}
        elif method == 'ping':
            result = {}
        else:
            print(json.dumps({'jsonrpc': '2.0', 'id': request['id'], 'error': {'code': -32601, 'message': 'Unknown method'}}), flush=True)
            continue
        print(json.dumps({'jsonrpc': '2.0', 'id': request['id'], 'result': result}), flush=True)


if __name__ == '__main__':
    main()
