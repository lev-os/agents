---
name: rch
description: >-
  Diagnose and fix RCH remote compilation. Use when Rust builds are slow,
  cargo compiling locally, rch not offloading, or worker issues.
---

# RCH Remote Compilation Helper

Offloads Rust builds to remote workers via PreToolUse hook.

## Quick Diagnosis

```bash
rch daemon status --json          # 1. Daemon running?
rch workers probe --all           # 2. Workers reachable?
echo '{"tool_name":"Bash","tool_input":{"command":"cargo build"}}' | /usr/local/bin/rch 2>&1  # 3. Hook test
```

**Success:** "Selected worker: X", "Remote compilation succeeded"

---

## The Three Killers

### 1. Socket Path Mismatch
**Symptom:** Falls back to local. **Check:** `rch config show | grep socket` vs `rch daemon status --json | grep socket`
**Fix:** `~/.config/rch/config.toml` → `socket_path = "/tmp/rch.sock"`

### 2. Output Visibility Hidden
**Symptom:** `rch status` shows nothing.
**Fix:** `~/.config/rch/config.toml` → `visibility = "normal"` (not "none")

### 3. Worker Missing Rust
**Symptom:** "rustup: not found" in hook output.
**Fix A:** `ssh -i KEY ubuntu@IP "curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly"`
**Fix B:** Comment out worker in `~/.config/rch/workers.toml`

---

## After Fixes

```bash
pkill -9 rchd; sleep 1; rch daemon start && rch workers probe --all
```

---

## Validation

Hook returns `"permissionDecision":"deny"` = SUCCESS (deny local because remote succeeded)

---

## Commands

| Command | Purpose |
|---------|---------|
| `rch workers list` | Show workers |
| `rch workers probe --all` | Test connectivity |
| `rch daemon start/stop` | Manage daemon |
| `rch config show --sources` | Config with sources |

---

## References

- [WORKERS.md](references/WORKERS.md) — Update Rust, add/remove workers
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) — Full diagnostic flowchart
- [CONFIGURATION.md](references/CONFIGURATION.md) — All config options
- [HOOKS.md](references/HOOKS.md) — PreToolUse hook setup & configuration

## Assets

- `assets/workers-template.toml` — Template for workers.toml configuration

## Script

`./scripts/diagnose-rch.sh` — Automated diagnostic
