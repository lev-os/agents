# Chezmoi Troubleshooting

## Quick Diagnostics

```bash
chezmoi doctor    # First thing to run - checks for problems
chezmoi verify    # Verify target matches source state
chezmoi status    # Show what needs updating
chezmoi diff      # Show exact changes
chezmoi data      # Show available template data
```

---

## Pager Issues

### Vimpager + AnsiEsc ANSI Color Code Errors

**Symptom**: Running `chezmoi diff` produces garbage output or errors when using vimpager with the AnsiEsc plugin.

**Root Cause**: This is a vimpager + AnsiEsc plugin issue, not chezmoi itself. The AnsiEsc vim plugin chokes on ANSI color codes.

**Solutions (Ranked by Practicality)**:

#### 1. Change Chezmoi's Pager (Recommended - Instant Fix)

```bash
# One-time use
chezmoi diff --pager="less -R"

# Permanent fix in ~/.config/chezmoi/chezmoi.toml
[diff]
    pager = "less -R"
```

#### 2. Use Delta (Best UX - Recommended Investment)

```bash
# Install delta (modern diff viewer)
brew install git-delta

# Configure chezmoi
[diff]
    pager = "delta"
```

Delta provides:
- Syntax highlighting
- Side-by-side diffs
- Line numbers
- Git integration

#### 3. Disable Pager Entirely

```bash
chezmoi diff --no-pager
chezmoi diff | cat
```

#### 4. Fix Vimpager's AnsiEsc Plugin

```vim
" In ~/.vimrc or vimpager config
let g:no_cecutil_maps = 1
" Or disable AnsiEsc entirely for vimpager
```

#### 5. Bypass for Current Session

```bash
PAGER="less -R" chezmoi diff
```

### Diff Output Broken / No Color

**Symptom**: `chezmoi diff` shows monochrome output with raw escape sequences like `ESC[37m`.

**Cause**: Your pager doesn't pass through ANSI color codes.

**Fix**:
```bash
# Set LESS to handle raw control characters
export LESS=-R

# Or configure in chezmoi.toml
pager = "less -R"
```

### Trade-off Analysis

| Solution | Pros | Cons |
|----------|------|------|
| `less -R` | Zero install, instant | Basic diff display |
| `delta` | Beautiful diffs, syntax highlighting | Requires install |
| Disable pager | Works everywhere | Loses pagination |
| Fix vimpager | Fixes root cause | Vimpager + AnsiEsc is fragile |

**Recommendation**: Use delta for long-term investment, `less -R` for immediate fix.

---

## Script Execution Errors

### "exec format error" on Template Scripts

**Symptom**: `chezmoi: fork/exec /tmp/XXXXXXXXXX.XX: exec format error`

**Cause**: Newline before `#!` shebang in template.

**Wrong**:
```go
{{ if eq .chezmoi.os "linux" }}
#!/bin/bash
```

**Correct** (note the `-`):
```go
{{- if eq .chezmoi.os "linux" }}
#!/bin/bash
```

### "permission denied" Executing Scripts

**Symptom**: `chezmoi: fork/exec /tmp/XXXXXXXXXX.XX: permission denied`

**Cause**: Temp directory mounted with `noexec` option.

**Fix**: Configure a different script temp directory:

```toml
# ~/.config/chezmoi/chezmoi.toml
scriptTempDir = "~/tmp"
```

### "no such file or directory" on Nix/Termux

**Symptom**: `fork/exec ...: no such file or directory` when running scripts.

**Cause**: Hardcoded `/bin/bash` doesn't exist on Nix/Termux.

**Fix**: Use dynamic shebang:
```bash
#!{{ lookPath "bash" }}
```

Or use env:
```bash
#!/usr/bin/env bash
```

---

## Template Errors

### Testing Templates

```bash
# Test single expression
chezmoi execute-template '{{ .chezmoi.hostname }}'

# Test entire file
chezmoi execute-template < dot_bashrc.tmpl

# Show rendered output of managed file
chezmoi cat ~/.bashrc

# Debug with verbose output
chezmoi apply -v --debug
```

### "missingkey" Errors

**Symptom**: Template fails because a variable doesn't exist.

**Fix**: Configure lenient behavior:

```toml
# ~/.config/chezmoi/chezmoi.toml
[template]
    options = ["missingkey=zero"]
```

### Check Available Data

```bash
chezmoi data              # JSON format
chezmoi data --format=yaml
```

---

## Permission Issues

### "~/.ssh/config group writeable"

**Symptom**: SSH complains about config file permissions.

**Cause**: System umask is `002` (group writeable default).

**Fix**: Set explicit umask in config:

```toml
# ~/.config/chezmoi/chezmoi.toml
umask = 0o022
```

### Private File Permissions

Ensure private files use `private_` prefix:
```
private_dot_ssh/private_config    # Creates ~/.ssh/config with 0600
private_dot_gnupg/                # Creates ~/.gnupg with 0700
```

---

## Edit Command Issues

