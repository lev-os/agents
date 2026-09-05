#!/usr/bin/env python3
"""Deterministic contract checks for the coder skill package."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(path: Path, needles: list[str]) -> list[str]:
    text = path.read_text()
    return [f"{path.relative_to(ROOT)} missing {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    failures: list[str] = []
    failures += require(ROOT / "SKILL.md", [
        "name: coder", "caam list --json", "lev exec --help",
        "same blocker twice", "Never expose tokens",
        "--sdd=checkpoint", "--sdd=pair", "--lazycodex", "--fable",
        "thread.started.thread_id", "lazycodex-worker-low|medium|high",
        "Luna `max`", "Sol `medium`", "references/claude.md",
        "references/pi.md", "references/opencode.md", "--disable fast_mode",
        "resume` surface has no `-C`", "non-overlapping scope",
        "--include-partial-messages", "type: \"result\"",
        "skill://exec", "skill://work", "lev://exec/<flow>",
        "lev://entity/work/task/<id>", "lev://subagent/<workstream>/<role>",
        "Gemini direct fallback", "live 401", "overrides a passive `valid`",
    ])
    failures += require(ROOT / "references/claude.md", [
        "stream-json", "macOS Claude Code keychain", "global activation",
    ])
    failures += require(ROOT / "references/pi.md", [
        "Lev-flavored Pi", "--no-extensions", "identity boundary as unverified",
    ])

    skills_root = ROOT.parent
    failures += require(skills_root / "coding-agent/SKILL.md", ["$coder", "Compatibility"])
    failures += require(skills_root / "codex-runner/SKILL.md", ["$coder --lazycodex", "Compatibility"])
    failures += require(skills_root / "subagent-driven-development/SKILL.md", ["$coder --sdd=checkpoint", "Compatibility"])
    failures += require(skills_root / "goal-exec/SKILL.md", ["--coder", "--sdd=checkpoint", "Tools: $coder"])

    if failures:
        print("coder contract: FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("coder contract: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
