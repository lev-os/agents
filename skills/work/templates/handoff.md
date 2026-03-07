---
status: active | paused | completed
workstream: {slug}
component: {slug}
slug: {slug}
session: {N}
created_at: YYYY-MM-DD
predecessor: {filename.md}
confidence: 0.0-1.0
decisions_start: D{N}
---

<!-- AGENT BOOTSTRAP — read this first, act on it -->

## You Are Here

**{workstream}** — Session {N} | {status}

{One sentence: what's in progress, what's next.}

### Resume Protocol

1. Read this bootstrap + Next Agent Brief
2. Scan Timeline for 📖 Load entries — selectively load files to rebuild context
3. Verify understanding with the checklist in the brief
4. If confidence < 0.8, replay more Timeline entries
5. If you don't have `/work`: `cat ~/.agents/skills/work/SKILL.md`

**Predecessor**: [{previous session}]({path})

---

## Next Agent Brief

**Project State**: {brief description of overall project state}

**Current Focus**: {what we're actively working on and why it matters}

**Critical Knowledge:**
1. {Insight}: {why it matters}
2. {Insight}: {why it matters}
3. {Insight}: {why it matters}

**What to do next:**
{2-5 sentences: actionable instructions for the next agent — what to build/fix/research, what direction to take, what decisions are pending.}

### Quick Start

```bash
cd /path/to/project
{essential commands to get oriented}
```

### Verify You Understand

After replaying the Timeline, confirm these before proceeding:

- [ ] {critical insight — must be confirmed}
- [ ] {critical insight}
- [ ] {critical insight}

If any don't click, search the Timeline for the entry that established it.

**Confidence**: {X%} — {what's missing or uncertain, what to load first to raise it}

---

## Timeline

Chronological replay of context changes. Each entry records what happened and what was understood.
The next agent selectively replays entries to rebuild context — you don't need to read every one.

**Entry types**: 📖 Load | 🧭 Decision | 🔬 Research | 🔨 Build | 📋 Issue | 💬 Feedback | ✅ Gate

### T1: 📖 {title}

{What file/doc was read and why.}

**Now understood**: {the key insight — what changed in the agent's mental model}
**Refs**: `file.ts:42`, `doc.md`

### T2: 🧭 D{N}: {decision title}

{Context for why this decision was needed.}

**Decided**: {what}
**Because**: {why}
**Alternatives**: {what was rejected and why}
**Source**: {user | research | gate | inference}

### T3: 🔬 {research topic}

{What was found and what it means.}

**Now understood**: {insight for the workstream}
**Source**: {URL, report path, tool}

### T4: 🔨 {what was built}

**Changed**: `file.ts` (+50/-10), `test.ts` (+30)
**Result**: {outcome — tests pass, build green, etc.}

### T5: 📋 {issue title}

**BD**: {issue-id} → {status change}
**Context**: {why this matters}

### T6: 💬 {user feedback title}

> "{user quote or paraphrase}"

**Adjusted**: {what changed in approach or understanding}

### T7: ✅ {gate name}

**Gate**: {which gate, what was evaluated}
**Result**: {pass | fail — with evidence}
**Impact**: {what happens next because of this result}

---

## Decisions Log

> Decisions D1-D{N} in [{predecessor}]({path}). This session continues from D{N+1}.

### D{N+1}: {title} (T{M})

- **Statement**: {what was decided}
- **Rationale**: {why}
- **Alternatives**: {rejected options + why — prevents re-litigating}
- **Source**: {user | research | gate | inference}

---

## Open Questions

- [ ] {question} — raised T{N}
- [x] {question} — raised T{N}, resolved T{M}: {answer}

---

## Learned Patterns

Accumulates across sessions. When closing a workstream, distill these into the final Next Agent Brief.

### What Worked

- **{pattern}**: {why it worked, where to reuse}

### What Didn't Work

- **{anti-pattern}**: {why it failed, what to do instead}

### Code Patterns

- `path/to/example.ts:line` — {pattern description, when to apply it}

---

## Entity Matrix

For multi-entity sprints. Skip for single-task sessions.

| # | Entity | Lifecycle | Blocked By | Next Action |
|---|--------|-----------|------------|-------------|
| 1 | {entity} | {state} | {blocker} | {action} |

---

## Meta

| Rule | Value |
|------|-------|
| Line cap | Soft cap at ~500 lines; consolidate first, then shard only if unresolved work still makes the handoff dense |
| Session cap | No hard cap; shard by clarity and unresolved context, not by session count alone |
| Naming | `{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md` |
| Session progression | `session-1` only when `predecessor: null`; otherwise shard to `session-{N+1}` |
| Decision numbering | Global, never resets |
| Tick numbering | Session-local (T1, T2...) |
