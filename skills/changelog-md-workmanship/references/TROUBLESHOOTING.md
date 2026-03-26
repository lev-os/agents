# Troubleshooting

## The history is too large to hold in context

Do not "try harder." Switch to chunked reconstruction:

- one tag range at a time
- one month at a time
- one epic at a time

Write findings into both:

- `CHANGELOG_RESEARCH.md`
- the live `CHANGELOG.md`

## The tag list and release list do not match

This is normal in many repos.

Use this rule:

- published GitHub Release: link the release page
- tag only: link the tag or tree page
- draft release: mark it as a draft

## The repo has no issue tracker

Then use:

- git history
- tags and releases
- existing docs
- commit subjects

Do not invent workstreams. Just omit that layer.

## The old changelog disagrees with the actual history

Treat the old changelog as a weak source.

Reconstruct from:

1. git history
2. tags
3. releases
4. tracker

Then rewrite the prose to match reality.

## The changelog reads like fluff

This usually means the section titles are too vague.

Fix by renaming sections around real landings:

- "Sync safety became explicit engineering work"
- "Multi-agent concurrency hardening"
- "Performance and storage throughput improved"

## The changelog reads like a commit dump

You are missing the synthesis step.

Ask:

- what capability landed?
- what user or agent behavior changed?
- what major fix/regression mattered?
- what was the turning-point commit?

Then rewrite around that.

## The changelog still feels incomplete

Use a coverage ledger in the research memo:

- chunk
- range
- status
- themes
- unresolved questions

If the ledger has gaps, the changelog has gaps.
