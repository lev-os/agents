---
name: chezmoi
description: Manage dotfiles across multiple machines with chezmoi. Use when working with dotfile management, templating, secrets, machine-specific configs, or chezmoi commands.
---

# Chezmoi Dotfile Manager

Manage your dotfiles across multiple diverse machines, securely.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `chezmoi init` | Initialize chezmoi (creates ~/.local/share/chezmoi) |
| `chezmoi add <file>` | Add file to source state |
| `chezmoi edit <file>` | Edit source version of file |
| `chezmoi diff` | Preview changes before applying |
| `chezmoi apply` | Apply changes to home directory |
| `chezmoi update` | Pull latest changes and apply |
| `chezmoi cd` | Open shell in source directory |
| `chezmoi doctor` | Check for problems |

## One-liner Bootstrap

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply $GITHUB_USERNAME
```

## Core Concepts

### Source State vs Target State

- **Source state**: Files in `~/.local/share/chezmoi/` (managed by chezmoi)
- **Target state**: Files in your home directory (what chezmoi manages)
- **Destination directory**: Usually `~` (your home)

### File Naming Conventions

| Prefix/Suffix | Meaning | Example |
|---------------|---------|---------|
| `dot_` | Creates `.` prefix | `dot_bashrc` → `.bashrc` |
| `private_` | Mode 0600 | `private_dot_ssh/` |
| `executable_` | Mode +x | `executable_dot_local/bin/myscript` |
| `readonly_` | Read-only | `readonly_dot_config/` |
| `empty_` | Create empty file | `empty_dot_gitkeep` |
| `symlink_` | Create symlink | `symlink_dot_config` |
| `.tmpl` | Template file | `dot_bashrc.tmpl` |

### Directory Attributes

```
~/.local/share/chezmoi/
├── dot_config/
│   ├── exact_nvim/           # exact_ = remove unlisted files
│   └── private_gnupg/        # private_ = mode 0700
├── private_dot_ssh/
│   └── private_config        # mode 0600
└── dot_bashrc.tmpl           # template
```

## Templating

### Basic Template Syntax

```
{{ .chezmoi.hostname }}       # Current hostname
{{ .chezmoi.os }}             # darwin, linux, windows
{{ .chezmoi.arch }}           # amd64, arm64
{{ .chezmoi.username }}       # Current user
{{ .chezmoi.homeDir }}        # Home directory path
```

### Conditionals

```bash
# dot_bashrc.tmpl
{{ if eq .chezmoi.os "darwin" -}}
export HOMEBREW_PREFIX="/opt/homebrew"
{{ else if eq .chezmoi.os "linux" -}}
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end -}}
```

### Machine-specific Config

Create `~/.config/chezmoi/chezmoi.toml` for machine-specific data:

```toml
[data]
    email = "me@work.com"
    git_signing_key = "ABC123"
    
[data.work]
    enabled = true
```

Then in templates:
```
{{ .email }}
{{ if .work.enabled }}
# Work-specific config
{{ end }}
```

### Prompt for Data on Init

Create `.chezmoi.<format>.tmpl` (e.g., `.chezmoi.toml.tmpl`):

```toml
[data]
    email = {{ promptString "Email address" | quote }}
    signingkey = {{ promptString "GPG signing key" | quote }}
```

## Password Manager Integration

### 1Password

```toml
# In template
{{ onepasswordRead "op://vault/item/field" }}
{{ (onepassword "item-name").password }}
```

### Bitwarden

```toml
{{ (bitwarden "item-name").login.password }}
```

### pass (Unix Password Store)

```toml
{{ pass "path/to/secret" }}
```

### Generic (Any Password Manager)

```toml
# In chezmoi.toml
[secret]
    command = "my-secret-tool"
    args = ["get"]

# In templates
{{ secret "secret-name" }}
```

## Encryption

### Using age (Recommended)

```bash
# Generate key
chezmoi age-keygen

# Configure in chezmoi.toml
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1..."
```

### Encrypt Files

```bash
# Add encrypted file
chezmoi add --encrypt ~/.ssh/id_rsa

