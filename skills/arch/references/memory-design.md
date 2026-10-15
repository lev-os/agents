# Memory design

Read this branch when an architecture decision covers what an agent or system
keeps across steps or sessions: what persists, how it is found again, and how
its facts change. It feeds steps 4-8 of the decision flow. It reasons about fit;
adopting a store, provider or runtime remains a separate decision with its own
authority.

1. **Shallowest adequate mechanism** — start from the least structure that meets
   the stated retrieval and durability need (context, then files or records,
   then indexed search, then a graph). Escalate only for a named requirement
   or a measured retrieval failure the shallower layer cannot meet, and record
   that requirement as the tradeoff point.
2. **Stable entity identity** — give each tracked entity an identifier that
   survives renames, sessions and sources. Bind two records to one entity only
   through recorded evidence; a matching name establishes neither sameness nor
   difference.
3. **Applicability versus ingestion time** — keep when a fact holds (its
   validity interval) separate from when the system ingested it. "What was true
   at T" reads the interval; "what did we know at T" reads ingestion time.
4. **Supersession retains history** — a replaced or invalidated fact gets an
   end to its interval and stays queryable. Link a successor only when one is
   known; an explicit retraction stays a retraction, and an unknown successor
   stays unknown rather than invented.
   Exception: an explicit retention, privacy or deletion duty overrides
   retention and is recorded as its own rule.
5. **Verify and recover** — propose fitness functions that can falsify each
   choice: a point-in-time query, an identity-binding case, a superseded fact.
   When retrieval comes back empty, stale or conflicting, widen the query,
   choose the fact applicable at the requested query time (for a knowledge-time
   query, also ingested by then), and report any conflict left unresolved.
