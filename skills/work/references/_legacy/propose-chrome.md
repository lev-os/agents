# PROPOSE Dashboard Chrome

Display conventions for the PROPOSE stage output. Not a gate — purely presentation.

## Dashboard Footer

Every PROPOSE output ends with a structured footer. The agent renders it as markdown; the user responds with a number or letter shortcut.

```
---
🔨 **Work:** {stage} | 🎯 {layer} | 📊 Guard: {score}%

**Skills loaded:** {loaded_list}
**Available:** {available_count} more via skills-db

🪄 **Next:**
1. [s] Skills — browse/load from skills-db
2. [r] Research — deepen with lev-research
3. [p] Prior art — review beads and artifacts
4. Proceed to SPEC
5. All of the above
6. ⬅️ Back to DISCOVER
```

Shortcut behavior:
- [s] → `lev-skill resolve "{topic}" --json`, present results, offer to cat SKILL.md
- [r] → route to lev-research with current context
- [p] → `br search "{topic}"` + `cass search "{topic}"`

## SPEC Promotion Path

When a spec passes validation (`gate:propose-spec`) and template questions are answered, identify the promotion target:

1. **Start:** `.lev/pm/specs/spec-{topic}.md` (Ephemeral Draft)
2. **Review:** Gate passes.
3. **Promote:** Move to `docs/specs/spec-{module}.md` (Canonical)
   - If module exists: Update existing spec.
   - If new module: Create new spec file.
   - Naming: Use `spec-{module}.md` for core, `spec-{module}-{slug}.md` for extensions.

## FlowMind Naming Structure & Config Keys

The `work` skill recognizes specific configuration keys for identifying specs and promoting them:

| Key | Value Pattern | Purpose |
|-----|---------------|---------|
| `naming_structure` | `flowmind` | Enforce `spec-{module}.md` naming |
| `filename_mask` | `core-*-mask` | Regex for validating core filenames |
| `spec_target` | `docs/specs/` | Target directory for promotion |

Example Config (`.lev/config.yaml`):
```yaml
work:
  naming_structure: flowmind
  filename_mask: "spec-.*\\.md"
  spec_target: "docs/specs/"
```
