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

**Skill version: 1.9.0**

Create a live URL from any file or folder. Static hosting only.

To install or update (recommended): `npx skills add heredotnow/skill --skill here-now -g`

For repo-pinned/project-local installs, run the same command without `-g`.

## Requirements

- Required binaries: `curl`, `file`, `jq`
- Optional environment variable: `$HERENOW_API_KEY`
- Optional credentials file: `~/.herenow/credentials`

## Create a site

```bash
./scripts/publish.sh {file-or-dir}
```

Outputs the live URL (e.g. `https://bright-canvas-a7k2.here.now/`).

Under the hood this is a three-step flow: create/update -> upload files -> finalize. A site is not live until finalize succeeds.

Without an API key this creates an **anonymous site** that expires in 24 hours.
With a saved API key, the site is permanent.

**File structure:** For HTML sites, place `index.html` at the root of the directory you publish, not inside a subdirectory. The directory's contents become the site root. For example, publish `my-site/` where `my-site/index.html` exists — don't publish a parent folder that contains `my-site/`.

You can also publish raw files without any HTML. Single files get a rich auto-viewer (images, PDF, video, audio). Multiple files get an auto-generated directory listing with folder navigation and an image gallery.

## Update an existing site

```bash
./scripts/publish.sh {file-or-dir} --slug {slug}
```

The script auto-loads the `claimToken` from `.herenow/state.json` when updating anonymous sites. Pass `--claim-token {token}` to override.

Authenticated updates require a saved API key.

## Client attribution

Pass `--client` so here.now can track reliability by agent:

```bash
./scripts/publish.sh {file-or-dir} --client cursor
```

This sends `X-HereNow-Client: cursor/publish-sh` on publish API calls.
If omitted, the script sends a fallback value.

## API key storage

The publish script reads the API key from these sources (first match wins):

1. `--api-key {key}` flag (CI/scripting only — avoid in interactive use)
2. `$HERENOW_API_KEY` environment variable
3. `~/.herenow/credentials` file (recommended for agents)

To store a key, write it to the credentials file:

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

**IMPORTANT**: After receiving an API key, save it immediately — run the command above yourself. Do not ask the user to run it manually. Avoid passing the key via CLI flags (e.g. `--api-key`) in interactive sessions; the credentials file is the preferred storage method.

Never commit credentials or local state files (`~/.herenow/credentials`, `.herenow/state.json`) to source control.

## State file

After every site create/update, the script writes to `.herenow/state.json` in the working directory:

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

Before creating or updating sites, you may check this file to find prior slugs.
Treat `.herenow/state.json` as internal cache only.
Never present this local file path as a URL, and never use it as source of truth for auth mode, expiry, or claim URL.

## What to tell the user

- Always share the `siteUrl` from the current script run.
- Read and follow `publish_result.*` lines from script stderr to determine auth mode.
- When `publish_result.auth_mode=authenticated`: tell the user the site is **permanent** and saved to their account. No claim URL is needed.
- When `publish_result.auth_mode=anonymous`: tell the user the site **expires in 24 hours**. Share the claim URL (if `publish_result.claim_url` is non-empty and starts with `https://`) so they can keep it permanently. Warn that claim tokens are only returned once and cannot be recovered.
- Never tell the user to inspect `.herenow/state.json` for claim URLs or auth status.

## Limits

|                | Anonymous          | Authenticated                |
| -------------- | ------------------ | ---------------------------- |
| Max file size  | 250 MB             | 5 GB                         |
| Expiry         | 24 hours           | Permanent (or custom TTL)    |
| Rate limit     | 5 / hour / IP      | 60 / hour free, 200 / hour hobby |
| Account needed | No                 | Yes (get key at here.now)    |

## Getting an API key

To upgrade from anonymous (24h) to permanent sites:

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

5. Save the returned `apiKey` yourself (do not ask the user to do this):

```bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

## Script options

| Flag                   | Description                                  |
| ---------------------- | -------------------------------------------- |
| `--slug {slug}`        | Update an existing site instead of creating |
| `--claim-token {token}`| Override claim token for anonymous updates    |
| `--title {text}`       | Viewer title (non-HTML sites)             |
| `--description {text}` | Viewer description                            |
| `--ttl {seconds}`      | Set expiry (authenticated only)               |
| `--client {name}`      | Agent name for attribution (e.g. `cursor`)    |
| `--base-url {url}`     | API base URL (default: `https://here.now`)    |
| `--allow-nonherenow-base-url` | Allow sending auth to non-default `--base-url` |
| `--api-key {key}`      | API key override (prefer credentials file)    |

## Duplicate a site

```bash
curl -sS -X POST https://here.now/api/v1/publish/{slug}/duplicate \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Creates a full copy of the site under a new slug. All files are copied server-side — no upload needed. The new site is immediately live. Requires authentication and ownership of the source site.

Optionally override viewer metadata (shallow-merged with the source):

```bash
curl -sS -X POST https://here.now/api/v1/publish/{slug}/duplicate \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"viewer": {"title": "My Copy"}}'
```

## Beyond the script

For delete, metadata patch (including password protection and payment gating), duplicate, claim, list, and other operations, see [references/REFERENCE.md](references/REFERENCE.md).

## Payment gating

Sites can require stablecoin payment on the Tempo network before granting access. Payments go directly from the visitor's wallet to the publisher's wallet.

To receive payments you need a Tempo wallet address. Get one at [wallet.tempo.xyz](https://wallet.tempo.xyz/) or by running `npx mppx account create`.

**CLI commands:**

```bash
# Set your Tempo wallet address (once)
herenow wallet set 0xYOUR_ADDRESS --api-key $HERENOW_API_KEY

