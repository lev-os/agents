---
name: saas-cli-auth-flow
description: >-
  SaaS CLI-to-web auth: PKCE OAuth, RFC 8628 device code, token lifecycle, secure storage.
  Use when building CLI login, device-code verify, token refresh, or headless SSH auth.
---

<!-- TOC: Three-Tier Architecture | Environment Detection | Implementation Loop | Security Invariants | Token Format | Endpoints | Anti-Patterns | Credential Storage | Checklist | References -->

# SaaS CLI Authentication Flow

> **The One Rule:** A CLI user must authenticate against a web service without ever
> exposing credentials in transit, in logs, or at rest — and it must work whether the
> user has a local browser, is SSH'd into a remote server, or is running in CI.

## The Three-Tier Auth Architecture

Every SaaS CLI needs three authentication paths. Users don't choose — the CLI
auto-detects the environment and picks the best available tier.

```
Tier 1: Browser PKCE        Tier 2: Manual PKCE         Tier 3: Device Code (RFC 8628)
(local machine + browser)   (SSH/headless + copy-paste)  (fully headless, no loopback)
┌──────────────┐            ┌──────────────┐             ┌──────────────┐
│ CLI binds    │            │ CLI prints   │             │ CLI requests │
│ localhost    │            │ auth URL     │             │ device code  │
│ :random_port │            │ to stderr    │             │ from server  │
└──────┬───────┘            └──────┬───────┘             └──────┬───────┘
       │ opens browser             │ user opens                 │ displays
       ▼                           │ URL manually               ▼ ABCD-1234
┌──────────────┐            ┌──────┴───────┐             ┌──────────────┐
│ Web login    │            │ Web login    │             │ User visits  │
│ (Google, etc)│            │ + callback   │             │ /verify page │
└──────┬───────┘            │ page shows   │             │ enters code  │
       │ redirect to        │ copy button  │             └──────┬───────┘
       │ localhost:port     └──────┬───────┘                    │ server marks
       ▼                           │ user pastes                │ code verified
┌──────────────┐            ┌──────┴───────┐             ┌──────────────┐
│ CLI receives │            │ CLI parses   │             │ CLI polls    │
│ code+state   │            │ pasted URL   │             │ until verified│
│ on callback  │            │ from stdin   │             │ then exchanges│
└──────┬───────┘            └──────┬───────┘             └──────┬───────┘
       │                           │                            │
       ▼                           ▼                            ▼
       ──── All three converge on token minting (same output) ────
              Tier 1+2: POST /api/v1/auth/token
              Tier 3:   POST /api/v1/auth/device-token
              → { access_token, refresh_token }
```

### Environment Detection Logic

```
is_interactive()?
├── NO → Error: "Cannot authenticate in non-interactive mode. Use API key."
└── YES
    ├── --remote flag? → Tier 3 (device code)
    ├── --manual flag? → Tier 2 (manual PKCE)
    └── auto-detect:
        ├── SSH_CLIENT or SSH_TTY set? → Tier 3
        ├── Linux: DISPLAY or WAYLAND_DISPLAY set? → Tier 1
        ├── macOS: always has GUI → Tier 1
        ├── Windows: always has GUI → Tier 1
        └── fallback → Tier 2
```

## The Implementation Loop

```
1. Design protocol doc first (endpoints, error codes, security reqs)
2. Implement Tier 1 (browser PKCE) — the happy path
3. Add Tier 2 (manual paste) — minimal delta from Tier 1
4. Add Tier 3 (device code) — independent flow, new endpoints
5. Harden: timing-safe comparisons, replay prevention, race conditions
6. Add token refresh + revocation
7. Add secure credential storage (keyring → encrypted file fallback)
8. Iterate: abuse tracking, SSO enforcement, suspension checks
```

## Security Invariants (Non-Negotiable)

| Invariant | Why | How |
|-----------|-----|-----|
| PKCE (RFC 7636) on every code exchange | Prevents authorization code interception | SHA-256 challenge/verifier pair |
| CSRF state token | Prevents cross-site request forgery | Random 22-128 char token, verified on callback |
| One-time auth codes | Prevents replay attacks | Advisory lock on code fingerprint, check before mint |
| Timing-safe comparison | Prevents timing side-channels | `crypto.timingSafeEqual()` for all token/hash comparisons |
| Tokens never in URLs or logs | Prevents credential leakage | Bearer header only, mask in logs: `jsm_abc...xyz` |
| Short-lived auth codes | Limits window for stolen codes | 60-second expiry on authorization codes |
| Hash tokens before storage | Database breach doesn't leak tokens | SHA-256 hash in DB, never store raw token |
| Atomic operations | Prevents race conditions | DB advisory locks for concurrent refresh/exchange |

## Token Format Convention

```
<prefix>_<random_hex>

Access:  <prefix>_<64 hex chars>          (32 random bytes)
Refresh: <prefix>_refresh_<64 hex chars>  (distinct prefix prevents misuse)
API Key: <prefix>_<64 hex chars>          (same format as access token;
                                           distinguished by issuance context,
                                           not prefix — both use server-side lookup)
```

