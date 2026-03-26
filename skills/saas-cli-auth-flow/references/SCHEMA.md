# Database Schema for CLI Auth

> Two tables power the CLI auth system: `cli_tokens` for long-lived sessions
> and `device_codes` for the transient device code flow.

## Table: `cli_tokens`

Stores hashed CLI session tokens. One row per active CLI session.

```sql
CREATE TABLE cli_tokens (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash          TEXT NOT NULL UNIQUE,
    refresh_token_hash  TEXT UNIQUE,
    name                TEXT NOT NULL,       -- e.g., "CLI Session a3f2b1"
    last_used_at        TIMESTAMPTZ,         -- Debounced (1-hour granularity)
    expires_at          TIMESTAMPTZ,         -- 365 days from creation/refresh
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for user lookups (list sessions, cleanup)
CREATE INDEX idx_cli_tokens_user_id ON cli_tokens(user_id);

-- Index for expiry-based cleanup
CREATE INDEX idx_cli_tokens_expires_at ON cli_tokens(expires_at)
    WHERE expires_at IS NOT NULL;
```

### Column Design Decisions

| Column | Decision | Why |
|--------|----------|-----|
| `token_hash` | SHA-256 of raw token | Database breach doesn't leak tokens |
| `refresh_token_hash` | Separate column | Can revoke access without losing refresh |
| `name` | Contains fingerprint | Enables replay detection (`LIKE '%fingerprint%'`) |
| `last_used_at` | Debounced 1-hour | Useful analytics without per-request writes |
| `expires_at` | Nullable | API keys may not expire |

### Why Not JWT?

JWTs are stateless — you can't revoke them server-side without a blocklist.
For CLI tokens that may live 365 days, server-side revocation is essential.
Opaque tokens with server-side lookup give:
- Instant revocation (delete the row)
- Last-used tracking
- Session enumeration (list all active sessions)
- No clock-skew issues

## Table: `device_codes`

Transient storage for the RFC 8628 device code flow. Rows are created when the
CLI requests a code and deleted when the code is consumed or expires.

```sql
CREATE TABLE device_codes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code TEXT NOT NULL UNIQUE,       -- 64 hex chars (32 random bytes)
    user_code   TEXT NOT NULL UNIQUE,       -- 8 ambiguity-safe chars
    user_id     UUID REFERENCES users(id),  -- NULL until user verifies
    client_id   TEXT NOT NULL,              -- "my-cli"
    verified_at TIMESTAMPTZ,               -- NULL until user verifies
    expires_at  TIMESTAMPTZ NOT NULL,      -- 15 minutes from creation
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for polling lookups (by device_code)
CREATE INDEX idx_device_codes_device_code ON device_codes(device_code);

-- Index for verification lookups (by user_code, non-expired)
CREATE INDEX idx_device_codes_user_code ON device_codes(user_code)
    WHERE expires_at > now();

-- Index for cleanup (expired codes)
CREATE INDEX idx_device_codes_expires_at ON device_codes(expires_at);
```

### Column Design Decisions

| Column | Decision | Why |
|--------|----------|-----|
| `device_code` | 64 hex chars | High entropy, never shown to user |
| `user_code` | 8 chars, ambiguity-safe | Human-readable, typed on phones |
| `user_id` | Nullable | NULL until verified; NOT NULL = verified |
| `verified_at` | Nullable | Combined with user_id to detect corrupt state |
| `expires_at` | 15 min | Short window limits brute-force exposure |

### State Derivation from Columns

Rather than a `status` enum, the state is derived from `user_id` and `verified_at`:

```
user_id=NULL, verified_at=NULL   → PENDING
user_id=SET,  verified_at=SET    → VERIFIED
user_id=SET,  verified_at=NULL   → CORRUPT (should not happen)
user_id=NULL, verified_at=SET    → CORRUPT (should not happen)
```

This avoids enum drift and makes the state machine self-documenting.

## ORM Schema (Drizzle Example)

```typescript
import { pgTable, uuid, text, timestamp, uniqueIndex } from "drizzle-orm/pg-core";

export const cliTokens = pgTable("cli_tokens", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
    tokenHash: text("token_hash").notNull().unique(),
    refreshTokenHash: text("refresh_token_hash").unique(),
    name: text("name").notNull(),
    lastUsedAt: timestamp("last_used_at", { withTimezone: true }),
    expiresAt: timestamp("expires_at", { withTimezone: true }),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const deviceCodes = pgTable("device_codes", {
    id: uuid("id").primaryKey().defaultRandom(),
    deviceCode: text("device_code").notNull().unique(),
    userCode: text("user_code").notNull().unique(),
    userId: uuid("user_id").references(() => users.id),
    clientId: text("client_id").notNull(),
    verifiedAt: timestamp("verified_at", { withTimezone: true }),
    expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});
```

## Migration Template

```sql
-- Migration: add_cli_auth_tables
-- Description: Create tables for CLI token management and device code flow

CREATE TABLE IF NOT EXISTS cli_tokens (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash          TEXT NOT NULL UNIQUE,
    refresh_token_hash  TEXT UNIQUE,
    name                TEXT NOT NULL,
    last_used_at        TIMESTAMPTZ,
    expires_at          TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS device_codes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code TEXT NOT NULL UNIQUE,
    user_code   TEXT NOT NULL UNIQUE,
    user_id     UUID REFERENCES users(id),
    client_id   TEXT NOT NULL,
    verified_at TIMESTAMPTZ,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cli_tokens_user_id ON cli_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_cli_tokens_expires_at ON cli_tokens(expires_at)
    WHERE expires_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_device_codes_device_code ON device_codes(device_code);
CREATE INDEX IF NOT EXISTS idx_device_codes_user_code ON device_codes(user_code);
CREATE INDEX IF NOT EXISTS idx_device_codes_expires_at ON device_codes(expires_at);
```

## Cleanup Cron

Schedule periodic cleanup of expired records:

```typescript
// Run hourly or daily
async function cleanupAuthTables() {
    // Delete expired device codes
    const expiredCodes = await db.delete(deviceCodes)
        .where(lt(deviceCodes.expiresAt, new Date()))
        .returning({ id: deviceCodes.id });

    // Delete expired CLI tokens
    const expiredTokens = await db.delete(cliTokens)
        .where(and(
            isNotNull(cliTokens.expiresAt),
            lt(cliTokens.expiresAt, new Date())
        ))
        .returning({ id: cliTokens.id });

    logger.info({
        expiredDeviceCodes: expiredCodes.length,
        expiredCliTokens: expiredTokens.length,
    }, "Auth table cleanup completed");
}
```
