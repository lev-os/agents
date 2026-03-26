# Agent Hook Configuration Reference

Complete JSON/YAML formats for every supported AI coding agent.

---

## Claude Code

**Settings file:** `$HOME/.claude/settings.json`

**Hook type:** `PreToolUse` with `Bash` matcher

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/.local/bin/my-tool"
          }
        ]
      }
    ]
  }
}
```

**Merge strategy:** Try jq first, fall back to embedded Python3.

jq approach (simpler when available):
```bash
existing=$(cat "$settings_path")
echo "$existing" | jq ". * $hook_config" > "$settings_path"
```

Python3 approach (always available):
1. Loads existing JSON (tolerates parse errors → empty dict)
2. Finds or creates `PreToolUse` array
3. Finds or creates `Bash` matcher entry
4. Inserts new hook at position 0 (runs first)
5. Deduplicates by checking if binary name already in any command
6. Consolidates all Bash matchers into one entry

Full implementation: [PYTHON3-JSON-MERGE.md](PYTHON3-JSON-MERGE.md)

**Settings paths (multi-path detection):**
- `$HOME/.claude/settings.json`
- `$HOME/.config/claude/settings.json`
- `$HOME/Library/Application Support/Claude/settings.json`

**Backup:** `$HOME/.claude/settings.json.bak.YYYYMMDDHHMMSS`

**Status values:** `created` | `merged` | `already` | `failed`

---

## Gemini CLI

**Settings file:** `$HOME/.gemini/settings.json`

**Hook type:** `BeforeTool` with `run_shell_command` matcher

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {
            "name": "my-tool",
            "type": "command",
            "command": "/home/user/.local/bin/my-tool",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

**Key differences from Claude Code:**
- Hook key is `BeforeTool` not `PreToolUse`
- Matcher is `run_shell_command` not `Bash`
- Hooks entries include `name` and `timeout` fields

**Settings paths (multi-path detection):**
- `$HOME/.gemini/settings.json`
- `$HOME/.gemini-cli/settings.json`

**Detection:** Check `$HOME/.gemini` dir AND `$HOME/.gemini-cli` dir AND `gemini` command

---

## Codex CLI

**No pre-execution hooks.** Codex CLI only supports post-execution hooks:
- `notify`: Send notifications after events
- `agent-turn-complete`: Callback after agent completes

**Recommended workaround:** Install as git pre-commit hook.

**Status values:** `unsupported` | `skipped`

---

## Aider

**Settings file:** `$HOME/.aider.conf.yml`

**No shell hooks.** Aider does not have PreToolUse-style hooks.

**Best integration:** Enable `git-commit-verify: true` in YAML config so git hooks (including pre-commit) fire.

```yaml
# Created by installer
git-commit-verify: true
```

**Merge strategy:**
- If setting exists and is `true` → skip
- If setting exists and is `false` → sed replace to `true`
- If setting missing → append to file
- If file missing → create with header comment

---

## GitHub Copilot CLI

**Settings file:** `<repo>/.github/hooks/my-tool.json` (repository-local)

**Hook type:** `preToolUse` command hook

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "/home/user/.local/bin/my-tool",
        "powershell": "/home/user/.local/bin/my-tool",
        "cwd": ".",
        "timeoutSec": 30
      }
    ]
  }
}
```

**Key differences:**
- Repository-local (requires git repo)
- Separate `bash` and `powershell` command fields
- `timeoutSec` (not `timeout`)
- `cwd` field required
- Merge via Python3 with UNCHANGED/UPDATED/ADDED result tracking

**Prerequisites:** Must be inside a git repository (`git rev-parse --show-toplevel`)

---

## Cursor IDE

**Settings file:** `$HOME/.cursor/hooks.json`
**Hook script:** `$HOME/.cursor/hooks/my-tool-pre-shell.py`

**Two-part installation:**

1. **Python hook script** that wraps the binary:
```python
#!/usr/bin/env python3
# Reads JSON from stdin, passes to binary, emits allow/deny JSON to stdout
import json, subprocess, sys

def allow(): sys.stdout.write(json.dumps({"permission":"allow","continue":True}))
def deny(r): sys.stdout.write(json.dumps({"permission":"deny","continue":False,"userMessage":r}))

payload = json.load(sys.stdin)
command = payload.get("command", "")
hook_input = {"tool_name": "Bash", "tool_input": {"command": command}}
proc = subprocess.run(["my-tool"], input=json.dumps(hook_input), text=True, capture_output=True)
# Parse result, emit allow/deny
```

2. **hooks.json** referencing the script:
```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {"command": "/home/user/.cursor/hooks/my-tool-pre-shell.py"}
    ]
  }
}
```

**Detection:** Check `$HOME/.cursor` dir, Cursor settings paths, `cursor` command, and `pgrep -fl Cursor`

**Conflict handling:** If existing hook script exists without our marker → status `conflict`, don't overwrite

---

## Continue

**No shell hooks.** Continue does not have shell command interception.

**Detection:** Check `$HOME/.continue` dir and `cn` command.

**Status values:** `unsupported` | `skipped`

---

## Detection Function Template

```bash
detect_agents() {
  DETECTED_AGENTS=()

  # Claude Code
  if [[ -d "$HOME/.claude" ]] || command -v claude &>/dev/null; then
    DETECTED_AGENTS+=("claude-code")
  fi

  # Codex CLI
  if [[ -d "$HOME/.codex" ]] || command -v codex &>/dev/null; then
    DETECTED_AGENTS+=("codex-cli")
  fi

  # Gemini CLI (check both ~/.gemini and ~/.gemini-cli)
  if [[ -d "$HOME/.gemini" ]] || [[ -d "$HOME/.gemini-cli" ]] || command -v gemini &>/dev/null; then
    DETECTED_AGENTS+=("gemini-cli")
  fi

  # Aider
  if command -v aider &>/dev/null; then
    DETECTED_AGENTS+=("aider")
  fi

  # GitHub Copilot CLI
  if command -v copilot &>/dev/null || [[ -d "$HOME/.copilot" ]]; then
    DETECTED_AGENTS+=("github-copilot-cli")
  fi

  # Continue
  if [[ -d "$HOME/.continue" ]]; then
    DETECTED_AGENTS+=("continue")
  fi

  # Cursor IDE
  if [[ -d "$HOME/.cursor" ]] || command -v cursor &>/dev/null; then
    DETECTED_AGENTS+=("cursor-ide")
  fi
}
```

---

## Version Detection (with timeout)

```bash
try_version() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || return 0
  if command -v timeout >/dev/null 2>&1; then
    timeout 1 "$cmd" --version 2>/dev/null | head -1 || true
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout 1 "$cmd" --version 2>/dev/null | head -1 || true
  else
    "$cmd" --version 2>/dev/null | head -1 || true
  fi
}
```

---

## Print Detected Agents

```bash
print_detected_agents() {
  local count=${#DETECTED_AGENTS[@]}
  [[ $count -eq 0 ]] && { info "No AI coding agents detected"; return; }

  local plural=""
  [[ $count -gt 1 ]] && plural="s"

  if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ]; then
    gum style --foreground 39 --bold "Detected AI Coding Agent${plural}:"
    for agent in "${DETECTED_AGENTS[@]}"; do
      gum style --foreground 42 "  ✓ ${agent}"
    done
  else
    echo -e "\033[1;39mDetected AI Coding Agent${plural}:\033[0m"
    for agent in "${DETECTED_AGENTS[@]}"; do
      echo -e "  \033[0;32m✓\033[0m ${agent}"
    done
  fi
}
```
