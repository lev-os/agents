---
description: Unified visual explainer — generate diagrams, comparisons, diff reviews, plan reviews, project recaps, fact checks, slides, and implementation plans as beautiful HTML pages
---
Load the visual-explainer skill (`~/.agents/skills/visual-explainer/SKILL.md`). Read it fully — the Command Interface section defines how to parse these args.

**Parse `$@`:**

1. **Extract quality mode.** Check if the last token is `publish` or `all`. If so, pop it and set the quality mode. Otherwise, quality mode is `default` (local only).

2. **Extract type.** Match the first token (case-insensitive) against:
   - `diagram` / `diag` → freeform diagram (read `./references/css-patterns.md`, pick a template)
   - `comparison` / `compare` / `tradeoff` / `vs` → tradeoff analysis (read `./templates/data-table.html`, follow "Comparison / Tradeoff Analysis" in SKILL.md)
   - `diff-review` / `diff` / `review` → visual diff review (follow the diff-review workflow in SKILL.md references)
   - `plan-review` / `plan` → plan vs codebase analysis (follow the plan-review workflow)
   - `project-recap` / `recap` → mental model snapshot (follow the project-recap workflow)
   - `fact-check` / `check` / `verify` → verify claims against code (follow the fact-check workflow)
   - `slides` / `deck` / `presentation` → slide deck (read `./references/slide-patterns.md` and `./templates/slide-deck.html`)
   - `visual-plan` / `spec` / `implementation` → implementation plan (follow the visual-plan workflow)
   - `decision` / `feedback` / `decide` / `poll` → interactive decision capture (read `./templates/decision.html`, follow "Decision / Feedback Capture" in SKILL.md)
   - No match → treat entire arg string as a `diagram` topic

3. **Context args.** Everything between the type token and quality mode is the topic/context.

**Route to the appropriate workflow:**

For each type, read the corresponding reference files per SKILL.md's Structure section, then follow that type's workflow. The type-specific prompt files in `./prompts/` contain detailed instructions — read the matching one:

| Type | Reference prompt |
|------|-----------------|
| diagram | `./prompts/generate-web-diagram.md` |
| comparison | Use SKILL.md "Comparison / Tradeoff Analysis" section |
| diff-review | `./prompts/diff-review.md` |
| plan-review | `./prompts/plan-review.md` |
| project-recap | `./prompts/project-recap.md` |
| fact-check | `./prompts/fact-check.md` |
| slides | `./prompts/generate-slides.md` |
| visual-plan | `./prompts/generate-visual-plan.md` |
| decision | `./prompts/generate-decision.md` |

Read the matching prompt file for detailed instructions on data gathering, verification, and diagram structure. Then follow the visual-explainer skill workflow (Think → Structure → Style → Deliver).

**Quality mode execution** (at Deliver step):

- `default` — standard quality checks, open in browser, done
- `all` — full quality gate per SKILL.md's Deliver section quality table. Fix issues before showing the user.
- `publish` — full quality gate + publish via here.now. Run `./skills/here-now/scripts/publish.sh ~/.agents/diagrams/<filename>.html --client visual-explainer`. Return the live URL.

Ultrathink.

$@
