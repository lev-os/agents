# Idea Hoffman: Meeting/Brainstorming Assistant

**Status:** ✅ Implemented (clawd-7vo)
**Date:** 2026-01-13
**Pattern:** Reid Hoffman Agent Orchestration

## Overview

The `idea-hoffman` skill implements Reid Hoffman's intellectual agent orchestration pattern for brainstorming and idea refinement. It enables:

- **Quick Capture** (< 5s) via existing `idea-filter.ts`
- **Hoffman Orchestration** - Parallel multi-agent analysis (5 specialized perspectives)
- **Meeting Facilitation** - Real-time intellectual sparring during brainstorms

## Quick Start

### Mode 1: Quick Capture

```bash
bun run ~/clawd/tools/idea-filter.ts "Build a CLI for X"
```

Captures to `projects/2nd-brain/_inbox/ideation.jsonl` with background PARA sorting.

### Mode 2: Hoffman Orchestration (in Claude Code)

**Trigger:** Say `/idea` or "Let's brainstorm this"

**Example:**
```
User: /idea Build a CLI tool that auto-generates commit messages

Claude: Launching Hoffman Orchestration...
        Dispatching 5 parallel agents for multi-perspective analysis:
        - First Principles Critic
        - Market Analyst
        - Technical Architect
        - User Psychology (JTBD)
        - Business Model

        [Agents run in parallel using Task tool with haiku/sonnet models]

        [After 2-3 minutes, synthesis provided with:]
        - Summary of each perspective
        - Conflict identification (reveals uncertainty)
        - 3 key insights
        - Recommended next actions
        - Option to capture to BD
```

### Mode 3: Meeting Facilitator

**Trigger:** "Sit in on this meeting" or "Help us brainstorm in real-time"

Claude participates as intellectual sparring partner:
- Listens for patterns
- Asks clarifying questions
- Plays devil's advocate
- Synthesizes decisions and next actions

## Integration Points

### Files
- **Inbox:** `projects/2nd-brain/_inbox/ideation.jsonl`
- **Daily Notes:** `memory/YYYY-MM-DD.md` (brainstorm summaries)
- **Scratchpad:** `memory/scratchpad.md` (evolving ideas)
- **Lessons:** `memory/lessons/[topic].md` (extracted learnings)

### Tools
- `idea-filter.ts` - Quick capture CLI
- `bd create` - Task creation after refinement

### Beads Workflow
After Hoffman session:
1. Option to create BD task with refined idea
2. Links to appropriate epic (PARA-sorted)
3. Captures summary to daily notes

## Agent Team Composition

Standard 5-agent orchestration:

| Agent | Role | Model | Focus |
|-------|------|-------|-------|
| **First Principles Critic** | Challenge assumptions | haiku | Logical holes, counter-arguments |
| **Market Analyst** | Research landscape | haiku | Existing solutions, gaps, user complaints |
| **Technical Architect** | Assess feasibility | sonnet | Implementation, risks, tech stack |
| **User Psychology** | Understand JTBD | haiku | Why would users switch? Mental models |
| **Business Model** | Revenue strategy | haiku | GTM, pricing, distribution, moats |

**Why 5?** Provides comprehensive coverage without overwhelming synthesis. Can scale to 3 (fast) or 7 (deep) based on complexity.

## Reid Hoffman Pattern Principles

From transcript analysis:

1. **Parallelization** - Agents run simultaneously, not sequentially
2. **Long Workflows** - Multi-turn orchestration, not single-shot
3. **Work While Away** - Computer productive while you're offline
4. **Management & Orchestration** - Coordinate multiple specialists
5. **Intellectual Amplification** - Use agents to amplify thinking, not replace it

## Second Brain Compliance

Aligns with 12 Principles:

