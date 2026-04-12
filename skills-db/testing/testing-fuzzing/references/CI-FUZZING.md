# CI/CD Fuzzing Integration

> Run fuzzing in CI to catch regressions and continuously discover new bugs.

## Strategy: Two-Tier Fuzzing

| Tier | When | Duration | Purpose |
|------|------|----------|---------|
| **PR fuzzing** | Every pull request | 5-15 min | Catch regressions in changed code |
| **Continuous fuzzing** | Nightly on main | Hours-days | Deep exploration for new bugs |

## PR Fuzzing (Short Runs)

```yaml
# GitHub Actions: run fuzz regression corpus on every PR
name: Fuzz Regression
on: pull_request
jobs:
  fuzz:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@nightly
      - run: cargo install cargo-fuzz

      # Run each fuzz target against its committed corpus
      # This catches regressions — inputs that USED to not crash
      - name: Fuzz regression tests
        run: |
          for target in $(cargo fuzz list); do
            echo "=== $target ==="
            cargo fuzz run "$target" -- \
              -max_total_time=60 \
              -runs=10000 \
              2>&1 || { echo "CRASH in $target"; exit 1; }
          done
        timeout-minutes: 10

      # Upload any crash artifacts
      - name: Upload crash artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: fuzz-crashes
          path: fuzz/artifacts/
```

## Continuous Fuzzing (Long Runs)

```yaml
# Nightly: deep fuzzing with corpus persistence
name: Continuous Fuzz
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
  workflow_dispatch:

jobs:
  fuzz:
    runs-on: ubuntu-latest
    timeout-minutes: 360  # 6 hours
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@nightly
      - run: cargo install cargo-fuzz

      # Restore cached corpus from previous runs
      - uses: actions/cache@v4
        with:
          path: fuzz/corpus/
          key: fuzz-corpus-${{ github.sha }}
          restore-keys: fuzz-corpus-

      - name: Run fuzzing
        run: |
          for target in $(cargo fuzz list); do
            cargo fuzz run "$target" -- \
              -max_total_time=3600 \
              -print_final_stats=1 \
              2>&1 | tee "fuzz-${target}.log"
          done

      # Minimize corpus after long run
      - name: Minimize corpus
        run: |
          for target in $(cargo fuzz list); do
            cargo fuzz cmin "$target" || true
          done

      # Save corpus for next run
      - uses: actions/cache/save@v4
        with:
          path: fuzz/corpus/
          key: fuzz-corpus-${{ github.sha }}

      - name: Upload crash artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: fuzz-crashes-nightly
          path: fuzz/artifacts/
```

## OSS-Fuzz Integration

For open-source projects, use Google's free continuous fuzzing:

```dockerfile
# oss-fuzz/Dockerfile
FROM gcr.io/oss-fuzz-base/base-builder-rust
RUN cargo install cargo-fuzz
COPY . $SRC/my_project
WORKDIR $SRC/my_project
COPY oss-fuzz/build.sh $SRC/build.sh
```

```bash
# oss-fuzz/build.sh
cd $SRC/my_project
cargo fuzz build
for target in $(cargo fuzz list); do
  cp fuzz/target/x86_64-unknown-linux-gnu/release/$target $OUT/
  cp -r fuzz/corpus/$target $OUT/${target}_seed_corpus || true
done
```

## Corpus Persistence Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| Git (committed corpus) | Always available, versioned | Bloats repo |
| CI cache (`actions/cache`) | Fast, no repo bloat | Evicted after 7 days |
| Cloud storage (S3/R2) | Persistent, large | Setup overhead |
| OSS-Fuzz (managed) | Free, professional | Open-source only |

**Recommendation:** Commit a minimized seed corpus to git. Use CI cache for the evolving corpus. Periodically `cmin` and re-commit.

## Converting Crashes to Issues

```yaml
# When CI finds a crash, auto-create a GitHub issue
- name: Create issue for crash
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const crashes = fs.readdirSync('fuzz/artifacts/').filter(f => f.startsWith('crash-'));
      if (crashes.length === 0) return;
      await github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: `Fuzz: ${crashes.length} crash(es) found`,
        body: `Crashes found:\n${crashes.map(c => '- ' + c).join('\n')}\n\nDownload artifacts from the workflow run.`,
        labels: ['bug', 'fuzzing'],
      });
```
