# Changelog Tips

Patterns for finding and parsing changelogs. Use alongside research-software.

---

## Priority Order

Check in this order:
1. **GitHub Releases** — usually most detailed
2. **CHANGELOG.md** — in repo root
3. **Migration guides** — for major versions
4. **Registry page** — basic version info
5. **Web search** — `"{package} {version} breaking changes"`

---

## URL Patterns by Ecosystem

| Ecosystem | Registry | Releases | Changelog |
|-----------|----------|----------|-----------|
| Rust | `crates.io/crates/{name}` | `github.com/{owner}/{repo}/releases` | `CHANGELOG.md` |
| Python | `pypi.org/project/{name}` | Via PyPI → Project URLs | `HISTORY.md` common |
| Node | `npmjs.com/package/{name}` | Via npm → Repository | `CHANGELOG.md` |
| Go | `pkg.go.dev/{module}` | `github.com/{path}/releases` | `CHANGELOG.md` |
| Ruby | `rubygems.org/gems/{name}` | Via RubyGems → Homepage | `CHANGELOG.md` |

---

## Web Search Patterns

```
"{package}" "{from_version}" "{to_version}" "breaking"
"{package}" "{to_version}" "migration"
"{package}" "{to_version}" "upgrade guide"
"{package}" "changelog" site:github.com
```

Useful site filters:
- `site:github.com` — issues discussing breakage
- `site:reddit.com/r/rust` (or /r/python, etc.)

---

## What to Grep For

```bash
grep -i "break\|deprecat\|remov\|chang\|migrat" CHANGELOG.md
```

---

## Semver Signals

| Version Change | Expected Impact |
|----------------|-----------------|
| `1.2.3 → 1.2.4` | Patch: bug fixes only |
| `1.2.3 → 1.3.0` | Minor: new features, no breaks |
| `1.2.3 → 2.0.0` | Major: breaking changes likely |

---

## Red Flags in Changelogs

- `BREAKING:` or `⚠️` markers
- "Removed" or "Deleted" sections
- "Minimum version now requires..." (language version)
- "Peer dependency version requirements" (Node especially)
- "API changed from X to Y"
- "Deprecated X, use Y instead"
- Migration guides (means major changes)

---

## Notable Packages with Migration Guides

### Rust
- **tokio** — tokio.rs/blog for major releases
- **axum** — GitHub releases have upgrade notes
- **sqlx** — CHANGELOG.md is comprehensive

### Python
- **django** — docs.djangoproject.com/en/X.Y/releases/
- **pydantic** — docs.pydantic.dev/latest/migration/
- **sqlalchemy** — docs have migration for each major
- **fastapi** — GitHub releases

### Node.js
- **express** — expressjs.com has upgrade guide
- **react** — reactjs.org/blog for releases
- **next** — nextjs.org/docs/upgrading
- **typescript** — TypeScript blog + release notes

### Go
- **gorm** — gorm.io/docs has migration guide for v2
- **Standard library** — tip.golang.org/doc/go1.X

### Ruby
- **rails** — guides.rubyonrails.org/upgrading_ruby_on_rails.html
- **sidekiq** — GitHub wiki has upgrade notes

---

## Finding Repo from Package

```bash
# Rust
cargo info serde  # shows repository URL

# Python
pip show requests  # shows Home-page

# Node
npm view express repository.url

# Go
# Module path IS the repo: github.com/gin-gonic/gin

# Ruby
gem specification rails homepage
```

---

## Quick Lookup Commands

```bash
# Rust: Open releases page
xdg-open "https://github.com/$(cargo info CRATE 2>/dev/null | grep -oP 'github.com/\K[^"]+' | head -1)/releases"

# Python: Open PyPI
xdg-open "https://pypi.org/project/PACKAGE/"

# Node: Open npm
xdg-open "https://www.npmjs.com/package/PACKAGE"

# Go: Open pkg.go.dev
xdg-open "https://pkg.go.dev/MODULE"
```

---

## Caching Strategy

For large updates, cache changelog data to avoid re-fetching:
```json
{
  "serde": {
    "1.0.215": {
      "fetched": "2025-01-16",
      "breaking": false,
      "notes": "Bug fixes only"
    }
  }
}
```
