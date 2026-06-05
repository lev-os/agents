# sync — .agents repo sync runbook

Full-boundary sync for the `.agents` skills repo. Run this instead of a bare
`git pull`/`push` so generated caches never cause merge conflicts again.

**Context:** `skills-inventory.jsonl` and `skill-graph.json` are *generated*
artifacts (machine-specific absolute paths, `usage_count`, `usage_tier`,
rotation telemetry). They are gitignored — never commit them. They rebuild from
the `SKILL.md` source files via `lev-skills`.

---

## Steps

### 0. Ensure rebuild hooks exist (self-bootstrap)
Check for the git hooks below; install any that are missing, then `chmod +x`.
This is what makes the rebuild automatic on every machine — the hooks live in
`.git/hooks/` which is *not* version-controlled, so each checkout installs its
own from this runbook.

- `.git/hooks/post-merge`  → rebuild caches after every pull/merge
- `.git/hooks/post-commit` → (installed by `lev install`) refreshes the lev index

Hook body for **post-merge** (and `post-rewrite`, optional):
```bash
#!/bin/bash
# Rebuild generated skill caches after pull/merge. Background, never blocks.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
command -v lev-skills >/dev/null 2>&1 || exit 0
( cd "$REPO_ROOT" && lev-skills inventory --rebuild >/dev/null 2>&1
  lev-skills graph rebuild >/dev/null 2>&1 ) &
exit 0
```

### 1. Commit all dirty files
Stage and commit everything tracked-and-dirty (the generated caches are
gitignored, so they won't be staged). Use a concise message describing the
session's changes.
```bash
git add -A && git commit -m "<message>"   # skip if nothing to commit
```

### 2. Pull
```bash
git pull
```

### 3. Rebuild skill graph + inventory caches
(The post-merge hook does this automatically; run manually if hooks were just
installed or you want it synchronous.)
```bash
lev-skills inventory --rebuild
lev-skills graph rebuild
```

### 4. Conflict resolution policy
If a pull leaves conflicts:
- **Generated caches** (`skills-inventory.jsonl`, `skill-graph.json`): never
  hand-merge — `git checkout --theirs <file>` (or remove) then rebuild. They
  should be gitignored; if one reappears tracked, `git rm --cached` it.
- **Trivial source conflicts** (additive, non-overlapping intent): triage,
  synthesize, and **preserve the intent of both sides** — merge them.
- **Non-trivial conflicts** (overlapping/competing intent): do NOT auto-merge.
  Present the best-shot merge strategy and the competing hunks for human
  decision.

### 5. Push
```bash
git push
```
