---
name: research
version: "2.0.0"
aliases: ["search", "research", "deep-research", "sherlock", "oracle", "social-search"]
triggers: ["/research", "/search", "/sherlock", "/oracle", "/deep"]
description: "Use when any research, search, or information gathering is needed."
skill_type: tool
category: process-research
primary_primitive: get
references:
  backends: references/backends.yaml
  strategies: references/strategies.yaml
  environment: references/environment.yaml
  perspectives: perspectives/COMPONENT.md
  templates: templates/COMPONENT.md
related_skills: ["lev-cdo", "notebooklm", "workflow-cited-research", "lev-social", "last30days"]
---

This skill does ONE thing: route a research query to the right backend at the right depth.

Never bypass the router. If the user said /search or /research, you classify complexity,
pick a strategy, call the backends, and return results. You are a router, not a researcher.
Do not improvise backend selection. Do not skip straight to a single tool when a strategy
was selected. Print the route line, execute the strategy, return results.

```yaml
steps:
  - id: classify
    action: Detect query complexity and select strategy
    instruction: |
      Parse the user's query and any explicit mode tag (quick/full/deep/max/social/academic).

      If no tag is given, classify by signal words:
        - "search", "lookup", "find", "what is" -> quick
        - "twitter", "reddit", "trending", "sentiment" -> social
        - "paper", "arxiv", "academic", "scholarly" -> academic
        - "research", "deep", "comprehensive", "analyze", "compare", "investigate" -> deep
        - "$research" with no override -> deep
        - "complete analysis", "exhaustive", "all angles" -> max

      If still ambiguous, default to quick. Speed wins when intent is unclear.
    validation: "You have selected exactly one strategy from: quick, full, deep, max, social, academic"
    on_failure: "Default to quick. Never stall asking the user to pick a mode."

  - id: announce_route
    action: Print the route line
    instruction: |
      Before calling any backend, print exactly one line:

        research-route: <strategy> | backends: <comma-separated list> | orchestration: <type>

      Example: research-route: deep | backends: valyu, perplexity, exa | orchestration: parallel-then-synthesize

      This is your contract. The backends you list are the backends you call.
    validation: "Output contains a line starting with 'research-route:'"
    on_failure: "Print the route line now, before proceeding."

  - id: execute
    action: Call backends per strategy definition
    instruction: |
      Execute the strategy from references/strategies.yaml:

        quick:    brave + tavily, first-success (return first good result)
        full:     brave + firecrawl + perplexity, parallel (merge all results)
        deep:     valyu + perplexity + exa, parallel then synthesize
        max:      all 5 backends, parallel then synthesize
        social:   grok + last30days, parallel
        academic: exa + perplexity, parallel

      Prefer MCP tools when available (brave, firecrawl, perplexity are MCP).
      Fall back to CLI commands from references/backends.yaml when MCP fails.

      For parallel strategies: call all backends, do not wait for one before starting others.
      For first-success: stop after the first backend returns usable results.
      For parallel-then-synthesize: gather all results, then write a synthesis.

      If a backend fails, skip it and continue with remaining backends.
      If ALL backends fail, tell the user which failed and why.
    validation: "At least one backend returned results, or all failures are reported with error messages"
    on_failure: "Try the next backend in the strategy. If none remain, report failure honestly."

  - id: synthesize
    action: Combine results (deep/max/academic only)
    instruction: |
      For strategies that end with synthesis (deep, max, academic):

      Write a synthesis with this structure:
        1. Executive summary (2-3 sentences)
        2. Key findings (numbered, each with source citation)
        3. Evidence table (claim | source | confidence)
        4. Open questions
        5. Sources (numbered URLs)

      Every claim needs a source. No source, no claim. If you are uncertain,
      say so in the open questions section rather than stating it as a finding.

      For quick/full/social: skip synthesis, return results directly.
    validation: "Every finding in the synthesis links to a source URL from the backend results"
    on_failure: "Remove any finding that lacks a source. Unsourced claims go to open questions."

  - id: deliver
    action: Return results to the user
    instruction: |
      Format depends on strategy:
        - quick/social: direct results with URLs
        - full: merged results grouped by source
        - deep/max/academic: full synthesis document

      For cited research that needs to persist beyond this conversation,
      hand off to notebooklm or workflow-cited-research.
    validation: "Response contains at least one URL from backend results"
    on_failure: "If no URLs in response, you hallucinated. Go back to execute step."

routing_config:
  default_mode: quick
  tag_parsing:
    quick: ["quick", "search", "lookup", "find"]
    full: ["full", "standard", "thorough"]
    deep: ["deep", "research", "analyze", "investigate", "sherlock"]
    max: ["max", "exhaustive", "complete", "all"]
    social: ["social", "twitter", "reddit", "trending", "sentiment"]
    academic: ["academic", "papers", "arxiv", "scholarly"]
  dollar_research_default: deep
  shim: ~/.claude/commands/search.md

mcp_tool_map:
  brave: [mcp__brave-search__brave_web_search, mcp__brave-search__brave_local_search]
  firecrawl: [mcp__firecrawl-mcp__firecrawl_search, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_extract]
  perplexity: [mcp__perplexity-mcp__search, mcp__perplexity-mcp__reason, mcp__perplexity-mcp__deep_research]

fallback_chain:
  - try: mcp tool
  - try: cli command from references/backends.yaml
  - try: next backend in strategy
  - finally: report failure with error
```

## Anti-Patterns

| Excuse | Reality |
|--------|---------|
| "I'll just use Brave directly, it's faster" | You are a router. Classify, announce, execute. No shortcuts when /search was invoked. |
| "The user probably wants a quick answer" | Parse their words. "Research X thoroughly" is not quick. Signal words decide, not your guess. |
| "I already know the answer from training data" | Training data is not a search result. You have no URLs. Call the backends. |
| "Let me search for a few things first to understand the query" | That is the quick strategy. If you classified as deep, run deep. Do not downgrade mid-execution. |
| "I'll synthesize later" | Synthesis happens in the same response. There is no later. |
| "One source is enough for this" | Quick = first-success is fine. Deep/max require the full backend set. Do not short-circuit. |
| "The MCP tool failed so I'll just answer from context" | Fail over to CLI. If CLI fails, try next backend. Only report failure when ALL options are exhausted. |
| "I need to ask which mode they want" | Default to quick. The user gave you a query, not a quiz. |
