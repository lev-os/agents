#!/usr/bin/env python3
"""
skill-decompile: FlowMind SKILL.md -> deterministic YAML for security analysis.

Usage:
    python3 decompile.py <skill.md> [--output yaml|json] [--verbose]
    python3 decompile.py --dir <path> [--report] [--output yaml|json]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

URL_RE = re.compile(r'https?://[^\s\)\]\>\"\'\`]+')
ENV_RE = re.compile(r'(?:\$\{?|\bprocess\.env\.)([A-Z_][A-Z0-9_]*)\}?')
FILE_PATH_RE = re.compile(
    r'(?:^|[\s\`\"\'])([~./][\w./_-]+(?:\.[\w]+)?)', re.MULTILINE
)
CODE_BLOCK_RE = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)

PROMPT_INJECTION_RE = re.compile(
    r'(?:ignore\s+(?:all\s+)?previous|you\s+are\s+now|disregard\s+(?:all\s+)?'
    r'(?:prior|previous)|forget\s+(?:all\s+)?(?:prior|previous)|override\s+'
    r'(?:system|instructions))',
    re.IGNORECASE,
)

EVAL_RE = re.compile(r'\b(?:eval|exec|compile|__import__)\s*\(')
BASE64_LONG_RE = re.compile(r'[A-Za-z0-9+/=]{100,}')
OBFUSCATION_RE = re.compile(
    r'(?:\\x[0-9a-fA-F]{2}){4,}|(?:\\u[0-9a-fA-F]{4}){3,}'
)

SAFE_DOMAINS = {'github.com', 'npmjs.com', 'pypi.org', 'localhost', '127.0.0.1'}
LOCAL_HOSTS = {'localhost', '127.0.0.1', '0.0.0.0', '::1'}

FS_MODIFY_RE = re.compile(
    r'\b(?:rm\s|rmdir\s|mv\s|cp\s.*?/(?:usr|etc|sys|boot|var))'
)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from a SKILL.md."""
    fm = {}
    body = text
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)', text, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            fm = {}
        body = match.group(2)
    return fm, body


def extract_code_blocks(body: str) -> list[dict]:
    """Return list of {lang, code} dicts."""
    return [
        {'lang': m.group(1) or 'unknown', 'code': m.group(2)}
        for m in CODE_BLOCK_RE.finditer(body)
    ]


def extract_urls(text: str) -> list[str]:
    return sorted(set(URL_RE.findall(text)))


def extract_env_vars(text: str) -> list[str]:
    return sorted(set(ENV_RE.findall(text)))


def extract_file_paths(text: str) -> list[str]:
    raw = FILE_PATH_RE.findall(text)
    # Filter noise: must have at least one slash or tilde
    return sorted(set(p for p in raw if '/' in p or p.startswith('~')))


def extract_shell_commands(code_blocks: list[dict]) -> list[str]:
    cmds = []
    for block in code_blocks:
        if block['lang'] in ('bash', 'sh', 'shell', 'zsh', 'unknown', ''):
            for line in block['code'].strip().splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    cmds.append(line)
    return cmds


def measure_decision_depth(body: str) -> int:
    """Rough heuristic: deepest nesting of decision-tree-like lines."""
    max_depth = 0
    for line in body.splitlines():
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        markers = ('├', '└', '│', '- if', '- else', '→')
        if any(m in stripped for m in markers):
            depth = indent // 2
            max_depth = max(max_depth, depth)
    return max_depth


# ---------------------------------------------------------------------------
# Risk scoring
# ---------------------------------------------------------------------------

