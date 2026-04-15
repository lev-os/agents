# Server-Side Implementation Guide

> This guide covers the complete server-side architecture for a SaaS CLI auth
> system. The implementation is framework-agnostic but uses Next.js API routes
> as the reference example.

## Endpoint Architecture

```
/api/v1/auth/
├── cli-login/route.ts      # GET  — Initiate browser PKCE flow
├── callback/route.ts       # GET  — Generate auth code after web login
├── token/route.ts          # POST — Exchange auth code for tokens (PKCE)
├── device-code/route.ts    # POST — Create device code
├── device-verify/route.ts  # POST — User verifies device code (browser)
├── device-token/route.ts   # POST — CLI exchanges device code for tokens
├── refresh/route.ts        # POST — Refresh access token
└── revoke/route.ts         # POST — Revoke token (logout)
```

## Route: `/api/v1/auth/cli-login` (GET)

**Purpose:** Entry point for browser PKCE flow. Validates CLI parameters,
creates a signed flow cookie, and redirects to web login.

```typescript
export async function GET(request: NextRequest) {
    const params = request.nextUrl.searchParams;

    // 1. Validate inputs
    const port = params.get("port");
    const codeChallenge = params.get("code_challenge");
    const state = params.get("state");

    if (!port || !isValidPort(port)) return error(400, "Invalid port");
    if (!codeChallenge || !isValidPkceCodeChallenge(codeChallenge))
        return error(400, "Invalid PKCE challenge");
    if (!state || !isValidCliState(state))
        return error(400, "Invalid state parameter");

    // 2. Sign flow data into tamper-proof payload
    const flowPayload = JSON.stringify({ port, codeChallenge, state });
    const signedFlow = sign(flowPayload);

    // 3. Create response with flow cookie
    const response = new NextResponse();
    response.cookies.set("cli_flow", Buffer.from(signedFlow).toString("base64url"), {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        maxAge: 600, // 10 minutes
        path: "/api/v1/auth",
    });

    // 4. Check if user is already authenticated
    const user = await getAuthenticatedUser(request);

    if (user) {
        // Already logged in → go straight to callback
        return redirect("/api/v1/auth/callback", response);
    } else {
        // Not logged in → send through login flow
        return redirect("/login?next=/api/v1/auth/callback", response);
    }
}
```

## Route: `/api/v1/auth/callback` (GET)

**Purpose:** After web login completes, generates a signed authorization code
and serves a callback page that directs the user back to the CLI.

```typescript
export async function GET(request: NextRequest) {
    // 1. Verify user is authenticated
    const user = await getAuthenticatedUser(request);
    if (!user) return redirect("/login?next=/api/v1/auth/callback");

    // 2. Check SSO/org policy enforcement
    const ssoDecision = await getOrgSsoPolicy(user);
    if (ssoDecision.action !== "allow") {
        return redirect(`/login?sso_required=${ssoDecision.provider}`);
    }

    // 3. Read and verify flow cookie
    const flowCookie = request.cookies.get("cli_flow")?.value;
    if (!flowCookie) return error(400, "Missing CLI flow state");

    const decoded = Buffer.from(flowCookie, "base64url").toString();
    const flowPayload = verify(decoded); // HMAC verification
    if (!flowPayload) return error(400, "Invalid flow state");

    const flowData = JSON.parse(flowPayload);
    const { port, codeChallenge, state } = flowData;

    // 4. Create signed authorization code (60-second expiry)
    const codePayload = JSON.stringify({
        userId: user.id,
        codeChallenge,
        expiresAt: new Date(Date.now() + 60_000).toISOString(),
    });
    const authCode = sign(codePayload);

    // 5. Build loopback callback URL
    const loopbackUrl = buildCliLoopbackCallbackUrl(port, authCode, state);

    // 6. Serve callback page (with <img> tag for best-effort callback)
    const html = buildCliCallbackPageHtml(loopbackUrl);

    // 7. Delete flow cookie (one-time use)
    const response = new NextResponse(html, {
        headers: { "Content-Type": "text/html; charset=utf-8" },
    });
    response.cookies.delete("cli_flow");

    return response;
}
```