### Blank Buffer When Running `chezmoi edit`

**Symptom**: Editor opens with empty file, warning about "returned in less than 1s".

**Cause**: Editor command forks and exits immediately (e.g., GUI editors).

**Fix**: Configure editor to wait:

```toml
# For VS Code
[edit]
    command = "code"
    args = ["--wait"]

# For Vim (if forking)
[edit]
    command = "vim"
    args = ["-f"]
```

Or set environment variable:
```bash
export EDITOR="code --wait"
export EDITOR="vim -f"
```

---

## Init and Setup Issues

### "file already exists" on Init

**Preview first**:
```bash
chezmoi init --dry-run $GITHUB_USERNAME
```

**Force overwrite** (careful!):
```bash
chezmoi init --force $GITHUB_USERNAME
```

### "mkdir: no such file or directory"

**Symptom**: Can't add file when parent is managed by `.chezmoiexternal`.

**Cause**: Directory exists via external but not in source state.

**Fix**: Create directory placeholder in source:
```bash
chezmoi cd
mkdir -p dot_config/
touch dot_config/.keep
```

---

## State and Lock Issues

### "timeout" or "timeout obtaining persistent state lock"

**Symptom**: chezmoi reports timeout errors.

**Cause**: Another chezmoi instance is running (including from scripts).

**Check**: Look for other chezmoi processes:
```bash
ps aux | grep chezmoi
```

**Commands that write-lock**: `add`, `apply`, `edit`, `forget`, `import`, `init`, `state`, `unmanage`, `update`

**Commands that read-lock**: `diff`, `status`, `verify`

### "user: lookup userid NNNNN: input/output error"

**Cause**: Using musl-compiled binary with LDAP/NIS.

**Fix**: Use distribution package (`.deb`, `.rpm`) instead of static binary.

---

## Platform-Specific Issues

### macOS

```bash
# Install via Homebrew
brew install chezmoi

# Check Homebrew PATH in templates
{{ if eq .chezmoi.os "darwin" }}
{{ if eq .chezmoi.arch "arm64" }}
export PATH="/opt/homebrew/bin:$PATH"
{{ else }}
export PATH="/usr/local/bin:$PATH"
{{ end }}
{{ end }}
```

### Linux

```bash
# Check distro in templates
{{ if eq .chezmoi.osRelease.id "ubuntu" }}
# Ubuntu-specific
{{ else if eq .chezmoi.osRelease.id "fedora" }}
# Fedora-specific
{{ end }}
```

### Windows

```powershell
# Install via Scoop
scoop install chezmoi

# Or WinGet
winget install chezmoi
```

---

## Encryption Issues

### Check Setup

```bash
chezmoi doctor    # Shows encryption status
```

### age Encryption

```bash
# Generate key
chezmoi age-keygen

# Configure
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1..."

# Test
chezmoi decrypt encrypted_file.age
```

### GPG Encryption

```bash
# Configure
[gpg]
    recipient = "your-key-id"

# Ensure GPG agent is running
gpg-agent --daemon
```

---

## Git Integration Issues

### Conflicts After Update

```bash
# See differences
chezmoi diff

# Merge specific file
chezmoi merge ~/.bashrc

# Re-add to resolve (overwrites source with target)
chezmoi re-add ~/.bashrc
```

### Auto-commit Changes

```toml
# ~/.config/chezmoi/chezmoi.toml
[git]
    autoCommit = true
    autoPush = false    # Set true to auto-push
```

---

## Snap Installation Issues

### "permission denied" with Redirects

**Symptom**: `read /dev/stdin: permission denied` or `write /dev/stdout: permission denied`

**Cause**: [Known snap bug](https://bugs.launchpad.net/ubuntu/+source/snapd/+bug/1849753).

**Workarounds**:

For stdin:
```bash
# Instead of: chezmoi cmd < file
cat file | chezmoi cmd
```

For stdout:
```bash
# Instead of: chezmoi cmd > file
chezmoi cmd -o file
chezmoi cmd --output=file
chezmoi cmd | tee file > /dev/null
```

**Better solution**: Install via non-snap method.

---

## Diagnostic Commands Summary

| Command | Purpose |
|---------|---------|
| `chezmoi doctor` | Check for problems |
| `chezmoi verify` | Verify target matches source |
| `chezmoi status` | Show what needs updating |
| `chezmoi diff` | Show exact changes |
| `chezmoi data` | Show template data |
| `chezmoi state dump` | Dump internal state |
| `chezmoi apply -v` | Verbose apply |
| `chezmoi apply --debug` | Debug output |
| `chezmoi execute-template` | Test templates |

---

## Getting Help

1. Run `chezmoi doctor` first
2. Search [GitHub Issues](https://github.com/twpayne/chezmoi/issues)
3. Read the [FAQ](https://www.chezmoi.io/user-guide/frequently-asked-questions/)
4. Open a [support request](https://github.com/twpayne/chezmoi/issues/new?template=01_support_request.md)
