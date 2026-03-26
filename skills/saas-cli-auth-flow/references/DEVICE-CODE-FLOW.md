# Device Code Flow (Tier 3, RFC 8628)

> The device code flow is for environments where the CLI cannot receive an HTTP
> callback: SSH sessions, containers, CI/CD, headless servers. The user enters
> a short human-readable code on any browser to authorize the CLI.

## Sequence Diagram

```
CLI                          User's Browser              Server
 │                              │                          │
 │ 1. Request device code ──────────────────────────────────▶
 │    POST /api/v1/auth/device-code                        │
 │    {client_id: "my-cli"}    │                          │
 │                              │                          │
 │ 2. Receive response ◀────────────────────────────────────│
 │    {device_code: "abc123...",│                          │
 │     user_code: "ABCD-1234", │                          │
 │     verification_url: "/verify",                        │
 │     verification_url_complete: "/verify?code=ABCD-1234",│
 │     expires_in: 900,        │                          │
 │     interval: 5}            │                          │
 │                              │                          │
 │ 3. Display to user:         │                          │
 │    "Visit: https://example.com/verify"                  │
 │    "Enter code: ABCD-1234"  │                          │
 │    "Or open: https://example.com/verify?code=ABCD-1234" │
 │                              │                          │
 │                              │ 4. User opens URL ───────▶
 │                              │    Logs in if needed      │
 │                              │    Enters/auto-submits    │
 │                              │    code ABCD-1234         │
 │                              │                          │
 │                              │ 5. POST /device-verify ──▶
 │                              │    {user_code: "ABCD1234"}│
 │                              │                          │
 │                              │ 6. Server atomically:    │
 │                              │    - Looks up by user_code│
 │                              │    - Checks not expired  │
 │                              │    - Sets userId +       │
 │                              │      verifiedAt          │
 │                              │    - Returns success     │
 │                              │                          │
 │ 7. CLI polls ────────────────────────────────────────────▶
 │    POST /api/v1/auth/device-token                       │
 │    {device_code, client_id} │                          │
 │                              │                          │
 │    Loop every `interval` seconds:                       │
 │    - 400 "authorization_pending" → keep polling         │
 │    - 429 "slow_down" → increase interval by 5s         │
 │    - 400 "expired_token" → abort                        │
 │    - 200 → tokens received!  │                          │
 │                              │                          │
 │ 8. Receive tokens ◀─────────────────────────────────────│
 │    Same response as PKCE:    │                          │
 │    {access_token, refresh_token, ...}                   │
 │                              │                          │
 │ 9. Store credentials         │                          │
```

## User Code Design

The user code must be easy to type on a phone/tablet while looking at a terminal.

### Ambiguity-Safe Alphabet

```
ABCDEFGHJKMNPQRSTUVWXYZ23456789
```

**Excluded characters** (too similar to other characters):
- `I` (looks like `1` or `l`)
- `L` (looks like `1` or `I`)
- `O` (looks like `0`)
- `0` (looks like `O`)
- `1` (looks like `I` or `l`)

### Format: `XXXX-YYYY`

- 8 characters, displayed as two groups of four with a dash
- The dash is for human readability only — strip it before lookup
- Normalize: remove all non-alphanumeric, uppercase

```typescript
const USER_CODE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
const USER_CODE_LENGTH = 8;

function generateUserCode(): string {
    // 256 - (256 % 31) = 249; accept bytes 0..248, reject 249..255
    const maxValidByte = 249;
    let result = "";
    while (result.length < USER_CODE_LENGTH) {
        const buffer = crypto.randomBytes(USER_CODE_LENGTH * 2);
        for (const byte of buffer) {
            if (byte >= maxValidByte) continue; // Modulo bias rejection
            result += USER_CODE_CHARS[byte % USER_CODE_CHARS.length];
            if (result.length === USER_CODE_LENGTH) break;
        }
    }
    return result;
}

function formatUserCode(code: string): string {
    return `${code.slice(0, 4)}-${code.slice(4)}`;
}

function normalizeUserCode(input: string): string {
    return input.replace(/[^A-Za-z0-9]/g, "").toUpperCase();
}
```

### Entropy Analysis

- Alphabet: 31 characters
- Length: 8 characters
- Total combinations: 31^8 = ~852 billion
- Collision probability: negligible at any realistic scale
- Brute-force: 5-second poll interval + 15-minute expiry = max 180 attempts

## Device Code Storage

