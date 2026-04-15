# Operational Patterns

> **Principle**: Production MCP servers need robust installation, multi-agent detection, and operational scripts that compose well with existing tooling.

## Multi-Stage Installation

Split installation into discrete, resumable stages:

```bash
# scripts/install.sh - User-facing entry point
#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib.sh"

main() {
    log_info "MCP Agent Mail Installation"

    # Stage 1: Prerequisites
    check_prerequisites || {
        log_error "Prerequisites not met. Please install: python3, pip, git"
        exit 1
    }

    # Stage 2: Python environment
    setup_python_env

    # Stage 3: Configuration
    configure_settings

    # Stage 4: Agent detection and integration
    detect_and_integrate_agents

    # Stage 5: Validation
    validate_installation

    log_success "Installation complete!"
}

main "$@"
```

## Shared Bash Library (lib.sh)

Reusable functions for all scripts (~18KB):

```bash
# scripts/lib.sh - Shared functions
#!/usr/bin/env bash

# --- Logging ---
log_info()    { echo "[INFO]  $*"; }
log_warn()    { echo "[WARN]  $*" >&2; }
log_error()   { echo "[ERROR] $*" >&2; }
log_success() { echo "[OK]    $*"; }
log_debug()   { [[ "${DEBUG:-}" == "1" ]] && echo "[DEBUG] $*"; }

# --- Atomic File Operations ---
atomic_write() {
    local target="$1"
    local content="$2"
    local mode="${3:-0644}"

    local tmpfile
    tmpfile=$(mktemp "${target}.XXXXXX")

    # Write to temp file
    printf '%s' "$content" > "$tmpfile"

    # Set permissions before moving (more secure)
    chmod "$mode" "$tmpfile"

    # Atomic move
    mv -f "$tmpfile" "$target"
}

atomic_append() {
    local target="$1"
    local content="$2"

    # Use flock for append safety
    (
        flock -x 200
        printf '%s\n' "$content" >> "$target"
    ) 200>"$target.lock"
    rm -f "$target.lock"
}

# --- JSON Manipulation ---
json_get() {
    local file="$1"
    local key="$2"
    python3 -c "import json; print(json.load(open('$file')).get('$key', ''))"
}

json_set() {
    local file="$1"
    local key="$2"
    local value="$3"

    local tmpfile
    tmpfile=$(mktemp)

    python3 -c "
import json
with open('$file', 'r') as f:
    data = json.load(f)
data['$key'] = '$value'
with open('$tmpfile', 'w') as f:
    json.dump(data, f, indent=2)
"
    mv -f "$tmpfile" "$file"
}

# --- Process Management ---
is_process_running() {
    local pidfile="$1"
    [[ -f "$pidfile" ]] && kill -0 "$(cat "$pidfile")" 2>/dev/null
}

wait_for_process() {
    local pidfile="$1"
    local timeout="${2:-30}"

    local elapsed=0
    while is_process_running "$pidfile"; do
        sleep 1
        ((elapsed++))
        if [[ $elapsed -ge $timeout ]]; then
            return 1
        fi
    done
    return 0
}

# --- Token Management ---
get_api_token() {
    local name="$1"

    # Token cascade: env -> .env -> keychain -> generate -> fail
    # 1. Environment variable
    local env_var="${name^^}_API_KEY"
    if [[ -n "${!env_var:-}" ]]; then
        echo "${!env_var}"
        return 0
    fi

    # 2. .env file
    if [[ -f "$HOME/.env" ]]; then
        local value
        value=$(grep "^${env_var}=" "$HOME/.env" | cut -d= -f2-)
        if [[ -n "$value" ]]; then
            echo "$value"
            return 0
        fi
    fi

    # 3. Keychain (macOS)
    if command -v security &>/dev/null; then
        local value
        value=$(security find-generic-password -s "$name" -w 2>/dev/null || true)
        if [[ -n "$value" ]]; then
            echo "$value"
            return 0
        fi
    fi

    # 4. Failed - return empty
    return 1
}
```

