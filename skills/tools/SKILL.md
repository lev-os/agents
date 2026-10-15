---
name: tools
description: GitHub, gh, issues, pull requests; Notion, ntn, pages, databases; Slack, chat, messaging, Block Kit; Exa, web search, semantic search, contents; AgentMail, email, inboxes, OTP; Herdr, terminal panes, agent sessions; computer use, macOS GUI, desktop automation, background clicks, drag, canvas; add tool, install skill, absorb integration.
---

# Tools

To design or repair a tool interface (overlapping purpose, examples, output
size, errors), read [Tool design](references/tool-design.md). It is
instructions only; existing leaves keep their operations.

## Contents

| Tool / request | Read this leaf or reference | Runtime / setup |
|---|---|---|
| GitHub repositories, issues, pull requests, Actions, API | [GitHub](references/github/SKILL.md) | Host `gh`; [setup](references/github/INSTALL.md) |
| Notion pages, databases, API, workers, uploads | [Notion](references/notion/SKILL.md) | Host `ntn`; [setup](references/notion/INSTALL.md) |
| Slack CLI, teams, apps, authentication, deployment | [Slack CLI branch](references/slack/SKILL.md#cli) | Optional host Slack CLI; [setup](references/slack/INSTALL.md) |
| Slack methods, OAuth scopes, pagination, rate limits | [Slack API branch](references/slack/SKILL.md#web-api) | HTTP/SDK or host CLI; [setup](references/slack/INSTALL.md) |
| Explicit Exa search, contents, answers, API | [Exa](references/exa/SKILL.md) | Bundled shell transport; [setup](references/exa/INSTALL.md) |
| AgentMail inboxes, messages, drafts, OTP, monitoring | [AgentMail](references/agentmail/SKILL.md) | Host `agentmail` or API; [setup](references/agentmail/INSTALL.md) |
| Herdr pane inspection and authorized agent coordination | [Herdr](references/herdr/SKILL.md) | Optional host `herdr`; [setup](references/herdr/INSTALL.md) |
| macOS GUI, background clicks, drag and canvas work | [Computer use](references/computer-use/SKILL.md) | Bundled bridge; [local setup](references/computer-use/INSTALL.md) |
| Add a tool, install a leaf, absorb an integration | [Add a tool](references/add-tool.md) | Skill workflow; intake/qualification belongs to `skill-builder` |
| Worker loading, skill IDs, FlowMind / Lev IR | [Lev skill-loading contract](../lev/references/tool-skills.md) | `skill://<top-level-or-db-id>`; host loads the selected package |

Resolve the target project from the task before running a command. Use that
project's root as `cwd`; use the current workspace when no target project is
named.

Load only the branch selected by the contents table. Paths are relative to
this file, so nested references remain valid if the skill is installed
elsewhere. Each integration is a leaf package with `SKILL.md` and `INSTALL.md`;
old reference paths remain compatibility routes. Slack's CLI and API guides
share one leaf and retain their existing paths.

General research routes to `skill://research`. Explicit Exa transport/API work
loads the Exa reference and its bundled `scripts/exa.sh`. AgentMail mailbox
operations also load its local `references/cli-and-monitoring.md`; SuntiQ
identity work loads `references/suntiq-auth.md`. Herdr is optional; the selected
agent/controller owns implementation and lifecycle evidence independently.

Inspect live CLI help before an unfamiliar command. Preserve the user's mutation boundary.

Provider credentials and CLI sessions are separate authorities. Verify the
credential type, target resource, and operation before a call. A successful
process exit is not completion: inspect the provider response, resulting ID or
URL, and any pagination or lifecycle state. An input rejected before any effect
is retryable once corrected. A mutation that timed out or returned an ambiguous
status has an uncertain effect: look up the target resource before acting again,
and hold and report when the lookup cannot settle it. Never replay an uncertain
effect.

The leaf/reference files describe operations; they do not grant permission to
send messages, enable a connector, install software or mutate external systems.
