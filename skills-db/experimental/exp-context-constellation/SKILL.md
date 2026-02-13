---
name: context-constellation
description: Map non-linear connections across files, thoughts, and projects. Reveal hidden patterns in seemingly unrelated work. Use when feeling scattered, when working across multiple domains, or when sensing connections but unable to articulate them.
skill_evolver:
  enabled: true
  version: 1.0.0
  log_path: ~/.config/lev/logs/skills.jsonl
  hooks:
    - on_invoke
    - on_fail
    - on_success
---

# Context Constellation

This skill provides specialized support for mapping work as constellations rather than hierarchies, revealing patterns across domains that neurodivergent cognition naturally senses but struggles to articulate.

## Purpose

To make visible the non-linear, networked connections that neurodivergent minds naturally perceive across files, thoughts, and projects - treating temporal proximity and conceptual proximity as independent dimensions.

## When to Use This Skill

Use this skill when:
- A user feels scattered across multiple projects or domains
- Work exists across seemingly unrelated files or contexts
- A user senses connections but cannot articulate them
- Context has been lost and needs reconstruction
- Abandoned work threads may connect to active projects

## How to Use This Skill

### Scan Mode: Comprehensive Context Mapping

**Temporal scan patterns**
- Recent files (last 7 days: heavy weight)
- Medium-term files (last 30 days: light weight)
- Do not assume recent = related

**Content sources to scan**
- Code files and embedded comments (thoughts in work)
- README fragments and half-written documentation
- Notes files and scratch documents
- Terminal history (exploration traces)
- Files opened but not edited (curiosity signals)
- Directories created but not filled (intention markers)

**What to look for**
- Unexpected connections between files
- Recurring metaphors or terms across domains
- Energy signatures (attention clustering patterns)
- Abandoned work that now has context
- Weak signals (touched once, almost explored)

### Pattern Revelation: Show Resonance, Not Hierarchy

**Present findings as constellation maps**
- Files that "feel related" often are (even across projects)
- Temporal proximity ≠ conceptual proximity
- Weak signals matter as much as strong ones
- Abandoned threads may connect to active work

**Connection types to surface**
- Shared terminology in unrelated contexts
- Parallel problem structures in different domains
- Similar approaches to unrelated challenges
- Recurring energy patterns (flow vs. friction zones)

**What NOT to do**
- Do not create "projects" or "categories"
- Do not impose hierarchical organization
- Do not force linear relationships
- Do not dismiss weak or unusual connections

### Context Recovery: Fragment-Based Reconstruction

When context is lost:

**Accept any fragment as starting point**
- Phrase, feeling, file name, partial thought
- Any signal, no matter how weak
- Trust that fragments connect to larger patterns

**Reconstruct the constellation**
- Find what the fragment belongs to
- Map connections radiating from it
- Show the energy field it exists within
- Present multiple possible contexts (not single "correct" one)

## Philosophical Foundation

This skill treats neurodivergent cognition as **pattern recognition across domains**, not hierarchical organization.

Neurodivergent minds naturally see connections that don't fit linear structures. This skill makes those connections visible without forcing them into hierarchies.

**Core principle**: Show resonance patterns and let the user feel which matter.

## Output Format

**Not**: "Here are your 3 projects organized by category"

**Instead**: "These files resonate around this energy... these share this metaphor... these show parallel structures..."

Then: silence. Allow the user to sense into the patterns.

Validation comes from felt sense - if patterns don't resonate, they may not be meaningful yet (or tuning needs adjustment).
## Technique Map

- **Temporal scan patterns** — Recent ≠ related; weight by recency but treat temporal and conceptual proximity as independent dimensions, because neurodivergent cognition naturally clusters by energy, not chronology.
- **Multi-source content scan** — Code, comments, README fragments, notes, terminal history, opened-but-not-edited files; because thoughts live in work traces, not just formal docs.
- **Constellation mapping over hierarchy** — Present files as resonant clusters, not categories; because hierarchies impose false structure and hide cross-domain connections.
- **Fragment-based reconstruction** — Accept any phrase, file, or partial thought as entry point; because lost context can be recovered from the weakest signal.
- **Silence after revelation** — Surface patterns then pause; because validation is felt sense, not agreement-seeking.

## Technique Notes

Trust temporal heaviness (7-day weight) but never assume recency = relevance. Weak signals matter as much as strong ones. Abandoned threads often connect to active work. Present multiple possible contexts, not a single "correct" one.

---

## Prompt Architect Overlay

**Role Definition:** Constellation mapper who surfaces non-linear connections across files, thoughts, and projects. Operates as pattern revealer—not organizer—embracing neurodivergent cognition's natural cross-domain sensing.

**Input Contract:** Accepts scattered work state, lost context, fragment phrases, file names, or "I sense connections but can't articulate them." No minimum structure required.

**Output Contract:** Constellation maps (resonance clusters, shared metaphors, parallel structures), multiple possible contexts for fragments, energy signatures. No hierarchical organization. Ends with silence for user to sense into patterns.

**Edge Cases & Fallbacks:** If no connections found→scan different sources (terminal history, half-read files). If user rejects patterns→treat as valid signal; try different scan zones or weaker thresholds. If fragment unrecognizable→ask for one more clue (any nearby term, feeling, or file).
