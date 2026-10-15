# Suite and Report Cookbook

## Run a Standard Matrix

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded,messages-seeded,tour-seeded \
  --suite-name full_matrix \
  --run-root /tmp/tui_inspector/suites
```

## Fast CI Matrix (short waits)

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded \
  --suite-name ci_quick \
  -- --boot-sleep 2 --snapshot-second 4
```

## Fail Fast for Strict Pipelines

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-seeded,messages-seeded \
  --fail-fast \
  -- --seed-required --snapshot-required
```

## Regenerate Report Only

```bash
bash /dp/tui_inspector/scripts/generate_tui_inspector_report.sh \
  --suite-dir /tmp/tui_inspector/suites/full_matrix
```

## Shareable Artifact Bundle

```bash
suite_dir="/tmp/tui_inspector/suites/full_matrix"
tar -czf "${suite_dir}.tar.gz" -C "$(dirname "$suite_dir")" "$(basename "$suite_dir")"
```

## Environment Validation Before Suite Runs

```bash
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh
```

With live smoke test:

```bash
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh --full
```
