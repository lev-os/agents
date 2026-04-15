# Architecture & Cost Model

> **TL;DR:** Vercel for SSR/RSC compute, Cloudflare for static/storage. Never reverse-proxy Vercel.

---

## Table of Contents

- [The Three-Way Split](#the-three-way-split)
- [Why Hostname Splitting](#why-hostname-splitting)
- [Cost Model](#cost-model)
- [Domain Configuration](#domain-configuration)
- [Recommended Setup](#recommended-setup)

---

## The Three-Way Split

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TRAFFIC ROUTING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   www.example.com ──► Cloudflare Pages                              │
│   │  Marketing, docs, changelog, pricing                            │
│   │  Static, cacheable, cheap bandwidth                             │
│   │  Deploy: wrangler pages deploy                                  │
│                                                                     │
│   app.example.com ──► Vercel (DNS-only in Cloudflare)              │
│   │  Authenticated SaaS app                                         │
│   │  SSR/RSC, route handlers, dynamic content                       │
│   │  Deploy: vercel --prod (manual/CI)                              │
│                                                                     │
│   assets.example.com ──► Cloudflare R2 + Worker                     │
│      User uploads, downloads, media                                 │
│      No egress fees, signed URLs                                    │
│      Deploy: wrangler deploy                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Why Hostname Splitting

**Two constraints that force this architecture:**

1. **Cloudflare Cache Rules require proxying** — You must "orange cloud" (proxy) a hostname to use Cloudflare caching, WAF, bot mitigation.

2. **Vercel does NOT recommend reverse proxying** — Putting Cloudflare as a proxy in front of Vercel causes:
   - Cache coherence issues
   - Reduced traffic visibility for Vercel
   - Latency overhead
   - Potential mitigation system conflicts

**Solution:** Split by hostname, not by path.

| Hostname | Cloudflare Mode | Why |
|----------|-----------------|-----|
| `app.example.com` | DNS-only (gray cloud) | Vercel serves directly |
| `www.example.com` | Proxied (orange cloud) | Cloudflare Pages |
| `assets.example.com` | Proxied (orange cloud) | R2 + Worker |

## Cost Model

### What You Pay For

| Service | You Pay For | Strategy |
|---------|-------------|----------|
| **Vercel** | Build minutes, function invocations, bandwidth | Reduce builds, offload static |
| **Cloudflare Pages** | Nothing (generous free tier) | Use for marketing |
| **Cloudflare R2** | Storage + Class A/B ops (NO egress) | Use for all user files |
| **Supabase** | DB size, function invocations | Standard optimization |

### Where Money Leaks

1. **Accidental builds** — Every push triggers preview deployment
2. **Bandwidth through Vercel** — User uploads/downloads transit your app
3. **Marketing traffic** — Homepage/pricing views burn Vercel bandwidth

### Cost Optimization Levers

| Lever | Impact | Implementation |
|-------|--------|----------------|
| Disable auto-deploys | ★★★★★ | `"git": { "deploymentEnabled": false }` |
| Prebuilt deploys | ★★★★☆ | `vercel build && vercel deploy --prebuilt` |
| R2 for uploads | ★★★★☆ | Client → Worker → R2 (bypasses Vercel) |
| Pages for marketing | ★★★☆☆ | Static export, Direct Upload |
| Fewer preview deploys | ★★☆☆☆ | Ignored Build Step (but still counts) |

## Domain Configuration

### Cloudflare DNS Records

```
# For Vercel (DNS-only, gray cloud)
app.example.com    CNAME   cname.vercel-dns.com   (proxy: OFF)

# For Cloudflare Pages (proxied, orange cloud)
www.example.com    CNAME   your-project.pages.dev (proxy: ON)

# For R2/Workers (proxied, orange cloud)
assets.example.com CNAME   your-worker.workers.dev (proxy: ON)
```

### Vercel Domain Setup

```bash
# Add domain
vercel domains add app.example.com

# List domains
vercel domains ls

# Remove domain
vercel domains rm app.example.com
```

## Recommended Setup

### Repo Structure

```
/
├── apps/
│   ├── web/              # Next.js 16 app → Vercel
│   └── marketing/        # Static site → Cloudflare Pages
├── packages/             # Shared code
├── workers/
│   └── assets/           # R2 upload/signing Worker
├── supabase/             # Migrations, seed, config
├── infra/                # Automation scripts
├── vercel.json           # Vercel config-as-code
└── wrangler.jsonc        # Worker config
```

### vercel.json (Minimal Cost-Optimized)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "git": {
    "deploymentEnabled": false
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

### wrangler.jsonc (Assets Worker)

```jsonc
{
  "name": "assets-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "r2_buckets": [
    { "binding": "UPLOADS", "bucket_name": "user-uploads" }
  ],
  "routes": [
    { "pattern": "assets.example.com/*", "zone_name": "example.com" }
  ]
}
```

## Path-Based Routing (If You Must)

If you absolutely need single-domain routing (`example.com/app/*` + `example.com/*`):

1. You'll reverse-proxy Vercel behind Cloudflare (not recommended)
2. Never cache `/app/*` responses at Cloudflare
3. Consider Vercel's Verified Proxy guidance for IP trust
4. Expect operational complexity

**Recommendation:** Just use the hostname split. It's cleaner.
