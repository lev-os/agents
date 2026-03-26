# Testing Strategies for CLI Auth

> CLI auth spans multiple systems (CLI binary, web server, identity provider,
> database, keyring) making end-to-end testing challenging. This guide covers
> testing at each layer.

## Test Layers

```
┌─────────────────────────────────────────────────┐
│ Layer 4: E2E (real CLI → real server → real IdP) │ ← Expensive, fragile
├─────────────────────────────────────────────────┤
│ Layer 3: Integration (API routes with real DB)   │ ← Core value
├─────────────────────────────────────────────────┤
│ Layer 2: Unit (crypto, validation, state logic)  │ ← Fast, stable
├─────────────────────────────────────────────────┤
│ Layer 1: Smoke (health check, connectivity)      │ ← CI gate
└─────────────────────────────────────────────────┘
```

## Layer 2: Unit Tests

### PKCE Validation

```typescript
describe("PKCE validation", () => {
    it("accepts valid code challenges", () => {
        // 43-128 chars, base64url-safe
        expect(isValidPkceCodeChallenge("a".repeat(43))).toBe(true);
        expect(isValidPkceCodeChallenge("ABCDEFabcdef0123456789-._~".repeat(2))).toBe(true);
    });

    it("rejects invalid challenges", () => {
        expect(isValidPkceCodeChallenge("short")).toBe(false);       // < 43 chars
        expect(isValidPkceCodeChallenge("a".repeat(129))).toBe(false); // > 128 chars
        expect(isValidPkceCodeChallenge("has spaces here")).toBe(false);
        expect(isValidPkceCodeChallenge("has+plus")).toBe(false);
    });
});
```

### State Validation

```typescript
describe("CLI state validation", () => {
    it("accepts 22-128 char states", () => {
        expect(isValidCliState("a".repeat(22))).toBe(true);  // Min length
        expect(isValidCliState("a".repeat(128))).toBe(true); // Max length
    });

    it("rejects invalid states", () => {
        expect(isValidCliState("a".repeat(21))).toBe(false);  // Too short
        expect(isValidCliState("a".repeat(129))).toBe(false); // Too long
    });
});
```

### Device Code Generation

```typescript
describe("device code generation", () => {
    it("generates 8-char codes from ambiguity-safe alphabet", () => {
        const code = generateUserCode();
        expect(code).toHaveLength(8);
        expect(code).toMatch(/^[ABCDEFGHJKMNPQRSTUVWXYZ23456789]{8}$/);
    });

    it("formats as XXXX-YYYY", () => {
        expect(formatUserCode("ABCD1234")).toBe("ABCD-1234");
    });

    it("normalizes input", () => {
        expect(normalizeUserCode("abcd-1234")).toBe("ABCD1234");
        expect(normalizeUserCode("  AbCd  1234  ")).toBe("ABCD1234");
        expect(normalizeUserCode("ABCD.1234")).toBe("ABCD1234");
    });

    it("generates unique codes", () => {
        const codes = new Set(Array.from({ length: 100 }, () => generateUserCode()));
        expect(codes.size).toBe(100); // All unique (probabilistic)
    });
});
```

### Token Format Validation

```typescript
describe("token validation", () => {
    it("validates access tokens", () => {
        expect(isCliTokenValue("jsm_" + "a".repeat(64))).toBe(true);
        expect(isCliTokenValue("jsm_" + "f".repeat(64))).toBe(true);
        expect(isCliTokenValue("jsm_short")).toBe(false);
        expect(isCliTokenValue("invalid_" + "a".repeat(64))).toBe(false);
    });

    it("validates refresh tokens", () => {
        expect(isRefreshTokenValue("jsm_refresh_" + "a".repeat(64))).toBe(true);
        expect(isRefreshTokenValue("jsm_" + "a".repeat(64))).toBe(false);
    });
});
```

### Signing and Verification

```typescript
describe("sign/verify", () => {
    it("round-trips correctly", () => {
        const payload = JSON.stringify({ userId: "123", expiresAt: "2026-01-01" });
        const signed = sign(payload);
        expect(verify(signed)).toBe(payload);
    });

    it("rejects tampered payloads", () => {
        const signed = sign("original");
        const tampered = signed.replace("original", "changed");
        expect(verify(tampered)).toBeNull();
    });

    it("rejects truncated signatures", () => {
        const signed = sign("payload");
        const truncated = signed.slice(0, -5);
        expect(verify(truncated)).toBeNull();
    });
});
```

## Layer 3: Integration Tests (API Routes)

### Token Exchange

