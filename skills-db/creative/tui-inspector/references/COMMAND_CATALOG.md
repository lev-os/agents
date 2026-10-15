# Command Catalog

## Single Run Commands

List profiles:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh --list-profiles
```

Baseline empty analytics:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-empty
```

Strict seeded analytics:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-seeded \
  --seed-required \
  --snapshot-required
```

## Suite Commands

Full matrix:

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded,messages-seeded,tour-seeded
```

Fast matrix:

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded \
  -- --boot-sleep 2 --snapshot-second 4
```

## Report Commands

Generate report:

```bash
bash /dp/tui_inspector/scripts/generate_tui_inspector_report.sh \
  --suite-dir /tmp/tui_inspector/suites/smoke_suite
```

## Health Commands

Doctor:

```bash
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh
```

Doctor with live smoke:

```bash
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh --full
```
