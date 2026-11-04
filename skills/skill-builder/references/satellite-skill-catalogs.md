# Satellite skill catalogs

Use when a user asks to intake a whole external skill repository/catalog, especially when it may overlap with an existing domain such as `marketing`.

## Pattern

Prefer a satellite-first model instead of blindly copying every upstream skill into the canonical library. Keep the default YAML sparse: infer domain from folder names, infer repo metadata from git/submodule state, and require only a repo-slug-to-glob mapping.

Minimal Option A shape:

```text
skills-db/
  <domain>/
    <canonical-skill>/
      SKILL.md
  _repos/
    <domain>/
      repos.yaml                # minimal slug -> SKILL.md glob map
      <source-id>/              # upstream repo as submodule or pinned clone; do not hand-edit
```

```yaml
# skills-db/_repos/<domain>/repos.yaml
<source-id>: "skills/*/SKILL.md"
```

Extended projection/review shape, only when needed:

```text
skills-db/
  _repos/
    <domain>/
      <source-id>/              # upstream repo as submodule or pinned clone; do not hand-edit
      _meta/<source-id>.yaml    # optional provenance/trust overrides if git metadata is insufficient
  <domain>/
    _subscriptions/
      <source-id>.yaml          # optional include/hold/exclude rules
    _projections/
      <source-id>/              # generated normalized candidates, not hand-edited
    <canonical-skill>/
      SKILL.md
      sources.yaml              # upstream refs and merge notes
```

## Minimum intake sequence

1. Clone or add the upstream repo under `_repos/<domain>/<source-id>`; keep raw source separate from canonical skills.
2. Record the repo in `_repos/<domain>/repos.yaml` as `<source-id>: "<skill-glob>"`. Only add optional metadata if git/submodule state cannot provide origin/ref/commit/license/trust.
3. Run upstream validation if provided, then local structural checks for `SKILL.md` frontmatter.
4. Build a raw index of skills: domain, source type, source slug, name, description, tags, relative path, line count, frontmatter keys, commands/scripts referenced, git commit.
5. Compare against canonical `skills-db/<domain>` for:
   - exact name overlap
   - trigger/description overlap
   - semantic overlap with different names
   - security/tooling risk
6. Keep satellite rows searchable but not promoted. Write optional `_subscriptions/<source-id>.yaml` only when human include/hold/exclude policy is needed.
7. Generate projection candidates only for approved includes; preserve source commit/path in each candidate.
8. Promote into canonical domain only after review. Never edit the satellite repo directly.

## Example subscription

```yaml
source: coreyhaines31-marketingskills
domain: marketing
mode: curated_projection
status: subscribed

include:
  - ai-seo
  - content-strategy
  - copywriting
  - marketing-loops
  - product-marketing
  - site-architecture

hold_for_merge_review:
  - cro
  - social
  - emails
  - ads
  - analytics
  - referrals

exclude:
  - image
  - video

merge_policy:
  exact_name_conflict: review
  semantic_overlap: create_diff_report
  canonical_wins: true
  upstream_updates: preserve_as_source_patch
```

## Indexing guidance

- Raw deterministic index is canonical for merge decisions and activation.
- Codebase Memory is useful for markdown section/file graph search and concept discovery, but should not be the only merge source of truth.
- QMD/graphify-style indexes can be used as spikes for docs/article rendering or semantic relationship extraction.

## Decision rule

If a repo contains many skills and any overlap exists with current domain skills, recommend satellite-first intake. Start with `_repos/<domain>/repos.yaml` only, make satellite rows queryable, then add subscription/projection YAML only for reviewed promotions or policy decisions. Full merge is only safe after a generated overlap report and explicit approval.
