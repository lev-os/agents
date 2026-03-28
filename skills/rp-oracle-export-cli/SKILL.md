---
name: "rp-oracle-export-cli"
description: "Export a ChatGPT-ready Question / Plan / Review prompt using rp-cli"
repoprompt_managed: true
repoprompt_skills_version: 29
repoprompt_variant: cli
---

# ChatGPT Prompt Export (CLI)

Task: $ARGUMENTS

Export a ChatGPT-ready prompt file with the right amount of context.

## Rules

- Infer **Question / Plan / Review** when obvious. Ask only if unclear.
- For vague requests, use repo evidence before asking questions.
- Use the fast path only when the scope is already small, concrete, and obviously file-local.
- For broad **Question/Plan** exports, `context_builder` is the default path.
- For review exports, `context_builder` is the default path.
- Do **not** spend exploratory tool calls proving that a broad request is complex enough for `context_builder`.
- When you do use `context_builder` here, keep `response_type: "clarify"`.
- If you used the fast path, review the selection and prompt text before exporting.
- If you used `context_builder`, trust its curated selection, budget, and generated prompt by default; only re-check or adjust prompt/selection/tokens if you noticed a concrete issue.
- Export to a unique repo-local file, usually in `prompt-exports/`.
- Derive a short slug from the user's request and use it in the filename.
- Use a relative repo-local path by default; do not use an absolute path or another folder unless the user explicitly asks for it.

## Workflow

### 0: Workspace Verification (REQUIRED)

Before any building context, confirm the target codebase is loaded:

```bash
# First, list available windows to find the right one
rp-cli -e 'windows'

# Then check roots in a specific window (REQUIRED - CLI cannot auto-bind)
rp-cli -w <window_id> -e 'tree --type roots'
```

**Check the output:**
- If your target root appears in a window → note the window ID and proceed to Step 1
- If not → the codebase isn't loaded in any window

**CLI Window Routing (CRITICAL):**
- CLI invocations are stateless—you MUST pass `-w <window_id>` to target the correct window
- Use `rp-cli -e 'windows'` to list all open windows and their workspaces
- Always include `-w <window_id>` in ALL subsequent commands

---
### 1. Determine intent and scope

Infer the prompt type from the request:
- **Review** for git diff / PR / branch comparison requests — i.e. the user wants to inspect *changes*
- **Plan** for design / approach / implementation-plan / architectural audit / code evaluation requests — even if the user says "review" or "audit", if there are no diffs involved, this is a Plan
- otherwise **Question** when that is clearly implied

If the request is vague:
- for **Review**: inspect git state first
- for **Question/Plan**: if it sounds broad, architectural, evaluative, redesign-oriented, or likely multi-file, skip manual exploration and go straight to `context_builder`

Ask **one specific question** only if needed, and base it on the repo state you found.
Good question shapes:
- “I see changes in A and B. Do you want review of these current uncommitted changes, or against `main`?”
- “I found likely touchpoints in X and Y. Is the fix plan for X only, or this broader flow?”


**If the scope is still unclear, STOP and ask the user.** Do not ask generic workflow questions when you could ask a concrete scope question instead.

### 2. Choose context path

Because this prompt does not expose the workflow export budget directly, prefer `context_builder` unless the review scope is obviously tiny.

#### Review

Start by checking git state:
```bash
rp-cli -w <window_id> -e 'git status'
rp-cli -w <window_id> -e 'git diff --detail files'
```

#### Review Scope Confirmation

Determine the comparison scope from the user's request and git state.

**If the user already specified a clear comparison target** (e.g., "review against main", "compare with develop", "review last 3 commits"), **skip confirmation and proceed** using the scope they specified.

**If the scope is ambiguous or not specified**, ask the user to clarify:
- **Current branch**: What branch are you on? (from git status)
- **Comparison target**: What should changes be compared against?
  - `uncommitted` – All uncommitted changes vs HEAD (default)
  - `staged` – Only staged changes vs HEAD
  - `back:N` – Last N commits
  - `main` or `master` – Compare current branch against trunk
  - `<branch_name>` – Compare against specific branch

**Example prompt to user (only if scope is unclear):**
> "You're on branch `feature/xyz`. What should I compare against?
> - `uncommitted` (default) - review all uncommitted changes
> - `main` - review all changes on this branch vs main
> - Other branch name?"

**If you need to ask, STOP and wait for user confirmation before proceeding.**

