# Real-World Automation Examples

## Scoring Summary

| Pattern | Freq/wk | Time Saved | Error Rate | Score | Type |
|---------|---------|------------|------------|-------|------|
| Log monitoring loop | 20 | 30 min/wk | High | 0.85 | Systemd |
| Retry wrapper (flaky curl) | 12 | 10 min/wk | High | 0.78 | Bash |
| Git add+commit+push | 40 | 5 min/wk | Low | 0.72 | Bash |
| Multi-repo status check | 10 | 8 min/wk | Low | 0.55 | Bash |
| DB backup before migration | 8 | 4 min/wk | Medium | 0.51 | Rust CLI |
| Project cd+build+test | 15 | 3 min/wk | Low | 0.45 | Alias |
| Morning triage ritual | 5 | 5 min/wk | Low | 0.38 | Timer |

Log monitoring scored highest: eliminated a high-error-rate manual loop entirely.

---

## High Score: Log Monitoring → Systemd Watchdog (0.85)

**Pattern:** `journalctl --user -u rchd.service -f` 20x/week, followed by `systemctl --user restart rchd`

**Fix:** Added watchdog + auto-restart to the service itself:
```ini
[Service]
Restart=on-failure
RestartSec=5
WatchdogSec=300
```
Eliminated the manual monitoring loop entirely.

## High Score: Retry Wrapper for Flaky Network (0.78)

**Pattern:** `curl -f https://...` with 45% failure rate, retried 3-4x manually each failure.

**Fix:** Bash wrapper with exponential backoff:
```bash
#!/usr/bin/env bash
set -euo pipefail
max_retries=5; delay=2
for ((i=1; i<=max_retries; i++)); do
    curl -sf "$@" && exit 0
    echo "Attempt $i failed, retrying in ${delay}s..." >&2
    sleep "$delay"; delay=$((delay * 2))
done
echo "All $max_retries attempts failed" >&2; exit 1
```

## Medium Score: Git Workflow (0.72)

**Pattern:** `git add . && git commit -m "..." && git push` — 40x/week, 3-command chain.

**Fix:** `gpush` script — `gpush "commit message"` or bare `gpush` reuses last message.

## Medium Score: Multi-Repo Status (0.55)

**Pattern:** `cd /data/projects/repo1 && git status` repeated across 8 repos, 10x/week.

**Fix:** `repo-status` — loops all repos, prints DIRTY/CLEAN with first 5 changed files.

## Medium Score: DB Backup Guard (0.51)

**Pattern:** `cp db db.bak && sqlite3 db "PRAGMA integrity_check"` — 8x/week before migrations.

**Fix:** Rust CLI `db-guard` with subcommands: `backup`, `verify`, `restore`. Creates timestamped backups, runs integrity_check before/after.

## Low Score: Morning Triage Ritual (0.38)

**Pattern detected via time-of-day query:**
- 9:00 AM: `br ready` + `bv --robot-triage`
- 6:00 PM: `br sync --flush-only` + `git push`

**Fix:** Systemd timers — morning triage at 9am, evening sync at 6pm.

---

## Key Insight

The highest-scoring automations aren't always the most frequent — they're the ones where **error rate × time wasted per error** is highest. The log monitoring pattern was only 20x/week but each instance wasted 10-15 minutes of manual investigation.
