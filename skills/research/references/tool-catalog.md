# Research tool catalog

Use this vocabulary:

- capability: required operation, such as search, fetch, crawl, enrich, or synthesize
- provider: service producing the result, such as Exa, Perplexity, Apollo, or OpenAlex
- gateway: access and billing path; `direct` or `monid`
- adapter: Lev code translating a gateway into the research contract
- tool: one provider endpoint
- evidence: returned URL, paper, profile, filing, post, or dataset row

## Direct adapter catalog

Read live state with `lev research adapters --json`. Current capability families are:

- web search: Brave, Tavily, Exa, Valyu, Firecrawl
- synthesis: Perplexity, Oracle, Grok
- academic: arXiv, Exa, Perplexity
- social: Grok, Hacker News, ScrapeCreators
- extraction: Firecrawl
- technical corpus: Hugging Face

## Monid gateway catalog

Monid is the fallback gateway for capabilities absent from direct adapters. Discovery and inspection are free; endpoint execution spends the Monid balance.

Run only the query prescribed by the selected routine:

```bash
NO_COLOR=1 monid discover -q "<capability description>" -l 20 -j
monid inspect -p <provider> -e <endpoint>
```

Mechanical preferences:

1. Use a healthy direct adapter when the matching direct credential exists.
2. Otherwise use the routine's named Monid provider/endpoint.
3. Use Monid discovery only when that endpoint is absent or unhealthy; select the highest-scoring verified healthy result within the routine's cost ceiling.
4. Never execute a paid endpoint without first reading its schema and price.

Known Monid capability families include web search/fetch/crawl/extract, academic papers and citation expansion, social-platform search, company/news/market data, people search, and lead enrichment. Treat `monid discover` as live authority because its catalog changes.
