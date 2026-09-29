---
name: slack-api
description: Use when a task needs a Slack Web API method, OAuth scope or token type, cursor pagination, rate-limit handling, or diagnosis of Slack API errors.
---

# Slack Web API

Use this reference for the method layer. The live method index and each
method's contract are the source of truth for HTTP method, arguments, token
type, scopes, errors, and rate tier:

- Index: <https://docs.slack.dev/reference/methods.md>
- Web API envelope: <https://docs.slack.dev/apis/web-api.md>
- Pagination: <https://docs.slack.dev/apis/web-api/pagination.md>
- Rate limits: <https://docs.slack.dev/apis/web-api/rate-limits.md>

## Select a method

If the request names a full `family.method`, open that method's current
contract. Otherwise search the index or use the optional Slack CLI's docs
search from `./slack-cli.md`. Method names use dot notation; Slack Lists uses
`slackLists.*`.

Read the contract before calling. Capture the required arguments, HTTP method,
required scopes, accepted token types, pagination fields, and method-specific
errors. Do not invent a method or scope from a similar name.

## Credentials and scope

The Slack CLI's authenticated team session and a raw HTTP token are separate
auth paths. A raw call must use the token type named by the method contract:

- `xoxb-...`: bot token for app/bot scopes.
- `xoxp-...`: user token for methods accepting user tokens and their scopes.
- `xapp-...`: app-level token only where the contract accepts it.

Read required scopes from the method contract and granted scopes from the
actual app/token configuration; docs do not prove token access.
`admin.*` methods require the documented Enterprise Grid org token.
`auth.test` validates a supplied token, not an unauthenticated session.
Check the current contract for public methods such as `api.test` and
`blocks.validate`. Never print or place a token in a
receipt, prompt, URL, or source file.

## Call a method

Resolve `SLACK_CMD` through `./slack-cli.md` before CLI examples. For SDK work,
consult the official SDK method contract: JavaScript uses `chat.postMessage`,
Python uses `chat_postMessage`. Check replacements before deprecated methods.

Read-only calls can run under the user's authorization. Show the exact
prepared request and use the user's existing authorization for methods that
post, update, delete, archive, kick, or otherwise mutate Slack state.

Via the optional CLI, run `"$SLACK_CMD" api --help` first; method parameters
are positional `key=value`, while `--team`, `--token`, `--json`, and `--data`
are CLI flags. For a raw request, follow the method's documented encoding:

```bash
curl --fail-with-body --silent --show-error --connect-timeout 10 --max-time 60 \
  -X POST 'https://slack.com/api/conversations.list' \
  -H 'Authorization: Bearer xoxb-REDACTED' \
  -d 'types=public_channel&limit=200'
```

For structured arguments use JSON only when the contract says JSON:

```bash
curl --fail-with-body --silent --show-error --connect-timeout 10 --max-time 60 \
  -X POST 'https://slack.com/api/chat.postMessage' \
  -H 'Authorization: Bearer xoxb-REDACTED' \
  -H 'Content-Type: application/json' \
  --data '{"channel":"C0123456789","text":"Prepared message"}'
```

The timeout is a transport bound, not proof of completion. For an uncertain
mutation response, preserve the operation as uncertain and do not blindly
retry it.

## Evaluate the response

Parse JSON and check the top-level `ok` before consuming data. On `ok: false`,
branch on `error`; use `needed` and `provided` for `missing_scope`, and read
the method's errors table for `channel_not_found`, `invalid_arguments`, and
other method-specific codes. Treat a zero curl or CLI exit status as transport
success only.

For HTTP 429 or Slack `ratelimited`, honor the `Retry-After` header and retry
only a safe read or a mutation whose idempotency contract explicitly supports
retry. Do not run a tight loop.

## Cursor pagination

For a collection, use the documented page size and pass the opaque
`response_metadata.next_cursor` to the next request until it is empty:

```bash
curl --fail-with-body --silent --show-error --connect-timeout 10 --max-time 60 \
  -X POST 'https://slack.com/api/conversations.history' \
  -H 'Authorization: Bearer xoxb-REDACTED' \
  -d 'channel=C0123456789&limit=200&cursor=OPAQUE_CURSOR'
```

Never construct, decode, or reuse an old cursor. Report the number of pages
and whether the final cursor was empty.

## Block Kit payloads

Payload shape and surface compatibility live in the local `./slack-cli.md`
Block Kit section and the official Block Kit reference. Keep method selection,
auth, scopes, response handling, and pagination here; validate the payload
against the target message, modal, or Home tab surface before sending it.

## Completion evidence

Return the method, target team/resource, token type and scopes used without
revealing the token, response `ok`/`error`, pagination result, and any returned
message, view, file, or operation ID. A prepared request, successful transport,
and provider-confirmed mutation are separate states.
