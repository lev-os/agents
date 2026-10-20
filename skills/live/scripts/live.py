#!/usr/bin/env python3
"""Local JSON progress views. Standard library only; no task execution."""
import argparse
from datetime import datetime, timezone
import fcntl
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import socket
import tempfile
from urllib.parse import quote, urlsplit
from urllib.request import urlopen
import uuid


def read(path):
    return json.loads(Path(path).read_text())


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as out:
            name = out.name
            out.write(text)
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def write(path, value):
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('status document must be an object')
    if data.get('schema_version') != 1:
        raise ValueError('schema_version must be 1')
    if type(data.get('revision')) is not int or data['revision'] < 0:
        raise ValueError('revision must be a nonnegative integer')
    reports = data.get('reports')
    if not isinstance(reports, dict) or data.get('root_report') not in reports:
        raise ValueError('root_report must name an existing report')
    for key, report in reports.items():
        if not isinstance(report, dict):
            raise ValueError('report must be an object')
        if not isinstance(key, str) or not key or '::' in key or report.get('id') != key:
            raise ValueError('report IDs must match map keys and reserve :: for detail routes')
        if not isinstance(report.get('title'), str) or not report['title']:
            raise ValueError('every report needs a title')
        if not isinstance(report.get('items'), list):
            raise ValueError('every report needs an items list')
        ids = set()
        for item in report['items']:
            if not isinstance(item, dict):
                raise ValueError('item must be an object')
            item_id = item.get('id')
            if not isinstance(item_id, str) or not item_id or item_id in ids or '::' in item_id:
                raise ValueError('item IDs must be unique within a report and reserve ::')
            if not isinstance(item.get('title'), str):
                raise ValueError('every item needs a title')
            ids.add(item_id)
            if item.get('report') and item['report'] not in reports:
                raise ValueError('item references an absent report')
        for node in [report, *report['items']]:
            for link in node.get('links', []):
                if link.get('kind') == 'external':
                    if urlsplit(link.get('href', '')).scheme not in {'http', 'https', 't3-thread', 'lev'}:
                        raise ValueError('external links need an allowed URL scheme')
                else:
                    path = link.get('path', '')
                    if not isinstance(path, str) or not path or urlsplit(path).scheme or path.startswith('/') or '..' in Path(path).parts:
                        raise ValueError('document links must stay relative to the declared document root')
        seen = {key}
        parent = report.get('parent')
        while parent:
            if parent not in reports or parent in seen:
                raise ValueError('report parents must resolve without a cycle')
            seen.add(parent)
            parent = reports[parent].get('parent')
    if reports[data['root_report']].get('parent'):
        raise ValueError('root report cannot have a parent')
    return data


def merge(target, patch):
    if not isinstance(patch, dict):
        return patch
    target = dict(target) if isinstance(target, dict) else {}
    for key, value in patch.items():
        if value is None:
            target.pop(key, None)
        else:
            target[key] = merge(target.get(key), value)
    return target


def render(args):
    source, output = Path(args.data).resolve(), Path(args.out).resolve()
    if source == output:
        raise ValueError('HTML output cannot overwrite its JSON input')
    data = validate(read(source))
    reference = read(args.reference) if args.reference else {'children': []}
    if not isinstance(reference, dict) or not isinstance(reference.get('children'), list):
        raise ValueError('reference must contain a children list')
    template = Path(__file__).resolve().parents[1] / 'assets/template.html'
    html = template.read_text()
    for marker, value in [('__STATUS__', data), ('__REFERENCE__', reference),
                          ('__DATA_URL__', os.path.relpath(source, output.parent))]:
        html = html.replace(marker, json.dumps(value, ensure_ascii=False).replace('<', '\\u003c'))
    write_text(output, html)
    return {'html': str(output), 'revision': data['revision'], 'reports': len(data['reports'])}


def status(path):
    state = read(path)
    if state.get('hostname') != socket.gethostname():
        return {**state, 'running': False, 'reason': 'state belongs to another host'}
    try:
        if state.get('server_id'):
            base = '{uri.scheme}://{uri.netloc}'.format(uri=urlsplit(state['url']))
            with urlopen(base + '/__live__/health', timeout=2) as response:
                health = json.load(response)
            running = health.get('server_id') == state['server_id'] and health.get('pid') == state['pid']
        else:
            os.kill(state['pid'], 0)
            with urlopen(state['url'], timeout=2) as response:
                running = response.status == 200
        return {**state, 'running': running}
    except (OSError, ValueError, KeyError) as error:
        return {**state, 'running': False, 'reason': str(error)}