# Require payment on a site (or change an existing price)
herenow price set <slug> 0.50 --api-key $HERENOW_API_KEY

# Use a different wallet for a specific site
herenow price set <slug> 1.00 --wallet 0xOTHER_ADDRESS --api-key $HERENOW_API_KEY

# Remove payment requirement
herenow price remove <slug> --api-key $HERENOW_API_KEY

# Check your wallet address
herenow wallet --api-key $HERENOW_API_KEY
```

Payment gating and password protection are mutually exclusive. You can also manage payments from the dashboard (Wallet tab for address, site menu for pricing).

## Accessing a paid site

If you fetch a here.now URL and get a `402 Payment Required` response, the site requires payment.

**If you have Tempo wallet + mppx installed:** payment is handled automatically. No action needed.

**If you have the Tempo CLI:** run `tempo request <url>` to pay and retrieve the content.

**If you don't have Tempo:** use the payment session flow. The 402 response body includes `paymentSession` URLs:

```json
{
  "price": { "amount": "0.10", "currency": "USD" },
  "paymentSession": {
    "createUrl": "https://here.now/api/pay/<slug>/session",
    "pollUrl": "https://here.now/api/pay/<slug>/poll",
    "grantUrl": "https://here.now/api/pay/<slug>/grant"
  },
  "walletUrl": "https://wallet.tempo.xyz/"
}
```

Steps:

1. `POST <createUrl>` to get a unique deposit address and session ID
2. Show the user the amount, deposit address, and wallet link (`https://wallet.tempo.xyz/`)
3. Poll `POST <pollUrl>` with `{"sessionId": "<id>"}` every 3 seconds
4. When the response has `"found": true`, call `POST <grantUrl>` with `{"sessionId": "<id>", "txHash": "<hash>"}`
5. The response contains a `token`. Fetch the original URL with `?__hn_grant=<token>` to get the content.

Example message to the user:

> This site requires payment of $0.10 (USD) on the Tempo network.
> Send $0.10 to: 0xBd46...DbB6
> If you need a Tempo wallet: https://wallet.tempo.xyz/

The agent should poll silently and present the content once payment is detected.

## Handle

Handles are user-owned subdomain namespaces on `here.now` (for example, `yourname.here.now`) that route paths to your sites. Claiming a handle requires a paid plan (Hobby or above).

- Handle endpoints: `/api/v1/handle`
- Handle format: lowercase letters/numbers/hyphens, 2-30 chars, no leading/trailing hyphens

## Custom domains

Bring your own domain (e.g. `example.com`) and serve sites from it. Custom domains: 1 on Free, up to 5 on Hobby.

- Domain endpoints: `/api/v1/domains` and `/api/v1/domains/:domain`

### Add a custom domain

```bash
curl -sS https://here.now/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

The response includes `is_apex`, DNS instructions, and (for apex domains) an `ownership_verification` object with TXT record details.

**DNS setup by domain type:**

- **Subdomains** (e.g. `docs.example.com`): Add a **CNAME** record pointing to `fallback.here.now`.
- **Apex domains** (e.g. `example.com`):
  1. Add an **ALIAS** record pointing to `fallback.here.now`. (Your DNS provider may call this ANAME or CNAME flattening.)
  2. Add a **TXT** record using the `name` and `value` from the `ownership_verification` field in the response.

SSL is provisioned automatically once DNS is verified.

### Check domain status

```bash
curl -sS https://here.now/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```

Status is `pending` until DNS is verified and SSL is active, then becomes `active`. For apex domains, the response includes `ownership_verification` with the TXT record details and may include `verification_errors` if there are issues.

### List custom domains

```bash
curl -sS https://here.now/api/v1/domains \
  -H "Authorization: Bearer {API_KEY}"
```

### Remove a custom domain

```bash
curl -sS -X DELETE https://here.now/api/v1/domains/example.com \
  -H "Authorization: Bearer {API_KEY}"
```

Removes the domain and all links under it.

## Links

Links connect a site to a location on your handle or a custom domain. The same endpoints work for both — omit the `domain` parameter to target your handle, or include it to target a custom domain.

- Link endpoints: `/api/v1/links` and `/api/v1/links/:location`
- Root location sentinel for path params: `__root__`
- Changes propagate globally in up to 60 seconds (Cloudflare KV)

Link to your handle:

```bash
curl -sS https://here.now/api/v1/links \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"location": "docs", "slug": "bright-canvas-a7k2"}'
```

Link to a custom domain:

```bash
curl -sS https://here.now/api/v1/links \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"location": "", "slug": "bright-canvas-a7k2", "domain": "example.com"}'
```

An empty `location` makes it the homepage (e.g. `https://example.com/`). Use `"location": "docs"` for `https://example.com/docs/`.

Full docs: https://here.now/docs
