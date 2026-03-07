---
name: oracle
description: |
  [WHAT] Route prompts + files to GPT-5 Pro, Gemini 3 Pro, Claude Opus 4.1, and more via oracle CLI
  [HOW] Uses oracle serve (persistent browser daemon on :9473) or API with OPENAI_API_KEY
  [WHEN] Second opinion, multi-model comparison, browser-only features (image gen, extended thinking)
  [WHY] Cross-model validation and access to models not available in current context

  Triggers: "ask gpt", "oracle", "second opinion", "ask chatgpt", "cross-check with gpt",
            "multi-model", "compare models", "gpt-5", "gemini", "use oracle"
---

# oracle 🧿

Bundle your prompt and files so another AI can answer with real context. Speaks GPT-5.x, Gemini 3 Pro, Claude Sonnet 4.5, Claude Opus 4.1, and more — via API or browser automation.

## Local Setup (THIS MACHINE)

**Browser mode is pre-configured.** `oracle serve` runs as a launchd daemon.
Agents just run `oracle -p "..." --file ...` — config handles routing to serve.

```
Engine:  browser (via oracle serve on 127.0.0.1:9473)
Config:  ~/.oracle/config.json (remoteHost + token already set)
Daemon:  ~/Library/LaunchAgents/com.oracle.serve.plist
API key: OPENAI_API_KEY in ~/.env.local (source it first)
```

**DO NOT** use `--engine browser` or `--browser-manual-login` flags directly.
**DO NOT** try to sniff Chrome cookies — macOS app-bound encryption blocks it.
**JUST RUN:** `oracle -p "your prompt" --file path/to/files`

If oracle fails with "unauthorized" or cookie errors:
1. Check serve is running: `launchctl list | grep oracle`
2. Restart: `launchctl stop com.oracle.serve && launchctl start com.oracle.serve`
3. Login needed: open `http://127.0.0.1:9473` — Chrome window should appear, login to ChatGPT once
4. For API mode: `source ~/.env.local && oracle --engine api -p "..."`