```typescript
describe("POST /api/v1/auth/token", () => {
    it("exchanges valid code for tokens", async () => {
        // Create a valid signed code
        const verifier = "a".repeat(43);
        const challenge = base64url(sha256(verifier));
        const code = sign(JSON.stringify({
            userId: testUser.id,
            codeChallenge: challenge,
            expiresAt: new Date(Date.now() + 60_000).toISOString(),
        }));

        const response = await POST(mockRequest({
            body: { code, code_verifier: verifier },
        }));

        expect(response.status).toBe(200);
        const body = await response.json();
        expect(body.access_token).toMatch(/^jsm_[a-f0-9]{64}$/);
        expect(body.refresh_token).toMatch(/^jsm_refresh_[a-f0-9]{64}$/);
        expect(body.token_type).toBe("Bearer");
    });

    it("rejects expired codes", async () => {
        const code = sign(JSON.stringify({
            userId: testUser.id,
            codeChallenge: "x".repeat(43),
            expiresAt: new Date(Date.now() - 1000).toISOString(), // Already expired
        }));

        const response = await POST(mockRequest({
            body: { code, code_verifier: "x".repeat(43) },
        }));

        expect(response.status).toBe(401);
    });

    it("rejects PKCE mismatch", async () => {
        const challenge = base64url(sha256("correct_verifier" + "x".repeat(30)));
        const code = sign(JSON.stringify({
            userId: testUser.id,
            codeChallenge: challenge,
            expiresAt: new Date(Date.now() + 60_000).toISOString(),
        }));

        const response = await POST(mockRequest({
            body: { code, code_verifier: "wrong_verifier" + "x".repeat(30) },
        }));

        expect(response.status).toBe(401);
    });

    it("prevents code replay", async () => {
        const verifier = "b".repeat(43);
        const challenge = base64url(sha256(verifier));
        const code = sign(JSON.stringify({
            userId: testUser.id,
            codeChallenge: challenge,
            expiresAt: new Date(Date.now() + 60_000).toISOString(),
        }));

        // First exchange succeeds
        const r1 = await POST(mockRequest({ body: { code, code_verifier: verifier } }));
        expect(r1.status).toBe(200);

        // Second exchange fails (replay)
        const r2 = await POST(mockRequest({ body: { code, code_verifier: verifier } }));
        expect(r2.status).toBe(409);
    });
});
```

### Device Code Flow

```typescript
describe("device code flow", () => {
    it("creates device code", async () => {
        const response = await POST("/api/v1/auth/device-code", {
            body: { client_id: "my-cli" },
        });

        expect(response.status).toBe(200);
        const body = await response.json();
        expect(body.user_code).toMatch(/^[A-Z0-9]{4}-[A-Z0-9]{4}$/);
        expect(body.expires_in).toBe(900);
        expect(body.interval).toBe(5);
    });

    it("returns pending before verification", async () => {
        const { device_code } = await createDeviceCode();

        const response = await POST("/api/v1/auth/device-token", {
            body: { device_code, client_id: "my-cli" },
        });

        expect(response.status).toBe(400);
        const body = await response.json();
        expect(body.error.code).toBe("authorization_pending");
    });

    it("returns tokens after verification", async () => {
        const { device_code, user_code } = await createDeviceCode();

        // Simulate user verification
        await verifyDeviceCodeAsUser(user_code, testUser.id);

        const response = await POST("/api/v1/auth/device-token", {
            body: { device_code, client_id: "my-cli" },
        });

        expect(response.status).toBe(200);
        const body = await response.json();
        expect(body.access_token).toMatch(/^jsm_[a-f0-9]{64}$/);
    });

    it("consumes device code on exchange", async () => {
        const { device_code, user_code } = await createDeviceCode();
        await verifyDeviceCodeAsUser(user_code, testUser.id);

        // First exchange
        const r1 = await POST("/api/v1/auth/device-token", {
            body: { device_code, client_id: "my-cli" },
        });
        expect(r1.status).toBe(200);

        // Second exchange fails (consumed)
        const r2 = await POST("/api/v1/auth/device-token", {
            body: { device_code, client_id: "my-cli" },
        });
        expect(r2.status).toBe(400);
    });
});
```

## Layer 1: Smoke Tests

```typescript
describe("health checks", () => {
    it("live endpoint responds quickly", async () => {
        const start = Date.now();
        const response = await fetch("/api/health/live");
        const elapsed = Date.now() - start;

        expect(response.status).toBe(200);
        expect(elapsed).toBeLessThan(1000); // < 1s
    });
});
```

## CLI-Side Test Patterns

```rust
#[cfg(test)]
mod tests {
    // Use test credentials from environment
    fn skip_if_no_test_creds() {
        if std::env::var("TEST_API_URL").is_err() {
            eprintln!("Skipping: TEST_API_URL not set");
            return;
        }
    }

    // Mock keyring for tests
    fn with_mock_keyring<F: FnOnce()>(f: F) {
        // Use temp file storage instead of real keyring
        let dir = tempdir().unwrap();
        std::env::set_var("MY_CLI_CONFIG_DIR", dir.path());
        f();
    }
}
```

## What to Test at Each Level

| Concern | Unit | Integration | E2E |
|---------|------|-------------|-----|
| PKCE math | Yes | — | — |
| Token format validation | Yes | — | — |
| State normalization | Yes | — | — |
| Code exchange happy path | — | Yes | — |
| Code replay prevention | — | Yes | — |
| Device code lifecycle | — | Yes | — |
| Suspension enforcement | — | Yes | — |
| Token refresh race | — | Yes | — |
| Full login flow | — | — | Yes |
| Credential storage | Unit (mock keyring) | — | Yes |
| Environment detection | Unit (mock env) | — | — |
