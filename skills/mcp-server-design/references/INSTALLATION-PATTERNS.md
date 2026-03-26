# MCP Server Installation Patterns

## Table of Contents
- [Overview](#overview)
- [Multi-Agent Detection](#multi-agent-detection)
- [Configuration File Management](#configuration-file-management)
- [Token Cascade Pattern](#token-cascade-pattern)
- [Hook Injection](#hook-injection)
- [CLI Stub Trick](#cli-stub-trick)
- [Atomic File Operations](#atomic-file-operations)
- [Shared Bash Library](#shared-bash-library)
- [Uninstallation](#uninstallation)

---

## Overview

Installation is where MCP servers succeed or fail. A confusing installation process leads to:
- Abandoned integrations
- Misconfigured servers
- Support burden
- Bad first impressions

**Key insight:** Installation scripts are the first code users interact with. Make them excellent.

**mcp_agent_mail's approach:**
- Auto-detect all supported agent platforms
- Install to all detected platforms in one command
- Provide sensible defaults with override options
- Never require manual JSON editing
- Clean uninstallation that restores original state

---

## Multi-Agent Detection

### Detection Pattern

```bash
#!/usr/bin/env bash

# Detect installed agent platforms
detect_agent_platforms() {
    local platforms=()

    # Claude Code (official)
    if [[ -d "${HOME}/.claude" ]] || command -v claude &>/dev/null; then
        platforms+=("claude-code")
    fi

    # Codex CLI
    if [[ -f "${HOME}/.codex/config.json" ]] || command -v codex &>/dev/null; then
        platforms+=("codex-cli")
    fi

    # Cursor
    if [[ -d "${HOME}/.cursor" ]] || [[ -d "/Applications/Cursor.app" ]]; then
        platforms+=("cursor")
    fi

    # Gemini CLI
    if [[ -f "${HOME}/.gemini/settings.json" ]] || command -v gemini &>/dev/null; then
        platforms+=("gemini-cli")
    fi

    # Continue.dev
    if [[ -d "${HOME}/.continue" ]]; then
        platforms+=("continue")
    fi

    # Windsurf
    if [[ -d "${HOME}/.windsurf" ]]; then
        platforms+=("windsurf")
    fi

    echo "${platforms[@]}"
}
```

### Platform-Specific Config Paths

```bash
# Configuration file paths per platform
get_config_path() {
    local platform="$1"

    case "$platform" in
        claude-code)
            echo "${HOME}/.claude/claude_desktop_config.json"
            ;;
        codex-cli)
            echo "${HOME}/.codex/config.json"
            ;;
        cursor)
            # macOS vs Linux
            if [[ -d "/Applications/Cursor.app" ]]; then
                echo "${HOME}/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/config.json"
            else
                echo "${HOME}/.config/Cursor/User/globalStorage/cursor.mcp/config.json"
            fi
            ;;
        gemini-cli)
            echo "${HOME}/.gemini/settings.json"
            ;;
        continue)
            echo "${HOME}/.continue/config.json"
            ;;
        windsurf)
            echo "${HOME}/.windsurf/config.json"
            ;;
        *)
            echo ""
            ;;
    esac
}
```

### Install to All Detected Platforms

```bash
install_to_all_platforms() {
    local server_name="$1"
    local server_command="$2"
    local platforms
    platforms=($(detect_agent_platforms))

    if [[ ${#platforms[@]} -eq 0 ]]; then
        echo "No supported agent platforms detected."
        echo "Supported: claude-code, codex-cli, cursor, gemini-cli, continue, windsurf"
        exit 1
    fi

    echo "Detected platforms: ${platforms[*]}"

    for platform in "${platforms[@]}"; do
        echo "Installing to $platform..."
        install_to_platform "$platform" "$server_name" "$server_command"
    done

    echo "Installation complete for ${#platforms[@]} platform(s)."
}
```

---

## Configuration File Management

### JSON Configuration Update

```bash
# Add MCP server to config using jq
add_server_to_config() {
    local config_path="$1"
    local server_name="$2"
    local server_command="$3"
    local server_args="$4"
    local env_vars="$5"

    # Ensure parent directory exists
    mkdir -p "$(dirname "$config_path")"

    # Create empty config if doesn't exist
    if [[ ! -f "$config_path" ]]; then
        echo '{"mcpServers": {}}' > "$config_path"
    fi

    # Build server configuration
    local server_config
    server_config=$(jq -n \
        --arg cmd "$server_command" \
        --argjson args "$server_args" \
        --argjson env "$env_vars" \
        '{command: $cmd, args: $args, env: $env}')

    # Merge into existing config
    local tmp_file
    tmp_file=$(mktemp)

    jq --arg name "$server_name" \
       --argjson server "$server_config" \
       '.mcpServers[$name] = $server' \
       "$config_path" > "$tmp_file"

    # Atomic move
    mv "$tmp_file" "$config_path"

    echo "Added $server_name to $config_path"
}
```

### Remove Server from Config

```bash
remove_server_from_config() {
    local config_path="$1"
    local server_name="$2"

    if [[ ! -f "$config_path" ]]; then
        return 0
    fi

    local tmp_file
    tmp_file=$(mktemp)

    jq --arg name "$server_name" \
       'del(.mcpServers[$name])' \
       "$config_path" > "$tmp_file"

    mv "$tmp_file" "$config_path"

    echo "Removed $server_name from $config_path"
}
```

### Backup Before Modification

```bash
backup_config() {
    local config_path="$1"
    local backup_path="${config_path}.backup.$(date +%Y%m%d_%H%M%S)"

    if [[ -f "$config_path" ]]; then
        cp "$config_path" "$backup_path"
        echo "Backed up to $backup_path"
    fi
}
```

---

## Token Cascade Pattern

When MCP servers need API tokens, use a cascade to find them:

### Implementation

```bash
# Token discovery cascade
get_api_token() {
    local token_name="$1"
    local env_var_name="${token_name^^}_API_KEY"  # e.g., ANTHROPIC_API_KEY

    # 1. Environment variable (highest priority)
    if [[ -n "${!env_var_name}" ]]; then
        echo "${!env_var_name}"
        return 0
    fi

    # 2. .env file in current directory
    if [[ -f ".env" ]] && grep -q "^${env_var_name}=" ".env"; then
        grep "^${env_var_name}=" ".env" | cut -d= -f2-
        return 0
    fi

    # 3. .env file in home directory
    if [[ -f "${HOME}/.env" ]] && grep -q "^${env_var_name}=" "${HOME}/.env"; then
        grep "^${env_var_name}=" "${HOME}/.env" | cut -d= -f2-
        return 0
    fi

    # 4. Platform-specific credential store
    case "$(uname -s)" in
        Darwin)
            # macOS Keychain
            security find-generic-password -s "$token_name" -w 2>/dev/null && return 0
            ;;
        Linux)
            # secret-tool (GNOME Keyring)
            secret-tool lookup service "$token_name" 2>/dev/null && return 0
            ;;
    esac

    # 5. Generate/prompt as last resort
    return 1
}

# Usage in install script
setup_token() {
    local token_name="$1"
    local token

    token=$(get_api_token "$token_name")

    if [[ -z "$token" ]]; then
        echo "No $token_name API key found."
        echo "Please enter your $token_name API key (or press Enter to skip):"
        read -rs token

        if [[ -n "$token" ]]; then
            # Store for future use
            echo "${token_name^^}_API_KEY=$token" >> "${HOME}/.env"
            echo "Saved to ~/.env"
        fi
    fi

    echo "$token"
}
```

### Token Injection into Server Config

```bash
# Inject discovered tokens into server environment
configure_server_env() {
    local anthropic_key openai_key

    anthropic_key=$(get_api_token "anthropic")
    openai_key=$(get_api_token "openai")

    # Build env JSON
    local env_json='{}'

    if [[ -n "$anthropic_key" ]]; then
        env_json=$(echo "$env_json" | jq --arg key "$anthropic_key" '. + {ANTHROPIC_API_KEY: $key}')
    fi

    if [[ -n "$openai_key" ]]; then
        env_json=$(echo "$env_json" | jq --arg key "$openai_key" '. + {OPENAI_API_KEY: $key}')
    fi

    echo "$env_json"
}
```

---

## Hook Injection

MCP servers can inject hooks into agent configurations for enhanced functionality.

### Claude Code Hooks

```bash
# Inject hooks into Claude Code settings
inject_claude_hooks() {
    local settings_path="${HOME}/.claude/settings.json"
    local server_name="$1"

    # Create settings if doesn't exist
    if [[ ! -f "$settings_path" ]]; then
        echo '{"hooks": {}}' > "$settings_path"
    fi

    # SessionStart hook - register on session start
    local session_start_hook
    session_start_hook=$(cat <<'EOF'
{
    "type": "command",
    "command": "mcp-agent-mail-hook session-start"
}
EOF
)

    # PreToolUse hook - check reservations before edits
    local pre_tool_hook
    pre_tool_hook=$(cat <<'EOF'
{
    "type": "command",
    "command": "mcp-agent-mail-hook pre-tool",
    "matcher": {
        "toolName": ["Edit", "Write", "NotebookEdit"]
    }
}
EOF
)

    # Merge hooks into settings
    local tmp_file
    tmp_file=$(mktemp)

    jq --argjson session "$session_start_hook" \
       --argjson pretool "$pre_tool_hook" \
       '.hooks.SessionStart += [$session] | .hooks.PreToolUse += [$pretool]' \
       "$settings_path" > "$tmp_file"

    mv "$tmp_file" "$settings_path"

    echo "Injected hooks into Claude Code settings"
}
```

### Hook Types

```bash
# Available hook points
# SessionStart - Called when agent session starts
# PreToolUse   - Called before tool execution (can block)
# PostToolUse  - Called after tool execution
# Notification - For informational updates

# Hook response formats
# PreToolUse can return:
#   {"decision": "allow"}           - Proceed with tool
#   {"decision": "block", "reason": "..."} - Block with reason
#   {"decision": "modify", "params": {...}} - Modify parameters
```

### Composable Hook Chain

```bash
# Chain-runner pattern: Preserve existing hooks
inject_hook_composably() {
    local settings_path="$1"
    local hook_type="$2"
    local new_hook="$3"

    # Check if hook already exists (by command)
    local existing
    existing=$(jq -r ".hooks.${hook_type}[]?.command // empty" "$settings_path" 2>/dev/null)

    local new_command
    new_command=$(echo "$new_hook" | jq -r '.command')

    if echo "$existing" | grep -qF "$new_command"; then
        echo "Hook already exists, skipping"
        return 0
    fi

    # Append to existing hooks (don't replace)
    local tmp_file
    tmp_file=$(mktemp)

    jq --argjson hook "$new_hook" \
       --arg type "$hook_type" \
       '.hooks[$type] = (.hooks[$type] // []) + [$hook]' \
       "$settings_path" > "$tmp_file"

    mv "$tmp_file" "$settings_path"
}
```

---

## CLI Stub Trick

Agents sometimes try to invoke MCP servers as CLI commands. The CLI stub intercepts this and provides helpful guidance.

### Stub Implementation

```bash
#!/usr/bin/env bash
# Fake CLI stub: mcp-agent-mail
# Installed to PATH to intercept confused agents

cat <<'EOF'
╔══════════════════════════════════════════════════════════════════╗
║  mcp-agent-mail is an MCP server, not a CLI tool                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  You're likely an AI agent trying to invoke this from bash.      ║
║  MCP servers don't work that way!                                ║
║                                                                  ║
║  Instead, use the MCP tools directly:                            ║
║                                                                  ║
║    mcp__mcp-agent-mail__register_agent                           ║
║    mcp__mcp-agent-mail__send_message                             ║
║    mcp__mcp-agent-mail__fetch_inbox                              ║
║    mcp__mcp-agent-mail__file_reservation_paths                   ║
║                                                                  ║
║  For discovery, use resources:                                   ║
║                                                                  ║
║    resource://agents/{project_key}                               ║
║    resource://inbox/{project_key}/{agent_name}                   ║
║                                                                  ║
║  Need help? Read the tool docstrings or ask your human.          ║
╚══════════════════════════════════════════════════════════════════╝
EOF

exit 1
```

### Stub Installation

```bash
install_cli_stub() {
    local server_name="$1"
    local stub_content="$2"

    # Find writable bin directory in PATH
    local bin_dir
    for dir in "${HOME}/.local/bin" "${HOME}/bin" "/usr/local/bin"; do
        if [[ -d "$dir" && -w "$dir" ]]; then
            bin_dir="$dir"
            break
        fi
    done

    if [[ -z "$bin_dir" ]]; then
        mkdir -p "${HOME}/.local/bin"
        bin_dir="${HOME}/.local/bin"
        echo "Created ${bin_dir} - add to PATH if needed"
    fi

    # Install stub
    local stub_path="${bin_dir}/${server_name}"
    echo "$stub_content" > "$stub_path"
    chmod +x "$stub_path"

    # Create common aliases/typos
    for alias in "${server_name//-/_}" "${server_name//_/-}" "$(echo "$server_name" | tr '[:upper:]' '[:lower:]')"; do
        if [[ "$alias" != "$server_name" ]]; then
            ln -sf "$stub_path" "${bin_dir}/${alias}" 2>/dev/null || true
        fi
    done

    echo "Installed CLI stub to $stub_path"
}
```

---

## Atomic File Operations

Never corrupt config files during installation.

### Atomic Write Pattern

```bash
# Safe file write using temp + move
atomic_write() {
    local target_path="$1"
    local content="$2"

    # Create temp in same directory (ensures same filesystem)
    local tmp_file
    tmp_file=$(mktemp "$(dirname "$target_path")/.tmp.XXXXXX")

    # Write content
    echo "$content" > "$tmp_file"

    # Atomic move
    mv "$tmp_file" "$target_path"
}

# Safe JSON update
atomic_json_update() {
    local json_path="$1"
    local jq_filter="$2"

    local tmp_file
    tmp_file=$(mktemp "$(dirname "$json_path")/.tmp.XXXXXX")

    if jq "$jq_filter" "$json_path" > "$tmp_file"; then
        mv "$tmp_file" "$json_path"
        return 0
    else
        rm -f "$tmp_file"
        return 1
    fi
}
```

### Transactional Multi-File Updates

```bash
# Install to multiple platforms atomically
transactional_install() {
    local server_name="$1"
    local temp_dir
    temp_dir=$(mktemp -d)

    local platforms
    platforms=($(detect_agent_platforms))

    # Phase 1: Prepare all changes in temp
    for platform in "${platforms[@]}"; do
        local config_path
        config_path=$(get_config_path "$platform")

        if [[ -f "$config_path" ]]; then
            cp "$config_path" "${temp_dir}/${platform}.json"
        else
            echo '{"mcpServers": {}}' > "${temp_dir}/${platform}.json"
        fi

        # Apply changes to temp copy
        jq --arg name "$server_name" \
           '.mcpServers[$name] = {"command": "uvx", "args": ["mcp-agent-mail"]}' \
           "${temp_dir}/${platform}.json" > "${temp_dir}/${platform}.new.json"
    done

    # Phase 2: Validate all changes
    for platform in "${platforms[@]}"; do
        if ! jq empty "${temp_dir}/${platform}.new.json" 2>/dev/null; then
            echo "Validation failed for $platform"
            rm -rf "$temp_dir"
            return 1
        fi
    done

    # Phase 3: Commit all changes
    for platform in "${platforms[@]}"; do
        local config_path
        config_path=$(get_config_path "$platform")
        mkdir -p "$(dirname "$config_path")"
        mv "${temp_dir}/${platform}.new.json" "$config_path"
    done

    rm -rf "$temp_dir"
    echo "Installation committed to ${#platforms[@]} platforms"
}
```

---

## Shared Bash Library

Factor common functions into a shared library.

### lib.sh Structure

```bash
#!/usr/bin/env bash
# lib.sh - Shared utilities for MCP server installation

set -euo pipefail

# Colors (only if terminal supports)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# Logging
log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Dependency checking
require_command() {
    local cmd="$1"
    local install_hint="${2:-}"

    if ! command -v "$cmd" &>/dev/null; then
        log_error "Required command not found: $cmd"
        if [[ -n "$install_hint" ]]; then
            echo "  Install with: $install_hint"
        fi
        exit 1
    fi
}

# JSON utilities
json_get() {
    local json_path="$1"
    local jq_path="$2"
    jq -r "$jq_path" "$json_path" 2>/dev/null || echo ""
}

json_set() {
    local json_path="$1"
    local jq_filter="$2"
    atomic_json_update "$json_path" "$jq_filter"
}

# Platform detection
is_macos() { [[ "$(uname -s)" == "Darwin" ]]; }
is_linux() { [[ "$(uname -s)" == "Linux" ]]; }

# User confirmation
confirm() {
    local prompt="${1:-Continue?}"
    local default="${2:-n}"

    if [[ "$default" == "y" ]]; then
        prompt="$prompt [Y/n] "
    else
        prompt="$prompt [y/N] "
    fi

    read -rp "$prompt" response
    response=${response:-$default}

    [[ "$response" =~ ^[Yy] ]]
}
```

### Using the Library

```bash
#!/usr/bin/env bash
# install.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

# Now use shared functions
require_command "jq" "brew install jq / apt install jq"
require_command "uv" "curl -LsSf https://astral.sh/uv/install.sh | sh"

log_info "Installing MCP server..."

platforms=($(detect_agent_platforms))
log_info "Detected: ${platforms[*]}"

for platform in "${platforms[@]}"; do
    install_to_platform "$platform"
    log_ok "Installed to $platform"
done

log_ok "Installation complete!"
```

---

## Uninstallation

Clean uninstallation is as important as installation.

### Uninstall Script

```bash
#!/usr/bin/env bash
# uninstall.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

SERVER_NAME="mcp-agent-mail"

uninstall() {
    log_info "Uninstalling $SERVER_NAME..."

    # Remove from all platform configs
    for platform in claude-code codex-cli cursor gemini-cli continue windsurf; do
        local config_path
        config_path=$(get_config_path "$platform")

        if [[ -f "$config_path" ]]; then
            if jq -e ".mcpServers[\"$SERVER_NAME\"]" "$config_path" &>/dev/null; then
                remove_server_from_config "$config_path" "$SERVER_NAME"
                log_ok "Removed from $platform"
            fi
        fi
    done

    # Remove CLI stub
    for bin_dir in "${HOME}/.local/bin" "${HOME}/bin" "/usr/local/bin"; do
        if [[ -f "${bin_dir}/${SERVER_NAME}" ]]; then
            rm -f "${bin_dir}/${SERVER_NAME}"
            rm -f "${bin_dir}/${SERVER_NAME//-/_}"
            rm -f "${bin_dir}/${SERVER_NAME//_/-}"
            log_ok "Removed CLI stub from $bin_dir"
        fi
    done

    # Remove hooks (careful not to break other hooks)
    remove_hooks

    # Optionally remove data
    if confirm "Remove all $SERVER_NAME data (messages, agents, etc.)?"; then
        rm -rf "${HOME}/.mcp-agent-mail"
        log_ok "Removed data directory"
    fi

    log_ok "Uninstallation complete!"
}

remove_hooks() {
    local settings_path="${HOME}/.claude/settings.json"

    if [[ -f "$settings_path" ]]; then
        # Remove only our hooks, preserve others
        local tmp_file
        tmp_file=$(mktemp)

        jq 'walk(if type == "array" then map(select(.command? | (. == null or (. | contains("mcp-agent-mail") | not)))) else . end)' \
           "$settings_path" > "$tmp_file"

        mv "$tmp_file" "$settings_path"
        log_ok "Removed hooks from Claude settings"
    fi
}

uninstall "$@"
```

---

## Summary: Installation Checklist

| # | Pattern | Purpose |
|---|---------|---------|
| 1 | **Multi-agent detection** | Find all installed platforms |
| 2 | **Token cascade** | Find API keys without prompting |
| 3 | **Atomic writes** | Never corrupt config files |
| 4 | **CLI stub** | Catch confused bash invocations |
| 5 | **Composable hooks** | Preserve existing hooks |
| 6 | **Shared library** | DRY installation code |
| 7 | **Clean uninstall** | Remove all traces safely |
| 8 | **Transactional** | All-or-nothing multi-platform install |
