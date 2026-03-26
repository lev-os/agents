---
name: path-rationalization
description: >-
  Audit and clean shell PATH pollution in .bashrc, .zshrc, .zshenv, .profile.
  Use when PATH has junk, wrong binary resolves, temp dirs in PATH, or duplicates.
---

# PATH Rationalization

<!-- TOC: Quick Router | Safety | Workflow (Steps 1-8) | Rollback | Validation | References -->

## Quick Router

| Symptom | Action |
|---------|--------|
| `which foo` returns `/tmp/...` or `/run/...` | Junk PATH entry — audit + remove |
| Binary just installed but old version runs | Shadowed by stale copy — find all with `type -a foo` |
| PATH has 40+ entries | Accumulated cruft — full audit needed |
| New shell starts slow | Excess PATH entries — rationalize |

## Safety Protocol (NON-NEGOTIABLE)

```
1. BACKUP every file before editing
2. VERIFY the backup exists and matches
3. EDIT the file
4. TEST in subshell (zsh -l -c 'echo $PATH | tr : \\n')
5. Only THEN tell user to source or open new shell
6. If anything breaks: restore from backup immediately
```

**Never leave the user's shell broken.** A bad `.zshrc` edit can lock someone out of their machine.

## Workflow

- [ ] **Step 1: Inventory** — Dump current PATH, find all shell config files
- [ ] **Step 2: Backup** — Copy each file to `~/.path-rationalization-backup/`
- [ ] **Step 3: Classify** — Separate legitimate vs junk PATH entries
- [ ] **Step 4: Edit** — Remove junk, deduplicate, fix ordering
- [ ] **Step 5: Verify binary resolution** — `type -a <binary>` for key tools
- [ ] **Step 6: Test** — Subshell test before sourcing
- [ ] **Step 7: Install binaries** — Copy to canonical location
- [ ] **Step 8: Confirm** — User sources config, runs `which <binary>`

## Step 1: Inventory

```bash
# Full numbered PATH dump
echo $PATH | tr ':' '\n' | cat -n

# All shell config files that modify PATH
grep -rn "PATH" ~/.zshrc ~/.zshenv ~/.zprofile ~/.profile ~/.bashrc ~/.bash_profile 2>/dev/null | grep -v "^#"

# Count PATH modifications per file
grep -c "PATH" ~/.zshrc ~/.zshenv ~/.zprofile ~/.profile ~/.bashrc ~/.bash_profile 2>/dev/null

# Find all copies of a specific binary
type -a ntm  # or whatever binary
```

## Step 2: Backup

```bash
mkdir -p ~/.path-rationalization-backup
for f in ~/.zshrc ~/.zshenv ~/.zprofile ~/.profile ~/.bashrc ~/.bash_profile; do
  [ -f "$f" ] && cp "$f" ~/.path-rationalization-backup/
done
ls -la ~/.path-rationalization-backup/
```

**Verify backups exist before proceeding.** Read back a backup file to confirm content matches.

## Step 3: Classify PATH Entries

### Junk (remove immediately)

| Pattern | Source | Why Junk |
|---------|--------|----------|
| `/tmp/.tmp*`, `/data/tmp/.tmp*` | Installer tests | Ephemeral temp dirs |
| `/tmp/*-test*`, `/tmp/*-install*` | Test scaffolding | Never cleaned up |
| `/run/user/*/fnm_multishells/*/bin` | fnm shell isolation | Session-ephemeral, not persistent |
| Duplicate entries | Appended on every shell start | Accumulate over time |

### Legitimate (keep, but deduplicate)

| Path | Purpose |
|------|---------|
| `~/.local/bin` | User binaries (canonical install location) |
| `~/.cargo/bin` | Rust toolchain |
| `~/go/bin` | Go binaries |
| `~/.bun/bin` | Bun runtime |
| `~/.nvm/versions/node/*/bin` | Node.js via nvm |
| `~/.atuin/bin` | Atuin shell history |
| `/usr/local/bin`, `/usr/bin`, `/bin` | System paths |
| `/snap/bin` | Snap packages |
| `$FNM_MULTISHELL_PATH/bin` | fnm Node.js (dynamic, OK in zshrc) |

### Requires Judgment (ask user)

- `~/mcp_agent_mail` — Is this still needed in PATH?
- Custom project dirs — Check if binary is actually there
- Vault/cloud SDK paths — May be needed for specific workflows

**When in doubt, ASK the user.** Don't remove paths you aren't sure about.

## Step 4: Edit

### File Roles (Know Which File Does What)

