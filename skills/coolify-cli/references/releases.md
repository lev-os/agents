# Releases

Version history for this repository (16 releases).

## v1.6.2: v1.6.2
**Published:** 2026-04-20

## What's New
- Added `coolify app previews delete <app_uuid> <pr_id>` command to tear down preview deployments via the Coolify API

## Bug Fixes
- None

## Documentation
- Updated `llms-full.txt` with the new preview delete command and `preview` alias

## Breaking Changes
- None

## Requirements
- Coolify `4.0.0-beta.474` or newer is required for the new preview delete endpoint

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.6.2)

---

## v1.6.1: v1.6.1
**Published:** 2026-04-16

## Bug Fixes
- Fixed JSON output format for service commands (#70)

## Documentation
- Generate `llms.txt` and `llms-full.txt` for AI tooling
- Release guide updated (Homebrew tap, automated version bumping)

## Breaking Changes
- None

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.6.1)

---

## v1.6.0: v1.6.0
**Published:** 2026-03-30

## What's New

- Added Homebrew tap support for CLI distribution.
- Added support for preview deploy fields in deployment request payloads.
- Improved llms.txt generation:
  - derive aliases from the command tree
  - include overview, data models, short flags, and defaults

## Fixes

- Fixed version update notices so they are written to stderr, preserving clean JSON output on stdout.

## Notes

- No breaking changes in this release.

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.6.0)

---

## v1.5.0: v1.5.0
**Published:** 2026-03-23

## Features

- **Storage Management**: Added comprehensive CRUD operations for persistent and file-based storage across applications, databases, and services
- **Environment Variables**: Support identifying env vars by UUID or key name in update commands, eliminating separate lookup requirement
- **Database Environments**: Added complete environment variable management for databases with sync command to load from .env files
- **Application Model**: Expanded Application with git, build, health check, and resource limit fields plus ApplicationSettings for feature flags
- **AI Integration**: Added `docs llms` command to generate machine-readable CLI specification for AI agent integration
- **Output Formatting**: Improved table rendering with new tablewriter implementation

## Fixes

- **Database Commands**: Fixed list and get commands to respect --format flag (json/pretty output now works correctly)
- **Environment Variables**: Fixed update command behavior and app env sync operations

## Improvements

- Reorganized parameter ordering in env update commands for consistency
- Enhanced table formatter with improved test robustness and clearer error messages
- Added CI workflow validation for llms.txt to keep documentation in sync
- Refactored docs generation using fmt.Fprintf for more efficient string formatting
- Restricted generated file permissions to 0600 for improved security
- Improved test assertions using idiomatic boolean helpers (assert.True/False)
- Enhanced request serialization validation in bulk env update tests

## Breaking Changes

- **API Version Requirement**: Storage operations now require minimum API version 4.0.0-beta.470
- **Environment Variable Updates**: Updated command interface for env var updates to use UUID/key identifier pattern
- **Bulk Operations**: ServiceEnvBulkUpdateResponse changed from message string to slice of environment variables

## What's Changed (Github)
* fix: update service env command by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/51
* Next by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/60
* refactor: improve table output format by @baer95 in https://github.com/coollabsio/coolify-cli/pull/55
* fix: app env bulk by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/50
* feat: Add llms.txt for AI agent command specification by @toanalien in https://github.com/coollabsio/coolify-cli/pull/52
* fix(database): respect --format flag in database list and get commands by @Dagnan in https://github.com/coollabsio/coolify-cli/pull/61
* feat(models): expand Application with extended configuration by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/63
* feat(env): allow updating vars by UUID or key identifier by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/65
* feat(storage): add CRUD operations for persistent and file storages by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/64

## New Contributors
* @baer95 made their first contribution in https://github.com/coollabsio/coolify-cli/pull/55
* @toanalien made their first contribution in https://github.com/coollabsio/coolify-cli/pull/52
* @Dagnan made their first contribution in https://github.com/coollabsio/coolify-cli/pull/61

**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/v1.4.0...v1.5.0

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.5.0)

---

## v1.4.0: v1.4.0
**Published:** 2025-12-12

## What's Changed
* feat: add create commands for applications, projects, and services by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/47


**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/v1.3.0...v1.4.0

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.4.0)

---

## v1.3.0: v1.3.0
**Published:** 2025-12-05

lol forgot that we need minor version as well 

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.3.0)

---

## v1.2: v1.2
**Published:** 2025-12-05

## What's Changed
* Check for CLI updates on every command by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/46


**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/v1.1...v1.2

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.2)

---

## v1.1: v1.1
**Published:** 2025-12-05

## What's Changed
* Add runtime env flag and improve service env handling by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/45


**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/v1.0.5...v1.1

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.1)

---

## v1.0.5: v1.0.5
**Published:** 2025-11-27

## What's Changed
* fix: leading 'v' for release filename of install script by @ncryptedV1 in https://github.com/coollabsio/coolify-cli/pull/41
* Fix is_buildtime JSON tag and add is_runtime, is_shared fields by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/42
* chore(deps): bump golang.org/x/crypto from 0.43.0 to 0.45.0 by @dependabot[bot] in https://github.com/coollabsio/coolify-cli/pull/43
* fix: update  release workflow by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/39

## New Contributors
* @ncryptedV1 made their first contribution in https://github.com/coollabsio/coolify-cli/pull/41
* @dependabot[bot] made their first contribution in https://github.com/coollabsio/coolify-cli/pull/43

**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/v1.0.4...v1.0.5

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.0.5)

---

## v1.0.4: v1.0.4
**Published:** 2025-11-10

