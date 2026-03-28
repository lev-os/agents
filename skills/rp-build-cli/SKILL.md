---
name: "rp-build-cli"
description: "Build with rp-cli context builder plan → implement"
repoprompt_managed: true
repoprompt_skills_version: 29
repoprompt_variant: cli
---

# CLI Builder Mode (CLI)

Task: $ARGUMENTS

Build deep context via `builder` to get a plan, then implement directly. Use follow-up reasoning only when navigating the selected code proves difficult or the plan leaves a concrete gap.

## Using rp-cli

This workflow uses **rp-cli** (RepoPrompt CLI) instead of MCP tool calls. Run commands via:

```bash
rp-cli -e '<command>'
```

**Quick reference:**

| MCP Tool | CLI Command |
|----------|-------------|
| `get_file_tree` | `rp-cli -e 'tree'` |
| `file_search` | `rp-cli -e 'search "pattern"'` |
| `get_code_structure` | `rp-cli -e 'structure path/'` |
| `read_file` | `rp-cli -e 'read path/file.swift'` |
| `manage_selection` | `rp-cli -e 'select add path/'` |
| `context_builder` | `rp-cli -e 'builder "instructions" --response-type plan'` |
| `chat_send` | `rp-cli -e 'chat "message" --mode plan'` |
| `apply_edits` | `rp-cli -e 'call apply_edits {"path":"...","search":"...","replace":"..."}'` |
| `file_actions` | `rp-cli -e 'call file_actions {"action":"create","path":"..."}'` |

Chain commands with `&&`:
```bash
rp-cli -e 'select set src/ && context'
```

Use `rp-cli -e 'describe <tool>'` for help on a specific tool, `rp-cli --tools-schema` for machine-readable JSON schemas, or `rp-cli --help` for CLI usage.

JSON args (`-j`) accept inline JSON, file paths (`.json` auto-detected), `@file`, or `@-` (stdin). Raw newlines in strings are auto-repaired.

**⚠️ TIMEOUT WARNING:** The `builder` and `chat` commands can take several minutes to complete. When invoking rp-cli, **set your command timeout to at least 2700 seconds (45 minutes)** to avoid premature termination.

---
## The Workflow

0. **Verify workspace** – Confirm the target codebase is loaded
1. **Quick scan** – Understand how the task relates to the codebase
2. **Context builder** – Call `builder` with a clear prompt to get deep context + an architectural plan
3. **Only if needed, ask `chat`** – Use it when navigating the selected code is difficult or the plan leaves a concrete unresolved gap
4. **Implement directly** – Use editing tools to make changes once the plan is clear

---

## CRITICAL REQUIREMENT

⚠️ **DO NOT START IMPLEMENTATION** until you have:
1. Completed Phase 0 (Workspace Verification)
2. Completed Phase 1 (Quick Scan)
3. **Called `builder`** and received its plan

Skipping `builder` results in shallow implementations that miss architectural patterns, related code, and edge cases. The quick scan alone is NOT sufficient for implementation.

---

## Phase 0: Workspace Verification (REQUIRED)

Before any exploration, confirm the target codebase is loaded:

```bash
# First, list available windows to find the right one
rp-cli -e 'windows'

# Then check roots in a specific window (REQUIRED - CLI cannot auto-bind)
rp-cli -w <window_id> -e 'tree --type roots'
```

**Check the output:**
- If your target root appears in a window → note the window ID and proceed to Phase 1
- If not → the codebase isn't loaded in any window

**CLI Window Routing (CRITICAL):**
- CLI invocations are stateless—you MUST pass `-w <window_id>` to target the correct window
- Use `rp-cli -e 'windows'` to list all open windows and their workspaces
- Always include `-w <window_id>` in ALL subsequent commands
- Without `-w`, commands may target the wrong workspace

---
## Phase 1: Quick Scan (LIMITED - 2-3 tool calls max)

⚠️ **This phase is intentionally brief.** Do NOT do extensive exploration here—that's what `builder` is for.

Start by getting a lay of the land with the file tree:
```bash
rp-cli -w <window_id> -e 'tree'
```

Then use targeted searches to understand how the task maps to the codebase:
```bash
rp-cli -w <window_id> -e 'search "<key term from task>"'
rp-cli -w <window_id> -e 'structure RootName/likely/relevant/area/'
```

Use what you learn to **reformulate the user's prompt** with added clarity—reference specific modules, patterns, or terminology from the codebase.

**STOP exploring after 2-3 searches.** Your goal is orientation, not deep understanding. `builder` will do the heavy lifting.

---

## Phase 2: Context Builder

Call `builder` with your informed prompt. Use `response_type: "plan"` to get an actionable architectural plan.

```bash
rp-cli -w <window_id> -e 'builder "<reformulated prompt with codebase context>" --response-type plan'
```

**What you get back:**
- Smart file selection (automatically curated within token budget)
- Architectural plan grounded in actual code
- Chat session for follow-up conversation
- `tab_id` for targeting the same tab in subsequent CLI invocations