| File | Shell | When Loaded | Use For |
|------|-------|-------------|---------|
| `~/.zshenv` | zsh | Every zsh invocation (interactive + non-interactive) | PATH for tools that scripts need |
| `~/.zshrc` | zsh | Interactive shells only | Aliases, completions, prompts, interactive PATH |
| `~/.zprofile` | zsh | Login shells only | Login-time setup (rare) |
| `~/.profile` | bash/sh | Login shells | PATH for bash login sessions |
| `~/.bashrc` | bash | Interactive non-login | Bash aliases, functions, interactive PATH |
| `~/.bash_profile` | bash | Login shells | Bash login setup |

### Ordering Principle

PATH entries are searched left-to-right. Order should be:

```
1. User-managed (highest priority): ~/.local/bin, ~/.cargo/bin, ~/go/bin
2. Language managers (dynamic): fnm, nvm, bun
3. System: /usr/local/bin, /usr/bin, /bin, /sbin
4. Optional: /snap/bin, google-cloud-sdk
```

### Deduplication Pattern (idempotent)

```bash
# GOOD: won't duplicate on re-source
case ":$PATH:" in
  *:"$HOME/.local/bin":*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

# BAD: duplicates every time shell config is sourced
export PATH="$HOME/.local/bin:$PATH"
```

### Anti-Patterns to Remove

```bash
# REMOVE: bare prepend without guard (duplicates on every source)
export PATH="/some/path:$PATH"

# REMOVE: temp directory paths
export PATH="/tmp/.tmpXYZ123:$PATH"
export PATH="/data/tmp/.tmpABC456:$PATH"

# REMOVE: test installer leftovers
export PATH="/tmp/jsm-test-install:$PATH"
export PATH="/tmp/am-install-test:$PATH"
```

## Step 5: Verify Binary Resolution

After editing, verify key binaries resolve correctly:

```bash
# In a subshell (doesn't affect current session)
zsh -l -c 'type -a ntm; type -a node; type -a cargo; type -a bun'

# Check the new PATH is clean
zsh -l -c 'echo $PATH | tr : \\n | cat -n'

# Verify no duplicates
zsh -l -c 'echo $PATH | tr : \\n | sort | uniq -d'

# Verify binary actually exists and works at resolved path
zsh -l -c 'which ntm && ntm version'
```

## Step 6: Test Before Sourcing

```bash
# Test zsh config in subshell
zsh -l -c 'echo "PATH entries:"; echo $PATH | tr : \\n | wc -l'

# Test bash config in subshell
bash -l -c 'echo "PATH entries:"; echo $PATH | tr : \\n | wc -l'
```

**Only proceed if subshell tests pass.** If they fail, restore from backup.

## Step 7: Install Binaries to Canonical Location

When a binary needs to be accessible, install to `~/.local/bin`:

```bash
# Build and install
go build -trimpath -ldflags "-s -w" -o ~/.local/bin/ntm ./cmd/ntm

# Verify
ls -la ~/.local/bin/ntm
~/.local/bin/ntm version
```

**Remove stale copies** from junk locations after installing to canonical path.

## Step 8: Confirm

Tell the user to reload their shell:

```bash
source ~/.zshrc   # or open a new terminal
which ntm         # should show ~/.local/bin/ntm
echo $PATH | tr ':' '\n' | wc -l   # should be ~15-20, not 40+
```

## Rollback

If anything goes wrong:

```bash
cp ~/.path-rationalization-backup/.zshrc ~/.zshrc
cp ~/.path-rationalization-backup/.bashrc ~/.bashrc
cp ~/.path-rationalization-backup/.zshenv ~/.zshenv
cp ~/.path-rationalization-backup/.profile ~/.profile
source ~/.zshrc
```

## Validation

```bash
# No temp dirs in PATH
echo $PATH | tr ':' '\n' | grep -E "^/tmp/|^/data/tmp/|^/run/user" | wc -l  # should be 0

# No duplicates
echo $PATH | tr ':' '\n' | sort | uniq -d | wc -l  # should be 0

# Reasonable entry count
echo $PATH | tr ':' '\n' | wc -l  # should be <25

# Key binaries resolve from canonical locations
which ntm   # ~/.local/bin/ntm
which cargo # ~/.cargo/bin/cargo
which node  # via fnm or nvm, not /tmp/
```

## Reference Index

| Topic | File |
|-------|------|
| Common junk patterns | [JUNK_PATTERNS.md](references/JUNK_PATTERNS.md) |
| Shell config file loading order | [SHELL_LOADING_ORDER.md](references/SHELL_LOADING_ORDER.md) |
| Real-world cleanup session | [SESSION_LOG.md](references/SESSION_LOG.md) |
