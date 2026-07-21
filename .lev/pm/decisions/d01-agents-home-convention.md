---
id: "d01"
title: "AGENTS_HOME path convention for skill references"
type: decision
status: accepted
created: 2026-07-18T01:20:00
updated: 2026-07-18T01:20:00
tags: [decision, conventions, portability, skills]
related_docs: [.lev/workshop/analysis/shaping-skills/analysis.md]
---

# ADR: AGENTS_HOME path convention for skill references

## Status

accepted

## Context

The repo supports multiple agent runtimes (Claude Code, Codex, and others), so
skills cannot assume `~/.claude/` layouts, and CI's hardcoded-path check fails
on any literal `/Users/<name>/` or `/home/<name>/` path. Six skill files and
several `levnow/*.json` reports currently violate this. The upstream
shaping-skills package also hardcodes `~/.claude/skills/` paths that must be
rewritten during adaptation.

We also want to run multiple agent-home *instances* (per-project or per-container
sandboxes) besides the single global default, which rules out a fixed literal
path even when it's tilde-relative.

## Decision

Canonical home pattern: `${AGENTS_HOME:-$HOME/.agents}`.

1. **Skills declare the pattern at the top.** Any SKILL.md that references
   files under the agents home states the resolution rule once near the top
   (e.g. in frontmatter-adjacent prose or its first section):
   `AGENTS_HOME` env var if set, else `$HOME/.agents`. All later references
   use `$AGENTS_HOME/...` shorthand.
2. **Shell scripts / hooks** use `"${AGENTS_HOME:-$HOME/.agents}"` verbatim.
3. **Prose and docs** may use `~/.agents/...` where a human is the reader.
4. **Instances**: a non-default instance sets `AGENTS_HOME` in its environment;
   skills and scripts inherit it without modification. The global default
   requires no setup.
5. **Never** write `/Users/<name>/...` or `/home/<name>/...` literals in any
   committed file.

## Decision Drivers

- Multi-runtime support: not Claude-specific, so `~/.claude/` is wrong as a base.
- Instance management: env-var indirection lets several agent homes coexist.
- CI: the hardcoded-path check enforces the "no literal home path" rule.
- Windows: WSL2/git-bash resolve `~` and `$HOME` normally; native shells set
  `AGENTS_HOME=%USERPROFILE%\.agents` once (README note, not a design driver).

## Alternatives Considered

- **XDG (`$XDG_DATA_HOME/agents`)** — strictly correct on Linux, ignored on
  macOS, no native Windows mapping, and reads as jargon in skill bodies. Rejected.
- **Literal `~/.agents` everywhere with no env var** — simple but blocks
  multi-instance layouts. Rejected.
- **Per-runtime homes (`~/.claude/skills`, `~/.codex/...`)** — fragments the
  catalog per runtime. Rejected.

## Consequences

- Adapted shaping-skill ports must rewrite upstream `~/.claude/skills/...`
  references to the pattern.
- A follow-up sweep replaces existing literal home paths in
  `skills/interview`, `skills/cdo`, `skills/cass-coverage` (SKILL.md +
  `scripts/merge.py`), `skills/codex-autoresearch/tests/`, `convex/AGENTS.md`,
  and elides absolute paths from `levnow/*.json` reports; this also turns the
  hardcoded-path CI check green.
- Bootstrap/instance tooling can provision an instance simply by exporting
  `AGENTS_HOME` before invoking any skill.