def serve(args):
    root = Path(args.root).resolve()
    page = (root / args.page).resolve()
    if not page.is_relative_to(root) or not page.is_file():
        raise ValueError('page must be an existing file inside root')
    state_path = Path(args.state).resolve()
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # One local starter at a time. Lock lives outside served content where possible.
    with state_path.with_suffix(state_path.suffix + '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if state_path.exists():
            old = status(state_path)
            if old['running']:
                if Path(old['content_root']).resolve() != root:
                    raise ValueError('state already belongs to another running report server')
                uri = urlsplit(old['url'])
                old['url'] = f'{uri.scheme}://{uri.netloc}/' + quote(str(page.relative_to(root)))
                print(json.dumps({**old, 'reused': True}), flush=True)
                return
        server_id = str(uuid.uuid4())

        class Handler(SimpleHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                if urlsplit(self.path).path == '/__live__/health':
                    content = json.dumps({'server_id': server_id, 'pid': os.getpid()}).encode()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    super().do_GET()

            def send_head(self):
                if not Path(self.translate_path(self.path)).resolve().is_relative_to(root):
                    self.send_error(403)
                    return None
                return super().send_head()

            def list_directory(self, _):
                self.send_error(403)
                return None

            def end_headers(self):
                self.send_header('Cache-Control', 'no-store')
                super().end_headers()

        server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(root)))
        port = server.server_address[1]
        info = {'pid': os.getpid(), 'hostname': socket.gethostname(), 'bind': '127.0.0.1',
                'port': port, 'url': f'http://127.0.0.1:{port}/' + quote(str(page.relative_to(root))),
                'content_root': str(root), 'server_id': server_id,
                'started_at': datetime.now(timezone.utc).isoformat()}
        write(state_path, info)
    print(json.dumps(info), flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Create an empty status document without overwriting one')
    init.add_argument('--data', required=True)
    init.add_argument('--title', required=True)
    rendering = sub.add_parser('render', help='Embed JSON in the portable HTML template')
    rendering.add_argument('--data', required=True)
    rendering.add_argument('--out', required=True)
    rendering.add_argument('--reference')
    update = sub.add_parser('update', help='Validate and atomically apply a JSON merge patch from stdin')
    update.add_argument('--data', required=True)
    update.add_argument('--expect-revision', required=True, type=int)
    serving = sub.add_parser('serve', help='Run a read-only loopback server in the foreground')
    serving.add_argument('--root', required=True)
    serving.add_argument('--page', required=True)
    serving.add_argument('--state', required=True)
    serving.add_argument('--port', type=int, default=0)
    checking = sub.add_parser('status', help='Check the recorded report server once')
    checking.add_argument('--state', required=True)
    stopping = sub.add_parser('stop', help='Stop a matching live-owned server')
    stopping.add_argument('--state', required=True)
    args = parser.parse_args()
    if args.command == 'init':
        target = Path(args.data)
        if target.exists():
            raise ValueError('status document already exists')
        report = {'id': 'overview', 'parent': None, 'title': args.title, 'status': 'pending',
                  'subtitle': 'No work has been reported yet.', 'items': [], 'body': [], 'links': []}
        data = {'schema_version': 1, 'revision': 0, 'updated_at': datetime.now(timezone.utc).isoformat(),
                'root_report': 'overview', 'reports': {'overview': report}, 'project': {'title': args.title},
                'orchestrator': {'current': 'No work has been reported yet.'}, 'proof': {}, 'links': {}}
        write(target, validate(data))
        result = {'data': str(target), 'revision': 0}
    elif args.command == 'render':
        result = render(args)
    elif args.command == 'update':
        import sys
        target = Path(args.data)
        patch = json.load(sys.stdin)
        if not isinstance(patch, dict) or any(key in patch for key in ['revision', 'updated_at']):
            raise ValueError('patch must be an object; revision and updated_at are managed')
        with target.with_suffix(target.suffix + '.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            before = validate(read(target))
            if before['revision'] != args.expect_revision:
                raise ValueError('revision changed; reread the current document before retrying')
            after = merge(before, patch)
            after['revision'] = before['revision'] + 1
            after['updated_at'] = datetime.now(timezone.utc).isoformat()
            write(target, validate(after))
        result = {'data': str(target), 'revision': after['revision']}
    elif args.command == 'serve':
        serve(args)
        return
    elif args.command == 'status':
        result = status(args.state)
    else:
        record = status(args.state)
        if not record.get('server_id') or not record['running']:
            raise ValueError('no matching live-owned server; no process was stopped')
        os.kill(record['pid'], signal.SIGTERM)
        result = {'stop_sent': True, 'pid': record['pid']}
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        import sys
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        sys.exit(1)
