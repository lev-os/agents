---
name: installer-workmanship
description: >-
  Write production-grade curl|bash installers. Use when creating install.sh,
  curl-pipe-bash installer, or one-liner install for CLI tools.
---

<!-- TOC: Non-Negotiables | THE PLAN | Reference Installers | Output & Formatting | Platform & Preflight | Binary Acquisition | Agent Auto-Configuration | Shell Integration | Final Summary | Anti-Patterns | Checklist | References -->

# Installer Workmanship

> **Core Principle:** Study `/dp/destructive_command_guard/install.sh` and `/dp/remote_compilation_helper/install.sh` and emulate them in every respect. These are the gold standard. Every installer you write must match their quality.

## The Non-Negotiables

Every installer MUST have ALL of these. No exceptions. No "we'll add it later."

| Feature | Why | Reference |
|---------|-----|-----------|
| `set -euo pipefail` | Fail fast, catch errors | DCG line 24 |
| `shopt -s lastpipe 2>/dev/null` | `read` in pipelines works | RCH line 7 |
| Curl one-liner header with cache buster | Install docs in script | [DOWNLOAD-PATTERNS.md](references/DOWNLOAD-PATTERNS.md) |
| Proxy support (`PROXY_ARGS` array) | Corporate networks | [DOWNLOAD-PATTERNS.md](references/DOWNLOAD-PATTERNS.md) |
| Gum detection + ANSI fallback | Beautiful everywhere | DCG lines 53-107 |
| `draw_box()` with box-drawing chars | Professional headers | DCG lines 109-156 |
| `info/ok/warn/err` log functions | Consistent formatting | DCG lines 59-95 |
| `run_with_spinner()` | Show progress on slow ops | DCG lines 97-107 |
| Branded header banner | First impression | DCG lines 783-798 |
| Platform detection (OS + arch) | Cross-platform | DCG lines 439-461 |
| Preflight checks (disk, perms, net) | Fail early, fail clearly | DCG lines 544-550 |
| Atomic locking (mkdir-based) | No concurrent installs | DCG lines 870-892 |
| Checksum verification (SHA256) | Supply chain security | DCG lines 665-700 |
| Sigstore/cosign verification | Authenticity | DCG lines 703-737 |
| Build-from-source fallback | Works when binaries fail | DCG lines 910-927 |
| Shell completions install | Polish | DCG lines 578-644 |
| AI agent auto-configuration | Zero-friction setup | DCG lines 1069-1865 |
| Skill installation (tarball + inline fallback) | Agent knowledge | RCH lines 1070-1236 |
| Final summary with status per-agent | User knows what happened | DCG lines 1941-2116 |
| Uninstall instructions | Reversibility | DCG lines 2103-2115 |
| `--quiet`, `--no-gum`, `--force` flags | Flexibility | DCG lines 28-51 |
| `--offline TARBALL` airgap mode | Works without internet | [DOWNLOAD-PATTERNS.md](references/DOWNLOAD-PATTERNS.md) |
| `trap cleanup EXIT` | Never leave temp files | DCG lines 894-900 |
| `umask 022` | Sane file permissions | DCG line 25 |

---

## THE PLAN

Follow this exact sequence when building an installer. Do NOT skip steps. Do NOT reorder.

```
Phase 1: Scaffold
  1. Copy the DCG installer structure (header, flags, logging, draw_box)
  2. Adapt project name, repo URL, binary names
  3. Wire up --help/usage with ALL flags documented

Phase 2: Core
  4. Platform detection (OS + arch → Rust triple, WSL detection)
  5. Proxy detection (HTTPS_PROXY → HTTP_PROXY → PROXY_ARGS array)
  6. Version resolution (CLI flag → Cargo.toml → GitHub API → redirect → hardcoded)
  7. Artifact URL construction (4-tier fallback chain)
  8. Preflight checks (disk space, write perms, network, existing install)
  9. Atomic locking (mkdir-based, stale PID detection)
  10. Download + extract (with build-from-source fallback)
  11. Checksum verification (dual tool: sha256sum/shasum + Sigstore)
  12. Install binary with `install -m 0755`

Phase 3: Integration
  13. Shell completions (bash/zsh/fish, XDG paths)
  14. PATH setup (--easy-mode auto-updates rc files)
  15. Service management if daemon (systemd user + launchd plist)
  16. AI agent detection (Claude Code, Codex, Gemini, Cursor, etc.)
  17. Agent hook auto-configuration (PreToolUse/BeforeTool hooks)
  18. Skill installation (tarball from releases, inline heredoc fallback)

Phase 4: Polish
  19. Self-test / --verify flag (post-install diagnostics)
  20. Predecessor detection and migration
  21. Final summary box (per-agent status, backup locations)
  22. Uninstall/revert instructions
```

