# Exa installation

## Bundled transport and prerequisites

This leaf contains `scripts/exa.sh`, `scripts/common.sh` and an offline fixture
test. No Exa CLI package or MCP installation is needed. Requests require host
Bash, curl and jq. Tests additionally use Python 3. The shell transport is for
macOS/Linux or another compatible Bash environment; native Windows without
those tools is not qualified.

Bind `EXA_ROOT` to the directory containing this leaf's `SKILL.md`, independent
of the target project working directory. Check prerequisites without calling
the provider:

```bash
command -v bash
command -v curl
command -v jq
EXA_ENV_FILE=/dev/null "$EXA_ROOT/scripts/exa.sh" help
```

On macOS with existing Homebrew, a requested jq install uses `brew install jq`.
Use the host's package manager for missing Bash/curl/Python rather than adding
a second Exa transport. Preserve executable bits when copying the package.

## Credentials and verification

Supply an authorized `EXA_API_KEY` in the process environment without printing
it. The helper also supports an explicitly selected `EXA_ENV_FILE` and its
existing credential-file branch; inspect source before relying on a default.
It loads the env file even for help, so `/dev/null` above keeps that check free
of machine-local credential reads.

```bash
python3 "$EXA_ROOT/scripts/test_exa.py"
```

This uses a fake curl service and temporary credentials. Provider verification
is separate: `status` performs a search, consumes quota and requires HTTP 200.
Run it only within a requested provider-check scope. Obtain a missing key
through the [Exa dashboard](https://dashboard.exa.ai/api-keys) for the authorized
account; do not create accounts or keys as part of this package update.

## Update and remove

Update bundled helpers through the Tools source owner and rerun the offline
fixture. Removal means deleting this selected leaf/route after preserving its
callers; it does not remove host Bash/curl/jq or revoke a provider key. For a
leaf relocation, resolve scripts from the new leaf directory.

Source: [Exa documentation index](https://exa.ai/docs/llms.txt), checked 2026-10-12; dependency and loading behavior verified from the bundled scripts.
