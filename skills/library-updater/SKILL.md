---
name: library-updater
description: >-
  Update dependencies to latest stable versions. Use when upgrading libraries,
  updating Cargo.toml, pyproject.toml, package.json, go.mod, Gemfile, or
  modernizing dependencies.
---

# deps-update — Dependency Updater

> **Core:** Update one dependency at a time. Research before updating. Test after each. Never batch untested changes.

## THE EXACT PROMPT

```
Update all dependencies in this project to their latest stable versions.

For each dependency:
1. Use /research-software to find breaking changes between current and target version
2. Update the version
3. Run tests
4. Fix any issues (search web for recent solutions if needed)
5. If unfixable after 3 attempts, rollback and log why

Log everything to UPGRADE_LOG.md. Ask me before any refactoring that touches >10 files.
```

---

## Supported Languages

| Language | Manifest | Lock File | Registry |
|----------|----------|-----------|----------|
| Rust | `Cargo.toml` | `Cargo.lock` | crates.io |
| Python | `pyproject.toml`, `requirements.txt` | `poetry.lock`, `uv.lock` | PyPI |
| Node.js | `package.json` | `package-lock.json`, `yarn.lock` | npm |
| Go | `go.mod` | `go.sum` | proxy.golang.org |
| Ruby | `Gemfile` | `Gemfile.lock` | rubygems.org |

---

## Workflow

### Phase 1: Discovery
- [ ] Detect manifest: `Cargo.toml` | `pyproject.toml` | `package.json` | `go.mod` | `Gemfile`
- [ ] List dependencies with current versions
- [ ] Create `UPGRADE_LOG.md` from [template](assets/UPGRADE_LOG_TEMPLATE.md)

### Phase 2: Per-Dependency Loop

```
For each dependency where current != latest stable:
│
├─ 1. RESEARCH (invoke research-software skill)
│     /research-software [package] changelog [current] to [latest]
│     → Get: breaking changes, deprecations, migration notes
│
├─ 2. UPDATE
│     Edit manifest → run install command
│
├─ 3. TEST
│     Run test suite
│     │
│     ├─ PASS → Log success, next dependency
│     │
│     └─ FAIL → Research fix (web search 2025-2026)
│               → Apply fix → Retest
│               → 3 failures? Rollback, log reason, continue
│
└─ 4. LOG to UPGRADE_LOG.md
```

### Phase 3: Finalize
- [ ] Run full test suite
- [ ] Run security audit
- [ ] Complete UPGRADE_LOG.md summary

---

## Commands Quick Reference

| Language | Outdated | Update One | Test | Audit |
|----------|----------|------------|------|-------|
| Rust | `cargo outdated` | `cargo update -p X` | `cargo test` | `cargo audit` |
| Python | `uv pip list --outdated` | `uv add X@latest` | `pytest` | `pip-audit` |
| Node | `npm outdated` | `npm i X@latest` | `npm test` | `npm audit` |
| Go | `go list -m -u all` | `go get X@latest` | `go test ./...` | `govulncheck` |
| Ruby | `bundle outdated` | `bundle update X` | `rspec` | `bundle audit` |

**Full commands & gotchas:** [LANGUAGES.md](references/LANGUAGES.md)

---

## Version Rules

```
UPGRADE:  1.2.3 → latest stable (e.g., 1.3.0)
PRESERVE: alpha/beta/rc, git refs, path deps, nightly → note in log
SKIP:     if only alpha/beta available → stay on current stable
```

---

## Failure Handling

| Scenario | Action |
|----------|--------|
| Tests fail | Research fix → apply → retest (max 3 attempts) |
| Can't fix | Rollback, log details with error messages |
| Deprecation warnings | Fix if <5 call sites, else log for user |
| Major refactor needed | **Stop and ask user** before proceeding |
| Network/registry error | Retry 3x, then skip with note |

### Circuit Breakers — Stop and Ask User

- 5+ dependencies fail consecutively
- Total test failures exceed 10
- Estimated refactoring exceeds 20 files
- Security vulnerability introduced (detected by audit tools)

### Rollback Procedure
```bash
# Git-based (preferred)
git checkout -- Cargo.toml Cargo.lock

# Or restore from backup
cp .upgrade-backup/Cargo.toml .
```

---

## Integrating research-software

For each dependency upgrade, invoke the research-software skill:

```
/research-software [package-name] breaking changes [old-version] to [new-version]
```

This returns:
- Breaking changes with code examples
- Deprecation notices
- Migration guides
- Recent issues/PRs about upgrade problems

**Why:** research-software searches GitHub releases, changelogs, and recent web content more effectively than manual lookup.

---

## Progress Tracking

Create `claude-upgrade-progress.json` for crash recovery:

```json
{
  "status": "in_progress",
  "current": "serde",
  "completed": ["tokio", "anyhow"],
  "failed": [],
  "pending": ["reqwest", "tracing"]
}
```

Update after each dependency. Resume from this state if interrupted.

---

## Validation

After all updates:
```bash
# Verify everything works
./scripts/validate-upgrade.sh

# Or manually:
# 1. Clean build
# 2. Full test suite
# 3. Security audit
# 4. No new deprecation warnings (or documented)
```

---

## UPGRADE_LOG.md Format

```markdown
# Dependency Upgrade Log

**Date:** 2025-01-16  |  **Project:** my-project  |  **Language:** Rust

## Summary
- **Updated:** 12  |  **Skipped:** 3  |  **Failed:** 1  |  **Needs attention:** 2

## Updates

### serde: 1.0.190 → 1.0.215
- **Breaking:** None
- **Tests:** ✓ Passed

### tokio: 1.35.0 → 1.40.0
- **Breaking:** `runtime::Handle::block_on` removed
- **Migration:** Replaced with `Runtime::block_on`
- **Tests:** ✓ Passed after fix

## Failed

### problematic-crate: 0.5.0 → 0.6.0
- **Reason:** Requires Rust 1.75+, project uses 1.70
- **Action:** Rolled back

## Needs Attention

### legacy-lib: 2.0.0 → 3.0.0
- **Issue:** Major API redesign, ~50 call sites
- **Migration guide:** https://example.com/migration
```

---

## Reference Index

| Topic | Reference |
|-------|-----------|
| Commands by language | [LANGUAGES.md](references/LANGUAGES.md) |
| Changelog reading tips | [CHANGELOG-TIPS.md](references/CHANGELOG-TIPS.md) |
| Progress template | [assets/progress-template.json](assets/progress-template.json) |
| Log template | [assets/UPGRADE_LOG_TEMPLATE.md](assets/UPGRADE_LOG_TEMPLATE.md) |

---

## Anti-Patterns

❌ **Batch updates** — Update 10 deps, then test. Which one broke it?
❌ **Skip research** — "It's just a patch version" → surprise breaking change
❌ **Ignore deprecations** — They become errors in the next major
❌ **Force through failures** — If it won't fix in 3 tries, it needs human judgment
