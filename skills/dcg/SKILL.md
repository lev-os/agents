---
name: dcg
description: Destructive Command Guard for coding agents. Use when you need to test, explain, install, or validate safety rails that block dangerous git and filesystem commands before an agent executes them.
---

# DCG

Use `dcg` when you need mechanical safety rails around destructive shell commands.

## Install

```bash
brew install dicklesworthstone/tap/dcg
```

## When to Use

- before enabling shell hooks for coding agents
- to explain why a dangerous command is blocked
- to validate a fresh environment with `dcg doctor`
- to install or uninstall the Claude hook

## Quick Start

```bash
dcg doctor
dcg test "rm -rf /"
dcg explain "git push -f"
dcg install
```

## Useful Commands

```bash
dcg packs
dcg config
dcg history
dcg scan .
dcg simulate
dcg allow "git clean -fd"
dcg allow-once
```

## Agent Notes

- Prefer `dcg test` or `dcg explain` before asking a human to run a risky command.
- Use `dcg doctor` after install or shell migration.
- For agent-friendly automation, set `DCG_ROBOT=1`.
- This is a safety boundary, not a general workflow router.

