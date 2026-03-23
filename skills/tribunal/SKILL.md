---
name: tribunal
description: |
  [WHAT] Multi-model consensus tool — same prompt, 3 models, zero coordination, compare outputs.
  [HOW] Spawns Haiku, Sonnet, Opus as parallel subagents with identical prompts. No leading. Compares answers for agreement, tension, and surprise.
  [WHEN] Naming decisions, architecture questions, design bikesheds, "what would you call this", any question where independent convergence beats one model's opinion.
  [WHY] Three models agreeing independently is stronger evidence than one model being confident. Eliminates anchoring bias. If they disagree, the disagreement itself is the insight.

  Triggers: "tribunal", "ask all models", "multi-model", "consensus", "what would you name", "3 models", "independent vote", "naming vote", "architecture vote", "cross-model", "cli runner", "test across models"
skill_type: workflow
category: decision-support
metadata:
  proven_in: "2026-03-21 devx session — 4 unanimous decisions (handlers/surfaces/generated/contracts, core/utils, restore fractal, triage-first)"
  tools:
    - Agent
    - Bash
  references:
    - references/cli-runners.md
---

# Tribunal: Multi-Model Independent Consensus

## Mode Detection

Tribunal operates in two modes:

**Default mode (Steps 1-4 below)**: Same prompt, 3 Claude models, compare answers. Use this for naming, architecture, bikesheds — anything where independent convergence is the goal.

**Cross-runner mode**: When the caller specifies CLI runners, model lists, or a test matrix — load `references/cli-runners.md` for invocation patterns. Dispatch to the specified runners/models with the specified prompts. The caller decides what to test and why. Tribunal just knows how to invoke the runners and collect results.

Cross-runner dispatch uses Bash to invoke external CLIs. The prompt can vary per-dispatch (the caller decides). Tribunal's job is execution and collection, not study design.

## Step 1: Frame the Question

Write ONE prompt that:
- Describes the context neutrally (no leading)
- Presents the options without preference (or asks for a name without suggesting one)
- Asks for a short answer with reasoning
- Does NOT reference what you think the answer should be

```markdown
## Template

You are [context]. Answer this question:

[Question framed neutrally with all relevant constraints]

[Options if applicable, presented equally]

[Output format: "One sentence answer with reasoning" or "directory tree with descriptions"]
```

**Anti-patterns:**
- "I'm leaning toward X, what do you think?" — anchoring
- "Should we use X (which is better) or Y?" — leading
- Giving one option more detail than others — framing bias

## Step 2: Dispatch Three Models in Parallel

Launch ALL THREE in a single message (parallel tool calls). Same prompt. No coordination.

```
Agent(model="haiku", prompt=THE_PROMPT, name="tribunal-haiku", run_in_background=true)
Agent(model="sonnet", prompt=THE_PROMPT, name="tribunal-sonnet", run_in_background=true)
Agent(model="opus", prompt=THE_PROMPT, name="tribunal-opus", run_in_background=true)
```

**Rules:**
- Identical prompt text for all three — copy-paste, don't rephrase
- All three launch in the SAME message (parallel, not sequential)
- `run_in_background: true` for all three
- Short, focused prompts work best (under 200 words)
- For complex questions, include the same file references for all three

## Step 3: Collect and Compare

When all three return, present results in this format:

```markdown
**[Question summary]**

| Model | Answer | Key Reasoning |
|-------|--------|---------------|
| Haiku | X | "because..." |
| Sonnet | X | "because..." |
| Opus | X | "because..." |

**Verdict: [UNANIMOUS / SPLIT / DIVERGENT]**
- UNANIMOUS: all three agree → strong signal, lock it in
- SPLIT (2-1): majority wins but note the dissent — it might be right
- DIVERGENT (3 different): the question needs reframing or more context
```

## Step 4: Interpret the Result

| Outcome | What It Means | Action |
|---------|--------------|--------|
| Unanimous, same reasoning | The answer is obvious to anyone thinking clearly | Lock it. Don't second-guess. |
| Unanimous, different reasoning | Right answer, multiple valid reasons | Lock it. Note the strongest reasoning. |
| 2-1 split | Genuine tension — the dissent might see something | Present both sides. User decides. |
| 3-way divergent | Question is ambiguous or context-dependent | Reframe with more constraints and re-run. |

## When to Use vs When to Skip

**Use tribunal for:**
- Naming (directories, packages, concepts) — naming is where bikeshedding kills momentum
- Binary architecture choices (split vs merge, keep vs delete, A vs B)
- "Does this make sense?" sanity checks on designs
- Quick opinion where you want independence, not groupthink

**Don't use tribunal for:**
- Questions with objectively correct answers (use grep/read instead)
- Questions that require reading large codebases (agents need context)
- Implementation details (just write the code)
- Anything the user has already decided (respect their call)

## Examples from Practice

### Naming (unanimous: handlers/)
```
Prompt: "Design poly's internal directory structure.
Names must be surface-agnostic. What do you call the
directory where handler implementations live?"

Result: All three chose handlers/ with identical reasoning
("command implies CLI, handler is transport-agnostic")
```

### Architecture (unanimous: core/utils/)
```
Prompt: "Package for shared runtime utilities sits next
to pure-types package core/domain/. Name it core/shared/
or core/utils/?"

Result: All three chose utils/ ("shared describes a
relationship, utils describes contents — package names
should describe contents")
```

### Strategy (unanimous: restore from git)
```
Prompt: "Module deleted during merge conflict. Concept still
needed, multiple subsystems reinvented parts of it. Restore
from git history or rewrite from scratch?"

Result: All three chose restore ("proof the design was right
is that people keep reinventing it")
```