**Validation regex:** `/^jsm_[a-f0-9]{64}$/` (access), `/^jsm_refresh_[a-f0-9]{64}$/` (refresh)

## Quick Reference: Endpoints

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/v1/auth/cli-login` | GET | Initiate browser PKCE flow | No (sets cookie) |
| `/api/v1/auth/callback` | GET | Generate auth code after login | Web session |
| `/api/v1/auth/token` | POST | Exchange auth code for tokens | No (code + verifier) |
| `/api/v1/auth/device-code` | POST | Create device code | No |
| `/api/v1/auth/device-verify` | POST | User verifies device code | Web session |
| `/api/v1/auth/device-token` | POST | CLI exchanges verified device code | No (device_code) |
| `/api/v1/auth/refresh` | POST | Refresh access token | Refresh token |
| `/api/v1/auth/revoke` | POST | Revoke token (logout) | Token being revoked |

## Anti-Patterns (Never Do)

| Anti-Pattern | Why It Fails | Do Instead |
|-------------|--------------|------------|
| Store raw tokens in DB | Database breach = full compromise | Hash with SHA-256, store hash only |
| Use timestamps as state tokens | Predictable, replayable | Cryptographic random bytes |
| Skip PKCE for "internal" CLIs | Same attack surface exists | Always PKCE, even internal tools |
| Retry auth code exchange on failure | Enables replay attacks | Fail permanently, user re-authenticates |
| Poll device-token without backoff | Server overload, rate limiting | Exponential backoff, honor `slow_down` |
| Single token for access + refresh | Can't rotate access without losing refresh | Distinct prefixes, independent lifecycle |
| Use JWT for CLI tokens | Can't revoke, clock skew issues | Opaque tokens + server-side lookup |
| Embed secrets in callback URLs | URL logging, browser history, referrer leakage | Signed short-lived codes only |
| Hard-code localhost port | Port conflicts across CLI instances | Bind to `127.0.0.1:0`, OS assigns port |
| Check `is_authenticated` with keyring prompt | Interactive keyring dialog during background ops | Try keyring read, suppress prompts in non-login paths |

## Credential Storage Hierarchy

```
1. OS Keyring (macOS Keychain, Linux Secret Service, Windows Credential Manager)
   ↓ (fails silently if unavailable)
2. Encrypted file: ~/.config/<cli>/credentials.json
   • AES-256-GCM with PBKDF2 key derivation
   • Base64url-encoded {salt, nonce, ciphertext}
   ↓ (last resort)
3. Error: inform user, suggest API key as alternative
```

## Checklist: Before You Ship

- [ ] PKCE challenge/verifier generated per-session (never cached)
- [ ] Auth codes expire in <=60 seconds
- [ ] Device codes expire in <=15 minutes
- [ ] All token comparisons are timing-safe
- [ ] Tokens hashed before database storage
- [ ] Concurrent token exchange serialized (advisory locks)
- [ ] Suspended/banned users checked at every exchange point
- [ ] Callback page works when CLI is on a different machine (copy button)
- [ ] `User-Agent: <cli>/<version> (<platform>/<arch>)` on every request
- [ ] Rate limiting on all auth endpoints
- [ ] Token refresh doesn't invalidate concurrent requests (lock + atomic swap)
- [ ] Logout revokes server-side before clearing local credentials
- [ ] Legacy token formats auto-migrated on first use

## References

| Need | Reference |
|------|-----------|
| Full PKCE browser flow | [PKCE-FLOW.md](references/PKCE-FLOW.md) |
| Device code flow (RFC 8628) | [DEVICE-CODE-FLOW.md](references/DEVICE-CODE-FLOW.md) |
| Token lifecycle (mint/refresh/revoke) | [TOKEN-LIFECYCLE.md](references/TOKEN-LIFECYCLE.md) |
| Server-side implementation | [SERVER-IMPLEMENTATION.md](references/SERVER-IMPLEMENTATION.md) |
| CLI-side implementation (Rust) | [CLI-IMPLEMENTATION.md](references/CLI-IMPLEMENTATION.md) |
| Credential storage | [CREDENTIAL-STORAGE.md](references/CREDENTIAL-STORAGE.md) |
| Web UI for device verification | [DEVICE-VERIFY-UI.md](references/DEVICE-VERIFY-UI.md) |
| Database schema | [SCHEMA.md](references/SCHEMA.md) |
| Security hardening | [SECURITY-HARDENING.md](references/SECURITY-HARDENING.md) |
| Protocol design template | [PROTOCOL-TEMPLATE.md](references/PROTOCOL-TEMPLATE.md) |
| Headless/SSH detection | [ENVIRONMENT-DETECTION.md](references/ENVIRONMENT-DETECTION.md) |
| Testing strategies | [TESTING.md](references/TESTING.md) |
| Anti-patterns deep dive | [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) |
| Evolution & lessons learned | [LESSONS-LEARNED.md](references/LESSONS-LEARNED.md) |