- ✅ **#1 Reduce to ONE**: Capture only (idea-filter.ts handles rest)
- ✅ **#3 AI Inside Loop**: Agents orchestrate in background
- ✅ **#4 Drop Box < 5s**: Quick capture mode
- ✅ **#5 Cognitive Tax**: Defer organization, brainstorm when ready
- ✅ **#6 Structured Markdown**: All outputs markdown
- ✅ **#7 Multiplier**: Context amplifies every agent prompt
- ✅ **#8 Unreliability**: Multiple agents = adversarial validation
- ✅ **#11 Persistent Lessons**: Extracts learnings to memory/

## Usage Examples

### Example 1: Technical Idea

```
User: /idea Build a local-first sync engine for SQLite

Hoffman Orchestration dispatches:
- Critic: CRDTs vs OT, conflict resolution complexity
- Market: Compares to Replicache, ElectricSQL, PowerSync
- Technical: Assesses vector clock implementation, storage overhead
- User: JTBD = "offline-first without backend complexity"
- Business: Self-hosted vs managed sync service revenue

Output: 3 insights, recommended starting with CRDT research + PowerSync comparison
```

### Example 2: Business Idea

```
User: /idea AI-powered legal document analyzer for SMBs

Hoffman Orchestration dispatches:
- Critic: Liability concerns, lawyer replacement anxiety
- Market: Researches Harvey AI, Lexion, existing solutions
- Technical: NLP model selection, accuracy requirements
- User: JTBD = "understand contracts without $500/hr lawyer"
- Business: B2B SaaS, per-document pricing vs subscription

Output: Identified key risk (liability), validated market gap, recommended MVP scope
```

### Example 3: Meeting Facilitation

```
[Team brainstorming new feature]

Team: "Should we add real-time collaboration or focus on async workflows?"

Claude (Hoffman):
"I notice an unstated assumption - that real-time = better UX.
What's the JTBD here? If users work across timezones, async might be the feature.
Have we validated that users want synchronous editing, or are we pattern-matching to Google Docs?"

Team: "Good point. We haven't actually asked users about timezone distribution..."

Claude: "Recommended: 10 user interviews asking 'Describe your workflow when collaborating on X.'
Listen for timezone pain vs waiting-for-response pain. Different JTBDs."
```

## Evolution Notes

**Future Enhancements:**
- **Agent Specialization**: Custom agent types beyond the standard 5
- **Adaptive Team Size**: 3 agents for quick, 7 for deep analysis
- **Session Persistence**: Resume Hoffman sessions across multiple turns
- **Learning Loop**: Track which agent combinations produce best insights
- **Voice Integration**: Hoffman orchestration via Vapi during calls

**Failure Modes to Watch:**
- Agents agreeing too quickly (lack of intellectual tension)
- Over-parallelization creating synthesis overload
- Premature convergence (jumping to solution before exploring problem space)

## Technical Implementation

**Core Pattern:**
```typescript
// Single message dispatch (parallel execution)
await Promise.all([
  Task({ agent: 'critic', model: 'haiku', ... }),
  Task({ agent: 'market', model: 'haiku', ... }),
  Task({ agent: 'technical', model: 'sonnet', ... }),
  Task({ agent: 'user', model: 'haiku', ... }),
  Task({ agent: 'business', model: 'haiku', ... })
])

// Synthesize results
const synthesis = analyzeConflicts(results) + extractInsights(results)
```

**Model Selection:**
- Haiku: Fast research, market analysis, brainstorming
- Sonnet: Deep technical assessment, complex synthesis
- Opus: Reserved for critical architectural decisions (rare)

## Metrics

Track effectiveness:
- **Time to insight**: Avg time from seed idea to synthesized output
- **Agent conflict rate**: How often agents disagree (higher = better exploration)
- **BD conversion**: % of Hoffman sessions → BD tasks
- **User satisfaction**: Subjective "was this useful?" after each session

## References

- Reid Hoffman Transcript: `memory/transcripts/reid-hoffman-2026-predictions.vtt`
- 12 Principles: `projects/2nd-brain/CODE-PRINCIPLES.md`
- Idea Filter: `tools/idea-filter.ts`
- Bead: clawd-7vo

---

**🧙🏽‍♂️ Orchestrate intellectual amplification.**
