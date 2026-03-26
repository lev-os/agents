# RCH Troubleshooting

## Diagnostic Flowchart

```
Builds running locally?
│
├─ Is daemon running?
│  $ rch daemon status --json
│  │
│  ├─ No → $ rch daemon start
│  │
│  └─ Yes → Is socket path correct?
│           $ rch config show --sources | grep socket
│           $ rch daemon status --json | grep socket
│           │
│           ├─ Mismatch → Fix ~/.config/rch/config.toml
│           │
│           └─ Match → Are workers reachable?
│                      $ rch workers probe --all
│                      │
│                      ├─ Failures → Check SSH keys, network
│                      │
│                      └─ All OK → Test hook directly
│                                  $ echo '{"tool_name":"Bash",...}' | /usr/local/bin/rch
│                                  │
│                                  ├─ "rustup: not found" → Worker missing Rust
│                                  │
│                                  ├─ "falling back to local" → Check full error
│                                  │
│                                  └─ "Remote compilation succeeded" → Hook works!
│                                     Check if hook is installed in Claude Code
```

---

## Common Errors

### "Could not send shutdown command"

**Cause:** Socket path mismatch between config and running daemon.

```bash
# Find actual socket
ls -la /tmp/rch*.sock /run/user/*/rch*.sock 2>/dev/null

# Update config to match
vim ~/.config/rch/config.toml
```

### "rustup: not found" / "cargo: not found"

**Cause:** Selected worker doesn't have Rust installed.

```bash
# Find which worker was selected (in hook output)
# "Selected worker: fmd at ubuntu@51.222.245.56"

# Install Rust on that worker
ssh -i KEY ubuntu@IP "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly"
```

### "falling back to local"

**Cause:** Remote execution failed for some reason.

Check the WARN line above it for details:
- Network timeout → Worker unreachable
- Command not found → Missing toolchain
- Exit code non-zero → Build failed remotely (artifacts not synced back)

### Hook not intercepting at all

**Cause:** Hook not installed in Claude Code settings.

```bash
# Check settings
cat ~/.claude/settings.json | grep -A10 PreToolUse
```

Should show:
```json
"PreToolUse": [{
  "matcher": "Bash",
  "hooks": [{"type": "command", "command": "/usr/local/bin/rch"}]
}]
```

If missing:
```bash
rch hook install
```

### Status commands show no output

**Cause:** Output visibility set to "none".

```bash
# Check
grep visibility ~/.config/rch/config.toml

# Fix
sed -i 's/visibility = "none"/visibility = "normal"/' ~/.config/rch/config.toml
```

---

## Debug Mode

Get maximum verbosity:

```bash
RCH_LOG_LEVEL=debug cargo build 2>&1 | head -100
```

Or test hook directly with debug:

```bash
RCH_LOG_LEVEL=debug echo '{"tool_name":"Bash","tool_input":{"command":"cargo check"}}' | /usr/local/bin/rch 2>&1
```

---

## Nuclear Option: Full Reset

```bash
# Stop everything
pkill -9 rchd
rm -f /tmp/rch*.sock /run/user/*/rch*.sock

# Verify config
cat ~/.config/rch/config.toml
cat ~/.config/rch/workers.toml

# Fresh start
rch daemon start
rch workers probe --all
rch hook test
```
