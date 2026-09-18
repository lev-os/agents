---
name: tools
description: Route GitHub gh, Notion ntn, Slack CLI/API, Exa research, AgentMail, and Herdr/OMP terminal-agent work through one self-contained integration router. Use for GitHub, Notion, Slack, Exa, AgentMail, Herdr, OMP, ntn, slack, gh, mailbox, or terminal-agent coordination.
---

# Tools

Run commands from `/Users/jean-patricksmith/ops` unless the task names another project.

- GitHub: read `references/github.md`; use `gh`.
- Notion: read `references/notion/notion.md`; use `ntn`.
- Slack CLI/app work: read `references/slack/slack-cli.md`; API method work also reads `references/slack/slack-api.md`.
- Exa/web research: read `references/exa/exa.md`; use `references/exa/scripts/exa.sh` when the direct API path is needed; preserve URLs, dates, claims and uncertainty.
- AgentMail: read `references/agentmail/agentmail.md`; supporting references and agent metadata live below that directory; use `agentmail` with `AGENTMAIL_API_KEY` from the machine-local environment.
- Herdr/OMP: read `references/herdr.md`; inspect and coordinate panes with `herdr`, while OMP performs implementation.

Inspect live CLI help before an unfamiliar command. Preserve the user's mutation boundary.

## Self-contained routing

This directory owns the complete integration guidance above. Do not route through the former global skill names. Read the matching reference directly, including its nested `references/`, `scripts/`, `agents/`, and asset folders, then use the relevant CLI or tool. The reference files are operational guidance, not permission to mutate external systems.

## Inventory

Managed here: GitHub (`gh`), Notion (`ntn`), Slack CLI and Web API, Exa/web research, AgentMail, and Herdr terminal-agent coordination with OMP. The router does not currently manage Trello, Asana, Airtable, Dropbox, Figma, Canva, Todoist, or other optional app plugins; those require their own connector or a future reference added here.
