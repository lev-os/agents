---
name: slack
description: Use when reading or searching Slack messages, DMs, threads or canvases, sending a Slack message, or working with Slack CLI apps, Web API methods, OAuth scopes or Block Kit payloads.
---

# Slack

## Contents

- [Workspace through mcporter](slack-mcporter.md): read and search messages, DMs, threads and canvases, and send, from any agent.
- [Installation](INSTALL.md): optional CLI or raw API transport, host dependencies, credentials and removal.
- [CLI](#cli): teams, apps, local development, deployment and existing-login reuse.
- [Web API](#web-api): methods, scopes, pagination, errors and Block Kit surfaces.

## Workspace

To read, search or send in a workspace, read [slack-mcporter.md](slack-mcporter.md).
It is the default route for every agent. The CLI login below has no history,
search or canvas scope.

## CLI

For CLI authentication, app setup, development, deployment or documentation
search, read [slack-cli.md](slack-cli.md). Resolve the actual official executable
before using commands; an unrelated binary called slack is not sufficient.

## Web API

For a method, scope, API error, cursor or rate-limit question, read
[slack-api.md](slack-api.md) and its credential bridge in
[slack-cli.md](slack-cli.md). The CLI is optional; raw HTTP can use the actual
method's required token type. Keep sends, app installation and provider writes
inside the user's authorized task.

Both guides and installation instructions are included in this package.
