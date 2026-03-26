# PKCE Browser Flow (Tier 1 + Tier 2)

> The PKCE (Proof Key for Code Exchange, RFC 7636) flow is the primary auth path
> for CLI tools that can reach a user's browser. It prevents authorization code
> interception attacks even when the redirect URI is `http://localhost`.

## Sequence Diagram

```
CLI                          Browser                    Server
 │                              │                          │
 │ 1. Generate PKCE pair        │                          │
 │    verifier = random(32B)    │                          │
 │    challenge = SHA256(verifier) base64url               │
 │    state = random(22-128 chars)                         │
 │                              │                          │
 │ 2. Bind TCP listener         │                          │
 │    127.0.0.1:0 (OS picks)   │                          │
 │                              │                          │
 │ 3. Open browser ─────────────▶                          │
 │    GET /api/v1/auth/cli-login                           │
 │    ?port=PORT                │                          │
 │    &code_challenge=CHALLENGE │                          │
 │    &state=STATE              │                          │
 │                              │ 4. Server validates ─────▶
 │                              │    port: 1-65535
 │                              │    challenge: 43-128 chars, base64url
 │                              │    state: 22-128 chars, URL-safe
 │                              │                          │
 │                              │ 5. Server signs flow data│
 │                              │    payload = {port, codeChallenge, state}
 │                              │    Sets httpOnly cookie   │
 │                              │    "cli_flow" (10 min TTL)│
 │                              │                          │
 │                              │ 6. Redirect to login ────▶
 │                              │    /login?next=/api/v1/auth/callback
 │                              │    (or directly if already logged in)
 │                              │                          │
 │                              │ 7. User authenticates    │
 │                              │    (Google OAuth, SSO, etc.)
 │                              │                          │
 │                              │ 8. Redirect to callback ─▶
 │                              │    GET /api/v1/auth/callback
 │                              │                          │
 │                              │ 9. Server reads cli_flow │
 │                              │    cookie, verifies sig  │
 │                              │    Creates signed auth   │
 │                              │    code (60s expiry):    │
 │                              │    {userId, codeChallenge,│
 │                              │     expiresAt}           │
 │                              │                          │
 │                              │ 10. Serves callback HTML │
 │                              │     with loopback URL    │
 │                              │     + copy button        │
 │                              │                          │
 │ 11a. <img> tag hits ◀────────┤                          │
 │      localhost:PORT/callback │                          │
 │      ?code=CODE&state=STATE  │                          │
 │                              │                          │
 │ OR 11b. User copies URL      │                          │
 │         and pastes to CLI    │                          │
 │                              │                          │
 │ 12. CLI verifies state match │                          │
 │                              │                          │
 │ 13. CLI exchanges code ──────────────────────────────────▶
 │     POST /api/v1/auth/token  │                          │
 │     {code, code_verifier}    │                          │
 │                              │                          │
 │                              │ 14. Server verifies:     │
 │                              │     - Code signature     │
 │                              │     - Code not expired   │
 │                              │     - SHA256(verifier)   │
 │                              │       == challenge       │
 │                              │     - Code not reused    │
 │                              │       (advisory lock)    │
 │                              │                          │
 │ 15. Receives tokens ◀────────────────────────────────────│
 │     {access_token, refresh_token,                       │
 │      expires_in, user_id, email}                        │
 │                              │                          │
 │ 16. Stores in keyring/file   │                          │
```

## PKCE Generation (CLI Side)

```rust
// Generate PKCE pair (RFC 7636)
fn generate_pkce() -> (String, String) {
    let verifier_bytes: [u8; 32] = rand::random();
    let verifier = base64url_encode(&verifier_bytes); // 43 chars

    let challenge = {
        let mut hasher = Sha256::new();
        hasher.update(verifier.as_bytes());
        base64url_encode(&hasher.finalize()) // 43 chars
    };

    (verifier, challenge)
}

// Generate CSRF state
fn generate_state() -> String {
    let state_bytes: [u8; 32] = rand::random();
    base64url_encode(&state_bytes) // 43 chars
}
```

## Server-Side Validation

### Input Validation (cli-login endpoint)

