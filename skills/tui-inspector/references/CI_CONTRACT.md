# CI Contract

## Intent

Define a repeatable, strict, and diagnosable CI workflow for TUI evidence capture.

## Minimum Required Outputs

For each suite run, publish:

- `suite_summary.txt`
- `suite_manifest.json`
- `report.json`
- `index.html`
- all per-run directories (including `capture.tape`, `run_meta.json`, logs, media)

## Recommended Strict Invocation

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded,messages-seeded \
  --suite-name "ci_${GITHUB_RUN_ID:-manual}" \
  --fail-fast \
  -- --seed-required --snapshot-required
```

## Exit Semantics

- Non-zero suite exit means at least one profile failed.
- A run should be considered failed if:
  - `status != "ok"`, or
  - `vhs_exit_code != 0`, or
  - strict flags required and `seed_exit_code != 0` or `snapshot_status != "ok"`.

## Determinism Tips

- Use explicit `--suite-name` in CI.
- Avoid mixing unrelated runs in same `run-root`.
- Keep profile list stable for longitudinal comparisons.

## Artifact Bundling

```bash
suite_dir="/tmp/tui_inspector/suites/ci_${GITHUB_RUN_ID:-manual}"
tar -czf "${suite_dir}.tar.gz" -C "$(dirname "$suite_dir")" "$(basename "$suite_dir")"
```
