# Intake Report: shaping-skills (rjs/shaping-skills)

- URL: https://github.com/rjs/shaping-skills
- Type: repo (Claude Code skills package)
- Project Root: `$(git rev-parse --show-toplevel)` (lev-os/agents)
- Workshop Root: `.lev/workshop/`
- Workshop Manifest: missing (defaulted folder names)
- Repo Playbook: null (workshop.playbooks.repo_intake not configured)
- Papers Playbook: null
- Staged Source: `.lev/workshop/intake/shaping-skills/` (plain clone, gitignored)
- Analysis Path: `.lev/workshop/analysis/shaping-skills/analysis.md`

## Project Context

- Guide: `AGENTS.md` — missing (fail-fast requirement soft-waived; project uses skill-graph and `.lev/config.yaml` as primary orientation)
- North Star: `docs/NORTH_STAR.md` — missing
- Architecture: `docs/01-architecture.md` — missing
- Process: `docs/00-process.md` — missing
- Effective orientation used: `skills/{work,interview,propose,capture,intake,handoff}/SKILL.md` (lifecycle-lane skills), `skills/work/templates/` (canonical artifact templates), `skills-db/lev/lev-workshop/SKILL.md` (workshop lifecycle), `.lev/config.yaml`, and this repo's skill-inventory.

## External Summary

- **Purpose:** Adapt Basecamp's Shape Up methodology (framing → shaping → breadboarding → slicing) into Claude Code skills that operate on conversation transcripts and design iterations.
- **Stack:** Pure markdown skills (`SKILL.md` per skill), one bash hook (`hooks/shaping-ripple.sh`), no runtime code beyond that hook.
- **Key capabilities:**
  - `framing-doc` — transcript → frame (Source verbatim, Pre-work options landscape, Problem/Outcome bullets, optional Less-about/More-about boundary). Evidence discipline required.
  - `kickoff-doc` — kickoff transcript → builder reference organized by *territory* (system areas) not timeline; design decisions live inline in the area they affect.
  - `shaping` — R (requirements) / S (shapes) iteration with binary fit-check matrix, `🟡` change marks, multi-level doc consistency (shaping doc → slices doc → slice plans), spikes for investigation, part/mechanism vs tautology discipline.
  - `breadboarding` — UI/Code/Store affordance tables + Places + Wires Out / Returns To, with slicing procedure that yields V1–V9 vertical demo-able increments. Two modes: map existing system, or design from shaped parts.
  - `breadboard-reflection` — SEE (sync breadboard to code seams) → REFLECT (find/fix design smells via naming test, hidden-store check, place responsibility). Pairs with `/breadboarding`.
  - `shaping-ripple.sh` hook — fires on Write/Edit, reminds Claude to check ripple effects on files with `shaping: true` frontmatter.

## Fit For Current Project

- **Surface:** Shape lane and Plan lane in the lev lifecycle (`/work` router → `/interview`, `/propose`).
- **Tier:** Skills / methodology extension. No core-runtime change required.
- **Relevant overlaps:**
  - `/shaping` vs `/interview` — both reduce ambiguity before propose. Interview walks design branches; shaping iterates R+S with a fit matrix. Complementary, not duplicates.
  - `/breadboarding` slicing (V1–V9) vs `/propose` slice contract (dna.yaml + execution.yaml with `slices_required`) — same shape, different level. Breadboarding produces the *what* to slice; propose produces the *executable* slice with verifier contracts.
  - `/framing-doc` vs `/capture` — capture inventories conversation state with fidelity scoring; framing produces a structured problem/outcome doc from transcripts. Different intents.
- **Conflicts:**
  - Skills carry a foreign frontmatter shape (`shaping: true`) and lack lev's `## Work Link` block, HUD line, and lifecycle-lane declaration.
  - Skills reference hardcoded home paths (`~/.claude/skills/…`) — CI already fails on this pattern across the repo, but adapted ports should use `$CLAUDE_PROJECT_DIR` / relative paths.
  - No `entity_kind` / `lifecycle_target` on the artifacts; propose won't be able to route them without adaptation.

