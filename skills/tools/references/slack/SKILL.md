---
name: slack
description: Use when working with Slack CLI apps, Slack Web API methods, workspace messaging, OAuth scopes or Block Kit payloads.
---

# Slack

## Contents

- [Installation](INSTALL.md): optional CLI or raw API transport, host dependencies, credentials and removal.
- [CLI](#cli): teams, apps, local development, deployment and existing-login reuse.
- [Web API](#web-api): methods, scopes, pagination, errors and Block Kit surfaces.

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
