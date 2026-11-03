# Sparse taxonomy gate-shaping pattern

Use this reference when a user is shaping a routing/config/taxonomy migration and is not ready to break ground with code yet.

## Core paradox

Default to sparse folders, but do not overfit data to sparse folders.

Meaning:

- Do not explode taxonomies before real data proves the need.
- Do not force real data into a premature sparse taxonomy just because a folder or rule exists.
- Use typed metadata, source receipts, facets, retrieval policies, and synthesis layers to absorb early ambiguity.
- Promote folders only when they are stable operational commitments: ownership, lifecycle, permissions, retrieval, or publication boundaries.

## Plan sections to add

### Current-state inventory

Summarize the artifact being replaced or migrated. For a target map/config, capture:

- declared source-of-record boundaries;
- destination taxonomies;
- routing rules and default/no-match behavior;
- gate refs and mutation rules;
- entity seeds or policy lists;
- risky behavior, especially any rule that lets agents auto-add taxonomy or routing rules.

Interpret the artifact as migration evidence unless the user explicitly says it remains canonical.

### What must be true

Examples:

- Company/project config declares id, source of record, sources, record types, retrieval policies, sparse taxonomy, derived layers, and mutation boundaries.
- Migration reader labels imported facts as `legacy_input`, `accepted_policy`, `needs_review`, or `discarded`.
- Loader fails closed when source-of-record, retrieval policy, sparse taxonomy, or company boundary is missing.
- Router emits a decision record, not just a path: route state, canonical/staging home, facets, evidence refs, confidence, promotion reason, rejected routes.
- Weak/ambiguous evidence routes to `source_receipt_only`, `stage_in_inbox_with_facets`, `needs_human_route`, or `propose_new_leaf_with_evidence`.
- Retrieval mode is selected before answer generation; exact/latest/provenance/status requests use structured/source-backed paths before semantic search.
- Mutations remain dry-run until approved.

### What must not be true

Examples:

- No automatic taxonomy expansion on no-match.
- No treating a folder name as evidence that an item belongs there.
- No empty destination leaves unless marked scaffold/system root with owner, reason, and review date.
- No coercing ambiguous data into the nearest known bucket.
- No duplicating one asset across conceptual folders; use facets/graph edges.
- No silent cross-boundary routing between companies/projects.
- No semantic retrieval as authority for exact/latest/provenance questions.
- No weakening gates/skills/configs to make a failing route pass.

## Gate candidates

Turn the above into named gates such as:

- `company_config_required`
- `target_map_legacy_only`
- `no_taxonomy_explosion`
- `no_overfit_to_sparse_taxonomy`
- `evidence_before_folder`
- `facets_before_folders`
- `one_asset_one_home`
- `company_boundary_enforced`
- `retrieval_mode_critic`
- `source_derived_separation`
- `conflict_visibility`
- `dry_run_mutations_only`

Each gate should have a fail condition that is mechanically checkable or fixture-testable.

## Before breaking ground

Separate future surfaces from current edits:

- Code: schema, loader, migration reader, dry-run router, linter/gate runner, eval scorer, retrieval-mode critic.
- Minimal folders: config files, schemas, eval fixtures, scripts.
- Explicit non-actions: do not create destination folder trees, Drive mirrors, per-prospect/client trees, or new routing leaves as part of shaping.
- Skills/instructions: update local AGENTS/gates only after names and policy stabilize; avoid broad skill rewrites until fixture proof exists.

## Pitfall

If the user is asking for gates, predicates, or shaping language, the deliverable is usually an enriched plan with examples and non-actions — not implementation. Keep unresolved policy choices visible as open decisions.