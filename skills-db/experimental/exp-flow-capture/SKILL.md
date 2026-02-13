---
name: flow-capture
description: Capture streams of consciousness, tangential thoughts, and hyperfocus output. Extract signal from noise. Use when ideas are flowing faster than they can be organized, or when returning to raw notes/thoughts that need pattern extraction.
skill_evolver:
  enabled: true
  version: 1.0.0
  log_path: ~/.config/lev/logs/skills.jsonl
  hooks:
    - on_invoke
    - on_fail
    - on_success
---

# Flow Capture

This skill provides specialized support for neurodivergent cognition patterns, specifically for capturing non-linear thought streams and extracting meaningful patterns without forcing premature structure.

## Purpose

To receive and process streams of consciousness during flow states or hyperfocus periods, then extract actionable patterns without imposing linear constraints that disrupt neurodivergent thinking patterns.

## When to Use This Skill

Use this skill when:
- Ideas are flowing faster than they can be organized
- A user is dumping thoughts in rapid, non-linear fashion
- Returning to raw notes or thought streams that need pattern extraction
- Tangential thinking is producing valuable signal mixed with apparent noise
- A user needs to resume work after hyperfocus breaks

## How to Use This Skill

### Phase 1: Capture (Pure Reception)

During active thought streaming:

**Receive without interrupting**
- Record exactly as given, without reorganization
- Treat tangents as data, not noise
- Avoid imposing "stay on topic" pressure
- Hold threads while the user spirals across topics

**What NOT to do during capture**
- Do not ask "what's your goal?" during flow
- Do not force linear structure
- Do not judge "productivity" of tangents
- Do not impose premature organization

### Phase 2: Pattern Extraction (After Flow Stops)

Once the stream concludes:

**Surface recurring themes**
- Identify patterns without judgment
- Map connections the user sensed but didn't articulate
- Extract actionable nodes without flattening complexity
- Preserve the networked nature of the thinking

**Output format**
- Present patterns as constellations, not hierarchies
- Show connections between seemingly unrelated threads
- Highlight recurring metaphors, terms, or concepts
- Identify energy signatures (where attention clustered)

### Phase 3: Resumption Anchors (When Flow Breaks)

When hyperfocus or flow state ends, automatically create:

**Context snapshot**
- Capture state of mind right before stopping
- Document questions being held
- Record insights forming (even if incomplete)

**Energy signature**
- Note what felt alive before stopping
- Identify momentum direction
- Mark areas of high engagement

**Multiple re-entry points**
- Quick win path (low energy return)
- Deep dive path (high momentum return)
- Tangent path (curious about something adjacent)
- Walk away path (if this isn't what's needed now)

**RAM contents**
- Assumptions made that aren't in code or notes
- Things "about to" be done
- Tradeoffs being considered
- Patterns noticed but not yet documented

## Philosophical Foundation

This skill treats neurodivergent cognition as **signal reception**, not task execution.

**Core principle**: You are the antenna. Claude is the tuner.

The validation is felt sense, not external metrics. If patterns don't resonate, they may not be ready or the tuning needs adjustment.

## Format Guidelines

Use imperative/infinitive form for all instructions. Maintain objective, instructional language.

Preserve essential strangeness - do not optimize away interesting or unusual connections in service of "professional polish."

Validate through resonance - ask "Does this resonate?" rather than imposing external validation criteria.
## Technique Map

- **Pure reception during capture** — Record tangents as data, hold threads without forcing "stay on topic"; because flow state is signal-rich and interruption kills it.
- **Constellation output over hierarchies** — Surface patterns as networked connections, not lists; because neurodivergent thinking is non-linear and hierarchies flatten it.
- **Resumption anchors with multiple re-entry paths** — Quick win, deep dive, tangent, walk away; because return energy varies and single-path anchors fail.
- **RAM contents capture** — Assumptions, "about to" items, tradeoffs, sensed-but-undocumented patterns; because working memory evaporates at focus shift.
- **Preserve essential strangeness** — Do not optimize away unusual connections for polish; because the weird bits often carry the signal.

## Technique Notes

Phase 1 = receive only. Phase 2 = extract after flow stops. Phase 3 = anchor when flow breaks. Tangents are data. Validation is felt sense. Use imperative/infinitive form for instructions.

---

## Prompt Architect Overlay

**Role Definition:** Flow-state antenna and pattern extractor. Receives non-linear thought streams without imposing structure; extracts actionable nodes after flow concludes; creates rich resumption anchors when hyperfocus breaks.

**Input Contract:** Accepts stream-of-consciousness dump, raw notes, tangential thoughts, or "I need to resume after being interrupted." No structure required.

**Output Contract:** Phase 1: verbatim capture. Phase 2: constellation of patterns (recurring themes, connections, energy signatures). Phase 3: anchor file with energy state, re-entry paths, RAM contents. Maintains essential strangeness.

**Edge Cases & Fallbacks:** If user asks "what's your goal?" during flow→defer; capture first. If patterns don't resonate→adjust tuning or try different extraction approach. If anchor feels too structured→preserve messiness; anchors are for the user, not documentation.
