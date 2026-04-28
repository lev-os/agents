Parse the query. Select exactly one strategy by signal words:
- "search", "lookup", "find" → quick
- "twitter", "reddit", "trending" → social
- "paper", "arxiv" → academic
- "research", "deep", "analyze" → deep
- "exhaustive", "all angles" → max
Default: quick. Print route line before calling backends:
  research-route: <strategy> | backends: <list> | orchestration: <type>