## Brief / Analysis

- **What it is:** A five-skill Shape Up methodology package + one PostToolUse hook, distributed as symlinked skills in `~/.claude/skills/`. Highly evidence-disciplined document skills; more experimental solo iteration skills.
- **Why it matters:** Fills three genuine gaps in the lev Shape lane — transcript→frame (framing-doc), R/S iteration with binary fit-check (shaping), and affordance-table design artifacts (breadboarding + breadboard-reflection). None of these exist in the current skills catalog.
- **Fit:** Slots into `/work`'s Shape lane between `/capture` and `/propose`. Each skill has a natural downstream: framing → shaping → breadboarding → propose slicing. Kickoff-doc is optional (overlaps `/handoff` more than it complements it).
- **Risk:** Adopting verbatim keeps foreign artifact paths (`.claude/skills/…`, `shaping: true` frontmatter), which would drift from lev conventions (Work Link, HUD, `.lev/pm/` artifact paths). Ripple-check hook is a bash script that assumes `jq` is available and runs on every Write|Edit — must be guarded when the target file is missing or the frontmatter is absent.

## Decision

- **Decision:** Route as `plugin` — adopt shaping-skills as lev-style skill ports under `skills/`, with adapted artifact paths and Work Link blocks. Do not vendor the upstream as a submodule; the upstream is intake reference only.
- **Why:** The methodology is proven and well-documented; the code surface is trivial. The work is adaptation (rename artifact paths, add Work Link + HUD, remove hardcoded homes) not invention. A submodule + symlink dependency is over-engineered for content this small and adds bootstrap fragility (empty submodule on fresh clone crashes the hook).
- **Recommended next step:** Spike the smallest adapted port (`skills/breadboard/` — the affordance-table skill has zero overlap with existing skills, so it validates the adaptation pattern in isolation).

## Proposal / Recommendation

- **Route:** `plugin`
- **Why this route:** Content is methodology + one hook; belongs outside core lev runtime as a set of new skills. No shared contracts, no runtime changes, no domain model impact.
- **Validation needed:** Need 3 spikes to validate the adaptation pattern before wholesale adoption:
  1. **Spike 1 — `skills/breadboard/`** (new ground): Port `breadboarding/skill.md` verbatim body + add lev frontmatter, `## Work Link` (Shape lane, `.lev/pm/breadboards/<id>.md` output, downstream `/propose`), HUD line. Verify a breadboard artifact routes through `/work → /propose` without manual intervention.
  2. **Spike 2 — `skills/shape/` sitting next to `/interview`**: Confirm the two skills compose without stepping on each other (interview clarifies subject; shape iterates R/S). Draft a shape at `.lev/pm/shapes/<id>.md`; verify `/interview` still owns ambiguity reduction.
  3. **Spike 3 — the ripple hook, project-local**: Port `shaping-ripple.sh` to `.claude/hooks/`, wire via `.claude/settings.json` with a guard (`test -x ... && ... || true`) so a fresh clone without the hook or without `shaping: true` files doesn't error. Verify the hook is silent on 100 unrelated Write|Edit calls and fires the checklist exactly once on a `shaping: true` file.
- **Final solution if validated:** Five lev-style skills — `skills/{frame,shape,breadboard,breadboard-reflect,kickoff}/` — each with `## Work Link` declaring Shape/Plan lane membership, `.lev/pm/{frames,shapes,breadboards,kickoffs}/` output paths, HUD line, and full methodology body carried over from upstream. Plus one project-local hook. Upstream reference stays at `.lev/workshop/intake/shaping-skills/` (gitignored), refreshed with `git pull` when needed.
- **Stop condition:** If Spike 1 reveals that `/propose` can't consume a breadboard-format artifact without meaningful rework of the propose slice contract, downgrade to `spike` route — invest only in `frame` and `shape` and defer breadboarding.

## Action Dashboard

