# Prompts

## Small repo or narrow scope

```text
Write a concise but serious CHANGELOG.md update for this repo.

Research first:
- recent git history
- tags or releases in scope
- issue tracker items in scope if available

Requirements:
- direct commit links
- concrete dates
- one short version timeline
- thematic grouping instead of raw commit dump
```

## Medium repo

```text
Rebuild this project's CHANGELOG.md for the requested history window.

Research the real history first:
1. AGENTS.md and README.md
2. git tags and release metadata
3. non-merge commit history
4. issue tracker or beads history

Output requirements:
- version timeline with release-vs-tag distinction
- thematic capability sections
- delivered capability / closed workstreams / representative commits
- live links, not bare hashes
- agent-friendly orientation value
```

## Large or sprawling repo

```text
Create a full-history CHANGELOG.md for this large repo.

You must treat this as a chunked research project, not a one-shot writing task.

Process requirements:
1. Create a durable research memo immediately.
2. Build the version spine first from tags and releases.
3. Split history into sequential chunks.
4. After each chunk, update the live CHANGELOG.md before moving on.
5. Merge chunk findings into thematic capability waves at the end.

The changelog must:
- cover the full requested scope
- distinguish Releases from plain tags
- use direct commit URLs
- use issue-tracker history where available
- make the project's evolution understandable to another agent
```