```typescript
// RFC 7636 verifier/challenge character set: "unreserved" chars, 43-128
const PKCE_REGEX = /^[A-Za-z0-9\-._~]{43,128}$/;

// State: high-entropy, 22-128 unreserved chars
// (22 minimum for backwards compatibility with older CLI builds)
const STATE_REGEX = /^[A-Za-z0-9\-._~]{22,128}$/;

function validateCliLoginParams(params: URLSearchParams) {
    const port = parseInt(params.get("port") ?? "", 10);
    if (isNaN(port) || port < 1 || port > 65535) throw "Invalid port";

    const challenge = params.get("code_challenge") ?? "";
    if (!PKCE_REGEX.test(challenge)) throw "Invalid PKCE challenge";

    const state = params.get("state") ?? "";
    if (!STATE_REGEX.test(state)) throw "Invalid state";

    return { port: String(port), challenge, state };
}
```

### Signed Flow Cookie

```typescript
// Sign the flow data so it can't be tampered with
const payload = JSON.stringify({ port, codeChallenge, state });
const signed = sign(payload); // HMAC-SHA256 with JWT_SECRET

// On a NextResponse object:
response.cookies.set("cli_flow", Buffer.from(signed).toString("base64url"), {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",       // Allows redirect from IdP
    maxAge: 600,           // 10 minutes
    path: "/api/v1/auth",  // Restrict scope
});
```

### Auth Code Generation (callback endpoint)

```typescript
// After verifying user is authenticated and cli_flow cookie is valid:
const flowData = JSON.parse(verify(atob(cookie.get("cli_flow"))));

// Create signed authorization code (60 second expiry)
const codePayload = JSON.stringify({
    userId: user.id,
    codeChallenge: flowData.codeChallenge,
    expiresAt: new Date(Date.now() + 60_000).toISOString(),
});
const authCode = sign(codePayload);

// Build loopback URL
const callbackUrl = `http://127.0.0.1:${flowData.port}/callback?code=${authCode}&state=${flowData.state}`;
```

## Tier 2: Manual Paste Variant

Same flow, but step 11 changes:

```
CLI prints to stderr:
  "Open this URL in your browser: https://example.com/api/v1/auth/cli-login?..."
  "Then paste the callback URL here: "

CLI waits for stdin input. Accepts:
  - Full URL: http://127.0.0.1:12345/callback?code=abc&state=xyz
  - Relative path: /callback?code=abc&state=xyz
  - Query string only: ?code=abc&state=xyz
  - Just the params: code=abc&state=xyz

All formats normalized to extract code and state.
```

### Callback Page Design for SSH Users

The callback HTML page served by the server must handle the case where the CLI
is running on a different machine than the browser:

```html
<!-- Best-effort loopback attempt via hidden image -->
<img src="http://127.0.0.1:PORT/callback?code=...&state=..." alt="" hidden />

<!-- Manual options for SSH users -->
<button onclick="navigator.clipboard.writeText(callbackUrl)">
    Copy callback URL
</button>
<pre class="code-block">http://127.0.0.1:PORT/callback?code=...&state=...</pre>

<p>If jsm is running over SSH, paste the full URL into the terminal.</p>
```

## Error Handling

| Error | Cause | CLI Action |
|-------|-------|------------|
| State mismatch | CSRF attack or expired flow | Abort, restart login |
| Code expired (>60s) | User was too slow | Abort, restart login |
| PKCE verification failed | Tampered code or wrong verifier | Abort, restart login |
| Code already used | Replay attack | Abort, warn user |
| Port not available | Another process on the port | Rebind to different port |
| Browser won't open | Headless environment | Fall through to Tier 2 or 3 |
| Connection refused on callback | CLI not running or wrong port | Show copy button prominently |

## Key Design Decisions

### Why `127.0.0.1` not `localhost`?

`localhost` may resolve to `::1` (IPv6) on some systems, causing TLS/port mismatch.
`127.0.0.1` is unambiguous IPv4 loopback.

### Why signed cookies instead of server-side session?

- No database write needed during flow initiation
- Cookie is tamper-proof (HMAC-SHA256)
- Automatically scoped to the auth path
- Self-expiring (maxAge)
- No cleanup needed

### Why signed auth codes instead of random codes stored in DB?

- Stateless: no database lookup during code generation
- Self-expiring: timestamp embedded in payload
- Tamper-proof: HMAC signature
- One-time use enforced at exchange time (advisory lock on fingerprint)

### Why `<img>` tag for callback instead of JavaScript fetch?

- `<img>` tag is a simple GET request — no CORS issues with localhost
- Works even if JavaScript is blocked
- Falls back gracefully (broken image is invisible)
- **Note:** Modern browsers may block or auto-upgrade mixed content (HTTP from
  HTTPS). The `<img>` tag is a best-effort mechanism — if it fails silently,
  the user falls back to the "Copy URL" button. This is by design.
