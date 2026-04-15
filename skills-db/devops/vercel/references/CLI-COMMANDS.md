# CLI Commands Reference

> Complete command reference for Vercel, Supabase, and Wrangler CLIs.

---

## Table of Contents

- [Authentication](#authentication)
- [Vercel CLI](#vercel-cli)
- [Supabase CLI](#supabase-cli)
- [Wrangler CLI](#wrangler-cli)

---

## Authentication

All CLIs support non-interactive auth via environment variables:

```bash
# Vercel
export VERCEL_TOKEN=xxx  # From https://vercel.com/account/tokens

# Cloudflare
export CLOUDFLARE_API_TOKEN=xxx  # From dashboard profile

# Supabase
export SUPABASE_ACCESS_TOKEN=xxx  # From dashboard settings
```

**Rule:** Always use `--token $VERCEL_TOKEN` in scripts for explicit auth.

---

## Vercel CLI

### Installation

```bash
npm i -g vercel
# or
pnpm add -g vercel
```

### Project Management

```bash
# Link current directory to Vercel project
vercel link

# Pull project settings and env vars locally
vercel pull --yes
vercel pull --yes --environment=production

# List projects
vercel project ls

# Inspect current project
vercel inspect
```

### Deployment

```bash
# Deploy preview
vercel

# Deploy production
vercel --prod

# Build locally (for prebuilt flow)
vercel build
vercel build --prod

# Deploy prebuilt artifacts
vercel deploy --prebuilt
vercel deploy --prebuilt --prod
vercel deploy --prebuilt --prod --archive=tgz

# List deployments
vercel ls

# Get deployment info
vercel inspect <deployment-url>

# Promote preview to production
vercel promote <deployment-url>

# Rollback
vercel rollback <deployment-url>
```

### Environment Variables

```bash
# List all env vars
vercel env ls

# Add env var (interactive)
vercel env add SECRET_NAME

# Add env var with target
vercel env add SECRET_NAME production
vercel env add SECRET_NAME preview
vercel env add SECRET_NAME development

# Pull env vars to local file
vercel env pull
vercel env pull .env.local
vercel env pull .env.production --environment=production

# Remove env var
vercel env rm SECRET_NAME production
```

### Domains

```bash
# List domains
vercel domains ls

# Add domain
vercel domains add example.com

# Remove domain
vercel domains rm example.com

# Inspect domain
vercel domains inspect example.com
```

### Secrets (Legacy)

```bash
# Note: Prefer env vars. Secrets are older.
vercel secrets add my-secret value
vercel secrets ls
vercel secrets rm my-secret
```

### Logs & Debugging

```bash
# View build logs
vercel logs <deployment-url>

# View runtime logs (streaming)
vercel logs <deployment-url> --follow

# Dev server (local)
vercel dev
```

### Global Options

| Flag | Purpose |
|------|---------|
| `--token TOKEN` | Use specific auth token |
| `--scope TEAM` | Use specific team scope |
| `--yes` / `-y` | Skip confirmation prompts |
| `--prod` | Target production |
| `--debug` | Verbose output |

---

## Supabase CLI

### Installation

```bash
npm i -g supabase
# or
brew install supabase/tap/supabase
```

### Project Management

```bash
# Login
supabase login

# Link to remote project
supabase link --project-ref <ref>

# Start local dev stack
supabase start

# Stop local stack
supabase stop

# Status
supabase status
```

### Migrations

```bash
# Create new migration
supabase migration new <name>

# List migrations
supabase migration list

# Apply migrations locally
supabase migration up

# Push migrations to remote (CI/CD)
supabase db push

# Pull remote schema to local
supabase db pull

# Diff local vs remote
supabase db diff
```

### Types

```bash
# Generate TypeScript types from schema
supabase gen types typescript --local > types/supabase.ts

# From remote
supabase gen types typescript --linked > types/supabase.ts

# With specific schema
supabase gen types typescript --local --schema public,auth
```

### Database

```bash
# Reset local database
supabase db reset

# Run SQL file
supabase db execute -f script.sql

# Dump schema
supabase db dump -f schema.sql

# Dump data
supabase db dump -f data.sql --data-only
```

### Functions (Edge Functions)

```bash
# Create function
supabase functions new my-function

# Serve locally
supabase functions serve

# Deploy
supabase functions deploy my-function

# Deploy all
supabase functions deploy
```

---

## Wrangler CLI

### Installation

```bash
npm i -g wrangler
# or
pnpm add -g wrangler
```

### Project Management

```bash
# Login (interactive)
wrangler login

# Logout
wrangler logout

# Who am I
wrangler whoami
```

### Workers

```bash
# Create new project
npx create-cloudflare@latest my-worker

# Local dev
wrangler dev

# Deploy
wrangler deploy

# Delete
wrangler delete

# View logs
wrangler tail

# Check config
wrangler check startup
```

### R2 Storage

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# List buckets
wrangler r2 bucket list

# Delete bucket
wrangler r2 bucket delete my-bucket

# Upload object
wrangler r2 object put my-bucket/path/file.txt --file ./local.txt

# Download object
wrangler r2 object get my-bucket/path/file.txt

# Delete object
wrangler r2 object delete my-bucket/path/file.txt

# List objects
wrangler r2 object list my-bucket
```

### D1 Database

```bash
# Create database
wrangler d1 create my-db

# List databases
wrangler d1 list

# Execute SQL
wrangler d1 execute my-db --command "SELECT * FROM users"

# Execute SQL file
wrangler d1 execute my-db --file schema.sql

# Export database
wrangler d1 export my-db --output dump.sql
```

### KV Storage

```bash
# Create namespace
wrangler kv namespace create MY_KV

# List namespaces
wrangler kv namespace list

# Put value
wrangler kv key put --namespace-id=xxx KEY "value"

# Get value
wrangler kv key get --namespace-id=xxx KEY

# Delete key
wrangler kv key delete --namespace-id=xxx KEY

# List keys
wrangler kv key list --namespace-id=xxx
```

### Secrets

```bash
# Add secret (interactive)
wrangler secret put SECRET_NAME

# Add secret (pipe)
echo "value" | wrangler secret put SECRET_NAME

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete SECRET_NAME
```

### Pages (Direct Upload)

```bash
# Deploy to Pages (Direct Upload)
wrangler pages deploy ./dist

# Deploy to specific branch
wrangler pages deploy ./dist --branch=main
wrangler pages deploy ./dist --branch=staging

# List deployments
wrangler pages deployment list

# Create project
wrangler pages project create my-project
```

### Types

```bash
# Generate types from bindings
wrangler types
```

---

## Quick Copy-Paste

### Vercel Manual Deploy

```bash
vercel pull --yes && vercel build --prod && vercel deploy --prebuilt --prod --token $VERCEL_TOKEN
```

### Supabase Migration Flow

```bash
supabase migration new add_feature && supabase migration up && supabase gen types typescript --local > types/supabase.ts
```

### Wrangler Full Deploy

```bash
wrangler deploy && wrangler tail
```

### Pages Direct Upload

```bash
pnpm build && wrangler pages deploy ./dist --branch=main
```