## What's Changed
* Enable parallel GoReleaser builds by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/29
* Add flags to env sync command by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/32
* feat: installable via go by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/31
* feat: testing ci with linter by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/33
* feat: Version inject by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/34
* Remove gzip file validation check by @LaurenceJJones in https://github.com/coollabsio/coolify-cli/pull/36
* Add deployment management commands for improved user experience by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/37

## New Contributors
* @LaurenceJJones made their first contribution in https://github.com/coollabsio/coolify-cli/pull/36

**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/1.0.3...v1.0.4

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/v1.0.4)

---

## 1.0.3: 1.0.3
**Published:** 2025-10-17

## What's Changed
* Update README with CLI command fixes by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/26
* Add minimum version checks to CLI commands by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/28
* Add CONTRIBUTING.md file by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/27


**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/1.0.2...1.0.3

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/1.0.3)

---

## 1.0.2: 1.0.2
**Published:** 2025-10-17

## What's Changed
* Add coolify config command by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/24
* Add context verify command by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/25


**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/1.0.1...1.0.2

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/1.0.2)

---

## 1.0.1: 1.0.1
**Published:** 2025-10-17

## What's Changed
* Proposal: Restructure of commands by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/21
* Fix: missing flags for some commands by @YaRissi in https://github.com/coollabsio/coolify-cli/pull/22
* Refactor: Use 'context' instead of 'instance' terminology by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/23

## New Contributors
* @YaRissi made their first contribution in https://github.com/coollabsio/coolify-cli/pull/21

**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/1.0.0...1.0.1

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/1.0.1)

---

## 1.0.0: 1.0.0
**Published:** 2025-10-16

We refactored the whole CLI to be usable everywhere. 

Sorry for breaking changes.

## What's Changed
* fix: MacOS shows unsupported architecture by @scmmishra in https://github.com/coollabsio/coolify-cli/pull/1
* feat: Complete CLI restructure with layered architecture by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/11
* fix cmd typo prompting user to update coolify by @jizaymes in https://github.com/coollabsio/coolify-cli/pull/9
* chore: update Go dependencies to fix security vulnerabilities by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/12
* feat: add Conductor workspace configuration by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/13
* docs: update CLAUDE.md with correct test commands by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/14
* Refactor cli and use all available endpoints by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/16
* update README.md by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/17
* Enhance install script with features and error handling by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/18
* Add HOW-TO-RELEASE.md for CLI by @andrasbacsai in https://github.com/coollabsio/coolify-cli/pull/19

## New Contributors
* @scmmishra made their first contribution in https://github.com/coollabsio/coolify-cli/pull/1
* @andrasbacsai made their first contribution in https://github.com/coollabsio/coolify-cli/pull/11
* @jizaymes made their first contribution in https://github.com/coollabsio/coolify-cli/pull/9

**Full Changelog**: https://github.com/coollabsio/coolify-cli/compare/0.0.1...1.0.0

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/1.0.0)

---

## 0.0.2-rc1: 0.0.2-rc1
**Published:** 2025-04-20
**Pre-release**

Hey everyone! 👋

I’m excited to introduce myself as one of the new maintainer of the cli-coolify project. I've been working on improving the CLI experience, and today I’m releasing an early Release Candidate (RC) for you to try out.

🆕 Notable Changes

Here’s a quick overview of what’s new under the hood:

- 🫧 Bubbletea-based UI
    The CLI now uses [Bubbletea](https://github.com/charmbracelet/bubbletea), a powerful TUI (Text User Interface) framework for Go. This enables interactive prompts, cleaner output, and a more intuitive UX overall — especially useful as we grow the feature set.

- 🧹 Codebase Refactor
    The project has undergone a full refactor to better support a long-term roadmap. It’s now more modular, readable, and easier to contribute to. In future we will publish a full roadmap of the CLI to allow the community to contribute. #2 

- ⚙️ Golang SDK Generation
    The CLI now uses a generated Go SDK from the Coolify openapi.yaml file. This ensures tighter alignment with the backend API, reduces the chance of client-side panics, and makes updates more maintainable. #6 

💬 Call for Feedback

This RC is very work in progress — not all commands from v0.0.1 are available yet, but your input now will shape what comes next. I’d really appreciate it if you could:

✅ Test the new CLI binary
📝 Share feedback or report issues here:
👉 https://github.com/coollabsio/cli-coolify/issues/7

> [!TIP]
> The current configuration within your `~/.config/coolify` is compatible with this RC, however, some items such as version have been stripped from the `configuration` and is now built into the binary itself.

I'm particularly interested in:

- Whether the new experience feels intuitive
- Any bugs, quirks, or regressions you hit
- Suggestions for improving command structure or flow

🧰 How to Test

Recommend steps for testing:

Make a temporary directory:
```bash
cd $(mktemp -d)
```

Grab the link from this release of the platform and arch you are on and run:
```bash
wget "https://github.com/coollabsio/cli-coolify/releases/download/0.0.2-rc1/coolify_0.0.2-rc1_linux_amd64.tar.gz" 
```

Decompress the tar.gz file:
```bash
tar xzf coolify_0.0.2-rc1_linux_amd64.tar.gz
```

Now you can run the coolify binary using relative path:
```bash
./coolify --help
```

> [!WARNING]
> Do not currently replace your coolify binary within `/usr/local/bin` until we released `0.0.2` as stable

Thank you for being part of the Coolify community! Your feedback is essential to shaping this tool to better fit your workflows.

Laurence

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/0.0.2-rc1)

---

## 0.0.1: 0.0.1
**Published:** 2024-03-06

Initial release.

[View on GitHub](https://github.com/coollabsio/coolify-cli/releases/tag/0.0.1)

---