**Repository:** [steipete/oracle](https://github.com/steipete/oracle)
**Homepage:** [askoracle.dev](https://askoracle.dev)
**Language:** TypeScript (95%) · JavaScript (4.2%) · Shell (0.8%)
**Stars:** 1,235 · **License:** Other
**Latest:** v0.8.5 (2026-01-19)

## Source Information

This skill synthesizes knowledge from the project README, CHANGELOG, GitHub issues, releases, and file structure — all sourced from the GitHub repository. Confidence is medium across all sources; no conflicting information was detected.

## When to Use This Skill

Use this skill when you need to:

- **Route a prompt + files to a stronger model** — bundle context and send to GPT-5 Pro, Gemini 3 Pro, Claude Opus 4.1, etc.
- **Multi-model comparison** — run the same prompt against multiple models in one invocation
- **Browser automation for ChatGPT/Gemini** — when you don't have API keys or need browser-specific features (image generation, thinking time)
- **Copy/render bundles** — assemble markdown bundles for manual paste into any AI chat
- **Session management** — track, replay, and reattach to long-running API sessions (GPT-5 Pro detaches by default)
- **MCP integration** — use Oracle as an MCP server for tool-based AI workflows
- **Remote browser service** — run `oracle serve` on a signed-in host, connect from clients
- **Check known issues** — browser mode quirks, attachment bugs, platform-specific workarounds

### Real-World Triggers

| Scenario | Command Pattern |
|----------|----------------|
| Get a second opinion from GPT-5 Pro | `oracle -p "Review this" --file src/**/*.ts` |
| Compare models on the same prompt | `oracle --models gpt-5.1-pro,gemini-3-pro -p "..." --file ...` |
| No API key, use browser | `oracle --engine browser -p "..." --file ...` |
| Preview token usage before sending | `oracle --dry-run summary -p "..." --file ...` |
| Copy bundle for manual paste | `oracle --render --copy -p "..." --file ...` |

## Quick Reference

### Installation

```bash
# npm (global)
npm install -g @steipete/oracle

# Homebrew
brew install steipete/tap/oracle

# One-shot (no install)
npx -y @steipete/oracle …
```

Requires **Node 22+**.

### Core Examples

**Simple API run** (needs `OPENAI_API_KEY`):
```bash
oracle -p "Write an architecture note for the storage adapters" --file src/storage/README.md
```

**Multi-model run:**
```bash
oracle -p "Cross-check the data layer assumptions" \
  --models gpt-5.1-pro,gemini-3-pro \
  --file "src/**/*.ts"
```

**Copy bundle for manual paste:**
```bash
oracle --render --copy \
  -p "Review the TS data layer for schema drift" \
  --file "src/**/*.ts,*/*.test.ts"
```

**Browser mode** (no API key needed):
```bash
oracle --engine browser -p "Walk through the UI smoke test" --file "src/**/*.ts"
```

**Dry run preview:**
```bash
oracle --dry-run summary -p "Check release notes" --file docs/release-notes.md
```

**Gemini browser image generation:**
```bash
oracle --engine browser --model gemini-3-pro \
  -p "a cute robot holding a banana" \
  --generate-image out.jpg --aspect 1:1
```

**Session management:**
```bash
oracle status                      # List sessions
oracle session <id> --render       # Replay a session
oracle status --clear --hours 168  # Prune old sessions
```

**Remote browser service:**
```bash
# Host (signed-in Chrome)
oracle serve --host 0.0.0.0:9473 --token secret123

# Client
oracle --engine browser --remote-host localhost:9473 --remote-token secret123 -p "..."
```

### Supported Models

| Model | Type | Notes |
|-------|------|-------|
| `gpt-5.1-pro` | API (default) | Alias to GPT-5.2 Pro |
| `gpt-5-pro` | API | Original GPT-5 Pro |
| `gpt-5.1` / `gpt-5.2` | API | Standard models |
| `gpt-5.1-codex` | API | Codex variant (API-only) |
| `gpt-5.2-instant` / `gpt-5.2-pro` | API | Speed/quality variants |
| `gemini-3-pro` | API + Browser | Needs `GEMINI_API_KEY` or Chrome cookies |
| `claude-4.5-sonnet` / `claude-4.1-opus` | API | Needs `ANTHROPIC_API_KEY` |
| Any OpenRouter ID | API | e.g., `minimax/minimax-m2` |

### Key Flags

| Flag | Purpose |
|------|---------|
| `-p, --prompt <text>` | Required prompt |
| `-f, --file <paths...>` | Attach files/dirs (globs + `!` excludes) |
| `-e, --engine <api\|browser>` | Choose API or browser |
| `-m, --model <name>` | Select model |
| `--models <list>` | Comma-separated models for multi-model runs |
| `--render`, `--copy` | Print/copy assembled markdown bundle |
| `--wait` | Block for background API runs |
| `--dry-run [summary\|json\|full]` | Preview without sending |
| `--write-output <path>` | Save final answer to file |
| `--files-report` | Print per-file token usage |
| `--base-url <url>` | Point API at LiteLLM/Azure/OpenRouter |
| `--browser-model-strategy` | `select\|current\|ignore` for ChatGPT picker |
| `--browser-thinking-time` | `light\|standard\|extended\|heavy` |
| `--browser-manual-login` | Reuse persistent automation profile |
| `--background` / `--no-background` | Force Responses API background mode |
| `--timeout <seconds\|auto>` | API deadline (auto = 60m for pro) |

### Configuration

Defaults in `~/.oracle/config.json` (JSON5). Key settings:

- `browser.chatgptUrl` — target a specific ChatGPT workspace/folder
- `browser.thinkingTime` / `browser.manualLogin` — browser defaults
- `browser.remoteHost` / `browser.remoteToken` — remote service connection
- `browser.forceEnglishLocale` — opt into `--lang/--accept-lang`

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | GPT-5.x API access |
| `GEMINI_API_KEY` | Gemini 3 Pro API access |
| `ANTHROPIC_API_KEY` | Claude models API access |
| `ORACLE_HOME_DIR` | Override session storage path (`~/.oracle/sessions`) |
| `AZURE_OPENAI_*` | Azure endpoint configuration |

### MCP Integration

Run the stdio server via `oracle-mcp`. Configure in `.mcp.json` or via [mcporter](https://github.com/steipete/mcporter).

### Codex Skill Integration

```bash
mkdir -p ~/.codex/skills
cp -R skills/oracle ~/.codex/skills/oracle
```

Then reference in `AGENTS.md`/`CLAUDE.md`.

## Key Concepts

- **Bundle** — Oracle assembles your prompt + files into a single markdown bundle. This bundle is what gets sent to the model (API) or pasted (browser/copy mode).
- **Engine** — `api` (default when keys present) or `browser` (experimental, uses Chrome automation). API is more reliable.
- **Multi-model runs** — `--models` sends the same bundle to multiple models, aggregating cost/usage.
- **Background/detach** — GPT-5 Pro API runs detach by default. Use `--wait` to block, or `oracle session <id>` to reattach.
- **Sessions** — Stored in `~/.oracle/sessions`. Replay with `oracle session <id> --render`. Prune with `oracle status --clear`.

## Known Issues (Open)

| Issue | Summary |
|-------|---------|
| [#79](https://github.com/steipete/oracle/issues/79) | Chrome opens and auto-closes in browser mode |
| [#76](https://github.com/steipete/oracle/issues/76) | `MAX_FILE_SIZE_BYTES` not configurable |
| [#75](https://github.com/steipete/oracle/issues/75) | Browser mode fails during manual login |
| [#65](https://github.com/steipete/oracle/issues/65) | Browser doesn't select ChatGPT 5.2-pro correctly |
| [#68](https://github.com/steipete/oracle/issues/68) | MCP consult tool ignores browser config |
| [#51](https://github.com/steipete/oracle/issues/51) | Windows cookie extraction for Gemini browser |

### Platform Notes

- **macOS**: Browser mode stable
- **Linux**: May need `--browser-chrome-path` / `--browser-cookie-path`
- **Windows**: Prefer `--browser-manual-login` or inline cookies if decryption is blocked

## Working with This Skill

### Beginner
Start with `--render --copy` to see what Oracle bundles, then paste manually. Graduate to API mode once you have keys set up.

### Intermediate
Use multi-model runs (`--models`) to cross-check answers. Use `--dry-run` to preview token costs. Set up `~/.oracle/config.json` for persistent defaults.

### Advanced
Deploy `oracle serve` for remote browser access. Integrate via MCP for tool-based workflows. Use `--background` with session management for long-running GPT-5 Pro queries.

## Available References

| File | Contents | Confidence |
|------|----------|------------|
| `references/README.md` | Full README with installation, usage, flags, integration | Medium |
| `references/CHANGELOG.md` | Version history from v0.7.2 through v0.8.5 | Medium |
| `references/issues.md` | 6 open + 29 closed GitHub issues | Medium |
| `references/releases.md` | 30 releases with detailed notes | Medium |
| `references/file_structure.md` | 342-item repository tree | Medium |

## Version History (Recent)

| Version | Date | Highlights |
|---------|------|------------|
| v0.8.5 | 2026-01-19 | Bridge workflow + MCP browser controls, background/zombie flags |
| v0.8.4 | 2026-01-05 | Zod 4.3.5, attachment upload fixes |
| v0.8.3 | 2025-12-31 | Cookie wait, force English locale, attachment hardening |
| v0.8.2 | 2025-12-30 | Release script fixes, test stabilization |
| v0.8.1 | 2025-12-30 | Config defaults for thinkingTime/manualLogin |
| v0.8.0 | 2025-12-28 | Browser reliability push (reattach, capture, uploads) |

---

**Generated by Skill Seeker** | Enhanced from GitHub repository sources
