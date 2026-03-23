---
name: cli-runners
description: Headless invocation patterns for AI coding CLIs — how to dispatch prompts, select models, and collect structured output
---

# CLI Runner Reference

Lookup table for headless AI CLI invocation. Tribunal uses this to dispatch prompts across models and providers. The caller decides what to test and why — this table just tells you HOW to invoke each runner.

## Invocation Table

| CLI | Non-Interactive Command | Model Flag | JSON Output | Auto-Approve | Install |
|-----|------------------------|------------|-------------|--------------|---------|
| **Claude Code** | `claude -p "prompt"` | `--model <id>` | `--output-format json` | `--dangerously-skip-permissions` | `npm i -g @anthropic-ai/claude-code` |
| **Codex CLI** | `codex -q "prompt"` | `--model <name>` / `-m` | `--json` (NDJSON) | `-a never` | `npm i -g @openai/codex` |
| **Gemini CLI** | `gemini -p "prompt"` | `--model <name>` / `-m` | `--output-format json` | `--yolo` | `npm i -g @google/gemini-cli` |
| **OpenCode** | `opencode run --command "prompt"` | `--model provider/model` | `--format json` | N/A (non-interactive by design) | `curl -fsSL https://opencode.ai/install \| bash` |
| **Aider** | `aider --message "prompt" --yes-always` | `--model <name>` | None | `--yes-always` | `curl https://aider.chat/install.sh \| sh` |
| **Cursor CLI** | `echo "prompt" \| cursor agent -p` | None (`CURSOR_MODEL` env) | None | `--force` | `curl https://cursor.com/install -fsSS \| bash` |

## Quick Recipes

```bash
# Claude Code — gold standard for headless
echo "prompt" | claude -p --model sonnet --output-format json --dangerously-skip-permissions

# Codex CLI — true headless requires -a never
codex -q "prompt" -m o4-mini -a never

# Gemini CLI — mirrors Claude Code pattern
gemini -p "prompt" -m gemini-2.5-flash --yolo --output-format json

# OpenCode — subcommand pattern
opencode run --command "prompt" --model anthropic/claude-3-sonnet --format json

# Aider — no JSON output, text only
aider --message "prompt" --model gpt-4o --yes-always --no-stream --no-auto-commits

# Cursor — limited, no JSON, can hang
echo "prompt" | cursor agent -p --force
```

## Capability Matrix

| Capability | Claude | Codex | Gemini | OpenCode | Aider | Cursor |
|------------|--------|-------|--------|----------|-------|--------|
| Pipe stdin | `-p` | Yes | `-p` | `run --command` | `--message` | Yes |
| JSON output | Yes | NDJSON | Yes | Yes | No | No |
| Schema validation | `--json-schema` | No | No | No | No | No |
| Model flag | Yes | Yes | Yes | Yes | Yes | No |
| Budget cap | `--max-budget-usd` | No | No | No | No | No |
| Streaming JSON | `stream-json` | NDJSON | No | No | No | No |
| Session resume | `-r` / `-c` | No | No | `-s` / `-c` | No | No |
| Sandbox | Yes | `--sandbox` | No | No | No | No |
| Fallback model | `--fallback-model` | No | No | No | No | No |

## Tiers

**Tier 1** (production-ready headless): Claude Code, Codex CLI, Gemini CLI — all have prompt flags, model selection, JSON output.

**Tier 2** (usable with caveats): OpenCode (subcommand pattern, less mature), Aider (no JSON, security risk with `--yes-always`).

**Tier 3** (not ready): Cursor CLI (hangs, no model flag, no JSON, requires interactive trust setup).

## Notes

- Claude Code is the most feature-complete: budget caps, schema validation, streaming, fallback models.
- Codex's `-q` (quiet) prints only final output. `--full-auto` is NOT truly non-interactive — combine with `-a never`.
- Gemini's `--yolo` is the full-auto equivalent. Auto-approvals persist globally in `~/.gemini/settings.json` — no project isolation.
- OpenCode uses slash-notation for providers: `anthropic/claude-3-sonnet`, `openai/gpt-4`.
- Aider tried JSON output but LLMs produce lower quality vs diff format — intentionally dropped.
- Cursor only loads `~/.zshenv` (not `~/.zshrc`), so PATH tools need env-level config.
