---
name: caffeine
description: Prevents macOS sleep using caffeinate/pmset and Caffeine.app.
---

# Caffeine Skill

Prevent Mac from sleeping via CLI or GUI.

## Quick Reference

### CLI Commands (built-in `caffeinate`)

```bash
# Prevent idle sleep (until killed)
caffeinate -i &

# Prevent system sleep on AC power
caffeinate -s &

# Prevent display sleep too
caffeinate -d &

# All assertions (system + display + disk + idle)
caffeinate -dims &

# Run for specific duration (seconds)
caffeinate -t 3600  # 1 hour

# Keep awake while a process runs
caffeinate -w <pid>

# Kill caffeinate
pkill caffeinate
```

### Check Status

```bash
# See what's preventing sleep
pmset -g assertions

# Current power settings
pmset -g

# Is caffeinate running?
pgrep -l caffeinate
```

### GUI App

**Caffeine.app** installed at `/Applications/Caffeine.app`
- Click coffee cup in menubar to toggle
- Filled cup = active (preventing sleep)
- Empty cup = inactive

### Permanent Settings (requires sudo)

```bash
# Never sleep system (AC power)
sudo pmset -c sleep 0

# Never sleep display
sudo pmset -c displaysleep 0

# Restore defaults
sudo pmset -c sleep 10
sudo pmset -c displaysleep 10
```

## Usage Examples

**Keep awake indefinitely for voice server:**
```bash
caffeinate -dims &
```

**Keep awake for 8 hours:**
```bash
caffeinate -dims -t 28800 &
```

**Check if already caffeinated:**
```bash
pgrep caffeinate && echo "Caffeinated ☕" || echo "Not caffeinated 😴"
```

## Notes

- `caffeinate` and Caffeine.app work independently
- System already configured with `sleep 0` (never sleeps)
- Display sleep was 180min, now set to 0 (never)
- For voice/server use: system sleep prevention is most important