```sql
CREATE TABLE device_codes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code TEXT NOT NULL UNIQUE,       -- 64 hex chars (32 bytes)
    user_code   TEXT NOT NULL UNIQUE,       -- 8 chars (ABCD1234)
    user_id     UUID REFERENCES users(id),  -- NULL until verified
    client_id   TEXT NOT NULL,              -- "my-cli"
    verified_at TIMESTAMPTZ,               -- NULL until verified
    expires_at  TIMESTAMPTZ NOT NULL,      -- 15 min from creation
    created_at  TIMESTAMPTZ DEFAULT now()
);
```

## Verification State Machine

```
                ┌─────────┐
                │ PENDING  │ userId=NULL, verifiedAt=NULL
                └────┬────┘
                     │ User enters code at /verify
                     │ Atomic: SET userId, verifiedAt
                     │ WHERE verifiedAt IS NULL AND userId IS NULL
                     ▼
                ┌─────────┐
                │VERIFIED  │ userId=SET, verifiedAt=SET
                └────┬────┘
                     │ CLI polls /device-token
                     │ Atomic: DELETE device_code, INSERT cli_token
                     ▼
                ┌─────────┐
                │CONSUMED  │ Row deleted from DB
                └─────────┘

Edge cases:
  CORRUPT = (userId SET, verifiedAt NULL) OR (userId NULL, verifiedAt SET)
  → Return 500, log for investigation
```

### Atomic Verification

```typescript
// WHERE clause prevents double-verification race
const result = await db.update(deviceCodes)
    .set({ userId, verifiedAt: new Date() })
    .where(and(
        eq(deviceCodes.id, codeId),
        gt(deviceCodes.expiresAt, new Date()),  // Not expired
        isNull(deviceCodes.verifiedAt),          // Not already verified
        isNull(deviceCodes.userId)               // Not already claimed
    ))
    .returning({ id: deviceCodes.id });

return result.length > 0; // true = we won the race
```

### Atomic Consumption

```typescript
// Delete device code + create CLI token in a transaction
await db.transaction(async (tx) => {
    // 1. Delete the device code (consume it)
    await tx.delete(deviceCodes).where(eq(deviceCodes.id, codeId));

    // 2. Create the CLI token
    await tx.insert(cliTokens).values({
        userId,
        tokenHash: hashToken(accessToken),
        refreshTokenHash: hashToken(refreshToken),
        name: `CLI Session ${fingerprint}`,
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
    });
});
```

## CLI-Side Polling

```rust
async fn poll_device_token(device_code: &str, mut interval: u64) -> Result<Tokens> {
    let deadline = Instant::now() + Duration::from_secs(900);

    loop {
        if Instant::now() > deadline {
            return Err("Device code expired");
        }

        sleep(Duration::from_secs(interval)).await;

        let response = client.post("/api/v1/auth/device-token")
            .json(&json!({ "device_code": device_code, "client_id": CLIENT_ID }))
            .send()
            .await?;

        match response.status() {
            StatusCode::OK => return response.json().await,
            StatusCode::BAD_REQUEST => {
                let body: ErrorResponse = response.json().await?;
                match body.error.code.as_str() {
                    "authorization_pending" => continue,
                    "slow_down" => { interval += 5; continue; }
                    "expired_token" => return Err("Code expired"),
                    _ => return Err(body.error.message),
                }
            }
            StatusCode::TOO_MANY_REQUESTS => {
                interval += 5;
                continue;
            }
            _ => return Err("Unexpected response"),
        }
    }
}
```

## Verification Web Page

The `/verify` page must:
1. Require the user to be logged in (redirect to login first)
2. Accept `?code=ABCD1234` query parameter for auto-fill
3. Auto-submit if the code is complete and valid-looking
4. Normalize input (strip dashes, uppercase)
5. Show clear success/error feedback

The verification page requires authentication, accepts URL query parameter for auto-fill,
normalizes input (strips dashes, uppercases), and auto-submits if the code is complete.

## Cleanup

Expired device codes accumulate in the database. Run periodic cleanup:

```typescript
// Cron job: delete expired device codes
async function cleanupExpiredDeviceCodes(): Promise<number> {
    const result = await db.delete(deviceCodes)
        .where(lt(deviceCodes.expiresAt, new Date()))
        .returning({ id: deviceCodes.id });
    return result.length;
}
```

Schedule this in your cron configuration (e.g., every hour).
