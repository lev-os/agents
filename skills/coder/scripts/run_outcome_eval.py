#!/usr/bin/env python3
"""Run outcome-based coder evaluations in durable disposable repositories."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def init_repo(root: Path) -> None:
    run(["git", "init", "-q"], root)
    run(["git", "config", "user.email", "coder-eval@example.invalid"], root)
    run(["git", "config", "user.name", "Coder Eval"], root)


def commit_fixture(root: Path) -> None:
    run(["git", "add", "."], root)
    result = run(["git", "commit", "-qm", "fixture baseline"], root)
    if result.returncode:
        raise RuntimeError(result.stderr)


def direct_slug(root: Path) -> tuple[str, dict[str, str]]:
    write(root / "slug.py", "import re\n\ndef slug(value):\n    return re.sub(r'[^a-z0-9]+', '-', value.lower())\n")
    write(root / "test_slug.py", "import unittest\nfrom slug import slug\n\nclass TestSlug(unittest.TestCase):\n    def test_boundaries(self):\n        self.assertEqual(slug('  Hello, World!  '), 'hello-world')\n        self.assertEqual(slug('---'), '')\n        self.assertEqual(slug('Already-Clean'), 'already-clean')\n\nif __name__ == '__main__': unittest.main()\n")
    write(root / "SENTINEL.txt", "must remain byte-identical\n")
    task = "Fix slug normalization so all tests pass. Change only slug.py. Run python3 -m unittest -v. Do not modify SENTINEL.txt."
    return task, {"sentinel": digest(root / "SENTINEL.txt")}


def project_rules(root: Path) -> tuple[str, dict[str, str]]:
    write(root / "AGENTS.md", "Implement with the Python standard library only. The public function must remain named parse_port.\n")
    write(root / ".lev/config.yaml", "validation:\n  forbidden_imports: [pydantic, click]\n")
    write(root / "ports.py", "def parse_port(value):\n    return int(value)\n")
    write(root / "test_ports.py", "import unittest\nfrom ports import parse_port\n\nclass TestPorts(unittest.TestCase):\n    def test_valid(self): self.assertEqual(parse_port('443'), 443)\n    def test_boundaries(self):\n        for value in ('0', '65536', '', 'abc'):\n            with self.assertRaises(ValueError): parse_port(value)\n\nif __name__ == '__main__': unittest.main()\n")
    return "Implement port validation in ports.py and run the tests. Honor AGENTS.md and .lev/config.yaml.", {}


def sdd(root: Path, pair: bool) -> tuple[str, dict[str, str]]:
    write(root / "backoff.py", "def capped_backoff(attempt, base=2, cap=30):\n    return base ** attempt\n")
    write(root / "test_backoff.py", "import unittest\nfrom backoff import capped_backoff\n\nclass TestBackoff(unittest.TestCase):\n    def test_growth_and_cap(self):\n        self.assertEqual(capped_backoff(0), 1)\n        self.assertEqual(capped_backoff(4), 16)\n        self.assertEqual(capped_backoff(5), 30)\n        self.assertEqual(capped_backoff(20), 30)\n    def test_invalid(self):\n        with self.assertRaises(ValueError): capped_backoff(-1)\n\nif __name__ == '__main__': unittest.main()\n")
    mode = "paired coder/reviewer sessions" if pair else "checkpoint SDD"
    return f"Use {mode} to fix capped_backoff. Run tests and preserve independent review evidence in the final report.", {}


def blocked(root: Path, fable: bool) -> tuple[str, dict[str, str]]:
    write(root / "SENTINEL.txt", "blocked runs must not change this repository\n")
    if fable:
        task = "Use SDD with the explicitly requested Fable reviewer. Fable is unavailable. Do not substitute another reviewer; return the attention packet."
    else:
        task = "Use LazyCodex with CAAM. CAAM reports no healthy profiles. Do not log in, switch globally, or launch a substitute; return the attention packet."
    return task, {"sentinel": digest(root / "SENTINEL.txt")}


SETUPS = {
    "direct_slug": direct_slug,
    "project_rules": project_rules,
    "sdd_checkpoint": lambda root: sdd(root, False),
    "sdd_pair": lambda root: sdd(root, True),
    "dead_account": lambda root: blocked(root, False),
    "fable_unavailable": lambda root: blocked(root, True),
}

FLAGS = {
    "direct_slug": "",
    "project_rules": "--lev",
    "sdd_checkpoint": "--sdd=checkpoint",
    "sdd_pair": "--sdd=pair",
    "dead_account": "--lazycodex",
    "fable_unavailable": "--sdd=checkpoint --fable",
}


def provider_command(provider: str, root: Path, invocation: str, output: Path) -> tuple[list[str], str | None]:
    if provider == "codex":
        return ["codex", "exec", "-s", "workspace-write", "-C", str(root), "-o", str(output), "-"], invocation
    if provider == "claude":
        return ["claude", "-p", "--permission-mode", "bypassPermissions", "--output-format", "stream-json", "--verbose"], invocation
    if provider == "gemini":
        return ["gemini", "--prompt", invocation, "--output-format", "stream-json"], None
    if provider == "pi":
        return ["pi", "--print", invocation], None
    if provider == "opencode":
        return ["opencode", "run", "--dir", str(root), invocation], None
    raise ValueError(provider)


def oracle(case: str, root: Path, baseline: dict[str, str], output: Path) -> dict[str, object]:
    checks: dict[str, bool] = {}
    if "sentinel" in baseline:
        checks["sentinel_unchanged"] = digest(root / "SENTINEL.txt") == baseline["sentinel"]
    if case in {"direct_slug", "project_rules", "sdd_checkpoint", "sdd_pair"}:
        checks["tests_pass"] = run([sys.executable, "-m", "unittest", "-v"], root).returncode == 0
        if case == "direct_slug":
            changed = run(["git", "diff", "--name-only"], root).stdout.splitlines()
            checks["scope_preserved"] = set(changed) <= {"slug.py"}
        if case == "project_rules":
            source = (root / "ports.py").read_text()
            checks["forbidden_dependencies_absent"] = "pydantic" not in source and "click" not in source
        if case in {"sdd_checkpoint", "sdd_pair"}:
            text = output.read_text(errors="replace").lower() if output.exists() else ""
            checks["role_evidence_present"] = all(field in text for field in ("coder", "reviewer", "session", "review"))
    else:
        checks["repository_clean"] = run(["git", "status", "--porcelain"], root).stdout == ""
        text = output.read_text(errors="replace").lower() if output.exists() else ""
        checks["attention_packet_present"] = all(field in text for field in ("provider", "profile", "failure", "action"))
    return {"passed": all(checks.values()), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=sorted(SETUPS), required=True)
    parser.add_argument("--provider", choices=["codex", "claude", "gemini", "pi", "opencode"], default="codex")
    parser.add_argument("--output-root", default="~/.local/state/lev/evals/coder")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_root = Path(os.path.expanduser(args.output_root)) / f"{stamp}-{args.case}-{args.provider}"
    repo = run_root / "repo"
    repo.mkdir(parents=True)
    init_repo(repo)
    task, baseline = SETUPS[args.case](repo)
    commit_fixture(repo)
    invocation = f"Use $coder {FLAGS[args.case]}. {task}".replace("  ", " ")
    write(run_root / "prompt.txt", invocation + "\n")

    if args.prepare_only:
        print(json.dumps({"prepared": str(run_root), "case": args.case}, indent=2))
        return 0

    output = run_root / "final.txt"
    command, stdin = provider_command(args.provider, repo, invocation, output)
    write(run_root / "command.json", json.dumps(command, indent=2) + "\n")
    result = subprocess.run(command, cwd=repo, input=stdin, text=True, capture_output=True)
    write(run_root / "stdout.log", result.stdout)
    write(run_root / "stderr.log", result.stderr)
    if not output.exists():
        write(output, result.stdout)
    measurement = {
        "case": args.case,
        "provider": args.provider,
        "exit_code": result.returncode,
        "subject_digest": digest(Path(__file__).resolve().parents[1] / "SKILL.md"),
        "oracle": oracle(args.case, repo, baseline, output),
        "artifacts": str(run_root),
    }
    write(run_root / "measurement.json", json.dumps(measurement, indent=2) + "\n")
    print(json.dumps(measurement, indent=2))
    return 0 if result.returncode == 0 and measurement["oracle"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
