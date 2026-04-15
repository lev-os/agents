# Templates (Copy/Paste)

## 1) Unified Route Map
```md
# Admin Route Map
- /admin
- /admin/users
- /admin/users/[id]
- /admin/billing
- /admin/support
- /admin/moderation
- /admin/content
- /admin/analytics
- /admin/experiments
- /admin/operations
- /admin/compliance
- /admin/health
```

## 2) Permission Matrix
```md
| Domain | Action | Permission | Roles | Notes |
|--------|--------|------------|-------|-------|
| users | read | users.read | support, admin | list/detail |
| users | impersonate | users.impersonate | super_admin | audited + TTL |
| billing | refund | billing.refund | finance_admin | reason required |
| moderation | action | moderation.action | moderator, admin | reason templates |
| ops | retry | ops.retry | admin | retry guardrails |
```

## 3) Endpoint Contract
```md
## POST /api/admin/<domain>/<action>

### Request
- auth: admin + `<domain>.<action>`
- Zod body: `targetId`, `reason` (high-risk required), `metadata?`

### Success
- `ok: true`
- `data: { ...canonical state... }`
- `meta: { requestId, serverTime }`

### Errors
- `UNAUTHORIZED`, `FORBIDDEN`, `VALIDATION_ERROR`, `CONFLICT`, `INTERNAL_ERROR`
```

## 4) Audit Taxonomy
```md
| Event | Actor | Target | Required Fields |
|-------|-------|--------|-----------------|
| user_impersonation_started | admin | user | reason, expiresAt |
| refund_approved | admin | refund | reason, amount |
| moderation_action_applied | moderator | entity | action, reason |
| job_retry_triggered | admin | job_run | reason |
| experiment_winner_declared | admin | experiment | winner, reason |
```

## 5) Vertical Slice Plan
```md
## Slice: <name>

### Scope
- UI:
- API:
- Schema:

### Risks
- authorization:
- data integrity:
- operational:

### Acceptance Criteria
- [ ] happy path
- [ ] permission denial
- [ ] audit emission
- [ ] stale/error handling
- [ ] test coverage
```

## 6) Queue State Machine
```md
States: pending, in_review, blocked, resolved

Transitions:
- pending -> in_review (assign)
- in_review -> blocked (needs info)
- in_review -> resolved (action complete)
- blocked -> in_review (info received)

Rules:
- only authorized roles transition
- each transition emits audit event
- terminal transitions require reason
```