## Multi-Agent Auto-Detection

Detect all installed coding agents:

```bash
# scripts/detect_agents.sh
#!/usr/bin/env bash
source "$(dirname "$0")/lib.sh"

# Known agent config locations
declare -A AGENT_CONFIGS=(
    ["claude-code"]="$HOME/.claude/settings.json"
    ["codex-cli"]="$HOME/.codex/config.yaml"
    ["cursor"]="$HOME/.cursor/settings.json"
    ["continue"]="$HOME/.continue/config.json"
    ["aider"]="$HOME/.aider.conf.yml"
    ["copilot"]="$HOME/.config/github-copilot/hosts.json"
    ["gemini-cli"]="$HOME/.gemini/config.json"
    ["cline"]="$HOME/.cline/settings.json"
    ["windsurf"]="$HOME/.windsurf/config.json"
    ["bolt"]="$HOME/.bolt/settings.json"
)

# Detect by checking config file existence
detect_agents() {
    local detected=()

    for agent in "${!AGENT_CONFIGS[@]}"; do
        local config="${AGENT_CONFIGS[$agent]}"
        if [[ -f "$config" ]]; then
            detected+=("$agent")
            log_info "Detected: $agent ($config)"
        fi
    done

    # Also check for running processes
    for proc in claude codex cursor aider gemini; do
        if pgrep -x "$proc" &>/dev/null; then
            if [[ ! " ${detected[*]} " =~ " $proc " ]]; then
                detected+=("$proc")
                log_info "Detected (running): $proc"
            fi
        fi
    done

    printf '%s\n' "${detected[@]}"
}

# Get config path for an agent
get_agent_config() {
    local agent="$1"
    echo "${AGENT_CONFIGS[$agent]:-}"
}
```

## Per-IDE Integration Scripts

Separate scripts for each agent integration:

```bash
# scripts/integrations/claude.sh
#!/usr/bin/env bash
source "$(dirname "$0")/../lib.sh"

CLAUDE_SETTINGS="$HOME/.claude/settings.json"
CLAUDE_MCP_CONFIG="$HOME/.claude/claude_desktop_config.json"

integrate_claude() {
    log_info "Integrating with Claude Code..."

    # Ensure config directory exists
    mkdir -p "$(dirname "$CLAUDE_MCP_CONFIG")"

    # Add MCP server configuration
    local mcp_entry
    mcp_entry=$(cat <<'JSON'
{
  "mcpServers": {
    "mcp-agent-mail": {
      "command": "python",
      "args": ["-m", "mcp_agent_mail"],
      "env": {
        "MCP_AGENT_MAIL_DB": "${HOME}/.mcp-agent-mail/db.sqlite"
      }
    }
  }
}
JSON
)

    if [[ -f "$CLAUDE_MCP_CONFIG" ]]; then
        # Merge with existing config
        python3 -c "
import json
with open('$CLAUDE_MCP_CONFIG') as f:
    existing = json.load(f)
new_config = json.loads('''$mcp_entry''')
existing.setdefault('mcpServers', {}).update(new_config['mcpServers'])
with open('$CLAUDE_MCP_CONFIG', 'w') as f:
    json.dump(existing, f, indent=2)
"
    else
        echo "$mcp_entry" > "$CLAUDE_MCP_CONFIG"
    fi

    log_success "Claude Code integration complete"
}

# Add SessionStart hook for inbox checking
add_claude_hooks() {
    local hooks_dir="$HOME/.claude/hooks"
    mkdir -p "$hooks_dir"

    # SessionStart hook
    cat > "$hooks_dir/session_start.sh" <<'HOOK'
#!/usr/bin/env bash
# Check inbox on session start
python3 -c "
from mcp_agent_mail import check_inbox
unread = check_inbox()
if unread:
    print(f'You have {unread} unread messages')
" 2>/dev/null || true
HOOK
    chmod +x "$hooks_dir/session_start.sh"
}
```

