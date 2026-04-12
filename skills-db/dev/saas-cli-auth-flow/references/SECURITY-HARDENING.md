# Security Hardening

> This document covers the security measures that elevate a basic OAuth flow
> into a production-grade system resistant to real-world attacks.

## Threat Model

| Threat | Attack Vector | Mitigation |
|--------|---------------|------------|
| Authorization code interception | Network sniffing on localhost | PKCE (SHA-256 challenge/verifier) |
| Cross-site request forgery | Attacker initiates flow, victim completes | CSRF state token verified on callback |
| Authorization code replay | Attacker replays captured code | One-time use enforcement via advisory lock |
| Token theft from database | SQL injection or DB breach | SHA-256 hash before storage |
| Timing side-channel | Compare tokens byte-by-byte, measure time | `crypto.timingSafeEqual()` everywhere |
| Credential theft from disk | File system access | OS keyring or AES-256-GCM encryption |
| Token leakage in logs | Structured logging includes tokens | Regex-mask tokens in log pipeline |
| Device code brute force | Guess 8-char code within 15 min | Ambiguity-safe alphabet, 5s poll, max 180 attempts |
| Concurrent refresh race | Two processes refresh simultaneously | PostgreSQL advisory locks |
| Suspended user bypass | Cached token used after suspension | Check user status at every exchange point |
| SSO policy bypass | CLI auth bypasses org SSO requirement | Enforce SSO policy in callback route |

## PKCE Implementation Details

### Why PKCE is Non-Negotiable

Even for `localhost` redirect URIs, PKCE prevents:
1. **Malicious apps** listening on the same port before your CLI binds
2. **Browser extensions** that can intercept redirects
3. **OS-level URL handlers** that may capture the callback

### Code Challenge Method

Always use `S256` (SHA-256), never `plain`:

```typescript
// Server-side verification
function verifyPkce(codeVerifier: string, codeChallenge: string): boolean {
    const computed = createHash("sha256")
        .update(codeVerifier)
        .digest("base64url");

    // MUST use timing-safe comparison
    return timingSafeEqual(
        Buffer.from(computed),
        Buffer.from(codeChallenge)
    );
}
```

## Timing-Safe Comparisons

Every comparison involving secrets must be constant-time:

```typescript
import { timingSafeEqual } from "crypto";

// Note: length check leaks whether strings are same length, but for
// fixed-format tokens (PKCE challenges, hex hashes) lengths are known/fixed.
// For truly variable-length secrets, pad to equal length first.
function safeCompare(a: string, b: string): boolean {
    if (a.length !== b.length) return false;
    return timingSafeEqual(Buffer.from(a), Buffer.from(b));
}
```

**Where to use:**
- PKCE verification (challenge vs computed)
- CSRF state comparison
- Token hash comparison
- Cookie signature verification
- Refresh token validation

## One-Time Code Enforcement

Authorization codes must be single-use. The race condition:

```
Request A: Exchange code "abc" → starts processing
Request B: Exchange code "abc" → starts processing
Request A: Checks DB → no session with fingerprint → creates token
Request B: Checks DB → no session with fingerprint → creates DUPLICATE token
```

### Solution: Advisory Lock on Code Fingerprint

```typescript
// Serialize concurrent exchanges of the same code
const fingerprint = hashToken(codeChallenge).slice(0, 12);

// PostgreSQL advisory lock (held for transaction duration)
await db.execute(
    sql`SELECT pg_advisory_xact_lock(hashtext(${fingerprint}))`
);

// Now check for replay — serialized, no race
const existing = await db.query.cliTokens.findFirst({
    where: like(cliTokens.name, `%${fingerprint}%`),
});

if (existing) {
    throw new Error("Authorization code already exchanged");
}
```

**Why `pg_advisory_xact_lock`?**
- Released automatically when the transaction commits/rolls back
- No cleanup needed
- No deadlock risk (single lock per operation)
- Uses `hashtext()` to convert string fingerprint to integer lock key

## Abuse Tracking

Track failed authentication attempts for anomaly detection:

