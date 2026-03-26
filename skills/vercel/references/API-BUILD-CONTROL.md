# Vercel Build Control via API

> **The problem:** Every git push triggers a build, burning through credits.
> **The solution:** API-based control over deployments.

## Disable Auto-Deployments

```bash
curl -s -X PATCH "https://api.vercel.com/v9/projects/${PROJECT_ID}?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "gitProviderOptions": {
      "createDeployments": "disabled"
    }
  }'
```

## Smart Build Skipping (Monorepos)

```bash
curl -s -X PATCH "https://api.vercel.com/v9/projects/${PROJECT_ID}?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "enableAffectedProjectsDeployments": true
  }'
```

## Custom Ignore Build Script

Create `scripts/vercel-ignore-build.sh`:

```bash
#!/bin/bash
# Exit 1 = SKIP build, Exit 0 = PROCEED
set -e

PREV_SHA="${VERCEL_GIT_PREVIOUS_SHA:-HEAD~1}"
CURR_SHA="${VERCEL_GIT_COMMIT_SHA:-HEAD}"

TRIGGER_PATHS=(
    "apps/web/"
    "packages/ui/"
    "package.json"
    "pnpm-lock.yaml"
)

for path in "${TRIGGER_PATHS[@]}"; do
    if git diff --name-only "$PREV_SHA" "$CURR_SHA" 2>/dev/null | grep -q "^${path}"; then
        echo "✓ Changes in: $path"
        exit 0  # Build
    fi
done

echo "✗ No relevant changes"
exit 1  # Skip
```

Configure via API:

```bash
curl -s -X PATCH "https://api.vercel.com/v9/projects/${PROJECT_ID}?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "commandForIgnoringBuildStep": "bash scripts/vercel-ignore-build.sh"
  }'
```

## All-in-One Configuration

```bash
curl -s -X PATCH "https://api.vercel.com/v9/projects/${PROJECT_ID}?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "gitProviderOptions": {
      "createDeployments": "disabled"
    },
    "enableAffectedProjectsDeployments": true,
    "commandForIgnoringBuildStep": "bash scripts/vercel-ignore-build.sh"
  }'
```

## Verify Settings

```bash
curl -s -X GET "https://api.vercel.com/v9/projects/${PROJECT_ID}?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" | jq '{
    name: .name,
    createDeployments: .gitProviderOptions.createDeployments,
    affectedProjects: .enableAffectedProjectsDeployments,
    ignoreCommand: .commandForIgnoringBuildStep
  }'
```

## Getting Credentials

```bash
# Token from Vercel CLI auth
cat "$HOME/Library/Application Support/com.vercel.cli/auth.json"

# Project and Team IDs
cat .vercel/project.json
# {"projectId":"prj_abc...", "orgId":"team_xyz..."}
```

## Quick Reference

| Setting | API Field | Value |
|---------|-----------|-------|
| Disable auto-deploy | `gitProviderOptions.createDeployments` | `"disabled"` |
| Smart skip | `enableAffectedProjectsDeployments` | `true` |
| Custom check | `commandForIgnoringBuildStep` | `"bash ..."` |
