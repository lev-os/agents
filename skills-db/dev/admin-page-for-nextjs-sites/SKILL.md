---
name: admin-page-for-nextjs-sites
description: >-
  Design cohesive Next.js SaaS admin cockpits. Use when building or expanding `/admin` and `/api/admin` with unified IA, permissions, audit, analytics, ops, moderation, billing, and user-management.
---

<!-- TOC: Core | Use When | Exact Prompts | Quick Start | Workflow | Invariants | Deliverables | Anti-Patterns | References -->

# Admin Page for Next.js Sites

## Use When
- Building a new Next.js admin console.
- Expanding `/admin` without duplicating capability.
- Merging multiple admin systems into one cockpit.
- Hardening privileged flows (refunds, moderation, impersonation, retries).

## THE EXACT PROMPTS

### 1) Build/Expand
```text
Design and implement a cohesive admin cockpit for this Next.js SaaS codebase.

Requirements:
1. Inventory `/admin` pages, APIs, permissions, data sources, jobs.
2. Build a harmonized IA (Overview, Users, Billing, Support, Moderation, Content, Analytics, Experiments, Operations, Compliance, Health).
3. Integrate non-duplicative features via shared primitives (shell, filters, tables, permissions, audit, response envelope).
4. Implement vertical slices with explicit acceptance criteria and no parallel systems.
5. Add tests for high-risk mutations and operator flows.

Output:
- route map, API/contracts plan, data model deltas
- phased rollout plan + concrete code changes
```

### 2) Consolidation/Audit
```text
Audit this Next.js admin system for fragmentation, risk, and missing operator workflows.

Return:
1. Overlapping capabilities to merge.
2. High-risk endpoints missing permission + audit controls.
3. Read-only dashboards that should become action queues.
4. Missing operational controls (job retries, provider health, stale-data indicators).
5. Prioritized remediation slices with acceptance criteria.
```

### 3) Security + Audit Deep Dive
Use `references/CASS-PROMPT-ARCHETYPES.md` (Archetype 6).

### 4) Admin API Integrity Sweep
Use `references/CASS-PROMPT-ARCHETYPES.md` (Archetype 5).

### 5) Moderation Queue Slice Prompt
Use `references/CASS-PROMPT-ARCHETYPES.md` (Archetype 3).

### 6) Cross-Repo Pattern Mining Prompt
Use `references/CASS-PROMPT-ARCHETYPES.md` (Archetype 2).

### 7) World-Class Enhancement Plan Prompt
Use `references/CASS-PROMPT-ARCHETYPES.md` (Archetype 7).

## Cass Grounding Loop (Use Before Large Admin Work)
```bash
cass status --json && cass index --json
cass search "*" --workspace /data/projects/<repo> --aggregate agent,date --limit 1 --json
cass search "admin" --workspace /data/projects/<repo> --fields minimal --limit 80 --json \
  | jq '[.hits[] | select(.line_number <= 3)]'
# Follow best hits:
cass view <source_path> -n <line> -C 20
```
- Treat repeated prompt families as operating playbooks.
- Reuse real prompt skeletons, then generalize names/paths/constraints.
- Prefer prompts with explicit deliverables, acceptance criteria, and bug-report format.

## Quick Start
```bash
rg --files src/app | rg '/admin|api/admin'
rg -n "requireAdmin|isAdmin|permission|audit|role" src
rg -n "job|queue|retry|webhook|health" src/app src/lib src/services
# Build EXISTING/PARTIAL/MISSING map via FEATURE-CATALOG
# Start with shell + permissions + audit + query patterns
```

## Workflow (Harmonization)
1. **Mine cass first**: collect 3-5 relevant prompt archetypes; adapt, do not invent blindly.
2. **Map state**: pages/APIs/mutations/permissions; tag `EXISTING|PARTIAL|MISSING`.
3. **Define IA once**: one route tree, grouped nav, no parallel sections.
4. **Shared primitives**: `AdminShell`, filters/date range, cards/toolbars, table primitives.
5. **Unified contracts**: response envelope, error codes, validation.
6. **Permissions**: domain-action keys (`users.read`, `billing.adjust`, `ops.retry`) at page/API boundaries.
7. **Audit high-risk actions**: actor/action/target/reason/before-after/request-context.
8. **Operator workflows first**: queues + transitions, not chart-only pages.
9. **Observability**: jobs, failed queues + retry, provider health, freshness timestamps.
10. **Vertical slices**: Foundation -> Users -> Billing/Ops -> Support/Moderation -> Analytics/Experiments -> Content/Comms.
11. **Harden before breadth**: integration/E2E for dangerous flows.

## Hard Invariants
- **One admin shell** (single nav + context).
- **One permission registry** (no ad-hoc inline checks).
- **One audit pipeline** (all privileged mutations).
- **One query-key strategy** (central keys + TanStack hooks).
- **One mutation contract** (validated input, deterministic responses).
- **One ops model** (status, retries, last error for async jobs).

## Deliverables
- Unified route map.
- Permission matrix by domain/action.
- Admin API contract map (read + mutation).
- Audit event taxonomy.
- Phased rollout with acceptance criteria.
- Test plan for high-risk flows.

## Anti-Patterns
- Many dashboards, few actions.
- Duplicate capability under different section names.
- UI-only auth checks without API enforcement.
- Privileged mutations without reason + audit.
- Ad-hoc fetches instead of shared query hooks.
- Breadth expansion before foundation hardening.

## References
- Feature inventory: [FEATURE-CATALOG.md](references/FEATURE-CATALOG.md)
- Architecture blueprint: [IMPLEMENTATION-BLUEPRINT.md](references/IMPLEMENTATION-BLUEPRINT.md)
- Phased rollout: [PHASED-ROLL-OUT.md](references/PHASED-ROLL-OUT.md)
- Build/review checklist: [CHECKLIST.md](references/CHECKLIST.md)
- Copy-paste templates: [TEMPLATES.md](references/TEMPLATES.md)
- Failure modes: [FAILURE-MODES.md](references/FAILURE-MODES.md)
- Operator UX standards: [OPERATOR-UX-STANDARDS.md](references/OPERATOR-UX-STANDARDS.md)
- Cass prompt archetypes: [CASS-PROMPT-ARCHETYPES.md](references/CASS-PROMPT-ARCHETYPES.md)

## Reference Index

| Need | Open |
|------|------|
| Capability map | [FEATURE-CATALOG.md](references/FEATURE-CATALOG.md) |
| Architecture | [IMPLEMENTATION-BLUEPRINT.md](references/IMPLEMENTATION-BLUEPRINT.md) |
| Rollout | [PHASED-ROLL-OUT.md](references/PHASED-ROLL-OUT.md) |
| Quality gates | [CHECKLIST.md](references/CHECKLIST.md) |
| Templates | [TEMPLATES.md](references/TEMPLATES.md) |
| Failures | [FAILURE-MODES.md](references/FAILURE-MODES.md) |
| Operator UX | [OPERATOR-UX-STANDARDS.md](references/OPERATOR-UX-STANDARDS.md) |
| Cass archetypes | [CASS-PROMPT-ARCHETYPES.md](references/CASS-PROMPT-ARCHETYPES.md) |
