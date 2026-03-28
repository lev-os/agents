# here.now API Reference

Base URL: `https://here.now`

## Authentication

Two modes:

- **Authenticated**: include `Authorization: Bearer <API_KEY>` header.
- **Anonymous**: omit the header entirely. Sites expire in 24 hours with lower limits.

### Optional client attribution header

You can include an optional header on site API calls:

- `X-HereNow-Client: <agent>/<tool>`

Examples:

- `X-HereNow-Client: cursor/publish-sh`
- `X-HereNow-Client: claude-code/publish-sh`
- `X-HereNow-Client: codex/cli`
- `X-HereNow-Client: openclaw/direct-api`

This helps here.now debug publish reliability by client. Missing or invalid values are ignored; publishes are never rejected because this header is absent.

### Getting an API key

There are two ways to obtain an API key:

#### Option A: Agent-assisted sign-up

The sign-up flow can be completed entirely within the agent, without requiring the user to open a browser.

**1. Request a one-time code by email:**

```bash
curl -sS https://here.now/api/auth/agent/request-code \
  -H "content-type: application/json" \
  -d '{"email": "user@example.com"}'
```

Response:

```json
{ "success": true, "requiresCodeEntry": true, "expiresAt": "2026-03-01T12:34:56.000Z" }
```

**2. User copies the code from email** and pastes it into the agent.

**3. Verify code and receive API key:**

```bash
curl -sS https://here.now/api/auth/agent/verify-code \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
```

Response:

```json
{
  "success": true,
  "email": "user@example.com",
  "apiKey": "<API_KEY>",
  "isNewUser": true
}
```

If the code is invalid or expired, verify returns `400`.

**4. Save the API key to the credentials file:**

```bash
mkdir -p ~/.herenow && echo "<API_KEY>" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
```

#### Option B: Dashboard sign-up