---

## Reference Installers

**ALWAYS read these before writing ANY installer.** They are the canonical examples.

```bash
# THE gold standard (2116 lines)
cat /dp/destructive_command_guard/install.sh

# The companion reference (2600+ lines)
cat /dp/remote_compilation_helper/install.sh
```

### What to steal from DCG

- Gum + ANSI dual-path output system
- `draw_box()` with automatic width calculation and ANSI stripping
- Agent detection that scans for 7 agents with version reporting
- JSON settings merging via embedded Python3 (with backup + rollback)
- Version-already-installed short-circuit (skip download, still configure)
- Predecessor detection with upgrade banner showing feature comparison

### What to steal from RCH

- ASCII art banner with project name
- Multi-mode installer (`--local` / `--worker` / `--from-source`)
- `install_skill()` with tarball primary + inline heredoc fallback
- Service management (systemd user service + macOS launchd plist)
- Post-install diagnostics (`rch doctor`)
- Fleet harmonization (deploy to remote workers after local install)
- Proxy support (`HTTP_PROXY` / `HTTPS_PROXY`)

---

## Output & Formatting

### The Output Stack (Required)

```bash
# Detect gum (https://github.com/charmbracelet/gum)
HAS_GUM=0
if command -v gum &> /dev/null && [ -t 1 ]; then
  HAS_GUM=1
fi

# Every function: gum path + ANSI fallback
info() {
  [ "$QUIET" -eq 1 ] && return 0
  if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ]; then
    gum style --foreground 39 "-> $*"
  else
    echo -e "\033[0;34m->\033[0m $*"
  fi
}

ok()   { ... --foreground 42  ... "\033[0;32m" ... }  # green checkmark
warn() { ... --foreground 214 ... "\033[1;33m" ... }  # yellow warning
err()  { ... --foreground 196 ... "\033[0;31m" ... }  # red X (NO quiet gate)

run_with_spinner() {
  local title="$1"; shift
  if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ] && [ "$QUIET" -eq 0 ]; then
    gum spin --spinner dot --title "$title" -- "$@"
  else
    info "$title"
    "$@"
  fi
}
```

### Box Drawing (Required)

```bash
draw_box() {
  local color="$1"; shift
  local lines=("$@")
  # Strip ANSI for width calculation
  # Use double-line box chars: ══ ╔ ╗ ║ ╚ ╝
  # See DCG lines 109-156 for full implementation
}
```

### Header Banner (Required)

```bash
if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ]; then
  gum style \
    --border normal --border-foreground 39 \
    --padding "0 1" --margin "1 0" \
    "$(gum style --foreground 42 --bold 'project-name installer')" \
    "$(gum style --foreground 245 'One-line description')"
else
  echo -e "\033[1;32mproject-name installer\033[0m"
  echo -e "\033[0;90mOne-line description\033[0m"
fi
```

---

## Platform & Preflight

### Platform Detection

```bash
detect_platform() {
  OS=$(uname -s | tr 'A-Z' 'a-z')
  ARCH=$(uname -m)
  case "$ARCH" in
    x86_64|amd64) ARCH="x86_64" ;;
    arm64|aarch64) ARCH="aarch64" ;;
  esac
  case "${OS}-${ARCH}" in
    linux-x86_64)   TARGET="x86_64-unknown-linux-musl" ;;
    linux-aarch64)  TARGET="aarch64-unknown-linux-musl" ;;
    darwin-x86_64)  TARGET="x86_64-apple-darwin" ;;
    darwin-aarch64) TARGET="aarch64-apple-darwin" ;;
    *) warn "No prebuilt for ${OS}/${ARCH}; falling back to source"; FROM_SOURCE=1 ;;
  esac
}
```

**Always use musl for Linux** (static linking, portable binaries).

### WSL Detection

```bash
if [[ "$OS" == "linux" ]] && grep -qi microsoft /proc/version 2>/dev/null; then
  warn "WSL detected. Some features may need additional configuration"
  # Continue with linux platform — don't block
fi
```

### Preflight Checks

```bash
preflight_checks() {
  info "Running preflight checks"
  check_disk_space    # df -Pk, minimum 10MB
  check_write_permissions  # mkdir -p + writable test
  check_existing_install   # Report current version if present
  check_network            # curl --connect-timeout 3 to artifact URL
}
```

### Version Resolution

```bash
resolve_version() {
  # Primary: GitHub API
  curl -fsSL "https://api.github.com/repos/OWNER/REPO/releases/latest" \
    | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'

  # Fallback: redirect URL parsing
  curl -fsSL -o /dev/null -w '%{url_effective}' \
    "https://github.com/OWNER/REPO/releases/latest" | sed -E 's|.*/tag/||'
}
```

