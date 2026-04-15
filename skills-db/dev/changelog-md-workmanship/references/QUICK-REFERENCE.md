# Quick Reference

## Do this first

```bash
cat AGENTS.md README.md 2>/dev/null
touch CHANGELOG_RESEARCH.md
git for-each-ref refs/tags --sort=creatordate --format='%(refname:short)%x09%(creatordate:short)%x09%(subject)'
gh release list --limit 100
```

## Three non-negotiables

1. Build the version spine first.
2. Distinguish Releases from plain tags.
3. Update `CHANGELOG.md` after each research chunk.

## Best default structure

1. Scope + methodology note
2. Version timeline
3. Capability-wave sections
4. Notes for agents

## Best default section shape

- short narrative paragraph
- `Delivered capability`
- `Closed workstreams`
- `Representative commits`

## Common failure modes

- writing from memory
- raw commit dump instead of synthesis
- fake release links for tag-only versions
- broad tracker links instead of precise ones
- waiting until the end to write the changelog
