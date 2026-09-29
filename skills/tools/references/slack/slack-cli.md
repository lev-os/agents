---
name: slack-cli
description: Use when a task works with the Slack CLI for authentication, teams, apps, local runs, deployment, manifests, Web API calls, or documentation search.
---

# Slack CLI

The Slack CLI is optional. Resolve its executable before use and keep the
resolved value in `SLACK_CMD` for this run.

## Resolve and discover

Check the official per-user path first:

```bash
if [[ -x "$HOME/.slack/bin/slack" ]]; then
  SLACK_CMD="$HOME/.slack/bin/slack"
elif command -v slack >/dev/null 2>&1 && [[ "$(slack _fingerprint 2>/dev/null || true)" == "d41d8cd98f00b204e9800998ecf8427e" ]]; then
  SLACK_CMD="$(command -v slack)"
else
  unset SLACK_CMD
fi
```

On Windows, check the documented `%USERPROFILE%\\AppData\\Local\\slack-cli\\bin\\slack.exe`
path before the equivalent PATH probe. If neither path identifies the public
CLI, ask the developer for the installed alias or whether installation is
wanted. Do not substitute an unverified command with the same name.

Before an unfamiliar command or flag, run live help:

```bash
"$SLACK_CMD" help
"$SLACK_CMD" <group> --help
"$SLACK_CMD" <group> <command> --help
```

The help output is the source of truth for CLI versions and project-local
features. Resolve app IDs with `app list` and team IDs with `auth list` when
those commands are present.

## Documentation search

When the CLI exposes documentation search, use it for Slack platform details:

```bash
"$SLACK_CMD" docs search "<query>" --output=text --limit=5
```

Otherwise read the official documentation index directly:
<https://docs.slack.dev/reference/>. The Web API method contract remains in
`./slack-api.md`.

## Authentication and teams

CLI login is a per-team session. Inspect existing teams with `auth list`, then
run the current `login --help` flow for the requested team. If the help exposes
the ticket flow, use `login --no-prompt`, ask the developer to submit the
printed `/slackauthticket ...` command in their workspace, collect the
challenge shown by Slack, and finish with the documented `--ticket` and
`--challenge` flags. Verify with `auth list` and record the team ID.

CLI login alone does not establish Web API access. `slack api --help` lists
token precedence: explicit token, app selection (which can install an app),
`SLACK_BOT_TOKEN`, `SLACK_USER_TOKEN`, then an app prompt. Resolve the intended
token without an unrequested install. Raw HTTP also needs an OAuth token;
see `./slack-api.md` for token type and scope rules. Never print a
token or treat a token's presence as proof that the target team is reachable.

## Web API calls

Use the CLI when it exposes `api` and run its help first:

```bash
"$SLACK_CMD" api --help
"$SLACK_CMD" api <family.method> key=value
```

Method arguments use positional `key=value`; CLI metadata such as `--team`,
`--token`, `--json`, and `--data` uses flags. Inspect the response envelope and
require `ok: true`. Read-only calls can run within the user's authorization;
post, update, delete, archive, kick, admin, deploy, and other state changes
need the user's existing mutation authorization.

## App setup, local run, and deployment

Use the command group exposed by live help for app creation or templates. The
current public CLI uses `create` with optional `--template`, but keep live help
as the authority for versioned flags:

```bash
"$SLACK_CMD" help
"$SLACK_CMD" create --help
"$SLACK_CMD" create --list
```

Choose the documented scaffold command, template, and project directory. Keep
the generated manifest in the target project and validate it before deployment:

```bash
"$SLACK_CMD" manifest --help
"$SLACK_CMD" manifest validate
```

For local execution, inspect `run --help`, resolve an app or team ID, and run
the documented command in the target project. `run` is local development;
`deploy` changes hosted Slack state and requires explicit authorization. Keep
long-running output attached to its process and record its actual endpoint or
session evidence.

For triggers, datastore, environment variables, collaborators, external auth,
and deploy operations, inspect the group help before acting. Interactive
commands need an attached terminal and explicit user input; do not background
them and infer completion from a quiet process.

## Block Kit

Block Kit guidance belongs here so the Tools package has no dependency on a
separate skill name. Read the surface compatibility and element contracts at
<https://docs.slack.dev/reference/block-kit/> and preview layouts in the Block
Kit Builder when visual review is useful. Build `blocks`, `elements`, and
composition objects according to the target surface (message, modal, or
Home tab), then validate when the CLI exposes the validator:

```bash
"$SLACK_CMD" api blocks.validate --no-auth 'blocks=[{"type":"section","text":{"type":"mrkdwn","text":"Hello"}}]'
```

Use the Web API reference for the surrounding method and token scopes; this
section owns only the payload shape and surface compatibility. Include a
meaningful top-level fallback `text` for messages and accessible labels or
alt text for images and controls; a visually valid Block Kit payload is not an
accessibility check.

## Evidence

Report the resolved CLI path, team/app target, command, provider response, and
resulting ID or URL. Distinguish local process state from Slack lifecycle
state, and CLI exit status from an API response with `ok: false`.