---

## Binary Acquisition

### Proxy Setup (Before Any Downloads)

```bash
setup_proxy() {
  PROXY_ARGS=()
  if [[ -n "${HTTPS_PROXY:-}" ]]; then
    PROXY_ARGS=(--proxy "$HTTPS_PROXY")
  elif [[ -n "${HTTP_PROXY:-}" ]]; then
    PROXY_ARGS=(--proxy "$HTTP_PROXY")
  fi
}
# Pass to EVERY curl call: curl -fsSL "${PROXY_ARGS[@]}" "$URL"
```

**Why a bash array?** `"${PROXY_ARGS[@]}"` expands to nothing when empty — no conditional curl construction.

### Download Strategy (4-Tier Fallback)

```
1. Versioned artifact: project-v{VERSION}-{TARGET}.tar.gz
2. Unversioned latest: /releases/latest/download/project-{TARGET}.tar.gz
3. Simple naming: project-{OS}-{ARCH}.tar.gz
4. Build from source: cargo build --release
```

After download:
- Verify checksum (SHA256 via `sha256sum` or `shasum -a 256`) — NEVER skip unless `--no-verify`
- Verify Sigstore bundle if cosign available (soft-skip if no cosign, hard-fail if cosign present + bad sig)
- Extract with tar -xf, find binary, `install -m 0755`

Full pattern with code: [DOWNLOAD-PATTERNS.md](references/DOWNLOAD-PATTERNS.md)

### Already-Installed Short-Circuit

```bash
if [ "$FORCE_INSTALL" -eq 0 ] && check_installed_version "$VERSION"; then
  ok "project $VERSION is already installed"
  info "Use --force to reinstall"
  # STILL run agent configuration (idempotent)
  exit 0
fi
```

---

## Agent Auto-Configuration

### Detection

```bash
detect_agents() {
  # Check for directories AND commands
  [[ -d "$HOME/.claude" ]] || command -v claude &>/dev/null  # Claude Code
  [[ -d "$HOME/.codex" ]]  || command -v codex &>/dev/null   # Codex CLI
  [[ -d "$HOME/.gemini" ]] || command -v gemini &>/dev/null  # Gemini CLI
  [[ -d "$HOME/.cursor" ]] || command -v cursor &>/dev/null  # Cursor IDE
  command -v aider &>/dev/null                                # Aider
  command -v copilot &>/dev/null                              # GitHub Copilot
  [[ -d "$HOME/.continue" ]]                                 # Continue
}
```

### Hook Configuration Pattern

For each agent that has hooks:

```
1. Check if already configured (grep for binary name) → skip if yes
2. Create timestamped backup: settings.bak.YYYYMMDDHHMMSS
3. If settings file exists → merge using embedded Python3 script
4. If settings file missing → create from heredoc template
5. Track status: created|merged|already|failed|skipped
```

**Claude Code hook** (PreToolUse, Bash matcher):
```json
{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"/path/to/binary"}]}]}}
```

**Gemini CLI hook** (BeforeTool, run_shell_command matcher):
```json
{"hooks":{"BeforeTool":[{"matcher":"run_shell_command","hooks":[{"name":"tool","type":"command","command":"/path/to/binary","timeout":5000}]}]}}
```

### Skill Installation

```bash
install_skill() {
  local claude_dest="$HOME/.claude/skills/project-name"
  local codex_dest="$HOME/.codex/skills/project-name"

  # Primary: download skill tarball from GitHub releases
  local skill_url="https://github.com/OWNER/REPO/releases/latest/download/skill.tar.gz"
  if curl -fsSL "$skill_url" -o "$TEMP/skill.tar.gz" 2>/dev/null; then
    tar -xzf "$TEMP/skill.tar.gz" -C "$HOME/.claude/skills"
    tar -xzf "$TEMP/skill.tar.gz" -C "$HOME/.codex/skills"
    return 0
  fi

  # Fallback: create minimal skill inline
  info "Creating minimal skill (download failed)..."
  cat > "$claude_dest/SKILL.md" << 'SKILL_EOF'
  # ... inline SKILL.md content ...
  SKILL_EOF
}
```

---

## Shell Integration

### Completions

```bash
install_completions_for_shell() {
  local shell="$1"
  case "$shell" in
    bash) target="${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions/project" ;;
    zsh)  target="${XDG_DATA_HOME:-$HOME/.local/share}/zsh/site-functions/_project" ;;
    fish) target="${XDG_CONFIG_HOME:-$HOME/.config}/fish/completions/project.fish" ;;
  esac
  mkdir -p "$(dirname "$target")"
  "$BINARY" completions "$shell" > "$target"
}
```

### PATH Setup

