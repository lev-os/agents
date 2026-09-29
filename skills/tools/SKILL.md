---
name: tools
description: Use when a task needs GitHub gh, Notion ntn, Slack CLI/API, explicit Exa transport, AgentMail, optional Herdr pane transport, or terminal-agent coordination through one self-contained integration router.
---

# Tools

Resolve the target project from the task before running a command. Use that
project's root as `cwd`; use the current workspace when no target project is
named.

Load only the branch needed for the request. Paths below are relative to this
file, so nested references remain valid if the skill is installed elsewhere.

- GitHub: read `references/github.md`; use `gh` and its live `--help` output.
- Notion: read `references/notion/notion.md`; use `ntn`.
- Slack CLI/app work: read `references/slack/slack-cli.md`; API method work also reads `references/slack/slack-api.md`.
- General research: route to the research skill. Explicit Exa transport or API work: read `references/exa/exa.md`; use `references/exa/scripts/exa.sh` for direct search, contents, or answer calls.
- AgentMail: read `references/agentmail/agentmail.md`; load `references/agentmail/references/cli-and-monitoring.md` for mailbox operations and `references/agentmail/references/suntiq-auth.md` only for SuntiQ identity work.
- Optional terminal transport: read `references/herdr.md` when the task selects Herdr or asks for pane/session operations. Herdr may inspect or coordinate a pane; the selected agent or controller owns implementation and lifecycle evidence independently.

Inspect live CLI help before an unfamiliar command. Preserve the user's mutation boundary.

Provider credentials and CLI sessions are separate authorities. Verify the
credential type, target resource, and operation before a call. A successful
process exit is not completion: inspect the provider response, resulting ID or
URL, and any pagination or lifecycle state.

## Self-contained routing

This directory owns the complete integration guidance above. Read the matching
reference directly, including nested `references/`, `scripts/`, and `agents/`
folders when that branch calls for them. Slack CLI, Block Kit, and app setup
guidance lives in the local Slack references. The reference files describe
operations; they do not grant permission to mutate external systems.

## Inventory

Managed here: GitHub (`gh`), Notion (`ntn`), Slack CLI and Web API, Exa/web
research, AgentMail, and optional Herdr pane transport. OMP, Codex, and other
agents can run without Herdr. Optional app plugins require their own connector
or a future reference added here.
