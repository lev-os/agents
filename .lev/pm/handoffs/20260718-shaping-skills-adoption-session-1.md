---
status: paused
workstream: shaping-skills
component: adoption
slug: shaping-skills-adoption
session: 1
created_at: 2026-07-18
predecessor: null
confidence: 0.9
related_tasks: []
related_docs:
  - .lev/workshop/analysis/shaping-skills/analysis.md
  - .lev/workshop/analysis/shaping-skills/proposal.md
  - .lev/pm/decisions/d01-agents-home-convention.md
depends_on: []
canonical_refs:
  - .lev/workshop/analysis/shaping-skills/proposal.md
---

# Session Handoff: Shaping-Skills Adoption — Session 1

## You Are Here

**Workstream:** shaping-skills
**Component:** adoption (intake → proposal; execution not started)
**Session:** 1
**Status:** paused — proposal awaiting discussion/approval; open questions Q1–Q5 unanswered

Intake of `rjs/shaping-skills` complete via the workshop lifecycle (no submodule — that attempt was made and reverted). Route: `plugin`. Full proposal written in the shaping format itself and pushed to PR #8 (`claude/adopt-shaping-skills-FQfvp`). Shape B (lev-style skills-first ports) selected by binary fit check; delivery slices V1–V6 + H1 defined. AGENTS_HOME path convention recorded as ADR d01. Nothing under `skills/` has been created yet.

## Next Agent Brief

**Long-Term Goal:** Shape Up methodology (frame → shape → breadboard → slice) available as lev-native skills, aligned with the leviathan decision-frontier plan's Slice A (skills-first convergence; FlowMind resolver/composition//use are later bindings).

**Done Condition:** Five ports live under `skills/{frame,shape,breadboard,breadboard-reflect}/` (+ kickoff verdict), each with Work Link + d01 path header, artifacts routing `.lev/pm/{frames,shapes,breadboards}/` → `/work` → `/propose`; ripple hook project-local and guarded; security workflow green via H1.

**Current Execution Slice:** None in flight. Next is V1 (`skills/breadboard/` port) once the proposal is approved and Q3 (Work Link schema) is answered.

**Why V1 First:** Breadboarding has zero overlap with existing skills, so it validates the entire adaptation pattern (Work Link, artifact path, d01 header, propose-consumption) in isolation. Its stop condition gates the rest: if `/propose` can't consume a breadboard artifact, halt after V2 and defer breadboarding.

**Out of Scope This Session:** Actual skill ports, hygiene sweep execution, distribution packaging.

## Roadmap To Goal

**Remaining Steps:** 7 (V1–V6 + H1; H1 parallel off main)

1. **V1 — `skills/breadboard/`**: port body, Work Link (Shape lane, `shaped -> breadboarded`), output `.lev/pm/breadboards/<id>.md`. Demo: `/propose` consumes a real breadboard as slice evidence.
2. **V2 — `skills/shape/`**: R/S iteration + binary fit check, sibling to `/interview` (interview = ambiguity reduction, shape = solution iteration — do not merge).
3. **V3 — ripple hook**: project-local copy at `.claude/hooks/shaping-ripple.sh`, guarded settings entry (`test -x … && … || true`). Demo: silent on 100 unrelated writes, fires once on `shaping: true`.
4. **V4 — `skills/frame/`**: transcript → frame with evidence discipline (every Problem/Outcome bullet traces to a quote).
5. **V5 — `skills/breadboard-reflect/` + `/work` router rows** for new artifact types.
6. **V6 — kickoff verdict**: port, fold into `/handoff`, or pass (overlap check first).
7. **H1 — hygiene PR off main**: `.gitleaksignore` (22 placeholder fingerprints — regenerate full list with `gitleaks detect --report-format json`; CI log tail is partial), d01 hardcoded-path sweep (6 skill files + levnow reports), remove stale `skills-db/real-time-backend-skill` gitlink (breaks `git submodule status`).

## Open Questions (blocking discussion — carry forward until answered)

