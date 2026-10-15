# Troubleshooting Map

## Runner Exits Non-Zero

1. Open `<run_dir>/run_meta.json`.
2. Check:
   - `vhs_exit_code`
   - `seed_exit_code`
   - `snapshot_status`
3. Open `<run_dir>/vhs.log` and (if seeded) `seed.stderr.log`.

## Seeded Profiles Show No Data

1. Use `--seed-required` to force failure when seeding misses.
2. Increase `--boot-sleep` and `--seed-timeout`.
3. Verify path/token consistency:
   - `--path /mcp/`
   - same `--auth-token` for runner+seeder.

## Snapshot Missing Target Screen

1. Increase waits in `--keys`.
2. Increase `--snapshot-second`.
3. Inspect the embedded video in suite `index.html` to find correct timestamp.

## Suite Report Missing Runs

1. Confirm each run directory has `run_meta.json`.
2. Re-run:
   `bash /dp/tui_inspector/scripts/generate_tui_inspector_report.sh --suite-dir <suite_dir>`
3. Check `<suite_dir>/suite_report.log`.

## Port Collisions

Use a unique port:

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --port 8891 \
  --profiles analytics-empty
```
