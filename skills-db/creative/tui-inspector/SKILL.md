---
name: tui-inspector
description: >-
  Records terminal UIs with VHS and deterministic snapshots. Use when
  debugging TUI rendering, reproducing visual regressions, or sharing
  keyboard-driven UI behavior.
---

# TUI Inspector

Use this skill to create reproducible TUI video + screenshot artifacts with the
tooling in `/dp/tui_inspector`.

## Quick Start

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-seeded \
  --binary /data/tmp/cargo-target/debug/mcp-agent-mail \
  --project-dir /data/projects/mcp_agent_mail_rust
```

Outputs:

- MP4 video at `--output`
- PNG snapshot at `<output_basename>.png` (unless `--no-snapshot`)

## Workflow

- [ ] Confirm dependencies: `vhs`, `ttyd`, and optional `ffmpeg`
- [ ] Pick a profile (`analytics-empty`, `analytics-seeded`, `messages-seeded`, `tour-seeded`)
- [ ] Run capture with explicit `--binary`, `--project-dir`
- [ ] Inspect generated PNG first for quick verification
- [ ] Share MP4 plus run metadata for full playback context

## Why This Is Reliable

- Forces MCP mode (`unset AM_INTERFACE_MODE`)
- Uses isolated runtime state:
  `DATABASE_URL='sqlite:///.../storage.sqlite3'` and per-run `STORAGE_ROOT`
- Optional live seeding via MCP HTTP JSON-RPC to avoid empty captures
- Avoids flaky captures from locked/shared local DB files

## Commands

List profiles:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh --list-profiles
```

Empty-state baseline:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-empty \
  --binary /data/tmp/cargo-target/debug/mcp-agent-mail \
  --project-dir /data/projects/mcp_agent_mail_rust
```

Seeded analytics:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-seeded \
  --binary /data/tmp/cargo-target/debug/mcp-agent-mail \
  --project-dir /data/projects/mcp_agent_mail_rust
```

Seeded messages:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile messages-seeded \
  --binary /data/tmp/cargo-target/debug/mcp-agent-mail \
  --project-dir /data/projects/mcp_agent_mail_rust
```

Custom key script:

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh \
  --profile analytics-empty \
  --keys "#,sleep:6,?,sleep:2,q"
```

Suite mode:

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded,messages-seeded \
  --suite-name nightly_smoke
```

Report generation from existing suite:

```bash
bash /dp/tui_inspector/scripts/generate_tui_inspector_report.sh \
  --suite-dir /tmp/tui_inspector/suites/nightly_smoke
```

Doctor checks:

```bash
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh
```

## Common Flags

- `--jump-key "#"`: switch to analytics screen (legacy alias mode)
- `--boot-sleep 6`: wait for TUI boot before keypress
- `--capture-sleep 8`: hold legacy jump target before quit
- `--snapshot-second 9`: timestamp to extract PNG frame
- `--no-snapshot`: skip PNG extraction
- `--seed-demo`: enable live JSON-RPC data seeding
- `--seed-messages 12`: increase data density
- `--run-name my_case`: stable artifact directory name
- `--seed-required`: fail run when seeding fails
- `--snapshot-required`: fail run when snapshot extraction fails

## Operating Modes

Use these explicit modes to avoid accidental misuse:

1. Empty-state regression mode:
   `--profile analytics-empty` when validating layout/text/chrome behavior independent of data.
2. Seeded-state behavior mode:
   `--profile analytics-seeded` or `messages-seeded` when validating data visibility and event-driven changes.
3. End-to-end smoke mode:
   suite runner with `--fail-fast` and strict pass-through flags (`--seed-required`, `--snapshot-required`).
4. Forensic mode:
   preserve full run artifacts and inspect `run_meta.json`, `vhs.log`, and seeder logs before reruns.

## Decision Matrix

Use this fast selection guide:

- Need to verify a static rendering bug quickly:
  use single run + `analytics-empty`.
- Need to prove data does not display:
  use `analytics-seeded` with `--seed-required`.
- Need confidence across multiple screens:
  use suite mode with `tour-seeded`.
- Need CI signal quality:
  use suite mode + strict flags + deterministic `--suite-name`.

## Artifacts

Each run stores:

- `capture.tape` (exact tape used)
- `vhs.log`
- `run_summary.txt`
- `run_meta.json`
- `capture.mp4`
- `snapshot.png` (unless disabled)
- `seed.log` + stdout/stderr logs when seeding is enabled
- suite-level outputs:
  `suite_summary.txt`, `suite_manifest.json`, `report.json`, `index.html`

Default root:

```text
/tmp/tui_inspector/runs/<timestamp>_<profile>/
```

## Metadata Contract

`run_meta.json` should be treated as the canonical machine-readable outcome.
Core fields to trust:

- `status`
- `duration_seconds`
- `vhs_exit_code`
- `seed_exit_code`
- `snapshot_status`
- `video_exists`
- `snapshot_exists`
- `video_duration_seconds`

In suite mode, use:

- `suite_summary.txt` for human quick scan
- `suite_manifest.json` for machine consumption
- `report.json` for report-backed pipelines

## Validation

```bash
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh --help
bash /dp/tui_inspector/scripts/capture_mcp_agent_mail_tui.sh --list-profiles
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh --help
bash /dp/tui_inspector/scripts/generate_tui_inspector_report.sh --help
bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh --help
validate-skill.py /cs/tui-inspector/ --verbose
```

## CI and Automation Defaults

Recommended strict CI invocation:

```bash
bash /dp/tui_inspector/scripts/run_mcp_agent_mail_tui_suite.sh \
  --profiles analytics-empty,analytics-seeded,messages-seeded \
  --suite-name "ci_${GITHUB_RUN_ID:-manual}" \
  --fail-fast \
  -- --seed-required --snapshot-required
