# Interfaces and operating contract

```mermaid
sequenceDiagram
    participant JP as JP / phone
    participant Relay as Lev Relay (this Codex chat)
    participant CLI as relay CLI
    participant Session as Claude / OMO / OMP session
    participant Schedule as Codex heartbeat
    participant Parent as Parent lev
    Parent-->>Relay: Optional setup / semantic catalog
    JP->>Relay: List / find / select / summary / trace
    Relay->>CLI: Exact machine + agent + session; local cursor
    CLI->>Session: Read permitted main-session JSONL
    Session-->>CLI: Complete records
    CLI-->>Relay: Sanitized prose + next cursor + omission notices
    Relay-->>JP: Delta in this same chat
    Schedule->>Relay: Requested bounded wake (default 15m / explicit 5m)
    Relay->>CLI: Scheduled wake / activity / expiry check
    CLI-->>Relay: Delta or idle/expiry pause action
    Relay->>Schedule: Pause after idle 15m / expiry
    JP->>Relay: Explicit approval of exact steering text
    Relay->>Session: Supported verified control route, once
    Session-->>Relay: Verified receipt or uncertain (no retry)
```

## Verified source contracts (Studio, 2026-10-01)

| Adapter | Installed product | Permitted source / documented interface |
|---|---|---|
| Claude | Claude Code 2.1.285 | `~/.claude/projects/<project>/<session-id>.jsonl`; `CLAUDE_CONFIG_DIR` override. Official Agent SDK `list_sessions` / `get_session_messages` is a possible future SDK adapter, not required or installed here. |
| OMO | `omo-ai` 5.1.3, native `@code-yeongyu/senpi` 2026.9.29-4 | `~/.omo/agent/sessions/**/*.jsonl`; `OMO_CODING_AGENT_DIR`, `SENPI_CODING_AGENT_DIR`, then `PI_CODING_AGENT_DIR` override. Session header + entry IDs/parent IDs. This is not the OpenCode edition. |
| OMP | `@oh-my-pi/pi-coding-agent` 18.4.4 | `~/.omp/agent/sessions/**/*.jsonl`, `~/.omp/profiles/<profile>/agent/sessions`; `PI_CONFIG_DIR`, `PI_CODING_AGENT_DIR`, `PI_CODING_AGENT_SESSION_DIR`, or explicit session-dir roots. Default FileSessionStorage; SQL storage excluded. |

Local package source references verified during discovery:

- `~/.bun/install/global/node_modules/omo-ai/plugin/skills/coding-agent-sessions/`:
  existing discovery/export knowledge, but its unrestricted finder can include
  Codex/hidden databases. Do not invoke that broad finder for this task.
- `~/.bun/install/global/node_modules/@code-yeongyu/senpi/docs/session-format.md`
  and `docs/rpc.md`: versions 1/2/3, `get_entries(since)`, `get_state`, classic
  stdio RPC and multi-session routing. A durable session ID differs from an
  ephemeral RPC routing handle. Closing the last attachment can park/close a
  runtime; resume/send/exit is not a universal safe monitor-preserving operation.
- `~/.bun/install/global/node_modules/@oh-my-pi/pi-coding-agent/src/session/`:
  title slot before header is mutable, entry IDs/parent IDs form append-order
  tree history. `modes/rpc/rpc-types.ts` supports prompt, get_state, get_entries,
  acknowledgment and prompt_result. No takeover is permitted by this skill.
- [Official Claude session SDK](https://code.claude.com/docs/en/agent-sdk/python#get_session_messages)
  and [session management](https://code.claude.com/docs/en/agent-sdk/sessions).

Session files are read only. No SessionManager constructors are used: opening
through them can migrate or create directories. No raw exports, system prompts,
thinking, tool inventory/arguments/results or credentials are emitted. Source
ownership and permission are required; explicit source paths are not authority
to override a denied path. `safe_path` refuses Codex/SSH/AWS/credential locations.

## Cursor and activity

The opaque v1 cursor contains a hash of machine/agent/profile/full session ID,
stable entry ID, record fingerprint and character continuation offset. It is
validated against complete records on every read. It survives inode rotation
and metadata title-slot rewrites when its anchor survives unchanged. Truncation
or editing that removes/changes the anchor produces an explicit gap, with no
silent skip or replay. The caller then chooses replay or a new binding.

Trailing partial JSON is deferred, malformed complete JSON fails with a line
number and no payload. Append-order branch changes are disclosed; a JSONL read
does not prove the runtime's selected active branch. Legacy entries without an
ID are content addressed; repeated identical legacy entries cannot prove distinct
delivery, so use an ID-preserving documented export for that case.

Latest parsed record timestamp determines activity, including tool/metadata
activity even when its payload is excluded. No timestamp means unknown activity,
not file mtime. An inventory end cursor is ready for future deltas; omit `--after`
to explicitly read existing history. Oversized prose pages split at character
offsets and concatenate without changed text. Source limit is 64 MiB and inventory
limit is 20,000 files; coverage errors are reported rather than hidden.

Local state is normally `~/.local/state/lev/relay/<machine-hash>/<relay-hash>.json`,
mode 0600 under mode-0700 directories. Locks, sanitized pending outbox, cursor
receipts and approval proposals stay there. No raw history cache is kept.
State writes use advisory flock, fsync and atomic replacement. Nothing under
`~/.agents`, `skills`, `.git` may be a runtime state root.

## Installation and validation

Sync only `~/.agents/skills/lev-relay/` through the existing skills repository.
Install a public executable wrapper at `~/.local/bin/relay` which execs
`python3 ~/.agents/skills/lev-relay/scripts/relay.py`; do not symlink the bundled
wrapper because its relative-path lookup would then target the wrong directory.
Do not overwrite an existing unrelated relay command.

```sh
python3 -B -m unittest discover -s ~/.agents/skills/lev-relay/tests -v
relay list --since-hours 24 > /local/private/output/inventory.json
```

The host coordinating setup owns implementation and commits. The other host
fetches and fast-forwards only when safe, verifies the exact commit and runs
these same commands. Inventory metadata is returned to Lev Relay through the
supported, human-authorized chat route. Preserve unrelated edits and machine-tick
work; never blanket-stage, rebase, force-push or synchronize runtime state.

## Acceptance boundary

Synthetic tests verify parsing, source filters, bindings/collisions, exact prose
pagination, cursors, pending delivery idempotency, wake catch-up, local monitoring
policy, expiry and idle handling. They do not prove phone visibility, actual
scheduler execution timing or native steering ownership. Report those separately
using supported app/API observations; no fake pass based on a schema alone.
