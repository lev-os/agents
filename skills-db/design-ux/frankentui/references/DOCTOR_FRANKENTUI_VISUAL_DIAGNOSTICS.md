# doctor_frankentui Visual Diagnostics

Practical runbook for using `doctor_frankentui` as a visual debugging instrument, not only a capture-status checker.

## Purpose

Use this when:
- diagnosing TUI visual defects,
- validating screen polish claims,
- debugging capture quality issues (snapshot timing, profile drift, runtime exits).

Primary target:
- `/data/projects/frankentui`

## Canonical Full-Suite Capture

```bash
cd /data/projects/frankentui
rch exec -- cargo build -p doctor_frankentui -p ftui-demo-showcase

RUN_ROOT="/tmp/doctor_frankentui_demo_audit_$(date +%Y%m%d_%H%M%S)"
./target/debug/doctor_frankentui suite \
  --app-command '/data/projects/frankentui/target/debug/ftui-demo-showcase' \
  --project-dir /data/projects/frankentui \
  --run-root "$RUN_ROOT" \
  --suite-name demo_showcase_audit \
  --keep-going
```

Artifacts:
- `$RUN_ROOT/demo_showcase_audit/report.json`
- `$RUN_ROOT/demo_showcase_audit/index.html`
- `$RUN_ROOT/demo_showcase_audit/demo_showcase_audit_<profile>/capture.mp4`
- `$RUN_ROOT/demo_showcase_audit/demo_showcase_audit_<profile>/snapshot.png`

## Minimum Health Triage

```bash
REPORT="$RUN_ROOT/demo_showcase_audit/report.json"
jq -r '.runs[] | [
  .profile,
  .status,
  ("capture_error_reason=" + (.capture_error_reason // "null")),
  ("vhs_driver=" + (.vhs_driver_used // "unknown")),
  ("fallback_active=" + (.fallback_active|tostring)),
  ("snapshot_status=" + (.snapshot_status // "unknown")),
  ("snapshot_exists=" + (.snapshot_exists|tostring)),
  ("video_exists=" + (.video_exists|tostring)),
  ("video_duration_seconds=" + (.video_duration_seconds|tostring))
] | @tsv' "$REPORT"
```

Always read this before opening visuals.

## Visual Inspection Protocol

### 1) Inspect per-profile snapshot

Open each:
- `.../snapshot.png`

### 2) Build timeline strip

```bash
SUITE_DIR="$RUN_ROOT/demo_showcase_audit"
for p in analytics-empty analytics-seeded messages-seeded tour-seeded; do
  d="$SUITE_DIR/demo_showcase_audit_${p}"
  ffmpeg -y -i "$d/capture.mp4" \
    -vf "fps=1,scale=640:-1,tile=8x1" \
    -frames:v 1 "$d/timeline_strip.png" >/dev/null 2>/dev/null
done
```

Open each:
- `.../timeline_strip.png`

### 3) Use `capture.mp4` as ground truth

If snapshot and timeline disagree, inspect `capture.mp4` directly.

## Interpretation Rules

- `status=ok` means capture pipeline succeeded, not that UI quality passed.
- Snapshot showing shell prompt is a failed visual diagnostic even if `snapshot_status=ok`.
- Timeline with UI frames + shell snapshot usually means snapshot timing drift.
- Timeline shell-only means app never stabilized in-capture.
- `fallback_active=true` or `vhs_driver_used=docker` means host path is degraded; treat timing conclusions cautiously.

## Fixing Profile Timing and Capture Drift

Profiles live in:
- `crates/doctor_frankentui/profiles/*.env`

Typical fix:
- tune `snapshot_second` to land before app exits and after intended UI state appears.

Example issue pattern:
- snapshot shows shell prompt
- timeline shows valid UI earlier
- action: lower `snapshot_second`

Important:
- these profile files are embedded via `include_str!`
- rebuild `doctor_frankentui` after editing profile env files

```bash
rch exec -- cargo build -p doctor_frankentui
```

## Fast Re-Verification Loop

Targeted profile:

```bash
RUN_ROOT="/tmp/doctor_frankentui_verify_$(date +%Y%m%d_%H%M%S)"
./target/debug/doctor_frankentui suite \
  --profiles analytics-empty \
  --app-command '/data/projects/frankentui/target/debug/ftui-demo-showcase' \
  --project-dir /data/projects/frankentui \
  --run-root "$RUN_ROOT" \
  --suite-name analytics_empty_verify \
  --keep-going
```

Then full suite again.

## When It’s a Real TUI Bug (Not Capture)

Treat as real app defect when:
- timeline + snapshots consistently show clipped, broken, or mis-layered UI across reruns,
- and the issue reproduces in capture videos for multiple timings/profiles.

Then patch screen implementation and re-run doctor flow.

## Quality Gates for doctor_frankentui Changes

```bash
rch exec -- cargo test -p doctor_frankentui
rch exec -- cargo clippy -p doctor_frankentui -- -D warnings
```

If you edited demo screen code too, also run:

```bash
rch exec -- cargo test -p ftui-demo-showcase
```
