---
name: cass-coverage
description: "Build a 3-week coding-agent capture dashboard. Cross-references cass session inventory with .lev/pm/ workstream/handoff citations, detects resume-chain lineage, classifies orphan chains against the workstream registry, emits a canonical coverage.json + thin static viewer. Use when auditing how much agent work is captured by Lev workstreams, finding orphan transcripts, building a healing pipeline, or scheduling a weekly coverage report."
argument-hint: "[--since 3w|1w|2w] [--window YYYY-MM-DD..YYYY-MM-DD] [--no-bake]"
allowed-tools: Read Write Edit Bash Glob Grep Agent
---

# /cass-coverage — Capture Dashboard Builder

Audit how much of recent coding-agent work (Claude Code, Codex) is captured by Leviathan workstreams. Produces a navigable HTML dashboard backed by a canonical `coverage.json` artifact.

## Architecture (data ↔ view split)

```
.lev/pm/captures/dashboard-<window>/    ← per-window output (gitignored if you commit captures elsewhere)
├── dashboard.html                      ← copy of viewer/dashboard.html (≈40 KB, no data)
└── coverage.json                       ← canonical artifact, ≈3 MB, schema-d (git-trackable)

~/.cache/cass-lev/<project>/            ← XDG cache, machine-local, never in repo
└── <chain-id>/<session-id>.html        ← cass-baked transcripts (≈100 MB+ total)

~/.claude/skills/cass-coverage/
├── viewer/dashboard.html               ← single-file vanilla-JS viewer (fetches coverage.json)
├── schema/coverage.schema.json         ← JSON Schema 2020-12
└── scripts/                            ← inventory → merge → classify → bake → render
```

The viewer is **dumb**: it fetches `./coverage.json` (or `?coverage=<url>`) and renders. No data hardcoded. Same HTML works for any coverage.json — local file://, hosted URL, here-now publish, etc.

## Pipeline

```bash
SKILL=~/.claude/skills/cass-coverage
WIN_FROM=2026-04-03; WIN_TO=2026-04-27
PROJECT=leviathan
WS_DIR=/Users/jean-patricksmith/digital/leviathan/.lev/pm/workstreams
OUT=/Users/jean-patricksmith/digital/leviathan/.lev/pm/captures/dashboard-${WIN_TO}
INVENTORY=$OUT/inventory

# 1. Inventory per agent (resume-chain detection + workstream match)
python3 $SKILL/scripts/inventory.py --agent claude_code --window $WIN_FROM $WIN_TO \
    --workstreams $WS_DIR --output-dir $INVENTORY
python3 $SKILL/scripts/inventory.py --agent codex --window $WIN_FROM $WIN_TO \
    --workstreams $WS_DIR --output-dir $INVENTORY

# 2. Merge → canonical coverage.json (filters human-rooted, applies fold rule, embeds ws snapshot)
python3 $SKILL/scripts/merge.py --window $WIN_FROM $WIN_TO --inputs $INVENTORY \
    --workstreams $WS_DIR --project $PROJECT --output $OUT/coverage.json

# 3. Classify orphans (heuristic) → updates coverage.json in-place
python3 $SKILL/scripts/classify.py --coverage $OUT/coverage.json \
    --output $OUT/classifier.json --update-coverage

# 4. Bake transcripts to ~/.cache/cass-lev/<project>/  (idempotent --lazy by default)
bash $SKILL/scripts/bake.sh --coverage $OUT/coverage.json --project $PROJECT

# 5. Render: copy viewer + coverage.json into output dir
python3 $SKILL/scripts/render.py --coverage $OUT/coverage.json --output-dir $OUT

open $OUT/dashboard.html
```

## Core data: coverage.json

One file, ~3 MB, schema'd by `schema/coverage.schema.json`. Top-level shape:

```jsonc
{
  "meta": { "project", "machine", "window", "generated_at", "totals": {...} },
  "agents": { "claude_code": {raw_sessions, all_chains, human_rooted}, "codex": {...} },
  "workstreams": [{ id, title, objective, status, phase }, …],
  "chains": [{
    "id": "<root-uuid> | fold:<kind>:<bucket>",
    "agent": "claude_code|codex",
    "topic", "topic_short", "msgs", "lineage", "n_sessions",
    "started", "ended", "started_full",
    "ws", "status",                    // captured iff session_id appears in .lev/pm/handoffs/*.md
    "session_paths", "transcript_path",
    "handoff_refs", "resume_signals",
    "is_fold", "fold_kind", "fold_members",
    "classification": { "ws", "score", "bucket", "alts", "reason" }  // for orphans w/ msg_total ≥ 50
  }, …]
}
```

