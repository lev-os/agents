#!/usr/bin/env python3
"""
Scan session history for synths: [] declarations in message footers.

Synth Protocol:
- Agents declare synths in their responses: synths: ["name1", "name2"]
- This script finds all synth declarations across session history
- Outputs candidates for materialization

Usage:
    python scan_session_synths.py [session_dir]
    python scan_session_synths.py --all
    python scan_session_synths.py --min-count 3  # Only synths used 3+ times
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

# Common session history locations
SESSION_PATHS = [
    Path.home() / ".claude" / "projects",
    Path.home() / ".lev" / "sessions",
    Path.home() / "clawd" / "sessions",
]

# Pattern to match synths: ["name1", "name2"] in message content
SYNTH_PATTERN = re.compile(
    r'synths:\s*\[([^\]]*)\]',
    re.IGNORECASE | re.MULTILINE
)

# Pattern to extract individual synth names
SYNTH_NAME_PATTERN = re.compile(r'["\']([^"\']+)["\']')


def find_session_files(base_path: Path) -> list[Path]:
    """Find all session history files (JSONL, JSON, MD)."""
    files = []
    for ext in ["*.jsonl", "*.json", "*history*.md", "*session*.md"]:
        files.extend(base_path.rglob(ext))
    return files


def extract_synths_from_content(content: str) -> list[str]:
    """Extract synth names from message content."""
    synths = []
    for match in SYNTH_PATTERN.finditer(content):
        synth_list_str = match.group(1)
        names = SYNTH_NAME_PATTERN.findall(synth_list_str)
        synths.extend(names)
    return synths


def scan_jsonl_file(filepath: Path) -> dict:
    """Scan a JSONL session file for synths."""
    synths_found = defaultdict(list)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                    content = ""

                    # Handle different message formats
                    if isinstance(msg, dict):
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            content = " ".join(
                                c.get("text", "") if isinstance(c, dict) else str(c)
                                for c in content
                            )
                        content = str(content)

                    synths = extract_synths_from_content(content)
                    for synth in synths:
                        synths_found[synth].append({
                            "file": str(filepath),
                            "line": line_num,
                            "timestamp": msg.get("timestamp", "unknown")
                        })
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return synths_found


def scan_markdown_file(filepath: Path) -> dict:
    """Scan a Markdown session file for synths."""
    synths_found = defaultdict(list)

    try:
        content = filepath.read_text(encoding='utf-8')
        synths = extract_synths_from_content(content)
        for synth in synths:
            synths_found[synth].append({
                "file": str(filepath),
                "line": 0,  # Markdown doesn't track line numbers well
                "timestamp": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            })
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return synths_found


def scan_sessions(paths: list[Path], min_count: int = 1) -> dict:
    """Scan all session paths for synths."""
    all_synths = defaultdict(list)
    files_scanned = 0

    for base_path in paths:
        if not base_path.exists():
            continue

        for filepath in find_session_files(base_path):
            files_scanned += 1

            if filepath.suffix == ".jsonl":
                synths = scan_jsonl_file(filepath)
            elif filepath.suffix in [".json", ".md"]:
                synths = scan_markdown_file(filepath)
            else:
                continue

            for name, occurrences in synths.items():
                all_synths[name].extend(occurrences)

    # Filter by min_count
    filtered = {
        name: occs for name, occs in all_synths.items()
        if len(occs) >= min_count
    }

    return {
        "synths": filtered,
        "files_scanned": files_scanned,
        "total_synths_found": len(all_synths),
        "synths_meeting_threshold": len(filtered)
    }


def format_output(results: dict, format_type: str = "table") -> str:
    """Format results for display."""
    if format_type == "json":
        return json.dumps(results, indent=2)

    # Table format
    lines = [
        f"Files scanned: {results['files_scanned']}",
        f"Total unique synths: {results['total_synths_found']}",
        f"Synths meeting threshold: {results['synths_meeting_threshold']}",
        "",
        "Synth Name                    | Count | First Seen",
        "-" * 60
    ]

    sorted_synths = sorted(
        results['synths'].items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    for name, occurrences in sorted_synths:
        first_seen = occurrences[0].get('timestamp', 'unknown')[:10]
        lines.append(f"{name:<30} | {len(occurrences):>5} | {first_seen}")

    if not sorted_synths:
        lines.append("No synths found matching criteria")

    lines.extend([
        "",
        "To materialize a synth:",
        "  lev build synth --name <synth-name> --from-session",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan session history for synth declarations"
    )
    parser.add_argument(
        "session_dir",
        nargs="?",
        help="Specific session directory to scan"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Scan all known session locations"
    )
    parser.add_argument(
        "--min-count", "-m",
        type=int,
        default=1,
        help="Minimum occurrences to include (default: 1)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    if args.session_dir:
        paths = [Path(args.session_dir)]
    elif args.all:
        paths = SESSION_PATHS
    else:
        # Default: current project sessions
        paths = [Path.cwd() / ".claude", Path.cwd() / ".lev"]

    results = scan_sessions(paths, min_count=args.min_count)

    output_format = "json" if args.json else "table"
    print(format_output(results, output_format))


if __name__ == "__main__":
    main()
