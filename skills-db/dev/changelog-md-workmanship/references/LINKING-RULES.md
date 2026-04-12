# Linking Rules

## Commit links

Use live commit URLs:

```text
https://github.com/<owner>/<repo>/commit/<sha>
```

Do not leave naked hashes unless the medium forbids links.

## Release vs tag links

Use these rules:

- If a GitHub Release exists, link `releases/tag/<version>`.
- If only a tag exists, link `tree/<version>` or the tag page.
- If the release is a draft, say so explicitly.

Do not fabricate release pages for tag-only versions.

## Issue tracker links

Prefer the most precise durable link available:

1. real issue page
2. checked-in issue tracker record
3. scoped code search that lands on the tracker file

For beads-style repos, scope search to `.beads/issues.jsonl` when possible.

## Version dates

Use concrete dates, not relative phrasing.

Good:

- `2026-03-21`
- `March 21, 2026`

Bad:

- `last week`
- `recently`
- `today`

## Representative commit selection

Choose commits that best explain:

- architecture landings
- major feature additions
- correctness fixes
- performance turning points
- reliability hardening

Do not flood the reader with every commit in the window.

## Evidence hierarchy

If there is a conflict:

1. git history
2. tag metadata
3. release metadata
4. issue tracker
5. docs and prior changelog prose

The changelog should reflect what actually landed, not what older prose claimed.
