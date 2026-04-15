# Embedded Python3 JSON Merge Pattern

The canonical pattern for safely merging JSON settings files from bash without jq. Used in DCG and RCH installers for agent hook configuration.

---

## Why Embedded Python3?

| Approach | Problem |
|----------|---------|
| `jq` | Not always installed |
| `sed`/`awk` | Breaks on special chars, nested JSON |
| `cat > file` | Overwrites existing settings |
| **Embedded Python3** | Available everywhere, handles edge cases |

---

## The Complete Pattern (Claude Code)

```bash
configure_claude_code() {
  local settings_file="$1"
  local remove_predecessor="$2"  # 0 or 1

  # 1. Check if already configured
  if [ -f "$settings_file" ] && grep -q "$BINARY_NAME" "$settings_file" 2>/dev/null; then
    CLAUDE_STATUS="already"
    return 0
  fi

  # 2. Settings file missing → create from template
  if [ ! -f "$settings_file" ]; then
    mkdir -p "$(dirname "$settings_file")"
    cat > "$settings_file" <<EOFSET
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$DEST/$BINARY_NAME"
          }
        ]
      }
    ]
  }
}
EOFSET
    CLAUDE_STATUS="created"
    return 0
  fi

  # 3. Settings file exists → merge with Python3
  if ! command -v python3 >/dev/null 2>&1; then
    CLAUDE_STATUS="failed"
    return 1
  fi

  # 4. Timestamped backup BEFORE any modification
  CLAUDE_BACKUP="${settings_file}.bak.$(date +%Y%m%d%H%M%S)"
  cp "$settings_file" "$CLAUDE_BACKUP"

  # 5. Merge via embedded Python3
  local py_result
  py_result=$(python3 - "$settings_file" "$DEST/$BINARY_NAME" "$remove_predecessor" <<'PYEOF'
import json
import sys

settings_file = sys.argv[1]
binary_path = sys.argv[2]
remove_predecessor = sys.argv[3] == "1"

# Tolerant load (handle parse errors)
try:
    with open(settings_file, "r") as f:
        settings = json.load(f)
except Exception:
    settings = {}

if not isinstance(settings, dict):
    settings = {}

# Navigate/create the hook path
hooks = settings.setdefault("hooks", {})
if not isinstance(hooks, dict):
    hooks = {}
    settings["hooks"] = hooks

pre_tool = hooks.get("PreToolUse")
if not isinstance(pre_tool, list):
    pre_tool = []
    hooks["PreToolUse"] = pre_tool

# Find or create the Bash matcher entry
bash_entry = None
for entry in pre_tool:
    if isinstance(entry, dict) and entry.get("matcher") == "Bash":
        bash_entry = entry
        break

if bash_entry is None:
    bash_entry = {"matcher": "Bash", "hooks": []}
    pre_tool.insert(0, bash_entry)

inner_hooks = bash_entry.get("hooks")
if not isinstance(inner_hooks, list):
    inner_hooks = []
    bash_entry["hooks"] = inner_hooks

# Dedup: check if binary already in any command
binary_name = binary_path.rsplit("/", 1)[-1]
for hook in inner_hooks:
    if isinstance(hook, dict) and binary_name in str(hook.get("command", "")):
        print("ALREADY")
        raise SystemExit(0)

# Insert at position 0 (runs first)
new_hook = {"type": "command", "command": binary_path}
inner_hooks.insert(0, new_hook)

# Consolidate: merge all Bash matchers into one
all_bash_hooks = []
non_bash = []
for entry in pre_tool:
    if isinstance(entry, dict) and entry.get("matcher") == "Bash":
        for h in entry.get("hooks", []):
            if h not in all_bash_hooks:
                all_bash_hooks.append(h)
    else:
        non_bash.append(entry)

hooks["PreToolUse"] = [{"matcher": "Bash", "hooks": all_bash_hooks}] + non_bash

# Optionally remove predecessor hooks
if remove_predecessor:
    for entry in hooks.get("PreToolUse", []):
        if isinstance(entry, dict):
            entry_hooks = entry.get("hooks", [])
            entry["hooks"] = [
                h for h in entry_hooks
                if not isinstance(h, dict) or "predecessor_name" not in str(h.get("command", ""))
            ]

# Write back
with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print("MERGED")
PYEOF
)

  # 6. Handle result
  case "$py_result" in
    ALREADY)
      CLAUDE_STATUS="already"
      rm -f "$CLAUDE_BACKUP" 2>/dev/null || true
      CLAUDE_BACKUP=""
      ;;
    MERGED)
      CLAUDE_STATUS="merged"
      ;;
    *)
      # Rollback on unexpected output
      mv "$CLAUDE_BACKUP" "$settings_file" 2>/dev/null || true
      CLAUDE_STATUS="failed"
      CLAUDE_BACKUP=""
      return 1
      ;;
  esac
}
```

