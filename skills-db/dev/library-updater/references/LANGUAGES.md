# Language-Specific Reference

Detailed commands, quirks, and patterns for each supported language.

---

## Table of Contents
- [Rust](#rust)
- [Python](#python)
- [Node.js](#nodejs)
- [Go](#go)
- [Ruby](#ruby)

---

## Rust

### Manifest
```toml
# Cargo.toml
[dependencies]
serde = "1.0"           # Stable - upgrade
serde = "=1.0.190"      # Pinned - ask before upgrade
tokio = { version = "1.35", features = ["full"] }

# Preserve these (don't upgrade):
my-crate = { git = "https://github.com/...", branch = "main" }
local-crate = { path = "../local" }
nightly-crate = "0.0.0-nightly.2024"
```

### Commands
```bash
# Check outdated
cargo outdated

# Update single dependency
cargo update -p serde

# Update all (respects Cargo.toml constraints)
cargo update

# Build & test
cargo build
cargo test
cargo test --all-features

# Security audit
cargo audit
cargo deny check
```

### Version Query
```bash
# Latest version from crates.io
cargo search serde --limit 1
# Or: curl https://crates.io/api/v1/crates/serde | jq '.crate.max_stable_version'
```

### Gotchas
- `cargo update` only updates within Cargo.toml constraints
- Must manually edit Cargo.toml for major version bumps
- Feature flags can cause incompatibilities
- Workspace members share Cargo.lock
- `edition` in Cargo.toml affects compatibility

---

## Python

### Manifests
```toml
# pyproject.toml (Poetry)
[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"     # Upgrade
django = "5.0a1"         # Alpha - preserve

# pyproject.toml (uv/pip)
[project]
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0,<3.0",
]

# requirements.txt
requests==2.31.0
django>=4.2,<5.0
```

### Commands
```bash
# Poetry
poetry show --outdated
poetry update requests
poetry update  # all
poetry install
poetry run pytest

# uv
uv pip list --outdated
uv add requests@latest
uv sync
uv run pytest

# pip
pip list --outdated
pip install requests --upgrade
pip install -r requirements.txt
pytest

# Security
pip-audit
safety check
```

### Version Query
```bash
# Latest from PyPI
curl -s https://pypi.org/pypi/requests/json | jq -r '.info.version'

# All versions
pip index versions requests
```

### Gotchas
- `^` (caret) in Poetry allows minor updates only
- `>=` can pull breaking changes on install
- Python version constraints matter
- Virtual environment must be active
- Some packages have `extras` that affect dependencies

---

## Node.js

### Manifest
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

### Commands
```bash
# npm
npm outdated
npm update express
npm update  # all (within package.json ranges)
npm install express@latest  # force latest
npm test
npm audit

# yarn
yarn outdated
yarn upgrade express
yarn upgrade-interactive
yarn test
yarn audit

# pnpm
pnpm outdated
pnpm update express
pnpm update
pnpm test
pnpm audit

# bun
bun outdated
bun update express
bun test
```

### Version Query
```bash
# Latest from npm
npm view express version
npm view express versions --json | jq '.[-1]'
```

### Gotchas
- `^` allows minor/patch, `~` allows patch only
- `package-lock.json` must be committed
- Peer dependency conflicts are common
- Node version in `engines` field matters
- Workspaces complicate updates

---

## Go

### Manifest
```go
// go.mod
module myproject

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    golang.org/x/sync v0.5.0
)

// Indirect dependencies managed automatically
```

### Commands
```bash
# Check outdated
go list -m -u all

# Update single
go get github.com/gin-gonic/gin@latest

# Update all
go get -u ./...

# Tidy (remove unused, add missing)
go mod tidy

# Build & test
go build ./...
go test ./...

# Security
govulncheck ./...
```

### Version Query
```bash
# Latest version
go list -m -versions github.com/gin-gonic/gin | awk '{print $NF}'

# Or via proxy
curl -s "https://proxy.golang.org/github.com/gin-gonic/gin/@latest" | jq -r '.Version'
```

### Gotchas
- Go uses commit-based versioning for v0.x and v2+
- `+incompatible` suffix means no go.mod in source
- Major versions v2+ require `/v2` import path
- `go mod tidy` can add/remove dependencies
- Minimum Go version in `go.mod` matters

---

## Ruby

### Manifest
```ruby
# Gemfile
source 'https://rubygems.org'

gem 'rails', '~> 7.1.0'
gem 'puma', '>= 5.0'
gem 'sidekiq'  # any version

group :development do
  gem 'rubocop'
end
```

### Commands
```bash
# Check outdated
bundle outdated

# Update single
bundle update rails

# Update all
bundle update

# Install
bundle install

# Test
bundle exec rspec
bundle exec rails test

# Security
bundle audit check --update
bundler-audit
```

### Version Query
```bash
# Latest from rubygems
gem search rails --remote --exact | head -1
curl -s "https://rubygems.org/api/v1/gems/rails.json" | jq -r '.version'
```

### Gotchas
- `~>` (pessimistic) allows patch updates only
- Bundler groups affect which gems load
- Ruby version in `.ruby-version` matters
- `Gemfile.lock` should be committed for apps
- Some gems have native extensions that can fail

---

## Quick Reference Table

| Task | Rust | Python (uv) | Node (npm) | Go |
|------|------|-------------|------------|-----|
| Outdated | `cargo outdated` | `uv pip list --outdated` | `npm outdated` | `go list -m -u all` |
| Update one | `cargo update -p X` | `uv add X@latest` | `npm i X@latest` | `go get X@latest` |
| Update all | `cargo update` | `uv sync` | `npm update` | `go get -u ./...` |
| Install | `cargo build` | `uv sync` | `npm install` | `go mod tidy` |
| Test | `cargo test` | `pytest` | `npm test` | `go test ./...` |
| Audit | `cargo audit` | `pip-audit` | `npm audit` | `govulncheck` |
