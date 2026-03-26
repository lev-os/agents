# Cass Prompt Archetypes (Admin Cockpit)

This reference distills high-signal admin prompts from real session history into reusable templates.
Goal: reuse proven prompt structures, then adapt constraints and deliverables to the current repo.

## Mining Method

```bash
cass status --json && cass index --json
cass search "*" --workspace /data/projects/<repo> --aggregate agent,date --limit 1 --json
cass search "admin" --workspace /data/projects/<repo> --fields minimal --limit 80 --json \
  | jq '[.hits[] | select(.line_number <= 3)]'
```

Follow each hit:

```bash
cass view <source_path> -n <line_number> -C 20
```

## Archetype 1: Full Admin + Analytics Topology Scan

Use when: you need a complete map before planning changes.

Generalized prompt:

```text
Thoroughly explore the admin dashboard and analytics implementation in this Next.js project.

I need to understand:
1. Admin pages/routes and what each does.
2. Admin API routes and their payloads.
3. Analytics services and data sources.
4. Visualization/chart components.
5. Existing KPIs/metrics/features.
6. Data providers and query paths.

Be very thorough. List all admin-related files and what each does.
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/da9ad1fd-8156-40f0-9a18-8efe8872471e/subagents/agent-a754342.jsonl:1`

## Archetype 2: Cross-Repo Pattern Mining

Use when: importing proven admin patterns from sister repos.

Generalized prompt:

```text
Exhaustively research <repoA>, <repoB>, <repoC> for admin dashboard patterns.

Look for:
1. Admin auth + route protection
2. Dashboard layout/shell
3. Analytics and monitoring surfaces
4. Queue/action workflows
5. Health/ops views

Return detailed findings with file paths and reusable code patterns.
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/a5934f39-1b3b-4a18-8d52-c03fed683447/subagents/agent-ae84e71.jsonl:1`

## Archetype 3: Moderation Queue Build Prep

Use when: adding moderation queue flows to an existing admin system.

Generalized prompt:

```text
I need to implement an admin moderation queue page.

Please find and report:
1. Admin layout/nav structure.
2. Existing admin page pattern using client component + TanStack Query.
3. Query-key conventions for admin hooks.
4. Existing query hooks and toast/notification patterns.
5. Existing moderation routes and status models.

Provide file paths and relevant code patterns.
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/038a8514-2aaf-476d-90b9-c39dbf6d074f/subagents/agent-a0c14cb.jsonl:1`

## Archetype 4: API Route Inventory + Contract Mapping

Use when: you need route coverage and dependency mapping before refactor/testing.

Generalized prompt:

```text
Find all files related to /api/admin routes in this Next.js project.

I need:
1. Route files under src/app/api/admin/
2. Endpoint inventory by capability
3. Auth pattern each route uses
4. Service functions or DB queries each route calls
5. Existing integration tests so I avoid duplication

Return file paths and concise summaries.
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/14ca84d4-7d1e-46d7-b7af-c883cd152eb5/subagents/agent-afbb9c6.jsonl:1`

## Archetype 5: Broken Route Sweep (Consistency + Coverage)

Use when: hardening many admin routes at once.

Generalized prompt:

```text
Search for broken admin API routes in this Next.js codebase.

1. List ALL src/app/api/admin/**/route.ts files.
2. For each route, verify imports, schema references, response shape, and auth checks.
3. Cross-reference all fetch("/api/admin/") calls against route files.
4. Flag placeholders/simulated data/TODO implementations.

Return all issues with file path + line number, ordered by severity.
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/42f04754-ddfe-4828-9da6-0d7cbd4de542/subagents/agent-a3b46cf.jsonl:1`

## Archetype 6: Security + Audit Threat-Hunt

Use when: auditing privilege boundaries and audit integrity.

Generalized prompt:

```text
Deeply explore the admin and audit logging system in this codebase.

Investigate:
1. Admin authentication and authorization flow
2. Admin endpoint privilege boundaries
3. Audit event emission/query pipeline
4. RBAC implementation details

Trace imports and execution flow. Report concrete bugs:
- auth bypass
- missing audit on sensitive actions
- role escalation
- IDOR
- missing validation or unsafe query paths
```

Sources:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreysprompts-premium/d075f557-0af8-4168-bb5e-fba07eccb60f/subagents/agent-a1dcb0d.jsonl:1`
- `/home/ubuntu/.claude/projects/-data-projects-jeffreysprompts-premium/54ce73a2-354c-4d6d-ad51-54b0655d9cdb/subagents/agent-a55a8e0.jsonl:1`

## Archetype 7: World-Class Enhancement Plan Spec

Use when: you want a large, implementation-ready roadmap.

Generalized prompt:

```text
Design a world-class admin dashboard enhancement plan for this SaaS.

Current state:
- existing admin pages/features
- data sources/APIs
- DB tables
- UI stack and constraints

Deliver:
1. architecture plan
2. new API endpoints
3. reusable component structure
4. data-fetch/caching strategy
5. phased implementation plan
6. integration checklist and risk controls
```

Source:
- `/home/ubuntu/.claude/projects/-data-projects-jeffreys-skills-md/a5934f39-1b3b-4a18-8d52-c03fed683447/subagents/agent-ad03ab4.jsonl:1`

## Ritual Frequency Snapshot (Last ~180 days)

Computed with:

```bash
cass search "admin" --json --fields summary --days 180 --limit 600 \
  | jq '[.hits[] | select(.line_number <= 3 and .title != null) | .title]
        | group_by(.) | map({title: .[0], count: length}) | sort_by(-.count) | .[0:20]'
```

Most repeated prompt families:

- `Deep-audit the admin, webhook, and premium API routes...` (count: 3)
- `I need to understand the admin page patterns for building an admin moderation queue page...` (count: 3)
- `Read ALL of these admin API route files and produce a concise summary...` (count: 3)
- `Thoroughly explore the admin section ... to find broken functionality...` (count: 3)
- `Deeply explore the admin and audit logging system...` (count: 2)
- `Search for more broken admin API routes...` (count: 2)
- `Find all files related to /api/admin routes...` (count: 2)

Interpretation:
- Repeated high-count families are operating rituals.
- Default to these before inventing new prompt structures.
- Favor prompts that enforce path-backed findings and severity ordering.

## Normalization Rules (Before Reuse)

1. Replace repo/app names with placeholders.
2. Replace stack/version specifics with current project stack.
3. Keep output contract style: deliverables, acceptance criteria, severity ordering.
4. Preserve security wording for audit tasks (auth bypass, IDOR, escalation).
5. Keep route/path specificity when asking for inventory or sweeps.

## Prompt Quality Rubric

- Specific scope (`/admin`, `/api/admin`, services, hooks)
- Explicit deliverables (route map, risk list, phased plan)
- Execution constraints (line numbers, file paths, severity ordering)
- Action orientation (not just describe; identify gaps and remediation)
- Provenance (derived from repeated successful prompt families)
