# Protocol Design Template

> Before writing any code, create a protocol document. This is the contract
> between CLI and server that prevents miscommunication and design drift.
> The document should be committed to the repo and kept up to date.

## Template

```markdown
# CLI ↔ Web Protocol Design

## Goals
- Secure authentication (browser OAuth + API keys)
- [Your specific goals]

## API Versioning

All endpoints use the v1 prefix:
    /api/v1/auth/...
    /api/v1/resources/...

## Authentication

### Web Sessions
[Cookie-based auth mechanism description]

### CLI Authentication

#### Method 1: Browser OAuth (Primary)
1. CLI starts local HTTP server on ephemeral port
2. CLI opens browser to /api/v1/auth/cli-login?port=PORT&code_challenge=CHALLENGE&state=STATE
3. User authenticates via [identity provider]
4. Server redirects to localhost callback with authorization code
5. CLI exchanges code + PKCE verifier for tokens
6. Tokens stored in OS keychain

#### Method 2: Device Code (Headless)
1. CLI requests device code from /api/v1/auth/device-code
2. User visits verification URL and enters code
3. CLI polls /api/v1/auth/device-token until verified
4. Receives same tokens as browser flow

#### Method 3: API Keys (Automation)
1. User generates key via web UI
2. Key passed via environment variable or stored credential
3. Sent in Authorization header

### Token Format
- Access: <prefix>_<64 hex chars>
- Refresh: <prefix>_refresh_<64 hex chars>
- Validation: /^<prefix>_[a-f0-9]{64}$/

### Token Refresh
POST /api/v1/auth/refresh
{refresh_token: "..."}
→ {access_token, refresh_token, expires_in}

## Request Format

### Headers
| Header | Value | Required |
|--------|-------|----------|
| Authorization | Bearer <access_token> | Yes |
| User-Agent | <cli>/<version> (<platform>/<arch>) | Yes |
| Accept | application/json | Yes |
| Content-Type | application/json | For POST/PUT |
| X-Request-ID | <uuid> | Recommended |

### Timeouts and Retries
| Operation | Timeout | Retries | Backoff |
|-----------|---------|---------|---------|
| Auth | 30s | 0 | — |
| Read operations | 15s | 1 | 1s, 2s |
| Downloads | 120s | 2 | 1s, 2s, 4s |
| Uploads | 60s | 1 | 2s |
| Health check | 10s | 3 | 500ms, 1s, 2s |

### Rate Limiting Headers
| Header | Meaning |
|--------|---------|
| X-RateLimit-Limit | Requests per window |
| X-RateLimit-Remaining | Requests remaining |
| X-RateLimit-Reset | Unix timestamp of window reset |
| Retry-After | Seconds to wait (on 429) |

## Error Envelope

{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable message",
        "details": { ... }
    }
}

### Error Codes
| Code | HTTP | CLI Message |
|------|------|-------------|
| UNAUTHORIZED | 401 | "Run `<cli> login`" |
| TOKEN_EXPIRED | 401 | "Session expired. Run `<cli> login`" |
| SUBSCRIPTION_REQUIRED | 403 | "Active subscription required" |
| NOT_FOUND | 404 | "Resource not found: {id}" |
| RATE_LIMITED | 429 | "Rate limited. Retry in {n}s" |
| INTERNAL_ERROR | 500 | "Server error. Try again later." |

## Security Requirements
- [ ] PKCE (S256) on every OAuth code exchange
- [ ] CSRF state parameter on every PKCE flow
- [ ] Timing-safe comparison for all secret comparisons
- [ ] Tokens hashed (SHA-256) before database storage
- [ ] One-time use enforcement for auth codes
- [ ] Short-lived auth codes (≤60s)
- [ ] Tokens and API keys never appear in logs
- [ ] Rate limiting on all auth endpoints
```

## What the Protocol Doc Prevents

| Problem | Without Doc | With Doc |
|---------|-------------|----------|
| CLI sends wrong content-type | Server returns 415, CLI logs "unknown error" | Both sides agree on JSON |
| Token format drift | CLI generates 32-char tokens, server expects 64-char | Format spec is the source of truth |
| Error code inconsistency | CLI checks for "auth_required", server sends "UNAUTHORIZED" | Error codes enumerated once |
| Timeout mismatch | CLI times out at 5s, server takes 8s to respond | Timeouts agreed per operation |
| Retry storms | CLI retries auth failures, creating duplicate sessions | Retries specified per endpoint |

## When to Update the Protocol Doc

- New endpoint added → add to doc first
- Error code added → enumerate in doc
- Header added → document in headers table
- Rate limit changed → update limits table
- Security requirement added → update checklist
- Breaking change → version bump, migration notes

## Protocol Versioning

Use URL path versioning (`/api/v1/`, `/api/v2/`):

- `v1` endpoints remain functional during `v2` rollout
- CLI sends `Accept-Version` header for content negotiation
- Deprecated endpoints return `Deprecation: true` and `Sunset` headers
- CLI warns users when hitting deprecated endpoints
