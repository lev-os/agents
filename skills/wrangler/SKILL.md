---
name: wrangler
description: >-
  Deploy and manage Cloudflare Workers, Pages, R2, D1, KV.
  Use when working with wrangler, Cloudflare Workers, or edge deployments.
---

# Using Wrangler

<!-- TOC: Quick Start | THE EXACT PROMPT | Core Commands | Config | Auto-Provisioning | Common Patterns | AGENTS.md Blurb | Gotchas | References -->

> **Version:** 4.59.2+ (Jan 2026). Config format: `wrangler.jsonc` recommended over `.toml`.

## Quick Start

```bash
# Create new project
npx create-cloudflare@latest my-worker

# Local dev
wrangler dev

# Deploy
wrangler deploy

# View logs
wrangler tail
```

## THE EXACT PROMPT — Deploy a Worker

```
Deploy Worker to Cloudflare:
1. Check wrangler.jsonc exists with name, main, compatibility_date
2. wrangler deploy (auto-provisions KV/R2/D1 bindings if IDs missing)
3. wrangler tail to verify
```

## Core Commands

| Task | Command |
|------|---------|
| Local dev | `wrangler dev` |
| Deploy | `wrangler deploy` |
| View logs | `wrangler tail` |
| Add secret | `wrangler secret put NAME` |
| List secrets | `wrangler secret list` |
| Generate types | `wrangler types` |
| Check config | `wrangler check startup` |

## Config (wrangler.jsonc)

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",

  // Routes
  "routes": [
    { "pattern": "example.com/*", "zone_name": "example.com" }
  ],

  // Bindings (IDs optional - auto-provisioned on deploy)
  "kv_namespaces": [{ "binding": "KV", "id": "..." }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  "d1_databases": [{ "binding": "DB", "database_id": "..." }],

  // Environment variables
  "vars": { "ENV": "production" }
}
```

## Auto-Provisioning (v4.57+)

Add bindings WITHOUT IDs — Wrangler creates resources on deploy:

```jsonc
{
  "kv_namespaces": [{ "binding": "CACHE" }],  // No id - auto-created
  "r2_buckets": [{ "binding": "ASSETS" }],    // No bucket_name - auto-created
  "d1_databases": [{ "binding": "DB" }]       // No database_id - auto-created
}
```

## Hidden/Experimental Flags

| Flag | Purpose |
|------|---------|
| `--x-provision` | Force auto-provision resources |
| `--x-auto-create` | Auto-create bindings with new resources |
| `--x-autoconfig` | Auto-detect framework (Next.js, Remix, etc.) |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLOUDFLARE_API_TOKEN` | Auth for CI/CD |
| `CLOUDFLARE_ACCOUNT_ID` | Override account |

## Decision Tree

```
What to do?
├─ New project → npx create-cloudflare@latest
├─ Local dev → wrangler dev
├─ Deploy → wrangler deploy
├─ Add secret → wrangler secret put NAME
├─ View logs → wrangler tail
├─ Database ops → wrangler d1 ...
├─ Storage ops → wrangler r2 ... or wrangler kv ...
└─ Scheduled jobs → Add [triggers] to config
```

## Common Patterns

### Add a Secret
```bash
wrangler secret put API_KEY
# Enter value when prompted (or pipe: echo "value" | wrangler secret put API_KEY)
```

### Multiple Environments
```jsonc
{
  "name": "my-worker",
  "env": {
    "staging": {
      "vars": { "ENV": "staging" },
      "routes": [{ "pattern": "staging.example.com/*" }]
    },
    "production": {
      "vars": { "ENV": "production" },
      "routes": [{ "pattern": "example.com/*" }]
    }
  }
}
```

```bash
wrangler deploy --env staging
wrangler deploy --env production
```

### D1 Database
```bash
wrangler d1 create my-db
wrangler d1 execute my-db --file schema.sql
wrangler d1 execute my-db --command "SELECT * FROM users"
```

### R2 Storage
```bash
wrangler r2 bucket create my-bucket
wrangler r2 object put my-bucket/file.txt --file ./local.txt
wrangler r2 object get my-bucket/file.txt
```

---

## AGENTS.md Blurb

Copy this to your project's AGENTS.md:

```markdown
### Cloudflare Wrangler

Wrangler is installed and authenticated.

R2 bucket: `<BUCKET_NAME>`
Account ID: `<ACCOUNT_ID>`

Common commands:

\`\`\`bash
wrangler r2 object put <BUCKET>/<path> --file ./local-file
wrangler r2 object get <BUCKET>/<path> --file ./downloaded
wrangler r2 bucket list
wrangler d1 execute <DB> --command "SELECT * FROM users"
wrangler deploy
\`\`\`
```

---

## Reference Index

| Topic | Reference |
|-------|-----------|
| All commands | [COMMANDS.md](references/COMMANDS.md) |
| Config options | [CONFIG.md](references/CONFIG.md) |
| Pages deployment | [PAGES.md](references/PAGES.md) |

## Gotchas

- **Dashboard changes overwritten:** Add `"keep_vars": true` to preserve dashboard edits
- **Secrets not in config:** Use `wrangler secret put`, never put secrets in config
- **Types outdated:** Run `wrangler types` after config changes
- **Old compatibility_date:** Update yearly for new features

## Sources

- Repo: cloudflare/workers-sdk @ v4.59.2
- Docs: [developers.cloudflare.com/workers/wrangler](https://developers.cloudflare.com/workers/wrangler/)
