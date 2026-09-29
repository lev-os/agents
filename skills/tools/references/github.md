---
name: gh
description: Use when a task needs GitHub repositories, issues, pull requests, Actions, releases, discussions, or API/GraphQL access through gh.
---

# GitHub CLI

Use the installed `gh` as the transport. The executable and its live help are
the command contract; this file supplies routing, structured output, and
fallbacks for version-dependent capabilities.

## Target and authentication

Run commands from the named project root so `gh` can resolve its remote. Pass
`--repo OWNER/REPO` when the target is explicit or the current directory is not
that repository. Check authentication without exposing a token; use the JSON
form only when the current `gh auth status --help` exposes it:

```bash
gh auth status
gh auth status --json hosts
```

Use `gh auth login` only when the user asks to establish a session.

## Discover before use

For a command or flag that has not been used in this session, run its exact
help first:

```bash
gh <group> --help
gh <group> <command> --help
```

Some installations accept a command but show parent help or return a preview
feature error. Treat that as unsupported for the current run and use `gh api`
or GraphQL. Do not infer support from a zero exit status alone.

## Structured reads

Prefer `--json` with an explicit field list, then `--jq` or `--template` for a
small result. Run `--json` without fields only to discover fields. On commands
where `-T`/`--template` is also a body-template flag, follow that command's
help rather than assuming the formatting flag. List calls
are capped; pass `--limit` and state the cap when a complete total is not
available. For raw REST collections use `--paginate`, and use GraphQL
`totalCount` when an exact count matters.

```bash
gh issue list --repo OWNER/REPO --state open --limit 100 --json number,title,url
gh pr view 42 --repo OWNER/REPO --json number,title,author,mergeStateStatus
gh api --paginate repos/OWNER/REPO/issues --jq '.[] | {number,title}'
```

Search and list have different query parsing. `gh search issues|prs|code|repos|commits|users`
accepts each qualifier as its own token (`repo:OWNER/REPO is:open`); quote
only multi-word free text. `gh issue list --search` and `gh pr list --search`
take the complete query as one quoted flag value. For bot-authored work,
`--app dependabot` matches the GitHub App while `--author dependabot` generally
does not; use the exact bot login when the command requires `--author`.

For search-vs-list quoting and bots, issue relationships, attachment constraints,
discussions, remote contents, or worktree flags, read
[compatibility details](github-compatibility.md). Its version-sensitive examples
require exact live-help support before use.

## Capability routes

| Need | Preferred route | Fallback or caveat |
|---|---|---|
| Repository, clone, fork, file tree | `gh repo ...` | `gh api repos/OWNER/REPO` and `contents/...` |
| Issues, labels, comments, assignments | `gh issue ...` | REST `issues/...` endpoints |
| Pull requests, checks, reviews, diff | `gh pr ...` | REST `pulls/...`, `issues/.../comments`, and review endpoints |
| Actions workflows and runs | `gh workflow ...`, `gh run ...` | REST Actions endpoints from the live API contract |
| Releases and assets | `gh release ...` | REST `releases` and `releases/.../assets` |
| Discussions and relationships | `gh discussion ...` or `gh issue ...` relationship flags | GraphQL when the installed CLI lacks the preview command or field |
| Remote files and directories | `gh repo read-file`, `gh repo read-dir` when shown by help | REST contents API; decode a file's base64 `content` |
| Arbitrary REST or GraphQL | `gh api`, `gh api graphql` | Read the endpoint schema first when it mutates state |

### Issues and pull requests

The common route is:

```bash
gh issue list --repo OWNER/REPO --limit 50
gh issue view 123 --repo OWNER/REPO --comments
gh pr list --repo OWNER/REPO --limit 50
gh pr view 42 --repo OWNER/REPO --comments
gh pr checks 42 --repo OWNER/REPO
gh pr diff 42 --repo OWNER/REPO
```

`gh pr view --comments` exposes issue-level conversation comments. Review-thread
comments on changed lines are a separate API surface; use the REST pull-request
review-comments endpoint or a GraphQL query when that distinction matters.

For create/edit/review/comment/merge, inspect the exact help immediately before
the mutation, show the prepared command, and require the user's existing
authorization for that effect. `gh pr checkout` changes local branch state;
use a worktree option when the help exposes one and isolation is requested.

Newer `gh issue` versions may expose issue types, parents, sub-issues,
blocking, and blocked-by relationships. If help does not show those flags,
use the matching REST or GraphQL mutation instead. Compare nested `nodes` and
`totalCount` when relationship fields are capped.

### Attachments and discussions

Some `gh` versions expose `--attach` for issue/PR create, edit, and comments.
Check each command's help before using it. If supported, quote paths that
contain `#` so the shell preserves alt text:

```bash
gh pr create --title "Title" --body-file ./body.md --attach './screen.png#Login state'
```

Check the per-command help for attachment count, host, and permission limits.
The public CLI's upload support is version and host dependent, may cap a
single invocation at 50 files, requires a supported GitHub host and write
permission, and cannot be combined with some web or dry-run modes. Uploads can
partially succeed; record the returned issue or PR URL and report the first
failed attachment. When `--attach` is absent, keep the body in a `--body-file`
and use a provider-supported upload or an already-hosted URL.

Discussions are preview/version-dependent. If `gh discussion --help` exposes
the group, use its `list`, `view`, `create`, `edit`, and `comment` commands
with live help. Otherwise use `gh api graphql` with the repository's
discussion schema and verify the returned node or URL; do not silently treat
an issue as a discussion.

### Actions and releases

Use live help for workflow names, inputs, and permissions:

```bash
gh workflow list --repo OWNER/REPO
gh run list --repo OWNER/REPO --limit 20
gh run view RUN_ID --repo OWNER/REPO --log-failed
gh run watch RUN_ID --repo OWNER/REPO
gh workflow run WORKFLOW --repo OWNER/REPO -f key=value
gh run rerun RUN_ID --repo OWNER/REPO --failed
```

`workflow run`, rerun, cancellation, and release operations mutate remote
state. Confirm the exact workflow/ref/environment and inspect resulting run or
release IDs. Release assets use `gh release upload` and `gh release download`
when those commands are present; REST is the fallback for installations that
only expose core release commands.

## API and GraphQL fallback

Use `gh api` for an endpoint or field missing from a typed command. REST
examples:

```bash
gh api repos/OWNER/REPO
gh api repos/OWNER/REPO/pulls/42/comments --paginate
gh api repos/OWNER/REPO/actions/runs --paginate --jq '.workflow_runs[] | {id,name,status}'
gh api repos/OWNER/REPO/contents/path/to/file --jq '.content'
```

Use `-f` for strings and `-F` for typed values. Adding fields selects POST
unless `--method GET` is explicit; distinguish read parameters from mutations. `-X PATCH` or `-X DELETE`
changes state and requires the same mutation gate as a typed command. For
GraphQL, pass a query with `-f query=...` and variables with `-f` or `-F`; keep
the query small and inspect `errors` before consuming `data`.

```bash
gh api graphql -f query='query { viewer { login } }'
```

## Completion evidence

Return the command path, target repository, operation result, and resulting ID
or URL. For reads, include the applied limit or pagination result. For Actions,
discussions, uploads, and API calls, distinguish command success from provider
success (`status`, `ok`, or GraphQL `errors`). Preserve uncertain external
effects as uncertain and do not retry a mutation blindly.
