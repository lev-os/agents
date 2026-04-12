# Failure Modes and Mitigations

1. **Fragmented IA**: same capability in multiple sections. Mitigate with one canonical route map and single ownership.
2. **Dashboard-only admin**: metrics without remediation actions. Mitigate with queue/action workflows and explicit transitions.
3. **Missing provenance**: privileged changes with no actor/why trace. Mitigate with mandatory audit fields (actor, reason, before/after, request context).
4. **Permission drift**: UI hides actions but API allows them. Mitigate with central permission registry and server/API enforcement.
5. **Stale ops data**: operators act on old status. Mitigate with freshness timestamps, stale indicators, bounded polling, manual refresh.
6. **Schema/UI mismatch**: UI ships before migrations. Mitigate with migration-first slices and API contract tests.
7. **No rollback path**: risky action cannot be reversed quickly. Mitigate with per-action rollback plan and idempotency where practical.
8. **Inconsistent table UX**: different filter/pagination semantics across sections. Mitigate with shared table/filter primitives and global list conventions.
