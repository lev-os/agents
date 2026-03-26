# Systemd User Timer Patterns

## Discovery

```bash
# List all user timers (active and inactive)
systemctl --user list-timers --all

# List all user services
systemctl --user list-units --type=service --all

# Find failed services (automation failures)
systemctl --user --failed

# Show a timer's schedule
systemctl --user cat <name>.timer

# Show a service's execution command
systemctl --user cat <name>.service
```

## Inspecting Existing Automation

```bash
# Check recent execution log for a service
journalctl --user -u <name>.service --since "7 days ago" --no-pager

# Check if timer is actually firing
journalctl --user -u <name>.timer --since "7 days ago" --no-pager

# Show next scheduled run
systemctl --user show <name>.timer -p NextElapseUSecRealtime

# Show accumulated run count
systemctl --user show <name>.timer -p LastTriggerUSec -p Result
```

## Gap Analysis

Look for automation opportunities by examining:

1. **Timers that fail silently** — `systemctl --user --failed`
2. **Timers with no recent runs** — check `LastTriggerUSec`
3. **Manual commands that should be timers** — cross-reference with atuin time-of-day patterns
4. **Long-running services without watchdog** — add `WatchdogSec=`

---

## Creating New Timers

### Timer Unit

```ini
# ~/.config/systemd/user/<name>.timer
[Unit]
Description=<Human-readable description>

[Timer]
# Calendar-based (cron-like)
OnCalendar=*-*-* 04:00:00      # Daily at 4am
# OR interval-based
OnUnitActiveSec=2h              # Every 2 hours after last run
# OR boot-relative
OnBootSec=10min                 # 10 min after boot

Persistent=true                 # Run missed events on boot
RandomizedDelaySec=60           # Jitter to avoid thundering herd

[Install]
WantedBy=timers.target
```

### Service Unit

```ini
# ~/.config/systemd/user/<name>.service
[Unit]
Description=<Same description>

[Service]
Type=oneshot
ExecStart=/home/ubuntu/.local/bin/<script>
# Environment variables
Environment=PATH=/home/ubuntu/.local/bin:/usr/bin:/bin
Environment=HOME=/home/ubuntu
# Resource limits
TimeoutStartSec=3600
Nice=10
# Logging
StandardOutput=journal
StandardError=journal
```

### Activation

```bash
systemctl --user daemon-reload
systemctl --user enable --now <name>.timer

# Verify
systemctl --user list-timers | grep <name>

# Test run (immediate)
systemctl --user start <name>.service
journalctl --user -u <name>.service -f
```

---

## Common Timer Patterns

| Pattern | OnCalendar | Use For |
|---------|------------|---------|
| Every 2 hours | `*-*-* 0/2:00:00` | Health checks, sync |
| Daily at 4am | `*-*-* 04:00:00` | Nightly updates, cleanup |
| Every 6 hours | `*-*-* 0/6:00:00` | Remote sync |
| Weekdays at 9am | `Mon..Fri *-*-* 09:00:00` | Work automation |
| Every 15 minutes | `*-*-* *:0/15:00` | Monitoring |
| First of month | `*-*-01 00:00:00` | Monthly reports |

---

## Monitoring

```bash
# Watch all user timer firings in real time
journalctl --user -f | grep -E 'timer|Timer'

# Summary of all timer runs in past week
for timer in $(systemctl --user list-timers --plain --no-legend | awk '{print $NF}'); do
  echo "=== $timer ==="
  journalctl --user -u "${timer%.timer}.service" --since "7 days ago" --no-pager | tail -3
  echo
done
```

---

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Timer never fires | `systemctl --user show <name>.timer` — check `NextElapseUSecRealtime` | `systemctl --user enable --now <name>.timer` |
| Service fails immediately | `journalctl --user -u <name>.service -n 20` | Check `ExecStart` path, permissions, `Environment=` |
| Timer fires but service does nothing | Check exit code: `systemctl --user show <name>.service -p Result` | Add logging to script, check `StandardOutput=journal` |
| Timer drifts | `RandomizedDelaySec` too large | Reduce or remove random delay |
| Service hangs | No `TimeoutStartSec` | Add timeout; consider `WatchdogSec` |
