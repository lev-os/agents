#!/usr/bin/env bash
set -euo pipefail

PROFILE="full"
WRITE_SHELL_RC=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --profile)
      PROFILE="${2:?Missing value for --profile}"
      shift 2
      ;;
    --write-shell-rc)
      WRITE_SHELL_RC=1
      shift
      ;;
    --help|-h)
      cat <<'EOF'
Usage: install.sh [--profile core|full] [--write-shell-rc]

Profiles:
  core  - portable baseline for clean Linux/macOS environments
  full  - core + niche toolchain where package managers support it
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

KIT_HOME="${HOME}/.agent-field-kit"
ENV_FILE="${KIT_HOME}/env.sh"
mkdir -p "$KIT_HOME"

log() {
  printf '%s\n' "$*"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

append_once() {
  local line="$1"
  local target="$2"
  touch "$target"
  grep -Fqx "$line" "$target" || printf '%s\n' "$line" >>"$target"
}

write_env_file() {
  cat >"$ENV_FILE" <<'EOF'
export PATH="$HOME/.local/bin:$PATH"

if command -v fdfind >/dev/null 2>&1 && ! command -v fd >/dev/null 2>&1; then
  alias fd='fdfind'
fi

if command -v ntm >/dev/null 2>&1; then
  if [ -n "${ZSH_VERSION:-}" ] && command -v compdef >/dev/null 2>&1; then
    eval "$(ntm shell zsh 2>/dev/null || true)"
  elif [ -n "${BASH_VERSION:-}" ]; then
    eval "$(ntm shell bash 2>/dev/null || true)"
  fi
fi
EOF
}

install_homebrew_formulae() {
  local formulae=("$@")
  if [ "${#formulae[@]}" -eq 0 ]; then
    return 0
  fi
  brew install "${formulae[@]}"
}

install_homebrew_if_missing() {
  local formula="$1"
  local binary="$2"
  if command_exists "$binary"; then
    log "Skipping $formula ($binary already present)"
    return 0
  fi
  brew install "$formula"
}

install_apt_packages() {
  local packages=("$@")
  if [ "${#packages[@]}" -eq 0 ]; then
    return 0
  fi
  sudo apt-get update
  sudo apt-get install -y "${packages[@]}"
}

install_npm_globals() {
  local packages=("$@")
  if [ "${#packages[@]}" -eq 0 ]; then
    return 0
  fi
  npm install -g "${packages[@]}"
}

install_npm_if_missing() {
  local package="$1"
  local binary="$2"
  if command_exists "$binary"; then
    log "Skipping $package ($binary already present)"
    return 0
  fi
  npm install -g "$package"
}

OS="$(uname -s)"

log "=== Agent Field Kit Install ==="
log "Profile: $PROFILE"
log "OS: $OS"
log ""

write_env_file

# On chezmoi-managed machines, packages.toml is the single source of truth.
# Field kit only uses its own hardcoded list as a fallback for containers/remote.
if command_exists dotfiles; then
  log "Detected chezmoi-managed machine — delegating to dotfiles packages"
  dotfiles packages
  # npm-only tools not in packages.toml
  if [ "$PROFILE" = "full" ]; then
    install_npm_if_missing agentmail-cli agentmail
  fi
elif [ "$OS" = "Darwin" ] || { [ "$OS" = "Linux" ] && command_exists brew; }; then
  command_exists brew || {
    echo "Homebrew is required on macOS" >&2
    exit 1
  }

  # Fallback: hardcoded list for environments without chezmoi
  log "No chezmoi detected — using embedded tool list"
  install_homebrew_if_missing ripgrep rg
  install_homebrew_if_missing fd fd
  install_homebrew_if_missing fzf fzf
  install_homebrew_if_missing duckdb duckdb
  install_homebrew_if_missing git-delta delta
  install_homebrew_if_missing xh xh
  install_homebrew_if_missing watchexec watchexec
  install_homebrew_if_missing just just
  install_homebrew_if_missing semgrep semgrep
  install_homebrew_if_missing repomix repomix
  install_homebrew_if_missing tree tree
  install_homebrew_if_missing tmux tmux

  if [ "$PROFILE" = "full" ]; then
    install_homebrew_if_missing dicklesworthstone/tap/dcg dcg
    install_npm_if_missing agentmail-cli agentmail
  fi
elif [ "$OS" = "Linux" ] && command_exists apt-get; then
  install_apt_packages curl git ca-certificates ripgrep fd-find fzf tree tmux python3 python3-pip npm
  if [ "$PROFILE" = "full" ]; then
    log "Full Linux profile is best-effort without Homebrew; baseline installed, advanced tools may need manual follow-up."
    install_npm_if_missing agentmail-cli agentmail || true
  fi
else
  echo "Unsupported environment: need chezmoi, Homebrew, or apt-get" >&2
  exit 1
fi

if [ "$WRITE_SHELL_RC" -eq 1 ]; then
  if [ -n "${ZSH_VERSION:-}" ] || [ -f "${HOME}/.zshrc" ]; then
    append_once 'source "$HOME/.agent-field-kit/env.sh"' "${HOME}/.zshrc"
  fi
  if [ -n "${BASH_VERSION:-}" ] || [ -f "${HOME}/.bashrc" ]; then
    append_once 'source "$HOME/.agent-field-kit/env.sh"' "${HOME}/.bashrc"
  fi
fi

log ""
log "Wrote env helper: $ENV_FILE"
log "Load it now with: source $ENV_FILE"
log ""
log "Suggested verification:"
log "  command -v rg fd fzf tree tmux"
log "  command -v duckdb delta xh watchexec just semgrep || true"
log "  command -v dcg cass ubs ntm agentmail || true"
