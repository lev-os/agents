# Slack installation

## mcporter

The route needs mcporter 0.17.1 or later; 0.17.1 added `oauthClientId`.

```sh
mcporter --version               # must print 0.17.1 or later
bun add -g mcporter@0.17.1       # install or upgrade when it does not
```

## The entry

Add one entry for each workspace to `~/.mcporter/mcporter.json`. Keep the other
entries in that file. Do not add an `imports` key: leaving it out keeps the
servers that mcporter imports from Cursor, Codex and the other editors.

```json
{
  "mcpServers": {
    "slack-suntiq": {
      "baseUrl": "https://mcp.slack.com/mcp",
      "auth": "oauth",
      "oauthClientId": "1601185624273.8899143856786",
      "oauthRedirectUrl": "http://localhost:3118/callback",
      "oauthTokenEndpointAuthMethod": "none"
    }
  }
}
```

The client id and callback port come from Slack's official plugin,
`github.com/slackapi/slack-mcp-plugin`, file `.mcp.json`. Slack's server does
not let a client register itself (its discovery file has no registration
endpoint), so a client id made ahead of time is required. This one is public,
uses PKCE and needs no secret. The file holds no secret.

## Sign in

Sign in when `mcporter list slack-<workspace>` says "auth required". The user
must click Allow on the "Add Claude to <workspace>" page. The page says Claude
because the client id belongs to Slack's Claude plugin. The default wait is 5
minutes, so set a longer one and run it in the background:

```sh
MCPORTER_OAUTH_TIMEOUT_MS=1800000 mcporter auth slack-suntiq
```

Tell the user to use the newest tab; a tab from an earlier attempt fails. Each
machine signs in once for each entry. The login is in
`~/.mcporter/credentials.json` and never leaves the machine.

## A new workspace

1. Copy the entry under a new name, `slack-<workspace>`, with the same values.
2. Run the sign-in for that name and pick that workspace on the Slack page.
3. Check with `mcporter list slack-<workspace>`.
4. For a Lev group, add `slack: { type: mcporter, server: slack-<workspace> }`
   to the group in `~/.config/lev/groups.yaml`, and copy the entry into
   `~/.config/lev/mcporter.json` with the same name.

(assumption) The same client id serves every workspace. Proven only for Suntiq.

## Remove

`mcporter auth slack-<workspace> --reset` clears the login. Then delete the
entry. A workspace admin can also revoke the Claude client in Slack under
Manage apps.

## Slack CLI (app development only)

The Slack developer CLI is for building Slack apps, not for reading a
workspace. To install, check or remove it, follow [slack-cli.md](slack-cli.md)
and the official guides: [macOS/Linux](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux/),
[Windows](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-windows/),
[uninstall](https://docs.slack.dev/tools/slack-cli/guides/uninstalling-the-slack-cli/).
Download and read the official install script before you run it.
