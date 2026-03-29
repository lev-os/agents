---
name: workflow-beads-rollout
description: Set up many projects for one shared Beads Dolt-native playbook across a machine or pair of machines. Invoke with /workflow beads-rollout.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Workflow: Beads Rollout

## Trigger

Use when you want to standardize many repos onto one Beads playbook instead of fixing each project manually.

## Inputs

- One or more root directories to scan for repos with `.beads/`
- Machine role:
  - `primary` for push-first machine
  - `secondary` for pull-first machine

## Steps

1. Upgrade and verify `bd` on the machine.
2. Scan all target roots for repos with `.beads/`.
3. For each repo:
   - derive deterministic Dolt database name
   - set `database`, `host`, and `port`
   - patch config to shared-server mode
   - start local Dolt server access
4. Sync:
   - `primary` -> `bd dolt push`
   - `secondary` -> `bd dolt pull`
5. Verify with `bd dolt show` and `bd ready`.

## Team

| Role | Responsibility |
|------|---------------|
| operator | chooses roots and machine role |
| workflow | runs the rollout helper and reports failures |

## Outputs

- JSON rollout report per repo
- Deterministic DB name per repo
- Shared-server Beads config stamped into each repo

## Validation

- `bd dolt show --json` succeeds for each repo
- `bd ready --json` succeeds for each repo
- config shows shared-server semantics and port `3308`

## Canonical Command

```bash
# audit only
python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py scan --roots /Users/jean-patricksmith/digital

# primary machine
python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py apply --roots /Users/jean-patricksmith/digital --sync push

# secondary machine
python3 /Users/jean-patricksmith/.agents/skills/beads-dolt-native/scripts/beads_rollout.py apply --roots /Users/jean-patricksmith/digital --sync pull
```
