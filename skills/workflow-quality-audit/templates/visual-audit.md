# Template: Visual Audit

Screenshot-focused evaluation. Use when the primary concern is how things look,
not how the code is structured.

## Categories

### VISUAL FIDELITY (weight: 0.5)
- [ ] Matches design mockup / wireframe
- [ ] Correct in light mode
- [ ] Correct in dark mode
- [ ] Spacing and alignment consistent with grid
- [ ] Typography hierarchy is clear
- [ ] Color palette matches brand tokens
- [ ] No clipping, overflow, or layout breaks

### STORYBOOK COVERAGE (weight: 0.3)
- [ ] Preview/storybook page exists for this item
- [ ] All major states represented (empty, loading, populated, error)
- [ ] Both color schemes shown
- [ ] Interactive variants demonstrated

### CODE STRUCTURE (weight: 0.2)
- [ ] View uses theme tokens (not hardcoded colors/sizes)
- [ ] Responsive to container size changes
- [ ] No deprecated rendering APIs

## Verdict Rules

- **PASS**: Visual fidelity >= 85% AND storybook coverage exists
- **NEEDS_WORK**: Visual issues found OR missing storybook coverage
- **BLOCKED**: Cannot capture screenshot or item not renderable
