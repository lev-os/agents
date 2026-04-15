# Automation Blueprint

> **TL;DR:** Idempotent state discovery → converge desired state → deploy manually.

---

## Table of Contents

- [Philosophy](#philosophy)
- [State Discovery](#state-discovery)
- [Environment Sync](#environment-sync)
- [Deploy Automation](#deploy-automation)
- [Full Pipeline](#full-pipeline)

---

## Philosophy

### Agent-Friendly Principles

1. **Idempotent operations** — Running twice = same result
2. **State discovery first** — Read before write
3. **Converge, don't replace** — Upsert, don't delete-then-create
4. **CLI + REST hybrid** — CLI for simple ops, REST for bulk
5. **Token-based auth** — No interactive prompts

### What Agents Should Do First

```bash
# 1. Discover current state
vercel project ls --token $VERCEL_TOKEN
vercel env ls --token $VERCEL_TOKEN
supabase projects list
wrangler r2 bucket list

# 2. Read local state
cat .vercel/project.json 2>/dev/null || echo "Not linked"
cat vercel.json 2>/dev/null || echo "No config"
```

---

## State Discovery

### Vercel Project State

```bash
# Check if linked
if [ -f .vercel/project.json ]; then
  PROJECT_ID=$(jq -r '.projectId' .vercel/project.json)
  ORG_ID=$(jq -r '.orgId' .vercel/project.json)
  echo "Linked: $PROJECT_ID (org: $ORG_ID)"
else
  echo "Not linked - run: vercel link"
fi

# Get project info via API
curl -s "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN" | jq '.name, .framework'
```

### Environment Variables State

```bash
# List all env vars
curl -s "https://api.vercel.com/v10/projects/$PROJECT_ID/env" \
  -H "Authorization: Bearer $VERCEL_TOKEN" | jq '.envs[] | {key, target, gitBranch}'
```

### Supabase State

```bash
# Check if linked
if [ -f supabase/.temp/project-ref ]; then
  echo "Linked to: $(cat supabase/.temp/project-ref)"
else
  echo "Not linked - run: supabase link --project-ref xxx"
fi

# List migrations
supabase migration list
```

### Cloudflare State

```bash
# Workers
wrangler whoami
wrangler deployments list

# R2
wrangler r2 bucket list

# Pages
wrangler pages project list
```

---

## Environment Sync

### Vault → Vercel (Bulk Sync)

```bash
#!/bin/bash
# sync-env-from-vault.sh

set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Required}"
VERCEL_TOKEN="${VERCEL_TOKEN:?Required}"
VAULT_PATH="${VAULT_PATH:-secret/data/prod}"

# Read all secrets from Vault
SECRETS=$(vault kv get -format=json "$VAULT_PATH" | jq -r '.data.data | to_entries[]')

# Sync each to Vercel
echo "$SECRETS" | while IFS= read -r entry; do
  key=$(echo "$entry" | jq -r '.key')
  value=$(echo "$entry" | jq -r '.value')

  echo "Syncing: $key"

  curl -s -X POST "https://api.vercel.com/v10/projects/$PROJECT_ID/env?upsert=true" \
    -H "Authorization: Bearer $VERCEL_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"key\":\"$key\",\"value\":\"$value\",\"target\":[\"production\"],\"type\":\"encrypted\"}" \
    | jq '.created // .updated'
done
```

### JSON Config → Vercel

```bash
#!/bin/bash
# sync-env-from-json.sh

CONFIG_FILE="${1:?Usage: $0 config.json}"
PROJECT_ID="${PROJECT_ID:?Required}"
VERCEL_TOKEN="${VERCEL_TOKEN:?Required}"

jq -c '.[]' "$CONFIG_FILE" | while IFS= read -r var; do
  curl -s -X POST "https://api.vercel.com/v10/projects/$PROJECT_ID/env?upsert=true" \
    -H "Authorization: Bearer $VERCEL_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$var"
done
```

Config file format:

```json
[
  { "key": "DATABASE_URL", "value": "postgres://...", "target": ["production"], "type": "encrypted" },
  { "key": "API_KEY", "value": "xxx", "target": ["production", "preview"], "type": "sensitive" }
]
```

### Diff Before Sync

```bash
#!/bin/bash
# diff-env.sh

PROJECT_ID="${PROJECT_ID:?Required}"
VERCEL_TOKEN="${VERCEL_TOKEN:?Required}"
DESIRED_FILE="${1:?Usage: $0 desired.json}"

# Get current state
CURRENT=$(curl -s "https://api.vercel.com/v10/projects/$PROJECT_ID/env" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  | jq '[.envs[] | {key, target}]' | sort)

# Get desired state
DESIRED=$(jq '[.[] | {key, target}]' "$DESIRED_FILE" | sort)

# Diff
diff <(echo "$CURRENT") <(echo "$DESIRED") || echo "Differences found"
```

---

## Deploy Automation

### Prebuilt Deploy Script

```bash
#!/bin/bash
# deploy.sh

set -euo pipefail

ENV="${1:-preview}"
VERCEL_TOKEN="${VERCEL_TOKEN:?Required}"

echo "Deploying to: $ENV"

# 1. Pull latest settings
vercel pull --yes --environment="$ENV" --token "$VERCEL_TOKEN"

# 2. Build
if [ "$ENV" = "production" ]; then
  vercel build --prod
else
  vercel build
fi

# 3. Deploy
if [ "$ENV" = "production" ]; then
  vercel deploy --prebuilt --prod --token "$VERCEL_TOKEN"
else
  vercel deploy --prebuilt --token "$VERCEL_TOKEN"
fi

echo "Deploy complete"
```

### Deploy with Rollback Safety

```bash
#!/bin/bash
# safe-deploy.sh

set -euo pipefail

VERCEL_TOKEN="${VERCEL_TOKEN:?Required}"

# Get current production deployment
CURRENT_PROD=$(vercel ls --prod --token "$VERCEL_TOKEN" | head -1 | awk '{print $2}')
echo "Current production: $CURRENT_PROD"

# Deploy
NEW_DEPLOY=$(vercel deploy --prebuilt --prod --token "$VERCEL_TOKEN" 2>&1 | tail -1)
echo "New deployment: $NEW_DEPLOY"

# Health check
if ! curl -sf "$NEW_DEPLOY/api/health" > /dev/null; then
  echo "Health check failed, rolling back..."
  vercel rollback "$CURRENT_PROD" --token "$VERCEL_TOKEN"
  exit 1
fi

echo "Deployment healthy"
```

---

## Full Pipeline

### GitHub Actions Workflow

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      target:
        description: 'Deploy target'
        required: true
        default: 'preview'
        type: choice
        options: [preview, production]

env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}

jobs:
  deploy-marketing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Marketing
        run: pnpm -C apps/marketing build

      - name: Deploy to Pages
        run: npx wrangler pages deploy apps/marketing/out --branch=${{ inputs.target == 'production' && 'main' || 'staging' }}

  deploy-app:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Dependencies
        run: pnpm install

      - name: Pull Vercel Config
        run: vercel pull --yes --environment=${{ inputs.target }} --token=$VERCEL_TOKEN

      - name: Build
        run: vercel build ${{ inputs.target == 'production' && '--prod' || '' }}

      - name: Deploy
        run: vercel deploy --prebuilt ${{ inputs.target == 'production' && '--prod' || '' }} --token=$VERCEL_TOKEN

  deploy-workers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy Assets Worker
        run: npx wrangler deploy -c workers/assets/wrangler.jsonc

  run-migrations:
    runs-on: ubuntu-latest
    if: inputs.target == 'production'
    needs: [deploy-app]
    steps:
      - uses: actions/checkout@v4

      - name: Run Migrations
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

### Makefile Alternative

```makefile
.PHONY: deploy-preview deploy-prod sync-env

VERCEL_TOKEN ?= $(error VERCEL_TOKEN required)

deploy-preview:
	vercel pull --yes --token $(VERCEL_TOKEN)
	vercel build
	vercel deploy --prebuilt --token $(VERCEL_TOKEN)

deploy-prod:
	vercel pull --yes --environment=production --token $(VERCEL_TOKEN)
	vercel build --prod
	vercel deploy --prebuilt --prod --token $(VERCEL_TOKEN)

deploy-marketing:
	pnpm -C apps/marketing build
	npx wrangler pages deploy apps/marketing/out --branch=main

deploy-workers:
	npx wrangler deploy -c workers/assets/wrangler.jsonc

deploy-all: deploy-marketing deploy-workers deploy-prod

sync-env:
	./scripts/sync-env-from-vault.sh
```

### CLI Wrapper Script

```bash
#!/bin/bash
# ops.sh - Single entry point for all operations

set -euo pipefail

CMD="${1:-help}"

case "$CMD" in
  status)
    echo "=== Vercel ==="
    vercel ls --token "$VERCEL_TOKEN" | head -5
    echo ""
    echo "=== Supabase ==="
    supabase migration list 2>/dev/null || echo "Not linked"
    echo ""
    echo "=== Cloudflare ==="
    wrangler deployments list 2>/dev/null | head -5 || echo "No deployments"
    ;;

  deploy)
    ENV="${2:-preview}"
    ./scripts/deploy.sh "$ENV"
    ;;

  sync-env)
    ./scripts/sync-env-from-vault.sh
    ;;

  migrate)
    supabase db push
    supabase gen types typescript --linked > types/supabase.ts
    ;;

  *)
    echo "Usage: $0 {status|deploy [env]|sync-env|migrate}"
    ;;
esac
```

---

## Quick Reference

```bash
# State discovery
vercel ls --token $VERCEL_TOKEN
vercel env ls --token $VERCEL_TOKEN

# Deploy preview
vercel pull --yes && vercel build && vercel deploy --prebuilt

# Deploy production
vercel pull --yes --environment=production && vercel build --prod && vercel deploy --prebuilt --prod

# Sync env vars (bulk)
curl -X POST "https://api.vercel.com/v10/projects/$PROJECT_ID/env?upsert=true" ...

# Marketing deploy
wrangler pages deploy ./dist --branch=main
```
