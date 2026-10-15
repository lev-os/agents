---
name: computer-use
description: Use when working with macOS GUI apps, desktop automation, background clicks, drag or canvas tasks through songkeys/claude-codex-computer-use.
---

# Computer use

## Contents

- [Install and connect locally](INSTALL.md): dependency checks, local MCP registration, verification and removal.
- [Use the tools](upstream/skills/computer-use/SKILL.md): app targeting, fresh accessibility indices, state/action/state loop and recovery.
- [Inspect provenance](UPSTREAM.md): pinned repo, byte-for-byte checks and qualification limits.
- [Inspect bridge behavior](upstream/README.md): runtime discovery, configuration and troubleshooting.

For setup or a missing MCP server, read `INSTALL.md` first. For an already
connected server, read the original upstream skill before taking an app action.
Resolve package paths from this leaf, independently of the target project cwd.
Prefer a dedicated API, connector or CLI when it covers the task.

This leaf vendors the GitHub repo unchanged. Its original skill names a Claude
plugin MCP prefix; local registration instead usually exposes
`mcp__computer-use__...`. Inspect the actual available MCP tool names and
schemas, and use the connected server's versions of the same tools. Never
invent a callable name or silently substitute a different computer-use engine.

The repo copy does not register a marketplace, load its plugin metadata or
connect an MCP server. Follow the local setup branch instead of the upstream
marketplace instructions. Its bridge uses the installed signed Codex launcher,
an unrestricted permission profile, and automatically accepts **all** upstream
`elicitation/create` requests with an ID, without checking that they are app
access requests. That protocol acceptance does not authorize a new task,
private-data access or an external mutation.

Follow the upstream observable state/action/state loop. If the user stops an
app session, stop the loop and wait for their instruction to continue, even
though the bridge can recycle its client. For completion, fetch fresh app state
and verify the requested result rather than relying on an action return code.
