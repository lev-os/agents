---
name: beads-dolt-native
description: Use when standardizing Beads across many repos or machines, especially to move projects onto one Dolt-native shared-server playbook with deterministic database names, fixed ports, and repeatable sync commands.
---

# Beads Dolt Native

One playbook for every repo. No per-project improvisation.

## When to Use

- A repo's `bd` keeps connecting to the wrong Dolt server
- Multiple Beads projects live on one machine
- You want one repeatable setup across two machines
- You need to rollout Beads config across many repos
- You want a deterministic database name per repo instead of ad hoc defaults

Do not use this skill for one-off issue edits. Use it for board setup, healing, and fleet-wide standardization.

## Canonical Playbook

### Machine policy

- Upgrade `bd` to the latest Homebrew release first
- Run Beads in Dolt-native mode
- Use one shared local Dolt server port: `3308`
- Use deterministic per-repo database names
- Use repo remote sync via `bd dolt push` / `bd dolt pull`
- Do not use DoltHub remotes

### Repo policy

For every Beads repo:

- `dolt.mode: server`
- `dolt.shared-server: true`
- `dolt.host: 127.0.0.1`
- `dolt.port: 3308`
- `dolt.database: beads_<repo>_<hash>`

### Sync policy

- Primary machine after local changes:
  - `bd dolt push`
  - `git push`
- Secondary machine before work:
  - `git pull`
  - `bd dolt pull`

## Automation

Use the rollout helper:

```bash
python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py scan --roots /Users/jean-patricksmith/digital

python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py apply --roots /Users/jean-patricksmith/digital --sync push

python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py apply --roots /Users/jean-patricksmith/digital --sync pull
```

`scan` reports what would change.

`apply --sync push` is the primary-machine path.

`apply --sync pull` is the secondary-machine path.

## Guarantees

- Stable DB names derived from repo identity
- Shared server config applied uniformly
- Stale project-local ports replaced with `3308`
- Verification uses `bd dolt show`, `bd dolt status`, and `bd ready`

## Notes

- This skill assumes the current stable machine-wide convention is shared-server on `3308`
- If a repo needs a different DB name than the derived one, override it explicitly after rollout
- If `bd dolt pull` fails because the remote state has never been pushed, run the primary-machine path first