| # | Question | Blocks | Notes |
|---|----------|--------|-------|
| Q1 | What are the four surfaces in the decision-frontier plan? | Work Link field shape | Plan lives in leviathan repo (not in this container); this repo's poly lists five surfaces (CLI/MCP/HTTP/gRPC/WS), so "four-surface" means something not visible here. If skills are themselves a surface, Work Link may need a surface declaration field. |
| Q2 | Does Slice A define a convergence checklist for incoming skills? | V1 acceptance criteria | If yes, validate V1 against it; if no, propose R1–R3/R7/R8 from the proposal as that checklist. |
| Q3 | Formalize Work Link as *the* FlowMind fragment schema now? | V1 start (answer before V1 completes) | Ports write Work Link as structured markdown. If composition slice wants YAML fragments, define the schema while only one port exists — avoids re-porting five skills. |
| Q4 | Where do durable planning artifacts live? | Ergonomics only | `.lev/pm` is gitignored; d01 and this handoff are force-added (matching the two tracked handoffs precedent). Proposed fix: `!.lev/pm/decisions/` + `!.lev/pm/proposals/` + `!.lev/pm/handoffs/` carve-outs in root `.gitignore`. |
| Q5 | Distribution scope + audience | V4+ packaging polish | Ports-only vs lifecycle bundle vs plugin package; personal vs team vs public. Hook delivery lean: ship project-local + guarded. |

## Key Decisions This Session

| # | Decision | Where |
|---|----------|-------|
| D1 | No submodule — upstream lives as gitignored workshop clone at `.lev/workshop/intake/shaping-skills/`, refreshed by `git pull` | analysis.md Notes; first PR #8 commit reverted via force-push |
| D2 | Route = `plugin` with 3-spike validation ladder (breadboard → shape → hook) | analysis.md Proposal |
| D3 | `${AGENTS_HOME:-$HOME/.agents}` canonical home pattern, declared once at top of each skill; supports per-instance homes; XDG rejected; literal home paths banned | ADR d01 (accepted) |
| D4 | Integration mode: adapt to lifecycle conventions (Work Link + HUD + `.lev/pm/` paths), keep upstream methodology bodies near-verbatim | analysis.md Session Learnings |
| D5 | Shape B (lev-style skills-first ports) selected — only fit-check column with no ❌; A (verbatim) fails d01/Work Link/artifact paths; C (wait for composition) fails this-cycle availability | proposal.md |
| D6 | CI failures triaged: both pre-existing on main; gitleaks 22 findings all placeholders (valyu `YOUR_VALYU_API_KEY_HERE` examples + Fireworks `Key Id:` doc line) — fix via `.gitleaksignore`, not history rewrite | analysis.md Session Learnings |

## Checkpoints

| T+0 | Intake compared upstream 5 skills vs `/interview` `/propose` `/work` `/capture` — gap analysis: breadboarding/shaping/reflection net-new; framing/kickoff yes-ish |
| T+1 | Submodule attempt (vendor/shaping-skills + symlinked hook + bootstrap script) committed and PR #8 opened |
| T+2 | User: no submodule dep; follow workshop intake pattern instead |
| T+3 | Branch force-pushed: submodule commit replaced with workshop intake (`.lev/workshop/.gitignore` + analysis.md) |
| T+4 | CI hardcoded-path hit on analysis (literal project root) — fixed `e70ab2e2` |
| T+5 | Gitleaks log pulled: 22 findings verified as doc placeholders, no real leaks |
| T+6 | AGENTS_HOME convention agreed → ADR d01; session learnings appended to analysis (`6ed548f1`) |
| T+7 | Leviathan decision-frontier checkpoint synthesized → proposal.md in shaping format (`5eb5acba`); artifact rendered to user |
| T+8 | This handoff |

## Repo/PR State

- Branch: `claude/adopt-shaping-skills-FQfvp`, PR #8 (open, subscribed to activity)
- Committed: workshop `.gitignore`, `analysis.md` (+ session learnings), `proposal.md`, ADR d01, this handoff
- CI: GitGuardian ✅ CodeRabbit ✅ (5/5 pre-merge) · hardcoded-path ❌ + gitleaks ❌ both pre-existing on main (10+ red runs), fixed by H1, not this PR
- Local: leviathan repo NOT present in this container; decision-frontier plan known only from user-pasted checkpoint summary
- `.lev/workshop/intake/shaping-skills/` exists locally (gitignored) — fresh containers must re-clone: `git clone --depth 1 https://github.com/rjs/shaping-skills.git .lev/workshop/intake/shaping-skills`

## Resume Prompt

> Resume shaping-skills adoption (session 2). Read `.lev/workshop/analysis/shaping-skills/proposal.md` and this handoff. If the proposal is approved and Q3 is answered, start V1: port `skills/breadboard/` per Shape B (upstream body from `.lev/workshop/intake/shaping-skills/breadboarding/skill.md` — re-clone if missing; add d01 AGENTS_HOME header, Work Link block, output `.lev/pm/breadboards/<id>.md`). Validate with `lev-skills.sh` discovery and a propose-consumption demo. H1 hygiene PR can run in parallel off main.
