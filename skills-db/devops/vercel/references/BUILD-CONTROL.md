# Build Control: Stopping Build Credit Burn

> **TL;DR:** Use `"git": { "deploymentEnabled": false }` in vercel.json, then deploy manually with `vercel --prod` or `--prebuilt`.

---

## Table of Contents

- [The Problem](#the-problem)
- [Solution Ranking](#solution-ranking)
- [Disable Auto-Deploys (Best)](#disable-auto-deploys-best)
- [Prebuilt Workflow](#prebuilt-workflow)
- [Ignored Build Step (Caution)](#ignored-build-step-caution)
- [Deploy Hooks](#deploy-hooks)
- [CI Integration](#ci-integration)

---

## The Problem

By default, Vercel creates:
- **Preview deployment** on every push to non-production branches
- **Production deployment** on every push to main/master

A typical dev workflow (commit, push, iterate) can trigger 20+ builds per day. At scale, this burns through build minutes fast.

## Solution Ranking

| Method | Config-as-Code | Stops Builds | Stops Quota Use |
|--------|----------------|--------------|-----------------|
| `git.deploymentEnabled: false` | ✅ | ✅ | ✅ |
| Prebuilt deploys | N/A | ✅ | ✅ |
| Ignored Build Step | ✅ | ⚠️ Partial | ❌ |
| Deploy Hooks | Dashboard | ✅ | ✅ |

## Disable Auto-Deploys (Best)

**The cleanest solution:** Disable automatic deployments entirely via config.

### vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "git": {
    "deploymentEnabled": false
  }
}
```

**Result:** Git pushes do nothing. You deploy only when you explicitly run `vercel` or `vercel --prod`.

### For Specific Branches

```json
{
  "git": {
    "deploymentEnabled": false
  }
}
```

Note: This is project-wide. For branch-specific control, combine with Ignored Build Step.

## Prebuilt Workflow

**Why:** Even with auto-deploys disabled, you can reduce Vercel build usage further by building locally/in CI and uploading artifacts.

### Full Flow

```bash
# 1. Pull project settings and env vars
vercel pull --yes --environment=production

# 2. Build locally (uses your machine's CPU, not Vercel's)
vercel build --prod

# 3. Deploy the prebuilt output
vercel deploy --prebuilt --prod

# Optional: Archive for faster upload
vercel deploy --prebuilt --prod --archive=tgz
```

### What Happens

1. `vercel pull` creates `.vercel/` with project config and env vars
2. `vercel build` creates `.vercel/output/` with build artifacts
3. `vercel deploy --prebuilt` uploads artifacts without running build

### Requirements

- `.vercel/project.json` must exist (created by `vercel pull` or `vercel link`)
- Build must complete successfully locally
- Same Node version as Vercel (check project settings)

## Ignored Build Step (Caution)

**Common misconception:** This does NOT prevent builds from being created.

### How It Works

In Project Settings → Git → Ignored Build Step, you provide a command. The exit code determines behavior:

| Exit Code | Result |
|-----------|--------|
| **0** | Skip the build (cancel) |
| **1** | Proceed with build |

**WARNING:** This is commonly documented backwards. Exit 0 = skip.

### Example Script

```bash
#!/bin/bash
# .vercel/ignore-build.sh

# Skip if only docs changed
if git diff --quiet HEAD^ HEAD -- docs/; then
  echo "Only docs changed, skipping"
  exit 0  # SKIP
fi

# Skip if commit message contains [skip ci]
if git log -1 --pretty=%B | grep -q "\[skip ci\]"; then
  echo "Skip CI requested"
  exit 0  # SKIP
fi

# Otherwise, build
exit 1  # BUILD
```

### Why This Is Not Enough

**Critical:** Ignored builds may still count toward:
- Deployment creation quotas
- Concurrent build slots

The build is "canceled" but the deployment record is created. For true cost control, disable auto-deploys instead.

## Deploy Hooks

Create an HTTP endpoint that triggers deployments.

### Setup

1. Dashboard → Project → Settings → Git → Deploy Hooks
2. Create hook for branch (e.g., `main`)
3. Get URL: `https://api.vercel.com/v1/integrations/deploy/xxx`

### Usage

```bash
# Trigger deploy
curl -X POST "https://api.vercel.com/v1/integrations/deploy/xxx"

# Trigger without cache
curl -X POST "https://api.vercel.com/v1/integrations/deploy/xxx?buildCache=false"
```

### Good For

- Centralized "who can deploy" control
- Triggering from external systems (CMS, webhook, etc.)
- Keeping Git pushes quiet

## CI Integration

### GitHub Actions (Manual Deploy Only)

```yaml
name: Deploy to Vercel
on:
  workflow_dispatch:  # Manual trigger only
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        default: 'preview'
        type: choice
        options:
          - preview
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Vercel CLI
        run: npm i -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=${{ inputs.environment }} --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build ${{ inputs.environment == 'production' && '--prod' || '' }}

      - name: Deploy
        run: vercel deploy --prebuilt ${{ inputs.environment == 'production' && '--prod' || '' }} --token=${{ secrets.VERCEL_TOKEN }}
```

### Key Points

- `workflow_dispatch` = manual trigger (no auto-deploy)
- `--prebuilt` = use CI-built artifacts
- `--token` = non-interactive auth

## Quick Reference

```bash
# Disable auto-deploys (add to vercel.json)
{ "git": { "deploymentEnabled": false } }

# Manual preview deploy
vercel

# Manual production deploy
vercel --prod

# Prebuilt workflow
vercel pull --yes && vercel build --prod && vercel deploy --prebuilt --prod

# Check deployment status
vercel ls
```
