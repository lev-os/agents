# Junk PATH Patterns — Recognition Guide

## Installer Test Leftovers

These appear when installers are tested and don't clean up:

```
/tmp/jsm-test-install
/tmp/jsm-test-install2
/tmp/jsm-test-install3
/tmp/jsm-test-install4
/tmp/am-install-test
/tmp/am-install-test2
/tmp/am-install-test3
/tmp/install-test
/tmp/ntm-install-test3
/tmp/cm-test
```

**Source:** Installer scripts that append `export PATH="/tmp/...:$PATH"` to shell configs during testing and never remove them.

**Fix:** Remove the `export PATH=...` lines from all shell config files.

## Temp Directory Accumulation

Agents or build tools creating temp dirs and adding them to PATH:

```
/tmp/.tmpnT9aTU
/tmp/.tmpmH1U3S
/data/tmp/.tmpK4V5FV
/data/tmp/.tmpmTJ7iR
/data/tmp/.tmpbwPhCy
```

**Signature:** Random 6-8 char suffix after `.tmp`. May be 50-100+ entries.

**Source:** Build/test processes that create temp dirs with `mktemp -d` patterns and persist PATH entries to shell configs. Often written by AI agents that don't clean up after themselves.

**Fix:** Remove ALL lines matching `export PATH=".*\.tmp.*:$PATH"` from shell configs. Never add temp dirs to persistent shell configs — use them only in the current session.

## fnm Multishell Ephemeral Paths

```
/run/user/1000/fnm_multishells/1918156_1774109763499/bin
/run/user/1000/fnm_multishells/1918149_1774109763340/bin
```

**What they are:** fnm (Fast Node Manager) creates per-shell-session directories in `/run/user/`. These are session-ephemeral — they exist only while that specific shell process is alive.

**Why they're in PATH:** fnm's `eval "$(fnm env --use-on-cd)"` adds the current multishell path. If an agent naively snapshots `$PATH` and writes it to a config file, these ephemeral paths get persisted.

**Fix:** Never persist these. Use the dynamic pattern instead:

```bash
if [ -n "${FNM_MULTISHELL_PATH:-}" ] && [ -d "$FNM_MULTISHELL_PATH/bin" ]; then
    export PATH="$FNM_MULTISHELL_PATH/bin:$PATH"
fi
```

## Data Tmp Build Artifacts

```
/data/tmp/tmp.U3XTyE8BaT
/data/tmp/.tmpWErbS0
```

**Source:** Build processes using `/data/tmp` as TMPDIR. Same as temp directory accumulation but in a non-standard temp location.

## Stale Binary Copies

When a binary exists at multiple PATH locations:

```
ntm is /run/user/1000/fnm_multishells/.../bin/ntm    # BAD: ephemeral
ntm is /home/ubuntu/.bun/bin/ntm                      # BAD: wrong tool's dir
ntm is /home/ubuntu/.local/bin/ntm                    # GOOD: canonical
ntm is /home/ubuntu/go/bin/ntm                        # OK: go install location
ntm is /usr/local/bin/ntm                             # OK: system-wide
```

**Fix:** Install to ONE canonical location (`~/.local/bin` for user tools) and remove copies from other locations. Then clean PATH so only the canonical location appears early.

## Detection Commands

```bash
# Find all temp-dir PATH entries
echo $PATH | tr ':' '\n' | grep -E "^/tmp/|^/data/tmp/|^/run/user"

# Find all duplicate PATH entries
echo $PATH | tr ':' '\n' | sort | uniq -d

# Count total entries (healthy is 10-20)
echo $PATH | tr ':' '\n' | wc -l

# Find PATH lines in all shell configs
grep -rn 'export PATH=' ~/.zshrc ~/.zshenv ~/.profile ~/.bashrc 2>/dev/null | wc -l
```
