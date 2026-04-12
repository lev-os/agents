# Token Lifecycle: Mint, Refresh, Revoke

> Tokens are the long-lived credentials that prove a CLI session is authorized.
> The lifecycle must handle concurrent processes, network failures, and account
> state changes (suspension, org policy changes) at every transition.

## Token Types

| Type | Prefix | Lifetime | Purpose |
|------|--------|----------|---------|
| Access Token | `jsm_` | 365 days | API authentication |
| Refresh Token | `jsm_refresh_` | 365 days | Mint new access tokens |
| API Key | `jsm_` | Until revoked | CI/CD, automation |

**Why distinct prefixes?** Prevents using an access token where a refresh token
is required (and vice versa). The server validates prefix before processing.

## Minting (Token Exchange)

Both PKCE and device code flows converge on the same token minting logic:

```typescript
// 1. Generate tokens
const accessToken = `jsm_${randomBytes(32).toString("hex")}`;   // 68 chars total
const refreshToken = `jsm_refresh_${randomBytes(32).toString("hex")}`; // 76 chars

// 2. Hash for storage (never store raw tokens)
const tokenHash = hashToken(accessToken);         // SHA-256
const refreshTokenHash = hashToken(refreshToken);

// 3. Create fingerprint from auth material (replay prevention)
const fingerprint = hashToken(codeChallenge).slice(0, 12);

// 4. Serialize on fingerprint (prevent concurrent exchange of same code)
await db.execute(sql`SELECT pg_advisory_xact_lock(hashtext(${fingerprint}))`);

// 5. Check for replay
const existing = await db.query.cliTokens.findFirst({
    where: like(cliTokens.name, `%${fingerprint}%`),
});
if (existing) throw new Error("Code already exchanged");

// 6. Insert token record
await db.insert(cliTokens).values({
    userId,
    tokenHash,
    refreshTokenHash,
    name: `CLI Session ${fingerprint}`,
    expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
});

// 7. Return to client (this is the ONLY time raw tokens leave the server)
return {
    access_token: accessToken,
    refresh_token: refreshToken,
    token_type: "Bearer",
    expires_in: 365 * 24 * 60 * 60,
    user_id: userId,
    email: user.email,
};
```

## Token Authentication (Every API Request)

```typescript
async function authenticateApiKey(rawToken: string): Promise<AuthUser | null> {
    // 1. Validate format
    if (!isCliTokenValue(rawToken)) return null;

    // 2. Hash and look up
    const hash = hashToken(rawToken);
    const record = await db.query.cliTokens.findFirst({
        where: eq(cliTokens.tokenHash, hash),
    });

    // 3. Try legacy hash format (migration support)
    if (!record) {
        const legacyHash = hashTokenLegacy(rawToken);
        const legacyRecord = await db.query.cliTokens.findFirst({
            where: eq(cliTokens.tokenHash, legacyHash),
        });
        if (legacyRecord) {
            // Auto-migrate to new hash format
            await db.update(cliTokens)
                .set({ tokenHash: hash })
                .where(eq(cliTokens.id, legacyRecord.id));
            return buildAuthUser(legacyRecord);
        }
        return null;
    }

    // 4. Check expiry
    if (record.expiresAt && record.expiresAt < new Date()) return null;

    // 5. Check user status
    const user = await getUser(record.userId);
    if (user?.suspended) return "suspended";

    // 6. Debounced lastUsedAt update (1-hour granularity)
    const oneHourAgo = new Date(Date.now() - 3600_000);
    if (!record.lastUsedAt || record.lastUsedAt < oneHourAgo) {
        await db.update(cliTokens)
            .set({ lastUsedAt: new Date() })
            .where(eq(cliTokens.id, record.id));
    }

    return buildAuthUser(record, user);
}
```

### Why Debounced `lastUsedAt`?

Updating on every request would create write amplification. 1-hour granularity
gives useful "last active" data without per-request DB writes.

## Token Refresh

```
POST /api/v1/auth/refresh
Content-Type: application/json

{
    "refresh_token": "jsm_refresh_abc123..."
}
```

### Server Implementation

