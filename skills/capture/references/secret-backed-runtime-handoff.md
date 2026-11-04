# Secret-backed runtime handoffs

Use this pattern when a captured handoff must activate a tool from secrets injected into an agent/container environment.

## The four contracts

1. **Host secret contract** — the environment variable names managed by the runtime. Record names only, never values.
2. **Consumer contract** — the variable names or credential format the target CLI/API accepts. These may differ from host names.
3. **Scoped activation contract** — map host names to consumer names only for the child process that needs them. Do not add persistent aliases to repo files, shell profiles, cron arguments, or captures.
4. **Durable runtime contract** — the post-activation cache/keyring/database path, owner, permissions, and intended `HOME`/user context for later noninteractive runs.

## Safe verification sequence

1. Confirm each required **host variable name** is non-empty without printing any value.
2. Create or validate the durable credential/cache directory with restrictive permissions.
3. Invoke activation with a child-process-only mapping; do not use shell tracing and do not pass secret values as CLI arguments.
4. Verify the target tool's success exit status and a non-secret discovery command.
5. Run a cache-only check with secret variables intentionally absent to prove later cron/noninteractive executions depend on the durable encrypted store rather than the interactive environment.
6. Keep activation separate from operational proof: a successful import/activation does not prove the next export, API call, or scheduled job will succeed. Record the remaining bounded proof and any stale heartbeat independently.

## Capture hygiene

- Persist variable **names**, tool version/contract evidence, cache location, and proof status only.
- Never persist values, redacted fragments, command output that might contain values, process listings, shell history, or raw `.env` content.
- If a previous capture uses the consumer variable names as the host contract, correct it explicitly and describe the scoped mapping.
- Keep unrelated integrations separate: e.g., a gateway bot token failure is not evidence that a browser-authenticated export tool failed.

## Slackdump example

For Slackdump v4.4.1, the CLI recognizes `SLACK_TOKEN` and `SLACK_COOKIE`. If a managed runtime owns browser-derived credentials under differently named variables, map them only into `slackdump workspace new -load-env <workspace>`; use the encrypted cache for subsequent runs under the same `HOME` and user context. Do not store the aliases or values in source control.
