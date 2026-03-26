# WezTerm Commands — Reference

## Table of Contents
- [Listing](#listing)
- [Pane Management](#pane-management)
- [Tab Management](#tab-management)
- [Sending Text](#sending-text)
- [Zoom](#zoom)
- [Workspaces](#workspaces)
- [Domains](#domains)
- [Launching](#launching)

---

## Listing

### List All Panes

```bash
# Plain text output
wezterm cli list

# JSON format (for scripting)
wezterm cli list --format json
```

Example JSON output:
```json
[
  {
    "window_id": 0,
    "tab_id": 0,
    "pane_id": 0,
    "workspace": "default",
    "size": { "rows": 24, "cols": 80 },
    "title": "bash",
    "cwd": "$HOME",
    "domain_name": "local"
  }
]
```

### List Clients

```bash
# List GUI windows
wezterm cli list-clients
```

### Extracting Data

```bash
# Get all pane IDs
wezterm cli list --format json | jq '.[].pane_id'

# Get pane by title
wezterm cli list --format json | jq '.[] | select(.title | contains("vim"))'

# Get panes in workspace
wezterm cli list --format json | jq '.[] | select(.workspace == "dev")'
```

---

## Pane Management

### Splitting

```bash
# Split horizontally (new pane to right)
wezterm cli split-pane --right

# Split vertically (new pane below)
wezterm cli split-pane --bottom

# Split to left/top
wezterm cli split-pane --left
wezterm cli split-pane --top

# Split with command
wezterm cli split-pane --right -- htop
wezterm cli split-pane --bottom -- tail -f /var/log/syslog

# Split in specific pane
wezterm cli split-pane --pane-id 5 --right

# Split with size percentage
wezterm cli split-pane --right --percent 30

# Split in working directory
wezterm cli split-pane --right --cwd /path/to/dir
```

### Focus Navigation

```bash
# Move focus by direction
wezterm cli activate-pane-direction up
wezterm cli activate-pane-direction down
wezterm cli activate-pane-direction left
wezterm cli activate-pane-direction right

# Activate specific pane
wezterm cli activate-pane --pane-id <id>
```

### Get Current Pane Direction

```bash
wezterm cli get-pane-direction
```

---

## Tab Management

### Creating Tabs

```bash
# New tab (default shell)
wezterm cli spawn

# New tab with command
wezterm cli spawn -- vim file.txt

# New tab in directory
wezterm cli spawn --cwd /path/to/dir

# New tab in domain
wezterm cli spawn --domain-name SSH:myserver

# New tab in specific window
wezterm cli spawn --window-id 0
```

### Switching Tabs

```bash
# Activate by index (0-based)
wezterm cli activate-tab --tab-index 0
wezterm cli activate-tab --tab-index 1

# Relative navigation
wezterm cli activate-tab --tab-relative 1   # next
wezterm cli activate-tab --tab-relative -1  # previous

# Activate tab in specific pane
wezterm cli activate-tab --tab-index 2 --pane-id 5
```

---

## Sending Text

### Basic Text Sending

```bash
# Send to specific pane
wezterm cli send-text --pane-id <id> "ls -la\n"

# Send to current pane
wezterm cli send-text "echo hello\n"

# Send without newline
wezterm cli send-text --pane-id <id> "partial command"

# Send with escape sequences
wezterm cli send-text --pane-id <id> $'\e[A'  # up arrow
```

### Command Execution Pattern

```bash
# Send command and execute
wezterm cli send-text --pane-id 0 "cd /project && npm start\n"

# Send Ctrl+C (interrupt)
wezterm cli send-text --pane-id 0 $'\x03'

# Send Ctrl+D (EOF)
wezterm cli send-text --pane-id 0 $'\x04'
```

---

## Zoom

```bash
# Toggle zoom on current pane
wezterm cli zoom-pane --toggle

# Zoom pane
wezterm cli zoom-pane --zoom

# Unzoom pane
wezterm cli zoom-pane --unzoom

# Zoom specific pane
wezterm cli zoom-pane --pane-id <id> --toggle
```

---

## Workspaces

### Listing Workspaces

```bash
# Get unique workspace names
wezterm cli list --format json | jq '.[].workspace' | sort -u
```

### Working with Workspaces

Workspaces are managed through the GUI or Lua config, not directly via CLI.

```lua
-- In wezterm.lua
wezterm.on("gui-startup", function(cmd)
  local tab, pane, window = wezterm.mux.spawn_window(cmd or {
    workspace = "default",
  })
end)
```

---

## Domains

### Listing Domains

```bash
# Get unique domain names
wezterm cli list --format json | jq '.[].domain_name' | sort -u
```

### Using SSH Domains

```bash
# Spawn in SSH domain
wezterm cli spawn --domain-name SSH:myserver

# Split in SSH domain
wezterm cli split-pane --domain-name SSH:myserver --right
```

### Mux Server

```bash
# Connect to running mux server
wezterm connect unix

# List mux connections
wezterm cli list --format json | jq '.[] | select(.domain_name != "local")'
```

---

## Launching

### Starting WezTerm

```bash
# Start new window
wezterm start

# Start with command
wezterm start -- htop

# Start in directory
wezterm start --cwd /path/to/dir

# Start maximized
wezterm start --maximized

# Start in workspace
wezterm start --workspace dev
```

### Server Mode

```bash
# Start mux server
wezterm-mux-server --daemonize

# Connect from another terminal
wezterm connect unix
```

---

## Scripting Patterns

### Create Development Layout

```bash
#!/bin/bash
# 3-pane layout: editor | terminal
#                       | logs

# Start editor
wezterm start --cwd ~/project -- nvim

# Wait for window
sleep 1

# Get pane ID
PANE=$(wezterm cli list --format json | jq '.[0].pane_id')

# Split for terminal
wezterm cli split-pane --pane-id $PANE --right --percent 40

# Get new pane
TERM_PANE=$(wezterm cli list --format json | jq '.[-1].pane_id')

# Split for logs
wezterm cli split-pane --pane-id $TERM_PANE --bottom -- tail -f app.log
```

### Send Commands to All Panes

```bash
#!/bin/bash
# Send command to all panes in current window
for pane in $(wezterm cli list --format json | jq '.[].pane_id'); do
  wezterm cli send-text --pane-id $pane "echo 'Hello from pane $pane'\n"
done
```
