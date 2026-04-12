# Examples

## Pattern: capability-first sections

Strong changelogs do not read like:

- "commit A happened"
- "then commit B happened"
- "then commit C happened"

They read like:

- an important capability wave landed
- here is what it changed
- here are the workstreams behind it
- here are the commits to inspect

## Pattern: version spine plus thematic synthesis

The best balance is:

- explicit version timeline for chronology
- thematic sections for comprehension

If you only do chronology, the document becomes noisy.

If you only do themes, the reader loses temporal orientation.

## Pattern: issue tracker as intent layer

When a repo has a tracker, use it to answer:

- what was the goal?
- what was the acceptance criteria?
- which related fixes belong in one wave?

The issue tracker gives intent. The commits give implementation evidence.

## Pattern: direct evidence links

Prefer:

- live release URLs
- live commit URLs
- precise tracker links

Avoid:

- naked hashes
- vague prose with no evidence
- broad search links when a scoped tracker link exists

## Pattern: compaction-resistant workflow

For big histories, the winning pattern is:

1. make a research memo
2. make the changelog skeleton
3. research one chunk
4. distill immediately into the changelog
5. repeat

This is the only reliable way to maintain quality when the investigation cannot fit in one context window.

## Pattern: separate canonical changelog from generated release notes

Generated release notes are ephemeral artifacts.

`CHANGELOG.md` is the durable historical orientation layer.

Do not conflate them.
