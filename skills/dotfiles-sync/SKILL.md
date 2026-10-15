---
name: dotfiles-sync
description: Reconcile chezmoi dotfiles and the separate ~/.agents Git repository using commits and merges, with semantic conflict review and quiet scheduled sync.
---

# Workflow: Dotfiles Sync

NEVER REBASE. ALWAYS MERGE.

Every invocation covers two repositories: `~/.agents` for shared skills and
`~/.local/share/chezmoi` for dotfiles. Complete each repository independently.
The `dotfiles` helper checks chezmoi only; its clean result says nothing about
Agents. Report both outcomes before calling the sync complete.

## Authorized recurring machine sync

When the user authorizes recurring sync, that authorization covers safe changes within the agreed scope; do not ask for routine confirmation on every tick. Keep the interactive report/confirmation flow below for ad hoc sync without standing authorization.

- Use one host-local hourly Codex tick, serial execution and a nonblocking lock. Sync `~/.agents` hourly; run the chezmoi workflow only when 24 hours have passed since its last attempt. Record attempts and successes separately. Preserve existing holds and deduplicate unchanged alerts.

## Repository rules (every run)

- Treat `~/.agents` as its own Git repository, not a new chezmoi-managed tree. Never `chezmoi add ~/.agents`. Keep existing repository and submodule boundaries; do not advance or recurse into vendor submodules automatically.
- Dirty and new skill source files are expected: this sync shares work in progress as well as finished skills. Inspect the branch, upstream, index, merge state and tracked/untracked paths. Review each changed skill with its new local references, scripts and assets as one coherent change. A new file inside a skill, or a new skill with `SKILL.md`, is eligible when its content serves that skill and passes the exclusions below; it does not need separate approval merely because it is untracked or unfinished.
- Stage only reviewed explicit paths, including eligible new dependencies, and inspect the staged diff before committing. Preserve pre-existing staging: include it only when its exact contents are reviewed and belong to the same eligible change; otherwise leave it intact and hold only the affected change. Recheck file/index contents before commit; if they changed during review, retry that change on a later tick. Commit the reviewed snapshot, fetch and MERGE the configured upstream, then push normally. Never rebase, force-push, mass-add unknown files, or overwrite concurrent work.
- A dirty tree, new dependency or work-in-progress label alone is not a blocker. Hold a change only for a concrete excluded file, missing required dependency, failed relevant validation, changing snapshot, or uncertain conflict. Continue independent eligible changes when Git can preserve the held work. If Git cannot merge safely with held paths present, preserve them and report that specific repository blocker. Re-evaluate automation-created holds each tick; clear them when their cause is verified resolved. Keep user-deferred decisions held until the user rules.
- Exclude secrets, credentials, runtime state, transcripts, caches, logs, generated indexes, installations and vendor content, even if tracked. If excluded dirty paths or unknown staged changes prevent a safe merge, hold that repository and report the blocker; do not stash, reset or clean them away.
- Resolve a new textual conflict only when both intents are clear, the semantic combination is unambiguous and validation supports it. Otherwise preserve the conflict and escalate with both intents and a concrete recommendation. Previously held conflicts require the user's decision before resolution.
- For chezmoi, retain its established managed scope and inspect local/remote intent before any re-add or apply. Do not enable optional files, change settings scope, run broad installers, remove files, or apply entire directories unattended. Override chezmoi autoCommit/autoPush for any approved re-add so review, commit, merge and push remain ordered.
- Keep routine success/no-change quiet. Persist concise host-local results and timestamps; report new actionable errors or conflicts, meaningful worsening, and recovery. Never include secret values or raw credential diffs in reports.

## Terminology

| Term | Meaning | Path |
|------|---------|------|
| **local** | The actual dotfiles on this machine (chezmoi target) | `$HOME/.<file>` |
| **remote** | The chezmoi source repo, git-tracked and pushed | `$HOME/.local/share/chezmoi` |

Always use "local" and "remote" when presenting drift reports. Never use chezmoi's internal "source/target" terminology in user-facing output.

## Trigger

Run this workflow when you need to:
- share modified or new agent skills and their dependencies
- reconcile local-vs-remote dotfile drift
- inspect pending chezmoi changes before apply
- perform a safe remote-first sync across machines

## Inputs