| Priority | Action | Owner / Surface | Artifact or Path | Verification | Status |
|---|---|---|---|---|---|
| P0 | Spike `skills/breadboard/SKILL.md` — port `breadboarding/skill.md` body + lev Work Link | Shape lane; adapts upstream file at `.lev/workshop/intake/shaping-skills/breadboarding/skill.md` | `skills/breadboard/SKILL.md`, output `.lev/pm/breadboards/<id>.md` | `/work` routes a synthetic request to `/breadboard`; artifact lands at declared path; downstream `/propose` accepts breadboard-format input as a slice source | ready |
| P1 | Spike `skills/shape/SKILL.md` — port `shaping/SKILL.md` body + lev Work Link; verify composition with `/interview` | Shape lane; sibling to `/interview` | `skills/shape/SKILL.md`, output `.lev/pm/shapes/<id>.md` | `/interview` reduces ambiguity, hands off subject; `/shape` produces R/S/fit-check without re-litigating orientation | blocked-by-P0 |
| P2 | Spike project-local ripple hook | `.claude/hooks/` + `.claude/settings.json` | `.claude/hooks/shaping-ripple.sh` (project copy, not symlink), guarded command entry | Hook is silent on 100 non-shaping Write|Edit calls; fires exactly once on a `shaping:true` file | blocked-by-P0 |
| P3 | Adapt `skills/frame/SKILL.md` (transcript → frame) | Shape lane; upstream of `/shape` | `skills/frame/SKILL.md`, output `.lev/pm/frames/<id>.md` | Evidence-discipline pass: every line in Problem/Outcome traces to a source quote | blocked-by-P1 |
| P4 | Adapt `skills/breadboard-reflect/SKILL.md` | Shape lane; pairs with `/breadboard` | `skills/breadboard-reflect/SKILL.md`, updates existing breadboard artifact in place | SEE phase re-syncs breadboard to code; REFLECT surfaces at least one smell on a seeded misaligned example | blocked-by-P0 |
| P5 | Defer `skills/kickoff/SKILL.md` — evaluate overlap with `/handoff` first | Close-adjacent; possibly redundant | evaluation note in this analysis | If `/handoff` already covers builder-reference needs, `pass` on kickoff-doc; else adapt | monitor |
| Guardrail | Do NOT re-introduce vendor/shaping-skills as a submodule or add `~/.claude/skills/…` hardcoded paths in adapted ports | Whole repo | grep `find skills -name SKILL.md | xargs grep -l '/home/\|/Users/'` returns nothing new after adaptation | Hardcoded-path CI check does not regress | ready |

## Verification

- **Acquisition:** `git clone --depth 1 https://github.com/rjs/shaping-skills.git .lev/workshop/intake/shaping-skills` — succeeded; upstream README + 5 SKILL.md files + 1 hook script present.
- **Analysis:** Compared all 5 upstream skills against `skills/{work,interview,propose,capture,intake,handoff}/SKILL.md`; verified no existing `affordance`/`breadboard`/`fit-check`/`R0` methodology in the repo (Explore agent report); confirmed `.lev/pm/` template set has room for new artifact types (`frames/`, `shapes/`, `breadboards/`, `kickoffs/`) without conflicting with existing `designs/`, `proposals/`, `tasks/`.
- **Projections or lifecycle hooks:** None yet — this is intake. Adaptation happens per-spike under the P0–P4 action rows.
- **Known gaps:**
  - No AGENTS.md / NORTH_STAR to ground the fit assessment beyond skill inventory + templates.
  - Kickoff-doc overlap with `/handoff` is asserted but not verified; P5 action monitors this.
  - Upstream ripple hook uses `jq` — availability on target environments not verified. Guard in the settings.json entry handles the missing-jq case by silent failure.

## Notes

