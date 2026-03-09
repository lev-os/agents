# here.now API Reference

Base URL: `https://here.now`

## Authentication

Two modes:

- **Authenticated**: include `Authorization: Bearer <API_KEY>` header.
- **Anonymous**: omit the header entirely. Artifacts expire in 24 hours with lower limits.

### Optional client attribution header

You can include an optional header on artifact API calls:

- `X-HereNow-Client: <agent>/<tool>`

Examples:

- `X-HereNow-Client: cursor/publish-sh`
- `X-HereNow-Client: claude-code/publish-sh`
- `X-HereNow-Client: codex/cli`
- `X-HereNow-Client: openclaw/direct-api`

This helps here.now debug publish reliability by client. Missing or invalid values are ignored; publishes are never rejected because this header is absent.

### Getting an API key (agent-assisted sign-up)

Agents can complete sign-up without requiring the user to open the dashboard:

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

The browser sign-in flow (`POST /api/auth/login`) remains available for normal web sessions.

## Endpoints

### Naming transition (backward compatibility)

The API is moving to new terminology:

- `publish` -> `artifact`
- `username` -> `handle`
- `mount` -> `link`

Backward compatibility is preserved:

- Existing routes continue to work (`/api/v1/publish`, `/api/v1/publishes`, `/api/v1/username`, `/api/v1/mounts`, etc.).
- New alias routes are available (`/api/v1/artifact`, `/api/v1/artifacts`, `/api/v1/handle`, `/api/v1/links`).
- New routes accept old and new request field names where applicable.

Preferred aliases:

- `POST /api/v1/artifact` (alias of `POST /api/v1/publish`)
- `GET /api/v1/artifacts` (alias of `GET /api/v1/publishes`)
- `PUT /api/v1/artifact/:slug` (alias of `PUT /api/v1/publish/:slug`)
- `POST /api/v1/artifact/:slug/finalize` (alias of `POST /api/v1/publish/:slug/finalize`)
- `POST /api/v1/artifact/:slug/claim` (alias of `POST /api/v1/publish/:slug/claim`)
- `PATCH /api/v1/artifact/:slug/metadata` (alias of `PATCH /api/v1/publish/:slug/metadata`)
- `DELETE /api/v1/artifact/:slug` (alias of `DELETE /api/v1/publish/:slug`)
- `POST /api/v1/artifact/:slug/uploads/refresh` (alias of `POST /api/v1/publish/:slug/uploads/refresh`)
- `POST /api/v1/handle` / `GET /api/v1/handle` / `PATCH /api/v1/handle` / `DELETE /api/v1/handle`
- `POST /api/v1/links` / `GET /api/v1/links` / `GET|PATCH|DELETE /api/v1/links/:location`

---

### Create a new artifact

`POST /api/v1/artifact` (alias: `POST /api/v1/publish`)

Creates a new artifact with a random slug. Works with or without authentication.

**Request body:**

```json
{
  "files": [
    { "path": "index.html", "size": 1234, "contentType": "text/html; charset=utf-8" },
    { "path": "assets/app.js", "size": 999, "contentType": "text/javascript; charset=utf-8" }
  ],
  "ttlSeconds": null,
  "viewer": {
    "title": "My site",
    "description": "Published by an agent",
    "ogImagePath": "assets/cover.png"
  }
}
```

- `files` (required): array of `{ path, size, contentType }`. At least one file. Paths should be relative to the artifact root (e.g. `index.html`, `assets/style.css`) — don't include a parent directory name like `my-project/index.html`.
- `ttlSeconds` (optional): expiry in seconds. Ignored for anonymous artifacts (always 24h).
- `viewer` (optional): metadata for auto-viewer pages (only used when no `index.html`).

**Response (authenticated):**

```json
{
  "slug": "bright-canvas-a7k2",
  "siteUrl": "https://bright-canvas-a7k2.here.now/",
  "status": "pending",
  "isLive": false,
  "requiresFinalize": true,
  "note": "Artifact created, but this slug is not live yet. Upload all files to upload.uploads[], then POST upload.finalizeUrl with {\"versionId\":\"...\"}.",
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
    "finalizeUrl": "https://here.now/api/v1/artifact/bright-canvas-a7k2/finalize",
    "expiresInSeconds": 3600
  }
}
```

**This step only creates a pending artifact. It is not complete yet.**