- Agents repository at `$HOME/.agents`, with its configured branch and upstream
- Chezmoi remote repo at `$HOME/.local/share/chezmoi`
- Local state under `$HOME`
- `dotfiles` helper available on PATH
- Optional handoff context in `.lev/pm/handoffs/`
- Workstream state at `.lev/pm/workstreams/dotfiles-sync/state/workstream.yaml`

## Steps

### Phase 1: Scan + Auto-Classify (immediate, no user interaction)

1. Inspect `~/.agents`: branch, upstream, index, merge state, and every tracked/untracked change. Review each changed skill with its dependencies under the repository rules above. Record every change as eligible or held with a concrete reason. Done: every Agents change has a disposition, including a clean repository that still needs upstream reconciliation.
2. Run `dotfiles status` and `dotfiles sync` in parallel.
3. Run `dotfiles inspect chezmoi-diff` to get full diff content for every entry.
4. **Auto-classify every chezmoi diff** into exactly one of these buckets. There is NO "manual review" bucket — every diff MUST be classified:
   - **remote-only** — exists in remote, not reflected locally. This does not automatically mean local intentionally removed it; it can also mean this machine never installed or does not use an optional file.
   - **local-drift** — local changed intentionally, remote is stale (MM where target newer)
   - **conflict** — both changed in the same area (MM where both recent, content diverges structurally)
   - **volatile** — runtime noise: `.tmp`, `installation_id`, cache files, lockfiles, IDE state (auto NO-GO, silent skip)
   - **script-rename** — chezmoi script naming convention change (R status). Inspect source to confirm equivalence, then classify as GO.
   - **intentional-removal** — file deleted locally on purpose (check memory + handoff history for prior decisions before asking user)

   Classification rules:
   - If the path is in `.chezmoiignore`, skip entirely — it should not appear in the report.
   - If the path matches known volatile patterns (`.tmp`, `installation_id`, `plugins/`, `cache/`, `*.log`, `*.lock`), classify as **volatile** automatically.
   - If the diff shows only whitespace, line-ending, or timestamp changes, classify as **volatile**.
   - If DA and source is newer, inspect intent before recommending apply. Local absence can mean "not installed on this machine", not "removed globally". Example: `.config/opencode/oh-my-opencode.json` existed only in remote while local `opencode.json` was newer; the correct action was to forget the remote-only optional file, not apply it locally.
   - If MM and target is newer, classify as **local-drift**.
   - If R (rename), read both old and new source files to determine if content is equivalent or changed.
   - If any parent source path starts with `exact_`, audit the parent ownership before classifying child diffs. Exact directories make local runtime files appear as delete/re-add drift. Example: `exact_dot_codex` caused Codex sqlite/native-host/runtime files to recur every sync; the correct action was to convert to non-exact `dot_codex/AGENTS.md`, not classify every runtime file independently.
   - Treat `run_onchange_*` scripts as executable side effects, not normal file updates. Inspect the script before GO. Example: the QMD installer was narrow; `install-deps` triggered broad Homebrew upgrades and was not safe as a QMD-scoped action.
   - Check `.lev/pm/handoffs/` and memory for prior decisions about specific paths before classifying ambiguous items.

5. For each classified diff, determine GO/NO-GO:
   - **remote-only** → GO only when the remote file is clearly desired on this machine; otherwise ESCALATE or intentional-removal/forget
   - **local-drift** → GO (re-add from local to remote)
   - **conflict** → ESCALATE (present both sides, require explicit user decision)
   - **volatile** → NO-GO (skip silently, recommend adding to `.chezmoiignore` if not already there)
   - **script-rename** → GO only after side-effect review confirms the script is safe for this sync scope
   - **intentional-removal** → GO (remove from remote via `chezmoi forget`)

### Phase 2: Enriched Report (first response to user)

Present a single enriched report. Use `/now` or a clear table format. The report MUST include:

