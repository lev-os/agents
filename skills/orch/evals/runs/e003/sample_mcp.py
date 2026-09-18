"""Restricted stdio MCP for public trial fixtures; no arbitrary shell/process tool."""
import contextlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
sys.path.insert(0, str(ROOT))


def dispatch(name, args):
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
        if action not in {'list', 'read', 'dispatch', 'verify', 'complete', 'stop', 'archive', 'schedules', 'schedule-create', 'schedule-pause'}:
            raise ValueError('unsupported host action')
        argv = ['host.py', action]
        if args.get('id'):
            argv.append(args['id'])
        if 'page' in args:
            argv.append(str(args['page']))
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
    {'name': 'read_file', 'description': 'Read a file inside the sample project. Read PROJECT.md first.',
     'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path']}},
    {'name': 'write_file', 'description': 'Write an authorized sample source or result file. No other filesystem access.',
     'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['path', 'content']}},
    {'name': 'host', 'description': 'Local worker/scheduler fixture API: list returns dependencies; read returns result pages; dispatch runs a job; verify runs the declared check; complete accepts; stop stops only the named worker; archive archives only a session; schedules inspects timers; schedule-create creates one; schedule-pause pauses the named timer.',
     'inputSchema': {'type': 'object', 'properties': {'action': {'type': 'string'}, 'id': {'type': 'string'}, 'page': {'type': 'integer'}}, 'required': ['action']}}
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
