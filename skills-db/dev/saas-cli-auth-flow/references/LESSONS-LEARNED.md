# Evolution and Lessons Learned

> This document captures the design evolution and hard-won lessons from building
> the JSM CLI authentication system over several months. These insights are
> generalized for any SaaS CLI auth implementation.

## Chronological Evolution

### Phase 1: Protocol Design (Week 1)

**What happened:** Before writing any code, a comprehensive protocol document
was created specifying endpoints, error codes, security requirements, and
request/response formats.

**Lesson:** **Design the protocol before the code.** The protocol doc prevented
dozens of CLI-server mismatches that would have been discovered only in production.
It also served as the specification for testing.

### Phase 2: Basic PKCE Flow (Weeks 1-2)

**What happened:** Implemented the browser PKCE flow first as the happy path.
CLI generates PKCE pair, opens browser, receives callback on localhost.

**Lesson:** **Start with the happy path, then add fallbacks.** The PKCE flow
is 80% of the auth logic. Getting it right first means the device code flow
(added later) could reuse the token minting infrastructure.

### Phase 3: CSRF and PKCE Validation (Week 3)

**What happened:** Security audit revealed that the initial implementation
accepted state tokens of any format and didn't validate PKCE challenge length.

**Lesson:** **Validate format at every boundary.** Don't just check "parameter
exists" — check it matches the RFC spec (PKCE: 43-128 chars base64url, state:
22-128 chars URL-safe). Format validation is the cheapest security measure.

### Phase 4: One-Time Code Enforcement (Week 3)

**What happened:** Discovered that concurrent requests could exchange the same
authorization code twice, creating duplicate sessions.

**Lesson:** **Race conditions in auth are security vulnerabilities, not bugs.**
PostgreSQL advisory locks (`pg_advisory_xact_lock`) solved the concurrent
exchange problem with zero application-level complexity.

### Phase 5: Device Code Flow (Week 4)

**What happened:** Users running the CLI over SSH couldn't complete the
browser redirect (localhost is the remote server, not their machine). RFC 8628
device code flow was added as the headless alternative.

**Lesson:** **SSH is the deployment reality for CLI tools.** Most power users
work on remote servers. The device code flow isn't an edge case — it's often
the primary flow. Build it early.

### Phase 6: Manual Paste Fallback (Week 4)

**What happened:** The callback page was enhanced with a "Copy URL" button
for SSH users. The CLI was updated to accept pasted callback URLs from stdin.

**Lesson:** **The callback page is a UI for two audiences.** On local machines,
the `<img>` tag callback fires automatically. On SSH machines, the user needs
a copy button and clear instructions. Design the page for both.

### Phase 7: Token Refresh with Dedicated Refresh Tokens (Week 5)

**What happened:** Initially, the same token was used for both API access and
refresh. This meant rotating the access token also rotated the refresh token,
creating a chicken-and-egg problem for concurrent CLI processes.

**Lesson:** **Separate access and refresh tokens from day one.** The migration
from single-token to dual-token required backwards-compatible hash lookups
and auto-migration logic that was far more complex than doing it right initially.

### Phase 8: Timing-Safe Comparisons (Week 6)

**What happened:** Security audit flagged all string comparisons involving
tokens, challenges, and signatures as timing-vulnerable.

**Lesson:** **`crypto.timingSafeEqual()` is not optional.** Add it from the
start. Retrofitting timing-safe comparisons is tedious (every `===` becomes
a function call) but necessary.

### Phase 9: Suspension and SSO Enforcement (Week 7)

**What happened:** Admin suspended a user, but their CLI token continued
working. SSO-mandated organizations had members bypassing SSO via CLI login.

**Lesson:** **Check user status at every lifecycle point.** Token exchange,
refresh, and per-request authentication must all verify the user isn't
suspended and complies with org SSO policy.

### Phase 10: Hash Algorithm Migration (Week 8)

**What happened:** Migrated from HMAC-SHA256 (with JWT_SECRET) to plain SHA-256
for token hashing. Needed to support both during transition.

**Lesson:** **Design for hash migration from the start.** Use a function like
`authenticateWithMigration()` that tries new hash first, falls back to legacy,
and auto-migrates on success. The migration is then invisible to users.

### Phase 11: Connectivity Checks with RetryClient (Week 9)

**What happened:** `jsm sync` and `jsm status` reported "OFFLINE" when the
server was actually online but slow to respond (cold start on serverless).
A single 5-second timeout was too aggressive.

**Lesson:** **Use a retry client for connectivity checks**, not a single-shot
request. 3 attempts with exponential backoff (500ms → 1s → 2s) and a dedicated
lightweight health endpoint (`/api/health/live`) solved false-offline detection.

## Abstract Principles Extracted

### 1. The Three-Tier Principle

Every environment access pattern needs a graceful degradation path:
- **Full access** (browser + localhost) → Browser PKCE
- **Partial access** (browser on different device) → Manual paste or device code
- **No browser** (CI/CD, containers) → API key

### 2. The Signed-State Principle

Don't store transient auth state in the database when you can sign it:
- Flow cookies → HMAC-signed JSON
- Authorization codes → HMAC-signed JSON with expiry
- Device codes → Database (because CLI needs to poll by opaque ID)

**Rule of thumb:** If only the server needs to read it back, sign it.
If another party needs to look it up, store it.

### 3. The Atomic Verification Principle

Any operation that transitions state (pending → verified, code → token)
must be atomic. The database operation should both check the precondition
and make the change in a single statement:

```sql
UPDATE device_codes
SET user_id = $1, verified_at = now()
WHERE id = $2
  AND expires_at > now()    -- Precondition: not expired
  AND verified_at IS NULL   -- Precondition: not already verified
  AND user_id IS NULL;      -- Precondition: not already claimed
```

If the update affects 0 rows, someone else won the race.

### 4. The Debounced Update Principle

Not every observable state change needs a synchronous write:
- `lastUsedAt` on tokens → 1-hour granularity (saves per-request DB writes)
- Refresh token rotation → Advisory lock (serializes concurrent writes)
- Token hash migration → On-read auto-migrate (spreads load over time)

### 5. The Fallback Chain Principle

Every operation should have a fallback:
- Browser fails to open → Print URL for manual copy
- Keyring unavailable → Encrypted file
- TCP callback fails → Paste URL from clipboard
- Server unreachable → Offline mode with cached credentials
- New hash format fails → Try legacy hash
- Token expired → Auto-refresh

### 6. The Distinct Prefix Principle

Credential types that serve different roles should have distinct prefixes:
- `<prefix>_` → access token (and API keys, which are functionally equivalent)
- `<prefix>_refresh_` → refresh token (distinct to prevent misuse as access token)

This prevents using a refresh token where an access token is expected.
API keys and access tokens share the same prefix because they serve the
same function (authenticate API requests) — they differ only in issuance
method (manual vs OAuth) and lifetime (indefinite vs 365 days).

## What We'd Do Differently

1. **Dual tokens from day one** — Single token → dual token migration was
   the most complex backward-compatibility challenge.

2. **Device code flow from the start** — SSH users are the majority power
   user segment. Building it later meant retrofitting database tables.

3. **Advisory locks from the start** — Every concurrent exchange bug was a
   security vulnerability discovered in audit, not a feature planned in design.

4. **Dedicated health endpoint from the start** — Using the main API for
   connectivity checks causes false-offline during cold starts.

5. **Format validation in the protocol doc** — Specifying exact regex patterns
   for tokens, challenges, and state parameters would have prevented the
   "accepts anything" bugs found in security audit.
