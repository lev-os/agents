# Service Management Patterns

For installers that need to run background daemons. Patterns from RCH installer.

---

## When You Need This

If your tool includes a daemon/service component (build worker, proxy, watcher), you need:
- systemd user service (Linux)
- launchd plist (macOS)
- Service lifecycle management (install, start, restart, uninstall)

---

## systemd User Service (Linux)

```bash
install_systemd_service() {
  local service_name="$1"
  local binary_path="$2"
  local config_dir="$3"

  local unit_dir="$HOME/.config/systemd/user"
  local unit_file="$unit_dir/${service_name}.service"

  mkdir -p "$unit_dir"
  mkdir -p "$config_dir/logs"

  cat > "$unit_file" << EOF
[Unit]
Description=${service_name} daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=${binary_path} --foreground --config ${config_dir}/daemon.toml
Restart=always
RestartSec=5
Environment=RUST_LOG=info

[Install]
WantedBy=default.target
EOF

  # Enable lingering (service persists after logout)
  if command -v loginctl >/dev/null 2>&1; then
    loginctl enable-linger "$(whoami)" 2>/dev/null || true
  fi

  # Reload, enable, start
  systemctl --user daemon-reload
  systemctl --user enable "$service_name" 2>/dev/null || true

  # Start may fail on fresh install (missing config) — that's OK
  if systemctl --user start "$service_name" 2>/dev/null; then
    ok "Service $service_name started"
  else
    warn "Service enabled but not started (configure first, then: systemctl --user start $service_name)"
  fi
}
```

### Key Details

- **`loginctl enable-linger`** — Without this, user services die on logout
- **`After=network.target network-online.target`** — Ensures network is up for remote connections
- **`Restart=always` + `RestartSec=5`** — Auto-restart on crash with 5s backoff
- **Separate enable from start** — Enable survives reboot; start may fail on fresh install

---

## macOS launchd Plist

```bash
install_launchd_service() {
  local service_label="$1"   # e.g., "com.project.daemon"
  local binary_path="$2"
  local config_dir="$3"

  local plist_dir="$HOME/Library/LaunchAgents"
  local plist_file="$plist_dir/${service_label}.plist"

  mkdir -p "$plist_dir"
  mkdir -p "$config_dir/logs"

  # Unload existing service BEFORE writing new plist
  if launchctl list "$service_label" >/dev/null 2>&1; then
    launchctl unload "$plist_file" 2>/dev/null || true
  fi

  cat > "$plist_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${service_label}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${binary_path}</string>
        <string>--foreground</string>
        <string>--config</string>
        <string>${config_dir}/daemon.toml</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${config_dir}/logs/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>${config_dir}/logs/daemon.err</string>
</dict>
</plist>
EOF

  if launchctl load "$plist_file" 2>/dev/null; then
    ok "Service $service_label loaded"
  else
    warn "Failed to load service (configure first, then: launchctl load $plist_file)"
  fi
}
```

### Key Details

- **Unload before load** — Prevents conflicts when upgrading
- **`KeepAlive` + `RunAtLoad`** — macOS equivalent of systemd `Restart=always`
- **Explicit log paths** — launchd has no journalctl, must specify stdout/stderr files
- **`ProgramArguments` as array** — Each arg is a separate `<string>` element

---

## Cross-Platform Service Installation

```bash
install_service() {
  local service_name="$1"
  local service_label="$2"
  local binary_path="$3"
  local config_dir="$4"

  case "$OS" in
    linux)
      if command -v systemctl >/dev/null 2>&1; then
        install_systemd_service "$service_name" "$binary_path" "$config_dir"
      else
        warn "systemd not found; service auto-start not configured"
        warn "Run manually: $binary_path --foreground"
      fi
      ;;
    darwin)
      install_launchd_service "$service_label" "$binary_path" "$config_dir"
      ;;
  esac
}
```

---

## Daemon Restart with 3-Tier Fallback

```bash
restart_daemon() {
  local binary_path="$1"
  local service_name="$2"
  local service_label="$3"

  # Tier 1: Binary's own restart subcommand
  if "$binary_path" daemon restart 2>/dev/null; then
    ok "Daemon restarted via CLI"
    return 0
  fi

  warn "CLI restart failed; trying service manager..."

  # Tier 2: systemctl (Linux)
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl --user restart "$service_name" 2>/dev/null; then
      ok "Daemon restarted via systemctl"
      return 0
    fi
  fi

  # Tier 3: launchctl (macOS)
  if command -v launchctl >/dev/null 2>&1; then
    local plist="$HOME/Library/LaunchAgents/${service_label}.plist"
    if [ -f "$plist" ]; then
      launchctl unload "$plist" 2>/dev/null || true
      if launchctl load "$plist" 2>/dev/null; then
        ok "Daemon restarted via launchctl"
        return 0
      fi
    fi
  fi

  warn "Could not restart daemon automatically"
  warn "Run manually: $binary_path daemon restart"
}
```

---

## Service Opt-In Cascade

For interactive installs, ask before installing system services:

```bash
should_install_service() {
  if [ "$EASY" -eq 1 ]; then
    return 0  # Easy mode: always yes
  fi

  if ! [ -t 0 ]; then
    return 0  # Non-interactive (curl|bash): default yes
  fi

  # Interactive: ask
  if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ]; then
    gum confirm "Install as system service (auto-start on login)?"
  else
    echo -n "Install as system service? (Y/n): "
    read -r ans
    case "$ans" in
      n|N|no|No|NO) return 1 ;;
      *) return 0 ;;
    esac
  fi
}
```

---

## Uninstall Service

```bash
uninstall_service() {
  # systemd
  if command -v systemctl >/dev/null 2>&1; then
    systemctl --user stop "$SERVICE_NAME" 2>/dev/null || true
    systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
    systemctl --user daemon-reload
  fi

  # launchd
  local plist="$HOME/Library/LaunchAgents/${SERVICE_LABEL}.plist"
  if [ -f "$plist" ]; then
    launchctl unload "$plist" 2>/dev/null || true
    rm -f "$plist"
  fi

  # Socket cleanup (if applicable)
  rm -f "$SOCKET_PATH" 2>/dev/null || true
}
```

**Always preserve config files** during uninstall — users may reinstall later.
