# CI/CD Golden File Workflows

> Golden files in CI must NEVER auto-update. CI compares only. Developers update locally, review diffs, then commit.

## The Iron Rule

```
CI = COMPARE ONLY (never write golden files)
Local = UPDATE mode available (developer reviews + commits)
```

## GitHub Actions: Golden File Check

```yaml
name: Golden File Check
on: [pull_request]

jobs:
  golden-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tests (strict golden comparison)
        run: cargo test
        env:
          INSTA_UPDATE: "no"          # Rust insta: fail on mismatch, never write
          # Or for custom golden frameworks:
          UPDATE_GOLDENS: ""           # Empty = compare mode

      - name: Check for pending snapshot updates
        run: |
          # insta: check for .snap.new files
          if find . -name '*.snap.new' | grep -q .; then
            echo "::error::Pending snapshot updates found!"
            echo "Run 'cargo insta review' locally and commit the updates."
            find . -name '*.snap.new' -exec echo "  {}" \;
            exit 1
          fi

          # Custom goldens: check for .actual files
          if find . -name '*.actual' | grep -q .; then
            echo "::error::Golden file mismatches found!"
            echo "Run with UPDATE_GOLDENS=1, review diffs, and commit."
            find . -name '*.actual' -exec echo "  {}" \;
            exit 1
          fi

      # On failure: upload the actual outputs for easy comparison
      - name: Upload golden diffs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: golden-diffs
          path: |
            **/*.snap.new
            **/*.actual
          retention-days: 7
```

## Vitest/Jest: Snapshot CI Mode

```yaml
      - name: Run tests (snapshot strict mode)
        run: npx vitest run --reporter=verbose
        env:
          CI: "true"
          # Vitest automatically fails on obsolete/missing snapshots in CI
```

```typescript
// vitest.config.ts — CI-specific snapshot behavior
export default defineConfig({
  test: {
    // In CI, fail immediately on snapshot mismatch
    snapshotOptions: {
      updateSnapshot: process.env.CI ? "none" : "new",
    },
  },
});
```

## PR Review Workflow for Golden Changes

When a PR includes golden file updates:

```yaml
      # Post a comment showing which golden files changed
      - name: Comment golden changes
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const { execSync } = await import('node:child_process');
            const diff = execSync('git diff --name-only HEAD~1 -- "**/*.golden" "**/*.snap"')
              .toString().trim();
            if (!diff) return;

            const files = diff.split('\n');
            const body = [
              '## Golden Files Changed',
              '',
              `${files.length} golden file(s) updated in this PR:`,
              ...files.map(f => `- \`${f}\``),
              '',
              '**Review each change carefully** — golden updates should be intentional.',
            ].join('\n');

            if (context.payload.pull_request) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.payload.pull_request.number,
                body,
              });
            }
```

## Developer Workflow

```bash
# 1. Make code changes
vim src/my_module.rs

# 2. Run tests — see failures
cargo test

# 3. Review what changed
cargo insta review          # Interactive TUI (Rust)
# or
UPDATE_GOLDENS=1 cargo test # Custom framework
git diff tests/golden/      # Review EVERY change

# 4. Accept changes you agree with
cargo insta accept           # Rust
# or
git add tests/golden/        # Custom

# 5. Commit with clear message
git commit -m "Update goldens: refactored output format for clarity"

# 6. CI will verify your committed goldens match
git push
```

## Preventing Stale Goldens

```yaml
# Weekly job: detect orphaned golden files (no test references them)
name: Golden Cleanup
on:
  schedule:
    - cron: '0 6 * * 1'  # Monday 6 AM

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Find orphaned snapshots
        run: |
          # insta: detect unreferenced snapshots
          INSTA_UPDATE=unseen cargo test 2>&1 | grep "unused snapshot" || echo "No orphans"
```

## Environment Variable Reference

| Variable | Value | Effect |
|----------|-------|--------|
| `INSTA_UPDATE=no` | CI | Fail on any mismatch, never write |
| `INSTA_UPDATE=always` | Local | Overwrite all snapshots |
| `INSTA_UPDATE=new` | Local | Only create new, fail on changed |
| `INSTA_UPDATE=unseen` | Cleanup | Flag unreferenced snapshots |
| `UPDATE_GOLDENS=1` | Local | Overwrite golden files (custom) |
| `UPDATE_EXPECT=1` | Local | Rewrite inline expects (expect_test) |
| `REGENERATE_GOLDENFILES=1` | Local | Overwrite (goldenfile crate) |
| `CI=true` | CI | Vitest/Jest strict snapshot mode |
