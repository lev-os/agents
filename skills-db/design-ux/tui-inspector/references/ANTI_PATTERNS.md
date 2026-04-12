# Anti-Patterns

## 1) Treating Video Creation as Success

Symptom:
- MP4 exists, but seeded state is empty.

Why bad:
- MP4 generation only proves recording worked, not data correctness.

Fix:
- Check `run_meta.json` fields:
  `seed_exit_code`, `status`, `snapshot_status`.

## 2) Running Seeded Profiles Without Strictness

Symptom:
- Intermittent “pass” despite occasional seeding failures.

Fix:
- Use `--seed-required`.

## 3) Using Ambiguous Run Names in CI

Symptom:
- Artifact collisions or hard-to-interpret history.

Fix:
- Use deterministic names, e.g.:
  `--suite-name "ci_${GITHUB_RUN_ID:-manual}"`.

## 4) Skipping Doctor Before Deep Debug

Symptom:
- Waste time chasing false application issues caused by missing tools or wiring.

Fix:
- Run:
  `bash /dp/tui_inspector/scripts/doctor_tui_inspector.sh`.

## 5) Rerunning Blindly Without Forensics

Symptom:
- Multiple reruns with no narrowing of root cause.

Fix:
1. `run_meta.json`
2. `vhs.log`
3. `seed.stderr.log` (if seeded)
4. then adjust flags/timing.
