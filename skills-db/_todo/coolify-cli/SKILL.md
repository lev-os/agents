---
name: coolify-cli
description: Use when installing, configuring, scripting, troubleshooting, or operating the Coolify CLI for Coolify Cloud or self-hosted Coolify instances.
---

# Coolify CLI

Use this skill for the `coolify` command-line client from `coollabsio/coolify-cli`.

## When to Use This Skill

- Installing or updating the `coolify` binary.
- Setting up Cloud or self-hosted contexts and API tokens.
- Scripting Coolify resources, deployments, applications, services, databases, servers, GitHub apps, teams, firewall, or alpha mesh commands.
- Looking up exact Coolify CLI flags and aliases before execution.

## Source of Truth

- Exact command/flag parity lives in `references/COMMANDS.md`, regenerated from `go run ./coolify docs llms` at source commit `1bac52400810125d8275e185844372294a61eee2`.
- Quick upstream instructions live in `references/LLMS.md`; the scraped README, releases, issues, and file structure are retained from Skill Seeker extraction.
- Upstream installers are bundled as `references/install.sh` and `references/install.ps1`.
- Public command catalog count: 123 `Command:` entries. Hidden developer docs commands are `coolify docs llms`, `coolify docs markdown`, and `coolify docs man`.

## Operating Rules

- Do not invent flags. Before issuing any non-trivial command, inspect `references/COMMANDS.md` or run `coolify <family> ... --help`.
- Prefer `--format json` for automation; use `--format pretty` for debugging and `table` only for human reading.
- Treat `--token`, context tokens, passwords, IPs, and `--show-sensitive` output as secrets. Do not paste them into logs.
- Coolify resources use UUIDs; teams use numeric IDs.
- `app env sync`, `database env sync`, and `service env sync` create or update variables from a file; they do not delete variables missing from the file.
- `coolify init` is alpha Coolify v5 mesh/bootstrap work and can modify remote network/firewall state; plan first unless the user explicitly asked to apply.

## Workflow

```yaml
steps:
  - id: install
    action: Install or locate the CLI
    instruction: |
      Check first: `command -v coolify && coolify version`.
      Linux/macOS release installer:
        `curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash`
      Linux/macOS user install:
        `curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash -s -- --user`
      Specific release:
        `curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash -s -- --user v1.6.2`
      Homebrew:
        `brew install coollabsio/coolify-cli/coolify-cli`
      Windows PowerShell:
        `irm https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.ps1 | iex`
      Windows user install:
        `$env:COOLIFY_USER_INSTALL=1; irm https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.ps1 | iex`
      Go install:
        `go install github.com/coollabsio/coolify-cli/coolify@latest`
    validation: "`command -v coolify` exits 0 and `coolify version` prints a version"
    on_failure: "Read bundled installer source in references/install.sh or references/install.ps1; do not guess release asset names."

  - id: authenticate
    action: Configure context and token
    instruction: |
      Get an API token from the Coolify dashboard at `/security/api-tokens`.
      Cloud: `coolify context set-token cloud <token>`.
      Self-hosted: `coolify context add -d <context_name> <url> <token>`.
      Switch default: `coolify context use <context_name>` or `coolify context set-default <context_name>`.
      Verify: `coolify context verify` and `coolify context version`.
      For one-off automation, prefer saved contexts plus `--context <name>`; use `--token <token>` only as an explicit override.
    validation: "`coolify context verify --format json` succeeds for the intended context"
    on_failure: "Check `coolify context list --format json`, URL scheme, token scope, and target Coolify API version."

  - id: choose_command
    action: Map intent to the exact command surface
    instruction: |
      Use the command map below to choose the family, then lookup exact flags:
      `rg -n '^Command: coolify app env sync' references/COMMANDS.md`
      `rg -n '^Command: coolify database create' references/COMMANDS.md`
      `rg -n '^Command: coolify init' references/COMMANDS.md`
      If local CLI version differs from the reference, prefer local `coolify ... --help` for execution.
    validation: "Exact command, required parameters, and output format are identified before execution"
    on_failure: "Open references/COMMANDS.md around the matching `Command:` entry or run command-specific `--help`."

  - id: execute_and_verify
    action: Run the command and prove the effect
    instruction: |
      For reads, use `--format json` and parse the returned identifiers/statuses.
      For writes, capture the target UUID/name before and after, then run the relevant `get`, `list`, `logs`, `deploy get`, `context verify`, or `version` command.
      For destructive commands (`delete`, `remove`, `revoke`, preview deletion, firewall changes, mesh init/bootstrap/extend/upgrade), confirm the user asked for that destructive action.
    validation: "A follow-up read command proves the intended state or captures the returned error"
    on_failure: "Do not claim completion; report the command, exit behavior, and the safest next verification command."
```

