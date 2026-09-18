Select one routine after the root has handled local retrieval and explicit child selectors.
Specific domain signals take precedence over generic depth words. If multiple domains
remain material and the requested decision does not resolve them, ask for the focus.
Do not change providers or stage order after selecting the routine.

Match the query to the following signals:
- "search", "lookup", "find" → quick
- "twitter", "reddit", "trending" → social
- "paper", "arxiv" → academic
- "research", "deep", "analyze" → deep
- "exhaustive", "all angles" → max
- people, employee, founder, executive → people
- company, competitor, firmographic → company
- lead, prospect, contact enrichment → lead
- market, category, vendor comparison → market
- docs, API, repository, implementation → technical
- news, current event, announcement → news
Default: quick. Print route line before calling backends:
  research-route: <routine> | stages: <fixed stage ids>

Quick, deep, max, social, and academic are executable `lev research` strategies. Domain routines are reference-only until FlowMind routing exists; load `../references/domain-routines.md` and execute the selected routine mechanically.
