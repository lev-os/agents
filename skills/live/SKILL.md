---
name: live
description: Maintain a local JSON-backed progress view with live refresh, nested work lists and linked evidence. Use for browser status reports and long-running work dashboards; execution stays with the existing work owner.
---

# Live

Turn the current work and verified evidence into a browser report. This is the
temporary manual reporting layer while the Lev integration is developed.
The JSON is a projection; canonical plans, task owners and acceptance records
keep their authority. Clicking the view never starts work.

## Use the current view

Find an existing report before creating another. Keep its project and workstream
binding. Reuse a healthy local server; read its recorded state once. Report
exactly which workers, goal and processes are running rather than treating an
open chat or active workstream as a running agent.

The view uses the user's status structure: outcome, changes, current versus
ideal, expert method, numbered work list, evidence and remaining decisions.
A row drills into a child report or its actions. Back keeps its header space.
The information button and document links use the detail pane. Dark mode is the
default; the saved light/dark choice persists. Mobile has 20 px side padding.

Read [the data contract](references/data.md) when creating a view or changing
its structure. The bundled template has no project-specific behavior.

## Commands

Use Python 3.10+ on macOS/Linux, or WSL on Windows. Resolve the skill directory
from this file; `<skill>` below means that directory, not the project's cwd.
Run `python3 <skill>/scripts/live.py --help` for the supported helper commands.
These are local helper commands, not Lev CLI registrations.

```bash
python3 <skill>/scripts/live.py init --data <report>/status.json --title 'Project progress'
python3 <skill>/scripts/live.py render --data <report>/status.json --out <report>/index.html
```

For an existing child-plan catalog, pass `--reference <catalog.json>` to render.
Preserve an existing report's filename and JSON contract. Data changes need no
HTML rebuild while the browser is open. Render again to refresh a standalone
snapshot, change the template or change the embedded catalog.

Use one root writer. Workers return owned receipts for review. Apply a JSON
merge patch through stdin with the revision just read. Arrays replace as a unit;
`null` removes a key. The helper validates and atomically writes the data.

```bash
jq -n --arg message 'Verified result and remaining work.' \
  '{orchestrator:{current:$message}}' |
  python3 <skill>/scripts/live.py update --data <report>/status.json --expect-revision <n>
```

A stale revision or invalid report reference fails without changing the JSON.
Adjacent `.lock` files and server-state records are host-local; keep them out
of version control. Data refresh runs in the browser, without model polling.

```bash
python3 <skill>/scripts/live.py serve --root <document-root> --page <relative-html-path> --state <host-local-state.json>
python3 <skill>/scripts/live.py status --state <host-local-state.json>
python3 <skill>/scripts/live.py stop --state <host-local-state.json>
```

Serve runs in the foreground, binds loopback and prints one JSON startup record.
Use the available background process supervisor or a detached process with a
log. Preserve its PID/state and reuse it; do not poll healthy logs in model
turns. An existing matching server is reused. Stop verifies its instance before
sending a signal; legacy servers can be inspected but are not stopped by this
helper. Open the returned HTTP URL in the collaborative browser, and in Brave
when that is the user's browser. Open `file://` artifacts in Brave.

## Finish the change

Verify the requested route in light and dark themes at mobile and desktop
widths. Check Back geometry, theme persistence, side padding, document links
and absence of horizontal overflow. Run the helper for any script behavior
changed. Save proof with the report and reconcile only affected work records.
State whether evidence came from a resized browser or physical hardware.

Keep runtime proof distinct from this view's tests. Starting a goal, task,
build, service, deployment or scheduled job retains its existing authorization.
A local report server grants none of those effects. General Lev/FlowMind/plugin
integration remains outside this temporary skill.
