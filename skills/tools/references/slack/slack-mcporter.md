# Slack workspace reads and sends through mcporter

Use this route to read or search Slack messages, DMs, threads, canvases, lists
and files, or to send a message. Any agent with a shell can use it: Claude,
Codex, Cursor, Grok, Pi, OMP, OMO, T3. The `slack` developer CLI cannot do this.
Its login holds app-building scopes only, with no history, search or canvas
scope.

## Route

- Server: Slack's hosted MCP server, `https://mcp.slack.com/mcp`.
- Entry: `slack-suntiq` in `~/.mcporter/mcporter.json`, which mcporter reads with
  no flag. Lev's groups file `~/.config/lev/mcporter.json` holds the same entry.
  The same name and URL share one login.
- Login: mcporter OAuth with the public client id from Slack's official plugin
  (`github.com/slackapi/slack-mcp-plugin`, `.mcp.json`). No Slack app of our own
  and no token variable. mcporter keeps and refreshes the login in
  `~/.mcporter/credentials.json`.
- Needs mcporter 0.17.1 or later, which has `oauthClientId`. Check with
  `mcporter --version`.
- Only the Suntiq workspace exists (JP 2026-11-18). Decision:
  `~/digital/leviathan/.lev/pm/decisions/20261118-slack-through-mcporter-oauth-no-app.yaml`.

The entry:

```json
"slack-suntiq": {
  "baseUrl": "https://mcp.slack.com/mcp",
  "auth": "oauth",
  "oauthClientId": "1601185624273.8899143856786",
  "oauthRedirectUrl": "http://localhost:3118/callback",
  "oauthTokenEndpointAuthMethod": "none"
}
```

## Sign in

Run the sign-in only when `mcporter list slack-suntiq` says auth required. JP
must click Allow on the "Add Claude to Suntiq" page. The name is Claude because
the client id belongs to Slack's Claude plugin. The default wait is 5 minutes,
so set a longer one:

```sh
MCPORTER_OAUTH_TIMEOUT_MS=1800000 mcporter auth slack-suntiq
```

Run it in the background and tell JP to use the newest tab. A tab from an
earlier attempt fails.

## Calls

Read the live schema before a call: `mcporter list slack-suntiq --schema --json`.

```sh
# My channels
mcporter call slack-suntiq.slack_list_user_channels --args '{"limit":20}' --output json

# Search messages, DMs included. Needs keywords or filters.
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

Other read tools: `slack_search_public`, `slack_search_channels`,
`slack_search_users`, `slack_read_user_profile`, `slack_list_channel_members`,
`slack_read_file`, `slack_read_list`, `slack_get_reactions`, `slack_search_emojis`.

## Writes

Write tools: `slack_send_message`, `slack_send_message_draft`,
`slack_schedule_message`, `slack_add_reaction`, `slack_create_conversation`,
`slack_create_canvas`, `slack_update_canvas`, the list tools and file upload.
A send reaches real people. Send only text the user approved for that channel or
person. When the user has not reviewed the text, use `slack_send_message_draft`.
Return the message link.

## Failures

- `isError: true` with exit 0 is a failure. Read `content[].text`.
- `parameter_validation_failed` on a search: give `keywords` or `filters`.
- `auth required` or HTTP 401: run the sign-in above. Do not add a token header.
