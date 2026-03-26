# Real-World PATH Cleanup Session (2026-03-21)

## Before State

Machine: Ubuntu dev server, heavy multi-agent AI coding use.

**PATH entry count:** 43 entries

**Shell config PATH line counts:**
- `~/.bashrc`: 140 PATH-related lines
- `~/.zshrc`: 20 PATH lines
- `~/.zshenv`: 21 PATH lines
- `~/.profile`: 16 PATH lines

**Junk categories found:**

| Category | Count | Example |
|----------|-------|---------|
| `/tmp/.tmp*` installer leftovers | ~40 in bashrc | `/tmp/.tmpnT9aTU` |
| `/data/tmp/.tmp*` build artifacts | ~65 in bashrc | `/data/tmp/.tmpK4V5FV` |
| `/tmp/jsm-test-install*` | 4 in zshrc | `/tmp/jsm-test-install3` |
| `/tmp/am-install-test*` | 3 in zshrc + 3 in zshenv + 3 in profile + 3 in bashrc | `/tmp/am-install-test2` |
| `/tmp/install-test` | 1 in zshrc | |
| `/tmp/cm-test` | 1 in bashrc | |
| `/tmp/ntm-install-test3` | 1 in zshrc + 1 in bashrc | |
| fnm multishell hardcoded | 2 in PATH | `/run/user/1000/fnm_multishells/...` |
| Duplicate `~/.local/bin` | 3+ times across files | |
| Duplicate `mcp_agent_mail` | 2+ times across files | |

**Binary resolution problem:**
```
$ which ntm
/run/user/1000/fnm_multishells/1918156_1774109763499/bin/ntm  # OLD binary from March 20

$ ls -la /home/ubuntu/.local/bin/ntm  # NEW binary from March 21
# This one was shadowed and never ran
```

## Root Cause

AI coding agents (Claude Code, Codex) writing installer scripts that append `export PATH="...:$PATH"` to shell configs during testing. Each test run adds a new line. Over weeks/months, hundreds of entries accumulate.

The fnm multishell paths appeared because an agent naively persisted `$FNM_MULTISHELL_PATH/bin` as a literal path instead of using the dynamic variable.

## Fix Applied

1. **Backed up** all four config files
2. **Rewrote** each file preserving only legitimate entries
3. **Removed** all temp/test PATH entries (~120 lines from bashrc alone)
4. **Deduplicated** remaining entries with `case ":$PATH:"` guards
5. **Installed** ntm binary to `~/.local/bin/ntm` (canonical location)
6. **Copied** new binary to all stale locations so current session works
7. **Verified** `type -a ntm` resolves correctly

## After State

**PATH entry count:** ~18 (down from 43)
**Shell config PATH lines:** ~5 per file (down from 140 in bashrc)

## Lessons Learned

1. **Never persist temp paths to shell configs.** Use them only in the current session via `export PATH="/tmp/foo:$PATH"` at the command line, not in rc files.
2. **Always use dedup guards** when adding to shell configs programmatically.
3. **Install binaries to ONE canonical location** (`~/.local/bin`) and verify with `which`.
4. **`type -a binary`** shows ALL resolution candidates — essential for debugging shadowing.
5. **Test in subshell first** (`zsh -l -c 'which ntm'`) before telling user to source.
6. **AI agents MUST clean up** test PATH entries they add. This should be enforced in AGENTS.md.
