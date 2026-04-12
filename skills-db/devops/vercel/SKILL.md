---
name: vercel
description: >-
  Operate Next.js 16 SaaS on Vercel with Cloudflare DNS + Supabase. Use when
  deploying to Vercel, reducing build costs, managing secrets, or splitting
  traffic between Vercel and Cloudflare.
---

# Vercel for SaaS

> **Core Insight:** Optimize three axes: operational control (CLI-first), cost control (avoid accidental builds), correctness (caching + auth without breaking SSR).

## Table of Contents

- [THE EXACT PROMPT](#the-exact-prompt)
- [Architecture Decision](#architecture-decision)
- [Quick Start](#quick-start-manual-deploy)
- [Stop Build Credit Burn](#stop-build-credit-burn)
- [Environment Variables](#environment-variables)
- [Workflow Checklist](#workflow-checklist)
- [Critical Gotchas](#critical-gotchas)
- [Core Commands](#core-commands)
- [AGENTS.md Blurb](#agentsmd-blurb)
- [References](#references)

---

## THE EXACT PROMPT

```
Set up [Next.js app / SaaS] on Vercel with:
1. Cloudflare DNS at: [domain.com]
2. Supabase project: [project-ref]
3. Build control: [manual deploys only / CI-triggered / default]
4. Cost offload: [R2 for assets / Cloudflare Pages for marketing / none]

Follow vercel-for-saas skill patterns.
```

## Architecture Decision

```
Where should traffic go?
│
├─ Authenticated app (SSR/RSC) ─────► Vercel (app.example.com)
│  • DNS-only in Cloudflare (no proxy)
│  • Manual deploys, prebuilt artifacts
│
├─ Marketing/docs (static) ─────────► Cloudflare Pages (www.example.com)
│  • Direct Upload for deploy control
│  • Aggressive caching, cheap bandwidth
│
└─ Uploads/assets (storage) ────────► Cloudflare R2 (assets.example.com)
   • Worker-signed URLs
   • No egress fees
```

**Why this split:** Vercel does NOT recommend reverse-proxying. Hostname splitting gets Cloudflare benefits without breaking Vercel's edge.

## Quick Start: Manual Deploy

```bash
# 1. Pull settings + env (creates .vercel/)
vercel pull --yes --token $VERCEL_TOKEN

# 2. Build locally (skips Vercel build minutes)
vercel build --prod

# 3. Upload prebuilt artifact
vercel deploy --prebuilt --prod --token $VERCEL_TOKEN
```

This is the **highest-leverage** pattern for cost control.

## Stop Build Credit Burn

| Method | How | Effectiveness |
|--------|-----|---------------|
| **Disable auto-deploys** | `vercel.json`: `"git": { "deploymentEnabled": false }` | ★★★★★ |
| **Prebuilt workflow** | Build outside Vercel, upload with `--prebuilt` | ★★★★☆ |
| Ignored Build Step | Exit 0 = skip, Exit 1 = build (commonly reversed!) | ★★☆☆☆ |
| Deploy Hooks | HTTP-triggered deploys only | ★★★☆☆ |

**Config-as-code (recommended):**

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "git": { "deploymentEnabled": false }
}
```

Details: [BUILD-CONTROL.md](references/BUILD-CONTROL.md)

## Environment Variables

```bash
# List
vercel env ls

# Add secret (interactive)
vercel env add SECRET_NAME production

# Pull to local .env
vercel env pull .env.local

# Bulk sync via REST (for agents)
curl -X POST "https://api.vercel.com/v10/projects/$PROJECT/env?upsert=true" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -d '{"key":"VAR","value":"val","target":["production"]}'
```

For OIDC + Vault: [SECRETS.md](references/SECRETS.md)

## Domain Setup

```bash
# Add domain to Vercel
vercel domains add example.com --token $VERCEL_TOKEN

# Then in Cloudflare DNS (DNS-only, not proxied):
# A record → Vercel IP  OR
# CNAME → cname.vercel-dns.com
```

## Workflow Checklist

### Phase 1: Initial Setup
- [ ] Install CLIs: `vercel`, `supabase`, `wrangler`, `jq`
- [ ] Set tokens: `VERCEL_TOKEN`, `CLOUDFLARE_API_TOKEN`
- [ ] Link project: `vercel link --yes`
- [ ] Pull env: `vercel pull --yes`

### Phase 2: Cost Optimization
- [ ] Add `"git": { "deploymentEnabled": false }` to vercel.json
- [ ] Set up prebuilt deploy workflow in CI
- [ ] Move marketing to Cloudflare Pages — [CLOUDFLARE-OFFLOAD.md](references/CLOUDFLARE-OFFLOAD.md)
- [ ] Move assets to R2 — [CLOUDFLARE-OFFLOAD.md](references/CLOUDFLARE-OFFLOAD.md)

### Phase 3: Secrets & Auth
- [ ] Store secrets via `vercel env add` or REST API
- [ ] Configure OIDC for cloud credentials — [SECRETS.md](references/SECRETS.md)
- [ ] Set up Supabase auth integration

### Phase 4: Database
- [ ] Create migrations: `supabase migration new`
- [ ] Apply: `supabase migration up` (local) / `supabase db push` (CI)
- [ ] Generate types: `supabase gen types typescript`

## Two-Button Deploy (Agent-Friendly)

```bash
# Marketing (Cloudflare Pages)
pnpm -C apps/marketing build
npx wrangler pages deploy apps/marketing/dist --branch=main

# App (Vercel prebuilt)
vercel pull --yes && vercel build --prod && vercel deploy --prebuilt --prod
```

## Critical Gotchas

| Gotcha | Fix |
|--------|-----|
| Ignored Build Step exits reversed | 0 = skip, 1 = build (not intuitive) |
| Ignored builds still count toward quotas | Use `git.deploymentEnabled: false` instead |
| Cloudflare proxy + Vercel = problems | Use DNS-only for Vercel domains |
| `.vercel/` folder committed | Add to `.gitignore` |
| Secrets in config files | Use `vercel env` or `wrangler secret put` |

Full list: [FOOTGUNS.md](references/FOOTGUNS.md)

## Core Commands

| Task | Command |
|------|---------|
| Deploy preview | `vercel` |
| Deploy prod | `vercel --prod` |
| Pull settings | `vercel pull` |
| Build locally | `vercel build` |
| Deploy prebuilt | `vercel deploy --prebuilt` |
| List env vars | `vercel env ls` |
| Add env var | `vercel env add NAME target` |
| Pull env to file | `vercel env pull` |

Full CLI reference: [CLI-COMMANDS.md](references/CLI-COMMANDS.md)

---

## AGENTS.md Blurb

Copy this to your project's AGENTS.md:

```markdown
### Vercel

Vercel CLI is installed and authenticated.

Project: `<PROJECT_NAME>`

Common commands:

\`\`\`bash
vercel pull --yes         # Fetch settings + env
vercel build --prod       # Build locally (saves build minutes)
vercel deploy --prebuilt --prod  # Deploy prebuilt artifact
vercel env ls             # List env vars
vercel env add SECRET production  # Add secret
\`\`\`

**Cost tip:** Use prebuilt workflow to avoid burning build credits.
```

## References

| Topic | Reference |
|-------|-----------|
| Architecture & cost model | [ARCHITECTURE.md](references/ARCHITECTURE.md) |
| Stopping build burn | [BUILD-CONTROL.md](references/BUILD-CONTROL.md) |
| **API-based build control** | [API-BUILD-CONTROL.md](references/API-BUILD-CONTROL.md) |
| All CLI commands | [CLI-COMMANDS.md](references/CLI-COMMANDS.md) |
| Secrets, env, OIDC, Vault | [SECRETS.md](references/SECRETS.md) |
| R2 + Pages cost offload | [CLOUDFLARE-OFFLOAD.md](references/CLOUDFLARE-OFFLOAD.md) |
| Full automation blueprint | [AUTOMATION-BLUEPRINT.md](references/AUTOMATION-BLUEPRINT.md) |
| Common mistakes | [FOOTGUNS.md](references/FOOTGUNS.md) |

## Token Setup (Non-Interactive Auth)

```bash
# Vercel: https://vercel.com/account/tokens
export VERCEL_TOKEN=xxx

# Cloudflare: https://dash.cloudflare.com/profile/api-tokens
export CLOUDFLARE_API_TOKEN=xxx

# Supabase: project settings → API
export SUPABASE_ACCESS_TOKEN=xxx
```

All CLIs read these automatically. No interactive login needed.