## Command Map

| Area | Commands |
| --- | --- |
| Root | `version`, `update`, `config`, `completion <bash|zsh|fish|powershell>`, hidden `docs llms|markdown|man` |
| Context | `context list/add/delete/get/set-default/set-token/update/use/verify/version` |
| Servers | `server list/get/add/remove/validate/domains` |
| Projects/resources | `project list/get/create`, `resource list` |
| Apps | `app list/get/update/delete/start/stop/restart/logs`, `app create public/github/deploy-key/dockerfile/dockerimage`, `app previews delete` |
| App internals | `app env list/get/create/update/delete/sync`, `app deployments list/logs`, `app storage list/create/update/delete` |
| Databases | `database list/get/create/update/delete/start/stop/restart`, supported types: `postgresql`, `mysql`, `mariadb`, `mongodb`, `redis`, `keydb`, `clickhouse`, `dragonfly` |
| Database internals | `database backup list/create/update/delete/executions/delete-execution/trigger`, `database env list/get/create/update/delete/sync`, `database storage list/create/update/delete` |
| Services | `service list/get/create/delete/start/stop/restart`, `service env list/get/create/update/delete/sync`, `service storage list/create/update/delete` |
| Deployments | `deploy list/get/name/uuid/batch/cancel` |
| Integrations | `github list/get/create/update/delete/repos/branches`, `private-key add/list/remove`, `teams current/get/list/members list` |
| Network/mesh | `firewall allow/revoke/list/containers`, `init plan/bootstrap/extend/upgrade` |

## Aliases

- Apps: `app`, `apps`, `application`, `applications`; env aliases: `env`, `envs`, `environment`; storage aliases: `storage`, `storages`; previews aliases: `preview`, `previews`.
- Databases: `database`, `databases`, `db`, `dbs`; storage aliases: `storage`, `storages`.
- Services: `service`, `services`, `svc`; storage aliases: `storage`, `storages`.
- GitHub: `github`, `gh`, `github-app`, `github-apps`.
- Private keys: `private-key`, `private-keys`, `key`, `keys`.
- Servers/projects/resources/teams accept singular or plural where shown in `references/COMMANDS.md`.

## Common Patterns

```bash
# Inventory
coolify --context prod server list --format json
coolify project list --format json
coolify resource list --format json
coolify app list --format json
coolify service list --format json
coolify database list --format json

# App lifecycle
coolify app get <uuid> --format json
coolify app start <uuid>
coolify app stop <uuid>
coolify app restart <uuid>
coolify app logs <uuid> --lines 100 --follow

# Environment sync
coolify app env sync <app_uuid> --file .env.production --build-time --preview
coolify database env sync <database_uuid> --file .env
coolify service env sync <service_uuid> --file .env

# Deployments
coolify deploy name <resource_name> --force
coolify deploy batch api,worker,frontend --force
coolify deploy get <deployment_uuid> --format json
coolify app deployments logs <app_uuid> <deployment_uuid> --lines 200 --debuglogs

# Coolify v5 mesh alpha: plan before apply
coolify init plan --servers 10.0.0.1,10.0.0.2 --ssh-key ~/.ssh/id_ed25519 --format json
```

<coolify_command_check>
Before executing:

1. State the target context and whether the command is read, write, or destructive.
2. Cite the exact `references/COMMANDS.md` command entry or local `--help` output used for flags.
3. Use `--format json` when the output will be parsed.
4. Define the follow-up read command that will verify success.
</coolify_command_check>
