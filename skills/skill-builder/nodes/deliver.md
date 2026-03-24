# Deliver: Catalog and Report

Final checklist:
- [ ] dna.yaml exists and `flow validate` passes
- [ ] All nodes/*.md files present
- [ ] Security scan passed
- [ ] At least 3 BDD scenarios tested
- [ ] Anti-patterns table has 5+ entries
- [ ] Under 300 lines for main skill content

Install location:
- A/B grade → `~/.agents/skills/{name}/`
- C grade → `~/.agents/skills-db/_todo/{name}/`
- D grade → `~/.agents/skills-db/.archive/{name}/`

Activation to ~/.agents/skills/ happens ONLY with user confirmation.

Produce a report:
```
─── Skill Builder Report ───
Skill: {name}
Nodes: {count}
Validation: {pass/fail}
Security: {pass/warn/fail}
BDD Scenarios: {passed}/{total}
Anti-patterns: {count}
Location: {installed_path}
────────────────────────────
```