```
DOTFILES SYNC REPORT — {hostname} — {date}

SUMMARY
  Total diffs: N
  Auto-resolved: N (GO)
  Escalations: N (need your call)
  Volatile skipped: N

REPOSITORIES
| Repository | Local changes | Upstream state | Action or concrete hold |
|------------|---------------|----------------|-------------------------|
| Agents (~/.agents) | reviewed eligible and held paths | verified or unavailable | commit, merge, push; or reason |
| Dotfiles (chezmoi) | classified differences | verified or unavailable | reviewed actions; or reason |

ACTIONS (GO)
| # | Path | Direction | What changes | Classification |
|---|------|-----------|-------------|----------------|
| 1 | .claude/settings.json | local → remote | +3 hooks, -1 deprecated key | local-drift |
| 2 | .codex/AGENTS.md | local → remote | updated agent list | local-drift |
| ... | | | | |

ESCALATIONS (need decision)
| # | Path | Local intent | Remote intent | My recommendation |
|---|------|-----------|-------------|-------------------|
| (none if clean) | | | | |

VOLATILE (auto-skipped)
| Path | Reason |
|------|--------|
| .codex/.tmp | runtime temp dir |

CHEZMOIIGNORE CANDIDATES
| Path | Why |
|------|-----|
| (paths that keep showing up as volatile but aren't in .chezmoiignore yet) |
```

For escalations, explain intent, not just timestamps. Timestamp is evidence only. Example: local OpenCode config newer than remote means local may win, but a single remote package-name correction can still be merged intentionally.

When execution is already authorized in this conversation or by the recurring
contract, proceed with the reviewed actions. Ask only for unresolved decisions
or actions outside that authorization. Otherwise end the report with a single go/no-go prompt:
- If zero escalations: "All N actions are auto-classified GO. Execute? [y/n]"
- If escalations exist: "N actions ready, M need your call. Resolve escalations first, then execute."

### Phase 3: Execute (within existing authorization or after confirmation)

6. Sync Agents first. Load [Sync](../sync/SKILL.md) and run its plan from `~/.agents`. Use its bounded run only when its whole-repository staging and submodule behavior fit the reviewed inventory. When excluded, held or concurrent paths make that unsafe, use explicit reviewed paths: stage, inspect the staged diff, recheck the snapshot, commit, fetch, merge the configured upstream, and push normally. Preserve other changes and existing staging. A clean Agents tree still needs fetch/merge/push reconciliation. Done: eligible changes are published, or a concrete Git/validation blocker is recorded; independent chezmoi work can continue.
7. Re-add local-drift files to remote: `chezmoi re-add <paths>`
8. Remove intentional-removal files from remote: `chezmoi forget --force <paths>`
9. Review `git -C ~/.local/share/chezmoi status --short`
10. Commit with descriptive message when changes exist
11. Fetch, then merge remote changes (NEVER rebase)
12. Push
13. Only after remote is settled: apply the reviewed remote-only and script-rename paths explicitly; exclude scripts unless their effects were reviewed and authorized.
14. Verify Agents: compare local HEAD with the live upstream branch, inspect remaining dirty paths, and account for every held or concurrently changed path. A failed upstream check leaves publication unverified.
15. Re-run `dotfiles sync` and `dotfiles status` to verify chezmoi state.
16. Report both repository outcomes, pushed commits, remaining differences and concrete holds. Done: neither repository is omitted or inferred from the other's success.

## Team

| Role | Responsibility |
|------|---------------|
| dotfiles operator | Scans, auto-classifies ALL diffs, builds enriched report |
| git reconciler | Commits, merges, pushes the chezmoi remote repo |
| escalation agent | Only activates when true conflicts exist (both sides changed structurally) |

## Outputs

- Enriched drift report (first response, always)
- Updated Agents and chezmoi remote repo states, with separate outcomes
- Updated local home state after apply
- Dry-run report at `~/.local/state/lev/dotfiles-sync-plan.latest.txt`
- Workstream state update at `.lev/pm/workstreams/dotfiles-sync/state/workstream.yaml`

## Validation

- Agents was inspected and reconciled on this invocation; eligible modified/new skills and dependencies were published or have a concrete blocker.
- Agents local HEAD matches the live upstream branch, or publication is explicitly unverified; remaining dirty paths are accounted for.
- The final report includes both Agents and chezmoi outcomes. Chezmoi-only success cannot complete this workflow.
- Every diff is classified — zero items in any "manual review" or "unclassified" bucket
- `dotfiles sync` completes clean after execution
- Any committed remote changes are pushed successfully
- `chezmoi apply --force` runs only after remote is reconciled
- True conflicts (both sides changed structurally) are escalated, never auto-merged
- Final `dotfiles status` reflects either clean state or explicitly accepted volatile noise
- Volatile paths not in `.chezmoiignore` are flagged as candidates for addition
