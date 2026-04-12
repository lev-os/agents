# Section Templates

## Canonical opening

```markdown
# Changelog

This is a synthesized, agent-facing changelog for the full history of `[project]`.

Scope window: project inception on `[start-date]` through `[end-version]` on `[end-date]`.

This document was rebuilt from git history, version tags, release metadata, and the project issue tracker.

This document is intentionally organized by landed capabilities, not raw diff order.
```

## Version timeline

```markdown
## Version Timeline

`Kind` distinguishes a published release from a plain git tag.

| Version | Kind | Date | Summary |
|---------|------|------|---------|
| [`vX.Y.Z`](URL) | Release | YYYY-MM-DD | One-line summary |
| [`vX.Y.Z`](URL) | Tag | YYYY-MM-DD | One-line summary |
```

## Capability wave section

```markdown
## N) [Capability Wave Title]

[Short paragraph explaining why this wave mattered.]

### Delivered capability

- Capability one
- Capability two
- Capability three

### Closed workstreams

- [`issue-id`](URL) Description
- [`epic-id`](URL) Description

### Representative commits

- [`abc1234`](URL) Short explanation.
- [`def5678`](URL) Short explanation.
- [`ghi9012`](URL) Short explanation.
```

## Notes for agents

```markdown
## Notes for Agents

- Start with the version timeline if you need chronology.
- Jump into the thematic sections if you need architectural understanding.
- Use workstream links for intent and commit links for implementation evidence.
```

## Research memo stub

```markdown
# Changelog Research

## Scope
- Requested window:
- Repo:

## Version spine
- Tags found:
- Releases found:
- Draft releases:

## Chunk 01
- Range:
- Themes:
- Candidate commits:
- Tracker items:
- Open questions:
```
