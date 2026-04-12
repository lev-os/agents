# Command Recipes

## Git-only repo

```bash
git for-each-ref refs/tags --sort=creatordate --format='%(refname:short)%x09%(creatordate:short)%x09%(subject)'
git log --reverse --oneline --decorate=no --no-merges | head -n 50
git log --oneline --decorate=no --no-merges --max-count 120
git log --oneline --decorate=no --no-merges <tag-a>..<tag-b>
```

## GitHub repo with releases

```bash
gh release list --limit 100
gh release view <tag> --json tagName,name,publishedAt,url,isDraft
gh issue list --state all --limit 200
```

## Beads-style checked-in tracker

```bash
jq -r 'select(.status=="closed") | [.id,.title,.closed_at] | @tsv' .beads/issues.jsonl
jq -r 'select(.status=="closed" and (.issue_type=="epic" or .issue_type=="feature")) | [.id,.title,.closed_at] | @tsv' .beads/issues.jsonl
```

## Large-history chunking

```bash
# Date window
git log --oneline --decorate=no --no-merges --since='2026-01-01' --until='2026-02-01'

# Tag window
git log --oneline --decorate=no --no-merges v0.1.10..v0.1.20

# Commit-count window
git log --oneline --decorate=no --no-merges --max-count 100
```

## Skill scripts

```bash
# Bootstrap research files in a repo
scripts/bootstrap-changelog-workdir.sh /path/to/repo

# Bootstrap huge-repo multi-pass scaffolding
scripts/bootstrap-changelog-workdir.sh --huge /path/to/repo

# Generate a version timeline skeleton
scripts/build-version-spine.py --repo /path/to/repo

# Normalize tracker workstreams from beads, GitHub Issues, Linear/Jira exports, or milestone docs
scripts/extract-tracker-workstreams.py --repo /path/to/repo --format markdown

# Cluster commit history into candidate capability waves
scripts/cluster-history.py --repo /path/to/repo --format markdown

# Audit a completed changelog
scripts/validate-changelog-md.py /path/to/repo/CHANGELOG.md

# Audit a completed changelog and verify live links
scripts/validate-changelog-md.py --verify-links /path/to/repo/CHANGELOG.md
```
