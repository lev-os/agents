# Intake Report: shaping-skills (rjs/shaping-skills)

- URL: https://github.com/rjs/shaping-skills
- Type: repo (Claude Code skills package)
- Project Root: /home/user/agents (lev-os/agents)
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
- Original submodule attempt (PR #8 first commit) has been reverted from local history; the branch will force-push to replace the submodule commit with this intake.