---

## Key Design Decisions

### Tolerant Load
```python
try:
    with open(settings_file, "r") as f:
        settings = json.load(f)
except Exception:
    settings = {}
```
If the file is corrupt or empty, start fresh rather than fail.

### Dedup by Binary Name
```python
binary_name = binary_path.rsplit("/", 1)[-1]
for hook in inner_hooks:
    if binary_name in str(hook.get("command", "")):
```
Checks if the binary name (not full path) appears anywhere in existing hooks. Prevents duplicate entries even if install path changed.

### Consolidate All Bash Matchers
Multiple Bash matcher entries get merged into one. This handles cases where previous installers or manual edits created duplicates.

### Rollback on Failure
```bash
mv "$CLAUDE_BACKUP" "$settings_file" 2>/dev/null || true
```
If Python3 fails or returns unexpected output, the original file is restored from backup.

---

## jq Alternative (from RCH)

When `jq` IS available, this is simpler:

```bash
configure_with_jq() {
  local settings_path="$1"
  local hook_config='{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"'"$DEST/$BINARY_NAME"'"}]}]}}'

  if [ ! -f "$settings_path" ]; then
    echo "$hook_config" | jq '.' > "$settings_path"
    return 0
  fi

  # Check if already configured
  if jq -e '.hooks.PreToolUse[] | select(.hooks[]? | .command? | contains("'"$BINARY_NAME"'"))' \
      "$settings_path" >/dev/null 2>&1; then
    return 0  # Already configured
  fi

  # Deep merge (preserves all existing settings)
  local existing
  existing=$(cat "$settings_path")
  echo "$existing" | jq ". * $hook_config" > "$settings_path"
}
```

**jq deep merge with `*`** preserves existing settings (PostToolUse, other hooks) while adding ours.

**Recommendation:** Try jq first, fall back to Python3:
```bash
if command -v jq >/dev/null 2>&1; then
  configure_with_jq "$settings_file"
elif command -v python3 >/dev/null 2>&1; then
  configure_with_python3 "$settings_file"
else
  warn "Neither jq nor python3 found; manual hook configuration required"
  AGENT_STATUS="failed"
fi
```

---

## Multi-Path Settings Detection

```bash
find_settings_file() {
  local agent="$1"
  local paths=()

  case "$agent" in
    claude)
      paths=(
        "$HOME/.claude/settings.json"
        "$HOME/.config/claude/settings.json"
        "$HOME/Library/Application Support/Claude/settings.json"
      )
      ;;
    gemini)
      paths=(
        "$HOME/.gemini/settings.json"
        "$HOME/.gemini-cli/settings.json"
      )
      ;;
  esac

  for p in "${paths[@]}"; do
    if [ -f "$p" ]; then echo "$p"; return 0; fi
  done

  # Return default (first path) for creation
  echo "${paths[0]}"
}
```

---

## Status Value Semantics

| Status | Meaning | Backup? |
|--------|---------|---------|
| `created` | New file written from template | No |
| `merged` | Existing file modified | Yes |
| `already` | Hook already present, no changes | No (removed) |
| `failed` | Python3/jq missing or error | No (rolled back) |
| `skipped` | Agent not installed | No |
| `unsupported` | Agent has no hook mechanism | No |
| `conflict` | Existing file from another tool | No |
| `no_repo` | Copilot needs git repo, not in one | No |