```

Recommended post-step bundle:

```bash
suite_dir="/tmp/tui_inspector/suites/ci_${GITHUB_RUN_ID:-manual}"
tar -czf "${suite_dir}.tar.gz" -C "$(dirname "$suite_dir")" "$(basename "$suite_dir")"
```

## Anti-Patterns

- Running seeded profiles without `--seed-required` when outcome strictness matters.
- Comparing screenshots without retaining `run_meta.json` and `vhs.log`.
- Reusing ambiguous run names in CI.
- Treating a passing MP4 generation as success when `seed_exit_code` failed.
- Skipping doctor checks after dependency or environment changes.

## Fast Incident Workflow

1. Run doctor:
   `bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh`
2. Run single strict seeded capture:
   `capture_mcp_agent_mail_tui.sh --profile analytics-seeded --seed-required --snapshot-required`
3. If failure:
   inspect `run_meta.json` first, then `vhs.log`, then `seed.stderr.log`.
4. Run minimal suite for blast-radius check:
   `analytics-empty,messages-seeded`.
5. Generate report and attach bundle to issue/PR.

## Preserved Baseline Content

The following baseline content is intentionally preserved (reorganized only):

- Quick-start capture command for analytics
- Output contract (`--output`, `<output_basename>.png`)
- Workflow checklist (deps, run, inspect PNG, share MP4)
- Reliability rationale (MCP mode + isolated runtime state)
- Common flags (`--jump-key`, `--boot-sleep`, `--capture-sleep`, `--snapshot-second`, `--no-snapshot`)
- Validation command pattern

## References

- Operational playbook: [PLAYBOOK.md](references/PLAYBOOK.md)
- Suite/report cookbook: [SUITE_AND_REPORT.md](references/SUITE_AND_REPORT.md)
- Failure triage map: [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- Mode selection matrix: [MODE_SELECTION.md](references/MODE_SELECTION.md)
- CI contract: [CI_CONTRACT.md](references/CI_CONTRACT.md)
- Anti-pattern catalog: [ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)
- Forensics handbook: [FORENSICS.md](references/FORENSICS.md)
- Command catalog: [COMMAND_CATALOG.md](references/COMMAND_CATALOG.md)

## Reference Index

- [PLAYBOOK.md](references/PLAYBOOK.md)
- [SUITE_AND_REPORT.md](references/SUITE_AND_REPORT.md)
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- [MODE_SELECTION.md](references/MODE_SELECTION.md)
- [CI_CONTRACT.md](references/CI_CONTRACT.md)
- [ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)
- [FORENSICS.md](references/FORENSICS.md)
- [COMMAND_CATALOG.md](references/COMMAND_CATALOG.md)
