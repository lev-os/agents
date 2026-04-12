# Feature Catalog (Deduplicated)

Canonical merge target for multi-repo admin systems.

## 1) Command Center
- Global shell + grouped nav
- Shared date/compare filters
- KPI strip with refresh/staleness
- Quick actions
- Section error boundaries

## 2) Users
- Search + advanced filters
- User 360 (activity/sessions/subscriptions/assets)
- Impersonation start/stop (TTL + banner + audit)
- Tier/beta/invite controls
- Manual account adjustments with reason

## 3) Billing & Finance Ops
- Subscriptions metrics (MRR/ARR/ARPU/churn/provider split)
- Refund queue (approve/reject/notes)
- Dunning + failed payment ops
- Payout/dispute dashboards
- Pricing/promotions/bulk gifts/affiliates
- Billing ledger + reconciliation

## 4) Support
- Inbox queues + assignee workflow
- Ticket workspace (comments + ownership)
- SLA metrics + breach alerts
- Request queue with transitions
- Feedback triage + issue creation

## 5) Moderation & Compliance
- Moderation queue + reason templates
- Compliance feed + resolution actions
- Feature/delist/relist controls
- Curator/candidate moderation queues
- AI-assisted anomaly/risk review

## 6) Content & Catalog Ops
- Catalog management (skills/prompts/content units)
- Detail editors (metadata/examples/relationships)
- Featured queue/scheduling/history
- Content quality/regression dashboards

## 7) Analytics & Projections
- Analytics hub + deep dives
- Revenue/acquisition/engagement/retention/path
- Demographic/geographic/payment analytics
- Runway/scenarios/Monte Carlo/break-even/unit economics

## 8) Experiments & Flags
- Feature flags + rollout metadata
- Experiment CRUD + variant weights
- Metrics/significance readouts
- Declare-winner/rollback/reset-weight actions

## 9) Operations
- Ops health (DB/queues/providers/external deps)
- Jobs monitor (status/lag/retry/error)
- Failed jobs queue + retry
- Webhook diagnostics/reprocessing
- Vendor/logistics/fulfillment ops (domain-specific)

## 10) Security & Audit
- Audit search/filtering
- Privileged-action provenance
- Guarded maintenance actions
- Provider health pages (payments/email/infra/cli)

## 11) Communications & Exports
- Announcements + segmented sends
- CSV/data exports
- Daily snapshots

## 12) AI Ops
- AI admin briefs/summaries
- Churn/anomaly risk queues
- AI-assisted prioritization (support/moderation)

## Prioritization Tiers
- Tier A: Command Center, Users, Billing/Finance Ops, Operations, Security/Audit
- Tier B: Support, Moderation/Compliance, Analytics/Projections, Experiments/Flags
- Tier C: Content/Catalog, Communications/Exports, AI Ops

## Scoring Rubric (0-3 each)
- Business impact
- Operational urgency
- Implementation effort (inverse)
- Dependency readiness

`Priority = impact + urgency + effort + readiness` (max 12)
- 10-12: immediate
- 7-9: next phase
- 0-6: backlog/prep

## Normalization Rules
- One canonical capability, one IA location.
- Prefer action queues over read-only dashboards.
- Every mutation maps to permission + audit.
