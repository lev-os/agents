# Antigravity Skills Archive Index

**Fetched:** 2026-02-10
**Source:** `sickn33/antigravity-awesome-skills` (GitHub)

## Production Installation (4/6)

These skills are installed and ready for immediate use:

- `/docker-expert` — Docker containerization expert
- `/clean-code` — Robert C. Martin's Clean Code principles
- `/tdd-workflow` — Test-Driven Development RED-GREEN-REFACTOR cycle
- `/github-workflow-automation` — GitHub PR/issue/CI automation

## Workshop Review (2/6)

These skills are archived for review before production installation:

- `ui-ux-pro-max/SKILL.md` — Multi-platform UI/UX design (50 styles, 21 palettes, 9 stacks)
- `mobile-design/SKILL.md` — Mobile-first doctrine for iOS/Android/React Native/Flutter

## File Manifest

```
~/.agents/skills-db/_workshop/antigravity/fetched/
├── docker-expert/
│   └── SKILL.md (14 KB, 408 lines)
├── clean-code/
│   └── SKILL.md (4.3 KB, 94 lines)
├── tdd-workflow/
│   └── SKILL.md (2.7 KB, 149 lines)
├── github-workflow-automation/
│   └── SKILL.md (21 KB, 846 lines)
├── ui-ux-pro-max/
│   └── SKILL.md (13 KB, 351 lines)
├── mobile-design/
│   └── SKILL.md (9.1 KB, 284 lines)
└── INDEX.md (this file)
```

## Installation Commands

To promote ui-ux-pro-max or mobile-design to production:

```bash
# Promote ui-ux-pro-max
mkdir -p ~/.agents/skills/ui-ux-pro-max
cp ~/.agents/skills-db/_workshop/antigravity/fetched/ui-ux-pro-max/SKILL.md ~/.agents/skills/ui-ux-pro-max/

# Promote mobile-design
mkdir -p ~/.agents/skills/mobile-design
cp ~/.agents/skills-db/_workshop/antigravity/fetched/mobile-design/SKILL.md ~/.agents/skills/mobile-design/
```

## Quality Notes

- **All skills well-formed:** Consistent metadata, clear descriptions, focused scope
- **Enterprise-ready:** github-workflow-automation is the most comprehensive (846 lines)
- **Multi-platform:** ui-ux-pro-max covers React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter
- **Principles-driven:** mobile-design teaches constraints over fixed layouts
- **No failures:** 100% fetch success rate via GitHub API

## Next Steps

1. Begin using production skills in automation workflows
2. Schedule review of ui-ux-pro-max against KinglyAssistant SwiftUI ecosystem
3. Evaluate mobile-design for iOS/macOS mobile-first integration
4. Set up upstream monitoring for `sickn33/antigravity-awesome-skills` updates
