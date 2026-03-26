---
name: wezterm
description: >-
  Control WezTerm terminal emulator via CLI. Use when managing panes, tabs,
  workspaces, sending commands to terminals, persistent sessions, or mux-server.
---

<!-- TOC: Quick Start | Essential Commands | THE EXACT PROMPT | Persistent Sessions | References -->

# WezTerm — Terminal Emulator CLI

> **Core Capability:** Control WezTerm panes, tabs, and multiplexer domains via CLI.

---

## Quick Start

```bash
# List all panes
wezterm cli list

# Split pane horizontally (new pane to right)
wezterm cli split-pane --right

# Split pane vertically (new pane below)
wezterm cli split-pane --bottom

# Send command to specific pane
wezterm cli send-text --pane-id <id> "ls -la\n"

# Create new tab
wezterm cli spawn
```

---

## Essential Commands

| Task | Command |
|------|---------|
| List all panes | `wezterm cli list` |
| List panes (JSON) | `wezterm cli list --format json` |
| List GUI windows | `wezterm cli list-clients` |
| Split right | `wezterm cli split-pane --right` |
| Split bottom | `wezterm cli split-pane --bottom` |
| Split with command | `wezterm cli split-pane --right -- htop` |
| Move focus | `wezterm cli activate-pane-direction <up/down/left/right>` |
| Activate pane | `wezterm cli activate-pane --pane-id <id>` |
| Create tab | `wezterm cli spawn` |
| Create tab with cmd | `wezterm cli spawn -- vim` |
| Activate tab | `wezterm cli activate-tab --tab-index <n>` |
| Next/prev tab | `wezterm cli activate-tab --tab-relative 1/-1` |
| Send text to pane | `wezterm cli send-text --pane-id <id> "text\n"` |
| Toggle zoom | `wezterm cli zoom-pane --toggle` |
| Start new window | `wezterm start` |
| Start in dir | `wezterm start --cwd /path/to/dir` |

---

## THE EXACT PROMPT — Multi-Pane Workflow

### Create Development Layout

```bash
# Start with htop on right, logs below
wezterm cli split-pane --right -- htop
wezterm cli split-pane --bottom -- tail -f /var/log/syslog

# Send command to specific pane
wezterm cli send-text --pane-id 0 "cd ~/project && npm start\n"
```

### Scripted Layout

```bash
#!/bin/bash
# Create 3-pane layout: main | htop
#                       logs |
wezterm cli split-pane --right -- htop
wezterm cli activate-pane-direction left
wezterm cli split-pane --bottom -- tail -f app.log
wezterm cli activate-pane-direction up
```

---

## Configuration

**Config file:** `~/.config/wezterm/wezterm.lua`

```bash
# Show key bindings
wezterm show-keys
```

---

## Multiplexer Domains

```bash
# List unique domains
wezterm cli list --format json | jq '.[].domain_name' | sort -u

# Spawn in SSH domain
wezterm cli spawn --domain-name SSH:myserver

# Connect to mux server
wezterm connect unix
```

---

## Persistent Remote Sessions

**The Problem:** Mac sleeps, reboots, or loses power → all terminal sessions vanish.

**The Solution:** `wezterm-mux-server` on each remote via systemd. Sessions persist on the server.

```bash
# Remote server setup (one-time)
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/wezterm-mux-server.service << 'EOF'
[Unit]
Description=WezTerm Mux Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/wezterm-mux-server --daemonize=false
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now wezterm-mux-server
sudo loginctl enable-linger $USER
```

```lua
-- Local config: SSH domain with mux
config.ssh_domains = {
  {
    name = 'dev-server',
    remote_address = '10.20.30.1',
    username = 'ubuntu',
    multiplexing = 'WezTerm',  -- Key setting
  },
}
```

See [PERSISTENT-SESSIONS.md](references/PERSISTENT-SESSIONS.md) for full setup with domain colors and smart startup.

---

## CLI Location

macOS:
```bash
/Applications/WezTerm.app/Contents/MacOS/wezterm
```

Or add to PATH for easier access.

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Persistent remote sessions | [PERSISTENT-SESSIONS.md](references/PERSISTENT-SESSIONS.md) |
