# Phased Rollout Plan

## Phase 0: Foundation
- Deliver: shell/nav, permission helpers, audit helpers, shared filters/tables, query-key conventions.
- Accept: existing routes still work; new primitives reused in real section.

## Phase 1: Users + Access Ops
- Deliver: users list/filter/detail-360, impersonation start/stop (TTL banner + audit), tier/beta toggles.
- Accept: all mutations permission + audit protected; impersonation lifecycle has E2E happy path.

## Phase 2: Billing + Finance Ops
- Deliver: subscriptions dashboard, refund queue, failed payment/dunning queue, optional disputes/payouts.
- Accept: billing mutations require reason + audit; approve/reject/refund transitions tested.

## Phase 3: Operations + Health
- Deliver: jobs monitor, failed queue + retry actions, ops health panel, provider health pages.
- Accept: failures diagnosable/retriable without SQL; freshness/staleness visible.

## Phase 4: Support + Moderation + Compliance
- Deliver: support inbox + tickets + SLA, moderation queues/actions, compliance feed + resolution workflow.
- Accept: queue actions audited; transitions server-validated.

## Phase 5: Analytics + Experiments
- Deliver: analytics hub/deep-dives, feature flags, experiment CRUD, winner/rollback/reset workflows.
- Accept: no duplicate analytics endpoints; experiment actions include provenance + rollback.

## Phase 6: Content + Communications
- Deliver: content/catalog admin, featured queue/scheduler, announcements + exports.
- Accept: editorial/comms workflows use the permission + audit model.

## Release Discipline (Each Phase)
1. Schema + migrations first.
2. API + permission/audit second.
3. UI consumes real APIs.
4. Tests (API + targeted E2E).
5. Lint/typecheck/tests green before merge.

## Dependency Guardrails
- Phase 1+ depends on real Phase 0 primitives.
- Mutation phases require audit wiring before merge.
- Queue phases require explicit transition validation.
- Analytics phases require freshness metadata.

## Slice Exit Criteria
A slice is complete only when UI + APIs + permissions + audit + tests all land.