This prompt does not expose the workflow export-mode budget directly. Lean on `context_builder` unless the uncommitted review scope is clearly tiny, obviously bounded, and safe to include in full.
For `Review`, the fast path is the **exception**, not the default. It is allowed only when the confirmed scope is **uncommitted changes** and the **full changed-file review scope** is obviously tiny and safe to include in full. Otherwise require `context_builder`.
For `Review`, this is the default path. If the review is not a tiny uncommitted-change export that is obviously safe to include in full, `context_builder` is required.
For review exports, explicitly reference the diff / changed files in the context you build.

**Always include the phrase "code review" in your `context_builder` instructions for Review exports.** This phrase activates diff analysis in the discovery agent. Without it, the builder treats the request as a general exploration.

#### Question / Plan

Default to `context_builder` for any request that is broad, architectural, evaluative, redesign-oriented, or likely to touch multiple files.

Do **not** spend tool calls proving that these requests are complex. If the user is asking you to evaluate logic, assess a design, rethink a flow, or reason about behavior across a system, call `context_builder` immediately.

Use the fast path only when the request is already small and obvious:
```bash
rp-cli -w <window_id> -e 'search "<key term>"'
rp-cli -w <window_id> -e 'select add RootName/path/to/FileA.swift RootName/path/to/FileB.swift'
```

If there is any real doubt that the fast path will fully cover the task, use `context_builder`.

Otherwise use `context_builder`:
```bash
rp-cli -w <window_id> -e 'builder "<task>Question / plan request here</task>
<context>Scope: <what you found>. Keep the export focused.</context>" --response-type clarify'

rp-cli -w <window_id> -e 'builder "<task>Code review of changes against <confirmed_scope>.</task>
<context>Intent: code review. Branch: <branch_name>.</context>" --response-type clarify'
```

### 3. Final check (fast path only — skip after `context_builder`)

**If you used `context_builder`, skip this step entirely and go straight to Step 4.** The builder already curated the selection, managed the token budget, and wrote the prompt. Do not read the prompt back, do not inspect the selection, do not check token counts, and do not critique, rewrite, or "improve" the generated prompt text. Treat the builder's output as the final payload for export.

**If you used the fast path**, check the selection and prompt text before exporting:
```bash
rp-cli -w <window_id> -e 'select get'
rp-cli -w <window_id> -e 'prompt get'
```

If available in this surface, the fast path may also inspect token state:
```bash
rp-cli -w <window_id> -e 'context --include selection,tokens'
```

If the prompt wording or selection is off, fix it before exporting.

### 4. Export

Use a unique repo-local relative path such as:
- `prompt-exports/<yyyy-mm-dd>-<hhmmss>-question-<slug-from-request>.md`
- `prompt-exports/<yyyy-mm-dd>-<hhmmss>-plan-<slug-from-request>.md`
- `prompt-exports/<yyyy-mm-dd>-<hhmmss>-review-<slug-from-request>.md`

Choose `<slug-from-request>` by summarizing the user's request into a short filesystem-safe phrase. Prefer descriptive slugs like `collapsing-tool-logic` or `agent-transcript-redesign`, not generic names like `export` or `question`.

Unless the user explicitly asks for another destination, keep the export path relative and repo-local under `prompt-exports/`.

Preset mapping:
- `Question` → `standard`
- `Plan` → `plan`
- `Review` → `codeReview`

```bash
rp-cli -w <window_id> -e 'prompt export "prompt-exports/<unique filename>.md" --copy-preset <standard|plan|codeReview>'
```

## Anti-patterns

- Asking generic workflow questions before checking repo state
- Skipping `context_builder` for branch / PR / large review exports
- Doing exploratory searches or file reads before `context_builder` for a broad Question/Plan export just to prove the task is complex
- Treating requests like "evaluate this logic", "assess this design", or "rethink this flow" as fast-path exports
- Using the fast path when scope is still vague
- Exporting from the fast path without checking the selection and prompt text
- Re-checking selection, prompt text, or tokens after `context_builder` — the builder already finalized the payload
- Reading the prompt back after `context_builder` to review, critique, rewrite, or "improve" it — export it as-is
- Calling `prompt get`, `manage_selection get`, or `workspace_context` after `context_builder` completed — go straight to export
- Reusing generic filenames like `oracle-prompt.md` by default
- Using generic slugs like `export`, `question`, or `plan` when the request gives you enough detail for a better filename
- Writing to an absolute path or outside the repo by default when the user did not ask for that

Report the final export path, prompt type, whether you used the fast path or `context_builder`, and token count if available.