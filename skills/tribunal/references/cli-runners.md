# CLI Runner Reference

Use the bundled detector as the source of current executable and model-roster
state. It is standalone and does not require Lev.

## Detection

```bash
# Cached runner and model roster
~/.agents/skills/tribunal/bin/detect-runners --json

# Force live executable, version, and model discovery
~/.agents/skills/tribunal/bin/detect-runners --refresh --json

# One runner's models; add --json for provenance
~/.agents/skills/tribunal/bin/detect-runners --models codex
~/.agents/skills/tribunal/bin/detect-runners --models cursor-agent --json
```

The detector writes `~/.cache/tribunal/runners.json` or the equivalent
`$XDG_CACHE_HOME` path. The cache TTL is 24 hours. Each runner reports its
executable path, version, model list, discovery source, whether the list is
exhaustive, and any timeout or discovery error.

Exhaustive means exhaustive for that CLI's discovery command, not proof that
every row is authenticated or runnable. OpenCode and Pi expose aggregate
multi-provider catalogs; expect per-cell auth failures unless the caller has
configured those providers.

`Claude Code`, direct `Gemini CLI`, and `Aider` do not expose a reliable
exhaustive model-list command in this contract. Claude contributes its declared
aliases; Gemini and Aider require caller-supplied model IDs when discovery is
unavailable. The detector labels these cases instead of pretending the roster is
complete.

## Read-Only Opinion Invocations

Use a separate prompt, output, and log file for every model. Substitute the
literal paths and model IDs; do not interpolate untrusted shell fragments.

| Runner | Invocation |
|---|---|
| Codex | `codex exec -s read-only -m MODEL -o OUTPUT - < PROMPT > LOG 2>&1` |
| Claude Code | `claude -p --permission-mode plan --model MODEL --output-format text < PROMPT > OUTPUT 2> LOG` |
| Gemini CLI | `gemini -p "PROMPT_TEXT" -m MODEL --output-format json > OUTPUT 2> LOG` |
| Antigravity (`agy`) | `agy --sandbox --model MODEL --print "PROMPT_TEXT" > OUTPUT 2> LOG` |
| Cursor Agent | `cursor-agent -p --mode ask --model MODEL --output-format text "PROMPT_TEXT" > OUTPUT 2> LOG` |
| OpenCode | `opencode run -m MODEL "PROMPT_TEXT" > OUTPUT 2> LOG` |
| Pi | `pi -p --no-tools --model MODEL "PROMPT_TEXT" > OUTPUT 2> LOG` |
| Aider | `aider --dry-run --no-auto-commits --message "PROMPT_TEXT" --model MODEL > OUTPUT 2> LOG` |

Prefer stdin-capable forms. For positional-only forms, read `PROMPT_TEXT` from a
trusted temporary file as one quoted argument. Do not add auto-approve flags:
Tribunal asks questions and must not need mutation permissions.

## Live Model Commands

| Runner | Discovery |
|---|---|
| Codex | `codex debug models` (JSON catalog) |
| Claude Code | Declared aliases: `haiku`, `sonnet`, `opus`, `fable`; non-exhaustive |
| Gemini CLI | No portable exhaustive command; explicit models required |
| Antigravity (`agy`) | `agy models` |
| Cursor Agent | `cursor-agent models` |
| OpenCode | `opencode models` |
| Pi | `pi --list-models` |
| Aider | No exhaustive command; explicit models required |

## Collection Rules

- Preserve one result row per `(runner, model)` even when the process fails.
- Parse structured output when available; otherwise retain text and mark parse
  status explicitly.
- Report both raw model counts and provider-balanced convergence.
- Never let process completion order choose the verdict.
