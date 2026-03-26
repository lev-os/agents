# RCH Configuration Reference

## Config Locations

| Priority | Location | Purpose |
|----------|----------|---------|
| 1 | Environment variables (`RCH_*`) | Runtime overrides |
| 2 | `.rch/config.toml` | Project-specific |
| 3 | `~/.config/rch/config.toml` | User defaults |
| 4 | Built-in defaults | Fallback |

Workers always at: `~/.config/rch/workers.toml`

---

## Main Config (~/.config/rch/config.toml)

```toml
[general]
enabled = true
log_level = "info"                    # trace, debug, info, warn, error
socket_path = "/tmp/rch.sock"         # MUST match daemon

[compilation]
confidence_threshold = 0.85           # Min confidence to intercept (0.0-1.0)
min_local_time_ms = 2000              # Don't offload trivial builds

[transfer]
compression_level = 3                 # zstd level 1-22
exclude_patterns = [
    "target/",
    "*.rlib",
    ".git/objects/",
    "node_modules/",
]

[circuit]
failure_threshold = 3                 # Failures before circuit opens
success_threshold = 2                 # Successes to close circuit
error_rate_threshold = 0.5
window_secs = 60
open_cooldown_secs = 30

[output]
visibility = "normal"                 # none, minimal, normal, verbose
first_run_complete = true
```

---

## Workers Config (~/.config/rch/workers.toml)

```toml
[[workers]]
id = "worker-name"                    # Unique identifier
host = "192.168.1.100"                # IP or hostname
user = "ubuntu"                       # SSH user
identity_file = "~/.ssh/key.pem"      # SSH private key
total_slots = 48                      # Concurrent job capacity
priority = 100                        # Higher = preferred
tags = ["fast", "local"]              # Optional categorization
```

### Slot Guidelines

| Worker CPUs | Recommended Slots |
|-------------|-------------------|
| 4 cores | 8 |
| 8 cores | 16 |
| 16 cores | 32 |
| 32+ cores | 48-64 |

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `RCH_LOG_LEVEL` | Override log level | `debug` |
| `RCH_DAEMON_SOCKET` | Override socket path | `/tmp/rch.sock` |
| `RCH_SSH_KEY` | Default SSH key | `~/.ssh/id_rsa` |
| `RCH_TRANSFER_ZSTD_LEVEL` | Compression | `3` |
| `RCH_ENABLE_METRICS` | Telemetry | `true` |

---

## Claude Code Hook Settings

Location: `~/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/local/bin/rch"
          }
        ]
      }
    ]
  }
}
```

Install automatically:
```bash
rch hook install
```

---

## Data Locations

| Path | Contents |
|------|----------|
| `~/.local/share/rch/telemetry/` | Usage metrics DB |
| `~/.local/share/rch/fleet_history/` | Worker history |
| `/tmp/rch.sock` | Daemon socket (default) |
| `/tmp/rch/` | Temp files during transfer |