**Tab routing:** Each `rp-cli` invocation is a fresh connection. To continue working in the same tab across separate invocations, pass `-t <tab_id>` (the tab ID returned by builder).
**Trust `builder`** – it explores deeply, aggregates the relevant context, and selects intelligently. Default to trusting the plan it returns. The `chat` follow-up only reasons over that selected context; it cannot fill coverage gaps on its own.

---

## Phase 3: Ask `chat` only if needed

`chat` deep-reasons over the files selected by `builder`. It sees those selected files **completely** (full content, not summaries), but it **only sees what's in the selection** — nothing else.

**This phase is optional.** If the builder's plan is already clear and navigation through the selected code is straightforward, proceed straight to Phase 4.

Bring a follow-up to `chat` only when:
- Navigating the selected code proves difficult even with the builder's plan
- You need cross-file reasoning over the files already selected
- The plan leaves a concrete unresolved gap you cannot close by reading the selected files directly

If the answer depends on files outside the current selection, `chat` cannot answer it from thin air. Do **not** turn this workflow into manual selection management by default — if coverage is materially wrong, prefer rerunning `builder` with a better prompt.

```bash
rp-cli -t '<tab_id>' -e 'chat "The plan points me to X and Y, but I'''m still having trouble tracing how they connect across these selected files. What am I missing, and what edge cases should I watch for?" --mode plan'
```

> **Note:** Pass `-t <tab_id>` to target the same tab across separate CLI invocations.

**`chat` excels at:**
- Deep reasoning over the context_builder output and selected files
- Spotting cross-file connections that piecemeal reading might miss
- Answering targeted "what am I missing in this selected context" questions

**Don't expect:**
- Knowledge of files outside the selection
- Repository exploration or missing-file discovery — that's `builder`'s job
- Implementation — that's your job

---

## Phase 4: Direct Implementation

**STOP** - Before implementing, verify you have:
- [ ] A builder result available (`tab_id` if follow-up is needed)
- [ ] An architectural plan grounded in actual code

If a specific point is still unclear, use `chat` to clarify before proceeding.

Implement the plan directly. **Do not use `chat` with `mode:"edit"`** – you implement directly.

**Primary tools:**
```bash
# Modify existing files (search/replace) - JSON format required
rp-cli -w <window_id> -e 'call apply_edits {"path":"Root/File.swift","search":"old","replace":"new"}'

# Multiline edits
rp-cli -w <window_id> -e 'call apply_edits {"path":"Root/File.swift","search":"old\ntext","replace":"new\ntext"}'

# Create new files
rp-cli -w <window_id> -e 'file create Root/NewFile.swift "content..."'

# Read specific sections during implementation
rp-cli -w <window_id> -e 'read Root/File.swift --start-line 50 --limit 30'
```

**Ask `chat` only when navigation or cross-file reasoning is the bottleneck:**
```bash
rp-cli -w <window_id> -t '<tab_id>' -e 'chat "I'''m implementing X. The plan does not fully explain Y, and reading the selected files still leaves a gap. What pattern or connection am I missing here?" --mode chat'
```

---

## Key Guidelines

**Token limit:** Stay under ~160k tokens. Check with `select get` if unsure. Context builder manages this, but be aware if you add files.

**Selection coverage:**
- `builder` should already have selected the files needed for the plan
- `chat` can reason only over that selected context; it cannot discover missing files on its own
- If a material coverage gap blocks you, prefer rerunning `builder` with a better prompt over hand-curating selection
- Use `manage_selection` only as a last resort for a very small, targeted addition

**`chat` sees only the selection:** If the answer depends on files outside the selection, `chat` cannot provide it until coverage changes — and in this workflow, coverage changes should usually come from `builder`, not from manual curation.

---

## Anti-patterns to Avoid

- 🚫 Using `chat` with `mode:"edit"` – implement directly with editing tools
- 🚫 Asking `chat` about files it cannot see in the current selection
- 🚫 Treating Phase 3 as mandatory when the builder's plan is already clear
- 🚫 Reopening or second-guessing the builder's plan by default instead of trusting it
- 🚫 Leaning on manual `manage_selection` work to patch coverage gaps that should be handled by `builder`
- 🚫 Skipping `builder` and going straight to implementation – you'll miss context
- 🚫 Using `manage_selection` with `op:"clear"` – this undoes `builder`'s work; only use small targeted additions if absolutely necessary
- 🚫 Exceeding ~160k tokens – use slices if needed
- 🚫 **CRITICAL:** Doing extensive exploration (5+ tool calls) before calling `builder` – the quick scan should be 2-3 calls max
- 🚫 Reading full file contents during Phase 1 – save that for after `builder` builds context
- 🚫 Convincing yourself you understand enough to skip `builder` – you don't
- 🚫 **CLI:** Forgetting to pass `-w <window_id>` – CLI invocations are stateless and require explicit window targeting

---

**Your job:** Get a solid plan from `builder`, trust it by default, use `chat` only when navigating the selected code proves difficult or the plan leaves a concrete unresolved gap, then implement directly and completely.