## Hook Injection Patterns

Inject lifecycle hooks into agent configurations:

```bash
# scripts/hooks/inject_hooks.sh
#!/usr/bin/env bash
source "$(dirname "$0")/../lib.sh"

# Hook types supported
HOOK_TYPES=("SessionStart" "PreToolUse" "PostToolUse" "SessionEnd")

inject_hook() {
    local agent="$1"
    local hook_type="$2"
    local script_path="$3"

    case "$agent" in
        claude-code)
            inject_claude_hook "$hook_type" "$script_path"
            ;;
        codex-cli)
            inject_codex_hook "$hook_type" "$script_path"
            ;;
        cursor)
            inject_cursor_hook "$hook_type" "$script_path"
            ;;
        *)
            log_warn "Hook injection not supported for: $agent"
            return 1
            ;;
    esac
}

inject_claude_hook() {
    local hook_type="$1"
    local script_path="$2"

    local settings_file="$HOME/.claude/settings.json"

    # Read existing settings
    if [[ ! -f "$settings_file" ]]; then
        echo '{}' > "$settings_file"
    fi

    # Add hook using Python for safe JSON manipulation
    python3 -c "
import json
with open('$settings_file') as f:
    settings = json.load(f)

settings.setdefault('hooks', {}).setdefault('$hook_type', [])
if '$script_path' not in settings['hooks']['$hook_type']:
    settings['hooks']['$hook_type'].append('$script_path')

with open('$settings_file', 'w') as f:
    json.dump(settings, f, indent=2)
"
    log_success "Injected $hook_type hook for Claude Code"
}
```

## Pre-commit Guard

Git hooks for coordination validation:

```bash
# scripts/hooks/pre-commit-guard.sh
#!/usr/bin/env bash
# Pre-commit hook that checks for file reservation conflicts

source "$(dirname "$0")/../lib.sh"

check_reservations() {
    # Get list of staged files
    local staged_files
    staged_files=$(git diff --cached --name-only)

    if [[ -z "$staged_files" ]]; then
        return 0
    fi

    # Check each file against reservations
    local conflicts=()
    while IFS= read -r file; do
        local reservation
        reservation=$(python3 -c "
from mcp_agent_mail import check_file_reservation
result = check_file_reservation('$file')
if result:
    print(f'{result[\"holder\"]} until {result[\"expires\"]}')
" 2>/dev/null)

        if [[ -n "$reservation" ]]; then
            conflicts+=("$file: reserved by $reservation")
        fi
    done <<< "$staged_files"

    if [[ ${#conflicts[@]} -gt 0 ]]; then
        log_error "File reservation conflicts detected:"
        printf '  %s\n' "${conflicts[@]}"
        log_info "Use 'mcp-agent-mail release' or wait for expiration"
        return 1
    fi

    return 0
}

main() {
    check_reservations
}

main "$@"
```

## Rate-Limited Polling

Inbox checking with rate limiting:

```bash
# scripts/hooks/check_inbox.sh
#!/usr/bin/env bash
source "$(dirname "$0")/../lib.sh"

LAST_CHECK_FILE="$HOME/.mcp-agent-mail/.last_inbox_check"
MIN_INTERVAL=300  # 5 minutes

should_check() {
    if [[ ! -f "$LAST_CHECK_FILE" ]]; then
        return 0
    fi

    local last_check
    last_check=$(cat "$LAST_CHECK_FILE")
    local now
    now=$(date +%s)

    if (( now - last_check >= MIN_INTERVAL )); then
        return 0
    fi

    return 1
}

check_inbox() {
    if ! should_check; then
        log_debug "Skipping inbox check (rate limited)"
        return 0
    fi

    # Update timestamp
    date +%s > "$LAST_CHECK_FILE"

    # Perform check
    local result
    result=$(python3 -c "
from mcp_agent_mail import fetch_inbox
inbox = fetch_inbox(urgent_only=True, limit=5)
for msg in inbox:
    print(f'[{msg[\"importance\"]}] {msg[\"subject\"]} (from {msg[\"from\"]})')
" 2>/dev/null)

    if [[ -n "$result" ]]; then
        echo "=== Urgent Messages ==="
        echo "$result"
        echo "======================="
    fi
}

check_inbox
```

