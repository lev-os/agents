# TUI Inspector Playbook

## Use Cases

1. Empty-state visual regression checks
2. Seeded-state smoke captures (messages/reservations/metrics)
3. Multi-screen demo reels for bug reports
4. CI artifact capture for flaky TUI issues

## Profile Guidance

- `analytics-empty`: isolate layout/text regressions in empty insight feed.
- `analytics-seeded`: capture analytics after generated tool traffic.
- `messages-seeded`: ensure data-backed list rendering is visible.
- `tour-seeded`: fast "does the whole shell render" overview.

## Fast Triage Loop

1. Run `analytics-empty` and inspect snapshot.
2. Run `analytics-seeded` and compare whether data appears.
3. If still blank, inspect `seed.stderr.log` and `vhs.log`.
4. If server exits early, check `run_summary.txt` + `run_meta.json`.

## Key Sequence Examples

- Analytics focus:
  `--keys "#,sleep:8,q"`
- Overlay check:
  `--keys "#,sleep:4,?,sleep:2,q"`
- Quick sweep:
  `--keys "1,sleep:2,2,sleep:2,3,sleep:2,q"`

## Common Failure Modes

- `database is locked`:
  Use the toolkit defaults; they isolate database/storage per run.
- Auth mismatch:
  Set `--auth-token` consistently for capture + seeding.
- Snapshot misses target state:
  Increase `--snapshot-second` and waits in `--keys`.
- No data after seeding:
  Increase `--boot-sleep` and `--seed-timeout`; review `seed.stderr.log`.
