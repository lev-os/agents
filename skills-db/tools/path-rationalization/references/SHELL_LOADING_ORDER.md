# Shell Config File Loading Order

Understanding which file loads when is critical for correct PATH management.

## Zsh Loading Order

```
Login shell (ssh, new terminal tab):
  1. /etc/zshenv
  2. ~/.zshenv          ← ALWAYS loaded, even non-interactive scripts
  3. /etc/zprofile
  4. ~/.zprofile         ← Login shells only
  5. /etc/zshrc
  6. ~/.zshrc            ← Interactive shells only
  7. /etc/zlogin
  8. ~/.zlogin

Interactive non-login (new shell in terminal):
  1. /etc/zshenv
  2. ~/.zshenv
  3. /etc/zshrc
  4. ~/.zshrc

Non-interactive script (zsh -c 'cmd'):
  1. /etc/zshenv
  2. ~/.zshenv           ← Only these two!
```

### Key Insight for PATH

- **~/.zshenv**: PATH entries here affect ALL zsh invocations including scripts, subshells, non-interactive. Use for essential tools that scripts depend on (cargo, node, local bins).
- **~/.zshrc**: PATH entries here affect only interactive shells. Use for convenience tools, completion paths, interactive-only additions.
- **~/.zprofile**: Rarely needed. Use for login-time-only setup.

### Common Mistake

Adding PATH entries to both `~/.zshenv` AND `~/.zshrc` causes duplicates because both are sourced for interactive shells.

**Fix:** Put core PATH in `~/.zshenv` with dedup guards. Put interactive-only additions in `~/.zshrc` with dedup guards.

## Bash Loading Order

```
Login shell (ssh, `bash -l`):
  1. /etc/profile
  2. First found of:
     - ~/.bash_profile
     - ~/.bash_login
     - ~/.profile         ← Only if the above two don't exist!
  3. (On exit: ~/.bash_logout)

Interactive non-login (`bash` in terminal):
  1. /etc/bash.bashrc
  2. ~/.bashrc

Non-interactive (`bash -c 'cmd'`):
  1. File in $BASH_ENV (if set)
```

### Key Insight for PATH

- **~/.profile**: Loaded by bash login shells (and sh). Good for PATH entries that should be available everywhere.
- **~/.bashrc**: Loaded by interactive non-login bash. Most common place for user PATH additions.
- **~/.bash_profile**: If this exists, `~/.profile` is NOT loaded by bash! Many setups have `~/.bash_profile` source `~/.bashrc`.

### Common Mistake

Having `~/.bash_profile` that doesn't source `~/.bashrc` means interactive login shells miss bashrc PATH entries. Standard fix:

```bash
# ~/.bash_profile
[ -f ~/.bashrc ] && source ~/.bashrc
```

## Recommended PATH Architecture

```
~/.zshenv (or ~/.profile for bash):
  - ~/.local/bin (user binaries — canonical location)
  - ~/.cargo/bin (Rust)
  - Node.js (via fnm/nvm dynamic detection)

~/.zshrc (or ~/.bashrc):
  - ~/.bun/bin (Bun — interactive convenience)
  - Dynamic entries (FNM_MULTISHELL_PATH)
  - Tool-specific (google-cloud-sdk, etc.)

NEVER in any config file:
  - /tmp/* paths
  - /run/user/* paths (ephemeral)
  - /data/tmp/* paths
  - Hardcoded absolute paths to session-specific dirs
```

## Deduplication Template

Use this pattern everywhere to prevent duplicates:

```bash
# Idempotent PATH addition — safe to source multiple times
path_add() {
  case ":$PATH:" in
    *:"$1":*) ;;
    *) export PATH="$1:$PATH" ;;
  esac
}

path_add "$HOME/.local/bin"
path_add "$HOME/.cargo/bin"
path_add "$HOME/go/bin"
```

Or inline without a function:

```bash
case ":$PATH:" in
  *:"$HOME/.local/bin":*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac
```
