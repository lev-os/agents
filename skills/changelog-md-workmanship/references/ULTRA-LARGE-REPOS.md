# Ultra-Large Repos

## When to switch to the huge workflow

Use the huge workflow when any of these are true:

- multi-year history
- hundreds of non-merge commits in scope
- many tags/releases
- multiple tracker systems or exports
- you already know one pass will not fit in context

## Bootstrap

```bash
scripts/bootstrap-changelog-workdir.sh --huge /path/to/repo
```

This creates:

- `CHANGELOG.md`
- `CHANGELOG_RESEARCH/COVERAGE-LEDGER.md`
- `CHANGELOG_RESEARCH/00-overview.md`
- `CHANGELOG_RESEARCH/01-version-spine.md`
- `CHANGELOG_RESEARCH/02-history-chunk-a.md`
- `CHANGELOG_RESEARCH/03-history-chunk-b.md`
- `CHANGELOG_RESEARCH/99-open-questions.md`

## Core rule

Every chunk must end with:

- distilled findings written into its chunk file
- coverage ledger updated
- live `CHANGELOG.md` updated if the chunk is understood well enough

Do not let chunks pile up as unprocessed notes.

## Suggested loop

1. Build version spine
2. Extract tracker workstreams
3. Cluster history into candidate waves
4. Research chunk A
5. Distill chunk A into `CHANGELOG.md`
6. Repeat