def compute_risk(
    urls: list[str],
    env_vars: list[str],
    shell_commands: list[str],
    has_eval: bool,
    has_base64: bool,
    has_obfuscation: bool,
    has_prompt_injection: bool,
    allowed_tools: list[str],
    body: str,
) -> tuple[int, list[str]]:
    score = 0
    flags: list[str] = []

    # URL scoring
    for url in urls:
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            host = parsed.hostname or ''
        except Exception:
            host = ''
        if host in LOCAL_HOSTS:
            pass  # +0
        elif any(host.endswith(d) for d in SAFE_DOMAINS):
            score += 2  # 5 - 3
        else:
            score += 5
            flags.append(f'external_url: {url}')

    # eval/exec
    if has_eval:
        score += 20
        flags.append('eval_exec_pattern_detected')

    # base64 blobs
    if has_base64:
        score += 30
        flags.append('long_base64_blob')

    # obfuscation
    if has_obfuscation:
        score += 25
        flags.append('obfuscation_detected')

    # prompt injection
    if has_prompt_injection:
        score += 25
        flags.append('prompt_injection_pattern')

    # env vars
    if env_vars:
        score += 15
        flags.append(f'env_var_access: {", ".join(env_vars)}')

    # unrestricted tools
    if 'unrestricted' in allowed_tools:
        score += 10
        flags.append('unrestricted_tool_access')

    # dangerous shell commands
    for cmd in shell_commands:
        if FS_MODIFY_RE.search(cmd):
            score += 5
            flags.append(f'fs_modify_cmd: {cmd[:80]}')

    # exfil pattern: curl/wget to non-safe URLs
    has_exfil = False
    for cmd in shell_commands:
        if re.search(r'\b(?:curl|wget)\b', cmd):
            cmd_urls = URL_RE.findall(cmd)
            for u in cmd_urls:
                from urllib.parse import urlparse as _up
                try:
                    h = (_up(u).hostname or '')
                except Exception:
                    h = ''
                if h and h not in LOCAL_HOSTS and not any(
                    h.endswith(d) for d in SAFE_DOMAINS
                ):
                    has_exfil = True
                    flags.append(f'exfil_pattern: {cmd[:80]}')

    if has_exfil:
        score += 10

    return min(score, 100), flags


def risk_level(score: int) -> str:
    if score <= 20:
        return 'safe'
    if score <= 40:
        return 'low'
    if score <= 60:
        return 'medium'
    if score <= 80:
        return 'high'
    return 'critical'


# ---------------------------------------------------------------------------
# Core decompile
# ---------------------------------------------------------------------------

def decompile(skill_path: str, verbose: bool = False) -> dict:
    text = Path(skill_path).read_text(encoding='utf-8', errors='replace')
    fm, body = parse_frontmatter(text)

    code_blocks = extract_code_blocks(body)
    urls = extract_urls(text)
    env_vars = extract_env_vars(text)
    file_paths = extract_file_paths(body)
    shell_commands = extract_shell_commands(code_blocks)

    # Permissions from frontmatter
    raw_tools = fm.get('allowed-tools', fm.get('allowed_tools', ''))
    if isinstance(raw_tools, list):
        allowed_tools = raw_tools if raw_tools else ['unrestricted']
    elif isinstance(raw_tools, str) and raw_tools.strip():
        allowed_tools = [t.strip() for t in raw_tools.split(',')]
    else:
        allowed_tools = ['unrestricted']

    has_eval = bool(EVAL_RE.search(text))
    has_base64 = bool(BASE64_LONG_RE.search(text))
    has_obfuscation = bool(OBFUSCATION_RE.search(text))
    has_prompt_injection = bool(PROMPT_INJECTION_RE.search(text))

    requests_bash = bool(shell_commands) or bool(
        re.search(r'\b(?:bash|shell|terminal|command.line)\b', body, re.I)
    )
    requests_write = bool(
        re.search(r'\b(?:Write|create.*file|save.*to|write.*to)\b', body, re.I)
    )
    requests_network = bool(urls) or bool(
        re.search(r'\b(?:fetch|curl|wget|http|request)\b', body, re.I)
    )
    requests_env = bool(env_vars)

    # Exfil detection
    has_exfil = False
    for cmd in shell_commands:
        if re.search(r'\b(?:curl|wget)\b', cmd):
            cmd_urls = URL_RE.findall(cmd)
            for u in cmd_urls:
                from urllib.parse import urlparse
                try:
                    h = (urlparse(u).hostname or '')
                except Exception:
                    h = ''
                if h and h not in LOCAL_HOSTS and not any(
                    h.endswith(d) for d in SAFE_DOMAINS
                ):
                    has_exfil = True

    # Reference files (files loaded/referenced in the skill)
    ref_files = [p for p in file_paths if any(
        p.endswith(ext) for ext in (
            '.md', '.yaml', '.yml', '.json', '.ts', '.js', '.py', '.sh',
            '.flow.yaml', '.toml',
        )
    )]

    score, flags = compute_risk(
        urls, env_vars, shell_commands,
        has_eval, has_base64, has_obfuscation, has_prompt_injection,
        allowed_tools, body,
    )

    source = 'local'
    for u in urls:
        from urllib.parse import urlparse as _up2
        try:
            h = (_up2(u).hostname or '')
        except Exception:
            h = ''
        if h and h not in LOCAL_HOSTS:
            source = 'external'
            break

    result = {
        'meta': {
            'name': fm.get('name', Path(skill_path).parent.name),
            'description': fm.get('description', ''),
            'skill_type': fm.get('skill_type', 'leaf'),
            'source': source,
        },
        'permissions': {
            'allowed_tools': allowed_tools,
            'requests_bash': requests_bash,
            'requests_write': requests_write,
            'requests_network': requests_network,
            'requests_env': requests_env,
        },
        'surfaces': {
            'urls': urls,
            'shell_commands': shell_commands,
            'env_vars': env_vars,
            'file_paths': file_paths,
        },
        'risk_signals': {
            'has_eval': has_eval,
            'has_base64': has_base64,
            'has_obfuscation': has_obfuscation,
            'has_exfil_pattern': has_exfil,
            'has_prompt_injection': has_prompt_injection,
        },
        'complexity': {
            'line_count': len(text.splitlines()),
            'code_block_count': len(code_blocks),
            'reference_file_count': len(ref_files),
            'decision_tree_depth': measure_decision_depth(body),
        },
        'verdict': {
            'risk_score': score,
            'risk_level': risk_level(score),
            'flags': flags,
        },
    }

    if verbose:
        result['_debug'] = {
            'frontmatter_keys': list(fm.keys()),
            'code_block_langs': [b['lang'] for b in code_blocks],
            'ref_files': ref_files,
        }

    return result


