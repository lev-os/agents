# Save, resume, or recover an idea

The idea record holds the intent. The Wizard shapes it. Classification can help
interpret it; it is not a prerequisite to save, resume, or connect the idea.
The HUD displays observations and records rather than owning their identity.

1. Resolve the project owner and its current schema and template. In Leviathan,
   read `core/workstream/config.yaml` and `.lev/pm/ideas/_template/`;
   `.lev/pm/ideas/<id>/idea.yaml` is the declared home. Discover current read
   commands through `lev idea --help`. On resume, resolve the current record by
   its slug and read it before drafting, even when the request points at an
   archived source. Direct authoring requires active write scope when the owner
   has no write operation.
2. Keep `target_state` as the text of the desired result when the owning schema
   requires text. Optional Five-Fold notes, ontology, candidate graph, and domain
   matching belong beside it. For example, a seed-library logo has a text goal
   and optional candidate terms for the logo and library. Putting a nested graph
   inside `target_state` would violate this project's record contract.
3. Emit `id` equal to the folder slug and `type: idea` for a new record. On resume,
   preserve the current record's identity; an archived ID does not replace it.
   For example, if `ceo-orchestrator` already exists, retain that ID and keep
   `2025-07-02-ceo-orchestrator` in its source or authoring aliases. Aliases do not
   imply CLI alias resolution. Preserve source dates as source metadata; emit
   new record keys with the owner's current spellings.
4. Keep relationships in one typed `refs` collection. Each reference uses `type`,
   never `kind`. Reuse a supported source layout; the archive already has
   `{type, target, description}` entries. This is authoring data, not a new
   global wire-format ruling, relation registry, inverse writer, or graph API.
   Retain `sources` and `workstreams` while the compatibility schema requires
   them. Preserve unsupported relationship values at their source.
5. Recover source records without deleting or rewriting the archive. Account for
   directories, loose ideas, index-only entries, and process material separately.
   Resolve links only from exact identity or unambiguous existing-path evidence.
   A missing or ambiguous target keeps its original value and an explicit gap;
   an old implementation claim does not establish current implementation.
6. Validate the filled record against its owner schema and read it through the
   existing reader. Omit stored lifecycle stage. Keep readback and unresolved
   revision values null. Check source coverage and link destinations before
   claiming recovery complete. A missing target is a remaining gap, not a reason
   to fabricate an entity or an available plugin.

Exploration alone stays in the conversation. Load domain-binding guidance when
captured intent needs manifestation owners; software, video, and identity
workflows must follow their own evidence and skills.
