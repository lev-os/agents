---
name: twg
description: Use when connecting to Atlassian or using Teamwork Graph, TWG, Rovo or Robo search, Jira, Confluence, and connected work context through the TWG CLI.
---

# Teamwork Graph (TWG)

Use Atlassian's official `twg` CLI. "Robo" is a user alias for Rovo.
This leaf belongs to Tools. It does not install another agent or replace `acli`.
For installation or login, read [INSTALL.md](INSTALL.md) before changing the host.
Rovo Dev (`acli rovodev`) is a separate coding agent. An explicit Rovo Dev
request does not authorize a TWG substitute.

## Resolve the command and account

1. Resolve the requested operation, site, account/profile, and resource.
   Use the named site. In the Ulta workspace, the existing target is
   `ulta.atlassian.net`; do not apply that default to unrelated projects.
   Done: the site and intended read or write are explicit.
2. Inspect live help before unfamiliar syntax:
   ```bash
   command -v twg
   twg --version
   twg help describe "confluence content get"
   twg help describe "rovo search"
   ```
   Use `twg help <terms>` to locate another native family, then describe it.
   Done: command arguments and flags come from the installed CLI.
3. Inspect identity with `twg auth profile list -o json`, then
   `twg whoami --site <site> --profile <profile> -o json` and
   `twg doctor --site <site> --profile <profile> -o json`.
   Select an existing matching profile. Login requires user authorization.
   Done: the selected account/site is confirmed, or authentication is pending.

## Read and search

For an exact Confluence ID or URL, prefer the native content read:

```bash
twg confluence content get <id-or-url> --detail full --format html --include-metadata --site <site> --profile <profile> -o json
```

For a fuzzy work-context request, use Rovo search:

```bash
twg rovo search "<topic>" --app confluence --space <space-key> --limit 20 --site <site> --profile <profile> -o json
```

For Jira records, use the native Jira family after inspecting its help.
For another connected product, inspect the available TWG command/connector.
Existing provider leaves, such as Slack, remain the owner for explicit
provider-native work unless the user requests cross-product TWG discovery.

Read returned metadata and body before claiming that content was retrieved.
Preserve source URLs, versions, per-item errors, and any snapshot token needed
by a later edit. Markdown output is lossy; use full HTML when preparing edits.

Rovo search is top-K, not an exhaustive or cursor-paginated census. Inspect
`resultInfo.partial`, warnings, failures, and source coverage. Exit 3 means
incomplete coverage: preserve useful results and report the missing sources.
An empty partial search does not establish absence. A permission failure needs
a native read of an already-known resource or an explicit access limitation.
Changing search wording does not repair permissions.

## Authenticate, mutate, and recover

Keep OAuth tokens, Bitbucket tokens, credential files, and authentication
headers out of arguments, prompts, source, and logs. Let the user complete
browser sign-in, site selection, access consent, and any CAPTCHA. Do not save
device codes or OAuth activation URLs in evidence. Preserve existing profiles;
`--force` is for an explicitly authorized replacement of the selected login.

TWG has the account's existing permissions. Login does not restore missing DSP
edit access or grant administrator access. Credentials for `acli`, browser
sessions, and TWG are separate authorities. Bitbucket/admin authentication
requires its own scoped setup; do not request broad admin keys for a page read.

A read request does not authorize creation, edits, comments, permission changes,
or outbound messages. For an authorized write, inspect its live contract and
current resource first. Preserve required draft/version/snapshot preconditions.
Verify the resulting ID, URL, and readback. A timeout leaves an uncertain effect:
look up the resource before any retry. Stop when the lookup cannot settle it.

Report CLI availability, skill routing, authentication, and target access
separately. Exit zero or an installed executable alone does not prove provider
success. Stop at missing consent, unsupported scopes, or denied access without
changing permissions or replacing credentials.
