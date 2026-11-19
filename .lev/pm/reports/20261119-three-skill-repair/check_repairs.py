#!/usr/bin/env python3
"""Checks for the 2026-11-19 repair of codex-autoresearch, lev and sitrep.

Structural checks read the instruction text. The codex fixture also runs the
checkpoint block from the protocol in a disposable git repository, so it shows
what the instructed commands do. No check shows model behavior.

Usage:
  check_repairs.py --all                      check the live files (expect pass)
  check_repairs.py --all --baseline DIR       check a baseline snapshot (expect fail)
  check_repairs.py --plant                    plant each fault in a copy (each must fail)
Exit 0 only when every requested check gives the expected result.

Evaluator generation 2 (2026-11-19): generation 1 missed planted faults P3
and P4 (a three-line window let the next YAML line satisfy a help step, and
the word `validate` also matched a handler path). Generation 2 needs the
pointer on the help step's own line and the command as `lev validate`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOME = Path.home()
LIVE = {
    "codex": HOME / ".codex/skills/codex-autoresearch",
    "lev": HOME / ".agents/skills/lev/SKILL.md",
    "sitrep": HOME / ".agents/skills/sitrep/SKILL.md",
}
CODEX_FILES = [
    "SKILL.md",
    "references/loop-workflow.md",
    "references/interaction-wizard.md",
    "references/autonomous-loop-protocol.md",
    "references/core-principles.md",
    "scripts/autoresearch_resume_prompt.py",
]
WHOLE_TREE = re.compile(r"git add (\.|-A|--all)(?=[\s`,\"']|$)|whole current tree|staged autoresearch artifacts are acceptable|as part of `git add")


def section(text: str, heading_re: str) -> str:
    lines = text.splitlines()
    out, inside, level = [], False, 0
    for line in lines:
        m = re.match(r"^(#+) ", line)
        if m and inside and len(m.group(1)) <= level:
            break
        if m and re.search(heading_re, line):
            inside, level = True, len(m.group(1))
        if inside:
            out.append(line)
    return "\n".join(out)


# ---------- codex-autoresearch ----------

def codex_static(root: Path) -> list[str]:
    fails = []
    for rel in CODEX_FILES:
        for n, line in enumerate((root / rel).read_text(encoding="utf-8").splitlines(), 1):
            if WHOLE_TREE.search(line):
                fails.append(f"{rel}:{n} stages the whole tree: {line.strip()[:120]}")
    need = {
        "SKILL.md": (r"git add -- <path>", 2),
        "references/loop-workflow.md": (r"git add -- <path>", 1),
        "references/core-principles.md": (r"git add -- <path>", 1),
        "references/autonomous-loop-protocol.md": (r"git add -- <changed-path>", 1),
        "references/interaction-wizard.md": (r"commit only the files that iteration changed", 1),
        "scripts/autoresearch_resume_prompt.py": (r"git add -- <path>", 1),
    }
    for rel, (pat, count) in need.items():
        found = len(re.findall(re.escape(pat), (root / rel).read_text(encoding="utf-8")))
        if found < count:
            fails.append(f"{rel}: explicit-path staging '{pat}' found {found} time(s), need {count}")
    return fails


def git(cwd: Path, *args: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True)


def codex_fixture(root: Path) -> list[str]:
    proto = (root / "references/autonomous-loop-protocol.md").read_text(encoding="utf-8")
    phase = section(proto, r"Phase 5: Commit")
    m = re.search(r"```bash\n(.*?)```", phase, re.S)
    if not m:
        return ["protocol Phase 5 has no bash block"]
    block = [l.strip() for l in m.group(1).splitlines() if l.strip()]
    tmp = Path(tempfile.mkdtemp(prefix="three-skill-repair-fixture-"))
    try:
        env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
               "HOME": str(tmp), "GIT_TERMINAL_PROMPT": "0"}
        remote, work = tmp / "remote.git", tmp / "work"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], env=env, check=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(work)], env=env, check=True)
        for k, v in [("user.name", "fixture"), ("user.email", "fixture@example.invalid"),
                     ("pull.rebase", "false"), ("core.hooksPath", "/dev/null"), ("commit.gpgsign", "false")]:
            git(work, "config", k, v, env=env)
        (work / "src").mkdir()
        (work / "src/parser.py").write_text("x = 1\n")
        (work / "notes.txt").write_text("base\n")
        git(work, "add", "--", "src/parser.py", "notes.txt", env=env)
        git(work, "commit", "-q", "-m", "base", env=env)
        git(work, "remote", "add", "origin", str(remote), env=env)
        r = git(work, "push", "-q", "-u", "origin", "main", env=env)
        if r.returncode:
            return [f"fixture setup push failed: {r.stderr.strip()}"]
        # Dirt that was there before the iteration, plus the run's own artifacts.
        (work / "notes.txt").write_text("someone else's edit\n")
        git(work, "add", "--", "notes.txt", env=env)
        (work / "other-run").mkdir()
        (work / "other-run/output.json").write_text("{}\n")
        (work / "research-results.tsv").write_text("iteration\tcommit\n")
        # The iteration's own change.
        (work / "src/parser.py").write_text("x = 2\n")
        owned = ["src/parser.py"]
        for line in block:
            line = line.replace("<changed-path>...", " ".join(owned))
            line = line.replace("<what changed and why>", "fixture change")
            if "<" in line:
                return [f"unresolved placeholder in instructed command: {line}"]
            r = subprocess.run(shlex.split(line), cwd=work, env=env, capture_output=True, text=True)
            if r.returncode:
                return [f"instructed command failed: {line}: {r.stderr.strip()[:200]}"]
        pushed = git(remote, "show", "--name-only", "--format=", "main", env=env).stdout.split()
        fails = []
        if sorted(pushed) != owned:
            fails.append(f"pushed commit holds {sorted(pushed)}, expected only {owned}")
        status = git(work, "status", "--porcelain", env=env).stdout
        for p in ["notes.txt", "other-run/", "research-results.tsv"]:
            if p not in status:
                fails.append(f"{p} no longer left dirty and unstaged in the work tree")
        staged = git(work, "diff", "--cached", "--name-only", env=env).stdout.split()
        if staged != ["notes.txt"]:
            fails.append(f"pre-existing staged notes.txt was not preserved: {staged}")
        return fails
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------- lev ----------

def lev_checks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fails = []
    rfm = section(text, r"^## Runtime First Move")
    if not rfm:
        return ["no Runtime First Move section"]
    if "`lev <command> --help`" not in rfm:
        fails.append("Runtime First Move no longer keeps ordinary `lev <command> --help`")
    if "help-unsafe" not in rfm:
        fails.append("Runtime First Move has no help-unsafe definition")
    defn = "\n".join(l for l in rfm.splitlines() if "help-unsafe" in l or re.match(r"^\s{3,}", l))
    for word, why in [("`lev validate`", "names the current help-unsafe command"),
                      ("handler", "says where to read usage without running"),
                      ("diagnostics", "says what to do when --help runs work")]:
        if word not in defn:
            fails.append(f"help-unsafe definition no longer {why} ('{word}' missing)")
    rfm_start = next(i for i, l in enumerate(lines) if l.startswith("## Runtime First Move"))
    rfm_end = rfm_start + len(rfm.splitlines())
    for i, line in enumerate(lines):
        if rfm_start <= i < rfm_end:
            continue
        generic = re.search(r"(<surface>|<command>) --help", line)
        mandatory = "Help-first is mandatory" in line
        if generic or mandatory:
            # A generic help step names the exception on its own line; the
            # 'mandatory' sentence may wrap onto the next line.
            window = line if generic else " ".join(lines[i:i + 2])
            if "help-unsafe" not in window:
                fails.append(f"lev SKILL.md:{i + 1} help step has no help-unsafe pointer: {line.strip()[:100]}")
        if re.search(r"doctor --help` currently runs doctor", line):
            fails.append(f"lev SKILL.md:{i + 1} stale: doctor --help prints help (doctor.ts parses it first)")
        m = re.search(r"`\$LEV (\S+) --help`[^|\n]*?(currently runs|executes)", line)
        if m and f"`lev {m.group(1)}`" not in defn:
            fails.append(f"lev SKILL.md:{i + 1} says `{m.group(1)} --help` runs work but the help-unsafe definition omits it")
    return fails


# ---------- sitrep ----------

def sitrep_checks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails = []
    if "Never mutates" not in text:
        fails.append("read-only statement 'Never mutates' removed")
    if not re.search(r"\*\*Projection only\.\*\* /sitrep never writes", text):
        fails.append("rule 'Projection only' removed")
    sec = section(text, r"^### 3\. Inline")
    if not sec:
        return fails + ["inline shortcut section missing (requests would be dropped)"]
    for n, line in enumerate(sec.splitlines(), 1):
        acts = re.search(r"\b(fire|fires|run|runs|emit|emits)\b", line, re.I)
        target = re.search(r"flow|trigger|://", line, re.I)
        if acts and target and "owner" not in line:
            fails.append(f"inline section line {n}: sitrep itself runs or emits: {line.strip()[:110]}")
    if "skill://lev" not in sec or "owner" not in sec:
        fails.append("inline section no longer routes the request to its owner (skill://lev)")
    return fails


# ---------- runners ----------

def run_all(codex: Path, lev: Path, sitrep: Path) -> dict:
    return {
        "C1.codex_static": codex_static(codex),
        "C1.codex_fixture": codex_fixture(codex),
        "C2.lev": lev_checks(lev),
        "C3.sitrep": sitrep_checks(sitrep),
    }


def mutate(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"plant failed: text not found in {path}: {old[:60]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def plant() -> dict:
    results = {}
    tmp = Path(tempfile.mkdtemp(prefix="three-skill-repair-plant-"))
    try:
        def fresh():
            d = tmp / f"copy{len(results)}"
            (d / "codex").mkdir(parents=True)
            for rel in CODEX_FILES:
                (d / "codex" / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(LIVE["codex"] / rel, d / "codex" / rel)
            shutil.copy2(LIVE["lev"], d / "lev.md")
            shutil.copy2(LIVE["sitrep"], d / "sitrep.md")
            return d
        d = fresh()
        mutate(d / "codex/references/autonomous-loop-protocol.md", "git add -- <changed-path>...", "git add .")
        results["P1"] = codex_static(d / "codex")
        d = fresh()
        mutate(d / "codex/SKILL.md", "(`git add -- <path>...`)", "(`git add .`)")
        results["P2"] = codex_static(d / "codex")
        d = fresh()
        mutate(d / "codex/references/autonomous-loop-protocol.md", 'git commit --only -m "experiment: <what changed and why>" -- <changed-path>...', 'git commit -m "experiment: <what changed and why>"')
        results["P6"] = codex_fixture(d / "codex")
        d = fresh()
        mutate(d / "lev.md", "action: Run `$LEV <surface> --help`, except for a help-unsafe command (Runtime First Move).",
               "action: Run `$LEV <surface> --help`.")
        results["P3"] = lev_checks(d / "lev.md")
        d = fresh()
        mutate(d / "lev.md", "today `lev validate`", "today none")
        results["P4"] = lev_checks(d / "lev.md")
        d = fresh()
        sec = section((d / "sitrep.md").read_text(encoding="utf-8"), r"^### 3\. Inline").splitlines()
        mutate(d / "sitrep.md", sec[-1], sec[-1] + "\n\nInline emotes run a flow (flow://lifecycle/<emote>) but DON'T require /close's full ceremony. They emit a trigger each.")
        results["P5"] = sitrep_checks(d / "sitrep.md")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--baseline", type=Path)
    ap.add_argument("--plant", action="store_true")
    a = ap.parse_args()
    ok = True
    out = {}
    if a.all:
        if a.baseline:
            res = run_all(a.baseline / "codex-autoresearch", a.baseline / "lev-SKILL.md", a.baseline / "sitrep-SKILL.md")
            out["baseline"] = {k: {"red": bool(v), "failures": v} for k, v in res.items()}
            ok &= all(bool(v) for v in res.values())
        else:
            res = run_all(LIVE["codex"], LIVE["lev"], LIVE["sitrep"])
            out["live"] = {k: {"pass": not v, "failures": v} for k, v in res.items()}
            ok &= not any(res.values())
    if a.plant:
        res = plant()
        out["planted"] = {k: {"caught": bool(v), "failures": v} for k, v in res.items()}
        ok &= all(bool(v) for v in res.values())
        live = run_all(LIVE["codex"], LIVE["lev"], LIVE["sitrep"])
        out["restored_live"] = {k: {"pass": not v, "failures": v} for k, v in live.items()}
        ok &= not any(live.values())
    out["result"] = "expected" if ok else "UNEXPECTED"
    print(json.dumps(out, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
