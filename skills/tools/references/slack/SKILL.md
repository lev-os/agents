---
name: slack
description: Use when reading or searching Slack messages, DMs, threads, canvases, lists or files, or sending a Slack message, from any agent through mcporter. Also routes Slack app development (Slack CLI, Web API, Block Kit).
---

# Slack

Any agent with a shell reaches a Slack workspace through `mcporter` and Slack's
hosted MCP server. Claude, Codex, Cursor, Grok, Pi, OMP, OMO and T3 all use the
same route. It has no Slack app of our own, no plugin and no token variable.

## Contents

- [Route](#route): one mcporter entry for each workspace.
- [Calls](#calls): read, search and canvas examples.
- [Writes](#writes): sends reach real people.
- [Failures](#failures)
- [Installation](INSTALL.md): mcporter version, the entry, sign-in, a new workspace, removal.
- [Build a Slack app](#build-a-slack-app): Slack CLI and Web API guides, for app development only.

## Route

- Server: `https://mcp.slack.com/mcp`.
- Entry: `slack-<workspace>` in mcporter's home config, `~/.mcporter/mcporter.json`.
  mcporter reads it with no flag. Today the only workspace is Suntiq, entry
  `slack-suntiq` (JP 2026-11-18).
- Login: mcporter OAuth with the public client id from Slack's official plugin.
  mcporter keeps and refreshes the login in `~/.mcporter/credentials.json`, for
  each entry, on each machine.
- Check the route first: `mcporter list slack-suntiq`. It lists 27 tools when the
  login is good, and says "auth required" when it is not.
- Lev groups: `~/.config/lev/groups.yaml` maps a group's `slack` account to its
  entry. Lev's copy of the entry, `~/.config/lev/mcporter.json`, has the same name
  and URL, so it shares the login.

The Slack developer CLI (`slack`) cannot read a workspace. Its login holds
app-building scopes only, with no history, search or canvas scope.

## Calls

Read the live schema before a call: `mcporter list slack-suntiq --schema --json`.
Every call takes `--args '<json>' --output json`.

```sh
# My channels
mcporter call slack-suntiq.slack_list_user_channels --args '{"limit":20}' --output json

# Search messages, DMs included. Give keywords or filters, or the call fails.
mcporter call slack-suntiq.slack_search_public_and_private \
  --args '{"keywords":["invoice"],"natural_language_query":"latest invoice discussion","limit":10}' --output json
mcporter call slack-suntiq.slack_search_public_and_private \
  --args '{"filters":"after:2026-11-01","keywords":[],"natural_language_query":"","limit":10}' --output json

# Find canvases, then read one as markdown
mcporter call slack-suntiq.slack_search_public_and_private \
  --args '{"content_types":"files","filters":"type:canvases","keywords":[],"natural_language_query":"","limit":10}' --output json
mcporter call slack-suntiq.slack_read_canvas --args '{"canvas_id":"F0..."}' --output json

# Read a channel or a thread
mcporter call slack-suntiq.slack_read_channel --args '{"channel_id":"C0...","limit":20}' --output json
mcporter call slack-suntiq.slack_read_thread --args '{"channel_id":"C0...","message_ts":"1731..."}' --output json
```

Search filters: `in:<#C…>`, `from:<@U…>`, `is:dm`, `is:thread`, `has:file`,
`before:`, `after:`, `on:` and `type:canvases`. Other read tools:
`slack_search_public`, `slack_search_channels` (needs a query),
`slack_search_users`, `slack_read_user_profile`, `slack_list_channel_members`,
`slack_read_file`, `slack_read_list`, `slack_get_reactions`, `slack_search_emojis`.

## Writes

Write tools: `slack_send_message`, `slack_send_message_draft`,
`slack_schedule_message`, `slack_add_reaction`, `slack_create_conversation`,
`slack_create_canvas`, `slack_update_canvas`, the list tools and file upload.
A send reaches real people. Send only text the user approved for that channel
or person. When the user has not reviewed the text, use
`slack_send_message_draft`. Return the message link.

## Failures

- `isError: true` with exit 0 is a failure. Read `content[].text`.
- `parameter_validation_failed`: a search needs `keywords` or `filters`.
- "auth required" or HTTP 401: sign in again ([Installation](INSTALL.md#sign-in)).
  Never add a token header.
- "Unknown server": the machine has no entry, or mcporter is older than 0.17.1.

## Build a Slack app

Only for building, running or deploying a Slack app: read
[slack-cli.md](slack-cli.md) for the Slack CLI and [slack-api.md](slack-api.md)
for Web API methods, scopes, pagination and Block Kit. Keep app installation
and provider writes inside the user's authorized task.
