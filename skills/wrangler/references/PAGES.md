# Cloudflare Pages with Wrangler

Deploy static sites and full-stack apps with Pages Functions.

---

## Quick Start

```bash
# Deploy static site
wrangler pages deploy ./dist

# Local dev with functions
wrangler pages dev ./dist

# Create project
wrangler pages project create my-site
```

---

## Static Site Deployment

```bash
# Build your site first
npm run build

# Deploy (creates project on first run)
wrangler pages deploy ./dist --project-name my-site
```

---

## Pages Functions

Functions live in `functions/` directory:

```
my-site/
├── functions/
│   ├── api/
│   │   └── hello.ts        # /api/hello
│   ├── [[path]].ts         # Catch-all
│   └── _middleware.ts      # Middleware
├── public/                  # Static assets
└── wrangler.jsonc
```

### Example Function

```typescript
// functions/api/hello.ts
export async function onRequest(context) {
  return new Response(JSON.stringify({ message: "Hello!" }), {
    headers: { "Content-Type": "application/json" }
  });
}

// Or with methods
export async function onRequestGet(context) {
  return new Response("GET request");
}

export async function onRequestPost(context) {
  const body = await context.request.json();
  return new Response(JSON.stringify(body));
}
```

### Middleware

```typescript
// functions/_middleware.ts
export async function onRequest(context) {
  // Run before all functions
  const response = await context.next();
  response.headers.set("X-Custom-Header", "value");
  return response;
}
```

---

## Config for Pages

```jsonc
{
  "name": "my-site",
  "pages_build_output_dir": "./dist",

  // Bindings available to functions
  "kv_namespaces": [{ "binding": "CACHE" }],
  "d1_databases": [{ "binding": "DB" }],
  "r2_buckets": [{ "binding": "ASSETS" }],

  "vars": {
    "ENVIRONMENT": "production"
  }
}
```

---

## Local Development

```bash
# Basic
wrangler pages dev ./dist

# With bindings
wrangler pages dev ./dist --kv CACHE --d1 DB

# Custom port
wrangler pages dev ./dist --port 3000

# With live reload
wrangler pages dev ./dist --live-reload
```

---

## Secrets

```bash
# Add secret
wrangler pages secret put API_KEY --project-name my-site

# List secrets
wrangler pages secret list --project-name my-site

# Bulk upload
wrangler pages secret bulk ./secrets.json --project-name my-site
```

---

## Environments

Pages has built-in preview/production environments:

```bash
# Deploy to production
wrangler pages deploy ./dist --project-name my-site

# Deploy to preview (branch deploy)
wrangler pages deploy ./dist --project-name my-site --branch feature-x

# Set branch-specific secrets
wrangler pages secret put API_KEY --project-name my-site --env preview
```

---

## Build Commands

```bash
# Build functions only
wrangler pages functions build --outdir ./functions-dist

# Optimize routes
wrangler pages functions optimize-routes --output ./optimized
```

---

## Framework Integration

### Next.js

```bash
# Use @cloudflare/next-on-pages
npx @cloudflare/next-on-pages

# Deploy
wrangler pages deploy .vercel/output/static
```

### Remix / Nuxt / SvelteKit

Use framework's Cloudflare adapter, then:

```bash
npm run build
wrangler pages deploy ./dist
```

### Auto-Detection (v4.57+)

```bash
# Wrangler auto-detects framework
wrangler pages deploy --x-autoconfig
```

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `wrangler pages dev DIR` | Local dev server |
| `wrangler pages deploy DIR` | Deploy to Pages |
| `wrangler pages project list` | List projects |
| `wrangler pages project create NAME` | Create project |
| `wrangler pages deployment list --project-name NAME` | List deployments |
| `wrangler pages deployment tail --project-name NAME` | Tail logs |
| `wrangler pages secret put NAME --project-name NAME` | Add secret |
| `wrangler pages download --project-name NAME` | Download deployment |

---

## Gotchas

- **Functions must export named handlers:** `onRequest`, `onRequestGet`, etc.
- **Middleware order:** `_middleware.ts` runs for all routes in that directory and below
- **Asset binding:** Use `context.env.ASSETS.fetch()` to serve static files from functions
- **Preview vs Production:** Branch deploys go to preview, main goes to production
- **Build output:** Framework builds to different directories (Next: `.vercel/output`, Remix: `build/`, etc.)
