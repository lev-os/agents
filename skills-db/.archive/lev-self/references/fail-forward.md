# Fail-Forward Protocol

When something fails, extract maximum learning value.

## The 5-Step Protocol

### 1. Capture (What happened?)
```yaml
failure:
  timestamp: "2026-01-17T00:00:00Z"
  error: "exact error message"
  context: "what was being attempted"
  stack: "relevant stack trace"
```

### 2. Root Cause (Why?)
Apply 5 Whys:
1. Why did the error occur? → Direct cause
2. Why was that possible? → Missing guard
3. Why wasn't it caught? → Gap in validation
4. Why does that gap exist? → Design assumption
5. Why was that assumed? → Root cause

### 3. Proposal (How to prevent?)
```yaml
prevention:
  type: skill-patch | config | guard | test
  target: specific file or system
  change: what to add/modify
  verification: how to confirm fix works
```

### 4. Confidence (How sure?)
- **High (≥80%)**: Clear root cause, verified fix
- **Medium (50-79%)**: Probable cause, untested fix
- **Low (<50%)**: Hypothesis only, needs investigation

### 5. Apply (With rollback plan)
```bash
lev learn apply <proposal-id> --dry-run  # Preview
lev learn apply <proposal-id>            # Apply
lev learn rollback <proposal-id>         # If issues
```

## Common Root Causes

| Symptom | Likely Cause | Fix Pattern |
|---------|--------------|-------------|
| Timeout | Missing timeout config | Add explicit timeout |
| Missing file | Path assumption | Check existence first |
| Parse error | Format change | Version validation |
| Permission denied | Wrong user/path | Check permissions |
