---
name: ubs-bug-scan
description: |
  [WHAT] Static analysis gate using Ultimate Bug Scanner (UBS) — multi-language AST-level bug detection.
  [HOW] Runs `ubs` scoped to changed/staged files, parses findings by severity, fixes critical issues inline.
  [WHEN] Before every commit. On PR review. When asked to scan for bugs, static analysis, or code quality.
  [WHY] Catches resource leaks, null derefs, type narrowing gaps, and concurrency bugs that linters miss.
skill_type: workflow
related_skills: [pr-review, security-best-practices, clean-code]
allowed_tools: Read, Bash, Glob, Grep
user_invocable: true
---

# UBS Bug Scan

## Prerequisites

```bash
# Install UBS
brew install dicklesworthstone/tap/ubs

# Verify
ubs --version
```

If `command -v ubs` fails, emit the install one-liner above and **stop**.

---

## Workflow

### 1. Determine Scope

Pick the narrowest scope that covers the work:

| Situation | Command | Speed |
|-----------|---------|-------|
| Pre-commit (staged files) | `ubs --staged` | <1s |
| Working tree changes | `ubs --diff` | <1s |
| Specific files | `ubs src/file.ts src/other.ts` | <1s |
| Full project | `ubs .` | ~30s |

**Speed tip:** Always scope to changed files. Full-project scans are for baselines only.

### 2. Run Scan

```bash
# Agent-parseable output (JSON)
ubs --staged --format=json --ci

# Token-efficient output (text, truncated)
ubs --staged --ci 2>&1 | tail -40

# Language-scoped
ubs --staged --only=js,python --ci
```

### 3. Parse Output

Findings have three severities:

| Severity | Action | Exit code |
|----------|--------|-----------|
| **critical** | Must fix before commit | non-zero |
| **warning** | Should fix, judgment call | non-zero with `--fail-on-warning` |
| **info** | Optional improvement | zero |

JSON output structure:
```json
{
  "summary": { "critical": 0, "warning": 1, "info": 3 },
  "findings": [
    {
      "file": "src/foo.ts",
      "line": 42,
      "severity": "warning",
      "category": "resource-lifecycle",
      "message": "File handle opened but never closed"
    }
  ]
}
```

### 4. Fix Findings

For each finding:
1. Navigate to `file:line`
2. Verify it's not a false positive (check surrounding context)
3. Fix the root cause (not just the symptom)
4. Re-run `ubs <file>` to confirm the fix
5. Repeat until exit 0

### 5. Commit Gate

```bash
# Golden rule: run before every commit
ubs --staged --ci
# Exit 0 = safe to commit
# Exit >0 = fix findings first
```

---

## Useful Flags

| Flag | Purpose |
|------|---------|
| `--format=json` | Machine-parseable output |
| `--format=sarif` | SARIF for IDE integration |
| `--ci` | Stable timestamps, CI-friendly |
| `--only=js,python` | Restrict to specific languages |
| `--exclude=rust` | Skip specific languages |
| `--category=resource-lifecycle` | Focus on category packs |
| `--fail-on-warning` | Treat warnings as failures |
| `--staged` | Scan only git-staged files |
| `--diff` | Scan only modified files (working tree vs HEAD) |
| `--comparison=baseline.json` | Diff against a baseline |
| `--html-report=report.html` | Generate shareable HTML report |
| `--suggest-ignore` | Show directories to add to `.ubsignore` |

---

## Anti-Patterns

- Running `ubs .` on every commit (slow, noisy)
- Ignoring critical findings with `UBS_SKIP=1`
- Fixing symptoms instead of root causes
- Not re-running after fixes to confirm resolution

---

## Reference

See `references/ubs-quickref.md` for condensed command reference and severity guide.
