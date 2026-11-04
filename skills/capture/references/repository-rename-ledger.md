# Repository rename inventory ledger

Use this pattern when asked to assess a naming migration and create a YAML ledger before making rename edits.

## Preconditions

1. Inspect repo-local routing/operating instructions and identify the repository's current canonical name, paths, and existing migration register.
2. Search both structural identifiers (paths, config keys, package/module names) and content references. Do not infer the requested spelling from one of those alone.
3. If the requested target spelling conflicts with the established in-repo canonical target, stop before any rename. Record the conflict as an explicit decision gate.

## Inventory buckets

Keep counts and entries distinct; a text hit count is not necessarily a rename obligation.

- `structural`: tracked paths, configuration keys, routing maps, module/package identifiers, automation/skill references.
- `live_content`: active operational docs and owned metadata that should change after the target is approved.
- `historical_or_evidence`: dated reports, source receipts, citations, immutable exports, and task IDs; preserve unless a separately approved remediation requires change.
- `external_identity`: domains, email addresses, SaaS workspaces, Drive/Notion/Slack identifiers, and brand assets; require external-system cutover evidence rather than blind repository edits.
- `binary_or_office`: DOCX/XLSX/PDF or embedded XML results; report separately and inspect their role before modifying.
- `ignored_or_runtime`: untracked/ignored artifacts; report scope but do not treat them as tracked rename work.

## YAML minimum contract

```yaml
schema_version: 1
ledger_id: <stable-id>
status: inventory_complete_target_name_confirmation_required | ready_for_execution
created_at_utc: <UTC timestamp>
target_name_decision:
  requested_in_current_session:
    display_name: <name>
    internal_key: <key>
  existing_repo_canonical:
    display_name: <name>
    internal_key: <key>
  evidence: []
  gate: confirmation_required | confirmed
scope_exclusions: []
inventory:
  structural: []
  live_content: []
  historical_or_evidence: []
  external_identity: []
  binary_or_office: []
  ignored_or_runtime: []
execution_gates: []
verification: []
```

## Verification

- Parse the YAML with an available parser.
- Verify required inventory categories and the target-name decision are present.
- Inspect `git status`/diff to confirm the only change is the requested ledger until the decision gate is resolved.
- Report structural counts separately from content-hit counts and external dependencies.

## Pitfalls

- Do not rename an established target merely because a user used a near-match spelling once.
- Do not use global text-replace for historical evidence, opaque IDs, URLs, or embedded Office XML.
- Do not claim a migration is complete because the legacy directory disappeared; configuration, operational docs, and external identity can remain.
