# Install and authenticate Teamwork Graph

- [Runtime and provenance](#runtime-and-provenance)
- [Inspect or install](#inspect-or-install)
- [Login and verification](#login-and-verification)
- [Update and remove](#update-and-remove)

## Runtime and provenance

The Tools leaf contains local guidance. The host provides Atlassian's official
`twg` binary. `acli` is a different executable. TWG is a standalone binary and
does not require Node.js. Official releases support macOS arm64/x64, Linux x64,
and Windows arm64/x64. This installation was checked on macOS arm64.

Sources:

- [Official installation](https://developer.atlassian.com/platform/teamwork-graph/twg-cli/getting-started/installation/)
- [Official OAuth/profile guide](https://atlassian.github.io/twg-cli/getting-started/configure-oauth/)
- [Official public repository](https://github.com/atlassian/twg-cli)

The inspected stable installer selected version 1.3.6. The macOS arm64 binary's
published SHA-256 was
`77435bb7600b031f6135056dcdd3a47cda866279fbbe718906b446d7b4714c67`.
Release identity is a checked snapshot. Inspect the current official source
before an upgrade rather than treating this version as permanently latest.

## Inspect or install

```bash
command -v twg
twg --version
twg --help
```

If missing, obtain the official installer and read it before execution:

```bash
curl -fsSL https://teamwork-graph.atlassian.com/cli/install -o /tmp/twg-install.sh
bash /tmp/twg-install.sh --help
```

The inspected installer supports a pinned version, custom install directory,
`--skip-login`, and `--skip-skills`. Its finalize step can write configuration
and setup state. Full setup can install agent skills and enable an upkeep
helper. Review those effects before selecting that path.

For this host, the binary came directly from the official versioned URL and
matched `SHA256SUMS-v1.3.6`. macOS verified its signature outside the agent
sandbox. Only the executable was installed to `~/.local/bin/twg`; that directory
was already on PATH. No shell profile, agent registry, upstream skill bundle,
or background helper was needed.

A fresh macOS arm64 host can use the same scoped method:

1. Download `https://teamwork-graph.atlassian.com/cli/twg-darwin-arm64-v1.3.6`
   and `https://teamwork-graph.atlassian.com/cli/SHA256SUMS-v1.3.6` to a temporary
   directory. Compare the binary hash with the matching manifest entry.
2. Run `codesign --verify --verbose=2 <downloaded-binary>`. A sandbox can block
   macOS trust services. Repeat that read-only check outside the sandbox before
   treating such a failure as a bad signature. Do not bypass a real rejection.
3. Confirm that the destination has no existing TWG installation to preserve.
   Run `install -m 755 <downloaded-binary> ~/.local/bin/twg` within the approved
   host scope. Use the full path if `~/.local/bin` is not on PATH.
4. Run `twg --version` and `twg --help`. Other platforms need the matching
   official binary or documented installer, not the macOS arm64 artifact.

## Login and verification

Inspect `twg login --help` and `twg auth profile --help` first. List existing
profiles without printing credential files:

```bash
twg auth profile list -o json
```

When the user requests a new Ulta connection and that profile does not exist:

```bash
twg login --site ulta --new-profile ulta
```

Use a controlling terminal. The user opens the device verification URL,
confirms the code, reviews access, and completes authentication on the laptop.
Leave legal/access consent and CAPTCHA completion to the user. Do not pass
`--force` or skip API verification during ordinary setup.

After completion:

```bash
twg whoami --site ulta --profile ulta -o json
twg doctor --site ulta --profile ulta -o json
twg confluence content get <known-page-id> --include-metadata --site ulta --profile ulta -o json
```

If login reports `login_timeout`, the old device code cannot complete sign-in.
Start a fresh interactive login when the user is ready. Do not loop on the
expired request.

The first two commands establish identity and health. A bounded content read
establishes actual target access. Check the response, not only the exit code.
TWG cannot grant rights missing from the signed-in account.

TWG owns credentials under its local config directory, normally `~/.config/twg`.
Do not read or copy those secrets into the skill. The CLI also supports separate
profiles and optional encrypted storage. Do not migrate an existing store or
install upkeep unless that additional change is authorized.

## Update and remove

Inspect `twg upgrade --help` before an upgrade. The CLI says upgrades can refresh
installed upstream skills with overwrite. Preserve the personal Tools leaf and
unrelated agent setup. Consult the current official release/checksum source.

For this manual binary-only installation, remove only the recorded executable
when requested. Credential revocation is separate. `twg uninstall --dry-run`
previews the broader official cleanup, which can also remove credentials,
config, installer-owned skills, and helpers. Never use it for binary-only
cleanup without reviewing its exact effects and scope.
