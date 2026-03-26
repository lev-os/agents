# Git Hooks & CI Security Checks

This repo uses pre-commit hooks and GitHub Actions to prevent secrets and hardcoded paths from being committed.

## Local Setup (pre-commit)

1. Install [pre-commit](https://pre-commit.com):
   ```bash
   pip install pre-commit
   # or: brew install pre-commit
   ```

2. Install the hooks:
   ```bash
   pre-commit install
   ```

3. (Optional) Run manually on all files:
   ```bash
   pre-commit run --all-files
   ```

### What runs on commit

- **gitleaks**: Scans staged files for secrets (API keys, tokens, passwords)
- **check-hardcoded-paths**: Blocks commits containing `/Users/username` or `/home/username` – use `$HOME` or relative paths instead

## CI (GitHub Actions)

On every push and PR to `main`:

- **secrets**: Gitleaks scans the full repo history
- **hardcoded-paths**: Grep check for `/Users/` or `/home/` with real-looking usernames

## Fixing failures

- **Secret detected**: Remove the secret, use env vars or a secrets manager, add to `.env` (gitignored)
- **Hardcoded path**: Replace `/Users/yourname/...` with `$HOME/...` or a relative path
