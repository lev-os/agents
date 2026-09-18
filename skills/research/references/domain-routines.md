# Proposed domain routines

These contracts are deterministic references, not native `lev research` strategies. The agent selects one routine and executes its stages in order. FlowMind ownership and automatic context injection are deferred.

## People

1. `identity-search`: Monid `ploid:/search`; fallback `pdl:/v5/person/search`.
2. `profile-resolve`: Monid `ploid:/enrich`; fallback provider returned by inspected catalog.
3. `cross-check`: quick web routine for employer and role claims.
4. `normalize`: preserve provider IDs and attach source URLs.

## Company

1. `entity-resolve`: Monid `the-companies-api:/search_companies`.
2. `official-evidence`: quick web routine restricted to the company domain.
3. `firmographics`: Monid `apollo:/organizations/enrich`; fallback `pdl:/v5/company/enrich`.
4. `news`: Monid `akta:/v1/news`; fallback `context.dev:/news/search`.
5. `normalize`: preserve provider identities, contradictions, dates, and sources.

## Lead enrichment

1. `qualify-company`: company routine.
2. `find-role`: Monid `apollo:/mixed_people/api_search`; fallback `pdl:/v5/person/search`.
3. `resolve-person`: people routine.
4. `enrich-contact`: use the inspected routine endpoint only when contact data was explicitly requested.
5. `validate`: retain provenance and mark unverified contact fields; never infer missing values.

## Market

1. `define-category`: deep web routine.
2. `discover-vendors`: Monid company search plus G2, Capterra, and GetApp catalog searches.
3. `compare`: official sites first, then reviews and market sources.
4. `validate`: reconcile names, dates, prices, and contradictory claims.
5. `synthesize`: return comparison, evidence coverage, and unknowns.

## Technical

1. `official-docs`: quick web routine restricted to vendor documentation.
2. `source`: inspect repository, releases, changelog, and package metadata with native CLIs.
3. `issues`: inspect current upstream issues only when behavior remains unresolved.
4. `verify`: distinguish documented, source-present, and runtime-proven behavior.

## News

1. `discover`: Monid `akta:/v1/news`; fallback `context.dev:/news/search`.
2. `normalize-event`: separate publication time from event time.
3. `trace-origin`: retrieve the primary announcement or original reporting.
4. `corroborate`: require a second independent source for material claims.
5. `synthesize`: report chronology, conflicts, and source URLs.

## Deferred FlowMind integration

- Domains become FlowMind-selected overlays rather than more flat strategies.
- Each stage emits a normalized research/tool event and evidence reference.
- FlowMind subscribes by stage and injects selected evidence into downstream node context.
- The callback contract must define event type, selector, context budget, ordering, deduplication, failure behavior, and provenance.
- Until that exists, the agent carries stage outputs forward explicitly and must not claim automatic injection.
