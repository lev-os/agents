# Template: Generic Audit

Bare scaffold for custom domain audits. Replace the placeholder categories
with your domain-specific criteria.

## Categories

### CATEGORY_1 (weight: 0.5)
- [ ] Criterion A: {describe what to check}
- [ ] Criterion B: {describe what to check}
- [ ] Criterion C: {describe what to check}

### CATEGORY_2 (weight: 0.5)
- [ ] Criterion A: {describe what to check}
- [ ] Criterion B: {describe what to check}
- [ ] Criterion C: {describe what to check}

## Verdict Rules

- **PASS**: All categories meet acceptance threshold
- **NEEDS_WORK**: One or more categories below threshold
- **BLOCKED**: Cannot evaluate (missing evidence or prerequisites)

## Customization

Replace categories and criteria with your domain-specific checklist.
Adjust weights to reflect relative importance. Add more categories as needed.
Custom verdict labels can be set via `reporting.verdict_taxonomy` in the config.
