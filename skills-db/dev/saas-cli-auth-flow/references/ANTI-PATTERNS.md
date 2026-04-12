# Anti-Patterns Deep Dive

> Each anti-pattern below was discovered through real production incidents,
> security audits, or painful debugging sessions. They are organized by
> the stage of implementation where they typically occur.

## Design-Phase Anti-Patterns

### 1. Skipping the Protocol Document

**What happens:** CLI and server teams implement incompatible assumptions.
CLI sends `content-type: text/plain`, server expects `application/json`.
Error codes don't match. Timeout expectations diverge.

**Why it's tempting:** "We'll figure it out as we go."

**What to do instead:** Write the protocol document first. Commit it. Refer to
it during implementation. Update it when things change.

### 2. Using JWT for CLI Tokens

**What happens:** JWTs can't be revoked without a blocklist. When a user runs
`logout`, the token continues working until expiry. When an account is suspended,
the JWT continues authenticating until expiry.

**Why it's tempting:** "No database lookup per request!"

**What to do instead:** Opaque tokens with server-side lookup. The database
lookup is 1-2ms — far cheaper than the business cost of non-revocable tokens.

### 3. Single Token (No Refresh Token)

**What happens:** When the access token expires or needs rotation, the user
must re-authenticate via browser. For long-running CLI sessions (365 days),
this means periodic disruption.

**Why it's tempting:** "Simpler to manage one token."

**What to do instead:** Separate access and refresh tokens with distinct prefixes.
Access token rotated transparently; refresh token survives the rotation.

## Implementation-Phase Anti-Patterns

### 4. Hard-Coding the Localhost Port

```rust
// BAD
let listener = TcpListener::bind("127.0.0.1:8080")?;

// GOOD
let listener = TcpListener::bind("127.0.0.1:0")?;
let port = listener.local_addr()?.port();
```

**What happens:** Two concurrent `my-cli login` invocations fight over the port.
The second one fails with "address already in use."

### 5. Using `localhost` Instead of `127.0.0.1`

**What happens:** On dual-stack systems, `localhost` may resolve to `::1` (IPv6).
The CLI binds to IPv4, but the browser redirects to IPv6. Connection refused.

**What to do instead:** Always use the literal `127.0.0.1` for loopback callbacks.

### 6. Storing Raw Tokens in the Database

```typescript
// BAD
await db.insert(cliTokens).values({ token: rawToken });

// GOOD
await db.insert(cliTokens).values({ tokenHash: hashToken(rawToken) });
```

**What happens:** A database breach (SQL injection, backup theft, admin error)
exposes every active session. Attackers can impersonate any CLI user.

### 7. Non-Timing-Safe Token Comparison

```typescript
// BAD — timing side-channel
if (computed === expected) { ... }

// GOOD — constant-time
if (timingSafeEqual(Buffer.from(computed), Buffer.from(expected))) { ... }
```

**What happens:** An attacker can determine how many bytes of a token match
by measuring response time. With enough requests, they reconstruct the token.

### 8. Retrying Code Exchange on Failure

```rust
// BAD
for attempt in 0..3 {
    match exchange_code(&code, &verifier).await {
        Ok(tokens) => return Ok(tokens),
        Err(_) => continue, // Retry!
    }
}

// GOOD
exchange_code(&code, &verifier).await
// If it fails, start a new login flow
```

**What happens:** Auth codes are one-time use. If the first exchange fails
(network timeout, server error), the code is already consumed. Retrying sends
the same code, which the server rejects as replay.

### 9. Polling Device Token Without Backoff

```rust
// BAD
loop {
    let response = poll_device_token().await;
    // No sleep, no backoff
}

// GOOD
loop {
    sleep(Duration::from_secs(interval)).await;
    let response = poll_device_token().await;
    if response.status() == 429 {
        interval += 5; // Slow down as requested
    }
}
```

**What happens:** Server gets hammered with poll requests. Rate limiter kicks in.
The CLI gets 429s and may never succeed within the 15-minute window.

### 10. Checking Auth State with Keyring Prompt

```rust
// BAD — triggers GUI password dialog
fn is_authenticated() -> bool {
    keyring::Entry::new("service", "user")
        .get_password()
        .is_ok()
}

// GOOD — suppress interactive prompts
fn is_authenticated_noninteractive() -> bool {
    match try_keyring_read_quiet() {
        Ok(_) => true,
        Err(_) => try_file_read().is_ok(),
    }
}
```

**What happens:** On Linux with GNOME Keyring, reading from the keyring may
trigger a GUI password dialog. This happens during `jsm sync` or `jsm status`
when checking if the user is logged in — blocking background operations with
an unexpected modal dialog.

## Security Anti-Patterns

### 11. Embedding Secrets in Callback URLs (Beyond Short-Lived Codes)

```
# BAD — long-lived token in URL
http://127.0.0.1:PORT/callback?token=jsm_abc123...

# GOOD — short-lived signed code that's exchanged server-side
http://127.0.0.1:PORT/callback?code=SIGNED_60s_CODE&state=CSRF_STATE
```

**What happens:** URLs end up in browser history, server access logs, referrer
headers, and browser extension telemetry. Long-lived tokens in URLs are
effectively public.

### 12. Skipping PKCE for "Internal" Tools

**What happens:** "Our CLI is internal, nobody's going to MITM localhost."
Then a browser extension captures the authorization code. Or a malicious app
binds to the same port before your CLI.

**What to do instead:** PKCE costs ~10 lines of code. Always use it.

### 13. Not Checking Suspension at Refresh

```typescript
// BAD
async function refresh(token: string) {
    const record = await lookupRefreshToken(token);
    // Skip user status check
    return mintNewAccessToken(record.userId);
}

// GOOD
async function refresh(token: string) {
    const record = await lookupRefreshToken(token);
    const user = await getUser(record.userId);
    if (user.suspended) throw new Error("Account suspended");
    return mintNewAccessToken(record.userId);
}
```

**What happens:** A suspended user's refresh token continues minting new
access tokens indefinitely. Suspension becomes ineffective for CLI users.

## Operational Anti-Patterns

### 14. Not Running Device Code Cleanup

**What happens:** The `device_codes` table grows unboundedly. Expired codes
accumulate. Unique constraints on `user_code` may eventually cause collisions
(unlikely but possible over years).

**What to do instead:** Cron job to delete expired device codes hourly.

### 15. Not Logging Auth Failures

**What happens:** Brute-force attempts go unnoticed. Credential stuffing
attacks succeed without alerts. You find out when users complain about
account compromise.

**What to do instead:** Log every auth failure with IP, user-agent, and
reason. Alert on anomalous patterns (>10 failures per IP per 5 minutes).

### 16. Breaking Backwards Compatibility Without Migration

```typescript
// BAD — changing hash algorithm without migration path
function hashToken(token: string): string {
    // Switched from HMAC-SHA256 to plain SHA-256
    // All existing tokens are now invalid!
    return sha256(token);
}

// GOOD — try new format first, then legacy, auto-migrate
async function authenticateToken(token: string) {
    let record = await lookupByHash(sha256(token));
    if (!record) {
        record = await lookupByHash(hmacSha256(token));
        if (record) await migrateHash(record.id, sha256(token));
    }
    return record;
}
```

**What happens:** Every active CLI session immediately breaks. Users must
re-authenticate. If they have 100 machines with saved credentials, that's
100 re-logins.