- You **must upload every file** in `upload.uploads[]`.
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
  "warning": "IMPORTANT: Save the claimToken and claimUrl. They are returned only once and cannot be recovered. Share the claimUrl with the user so they can keep the artifact permanently."
}
```

**IMPORTANT: The `claimToken` and `claimUrl` are returned only once and cannot be recovered. Always save the `claimToken` and share the `claimUrl` with the user so they can claim the artifact and keep it permanently. If you lose the claim token, the artifact will expire in 24 hours with no way to save it.**

`claimToken`, `claimUrl`, and `expiresAt` are only present for anonymous artifacts. Authenticated artifacts do not include these fields.

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

### Finalize an artifact

`POST /api/v1/artifact/:slug/finalize` (alias: `POST /api/v1/publish/:slug/finalize`)

Makes the artifact live by flipping the slug pointer to the new version.

**Request body:**

```json
{ "versionId": "01J..." }
```

**Auth:**
- Owned artifacts: requires `Authorization: Bearer <API_KEY>`.
- Anonymous artifacts: no auth required for finalize.

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

### Update an existing artifact

`PUT /api/v1/artifact/:slug` (alias: `PUT /api/v1/publish/:slug`)

Same request body as create. Returns new presigned upload URLs and a new `finalizeUrl`.
The update response also includes `status: "pending"` and `isLive: false` to indicate the new version is not live until finalize.

**Auth for owned artifacts:** requires `Authorization: Bearer <API_KEY>` matching the owner.

**Auth for anonymous artifacts:** include `claimToken` in the request body:

```json
{
  "files": [...],
  "claimToken": "<claimToken>"
}
```

Anonymous updates do not extend the original expiration timer. Returns `410 Gone` if expired.

---

### Claim an anonymous artifact

`POST /api/v1/artifact/:slug/claim` (alias: `POST /api/v1/publish/:slug/claim`)

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

### Patch viewer metadata

`PATCH /api/v1/artifact/:slug/metadata` (alias: `PATCH /api/v1/publish/:slug/metadata`)

Update title, description, og:image, or TTL without re-uploading files.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{
  "ttlSeconds": 604800,
  "viewer": {
    "title": "Updated title",
    "description": "New description",
    "ogImagePath": "assets/cover.png"
  }
}
```

All fields optional. `ogImagePath` must reference an image file within the current artifact.

**Response:**

```json
{
  "success": true,
  "effectiveForRootDocument": true,
  "note": "Viewer metadata applies because this artifact has no index.html."
}
```

If the artifact has an `index.html`, viewer metadata is stored but the site's own HTML controls what browsers see.

---

### Delete an artifact

`DELETE /api/v1/artifact/:slug` (alias: `DELETE /api/v1/publish/:slug`)

Hard deletes the artifact, all versions, and the slug-index entry.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{ "success": true }
```

---

### List artifacts

`GET /api/v1/artifacts` (alias: `GET /api/v1/publishes`)

Returns all artifacts owned by the authenticated user.

**Requires:** `Authorization: Bearer <API_KEY>`

**Response:**

```json
{
  "artifacts": [
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

### Refresh upload URLs

`POST /api/v1/artifact/:slug/uploads/refresh` (alias: `POST /api/v1/publish/:slug/uploads/refresh`)

Returns fresh presigned URLs for a pending upload (same version, no new version created).

**Requires:** `Authorization: Bearer <API_KEY>`

Use when presigned URLs expire mid-upload (they're valid for 1 hour).

---

### Register a handle

`POST /api/v1/handle`

Registers your handle for `handle.here.now`.

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

Changes an existing handle to a new one.

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

### Create a link under your handle

`POST /api/v1/links`

Links an artifact slug to a location under your handle.

**Requires:** `Authorization: Bearer <API_KEY>`

**Request body:**

```json
{
  "location": "docs",
  "slug": "bright-canvas-a7k2"
}
```

Use an empty `location` to link at root (`https://yourname.here.now/`).

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

Changes which artifact slug a location points to.

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

Each artifact gets its own subdomain: `https://<slug>.here.now/`

Asset paths work naturally from the subdomain root:
- `/styles.css`, `/images/a.jpg` resolve as expected
- Relative paths (`styles.css`, `./images/a.jpg`) also work

### Serving rules

1. If `index.html` exists at root → serve it as the document.
2. Else if exactly one file in the entire artifact → serve an auto-viewer page (images, PDF, video, audio get rich viewers; everything else gets a download page).
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