```bash
maybe_add_path() {
  case ":$PATH:" in
    *:"$DEST":*) return 0 ;;  # already in PATH
    *)
      if [ "$EASY" -eq 1 ]; then
        for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
          [ -e "$rc" ] && [ -w "$rc" ] && echo "export PATH=\"$DEST:\$PATH\"" >> "$rc"
        done
      else
        warn "Add $DEST to PATH to use project-name"
      fi
    ;;
  esac
}
```

---

## Final Summary

### Required Summary Box

```bash
# Build summary_lines array with per-agent status
# Show with gum style --border or draw_box fallback
# Include:
#   - Per-agent: Created|Merged|Already configured|Skipped|Failed
#   - Backup file locations
#   - What the tool does now
#   - Uninstall/revert instructions
```

### Status Tracking Pattern

```bash
CLAUDE_STATUS=""   # created|merged|already|failed
GEMINI_STATUS=""   # created|merged|already|failed|skipped
# ... per agent

# In summary:
case "$CLAUDE_STATUS" in
  created) summary_lines+=("Claude Code: Created settings with hook") ;;
  merged)  summary_lines+=("Claude Code: Added hook to existing settings") ;;
  already) summary_lines+=("Claude Code: Already configured") ;;
  failed)  summary_lines+=("Claude Code: Configuration failed") ;;
esac
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip checksum verification | Supply chain attacks | Always verify SHA256 |
| Use `gnu` target for Linux | Not portable | Use `musl` (static linking) |
| Modify settings without backup | Can't revert | `cp file file.bak.$(date +%s)` |
| Assume PATH includes `~/.local/bin` | Often doesn't | Check and offer `--easy-mode` |
| Hard-fail on optional features | Bad UX | Warn and continue |
| Use `flock` for locking | Not on macOS | Use `mkdir` (atomic everywhere) |
| Print raw text without formatting | Looks broken | Always use info/ok/warn/err |
| Skip the scan notice for slow ops | Users think it hung | Print notice BEFORE slow scan |
| Run `--version` without timeout | Some CLIs hang | Use `timeout 1` or `gtimeout 1` |
| Write JSON by hand in bash | Breaks on special chars | Use embedded Python3 for merges |
| Use `sha256sum` only | Not on macOS | Check `sha256sum` then `shasum -a 256` |
| Ignore proxy environment | Breaks in corp networks | `PROXY_ARGS` array on every curl |
| Skip `shopt -s lastpipe` | `read` in pipes fails | Add after `set -euo pipefail` |

---

## Checklist Before Shipping

- [ ] `set -euo pipefail` at top
- [ ] `umask 022` at top
- [ ] `trap cleanup EXIT` after temp dir creation
- [ ] Branded header with gum + ANSI fallback
- [ ] `--help` documents ALL flags
- [ ] curl one-liner with cache buster documented in header comment
- [ ] Platform detection covers linux/darwin x86_64/aarch64
- [ ] Preflight: disk space, write perms, network, existing install
- [ ] Atomic locking with stale PID detection
- [ ] SHA256 checksum verification
- [ ] Sigstore verification (best-effort, skip if no cosign)
- [ ] Build-from-source fallback
- [ ] Shell completions for detected shell
- [ ] AI agent detection and auto-configuration
- [ ] Skill installation with tarball + inline fallback
- [ ] Final summary with per-agent status
- [ ] Uninstall instructions shown
- [ ] All slow operations wrapped in spinner
- [ ] Agent scan notice printed before scan starts
- [ ] Version-already-installed short-circuit (still configures agents)
- [ ] Proxy support (`PROXY_ARGS` on every curl call)
- [ ] WSL detection with warning
- [ ] Dual checksum tool support (`sha256sum` / `shasum -a 256`)
- [ ] Tested with `bash install.sh --quiet` (no output except errors)
- [ ] Tested with `bash install.sh --no-gum` (ANSI fallback works)
- [ ] Tested with `bash install.sh --offline /path/to/tarball` (if applicable)

---

## References

| Need | Reference |
|------|-----------|
| Full DCG installer source | `/dp/destructive_command_guard/install.sh` |
| Full RCH installer source | `/dp/remote_compilation_helper/install.sh` |
| Agent hook JSON formats | [AGENT-HOOKS.md](references/AGENT-HOOKS.md) |
| Gum style recipes | [GUM-RECIPES.md](references/GUM-RECIPES.md) |
| Download, checksum, proxy, offline | [DOWNLOAD-PATTERNS.md](references/DOWNLOAD-PATTERNS.md) |
| JSON merge (Python3 + jq) | [PYTHON3-JSON-MERGE.md](references/PYTHON3-JSON-MERGE.md) |
| systemd + launchd services | [SERVICE-MANAGEMENT.md](references/SERVICE-MANAGEMENT.md) |
