---
name: skill-discovery
description: "Use when a task, agent brief, UX route, CDO plan, wave, or sprint needs relevant local skill material, or when selected material's applicability and loading must be checked."
skill_type: tool
category: process-find
primary_primitive: get
legacy_aliases: [discover-skills]
---

# Skill Discovery

Run this campaign before using discovered local skills or corpus material as task context. Keep project-local instructions under their own authorized project route; they are not corpus search results.

## Frame the task and source scope

1. Reduce the request to the task and outcome, topic, platform, material form, constraints or failure modes, and useful names, aliases, and tags. State which sources are in scope, the effective namespace, any physical collection filter, and what evidence would make the selected material sufficient for this task.
2. Keep semantic subject navigation separate from physical collection filters. Use `tree --view subjects|collections` to find navigation nodes. Pass a returned node ID to `browse`; pass a physical collection name to `--category`. For a corpus-only search, use `--namespace skills-db`; select `skills` or `_repos` only when that source scope is part of the request.
3. Select `--backend qmd` for hybrid search over `skills-db`. Select `--backend lexical` for installed `skills`, `_repos`, or a declared lexical comparison. The default remains lexical. Record the selected backend. If QMD is stale or unavailable, report its repair frontier; do not silently switch backends.

**Check:** The task brief names the needed outcome, search facets, source scope, and a task-specific sufficiency condition before results are judged.

## Start browse and query together

Launch a browse track and an initial query together. Keep both active, share useful nodes and terms across them, and let each continue while the other runs. When either returns a candidate that plausibly addresses a framed task facet within the authorized scope, load it immediately using the next section before waiting for query five or treating query-count or overlap requirements as complete. Keep the other track and remaining useful queries active during that load. A first hit never closes the campaign.

Use tree and browse to map relevant subject or collection branches and paginate descriptor results where needed:

```bash
lev-skills tree --view subjects --depth 3 --json
lev-skills tree --view collections --depth 3 --json
lev-skills browse --node <node-id> --limit 20 --json
lev-skills browse --cursor <token> --json
```

Use `discover` for distinct task questions. Start with one useful predicate so an early result can be loaded promptly. Replace these query forms with the current task's concrete terms; add `--tags <csv>` or `--category <physical-collection>` only when those filters change the requested scope. Repeated `--query` arguments are supported. Batch them only if the host lets you act on the first useful result before all groups finish; otherwise issue separate query steps:

```bash
lev-skills discover --query "skill-discovery lev-skills" --backend qmd --namespace skills-db --limit 5 --no-cache --json
```

The initial command shows an exact anchor or alias. Continue with distinct follow-up questions from other useful families, such as task outcome (`"choose local guidance for an agent task"`), mechanism or form (`"browse collections query source descriptors"`), constraint or failure (`"stale index cache replay unresolved source"`), and lateral use (`"agent prompt context skill package references"`). Repeating a query argument does not itself make its predicate distinct.

Treat the `--limit` value as a result-display bound, not a query-count or coverage guarantee. A browse page contains resource descriptors; its cursor paginates resources, not source lines or file bytes. Use any available filesystem inspection only to diagnose weak or unavailable corpus evidence. Record that inspection as supplementary evidence; it does not count as a completed public query.

**Check:** Browse and query began together, findings crossed between them while both remained active, and the first useful candidate started its full source load before query-count or overlap closure. If the host cannot establish concurrent execution and cross-feed, keep overlap unverified and the campaign incomplete.

## Load the first useful source while both tracks run

As soon as either track returns a candidate that plausibly addresses a framed task facet within the authorized scope, capture its descriptor and begin a full local read. Start this action before waiting for the fifth predicate or treating query-count or overlap requirements as complete, while the other track and remaining useful queries continue. This early load helps assess applicability; it does not close the campaign or waive its query and overlap requirements.

If the returned result lacks a path or digest needed for the read, obtain the descriptor early with optional `get` by returned source ID or exact name when available. `get` returns descriptors only; it does not load content. Never invent a path or digest. If no actual source path and digest can be established, retain the candidate as unresolved and keep discovery open.

For every candidate used as context, retain the returned `source_id`, `local_path`, `realpath`, `digest`, `index_revision`, and available bundle, relationship, extraction, and availability diagnostics. `matches` items and tree or browse results identify resources; they do not deliver full source bytes. Open the complete source through its returned actual path, read to EOF, and verify the bytes against the returned digest. Direct path loading is valid without a `get` call.

