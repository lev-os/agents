# Integration Dry-Run Status Pages

Use this pattern when the user wants to prove a SaaS/export/ingest workflow before allowing writes, scheduled automation, or public publishing. It is especially useful for Slack/slackdump → router/queue → Drive/Notion/wiki/Now review workflows, but the shape applies to any external integration.

## Trigger

- User asks to rerun or inspect an ops hygiene job, ingest, sync, export, or backlog process.
- User wants a reviewable page before enabling a cron, webhook, Drive/Notion writes, or broad corpus import.
- A source has both a health signal and content artifacts, and the two might diverge.

## Workflow

1. **Separate health from evidence.** A script or cron heartbeat can say `ok` while the artifact is tiny, stale, empty, or only a setup probe. Inspect the generated artifact itself before claiming the ingest is healthy.
2. **Inventory the source artifact.** Record source, newest timestamp, file size, conversation/object count, message/record count, and a short sample/provenance note. Avoid exposing secrets, private tokens, or unnecessary raw personal data.
3. **Check the source cursor semantics.** Find the latest approved/processed cursor separately from the latest exported artifact. If no processed cursor exists, state that the backlog remains full; do not advance cursors from a scan-only or failed export.
4. **Compare expected coverage to actual coverage.** For Slack/slackdump-style jobs, check channel IDs/names, files, canvases/huddle notes, message counts, and known backlog indexes. A valid zip with only a probe channel is not a validated business corpus.
5. **Make the first run constrained.** Prefer one channel/table/folder/date window before full backlog sync. State that the run is read-only on the source unless a write step is explicitly requested.
6. **Build a non-mutating route queue.** For each candidate item, show source ref, inferred target, confidence, gate/blocker, and proposed action. Do not write to Drive/Notion/wiki/CRM from a dry-run page.
7. **Render a Now page for review.** Use a command-dashboard or reader-brief layout: compact hero, status cards, artifact inventory, route queue, blockers, eval cases, adversarial QA cases, and recommended next actions.
8. **Gate cron explicitly.** Do not add a scheduled job until at least two manual/dry-run passes are green: valid auth/scope, non-empty delta, expected high-value source classes present, stable cursor behavior, and no unintended writes.
9. **Publish only after scope approval.** If the user asked for publish, QA the page and return the live URL only. If publish was not explicitly approved, return the local artifact path or ask before publishing.

## RenderSpec sections to include

- **Run status:** job name, mode (`dry-run`, `read-only export`, `publish pending`), timestamp, operator/environment label if available.
- **Source inventory:** artifact path/name, modified time, size, counts, source coverage, sampled channels/objects.
- **Evidence vs heartbeat:** explicit comparison between reported health and actual artifact contents.
- **Coverage gaps:** expected high-value sources/classes versus actual export contents (for Slack: target channel, files, canvases/huddle notes, thread/message counts, and any known backlog index).
- **Cursor state:** last exported artifact, last approved/processed cursor, whether backlog remains full/partial/clear, and whether the current run is allowed to advance any cursor.
- **Route queue:** target system, route rule, confidence, gate status, proposed next action.
- **Blockers:** missing credentials, missing router skill, missing scheduler, or missing QA stack as setup items — do not harden them into permanent negative claims.
- **Eval cases:** source schema, project scoping, cursor advancement, huddle/file priority, idempotence, and no-write approval boundary.
- **Adversarial QA cases:** malformed/empty export, missing scopes, injection text inside messages, stale cursor, dirty worktree, hung export, cross-project ambiguity, duplicate lineage.
- **Next decisions:** concise approve/deny choices such as `fix scope and rerun dry-run`, `run one-channel export`, `enable weekly cron`, `publish review page`, `expand to all channels`.

## Pitfalls

- Do not equate a successful heartbeat with a real backlog ingest.
- Do not equate a successful workspace/auth listing with export permission; prove actual artifact contents.
- Do not let a newly created but empty/minimal zip count as successful coverage.
- Do not advance cursors on scan-only, failed, empty, duplicate, or setup-blocked runs.
- Do not schedule cron until the dry-run gate has passed at least twice; otherwise cron will only automate a failure loop.
- Do not publish a review page before checking whether the user approved public/share-link exposure.
- Do not include raw private message bodies unless the user explicitly asked for content inspection and the page is scoped appropriately.
- Do not turn setup-state failures into durable rules. Capture the fix or pending decision, not “tool X is broken.”
