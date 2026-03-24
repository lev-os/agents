---
name: cli-runners
description: Dynamic CLI runner detection for tribunal cross-model dispatch
---

# CLI Runner Reference

Tribunal detects installed coding agent CLIs dynamically. No hardcoded model lists — models change constantly.

## Quick Commands

```bash
# Detect all installed runners
~/.claude/skills/tribunal/bin/detect-runners

# Force refresh (bypass 24h cache)
~/.claude/skills/tribunal/bin/detect-runners --refresh

# JSON output (for programmatic use)
~/.claude/skills/tribunal/bin/detect-runners --json

# List models for a specific CLI
~/.claude/skills/tribunal/bin/detect-runners --models cursor
~/.claude/skills/tribunal/bin/detect-runners --models pi
~/.claude/skills/tribunal/bin/detect-runners --models opencode
```

## Invocation Patterns

Each runner has a headless invocation pattern. The detect-runners script caches these in `~/.cache/tribunal/runners.json`. The agent reads the cache to construct dispatch commands.

| CLI | Prompt Flag | Model Flag | JSON Flag | Auto-Approve |
|-----|-------------|-----------|-----------|-------------|
| claude | `-p` | `--model` | `--output-format json` | `--dangerously-skip-permissions` |
| codex | `-q` | `-m` | `--json` | `-a never` |
| gemini | `-p` | `-m` | `--output-format json` | `--yolo` |
| cursor-agent | `-p` | `--model` | `--output-format json` | `--yolo --trust` |
| opencode | `run` | `-m provider/model` | `--format json` | N/A |
| pi | N/A | `--model provider/id` | N/A | N/A |
| aider | `--message` | `--model` | N/A | `--yes-always` |

## Config Paths

Where each CLI stores its config (for troubleshooting auth/model issues):

| CLI | Config Location |
|-----|----------------|
| claude | `~/.claude/settings.json` |
| codex | `~/.codex/config.toml` |
| gemini | `~/.gemini/settings.json` |
| cursor-agent | `~/.cursor-agent/` |
| opencode | `~/.local/share/opencode/auth.json` |
| pi | `~/.config/pi/` |
| aider | `~/.aider.conf.yml` |

## Tiers

Tiers are set in detect-runners based on headless maturity:

- **T1** (production headless): Claude, Codex, Gemini, Cursor — all have `-p`/`-q`, `--model`, JSON output
- **T2** (usable with caveats): OpenCode (subcommand pattern), Pi (no JSON output), Aider (no JSON, `--yes-always` security risk)

## Architecture

- **No hardcoded models** — models change constantly. Use `--models <cli>` to query at runtime.
- **24h cache** at `~/.cache/tribunal/runners.json` — refreshed with `--refresh`
- **Script is the source of truth** — `~/.claude/skills/tribunal/bin/detect-runners`
- **JSON output** for programmatic consumption by the tribunal adapter