Follow required local references and bundle members from their declared file or package base. Read and verify the full required local closure before using a package as context. Keep headerless and standalone files visible with their actual roles; record missing, ambiguous, unavailable, and external dependencies as unresolved. A path that exists, a preview, a descriptor, or a source mention does not establish complete loading or applicability. Do not execute bundled scripts or fetch external dependencies as an automatic lookup step.

Assess applicability from the loaded content against the framed task. Keep selection, applicability, full loading, injection, observed use, and task outcome as separate claims. Authored status, maturity, provenance labels, and runtime claims in a source remain unverified until their own evidence is observed.

**Check:** The first useful source has a digest-verified full read and required local reference or bundle closure before query-count or overlap closure, with both tracks still active. Missing descriptors remain unresolved rather than fabricated.

## Count completed query evidence

Complete at least five distinct matching predicates across at least two substantive strategy families, such as exact anchors or aliases, task and outcome language, domain or platform terms, mechanism or form, and constraints or failure modes. Each query must ask a useful question or change a meaningful filter. Whole-request sentences, cosmetic paraphrases, reordered or repeated terms, retries, and ranking variants do not create new predicates.

Use the currently available host-observed execution record, or a controller record when the active host provides one, alongside each returned query group's `evaluated`, `evaluation_origin`, `status`, normalized matching/ranking fingerprints, and index revision. Bind each group to its observed execution ID and timing; query arguments, planned calls, and group declarations alone do not establish an execution. Count a group only when an observed execution ID is bound to it, `evaluated=true`, its origin is verified as a fresh `cli_evaluation` or `qmd_query`, its terminal status is `ok` or `empty`, and its normalized matching predicate is distinct within the frozen campaign scope and index revision. Switching backends does not create another predicate, even when the matching fingerprint changes. If the origin or binding is unclear, leave the group uncounted and unverified. `evaluated=false`, cache replay, timeout, cancellation, malformed or invalid input, stale index, failed or nonterminal outcomes, retries, and unobserved plans or calls do not count. A ranking fingerprint change alone does not make a new predicate. Strategy labels alone do not prove useful diversity or overlap.

Use host-observed browse and query timings to verify that their execution intervals overlap, and record an observed result handoff between the tracks while both are active. A plan or two concurrent labels do not prove overlap. An evaluated `empty` group is query evidence, not proof that the corpus lacks a relevant source. If this host exposes no suitable execution IDs, timings, or result handoff, report the missing observation and keep counts, overlap, or the campaign unverified/incomplete. Ordinary caller completion may use the current host's qualifying observations; later S06 certification is a separate gate, not a prerequisite for operating or completing the caller campaign. Source delivery, applicability, concrete use, outcome, and independent evidence remain separate; S06 runtime certification stays pending until its owner measures it.

**Check:** Current host/controller records bind at least five distinct evaluated groups across two useful strategy families, and observed timings plus result handoffs establish browse/query overlap before campaign completion. Keep the campaign incomplete when the required observation is unavailable; report later S06 certification separately.

## Reuse, errors, and stops

Reuse a completed campaign only when task focus, outcome, effective constraints and scope, index revision, source digests and required closure, and sufficiency remain applicable. Reuse adds no new query executions. Reopen discovery when focus, constraints, index or source revision, coverage, or sufficiency changes; preserve earlier observations without silently combining incompatible revisions.

When reusing or reopening for a wave, node, or worker spawn, keep the caller's remaining wave/node, no-progress, and wall-clock budgets, assigned roles or seats, skill-count bounds, and injection rules in force. Discovery cannot reset or expand them. Inject only sources whose full required closure remains digest-verified and whose content remains applicable to that exact node or worker. If the remaining caller budget cannot reach sufficiency, stop incomplete with observations and the caller's resume frontier.

Continue beyond five when results remain irrelevant, empty, ambiguous, or insufficient and useful questions or branches remain. Stop on cancellation, time or budget limits, unavailable evidence, or an owner-bound error with observations and a concrete resume frontier. Five empty searches never prove global absence; scope any negative result to the inspected branch, queries, and recorded revision.

Preserve `stale_index` as an error and name the index or source-owner repair frontier. `--no-cache` bypasses cache use; it does not repair source staleness. Do not turn stale, invalid, failed, or unavailable results into empty results or absence claims. Keep stderr and structured failure evidence visible. Plain `lev-skills inventory --json` is a read-only view; explicit rebuild, usage, or provider writes stay with their own authorized owner and are not automatic lookup fallbacks.

**Check:** The result states whether the task-specific sufficiency condition was met, what was fully loaded and applicable, what remains unresolved, and whether the campaign ended complete or incomplete. Never claim live use, product outcome, or runtime certification from these instructions alone.
