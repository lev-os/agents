# HUD — Heads-Up Display (replaces graph footer)

One line. Always. Every response. This IS the status bar.

## The HUD Line

```
🧬 {ws} ⚡{exec_count} 📥{capture_count} ⏸️{paused_count} ✅{done_count} | 🚦{gate}={score} | ⏭️ {next} | 🔁{loop_state}
```

## Example

```
🧬 lifecycle-engine ⚡2 📥0 ⏸️3 ✅20 | 🚦convergence=0.78 | ⏭️ flow.schema | 🔁ll:t2 180s
```

## Expanded View = /siterep

When you need more than the HUD line, run /siterep for the full dashboard.
The HUD is the collapsed view. /siterep is the expanded view. Same data.

## HUD vs Footer — When to Use Which

| Context | Use | Format |
|---------|-----|--------|
| `/ll` (loop ticks) | **HUD** | 1-line status bar |
| `/siterep` | **HUD** | 1-line status bar (+ expanded dashboard above) |
| `/lev` (bare) | **HUD** | 1-line status bar (= big dashboard) |
| `/work`, `/capture`, `/exec`, `/propose` | **HUD** | 1-line status bar at end |
| `/interview`, `/research`, `/prior-art` | **Footer** | Skill-specific output template |
| `/now`, `/tribunal`, `/cdo` | **Footer** | Skill-specific output template |

**Rule:** Loop-aware skills get HUD. Domain skills get footer. Each skill declares which.

## Skill Output Template Contract

Every skill needs one of:
- `output_template: hud` — 1-line status bar (lifecycle-aware skills)
- `output_template: footer` — skill-specific multi-line block (domain skills)
- `output_template: dashboard` — full /siterep-style expanded view (status skills)

This becomes a field in SKILL.md frontmatter. The WASM convo walker checks for it.

## Old Footer Template (for domain skills that use footer mode)

## How to Populate

| Field | Source | How to Read |
|---|---|---|
| workstream_id | `.lev/pm/workstreams/*/state/workstream.yaml` | `grep workstream_id:` |
| active_overlays | `.lev/tasks/<id>/overlays/active.yaml` OR infer from skill names in context | list plugin names contributing |
| lifecycle_stage | Current verb's lane (Shape/Plan/Exec/Close) | from `dna/vernacular.yaml lifecycle_verbs` |
| proposed_next_verb | Computed from gate state | if gate passes → next verb; if fails → remediation verb |
| current_gate | The transition gate being evaluated | from `dna/gates.yaml lifecycle section` |
| decision_point | Set by /capture, visible from then on | keep / monitor / execute / reject |

## Stats Table (optional, for /capture)

When outputting capture sweep results, use this format:

| Metric | Count |
|---|---|
| Total inventoried | N |
| In memory → needs filing | N |
| Transitioning | N |
| Blocked | N |
| Already captured | N files in {path} |

## Verb Reference

```
Shape:   /research  /prior-art  /interview
Plan:    /propose   /capture
Exec:    /exec
Close:   /qa  /accept  /handoff
Router:  /work
```

Full definitions: `dna/vernacular.yaml` section `lifecycle_verbs`
Gate math: `dna/gates.yaml` section `LIFECYCLE TRANSITION GATES`
Visual reference: https://ember-marvel-tbjh.here.now/
