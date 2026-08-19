---
shaping: true
title: "Shaping-skills adoption × decision-frontier Slice A"
status: proposed
created: 2026-07-18
related:
  - .lev/workshop/analysis/shaping-skills/analysis.md
  - .lev/pm/decisions/d01-agents-home-convention.md
  - "leviathan: .lev/pm/plans/plan-impl-decision-frontier-planning.md (not in this repo)"
---

# Proposal: Shaping-Skills Adoption as a Slice-A Workload

This proposal is written *in* the shaping format it proposes to adopt — requirements (R), shape options (A/B/C), a binary fit check, and vertical slices. It synthesizes the shaping-skills intake (PR #8) with the decision-frontier plan checkpoint from the leviathan repo.

---

## Frame

**Problem.** The Shape lane is the thinnest lane in the lifecycle: `/capture` inventories and `/interview` clarifies, but nothing iterates requirements against solution options, nothing produces an affordance-level design artifact, and `/propose` compiles slices from narrative designs without a mechanical bridge. Meanwhile the decision-frontier plan has committed Slice A to **skills-first convergence** — capabilities land as skills now; FlowMind resolver, composition, and the `/use` runtime come as separate later slices.

**Outcome.** The Shape Up methodology (frame → shape → breadboard → slice) is available as lev-native skills that (a) work today with zero runtime dependencies, and (b) are already shaped as composition-ready units the later FlowMind slices can consume without rewrite.

---

## Synthesis with Decision-Frontier

What I could verify from this repo + your checkpoint summary; the plan file itself lives in leviathan and isn't in this container.

| Decision-frontier element | How this work aligns |
|---|---|
| **Slice A: skills-first convergence** | All five ports are pure-markdown skills. No `.flow.yaml` dependencies, no resolver, no runtime. This adoption is a *test case* for Slice A: a real external methodology converging into `skills/` under lev conventions. |
| **FlowMind resolver (later slice)** | `/propose` already references `plugins/sdlc/flows/propose-adversarial-contract.flow.yaml` — which doesn't exist here; it "runs or emulates" it inline. The ports follow the same discipline: protocol expressed inline in the skill body, flow-file references treated as future bindings, never hard dependencies. |
| **Composition (later slice)** | The `## Work Link` block on each port (lane, entity movement, upstream/downstream, HUD) is the declared seam. `/work` already says the graph-footer partial is "authoring reference only until the skill-builder pipeline can project FlowMind fragments into skill bodies" — Work Link is exactly the fragment shape that projection will consume. |
| **`/use` runtime (later slice)** | Ports stay self-contained and filesystem-discoverable (`lev-skills.sh` inventories `skills/` directly). No static cross-skill `@import` chains, so a future `/use` resolver can load a port standalone. |
| **Four-surface architecture** | **[unknown]** — the four surfaces aren't named in this repo (poly multiplexes CLI/MCP/HTTP/gRPC/WS, which is five). Assumption: skills are (or sit behind) one surface, and nothing in these ports binds them to any specific surface. Needs one confirmation from the plan doc. |
| **Provider-policy design** | Orthogonal. No dependency either direction. |

**The convergence claim:** the shaping ports and Slice A want the same invariant — *methodology as data (markdown), runtime as a later binding*. If the ports are done right, promoting them from "skill body" to "FlowMind-composed flow" in a later slice is a projection step, not a rewrite.

---

## R: Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Shape-lane methodology (frame → shape → breadboard → slice) available as skills in this repo | Core goal |
| R1 | Skills are runtime-free markdown — no FlowMind/resolver/`/use` dependency (Slice A discipline) | Must-have |
| R2 | All path references follow d01: `${AGENTS_HOME:-$HOME/.agents}` declared once at top of each skill; no literal home paths | Must-have |
| R3 | Each skill carries one `## Work Link` block — the composition seam for later FlowMind projection | Must-have |
| R4 | Artifacts land under `.lev/pm/{frames,shapes,breadboards}/` and route through `/work` → `/propose` | Must-have |
| R5 | Ripple consistency check works project-locally, guarded (missing script/jq never errors), core script runtime-agnostic | Must-have |
| R6 | Upstream refreshable without vendoring (workshop intake clone, no submodule) | Must-have |
| R7 | Ports discoverable by `lev-skills.sh` filesystem-first inventory | Must-have |
| R8 | Portable to `/use` runtime later without rewrite (self-contained bodies, no static cross-skill imports) | Must-have |
| R9 | Methodology usable this cycle — not gated on unbuilt runtime slices | Must-have |

---

## S: Shapes

### A: Verbatim import

Copy the five upstream skills into `skills/` unchanged; wire the hook per upstream README (global `~/.claude` symlinks).

| Part | Mechanism | Flag |
|------|-----------|:----:|
| A1 | Copy upstream skill folders into `skills/` | |
| A2 | Global hook install per upstream README (`~/.claude/hooks` symlink) | |

### B: Lev-style ports, skills-first *(selected)*

Port each skill: upstream methodology body near-verbatim, plus lev frontmatter, Work Link, d01 path pattern, `.lev/pm/` artifact paths. Hook ships project-local and guarded. Upstream stays a gitignored workshop clone.

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | `skills/breadboard/SKILL.md` — affordance tables + wiring + V1–V9 slicing; output `.lev/pm/breadboards/<id>.md`; Work Link: Shape lane, `shaped -> breadboarded`, downstream `/propose` | |
| B2 | `skills/shape/SKILL.md` — R/S iteration, binary fit check, 🟡 change marks, doc-hierarchy ripple rules; output `.lev/pm/shapes/<id>.md`; sibling to `/interview` (interview = ambiguity, shape = R/S) | |
| B3 | Ripple hook: project-local copy at `.claude/hooks/shaping-ripple.sh` + guarded `settings.json` entry (`test -x … && … \|\| true`); script core runtime-agnostic | |
| B4 | `skills/frame/SKILL.md` — transcript → Source/Pre-work/Problem/Outcome with evidence discipline; output `.lev/pm/frames/<id>.md` | |
| B5 | `skills/breadboard-reflect/SKILL.md` — SEE→REFLECT sync-then-smell loop; updates breadboards in place | |
| B6 | `/work` router updates: lane table, route table, templates table rows for frames/shapes/breadboards | |
| B7 | Kickoff-doc: deferred, `monitor` — evaluate `/handoff` overlap before porting | |

### C: Wait for composition

Defer adoption until FlowMind resolver + composition slices land, then project the skills from flow fragments directly.

| Part | Mechanism | Flag |
|------|-----------|:----:|
| C1 | Author shaping methodology as FlowMind fragments | ⚠️ |
| C2 | Skill-builder projects fragments into skill bodies | ⚠️ |

---

## Fit Check

| Req | Requirement | Status | A | B | C |
|-----|-------------|--------|---|---|---|
| R0 | Methodology available as skills here | Core goal | ✅ | ✅ | ✅ |
| R1 | Runtime-free markdown (Slice A discipline) | Must-have | ✅ | ✅ | ❌ |
| R2 | d01 path convention, no literal home paths | Must-have | ❌ | ✅ | ✅ |
| R3 | Work Link on every skill | Must-have | ❌ | ✅ | ✅ |
| R4 | Artifacts under `.lev/pm/`, routed via `/work` | Must-have | ❌ | ✅ | ✅ |
| R5 | Guarded project-local ripple check | Must-have | ❌ | ✅ | ✅ |
| R6 | Upstream refresh without vendoring | Must-have | ✅ | ✅ | ✅ |
| R7 | `lev-skills.sh` discoverable | Must-have | ✅ | ✅ | ✅ |
| R8 | `/use`-portable without rewrite | Must-have | ❌ | ✅ | ✅ |
| R9 | Usable this cycle | Must-have | ✅ | ✅ | ❌ |

**Notes:**
- A fails R2/R4: upstream bodies hardcode `~/.claude/skills/…` and foreign artifact paths. Fails R3/R8: no Work Link seam; bodies assume upstream's doc layout. Fails R5: upstream hook install is global and unguarded.
- C fails R1/R9: depends on resolver + composition slices that are explicitly *after* Slice A; C1/C2 are flagged unknowns (fragment format doesn't exist yet). C is the right *eventual* projection target — B is how we get there with working skills in the meantime.

**Shape B = the only column with no ❌.** Selected.

---

## Detail B: Delivery Slices

Every slice ends in something demoable. V1 is deliberately the highest-information slice: it validates the whole adaptation pattern (Work Link, artifact path, d01 header, propose-consumption) on the one skill with zero overlap against existing skills.

| # | Slice | Parts | Demo |
|---|-------|-------|------|
| V1 | Breadboard port | B1 | Run `/breadboard` on a real feature → affordance tables at `.lev/pm/breadboards/<id>.md` → `/propose` consumes it as slice evidence |
| V2 | Shape port | B2 | Run `/interview` then `/shape` on a live subject → R/S/fit-check artifact; interview and shape don't re-litigate each other |
| V3 | Ripple hook | B3 | 100 unrelated writes: silent. One write to a `shaping: true` file: checklist fires once |
| V4 | Frame port | B4 | Feed a real transcript → frame doc where every Problem/Outcome bullet traces to a quote |
| V5 | Reflect port + router | B5, B6 | Seed a drifted breadboard → SEE re-syncs, REFLECT surfaces ≥1 smell; `/work` routes all new artifact types |
| V6 | Kickoff decision | B7 | Written verdict: port, fold into `/handoff`, or pass |
| H1 | Hygiene (parallel, separate PR off main) | — | `.gitleaksignore` (22 placeholder fingerprints) + d01 path sweep (6 skill files, levnow reports) + stale `skills-db/real-time-backend-skill` gitlink → security workflow green |

**Stop condition** (unchanged from intake): if V1 shows `/propose` can't accept a breadboard artifact without reworking its slice contract, halt at V2 — keep frame+shape, defer breadboarding until the propose contract evolves.

---

## Open Questions for Discussion

| # | Question | Why it matters |
|---|----------|----------------|
| Q1 | What are the four surfaces in the decision-frontier plan? | Confirms the assumption that these ports are surface-neutral. If "skills" is itself a surface, the Work Link block may need a surface declaration field now to avoid churn later. |
| Q2 | Does the plan's Slice A define a convergence checklist for incoming skills? | If yes, V1 should be validated against it, not just against this proposal's R set. If no, this R set (R1–R3, R7, R8) is a candidate for that checklist. |
| Q3 | Should Work Link be formalized as *the* FlowMind fragment schema now? | B ports write Work Link as prose-structured markdown. If the composition slice will want YAML fragments, defining that schema now (even unused) avoids re-porting five skills. Cheap to do in V1. |
| Q4 | Where do proposals like this one live? | `.lev/pm` is gitignored (d01 was force-added like the tracked handoffs). If planning artifacts should be durable and shared, the ignore rule wants an explicit carve-out (`!.lev/pm/decisions/`, `!.lev/pm/proposals/`) — small change, big ergonomics. |
| Q5 | Distribution scope/audience (parked from intake) | Ports-only vs lifecycle bundle vs plugin package; personal vs team vs public. Blocks V4+ packaging polish, not V1–V3. |

**Recommended next action:** approve Shape B → start V1 (`skills/breadboard/`) on this branch, H1 in parallel off main. Answer Q3 before V1 completes so the Work Link shape is settled while only one port exists.
