# README Quick Reference

One-page cheatsheet. Print this.

---

## Golden Structure

```
1. HERO         → illustration + badges + one-liner + curl install
2. TL;DR        → Problem + Solution + Feature table
3. EXAMPLE      → 5-10 commands showing core workflow
4. REFERENCE    → Philosophy, Comparison, Install, Commands, Config, Architecture
5. SUPPORT      → Troubleshooting, Limitations, FAQ, Contributions, License
```

---

## 8 Critical Rules

| # | Rule | Implementation |
|---|------|----------------|
| 1 | Value before installation | TL;DR → Quick Example → Installation |
| 2 | Curl one-liner above fold | `curl -fsSL ... \| bash` in hero |
| 3 | Examples for every claim | Feature claim → code block |
| 4 | Tables over prose | Comparisons, features, options |
| 5 | Honest limitations | Dedicated section, no hiding |
| 6 | 3+ install methods | curl + pkg manager + source |
| 7 | Architecture diagrams | ASCII art for complex tools |
| 8 | Top 5 errors documented | Troubleshooting mandatory |

---

## Section Checklist

```
□ Hero: illustration, badges, one-liner, curl
□ TL;DR: problem, solution, feature table
□ Quick Example: 5-10 commands
□ Design Philosophy: 3-5 principles
□ Comparison: table vs 2+ alternatives
□ Installation: 3+ methods
□ Quick Start: numbered steps
□ Commands: every command + example
□ Configuration: full example + comments
□ Architecture: ASCII diagram
□ Troubleshooting: 5+ errors + fixes
□ Limitations: honest list
□ FAQ: 5+ questions
□ Contributions: EXACT policy text
□ License
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Installation first | TL;DR first |
| "This is a tool that..." | "Solves X by doing Y" |
| Screenshots | ASCII + code blocks |
| Abstract claims | Concrete examples |
| Hide limitations | Dedicated section |
| Single install method | 3+ methods |
| Skip troubleshooting | Top 5 errors |

---

## Badge Order

```markdown
[![CI](...)][ci] [![License](...)][license] [![Version](...)][version] [![Downloads](...)][downloads]
```

1. CI status (most important)
2. License
3. Version/Release
4. Package registry
5. Optional: coverage, downloads

---

## Hero Template

```markdown
# tool-name

<div align="center">
  <img src="illustration.webp" alt="tool-name">
</div>

<div align="center">

[![CI](badge)](link) [![License](badge)](link)

</div>

One-sentence description with key differentiator.

<div align="center">

```bash
curl -fsSL https://raw.githubusercontent.com/user/repo/main/install.sh | bash
```

</div>
```

---

## TL;DR Template

```markdown
## TL;DR

**The Problem**: [Specific pain point]

**The Solution**: [What this does]

### Why Use tool-name?

| Feature | Benefit |
|---------|---------|
| **Feature 1** | Concrete benefit |
| **Feature 2** | Quantified if possible |
```

---

## Comparison Template

```markdown
| Feature | tool-name | Alt A | Alt B |
|---------|-----------|-------|-------|
| Feature 1 | ✅ | ⚠️ | ❌ |
| Speed | ✅ <10ms | 🐢 ~500ms | ✅ |
| Setup | ✅ ~10s | ❌ Hours | ⚠️ |
```

---

## Contributions Section (MANDATORY)

```markdown
> *About Contributions:* Please don't take this the wrong way, but I do not accept outside contributions for any of my projects. I simply don't have the mental bandwidth to review anything, and it's my name on the thing, so I'm responsible for any problems it causes; thus, the risk-reward is highly asymmetric from my perspective. I'd also have to worry about other "stakeholders," which seems unwise for tools I mostly make for myself for free. Feel free to submit issues, and even PRs if you want to illustrate a proposed fix, but know I won't merge them directly. Instead, I'll have Claude or Codex review submissions via `gh` and independently decide whether and how to address them. Bug reports in particular are welcome. Sorry if this offends, but I want to avoid wasted time and hurt feelings. I understand this isn't in sync with the prevailing open-source ethos that seeks community contributions, but it's the only way I can move at this velocity and keep my sanity.
```

---

## File Links

| Need | Reference |
|------|-----------|
| Core templates | [CORE-TEMPLATES.md](CORE-TEMPLATES.md) |
| Extended templates | [EXTENDED-TEMPLATES.md](EXTENDED-TEMPLATES.md) |
| All badges | [BADGES.md](BADGES.md) |
| AGENTS.md format | [AGENTS-MD.md](AGENTS-MD.md) |
| Example READMEs | [EXAMPLES.md](EXAMPLES.md) |
| All prompts | [PROMPTS.md](PROMPTS.md) |