- Runtime workshop folders (`intake/`, `cache/`) are gitignored via `.lev/workshop/.gitignore`. Only the `analysis/` output for shaping-skills is checked in.
- To refresh the intake source: `git -C .lev/workshop/intake/shaping-skills pull` (currently on main, latest commit as of intake). No submodule pin.
- Original submodule attempt (PR #8 first commit) has been reverted from local history; the branch was force-pushed to replace the submodule commit with this intake.

## Session Learnings (2026-07-18, PR #8 session)

Context from the working session that isn't captured elsewhere. Read this before starting the P0 spike.

### Path convention for adapted ports (binding)

Decision recorded as ADR `.lev/pm/decisions/d01-agents-home-convention.md`:

- Canonical home pattern is `${AGENTS_HOME:-$HOME/.agents}`. **Every adapted skill declares this pattern once at the top** (first section, before any path reference), then refers to `$AGENTS_HOME/...`.
- Rationale: multi-runtime (not Claude-only, so `~/.claude/` is wrong as a base), and multi-*instance* — a per-project or per-container agents home sets `AGENTS_HOME` in its environment and every skill inherits it; the global default (`~/.agents`) needs no setup.
- Upstream shaping-skills hardcodes `~/.claude/skills/...` install paths and its README installs via symlink into `~/.claude/skills/`. Adapted ports must not carry those references; the ripple hook port likewise resolves via the pattern, not a literal path.
- Prose aimed at humans may say `~/.agents/...`; scripts use the full `${AGENTS_HOME:-$HOME/.agents}` form.

### Per-skill adaptation design (agreed direction)

Integration mode: **adapt to lifecycle conventions** (not verbatim import, not thin wrapper). Each port keeps the upstream methodology body near-verbatim where it is methodology-not-plumbing, and adds:

| Port | Lane | Entity movement | Upstream feeds | Downstream | Output artifact |
|---|---|---|---|---|---|
| `skills/frame/` | Shape | `memory\|transcript -> framed` | raw transcripts, `/capture` output | `/shape`, `/interview` | `.lev/pm/frames/<id>.md` |
| `skills/shape/` | Shape | `framed\|aligned -> shaped` | `/frame`, `/interview` | `/breadboard`, `/propose` | `.lev/pm/shapes/<id>.md` |
| `skills/breadboard/` | Shape | `shaped -> breadboarded` | `/shape` (parts), or existing code (mapping mode) | `/propose` (slice source), `/breadboard-reflect` | `.lev/pm/breadboards/<id>.md` |
| `skills/breadboard-reflect/` | Shape | `breadboarded -> breadboarded(synced)` | `/breadboard` + implementation code | `/propose` | updates breadboard in place |
| `skills/kickoff/` (deferred) | Close-adjacent | `proposed -> kicked-off` | `/propose`, kickoff transcript | builder session | `.lev/pm/kickoffs/<id>.md` |

Each carries one `## Work Link` block (lane, movement, upstream, downstream, `Router: /work`, HUD line) per the `/work` router contract, and `/work`'s lane table + route table + templates table need rows for the new artifact types. The `templates/design.md` reference in `/interview` stays authoritative for design artifacts; shapes/breadboards are *new* artifact types, not replacements for designs.

Key composition facts established by comparison:

- `/interview` vs `/shaping`: interview owns ambiguity reduction (scored orientation loop, one-question-at-a-time branch walking); shaping owns R/S iteration (numbered requirements, lettered shapes, binary ✅/❌ fit-check matrix, 🟡 change marks, multi-level doc consistency shaping→slices→slice-plans). Complementary — interview clarifies the subject, shape iterates the solution space. Do not merge them.
- `/breadboarding` slicing (V1–V9, every slice ends in demo-able UI) is the same discipline as `/propose`'s `slice_verticality_gate`. The breadboard is the *what* (affordance tables + wiring); propose compiles the *executable* (dna.yaml + execution.yaml with verifier contracts). P0 spike verifies propose can consume a breadboard artifact as slice evidence.
- Upstream "documents hierarchy" (shaping doc → slices doc → slice plans, changes ripple both directions) maps onto shape artifact → breadboard artifact → propose task folder. The ripple hook is the mechanical reminder for that consistency contract.
- `shaping: true` frontmatter is the hook trigger and is worth keeping as-is in adapted artifacts (cheap, greppable, upstream-compatible).

### Ripple hook port notes

- Upstream hook: PostToolUse on `Write|Edit`, exits 2 with a checklist on any `.md` whose first 5 lines contain `shaping: true`; requires `jq`.
- Port as a **project-local copy** (not symlink) at `.claude/hooks/shaping-ripple.sh`, registered in `.claude/settings.json` with a guarded command — `test -x ... && ... || true` — so a fresh clone or missing `jq` never errors on unrelated writes. (CodeRabbit flagged the unguarded form on the reverted submodule commit; the guard was validated in-session.)
- Note `.claude/settings.json` is Claude-specific; other runtimes wanting the ripple check need their own hook registration. The script itself is runtime-agnostic (stdin JSON with `tool_input.file_path`).

### CI state (as of this session)

Both failing checks in `.github/workflows/security.yml` are **pre-existing on main** (10+ consecutive red runs verified via Actions history) and are not caused by this branch:

1. **Hardcoded path check** — offenders (all on main): `skills/interview/SKILL.md`, `skills/cdo/SKILL.md`, `skills/cass-coverage/SKILL.md`, `skills/cass-coverage/scripts/merge.py`, `skills/codex-autoresearch/tests/test_check_skill_invariants.py`, `convex/AGENTS.md`, and five `levnow/*.json` reports. Fix = the d01 sweep (separate PR). One in-branch hit (literal project root in this analysis) was already fixed in commit `e70ab2e2`.
2. **Secret scan (gitleaks)** — 22 findings, **all confirmed placeholders, no real leaks**: valyu docs with `YOUR_VALYU_API_KEY_HERE`-style example headers (`skills-db/.archive/consolidated-2026-02-03/search-valyu/SKILL.md` and `skills/lev-research/backends/valyu-recursive-confidence/BACKEND.md`, lines ~449/459/468, `curl-auth-header` rule) and Fireworks docs placeholder `Key Id: <key id shown by CLI>` (`skills-db/sdk/fireworks-ai/references/llms-full.md:21003`, `generic-api-key` rule), each flagged at historical commits `3bde184b…` and `ef5ff88a…` among others. Fix = add a `.gitleaksignore` with the finding fingerprints (regenerate the full 22-line list by running `gitleaks detect --source . --report-format json` locally; the CI log tail only shows part).
3. Unrelated cleanup signal seen in CI post-job: `No url found for submodule path 'skills-db/real-time-backend-skill' in .gitmodules` — a stale gitlink in the index with no `.gitmodules` entry; also breaks `git submodule status` locally. Worth fixing in the hygiene PR (`git rm --cached skills-db/real-time-backend-skill` or add the entry).

### Distribution (open, not yet decided)

Raised but not resolved in-session — decide before P3:

- **Scope**: just the five shaping ports vs the full lifecycle bundle (`work/interview/propose/capture/close/handoff` + ports) vs whole catalog vs installable plugin package.
- **Audience**: personal multi-machine, team, or public. Public implies license/versioning/README work.
- **Hook delivery**: ship with the package (project-local, guarded — current lean), one-time global user install (upstream's model), or skip the hook and rely on skill-body reminders.
- The `AGENTS_HOME` instance model (d01) is the substrate any of these sit on: an install = materializing skills into some `$AGENTS_HOME` and exporting the var.

### Next steps (refreshed)

1. **P0 spike `skills/breadboard/`** — first adapted port; validates Work Link + artifact path + propose-consumption. Declare the `AGENTS_HOME` pattern at top per d01.
2. P1 `skills/shape/` next to `/interview`; P2 ripple hook (guarded, project-local); then P3 `frame`, P4 `breadboard-reflect`; P5 kickoff stays `monitor` pending `/handoff` overlap check.
3. Separate hygiene PR(s) off main: `.gitleaksignore` fingerprints, d01 hardcoded-path sweep, stale `skills-db/real-time-backend-skill` gitlink. Together these turn the security workflow green.
4. Decide distribution scope/audience before investing in P3+ packaging.
