# Markdown skill catalog indexing with Codebase Memory

Use this when indexing a repository that is mostly Agent Skills or Markdown catalogs rather than application source code.

## What to expect

- The graph may be dominated by `File`, `Folder`, and `Section` nodes rather than functions/classes/routes.
- `DEFINES`/containment edges are still useful for finding where concepts appear, but there may be little or no call graph.
- Section search is good for questions like "where is `Article/BlogPosting` discussed?" or "which skill mentions CRO?"
- It is not a sufficient canonical merge engine for skills because merge/activation decisions need frontmatter, provenance, validation, security, and subscription policy.

## Recommended layered index

1. Raw deterministic index: parse each `SKILL.md` frontmatter and path; this is canonical for skill inventory and merge gates.
2. Codebase Memory: index the repo for section/file graph search and exploratory architecture/discovery.
3. Optional semantic graph/index: use only as advisory evidence for overlap and aliases.

## Safe conclusion to report

"CBM is useful as a Markdown section/file graph for discovery, but skill subscription and merge decisions should be driven by a deterministic catalog index plus explicit policy."