## Fold rule (autoresearch fan-out collapse)

Codex parallel fan-outs (`$codex-autoresearch`, `CDO Turn`, `Adaptive CDO`, `Hermes deep dive`, `You are the * mode`, `You are the Discover`, `tCursor Agent v`) get collapsed into virtual parent chains keyed by `(prefix_class, started_at_5min_bucket)`. Real human chains in the same window are unaffected. Reduces sidebar inflation; the audit found ~83 codex chains collapse to ~30-35 real human-rooted threads.

## Classifier (heuristic)

Each orphan with `msg_total ≥ 50` scored against workstream registry via:
- token overlap (workstream id + title + objective tokens vs topic + handoff_refs tokens)
- slug literal hit in topic = +2
- handoff filename containing slug = +3

Buckets:
- `auto_attribute` (≥7) — high confidence, can update workstream session_refs without human review
- `needs_review`  (4-6.99) — likely fit, verify by reading transcript
- `archive`       (<4)    — no fit, close as ephemeral
- `bot_dispatch`         — `$skill` / `# Task` / `<command-message>` prefixes; attribute via invoker

Upgrade path: replace the heuristic with Sonnet via Anthropic SDK + prompt-cached workstream descriptions; same bucket schema.

## Viewer features

- Cursor-style left sidebar (collapsible via ≡; persists in localStorage; <900px viewport → drawer)
- Sidebar groups: Dashboard ▦ + Captured-by-workstream + Orphans-by-agent
- Cards: agent badge · ws pill · ⌥ fold badge · ⚙ classifier suggestion (auto/review/archive/bot)
- Click card → loads cass-baked transcript in iframe; injects `__lev_override` CSS to kill cass left-border + hover-bg
- `/capture` button → copies structured prompt to clipboard, marks card "queued" (localStorage persists)
- Filters: agent · status (captured/orphan/queued) · debounced search · min-msgs slider
- Performance: `content-visibility: auto` on cards; payloads in single JS object (not inline data-attrs)

## Verification (agent-browser)

```bash
AB=/path/to/agent-browser
$AB set viewport 1600 1000
$AB open "file://$OUT/dashboard.html"
$AB screenshot /tmp/dash.png
$AB set viewport 768 1024 && $AB reload && $AB screenshot /tmp/dash-tablet.png
```

Click any orphan-codex chain → iframe loads transcript with no green left-border on user msgs.
Click ≡ toggle → `.main` width = 1600 on a 1600 viewport.

## Cross-machine (future)

`coverage.json` is machine-scoped (`meta.machine` field). Each machine produces its own. Merge across machines = union by `chain_id` (UUIDs are globally unique) with workstream as cross-machine spine. Out of scope for v1; see "swarm" track.

## Known gaps

- **cursor support**: `cass --workspace` filter returns 0 for cursor (rowid in 8.4 GB sqlite). Workaround = mine `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` directly + map workspaces via `workspaceStorage/<hash>/workspace.json`. Not in v1.
- **claude resume detector**: conservative — only links sessions when a handoff filename appears in both. Misses `/clear`+resume pairs without explicit handoff. Add proximity-only relaxation (gap < 6h, same project, resume keyword in B's first user msg) for ~10% more captures.
- **classifier**: keyword-overlap only. Sonnet upgrade via prompt-cached workstream descriptions costs ~5¢/run for 30 orphans.
- **transcript bake**: 117 MB for 366 transcripts is the floor; lazy-bake-on-click would cut to ~5 MB but requires a tiny local server (current viewer is pure file://).

## Scheduling

Weekly Monday refresh:
```bash
/schedule cass-coverage --window $(date -v-1w +%F) $(date +%F)
```
Use a small wrapper that runs the 5-step pipeline and posts the new coverage.json to a chosen sync surface (here-now URL, gist, or a shared bucket).
