# Tracker Adapters

## Supported sources

The skill now has direct extraction support for:

- beads-style `.beads/issues.jsonl`
- GitHub Issues via `gh`
- Linear-style JSON exports
- Jira-style JSON exports
- milestone markdown documents

## Normalized fields

All adapters try to emit:

- `id`
- `title`
- `status`
- `closed_at`
- `kind`
- `url`
- `labels`
- `source`

## When to use which

- Use beads when the repo keeps tracker history in git.
- Use GitHub Issues when the project uses GitHub as the live tracker.
- Use Linear or Jira exports when the history is external but exportable.
- Use milestone markdown when the project tracks work in roadmap docs instead of issues.

## Script entry point

```bash
scripts/extract-tracker-workstreams.py --repo /path/to/repo --format markdown
```

Examples:

```bash
# beads auto-detection
scripts/extract-tracker-workstreams.py --repo /path/to/repo --format markdown

# GitHub Issues
scripts/extract-tracker-workstreams.py --repo /path/to/repo --kind github --state closed --format json

# Linear export
scripts/extract-tracker-workstreams.py --kind linear --input linear-export.json --format markdown

# Jira export
scripts/extract-tracker-workstreams.py --kind jira --input jira-export.json --format json

# milestone markdown
scripts/extract-tracker-workstreams.py --kind milestones --input MILESTONES.md --format markdown
```