```typescript
async function trackAuthFailure(request: NextRequest, reason: string) {
    const ip = getClientIp(request);
    const userAgent = request.headers.get("user-agent") ?? "unknown";

    await db.insert(authFailures).values({
        ip,
        userAgent,
        reason,
        endpoint: request.nextUrl.pathname,
        timestamp: new Date(),
    });

    // Check for rate limiting
    const recentFailures = await countRecentFailures(ip, "5 minutes");
    if (recentFailures > 10) {
        await blockIp(ip, "30 minutes");
    }
}
```

## Suspension Enforcement

Check user suspension at every token lifecycle point:

```
Token Exchange (PKCE)   → Check before minting tokens
Token Exchange (Device) → Check before minting tokens
Token Refresh           → Check before issuing new access token
API Authentication      → Check on every request (cached per-hour)
```

This means a suspended user's tokens stop working within 1 hour (the
`lastUsedAt` debounce granularity for the auth check cache).

## SSO Policy Enforcement in CLI Auth

If a user's organization requires SSO authentication:

```typescript
// In /api/v1/auth/callback
const ssoDecision = await getOrgSsoTransitionDecision(user);

switch (ssoDecision.cliAction) {
    case "allow":
        // Normal flow continues
        break;
    case "require_reauth":
        // Redirect to SSO provider login
        return redirect(`/login?sso=${ssoDecision.provider}`);
    case "block":
        // CLI auth forbidden until SSO completed
        return error(403, "Organization requires SSO authentication");
}
```

## Cookie Security

The `cli_flow` cookie that carries PKCE state:

```typescript
{
    httpOnly: true,      // No JavaScript access
    secure: true,        // HTTPS only (disable for localhost dev)
    sameSite: "lax",     // Allows redirect from IdP
    maxAge: 600,         // 10-minute expiry
    path: "/api/v1/auth" // Only sent to auth endpoints
}
```

**Why `sameSite: "lax"` not `strict`?**
The login flow involves a redirect from the identity provider (Google, Okta, etc.)
back to our callback URL. `strict` would strip the cookie on this cross-site redirect.
`lax` allows the cookie on top-level navigations (which is what a redirect is).

## Token Masking in Logs

```typescript
function maskToken(token: string): string {
    if (token.length <= 8) return "***";
    return `${token.slice(0, 4)}...${token.slice(-4)}`;
}

// In structured logging
logger.info({
    token: maskToken(rawToken), // "jsm_...f2a1"
    userId,
    action: "token_exchanged",
});
```

## Signed Payloads

All server-generated payloads use HMAC-SHA256:

```typescript
function sign(payload: string): string {
    const sig = createHmac("sha256", JWT_SECRET)
        .update(payload)
        .digest("base64url");
    return `${payload}.${sig}`;
}

function verify(signed: string): string | null {
    const lastDot = signed.lastIndexOf(".");
    if (lastDot === -1) return null;

    const payload = signed.slice(0, lastDot);
    const sig = signed.slice(lastDot + 1);
    const expected = createHmac("sha256", JWT_SECRET)
        .update(payload)
        .digest("base64url");

    if (!timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
        return null;
    }
    return payload;
}
```

**Where used:**
- `cli_flow` cookie payload
- Authorization codes
- Any server-generated credential that must be tamper-proof

## Checklist: Security Audit

- [ ] PKCE S256 on every code exchange (never plain)
- [ ] CSRF state on every PKCE flow (22-128 chars, cryptographic random)
- [ ] Timing-safe comparison on every secret comparison
- [ ] Advisory lock on every code exchange (prevents replay)
- [ ] Token hashed before DB storage (SHA-256, not raw)
- [ ] Suspension check at exchange, refresh, and auth points
- [ ] SSO policy enforcement in callback route
- [ ] Cookies: httpOnly, secure, sameSite, scoped path, short maxAge
- [ ] Tokens masked in all log output
- [ ] Signed payloads verified before trust
- [ ] Device code cleanup cron running
- [ ] Rate limiting on all auth endpoints
- [ ] Error responses don't leak internal details
