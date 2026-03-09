---
name: here-now
description: >
  Publish files and folders to the web instantly. Static hosting for HTML sites,
  images, PDFs, and any file type. Use when asked to "publish this", "host this",
  "deploy this", "share this on the web", "make a website", "put this online",
  "upload to the web", "create a webpage", "share a link", "serve this site",
  or "generate a URL". Outputs a live, shareable URL at {slug}.here.now.
---

# here.now

**Skill version: 1.6.5**

Create a live URL from any file or folder. Static hosting only.

To install or update (recommended): `npx skills add heredotnow/skill --skill here-now -g`

For repo-pinned/project-local installs, run the same command without `-g`.

If npm is unavailable, see fallback install docs: https://here.now/docs#install-skill

## Requirements

- Required binaries: `curl`, `file`, `jq`
- Optional environment variable: `$HERENOW_API_KEY`
- Optional credentials file: `~/.herenow/credentials`

## Create an artifact

```bash
./scripts/publish.sh {file-or-dir}
```

Outputs the live URL (e.g. `https://bright-canvas-a7k2.here.now/`).

Under the hood this is a three-step flow: create/update -> upload files -> finalize. An artifact is not live until finalize succeeds.

Without an API key this creates an **anonymous artifact** that expires in 24 hours.
With a saved API key, the artifact is permanent.

**File structure:** For HTML sites, place `index.html` at the root of the directory you publish, not inside a subdirectory. The directory's contents become the site root. For example, publish `my-site/` where `my-site/index.html` exists — don't publish a parent folder that contains `my-site/`.

You can also publish raw files without any HTML. Single files get a rich auto-viewer (images, PDF, video, audio). Multiple files get an auto-generated directory listing with folder navigation and an image gallery.

## Update an existing artifact

```bash
./scripts/publish.sh {file-or-dir} --slug {slug}
```

The script auto-loads the `claimToken` from `.herenow/state.json` when updating anonymous artifacts. Pass `--claim-token {token}` to override.

Authenticated updates require a saved API key.

## Client attribution

Pass `--client` so here.now can track reliability by agent:

```bash
./scripts/publish.sh {file-or-dir} --client cursor
```

This sends `X-HereNow-Client: cursor/publish-sh` on artifact API calls.
If omitted, the script sends a fallback value.

## API key storage

The artifact script reads the API key from these sources (first match wins):

1. `--api-key {key}` flag (CI/scripting only — avoid in interactive use)
2. `$HERENOW_API_KEY` environment variable
3. `~/.herenow/credentials` file (recommended for agents)

To store a key, write it to the credentials file:

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

**IMPORTANT**: Never pass the API key directly in shell commands. Always write it to `~/.herenow/credentials` using the command above. This keeps the key out of terminal history and logs.

Never commit credentials or local state files (`~/.herenow/credentials`, `.herenow/state.json`) to source control.

## State file

After every artifact create/update, the script writes to `.herenow/state.json` in the working directory:

```json
{
  "publishes": {
    "bright-canvas-a7k2": {
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "claimToken": "abc123",
      "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",
      "expiresAt": "2026-02-18T01:00:00.000Z"
    }
  }
}
```

Before creating or updating artifacts, you may check this file to find prior slugs.
Treat `.herenow/state.json` as internal cache only.
Never present this local file path as a URL, and never use it as source of truth for auth mode, expiry, or claim URL.

## What to tell the user

- Always share the `siteUrl` from the current script run.
- Read and follow `publish_result.*` lines from script stderr.
- Only state "expires in 24 hours" when `publish_result.auth_mode=anonymous`.
- Only share a claim URL when `publish_result.claim_url` is non-empty and starts with `https://`.
- Never tell the user to inspect `.herenow/state.json` for claim URLs or auth status.
- Warn: claim tokens are only returned once and cannot be recovered.

## Limits

|                | Anonymous          | Authenticated                |
| -------------- | ------------------ | ---------------------------- |
| Max file size  | 250 MB             | 5 GB                         |
| Expiry         | 24 hours           | Permanent (or custom TTL)    |
| Rate limit     | 5 / hour / IP      | 60 / hour free, 200 / hour hobby |
| Account needed | No                 | Yes (get key at here.now)    |

## Getting an API key

To upgrade from anonymous (24h) to permanent artifacts:

1. Ask the user for their email address.
2. Request a one-time sign-in code:

```bash
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

3. Tell the user: "Check your inbox for a sign-in code from here.now and paste it here."
4. Verify the code and get the API key:

```bash
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

5. Save the returned `apiKey`:

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

## Script options

| Flag                   | Description                                  |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | Update an existing artifact instead of creating |
| `--claim-token {token}`| Override claim token for anonymous updates    |
| `--title {text}`       | Viewer title (non-site artifacts)             |
| `--description {text}` | Viewer description                            |
| `--ttl {seconds}`      | Set expiry (authenticated only)               |
| `--client {name}`      | Agent name for attribution (e.g. `cursor`)    |
| `--base-url {url}`     | API base URL (default: `https://here.now`)    |
| `--allow-nonherenow-base-url` | Allow sending auth to non-default `--base-url` |
| `--api-key {key}`      | API key override (prefer credentials file)    |

## Beyond the script

For delete, metadata patch, claim, list, and other operations, see [references/REFERENCE.md](references/REFERENCE.md).

## Terminology and API aliases

The API is transitioning to:

- `artifact` (formerly `publish`)
- `handle` (formerly `username`)
- `link` (formerly `mount`)

Both old and new route families are supported during the transition. Existing integrations using `/api/v1/publish*` continue to work.

## Handle and links quick reference

- Handles are user-owned subdomain namespaces on `here.now` (for example, `yourname.here.now`) that route paths to your artifacts.
- Any account with an API key can claim a handle.
- Handle endpoints: `/api/v1/handle`
- Link endpoints: `/api/v1/links` and `/api/v1/links/:location`
- Root location sentinel for path params remains `__root__`
- Handle/link changes can take up to 60 seconds to propagate globally (Cloudflare KV)

Full docs: https://here.now/docs