# ---------------------------------------------------------------------------
# Directory scan + report
# ---------------------------------------------------------------------------

def scan_directory(dir_path: str, verbose: bool = False) -> list[dict]:
    results = []
    root = Path(dir_path).expanduser().resolve()
    for skill_md in sorted(root.rglob('SKILL.md')):
        try:
            result = decompile(str(skill_md), verbose=verbose)
            result['_source_path'] = str(skill_md)
            results.append(result)
        except Exception as e:
            results.append({
                '_source_path': str(skill_md),
                '_error': str(e),
            })
    return results


def print_report(results: list[dict]) -> None:
    """Print a summary table to stdout."""
    # Header
    header = f'{"Skill":<30} {"Type":<12} {"Risk":>5} {"Level":<10} {"Flags"}'
    print('\n' + '=' * 90)
    print('  SKILL DECOMPILE — Security Report')
    print('=' * 90)
    print(header)
    print('-' * 90)

    for r in results:
        if '_error' in r:
            name = Path(r['_source_path']).parent.name
            print(f'{name:<30} {"ERROR":<12} {"?":<5} {"error":<10} {r["_error"]}')
            continue

        name = r['meta']['name'][:29]
        stype = r['meta']['skill_type'][:11]
        score = r['verdict']['risk_score']
        level = r['verdict']['risk_level']
        n_flags = len(r['verdict']['flags'])
        flag_summary = f'{n_flags} flag(s)' if n_flags else '-'
        print(f'{name:<30} {stype:<12} {score:>5} {level:<10} {flag_summary}')

    print('-' * 90)
    total = len(results)
    errors = sum(1 for r in results if '_error' in r)
    by_level = {}
    for r in results:
        if '_error' not in r:
            lvl = r['verdict']['risk_level']
            by_level[lvl] = by_level.get(lvl, 0) + 1

    print(f'Total: {total} | Errors: {errors} | '
          + ' | '.join(f'{k}: {v}' for k, v in sorted(by_level.items())))
    print('=' * 90 + '\n')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Decompile SKILL.md files into structured YAML for security analysis.',
    )
    parser.add_argument('skill', nargs='?', help='Path to a SKILL.md file')
    parser.add_argument('--dir', help='Scan a directory for all SKILL.md files')
    parser.add_argument(
        '--output', choices=['yaml', 'json'], default='yaml',
        help='Output format (default: yaml)',
    )
    parser.add_argument('--report', action='store_true', help='Print summary report table')
    parser.add_argument('--verbose', action='store_true', help='Include debug info')

    args = parser.parse_args()

    if not args.skill and not args.dir:
        parser.print_help()
        sys.exit(1)

    if args.dir:
        results = scan_directory(args.dir, verbose=args.verbose)
        if args.report:
            print_report(results)
        else:
            output = [r for r in results]
            if args.output == 'json':
                print(json.dumps(output, indent=2, default=str))
            else:
                print(yaml.dump(output, default_flow_style=False, sort_keys=False))
    else:
        skill_path = args.skill
        if not Path(skill_path).exists():
            print(f'Error: {skill_path} not found', file=sys.stderr)
            sys.exit(1)
        result = decompile(skill_path, verbose=args.verbose)
        if args.output == 'json':
            print(json.dumps(result, indent=2, default=str))
        else:
            # Add header comment
            print('# Auto-generated by skill-decompile')
            print(yaml.dump(result, default_flow_style=False, sort_keys=False))


if __name__ == '__main__':
    main()