## Route: `/api/v1/auth/token` (POST)

**Purpose:** Exchange a PKCE authorization code for access and refresh tokens.
This is the most security-critical endpoint.

```typescript
export async function POST(request: NextRequest) {
    const body = await request.json();
    const { code, code_verifier } = body;

    // 1. Verify authorization code signature
    const payload = verify(code);
    if (!payload) return error(401, "Invalid authorization code");

    const { userId, codeChallenge, expiresAt } = JSON.parse(payload);

    // 2. Check expiration (60-second window)
    if (new Date(expiresAt) < new Date()) {
        return error(401, "Authorization code expired");
    }

    // 3. Verify PKCE: SHA256(code_verifier) must equal code_challenge
    const computedChallenge = base64url(sha256(code_verifier));
    if (!timingSafeEqual(computedChallenge, codeChallenge)) {
        return error(401, "PKCE verification failed");
    }

    // 4. Create code fingerprint for replay prevention
    const fingerprint = hashToken(codeChallenge).slice(0, 12);

    // 5. Serialize on fingerprint (prevent concurrent exchange)
    await db.execute(sql`SELECT pg_advisory_xact_lock(hashtext(${fingerprint}))`);

    // 6. Check for replay (fingerprint already in session name)
    const existing = await db.query.cliTokens.findFirst({
        where: like(cliTokens.name, `%${fingerprint}%`),
    });
    if (existing) return error(409, "Code already exchanged");

    // 7. Verify user exists and is not suspended
    const user = await getUser(userId);
    if (!user) return error(404, "User not found");
    if (user.suspended) return error(403, "Account suspended");

    // 8. Generate tokens
    const accessToken = generateToken("jsm");
    const refreshToken = generateToken("jsm_refresh");

    // 9. Store hashed tokens
    await db.insert(cliTokens).values({
        userId,
        tokenHash: hashToken(accessToken),
        refreshTokenHash: hashToken(refreshToken),
        name: `CLI Session ${fingerprint}`,
        expiresAt: new Date(Date.now() + 365 * 86400 * 1000),
    });

    // 10. Return tokens (only time raw tokens leave server)
    return NextResponse.json({
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: "Bearer",
        expires_in: 365 * 86400,
        user_id: userId,
        email: user.email,
    });
}
```

## Route: `/api/v1/auth/device-code` (POST)

```typescript
export async function POST(request: NextRequest) {
    const body = await request.json();
    const clientId = body.client_id;

    if (clientId !== "my-cli") return error(400, "Unknown client");

    const created = await createDeviceCode(clientId);
    const baseUrl = process.env.NEXT_PUBLIC_URL;

    return NextResponse.json({
        device_code: created.deviceCode,
        user_code: formatUserCode(created.userCode),
        verification_url: `${baseUrl}/verify`,
        verification_url_complete: `${baseUrl}/verify?code=${formatUserCode(created.userCode)}`,
        expires_in: DEVICE_CODE_CONFIG.expiresIn,
        interval: DEVICE_CODE_CONFIG.interval,
    });
}
```

## Route: `/api/v1/auth/device-verify` (POST)

```typescript
export async function POST(request: NextRequest) {
    // 1. Require authenticated user
    const user = await getAuthenticatedUser(request);
    if (!user) return error(401, "Authentication required");

    const body = await request.json();
    const rawCode = body.user_code;

    // 2. Normalize and validate
    const normalized = normalizeUserCode(rawCode);
    if (normalized.length !== 8) return error(400, "Invalid code format");

    // 3. Look up (non-expired only)
    const deviceCode = await getDeviceCodeByUserCode(normalized);
    if (!deviceCode) return error(404, "Code not found or expired");

    // 4. Atomic verification (race-safe)
    const verified = await verifyDeviceCode(deviceCode.id, user.id);
    if (!verified) return error(409, "Code already verified");

    return NextResponse.json({ success: true });
}
```

## Route: `/api/v1/auth/device-token` (POST)

