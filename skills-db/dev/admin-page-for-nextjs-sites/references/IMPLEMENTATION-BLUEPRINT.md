# Implementation Blueprint (Next.js Admin Cockpit)

## 1) Frontend Architecture

### Route + Layout
- App Router admin group:
  - `src/app/(app)/admin/layout.tsx`
  - `src/app/(app)/admin/page.tsx`
- Nav sections: Overview, Users, Billing, Support, Moderation, Content, Analytics, Experiments, Operations, Compliance, Health

### Shared UI Primitives
- `AdminShell`
- `AdminFiltersBar` (date/environment/saved filters)
- `MetricCard`, `StatusPill`, `InlineError`, `SectionCard`
- `AdminDataTable` (search/filter/sort/pagination/bulk actions)

### Data Fetching
- Central query keys (`queryKeys.admin.*`)
- Domain hooks (`use-admin-users.ts`, etc.)
- Polling only on ops/jobs/health surfaces

## 2) API Contract Model

### Read endpoints
- Uniform filtering/sorting/pagination
- Freshness metadata (`asOf`, `generatedAt`) where relevant

### Mutation endpoints
- Zod validation
- Permission check by domain/action
- `reason` required for high-risk actions
- Audit emission with before/after context
- Deterministic response/errors

## 3) Permission Model

Examples:
- `users.read`, `users.update`, `users.impersonate`
- `billing.read`, `billing.refund`, `billing.adjust`
- `support.read`, `support.assign`, `support.resolve`
- `moderation.read`, `moderation.action`
- `ops.read`, `ops.retry`, `ops.reprocess`
- `experiments.read`, `experiments.write`, `experiments.declare_winner`

Rules:
- Enforce on API handlers and server loaders
- No inline role branching in presentational components

## 4) Audit & Provenance

Capture:
- actor id/email
- action type
- target entity id/type
- reason
- before/after snapshot or diff
- request context (ip/user-agent/requestId)
- timestamp

Mandatory flows:
- refunds/payment overrides
- impersonation start/stop
- moderation actions
- experiment winner/rollback
- bulk exports/announcements

## 5) Data Model Extensions (as needed)

Typical tables:
- support tickets/messages/sla events
- feature flags/experiments/assignments
- payout/dispute/billing events
- job runs/failures
- announcements
- compliance events/provenance
- analytics daily snapshots

Use materialized views/snapshots for heavy rollups.

## 6) Queue-Oriented UX

Action-heavy domains should expose:
- states (`pending`, `in_review`, `blocked`, `resolved`)
- ownership (`assignee`)
- SLA timers
- batch-safe actions

Prefer queues over dashboard-only pages.

## 7) Operational Reliability

- Jobs panel: last/next run, status, duration, error
- Failed queue: guarded retry single/retry all
- Provider health: status + degradation notes
- Freshness + stale indicators everywhere

## 8) Testing Strategy

Minimum:
- API auth/permission tests for all mutations
- Queue transition tests
- E2E smoke for `/admin`, `/admin/users`, one high-risk flow
- UI smoke screenshots for key surfaces

## 9) Delivery Strategy

Vertical slices only; each includes:
- page(s)
- API(s)
- permission checks
- audit events
- tests

Do not merge page-only slices.

## 10) Recommended Module Layout

```text
src/
  app/(app)/admin/
    layout.tsx
    page.tsx
    users/
    billing/
    support/
    moderation/
    analytics/
    operations/
  app/api/admin/
    users/
    billing/
    support/
    moderation/
    analytics/
    jobs/
    health/
  components/admin/
    shell/
    tables/
    filters/
    cards/
  hooks/queries/
    use-admin-users.ts
    use-admin-billing.ts
    use-admin-jobs.ts
  lib/admin/
    permissions.ts
    audit.ts
    contracts.ts
```

## 11) Endpoint Rules

- List endpoints: `page`, `pageSize`, `sort`, `order`, `q`, typed filters; response with `items`, `total`, `page`, `pageSize`.
- Mutation endpoints: idempotency key when practical, mandatory `reason` for destructive/financial actions, return canonical post-mutation state.

## 12) Query Key / Cache Discipline

- Namespace keys by domain (`users.*`, `billing.*`, `jobs.*`)
- Domain-level invalidation after mutations
- Polling only on operational pages