## Notification Integration

Cross-platform notifications:

```bash
# scripts/notify.sh
#!/usr/bin/env bash
source "$(dirname "$0")/lib.sh"

notify() {
    local title="$1"
    local message="$2"
    local urgency="${3:-normal}"  # low, normal, critical

    # macOS
    if command -v osascript &>/dev/null; then
        osascript -e "display notification \"$message\" with title \"$title\""
        return 0
    fi

    # Linux with notify-send
    if command -v notify-send &>/dev/null; then
        notify-send -u "$urgency" "$title" "$message"
        return 0
    fi

    # Windows with powershell
    if command -v powershell.exe &>/dev/null; then
        powershell.exe -Command "
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
            \$template.SelectSingleNode('//text[@id=1]').InnerText = '$title'
            \$template.SelectSingleNode('//text[@id=2]').InnerText = '$message'
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('MCP Agent Mail').Show(\$template)
        " 2>/dev/null
        return 0
    fi

    # Fallback: terminal bell + message
    echo -e "\a$title: $message"
}

# Notify on urgent messages
notify_urgent() {
    local count="$1"
    if [[ "$count" -gt 0 ]]; then
        notify "MCP Agent Mail" "You have $count urgent message(s)" "critical"
    fi
}
```

## Validation and Health Checks

Comprehensive installation validation:

```bash
# scripts/validate.sh
#!/usr/bin/env bash
source "$(dirname "$0")/lib.sh"

validate_installation() {
    local errors=0

    # Check Python module
    log_info "Checking Python module..."
    if ! python3 -c "import mcp_agent_mail" 2>/dev/null; then
        log_error "Python module not installed"
        ((errors++))
    else
        log_success "Python module OK"
    fi

    # Check database
    log_info "Checking database..."
    local db_path="$HOME/.mcp-agent-mail/db.sqlite"
    if [[ ! -f "$db_path" ]]; then
        log_warn "Database not initialized (will be created on first use)"
    else
        log_success "Database OK"
    fi

    # Check agent integrations
    log_info "Checking agent integrations..."
    for agent in claude-code codex-cli cursor; do
        if is_agent_integrated "$agent"; then
            log_success "$agent integration OK"
        else
            log_warn "$agent not integrated"
        fi
    done

    # Check hooks
    log_info "Checking hooks..."
    local hooks_dir="$HOME/.claude/hooks"
    if [[ -d "$hooks_dir" ]] && [[ -n "$(ls -A "$hooks_dir" 2>/dev/null)" ]]; then
        log_success "Hooks installed"
    else
        log_warn "No hooks installed"
    fi

    if [[ $errors -gt 0 ]]; then
        log_error "Validation failed with $errors error(s)"
        return 1
    fi

    log_success "All validations passed"
    return 0
}

is_agent_integrated() {
    local agent="$1"
    case "$agent" in
        claude-code)
            grep -q "mcp-agent-mail" "$HOME/.claude/claude_desktop_config.json" 2>/dev/null
            ;;
        codex-cli)
            grep -q "mcp-agent-mail" "$HOME/.codex/config.yaml" 2>/dev/null
            ;;
        *)
            return 1
            ;;
    esac
}

validate_installation
```

## Do / Don't

**Do:**
- Split installation into resumable stages
- Use atomic file operations for config changes
- Support multiple agents with per-IDE scripts
- Implement rate limiting for polling
- Validate installation with health checks

**Don't:**
- Overwrite existing configs without backup
- Assume specific shell features (use POSIX where possible)
- Skip permission checks on script files
- Ignore cross-platform differences
- Hard-code paths (use variables)
