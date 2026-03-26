# WezTerm Persistent Remote Sessions — Reference

## Table of Contents
- [Why Mux-Server](#why-mux-server)
- [Architecture](#architecture)
- [Remote Server Setup](#remote-server-setup)
- [Local Configuration](#local-configuration)
- [Domain Colors](#domain-colors)
- [Smart Startup](#smart-startup)
- [Keybindings](#keybindings)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

---

## Why Mux-Server

**Problem:** Mac sleeps, reboots, or loses power → all terminal sessions vanish.

**Solution:** `wezterm-mux-server` on each remote via systemd. Sessions persist on the server; your Mac just reconnects.

| Feature | tmux | WezTerm Mux |
|:--------|:-----|:------------|
| Scrollback | Nested (confusing) | Native terminal |
| Keybindings | Prefix conflicts | Single namespace |
| GPU rendering | Text only | Full acceleration |
| Mouse | Needs config | Native |
| Theming | Limited | Full colors, gradients |

---

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    YOUR MAC (WezTerm GUI)                      │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Local    │  │ Dev      │  │ Staging  │  │ Workstation│     │
│  │ (fresh)  │  │ (purple) │  │ (amber)  │  │ (crimson)  │     │
│  └──────────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘     │
│        │            │             │              │             │
│   fresh each     SSH+Mux      SSH+Mux        SSH+Mux          │
│    startup     (persistent)  (persistent)  (persistent)       │
└────────┼────────────┼─────────────┼──────────────┼────────────┘
         │            ▼             ▼              ▼
         │   ┌─────────────────────────────────────────┐
         │   │          REMOTE SERVERS                  │
         │   │  wezterm-mux-server (systemd, linger)   │
         │   │  Sessions survive Mac sleep/reboot      │
         │   └─────────────────────────────────────────┘
```

---

## Remote Server Setup

### Step 1: Install WezTerm

```bash
# Ubuntu/Debian
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
sudo apt update && sudo apt install wezterm

# Verify version matches local
wezterm --version
```

### Step 2: Create Systemd Service

```bash
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
Environment=WEZTERM_LOG=warn

[Install]
WantedBy=default.target
EOF
```

### Step 3: Enable Service

```bash
systemctl --user daemon-reload
systemctl --user enable --now wezterm-mux-server
sudo loginctl enable-linger $USER
```

### Step 4: Verify

```bash
systemctl --user status wezterm-mux-server
# Should show "active (running)"
```

---

## Local Configuration

### SSH Domains

```lua
config.ssh_domains = {
  {
    name = 'dev-server',
    remote_address = '10.20.30.1',
    username = 'ubuntu',
    multiplexing = 'WezTerm',
    assume_shell = 'Posix',
  },
  {
    name = 'staging',
    remote_address = '10.20.30.2',
    username = 'ubuntu',
    multiplexing = 'WezTerm',
    assume_shell = 'Posix',
  },
}
```

---

## Domain Colors

Apply different background colors per domain for visual context:

```lua
local domain_colors = {
  ['dev-server'] = {
    background = {{
      source = { Gradient = {
        colors = { '#1a0d1a', '#2e1a2e', '#3e163e' },
        orientation = { Linear = { angle = -45.0 } },
      }},
      width = '100%', height = '100%', opacity = 0.92,
    }},
    colors = {
      cursor_bg = '#bb9af7',
      tab_bar = {
        active_tab = { bg_color = '#bb9af7', fg_color = '#1a0d1a' },
      },
    },
  },
}

wezterm.on('update-status', function(window, pane)
  local domain = pane:get_domain_name()
  local overrides = window:get_config_overrides() or {}
  if domain_colors[domain] then
    overrides.background = domain_colors[domain].background
    overrides.colors = domain_colors[domain].colors
  else
    overrides.background = nil
    overrides.colors = nil
  end
  window:set_config_overrides(overrides)
end)
```

---

## Smart Startup

Create windows without tab accumulation on restart:

```lua
local remote_domains = {
  { name = 'dev-server',  cwd = '/data/projects' },
  { name = 'staging',     cwd = '/var/www' },
}

wezterm.on('gui-startup', function(cmd)
  -- Local window
  local _, _, local_window = wezterm.mux.spawn_window {
    cwd = wezterm.home_dir .. '/projects',
  }
  for i = 2, 3 do
    local_window:spawn_tab { cwd = wezterm.home_dir .. '/projects' }
  end

  -- Remote windows
  for _, remote in ipairs(remote_domains) do
    local ok, err = pcall(function()
      local _, _, window = wezterm.mux.spawn_window {
        domain = { DomainName = remote.name },
        cwd = remote.cwd,
      }
      -- Only create tabs if mux-server is fresh
      if #window:tabs() <= 1 then
        for i = 2, 3 do
          window:spawn_tab { cwd = remote.cwd }
        end
      end
    end)
  end
end)
```

---

## Keybindings

```lua
config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }

config.keys = {
  -- Quick tab in domain
  { key = '1', mods = 'LEADER', action = wezterm.action.SpawnCommandInNewTab {
    domain = { DomainName = 'dev-server' }, cwd = '/data/projects' }},
  { key = '2', mods = 'LEADER', action = wezterm.action.SpawnCommandInNewTab {
    domain = { DomainName = 'staging' }, cwd = '/var/www' }},

  -- Tab switching
  { key = 'LeftArrow', mods = 'SHIFT|CTRL', action = wezterm.action.ActivateTabRelative(-1) },
  { key = 'RightArrow', mods = 'SHIFT|CTRL', action = wezterm.action.ActivateTabRelative(1) },

  -- Domain launcher
  { key = 'w', mods = 'LEADER', action = wezterm.action.ShowLauncherArgs { flags = 'DOMAINS' } },
}
```

---

## Maintenance

```bash
# Check status
ssh host 'systemctl --user status wezterm-mux-server'

# View logs
ssh host 'journalctl --user -u wezterm-mux-server --since "1 hour ago"'

# Restart (clears all tabs)
ssh host 'systemctl --user restart wezterm-mux-server'

# Version check (must match local)
ssh host 'wezterm --version'
```

---

## Troubleshooting

| Symptom | Fix |
|:--------|:----|
| Connection failed | Check SSH; verify systemd service active |
| Wrong tab count | Restart mux-server |
| Mux-server dies on disconnect | `sudo loginctl enable-linger $USER` |
| Version mismatch errors | Update WezTerm on both ends |
| Colors not applying | Check `pane:get_domain_name()` value |

Debug: `Ctrl+Shift+L` opens debug overlay.

---

## Adding New Domain

1. Add to `config.ssh_domains`
2. Add to `remote_domains` for startup
3. Add color scheme to `domain_colors`
4. Set up mux-server on remote
