# Admin Cockpit Checklist

## Preflight
- [ ] Inventory `/admin` pages + `/api/admin` endpoints.
- [ ] Document permission model + roles.
- [ ] Document audit model + gaps.
- [ ] Map capabilities to canonical domains.

## Design
- [ ] Single IA; no duplicate sections.
- [ ] Shared admin primitives defined.
- [ ] Query-key/hook boundaries defined.
- [ ] Mutation contract template agreed.

## Backend
- [ ] Permission checks on all mutations.
- [ ] Zod schemas for body/query params.
- [ ] `reason` required for high-risk actions.
- [ ] Audit emission for privileged actions.

## Frontend
- [ ] Consistent shell/nav across sections.
- [ ] Queue/action flows for operator work.
- [ ] Consistent search/sort/filter/pagination.
- [ ] Freshness + error states visible/actionable.

## Quality
- [ ] API tests for auth/permissions/transitions.
- [ ] E2E smoke for `/admin` + one critical mutation.
- [ ] Lint, typecheck, tests pass.
- [ ] No parallel admin systems added.

## Launch Readiness
- [ ] Runbook for critical flows.
- [ ] Rollback path for risky actions.
- [ ] Monitoring/alerts for admin job failures.
- [ ] Operator feedback loop in place.

## DoD (Per Slice)
- [ ] End-to-end operator path works.
- [ ] Privileged actions are permission-protected + audited.
- [ ] Empty/loading/error/stale states handled.
- [ ] Freshness timestamps shown where needed.
- [ ] Long-term owner assigned.

## Red Flags (Stop and Fix)
- [ ] Duplicate capability introduced.
- [ ] High-risk mutation lacks reason + audit.
- [ ] Data-grid behavior inconsistent with rest of admin.
- [ ] Operational page lacks retry/escalation controls.
- [ ] Risky action has no rollback path.