Users can also sign in at [here.now](https://here.now) and copy their API key from the dashboard. The key should then be saved to the credentials file using the same command as step 4 above.

### Storing the API key

The publish script reads the API key from these sources (first match wins):

1. `--api-key {key}` flag (CI/scripting only — avoid in interactive use)
2. `$HERENOW_API_KEY` environment variable
3. `~/.herenow/credentials` file (recommended)

The credentials file is the recommended storage method. Avoid passing the key via CLI flags in interactive sessions.

## Endpoints

### Create a new site

`POST /api/v1/publish` (alias: `POST /api/v1/artifact`)

Creates a new site with a random slug. Works with or without authentication.

**Request body:**

```json
{
  "files": [
    { "path": "index.html", "size": 1234, "contentType": "text/html; charset=utf-8", "hash": "a1b2c3d4..." },
    { "path": "assets/app.js", "size": 999, "contentType": "text/javascript; charset=utf-8", "hash": "e5f6a7b8..." }
  ],
  "ttlSeconds": null,
  "viewer": {
    "title": "My site",
    "description": "Published by an agent",
    "ogImagePath": "assets/cover.png"
  }
}
```

- `files` (required): array of `{ path, size, contentType, hash }`. At least one file. Paths should be relative to the site root (e.g. `index.html`, `assets/style.css`) — don't include a parent directory name like `my-project/index.html`.
- `hash` (optional): SHA-256 hex digest (64 lowercase chars) of the file contents. When updating an existing site, files whose hash matches the previous version are skipped from `upload.uploads[]` and listed in `upload.skipped[]` instead. The server copies them automatically at finalize. Omitting `hash` gives the default behavior (all files require upload).
- `ttlSeconds` (optional): expiry in seconds. Ignored for anonymous sites (always 24h).
- `viewer` (optional): metadata for auto-viewer pages (only used when no `index.html`).

**Response (authenticated):**

```json
{
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "status": "pending",
  "isLive": false,
  "requiresFinalize": true,
  "note": "Site created, but this slug is not live yet. Upload all files to upload.uploads[], then POST upload.finalizeUrl with {\"versionId\":\"...\"}.",
  "upload": {
    "versionId": "01J...",
    "uploads": [
      {
        "path": "index.html",
        "method": "PUT",
        "url": "https://<presigned-r2-url>",
        "headers": { "Content-Type": "text/html; charset=utf-8" }
      }
    ],
    "skipped": ["assets/app.js"],
    "finalizeUrl": "https://here.now/api/v1/publish/bright-canvas-a7k2/finalize",
    "expiresInSeconds": 3600
  }
}
```

**This step only creates a pending site. It is not complete yet.**

- You **must upload every file** in `upload.uploads[]`.
- Files in `upload.skipped[]` are unchanged from the previous version and will be copied server-side at finalize. Do not upload them.
- Then you **must finalize** with `POST upload.finalizeUrl` and body `{ "versionId": "..." }`.
- For brand-new slugs, `siteUrl` may return 404 until finalize succeeds.
- For updates to an existing slug, the previous version can stay live until finalize switches to the new version.

**Response (anonymous), additional fields:**

```json
{
  "claimToken": "abc123...",
  "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123...",
  "expiresAt": "2026-02-19T01:00:00.000Z",
  "anonymous": true,
  "warning": "IMPORTANT: Save the claimToken and claimUrl. They are returned only once and cannot be recovered. Share the claimUrl with the user so they can keep the site permanently."
}
```

**IMPORTANT: The `claimToken` and `claimUrl` are returned only once and cannot be recovered. Always save the `claimToken` and share the `claimUrl` with the user so they can claim the site and keep it permanently. If you lose the claim token, the site will expire in 24 hours with no way to save it.**

`claimToken`, `claimUrl`, and `expiresAt` are only present for anonymous sites. Authenticated sites do not include these fields.

---

### Upload files

For each entry in `upload.uploads[]`, PUT the file to the presigned URL:

```bash
curl -X PUT "<presigned-url>" \
  -H "Content-Type: <content-type>" \
  --data-binary @<local-file>
```

Uploads can run in parallel. Presigned URLs are valid for 1 hour.

---

### Finalize a site

`POST /api/v1/publish/:slug/finalize` (alias: `POST /api/v1/artifact/:slug/finalize`)

Makes the site live by flipping the slug pointer to the new version.

**Request body:**

```json
{ "versionId": "01J..." }
```

**Auth:**
- Owned sites: requires `Authorization: Bearer <API_KEY>`.
- Anonymous sites: no auth required for finalize.

**Response:**

```json
{
  "success": true,
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "previousVersionId": null,
  "currentVersionId": "01J..."
}
```

---

### Update an existing site

`PUT /api/v1/publish/:slug` (alias: `PUT /api/v1/artifact/:slug`)

Same request body as create. Returns new presigned upload URLs and a new `finalizeUrl`.
The update response also includes `status: "pending"` and `isLive: false` to indicate the new version is not live until finalize.

**Incremental deploys:** Include `hash` (SHA-256 hex) on each file. Files whose hash matches the previous version appear in `upload.skipped[]` instead of `upload.uploads[]` — no upload needed. The server copies them at finalize. This is the recommended approach for iterative development.

**Auth for owned sites:** requires `Authorization: Bearer <API_KEY>` matching the owner.

**Auth for anonymous sites:** include `claimToken` in the request body:

```json
{
  "files": [...],
  "claimToken": "<claimToken>"
}
```

Anonymous updates do not extend the original expiration timer. Returns `410 Gone` if expired.

---

### Claim an anonymous site

`POST /api/v1/publish/:slug/claim` (alias: `POST /api/v1/artifact/:slug/claim`)

Transfers ownership to an authenticated user and removes the expiration.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{ "claimToken": "abc123..." }
```

**Response:**

```json
{
  "success": true,
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "expiresAt": null
}
```

Users can also claim by visiting the `claimUrl` in a browser and signing in.

---

### Password protection

Add a password to any site so visitors must authenticate before viewing. This is server-side enforcement — content is never sent to the browser until the password is verified. All files under the site are protected, not just the index page.

Set or change a password via `PATCH /api/v1/publish/:slug/metadata` with `{"password": "secret"}`. Remove it with `{"password": null}`. You can also manage passwords from the dashboard via the `⋯` menu on each site.

Password protection survives redeploys — it's metadata, not content. Changing or removing a password immediately invalidates all existing sessions. Requires an authenticated site (anonymous sites cannot be password-protected).

Payment gating and password protection are mutually exclusive. Setting a price removes the password, and setting a password removes the price.

---

### Payment gating

Require visitors to pay with stablecoins on the Tempo network before accessing your site. Payments go directly from the visitor's wallet to yours.

**Setup:**

1. Set your Tempo wallet address: `PATCH /api/v1/wallet` with `{"address": "0x..."}`.
2. Set a price on any site: `PATCH /api/v1/publish/:slug/metadata` with `{"price": {"amount": "0.50", "currency": "USD"}}`.

Visitors see a payment page with a QR code and deposit address. After paying, access is granted permanently.

Payment gating survives redeploys. Changing or removing the price immediately invalidates all existing access sessions. Requires an authenticated site with a wallet address configured.

#### 402 response for agents

When a programmatic client (non-browser) hits a paid site, the response includes the MPP `WWW-Authenticate: Payment` challenge header plus a JSON body with session URLs for agents that don't have mppx installed:

```json
{
  "price": {
    "amount": "0.10",
    "currency": "USD",
    "recipientAddress": "0xe661..."
  },
  "paymentSession": {
    "createUrl": "https://here.now/api/pay/<slug>/session",
    "pollUrl": "https://here.now/api/pay/<slug>/poll",
    "grantUrl": "https://here.now/api/pay/<slug>/grant"
  },
  "walletUrl": "https://wallet.tempo.xyz/"
}
```

**Session flow (for agents without mppx):**

1. `POST <createUrl>` with `{}` to create a payment session. Returns `{ sessionId, address, amount, currency, expiresAt }`.
2. Show the user the deposit address and amount. The address is unique to this session.
3. `POST <pollUrl>` with `{ "sessionId": "<id>" }` every few seconds. Returns `{ found: true, txHash }` when payment is detected.
4. `POST <grantUrl>` with `{ "sessionId": "<id>", "txHash": "<hash>" }`. Returns `{ token }`.
5. Fetch the original URL with `?__hn_grant=<token>` to retrieve the content.

Sessions expire after 30 minutes. Create a new session if the current one expires.

---

### Wallet management

`GET /api/v1/wallet`

Returns the Tempo wallet address for the authenticated user.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{
  "address": "0xe66178B0D33807f5efb2069f9252eD02c13bbF59"
}
```

`PATCH /api/v1/wallet`

Set, change, or remove the wallet address.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{
  "address": "0xe66178B0D33807f5efb2069f9252eD02c13bbF59"
}
```

Set `address` to `null` to remove. Must be a valid `0x`-prefixed 40-character hex address.

**Response:**

```json
{
  "success": true,
  "address": "0xe66178B0D33807f5efb2069f9252eD02c13bbF59"
}
```

---

### Duplicate a site

`POST /api/v1/publish/:slug/duplicate`

Creates a complete server-side copy of the site under a new slug. All files are copied server-side — no client upload or finalize step needed. The new site is immediately live.

Copies all files and viewer metadata. Does not copy password protection, handle/domain links, or TTL.

**Requires:** `Authorization: Bearer <API_KEY>` (must own the source site)

**Request body:** (optional)

```json
{
  "viewer": {
    "title": "My Copy",
    "description": "Copy of bright-canvas-a7k2"
  }
}
```

- `viewer` (optional): Shallow-merged with the source site's viewer metadata. Only provided fields are overridden; omitted fields are preserved from the source. If `viewer` is omitted entirely, the source's metadata is copied as-is.

**Response:**

```json
{
  "slug": "warm-lake-f3k9",
  "siteUrl": "https://warm-lake-f3k9.here.now/",
  "sourceSlug": "bright-canvas-a7k2",
  "status": "active",
  "currentVersionId": "01J...",
  "filesCount": 36
}
```

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid API key |
| 403 | API key doesn't match the source site's owner |
| 404 | Source slug doesn't exist or is deleted |
| 409 | Source site is in `pending` status (not yet finalized) |
| 429 | Rate limit exceeded |

---

### Patch metadata

`PATCH /api/v1/publish/:slug/metadata` (alias: `PATCH /api/v1/artifact/:slug/metadata`)

Update title, description, og:image, TTL, password, or price without re-uploading files.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{
  "ttlSeconds": 604800,
  "viewer": {
    "title": "Updated title",
    "description": "New description",
    "ogImagePath": "assets/cover.png"
  },
  "password": "secret123",
  "price": {
    "amount": "0.50",
    "currency": "USD"
  }
}
```

All fields optional. `ogImagePath` must reference an image file within the current site.

- `password`: string to set or change, `null` to remove, omit for no change. When set, visitors must enter the password before any content is served. Server-side enforcement. Changing or removing the password immediately invalidates all existing sessions.
- `price`: object to set, change, or remove. `null` removes the price, omit for no change. To change the price, set it again with the new amount (existing access sessions are invalidated). Requires a wallet address on the account (see Wallet management). Fields:
  - `amount` (required): price in USD as a string (e.g. `"0.50"`, `".25"`, `"5"`)
  - `currency` (required): `"USD"`
  - `recipientAddress` (optional): per-site wallet override. If omitted, uses the account-level wallet address.
- Password and price are mutually exclusive. Setting one removes the other. The response includes `passwordRemoved: true` or `priceRemoved: true` when this happens.

**Response:**

```json
{
  "success": true,
  "effectiveForRootDocument": true,
  "priced": true,
  "recipientAddress": "0xe66178B0D33807f5efb2069f9252eD02c13bbF59"
}
```

If the site has an `index.html`, viewer metadata is stored but the site's own HTML controls what browsers see.

---

### Delete a site

`DELETE /api/v1/publish/:slug` (alias: `DELETE /api/v1/artifact/:slug`)

Hard deletes the site, all versions, and the slug-index entry.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{ "success": true }
```

---

### List sites

`GET /api/v1/publishes` (alias: `GET /api/v1/artifacts`)

Returns all sites owned by the authenticated user.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{
  "publishes": [
    {
      "slug": "bright-canvas-a7k2",
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      "updatedAt": "2026-02-18T...",
      "expiresAt": null,
      "status": "active",
      "currentVersionId": "01J...",
      "pendingVersionId": null
    }
  ]
}
```

---

### Get site details

`GET /api/v1/publish/:slug` (alias: `GET /api/v1/artifact/:slug`)

Returns metadata and the full file manifest for a site you own.

**Requires:** `Authorization: Bearer <API_KEY>` (owner only)

**Response:**

```json
{
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "status": "active",
  "createdAt": "2026-02-18T...",
  "updatedAt": "2026-02-18T...",
  "expiresAt": null,
  "currentVersionId": "01J...",
  "pendingVersionId": null,
  "manifest": [
    { "path": "index.html", "size": 1234, "contentType": "text/html; charset=utf-8", "hash": "a1b2c3d4..." },
    { "path": "assets/app.js", "size": 999, "contentType": "text/javascript; charset=utf-8", "hash": "e5f6a7b8..." }
  ]
}
```

The `manifest` array lists all files in the current live version with their paths, sizes, content types, and hashes (if available). File contents can be fetched from the live `siteUrl` (e.g. `https://bright-canvas-a7k2.here.now/index.html`).

---

### Refresh upload URLs

`POST /api/v1/publish/:slug/uploads/refresh` (alias: `POST /api/v1/artifact/:slug/uploads/refresh`)

Returns fresh presigned URLs for a pending upload (same version, no new version created).

**Requires:** `Authorization: Bearer <API_KEY>`

Use when presigned URLs expire mid-upload (they're valid for 1 hour).

---

### Register a handle

`POST /api/v1/handle`

Registers your handle for `handle.here.now`. Requires a paid plan (Hobby or above). Returns 403 with `upgrade_url` on the free plan.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{ "handle": "yourname" }
```

**Response:**

```json
{
  "handle": "yourname",
  "hostname": "yourname.here.now",
  "namespace_id": "uuid"
}
```

Handle rules: 2-30 chars, lowercase letters/numbers/hyphens, no leading/trailing hyphen, reserved names blocked.

---

### Get current handle

`GET /api/v1/handle`

Returns your current handle and links.

**Requires:** `Authorization: Bearer <API_KEY>`

---

### Change handle

`PATCH /api/v1/handle`

Changes an existing handle to a new one. Requires a paid plan (Hobby or above). Returns 403 with `upgrade_url` on the free plan.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{ "handle": "newname" }
```

---

### Delete handle

`DELETE /api/v1/handle`

Deletes your handle and all links under it.

**Requires:** `Authorization: Bearer <API_KEY>`

---

### Add a custom domain

`POST /api/v1/domains`

Registers a custom domain for your account. Free plan: 1 domain. Hobby plan: up to 5 domains.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{ "domain": "example.com" }
```

**Response (apex domain example):**

```json
{
  "domain": "example.com",
  "namespace_id": "uuid",
  "status": "pending",
  "is_apex": true,
  "dns_instructions": {
    "type": "ALIAS",
    "name": "example.com",
    "target": "fallback.here.now",
    "note": "Add an ALIAS record (sometimes called ANAME or CNAME flattening) pointing to fallback.here.now."
  },
  "ownership_verification": {
    "type": "txt",
    "name": "_cf-custom-hostname.example.com",
    "value": "uuid-token"
  }
}
```

**DNS setup by domain type:**

- **Subdomains** (e.g. `docs.example.com`): Add a **CNAME** record pointing to `fallback.here.now`.
- **Apex domains** (e.g. `example.com`):
  1. Add an **ALIAS** record pointing to `fallback.here.now`. (Your DNS provider may call this ANAME or CNAME flattening.)
  2. Add a **TXT** record using the `name` and `value` from `ownership_verification`.

SSL is provisioned automatically once DNS is verified.

---

### List custom domains

`GET /api/v1/domains`

Returns all custom domains for the authenticated user, including their status and links.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{
  "domains": [
    {
      "domain": "example.com",
      "namespace_id": "uuid",
      "status": "active",
      "ssl_status": "active",
      "is_apex": true,
      "created_at": "2026-03-09T...",
      "verified_at": "2026-03-09T...",
      "mounts": [
        { "mount_path": "", "slug": "bright-canvas-a7k2" }
      ]
    }
  ]
}
```

For pending domains, this endpoint also polls Cloudflare for SSL verification status and updates automatically. Apex domains include `ownership_verification` with TXT record details.

---

### Get custom domain status

`GET /api/v1/domains/:domain`

Returns details for a specific custom domain. Triggers on-demand verification for pending domains. Includes `is_apex`, `ownership_verification` (for apex domains), and `verification_errors` (when applicable).

**Requires:** `Authorization: Bearer <API_KEY>`

---

### Remove a custom domain

`DELETE /api/v1/domains/:domain`

Removes a custom domain and all links under it.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{ "deleted": true }
```

---

### Create a link under your handle or custom domain

`POST /api/v1/links`

Links a site slug to a location under your handle or a custom domain.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{
  "location": "docs",
  "slug": "bright-canvas-a7k2"
}
```

Use an empty `location` to link at root (`https://yourname.here.now/`).

To link to a custom domain instead of your handle, add the `domain` parameter:

```json
{
  "location": "",
  "slug": "bright-canvas-a7k2",
  "domain": "example.com"
}
```

This makes `https://example.com/` serve the site. The domain must be active (verified).

---

### List links under your handle

`GET /api/v1/links`

Lists all links for your current handle.

**Requires:** `Authorization: Bearer <API_KEY>`

---

### Get one link

`GET /api/v1/links/:location`

Gets a single link by location. Use `__root__` for the root location.

**Requires:** `Authorization: Bearer <API_KEY>`

---

### Update one link

`PATCH /api/v1/links/:location`

Changes which site slug a location points to.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{ "slug": "another-slug-x9f1" }
```

---

### Delete one link

`DELETE /api/v1/links/:location`

Removes a link by location. Use `__root__` for the root location.

**Requires:** `Authorization: Bearer <API_KEY>`

To delete a link from a custom domain (instead of your handle), add `?domain=example.com` as a query parameter.

---

### Start checkout (paid plan)

`POST /api/v1/billing/checkout`

Creates a Stripe checkout session for the Hobby plan.

**Requires:** `Authorization: Bearer <API_KEY>` (or browser session auth).

**Response:**

```json
{ "url": "https://checkout.stripe.com/..." }
```

---

### Open billing portal

`POST /api/v1/billing/portal`

Creates a Stripe billing portal session.

**Requires:** `Authorization: Bearer <API_KEY>` (or browser session auth).

**Response:**

```json
{ "url": "https://billing.stripe.com/..." }
```

---

Handle and link changes are written to Cloudflare KV and may take up to 60 seconds to propagate globally.

---

## URL Structure

Each site gets its own subdomain: `https://<slug>.here.now/`

Asset paths work naturally from the subdomain root:
- `/styles.css`, `/images/a.jpg` resolve as expected
- Relative paths (`styles.css`, `./images/a.jpg`) also work

### Serving rules

1. If `index.html` exists at root → serve it as the document.
2. Else if exactly one file in the entire site → serve an auto-viewer page (images, PDF, video, audio get rich viewers; everything else gets a download page).
3. Else if an `index.html` exists in any subdirectory → serve the first one found.
4. Otherwise → serve an auto-generated directory listing. Folders are clickable, images render as a gallery, and other files are listed with sizes. No `index.html` required.

Direct file paths always work: `https://<slug>.here.now/report.pdf`

## Limits

|                | Anonymous          | Authenticated                |
| -------------- | ------------------ | ---------------------------- |
| Max file size  | 250 MB             | 5 GB                         |
| Expiry         | 24 hours           | Permanent (or custom TTL)    |
| Rate limit     | 5 / hour / IP      | 60 / hour free, 200 / hour hobby |
| Account needed | No                 | Yes (get key at here.now)    |