# Result: encrypted_private_dot_ssh/private_id_rsa.age
```

## Scripts

### Run Scripts on Apply

| Prefix | Runs When |
|--------|-----------|
| `run_` | Every apply |
| `run_once_` | Only once (tracked by checksum) |
| `run_onchange_` | When script content changes |

### Script Ordering

Scripts run alphabetically. Use numeric prefixes:

```
.chezmoiscripts/
├── run_once_before_01-install-homebrew.sh
├── run_once_before_02-install-packages.sh
└── run_onchange_after_reload-shell.sh
```

### Script Template

```bash
#!/bin/bash
# run_once_before_install-packages.sh.tmpl

{{ if eq .chezmoi.os "darwin" -}}
brew bundle --file=/dev/stdin <<EOF
brew "ripgrep"
brew "fd"
cask "wezterm"
EOF
{{ else if eq .chezmoi.os "linux" -}}
sudo apt-get install -y ripgrep fd-find
{{ end -}}
```

## External Files

### Import from URL/Archive

Create `.chezmoiexternal.toml`:

```toml
[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    stripComponents = 1
    refreshPeriod = "168h"

[".local/bin/starship"]
    type = "file"
    url = "https://starship.rs/install.sh"
    executable = true
```

### Import from Git

```toml
[".tmux/plugins/tpm"]
    type = "git-repo"
    url = "https://github.com/tmux-plugins/tpm.git"
    refreshPeriod = "168h"
```

## Configuration File

Located at `~/.config/chezmoi/chezmoi.toml`:

```toml
# Source directory (default: ~/.local/share/chezmoi)
sourceDir = "~/.dotfiles"

# Diff tool
[diff]
    pager = "delta"

# Merge tool  
[merge]
    command = "nvim"
    args = ["-d", "{{ .Destination }}", "{{ .Source }}", "{{ .Target }}"]

# Git auto-commit
[git]
    autoCommit = true
    autoPush = false

# Data for templates
[data]
    name = "Your Name"
    email = "your@email.com"
```

## Common Workflows

### New Machine Setup

```bash
# Install chezmoi and apply dotfiles
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply $GITHUB_USERNAME
```

### Daily Updates

```bash
# Pull changes and apply
chezmoi update

# Or step-by-step
chezmoi git pull
chezmoi diff
chezmoi apply
```

### Adding New Files

```bash
chezmoi add ~/.bashrc                    # Regular file
chezmoi add --encrypt ~/.ssh/config      # Encrypted
chezmoi add --template ~/.gitconfig      # As template
chezmoi add --autotemplate ~/.config/X   # Auto-detect template
```

### Editing Files

```bash
chezmoi edit ~/.bashrc     # Edit source, then apply
chezmoi edit-config        # Edit chezmoi.toml
```

## Troubleshooting

See `references/troubleshooting.md` for common issues including:
- Vimpager/AnsiEsc ANSI escape code issues
- Diff pager configuration
- Encryption setup problems

## References

- **Official Docs**: https://www.chezmoi.io/
- **GitHub**: https://github.com/twpayne/chezmoi
- **Quick Start**: https://www.chezmoi.io/quick-start/
- **User Guide**: https://www.chezmoi.io/user-guide/
- **Reference**: https://www.chezmoi.io/reference/

## Template Functions Reference

### Filesystem

| Function | Description |
|----------|-------------|
| `glob "pattern"` | Find files matching pattern |
| `include "path"` | Include file contents |
| `stat "path"` | Get file info |
| `lookPath "cmd"` | Find command in PATH |

### Strings

| Function | Description |
|----------|-------------|
| `contains "substr" "str"` | Check substring |
| `hasPrefix "pre" "str"` | Check prefix |
| `hasSuffix "suf" "str"` | Check suffix |
| `replace "old" "new" "str"` | Replace in string |
| `trim "str"` | Trim whitespace |
| `quote "str"` | Quote for TOML |

### Data Formats

| Function | Description |
|----------|-------------|
| `toJson .data` | Convert to JSON |
| `toToml .data` | Convert to TOML |
| `toYaml .data` | Convert to YAML |
| `fromJson "str"` | Parse JSON |
| `fromToml "str"` | Parse TOML |
| `fromYaml "str"` | Parse YAML |

### Execution

| Function | Description |
|----------|-------------|
| `output "cmd" "args"...` | Run command, return output |
| `env "VAR"` | Get environment variable |
