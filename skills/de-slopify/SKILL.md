---
name: de-slopify
description: >-
  Remove telltale signs of AI-generated "slop" writing. Use when polishing READMEs,
  docs, marketing copy, or public-facing text, or when text "sounds like ChatGPT".
---

<!-- TOC: THE EXACT PROMPT | Core Insight | High-Signal Tells | Judgment Calls | Red Herrings | Examples | Workflow | Reference Index -->

# De-Slopify — Remove AI Writing Artifacts

> **Core Insight:** You can't do this with regex or a script. It requires manual, systematic review of each line. Slop has a mechanism: the text becomes simultaneously less specific and more exaggerated — rare concrete facts get smoothed into generic important-sounding claims. So the fix is never just deleting tics; it's reinstating the concrete detail the slop displaced. Human writers use most of these devices intentionally and sparingly; the problem is density and reflex, not any single occurrence.

## THE EXACT PROMPT — Full De-Slopify

```
I want you to read through the complete text carefully and look for any telltale
signs of "AI slop" style writing; one big tell is the use of emdash. You should
try to replace this with a semicolon, a comma, or just recast the sentence
accordingly so it sounds good while avoiding emdash. This applies to emdashes
used as prose punctuation only: leave dash/minus characters alone when they are
doing non-prose work, such as in math formulas, code, CLI flags, numeric ranges,
or tables.

Also, you want to avoid certain telltale writing tropes:
- Setup-reversal copy ("Four steps, and only one of them is yours." /
  "Everything about billing changed. Your invoice didn't.")
- Negative parallelism ("It's not [just] XYZ, it's ABC")
- Clickbait lead-ins ("Here's why", "Here's the thing")
- AI vocabulary clusters (delve, pivotal, tapestry, intricate, underscores,
  seamless, robust, vibrant, leverage) and copula avoidance ("serves as",
  "marks a", "boasts" instead of plain "is"/"has")
- Significance inflation ("marks a pivotal moment", trailing "-ing" commentary
  clauses like "highlighting its importance")
- Bullet lists of "- **Snappy Label:** text" where prose would read better
- Filler: paragraphs that say in four sentences what fits in one
Basically, anything that sounds like the kind of thing an LLM would write
disproportionately more commonly than a human writer and which sounds
inauthentic/cringe.

And you can't do this sort of thing using regex or a script, you MUST manually
read each line of the text and revise it manually in a systematic, methodical,
diligent way. Use ultrathink.
```

## THE EXACT PROMPT — Quick Version

```
Review this text and remove AI slop patterns: emdashes used as prose
punctuation (not dashes in math, code, or ranges), setup-reversal copy, "It's not X, it's Y" formulas, "Here's
why" lead-ins, AI vocabulary (delve/pivotal/tapestry/underscores/seamless),
"serves as" instead of "is", trailing "-ing" significance clauses, bold-label
bullet lists, and filler. Recast sentences to sound naturally human; restore
concrete specifics where slop replaced them. Use ultrathink.
```

---

## High-Signal Tells (fix on sight)

| Pattern | Example | Fix |
|---------|---------|-----|
| **Setup-reversal copy (paraprosdokian)** | "Four steps, and only one of them is yours." / "A thousand integrations, and you'll only ever click one." / "Everything about billing changed. Your invoice didn't." | State what the tool does plainly. No dramatic pivot. |
| **Negative parallelism** | "It's not just a linter—it's a complete system" / "not X, but Y" / "no X, no Y, just Z" | Say what it is; drop the strawman denial |
| **AI vocabulary clusters** | delve, tapestry, intricate, pivotal, robust, seamless, vibrant, leverage, testament, landscape, spine, seam, smoke-test (several together) | Plain synonyms; density is the signal |
| **Copula avoidance** | "serves as", "stands as", "marks a", "boasts/features/offers" for has, "holds the distinction of being" | "is" / "has" |
| **Significance inflation** | "marks a pivotal moment", "underscores the importance", trailing ", highlighting..." / ", emphasizing..." / ", ensuring..." clauses | Cut the commentary; keep or add the fact |
| **"Here's why" family** | "Here's why it matters:", "Here's the thing", "The solution? Simpler than you think." | Explain directly, or delete |
| **Emdash overuse** | `—` as prose punctuation (never dashes in math, code, or ranges) | Comma, semicolon, colon, or split the sentence |
| **Bold-label bullets** | `- **Blazing Fast:** processes files in ms` | Prose, or plain bullets |
| **Forced enthusiasm** | "Let's dive in!", "We're thrilled to announce" | Just start / just announce |
| **Reflexive triads** | "Fast, efficient, and reliable" / third item padded with "and other X" | Keep the one or two claims that are true and specific |
| **Vapid transitions** | "As technology continues to evolve", "In today's fast-paced world", sentence-initial "Additionally," | Delete or replace with a real transition |

