# Cloudflare Cost Offload

> **TL;DR:** Move marketing to Pages, uploads to R2. Keep Vercel thin — only authenticated app traffic.

---

## Table of Contents

- [Why Offload](#why-offload)
- [Cloudflare Pages for Marketing](#cloudflare-pages-for-marketing)
- [R2 for Uploads/Assets](#r2-for-uploadsassets)
- [Caching Strategy](#caching-strategy)
- [Worker Patterns](#worker-patterns)

---

## Why Offload

### Cost Comparison

| Traffic Type | On Vercel | On Cloudflare |
|--------------|-----------|---------------|
| Marketing HTML | Bandwidth charges | Free (Pages) |
| User uploads | Function + bandwidth | R2 ops only (no egress) |
| Static assets | CDN bandwidth | Free (Pages/R2) |
| API calls | Function invocations | Worker invocations |

### The Math

If your marketing page gets 100k visits/month and your app gets 5k authenticated users:
- **Without offload:** 105k requests hit Vercel
- **With offload:** 5k requests hit Vercel (95% reduction)

---

## Cloudflare Pages for Marketing

### Why Pages Instead of Vercel

- Free generous tier (unlimited bandwidth)
- Global CDN by default
- Direct Upload = deploy control (no auto-builds)

### Static Export (Recommended)

```javascript
// next.config.js (for static marketing site)
module.exports = {
  output: 'export',
  images: { unoptimized: true }
}
```

### Direct Upload Deploy

```bash
# Build
pnpm -C apps/marketing build

# Deploy to production
npx wrangler pages deploy apps/marketing/out --branch=main

# Deploy preview
npx wrangler pages deploy apps/marketing/out --branch=staging
```

**Why Direct Upload:** No Git integration = no accidental builds. You control when deploys happen.

### Redirects to App

Create `_redirects` in your output folder:

```
# _redirects
/login       https://app.example.com/login      302
/dashboard   https://app.example.com/dashboard  302
/app/*       https://app.example.com/app/:splat 302
```

Users can visit `www.example.com/login` and get redirected to your Vercel app.

### Custom Headers

Create `_headers` in your output folder:

```
# _headers
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Cache-Control: public, max-age=0, s-maxage=3600, stale-while-revalidate=86400

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.js
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable
```

---

## R2 for Uploads/Assets

### Why R2

- **No egress fees** — You pay for storage and operations, not bandwidth
- **S3-compatible** — Works with existing S3 tools/libraries
- **Worker bindings** — Fast path from Workers

### Create Bucket

```bash
wrangler r2 bucket create user-uploads
wrangler r2 bucket create static-assets
```

### Upload Worker Pattern

Create a Worker that handles uploads and generates signed URLs:

```typescript
// workers/upload/src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Generate presigned upload URL
    if (url.pathname === '/upload' && request.method === 'POST') {
      const { filename, contentType } = await request.json();
      const key = `uploads/${crypto.randomUUID()}/${filename}`;

      // Generate signed URL (valid 15 min)
      const signedUrl = await env.UPLOADS.createSignedUrl(key, {
        method: 'PUT',
        expiresIn: 900,
        headers: { 'Content-Type': contentType }
      });

      return Response.json({ uploadUrl: signedUrl, key });
    }

    // Serve files
    if (url.pathname.startsWith('/files/')) {
      const key = url.pathname.replace('/files/', '');
      const object = await env.UPLOADS.get(key);

      if (!object) {
        return new Response('Not Found', { status: 404 });
      }

      return new Response(object.body, {
        headers: {
          'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
          'Cache-Control': 'public, max-age=31536000, immutable'
        }
      });
    }

    return new Response('Not Found', { status: 404 });
  }
};

interface Env {
  UPLOADS: R2Bucket;
}
```

### wrangler.jsonc

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

### Client Upload Flow

```typescript
// In your Next.js app
async function uploadFile(file: File) {
  // 1. Get signed URL from Worker
  const res = await fetch('https://assets.example.com/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type
    })
  });
  const { uploadUrl, key } = await res.json();

  // 2. Upload directly to R2 (bypasses your app entirely)
  await fetch(uploadUrl, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': file.type }
  });

  // 3. Store key in your database
  return key;  // e.g., "uploads/uuid/filename.jpg"
}
```

**Result:** File uploads never touch Vercel. Zero bandwidth cost.

---

## Caching Strategy

### Safe Caching Rules

| Content | Cache-Control | Why |
|---------|---------------|-----|
| HTML (public) | `s-maxage=3600, stale-while-revalidate=86400` | Fresh hourly, stale OK |
| JS/CSS bundles | `max-age=31536000, immutable` | Fingerprinted, cache forever |
| Images | `max-age=31536000, immutable` | Usually fingerprinted |
| API responses | `no-store` or `private` | Never cache auth content |
| User uploads | `max-age=31536000, immutable` | UUID keys = immutable |

### Cloudflare-Specific Headers

```
# CDN-Cache-Control: Control CDN separately from browser
CDN-Cache-Control: max-age=3600

# Cloudflare-CDN-Cache-Control: Cloudflare-specific
Cloudflare-CDN-Cache-Control: max-age=86400
```

### Never Cache These

- Responses that vary by auth/cookies
- User-specific content
- API endpoints returning personalized data

---

## Worker Patterns

### Auth Middleware

```typescript
async function authenticate(request: Request, env: Env): Promise<string | null> {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token) return null;

  // Verify JWT / check session
  try {
    const payload = await verifyToken(token, env.JWT_SECRET);
    return payload.userId;
  } catch {
    return null;
  }
}
```

### Signed URL Generation

```typescript
function generateSignedUrl(key: string, secret: string, expiresIn: number): string {
  const expires = Math.floor(Date.now() / 1000) + expiresIn;
  const signature = hmacSha256(`${key}:${expires}`, secret);
  return `https://assets.example.com/files/${key}?expires=${expires}&sig=${signature}`;
}
```

### Rate Limiting

```typescript
async function rateLimit(request: Request, env: Env): Promise<boolean> {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `ratelimit:${ip}`;

  const count = await env.KV.get(key);
  if (count && parseInt(count) > 100) {
    return false;  // Rate limited
  }

  await env.KV.put(key, String((parseInt(count || '0') + 1)), { expirationTtl: 60 });
  return true;
}
```

---

## Deployment Workflow

### Two-Button Deploy

```bash
# Marketing (Cloudflare Pages)
pnpm -C apps/marketing build && wrangler pages deploy apps/marketing/out --branch=main

# Assets Worker (Cloudflare Workers)
wrangler deploy -c workers/assets/wrangler.jsonc

# App (Vercel)
vercel pull --yes && vercel build --prod && vercel deploy --prebuilt --prod
```

### DNS Configuration

```
# Cloudflare DNS
www.example.com     CNAME   project.pages.dev      (proxied)
assets.example.com  CNAME   assets-worker.workers.dev  (proxied)
app.example.com     CNAME   cname.vercel-dns.com   (DNS-only)
```
