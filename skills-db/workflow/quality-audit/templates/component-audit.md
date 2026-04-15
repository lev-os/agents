# Template: Component Audit

Per-item evaluation checklist for UI components. Covers visual fidelity,
code quality, accessibility, and standards compliance.

## Categories

### VISUAL (weight: 0.3)
- [ ] Renders correctly in light mode
- [ ] Renders correctly in dark mode
- [ ] Layout matches design specification
- [ ] Spacing and alignment are consistent
- [ ] Typography uses design tokens (not hardcoded sizes)
- [ ] Colors use theme tokens (no raw Color literals)
- [ ] Interactive states visible (hover, pressed, disabled, focused)

### CODE QUALITY (weight: 0.3)
- [ ] Uses @Observable (not ObservableObject) where applicable
- [ ] No deprecated API usage (.foregroundColor, .cornerRadius, NavigationView)
- [ ] File length under 500 LOC
- [ ] Follows project naming conventions
- [ ] No hardcoded strings (uses localization or constants)
- [ ] Error states handled gracefully

### ACCESSIBILITY (weight: 0.2)
- [ ] All interactive elements have .accessibilityIdentifier
- [ ] Meaningful .accessibilityLabel on icons and images
- [ ] Supports Dynamic Type (no .font(.system(size:)))
- [ ] VoiceOver navigation order is logical
- [ ] Sufficient color contrast (4.5:1 for text, 3:1 for large text)

### STANDARDS COMPLIANCE (weight: 0.2)
- [ ] Matches documented component API in standards doc
- [ ] Props/parameters match expected interface
- [ ] Storybook/preview coverage exists
- [ ] Known gaps documented (not silently missing)

## Verdict Rules

- **PASS**: All categories score >= 80% AND no P0 issues
- **NEEDS_WORK**: Any category < 80% OR any P0/P1 issue present
- **BLOCKED**: Evidence capture failed OR prerequisites missing
