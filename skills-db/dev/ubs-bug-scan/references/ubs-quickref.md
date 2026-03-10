# UBS Quick Reference

## Commands

```bash
# Pre-commit (fastest)
ubs --staged --ci

# Working tree changes
ubs --diff --ci

# Specific files
ubs src/foo.ts src/bar.ts

# Full project baseline
ubs . --format=json --ci --report-json=ubs-baseline.json

# Language-scoped
ubs --staged --only=js,python,rust --ci

# Category-focused
ubs --staged --category=resource-lifecycle --ci

# Diff against baseline
ubs . --format=json --ci --comparison=ubs-baseline.json

# HTML report
ubs . --html-report=ubs-report.html

# Doctor (validate modules)
ubs doctor --fix
```

## Output Parsing (JSON)

```bash
# Get summary counts
ubs --staged --format=json --ci | jq '.summary'

# Get critical findings only
ubs --staged --format=json --ci | jq '[.findings[] | select(.severity == "critical")]'

# Get findings for a specific file
ubs --staged --format=json --ci | jq '[.findings[] | select(.file | contains("src/foo.ts"))]'
```

## Severity Guide

| Severity | Meaning | Action |
|----------|---------|--------|
| `critical` | Likely bug: null deref, resource leak, data race | Must fix |
| `warning` | Potential bug: unchecked return, missing error handling | Should fix |
| `info` | Style/improvement: unused variable, redundant check | Optional |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No critical issues (safe to commit) |
| >0 | Critical issues found (fix before commit) |

With `--fail-on-warning`: warnings also produce non-zero exit.

## Ignore Patterns

Create `.ubsignore` at project root (gitignore syntax):

```
node_modules/
dist/
*.generated.ts
vendor/
```

## Environment Variables

| Variable | Effect |
|----------|--------|
| `UBS_SKIP` | Skip UBS entirely (set to any value) |
| `UBS_STRICT_MISSING` | Fail if ubs binary not installed |
| `UBS_ENABLE_AUTO_UPDATE` | Enable auto-update checks |

## Supported Languages

js, python, cpp, rust, golang, java, ruby, swift, kotlin (auto-detected)
