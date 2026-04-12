# Footguns: Common Mistakes

> **TL;DR:** Exit codes are backwards, ignored builds still count, don't proxy Vercel, and `.vercel/` is machine state.

---

## Table of Contents

- [Build Control Mistakes](#build-control-mistakes)
- [DNS & Proxy Mistakes](#dns--proxy-mistakes)
- [Secrets Mistakes](#secrets-mistakes)
- [Caching Mistakes](#caching-mistakes)
- [CLI Mistakes](#cli-mistakes)
- [Supabase Mistakes](#supabase-mistakes)

---

## Build Control Mistakes

### #1: Ignored Build Step Exit Codes Are Backwards

**The trap:** Most CI systems use exit 0 = success = proceed. Vercel is different.

| Exit Code | Vercel Behavior |
|-----------|-----------------|
| **0** | **SKIP** the build |
| **1** | **PROCEED** with build |

```bash
# WRONG - this BUILDS (exit 1 = proceed)
if [ "$VERCEL_ENV" = "preview" ]; then
  exit 1  # Thinking "fail = skip"
fi

# CORRECT - this SKIPS
if [ "$VERCEL_ENV" = "preview" ]; then
  exit 0  # Exit 0 = skip
fi
```

### #2: Thinking Ignored Builds Don't Count

**The trap:** You skip builds to save credits, but deployments are still created.

**Reality:** Ignored/canceled builds may still count toward:
- Deployment creation quotas
- Concurrent build slots

**Fix:** Use `"git": { "deploymentEnabled": false }` to prevent deployment creation entirely.

### #3: Not Disabling Auto-Deploys in Config

**The trap:** Manually avoiding pushes, using ignored build step, etc.

**Fix:** Just disable it properly:

```json
{
  "git": { "deploymentEnabled": false }
}
```

This is the only config-as-code way to truly stop automatic deployments.

---

## DNS & Proxy Mistakes

### #4: Proxying Vercel Through Cloudflare

**The trap:** You want Cloudflare WAF/caching for your Vercel app, so you enable proxy (orange cloud).

**Reality:** Vercel explicitly does NOT recommend this. Issues include:
- Cache coherence problems
- Reduced traffic visibility
- Potential mitigation system conflicts
- Latency overhead

**Fix:** Use DNS-only (gray cloud) for Vercel domains:

```
app.example.com  CNAME  cname.vercel-dns.com  (proxy: OFF)
```

Put Cloudflare proxy only on domains where Cloudflare is the origin (Pages, Workers, R2).

### #5: Single-Domain Path Routing

**The trap:** You want `example.com/app` to go to Vercel and `example.com/*` to Cloudflare.

**Reality:** This requires reverse-proxying Vercel, which Vercel discourages.

**Fix:** Split by hostname:
- `app.example.com` → Vercel
- `www.example.com` → Cloudflare Pages

Use `_redirects` on Pages to redirect `/app/*` to the Vercel domain.

---

## Secrets Mistakes

### #6: Committing `.vercel/` Directory

**The trap:** `.vercel/` contains useful project state, so you commit it.

**Reality:** It contains:
- Machine-specific paths
- Pulled environment variables (including secrets!)
- Project linkage that may differ per developer

**Fix:**

```gitignore
# .gitignore
.vercel/
```

### #7: Secrets in Config Files

**The trap:** Putting secrets directly in `vercel.json`, `wrangler.jsonc`, or code.

**Fix:**
- Vercel: `vercel env add` or REST API
- Workers: `wrangler secret put`
- Never in config files or source code

### #8: Using Plain Type for Secrets

**The trap:** Adding env vars via CLI without specifying type.

**Reality:** Default may be `plain`, visible in dashboard/logs.

**Fix:** Use REST API with `"type": "encrypted"` or `"type": "sensitive"`:

```bash
curl -X POST "https://api.vercel.com/v10/projects/$PROJECT_ID/env?upsert=true" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -d '{"key":"SECRET","value":"xxx","target":["production"],"type":"encrypted"}'
```

### #9: Long-Lived Cloud Credentials in Env Vars

**The trap:** Storing AWS keys, GCP service account JSON in Vercel env vars.

**Fix:** Use OIDC federation:
- `VERCEL_OIDC_TOKEN` is available in builds/functions
- Exchange for short-lived credentials
- No static secrets to rotate

---

## Caching Mistakes

### #10: Caching Authenticated Content

**The trap:** Adding `Cache-Control` headers without considering auth.

**Reality:** If a response varies by user (cookies, auth headers), caching it serves wrong content to other users.

**Fix:**
- Never cache responses that depend on authentication
- Use `Cache-Control: private` or `no-store` for personalized content
- Only cache truly public, non-personalized content

### #11: Not Using Immutable for Hashed Assets

**The trap:** Using short cache times for JS/CSS bundles.

**Reality:** Next.js bundles are fingerprinted (e.g., `main-abc123.js`). They can be cached forever.

**Fix:**

```
/_next/static/*
  Cache-Control: public, max-age=31536000, immutable
```

---

## CLI Mistakes

### #12: Forgetting `--token` in Scripts

**The trap:** Scripts work locally (where you're logged in), fail in CI.

**Fix:** Always use `--token` for Vercel CLI:

```bash
vercel --token "$VERCEL_TOKEN" --prod
```

### #13: Using `vercel env pull` in Production

**The trap:** Pulling production secrets to local machine.

**Reality:** Secrets now exist outside your secure environment.

**Fix:**
- Use separate dev/staging secrets
- If you must pull production, immediately rotate after debugging

### #14: Not Using `--yes` in Automation

**The trap:** Scripts hang waiting for confirmation.

**Fix:**

```bash
vercel pull --yes --token "$VERCEL_TOKEN"
vercel link --yes --token "$VERCEL_TOKEN"
```

---

## Supabase Mistakes

### #15: Using `db push` in Development

**The trap:** `supabase db push` is convenient, so you use it everywhere.

**Reality:** `db push` is designed for CI/CD. For local development:
- Use `supabase migration new` to create migrations
- Use `supabase migration up` to apply locally

**Fix:**
- Local: `migration new` → `migration up`
- CI/CD: `db push`

### #16: Not Generating Types After Schema Changes

**The trap:** Change schema, forget to regenerate TypeScript types.

**Fix:** Make it part of your workflow:

```bash
supabase migration up && supabase gen types typescript --local > types/supabase.ts
```

### #17: Forgetting to Link Supabase Project

**The trap:** Commands fail with cryptic errors.

**Fix:**

```bash
supabase link --project-ref your-project-ref
```

Check if linked:

```bash
cat supabase/.temp/project-ref 2>/dev/null || echo "Not linked"
```

---

## Quick Checklist

Before deploying, verify:

- [ ] Auto-deploys disabled: `"git": { "deploymentEnabled": false }`
- [ ] `.vercel/` in `.gitignore`
- [ ] Vercel domain is DNS-only in Cloudflare (gray cloud)
- [ ] No secrets in config files
- [ ] Using `--token` in all scripts
- [ ] Using `--yes` for non-interactive execution
- [ ] Supabase project linked
- [ ] TypeScript types regenerated after schema changes

---

## Error Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| "Not linked to project" | Missing `.vercel/project.json` | `vercel link --yes` |
| "Unauthorized" | Bad/missing token | Check `$VERCEL_TOKEN` |
| "Build canceled" | Ignored build step returned 0 | Expected behavior (0 = skip) |
| "Cannot proxy" | Cloudflare proxy + Vercel | Use DNS-only |
| "Migration failed" | Supabase not linked | `supabase link` |
| "Types not found" | Forgot to generate | `supabase gen types` |