```typescript
async function handleRefresh(refreshToken: string) {
    // 1. Validate prefix — MUST be a refresh token
    if (!isRefreshTokenValue(refreshToken)) {
        throw new Error("Invalid refresh token format");
    }

    // 2. Block access tokens from being used for refresh
    if (isCliTokenValue(refreshToken) && !refreshToken.startsWith("jsm_refresh_")) {
        throw new Error("Access tokens cannot be used for refresh");
    }

    // 3. Look up by refresh token hash
    const hash = hashToken(refreshToken);
    const record = await db.query.cliTokens.findFirst({
        where: eq(cliTokens.refreshTokenHash, hash),
    });
    if (!record) throw new Error("Unknown refresh token");

    // 4. Check expiry and user status
    if (record.expiresAt && record.expiresAt < new Date()) {
        throw new Error("Refresh token expired");
    }
    const user = await getUser(record.userId);
    if (user?.suspended) throw new Error("Account suspended");

    // 5. Serialize concurrent refreshes (advisory lock)
    await db.execute(sql`SELECT pg_advisory_xact_lock(hashtext(${hash}))`);

    // 6. Mint new access token (keep existing refresh token)
    const newAccessToken = generateToken("jsm");
    const newTokenHash = hashToken(newAccessToken);

    // 7. Atomic update
    await db.update(cliTokens)
        .set({
            tokenHash: newTokenHash,
            expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
        })
        .where(eq(cliTokens.id, record.id));

    return {
        access_token: newAccessToken,
        refresh_token: refreshToken, // Same refresh token persists
        token_type: "Bearer",
        expires_in: 365 * 24 * 60 * 60,
    };
}
```

### Why Advisory Lock on Refresh?

Without it, two concurrent refresh requests could both succeed:
1. Request A reads old token hash
2. Request B reads old token hash
3. Request A writes new hash → old token now invalid
4. Request B writes new hash → Request A's new token now invalid

The advisory lock serializes: only one refresh can proceed at a time.

## Token Revocation

```
POST /api/v1/auth/revoke
Content-Type: application/json

{
    "token": "jsm_abc123..."   // or "jsm_refresh_abc123..."
}
```

### Server Implementation

```typescript
async function handleRevoke(token: string) {
    const hash = hashToken(token);

    // Try both columns (access token or refresh token)
    let deleted = await db.delete(cliTokens)
        .where(eq(cliTokens.tokenHash, hash))
        .returning({ id: cliTokens.id });

    if (deleted.length === 0) {
        deleted = await db.delete(cliTokens)
            .where(eq(cliTokens.refreshTokenHash, hash))
            .returning({ id: cliTokens.id });
    }

    return { revoked: deleted.length > 0 };
}
```

### CLI Logout Flow

```rust
async fn logout() -> Result<()> {
    let creds = load_credentials()?;

    // 1. Revoke all tokens on server (best-effort)
    for token in [&creds.access_token, &creds.refresh_token].iter().flatten() {
        let _ = client.post("/api/v1/auth/revoke")
            .json(&json!({ "token": token }))
            .send()
            .await; // Ignore errors — server may be unreachable
    }

    // 2. Clear local credentials (always succeeds)
    delete_credentials()?;

    println!("Logged out successfully");
    Ok(())
}
```

**Critical:** Always clear local credentials even if server revocation fails.
The user expects `logout` to be effective locally regardless of network state.

## Hash Migration Strategy

When changing hash algorithms (e.g., HMAC-SHA256 → plain SHA-256):

```typescript
// Authentication tries new hash first, then legacy
async function authenticateWithMigration(token: string) {
    // Try current hash
    let record = await lookupByHash(hashToken(token));

    if (!record) {
        // Try legacy hash
        record = await lookupByHash(hashTokenLegacy(token));
        if (record) {
            // Auto-migrate on successful auth
            await updateHash(record.id, hashToken(token));
        }
    }

    return record;
}
```

This is transparent to users — tokens continue working across the migration.

## Expiry Timeline

```
Day 0: Token minted (365-day expiry)
  │
  ├── Day 1-364: Normal use, lastUsedAt updated hourly
  │
  ├── Day 300: CLI could warn "token expires in 65 days"
  │
  ├── Day 364: CLI auto-refreshes (within 30s safety window)
  │
  └── Day 365: Token expires → CLI prompts re-login
```

## Concurrent Process Safety

Multiple CLI processes may share the same credentials:

```
Process A: jsm sync     ─── uses access_token ───▶ 200 OK
Process B: jsm install  ─── uses access_token ───▶ 200 OK
Process A: refresh      ─── mints new token   ───▶ new_token_A
Process B: API call     ─── uses OLD token    ───▶ 401 (old token invalid)
Process B: refresh      ─── uses refresh_token ──▶ new_token_B (locks, waits for A)
```

The advisory lock prevents this race. Process B's refresh waits for A to complete,
then reads the already-updated record and returns the same new token.