```typescript
export async function POST(request: NextRequest) {
    const body = await request.json();
    const { device_code, client_id } = body;

    // 1. Look up (include expired for better error messages)
    const record = await getDeviceCodeByCode(device_code, { includeExpired: true });
    if (!record) return error(400, "invalid_grant", "Unknown device code");

    // 2. Check expiry
    if (record.expiresAt < new Date()) {
        return error(400, "expired_token", "Device code expired");
    }

    // 3. Check verification state
    const state = getDeviceCodeVerificationState(record);

    if (state === "pending") {
        return error(400, "authorization_pending", "User has not yet verified");
    }

    if (state === "corrupt") {
        return error(500, "server_error", "Device code in corrupt state");
    }

    // state === "verified"
    // 4. Check user status
    const user = await getUser(record.userId!);
    if (!user) return error(404, "User not found");
    if (user.suspended) return error(403, "Account suspended");

    // 5. Generate tokens
    const accessToken = generateToken("jsm");
    const refreshToken = generateToken("jsm_refresh");

    // 6. Atomic: delete device code + insert CLI token
    await db.transaction(async (tx) => {
        await tx.delete(deviceCodes).where(eq(deviceCodes.id, record.id));
        await tx.insert(cliTokens).values({
            userId: record.userId!,
            tokenHash: hashToken(accessToken),
            refreshTokenHash: hashToken(refreshToken),
            name: `CLI Device ${device_code.slice(0, 8)}`,
            expiresAt: new Date(Date.now() + 365 * 86400 * 1000),
        });
    });

    return NextResponse.json({
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: "Bearer",
        expires_in: 365 * 86400,
        user_id: record.userId,
        email: user.email,
    });
}
```

## Shared Utilities

### Cryptographic Primitives

```typescript
// crypto.ts
import { createHash, createHmac, randomBytes, timingSafeEqual } from "crypto";

const JWT_SECRET = process.env.JWT_SECRET!; // Min 32 chars

export function generateToken(prefix: string, length = 32): string {
    return `${prefix}_${randomBytes(length).toString("hex")}`;
}

export function hashToken(token: string): string {
    return createHash("sha256").update(token).digest("hex");
}

export function sign(payload: string): string {
    const sig = createHmac("sha256", JWT_SECRET).update(payload).digest("base64url");
    return `${payload}.${sig}`;
}

export function verify(signed: string): string | null {
    const lastDot = signed.lastIndexOf(".");
    if (lastDot === -1) return null;

    const payload = signed.slice(0, lastDot);
    const signature = signed.slice(lastDot + 1);

    const expected = createHmac("sha256", JWT_SECRET).update(payload).digest("base64url");
    if (!timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) return null;

    return payload;
}
```

### Error Response Helper

```typescript
// Overloaded: error(status, message) or error(status, code, message)
function error(status: number, codeOrMessage: string, message?: string) {
    const code = message ? codeOrMessage : "error";
    const msg = message ?? codeOrMessage;
    return NextResponse.json(
        { error: { code, message: msg } },
        { status }
    );
}
```

## API Versioning and Deprecation

When migrating auth endpoints (e.g., `/api/cli/auth` → `/api/v1/auth/cli-login`):

```typescript
// Legacy route: identical behavior + deprecation headers
export async function GET(request: NextRequest) {
    const response = await newEndpoint(request);
    response.headers.set("Deprecation", "true");
    response.headers.set("Sunset", "Fri, 01 Apr 2026 00:00:00 GMT");
    response.headers.set("Link", '</api/v1/auth/cli-login>; rel="successor-version"');
    return response;
}
```

## Rate Limiting

Auth endpoints need stricter rate limits than regular API:

| Endpoint | Limit | Window | Why |
|----------|-------|--------|-----|
| cli-login | 10 | 1 min | Prevents flow spam |
| token | 5 | 1 min | Code exchange is once per login |
| device-code | 10 | 1 min | Prevents code pool exhaustion |
| device-token | 60 | 1 min | Polling needs headroom |
| refresh | 10 | 1 min | Normal refresh is infrequent |
| revoke | 10 | 1 min | Logout is infrequent |

Subscribers can bypass rate limits (they've proven identity via payment).