## Judgment Calls (fix when dense, keep when earned)

- **Filler**: a paragraph whose content fits in one sentence, or that has no
  discernible claim. Compress or delete; this is the essence of slop.
- **Generic analogies**: plausible but unconsidered metaphors ("every chord is a
  puzzle piece that clicks into a song"). Delete or make them specific.
- **Hedges** ("It's worth noting...", "Keep in mind..."): delete unless the caveat changes reader behavior.
- **Formatting slop**: bold scattered without emphasis logic, emoji bullets (✅🎯🚀), Title Case Headings, heading-only sections, rules between every section, tables for prose, heavy bullet density.
- **Monotone rhythm**: every sentence the same length, unnaturally uniform tense/POV. Vary it.
- **Elegant variation**: rotating synonyms for a key term. Technical writing should repeat the term.
- **Weasel attribution**: "Experts argue", "Industry reports suggest". Name the source or cut the claim.
- **The challenges formula**: "Despite X, faces several challenges... Future outlook..." Cut the arc; keep one real limitation.

## Red Herrings (do NOT "fix")

- Perfect grammar and absent typos — humans have spell-check too
- Absence of contractions — may be house style or non-native phrasing
- Academic vocabulary alone — "ascertain" in one spot isn't slop; a cluster of AI-vocabulary words is
- Dash characters outside prose — minus signs in math formulas, dashes in code or CLI flags, en dashes in numeric ranges, table syntax. Only prose-punctuation emdashes are the tell
- AI-detector tool output — these tools false-positive constantly; the review is manual judgment, in both directions

---

## Before/After Examples

**Setup-reversal copy:**
```
Before: Ten features. Zero headaches.
After:  Includes ten features for managing billing, invoicing, and usage tracking.
```

**Emdash + negative parallelism:**
```
Before: It's not just a linter—it's a complete code quality system.
After:  A code quality system that covers linting, formatting, and CI checks.
```

**"Here's why":**
```
Before: We chose Rust for this component. Here's why: performance matters.
After:  We chose Rust for this component because performance matters.
```

**Significance inflation (restore the specific fact):**
```
Before: The v2 release marks a pivotal moment, underscoring our commitment to reliability.
After:  v2 fixes the three crash bugs reported since March.
```

**Copula avoidance:**
```
Before: The CLI serves as the primary entry point and boasts a robust plugin system.
After:  The CLI is the primary entry point and has a plugin system.
```

**Forced enthusiasm:**
```
Before: Let's dive in! We're excited to help you get up and running.
After:  Install the tool and run your first command in under a minute.
```

---

## Workflow

- [ ] Read the entire text once for register: does it sound like ad copy or a lecture?
- [ ] Line-by-line pass: mark every high-signal tell (table above)
- [ ] Density pass: judgment-call patterns — fix only where they cluster
- [ ] Specificity pass: wherever you cut inflated claims, reinstate concrete facts
- [ ] Reread the result; it should sound like a competent engineer explaining, not a brand

## Why Manual Review is Required

1. **Context matters** — sometimes an emdash or triad is actually the right choice
2. **Recasting sentences** — often the fix isn't substitution but rewriting
3. **Restoring specifics** — a script can delete "pivotal" but can't supply the missing fact
4. **Tone consistency** — need to maintain one voice throughout

## When to De-Slopify

- Before publishing a README
- Before releasing documentation
- After AI-assisted writing sessions
- During documentation reviews

## What NOT to Fix

- **Technical accuracy** — don't sacrifice correctness for style
- **Necessary structure** — headers and lists that organize real content are fine
- **Clear explanations** — being thorough isn't slop; filler is saying nothing at length
- **Code examples** — focus on prose, not code
- **Earned devices** — a device used once, deliberately, for real effect can stay

---

## Reference Index

| Topic | Reference |
|-------|-----------|
| Complete pattern catalog with fixes | [PATTERNS.md](references/PATTERNS.md) |
