# Forensics Handbook

## Primary Evidence Order

1. `run_meta.json` (canonical status envelope)
2. `run_summary.txt` (quick human summary)
3. `vhs.log` (recording/runtime details)
4. `seed.stderr.log` and `seed.log` (data-path diagnostics)
5. `capture.tape` (exact deterministic replay script)
6. media (`capture.mp4`, `snapshot.png`)

## Rapid Diagnosis Mapping

| Observation | First check | Likely issue |
|-------------|-------------|--------------|
| `status=failed` with `vhs_exit_code!=0` | `vhs.log` | tape/runtime or startup failure |
| `status=ok` but no data in UI | `seed_exit_code`, `seed.stderr.log` | seed not applied or timing mismatch |
| snapshot missing target content | `snapshot_status`, `snapshot_second`, `keys` | extraction timestamp too early/late |
| suite report missing run | `run_meta.json` presence | run artifact incomplete |

## Replay Strategy

Use tape + metadata to replay:

1. copy the exact `capture.tape`.
2. rerun `vhs` directly on tape.
3. if needed, adjust one variable at a time (`boot_sleep`, `snapshot_second`, `keys` waits).

## Issue Report Template

Include:

- suite/run directory
- `run_meta.json`
- exact command used
- one screenshot + short MP4 excerpt
- whether strict flags were enabled
