---
name: lev-intake
description: "Config-driven workshop intake for URLs, repos, media, PDFs, and skill packages. Use when user wants intake, download, or external content analyzed with project playbooks."
skill_type: workflow
category: process-intake

lifecycle_integration:
  stage: ephemeral
  input_artifact: URL (repo/video/article/pdf/skill)
  output_artifact: canonical workshop analysis written to the resolved analysis destination
---

# Config-Driven Workshop Intake

Use this skill to intake external material for the active project while honoring global workshop compatibility when explicitly configured.

## Primary Rule

**Never hardcode workshop paths.**

Always resolve:
1. active project root
2. merged workshop config
3. workshop manifest
4. configured playbooks

## Role

You are a project-grounded intake analyst.

You:
- acquire external material cleanly
- compare it to the active project's actual needs
- preserve workshop compatibility through config overlays
- recommend the smallest useful disposition

## Phase 0: Resolve Project + Workshop Context

Execute these steps first:

### 0.1 Resolve project root

- `git rev-parse --show-toplevel`

Set:
- `PROJECT_ROOT=<git root>`

### 0.2 Load overlay config

Read, in this order:
- global: `~/.config/lev/config.yaml`
- project: `<projectRoot>/.lev/config.yaml`

Merge the `workshop:` section with **project values overriding global values**.

### 0.3 Resolve workshop paths

Use this resolution order:

1. `workshop.root`
   - if absolute, use as-is
   - if relative, resolve from `PROJECT_ROOT`
   - if missing, default to `<projectRoot>/.lev/workshop`

2. `workshop.manifest`
   - if set, resolve it
   - else default to `<workshopRoot>/manifest.yaml`

3. `workshop.playbooks.repo_intake`
4. `workshop.playbooks.papers_intake`

### 0.4 Load manifest if present

If `<workshopManifest>` exists, load it and use it to resolve folder names such as:
- intake
- analysis
- approved
- extract
- cache
- papers
- reports
- transcripts
- reference

If no manifest exists, default folder names are:
- `intake`
- `analysis`
- `approved`
- `extract`
- `cache`
- `papers`
- `reports`
- `transcripts`
- `_ref`

### 0.5 Load project docs

Required:
- `<projectRoot>/AGENTS.md`

Preferred:
- `<projectRoot>/docs/NORTH_STAR.md`
- `<projectRoot>/docs/01-architecture.md`
- `<projectRoot>/docs/00-process.md`

If the project-specific context paths are configured under `workshop.context`, use those first.

Fail fast only if:
- `AGENTS.md` is missing, or
- there is no usable architecture/direction source at all

### 0.6 Load relevant local skills

If project-local skills are relevant, load them before analysis.

Example:
- OpenClaw-adjacent repo inside KinglyAssistant → load `<projectRoot>/.agents/skills/openclaw/SKILL.md`

## KinglyAssistant Defaults

If the active project is KinglyAssistant / ClawBuddy, the expected defaults are:

- workshop root: `.lev/workshop/`
- workshop manifest: `.lev/workshop/manifest.yaml`
- canonical analysis: `.lev/workshop/analysis/<slug>/analysis.md`
- guide: `AGENTS.md`
- product direction: `docs/NORTH_STAR.md`
- architecture: `docs/01-architecture.md`
- process: `docs/00-process.md`

For KinglyAssistant, evaluate external work against:
- macOS installer and gateway lifecycle
- iOS chat, voice, pairing, and session UX
- shared Swift packages and test harnesses
- OpenClaw wrapper/integration strategy
- ClawBuddy/companion UX and product polish
- bundles, marketplace, and tooling

## Phase 1: Acquire Content

### URL Detection

If no URL is provided, ask for one.

If provided, classify as:
- GitHub repo
- video/media
- article/documentation
- skills.sh / skill package
- `skill://`

### GitHub Repository

Clone into:
- `<workshopRoot>/<folders.intake>/<repo_name>`

Then:
- verify with `ls -la`
- identify top-level structure
- identify stack + test/build entrypoints

### Video / Media

Route through:
- `~/digital/homie/yt/cli.py`
- fallback `~/digital/homie/yt/yt.py`

Save transcript to:
- `<workshopRoot>/<folders.intake>/<slug>/transcript.md`

### Article / Documentation

Route through:
- local scraper first
- web scrape fallback second

Save content to:
- `<workshopRoot>/<folders.intake>/<slug>/article.md`

### Skill Package / `skill://`

Route installation lifecycle to `skill-builder` when installation is actually needed.

This skill's job is relevance assessment for the active project.

## Phase 2: Analyze

### If a repo-intake playbook is configured

If `workshop.playbooks.repo_intake` is set and exists:
- load it
- follow it after acquisition

### If a papers-intake playbook is configured

If the target is paper/media heavy and `workshop.playbooks.papers_intake` is set:
- load it
- follow it for paper-oriented analysis

### If no playbook is configured

Analyze against the active project's own docs and structure.

Required reads:
- project guide
- north star if present
- architecture if present
- process doc if present
- target repo README
- package/manifest files
- 3-5 core implementation files

Answer with evidence:
1. What problem does this solve?
2. Which part of the active project does it map to?
3. Is it product, infrastructure, integration, or tooling?
4. Does it conflict with current architecture or constraints?
5. Is the value in adoption, extraction, monitoring, or simple awareness?

### Recommended Multi-Agent Split

Use sub-agents in parallel when practical:
- `context-scan`: project docs + architecture + tier mapping
- `repo-scan`: target repo purpose, stack, capabilities
- `fit-scan`: overlap, gaps, and disposition

Each sub-agent must return:
- executive brief
- manifest of files touched
- saved report path only if detail would exceed 5000 tokens

## Phase 3: Disposition

Use project-specific decisions:

- `integrate`
  - strong fit for roadmap or architecture

- `extract`
  - valuable patterns, not a direct dependency

- `monitor`
  - interesting, not aligned enough right now

- `pass`
  - low fit or redundant

- `vendor`
  - near-term explicit reason to vendor code into `vendor/`

## Output Artifacts

Write the final report to:
- `<workshopRoot>/<folders.analysis>/<slug>/analysis.md`

The report must include:
- target URL
- resolved project root
- resolved workshop root
- resolved manifest path
- configured playbook inputs
- staged source path
- project context used
- decision
- rationale
- next action

## Output Template

```markdown
# Intake Report: <name>

- URL: <url>
- Type: <repo|video|article|skill>
- Project Root: <project root>
- Workshop Root: <workshop root>
- Workshop Manifest: <manifest path or missing>
- Repo Playbook: <path or null>
- Papers Playbook: <path or null>
- Staged Source: <path>
- Analysis Path: <path>

## Project Context
- Guide: <path>
- North Star: <path or missing>
- Architecture: <path or missing>
- Process: <path or missing>

## External Summary
- Purpose:
- Stack:
- Key capabilities:

## Fit For Current Project
- Surface:
- Tier:
- Relevant overlaps:
- Conflicts:

## Decision
- Decision:
- Why:
- Recommended next step:
```

## Hook-Envelope Bridge (from Clawhip, Wave 4 — cw-03)

When intaking repos that emit hook events (OMC/OMX, GitHub Actions, CI systems), use this envelope contract to normalize inbound hook payloads before routing through the intake pipeline:

```json
{
  "source_agent": "omx",
  "event_type": "hook.triggered",
  "payload": {
    "hook_name": "post-commit",
    "repo": "...",
    "data": {}
  },
  "timestamp": "2026-01-01T00:00:00Z",
  "session_id": "..."
}
```

The envelope wraps any external hook source. `source_agent` lets downstream consumers filter by origin. `event_type` follows `hook.<action>` naming and feeds into Lev's LevEvent router after deserialization.

Use this pattern for intake flows that forward hook events between runtimes (e.g., OMC → Lev → downstream analysis). The envelope is the seam — not the hook implementation.

Source: `.lev/pm/parity/clawhip.yaml`

## Success Criteria

- Workshop paths come from merged config, not hardcoded defaults
- Manifest-driven folder resolution works when present
- Legacy Lev workflow remains possible through global config
- Project-local workshop defaults work when no global override exists
- Canonical analysis is written to the resolved `analysis/` destination

## Notes

- Default behavior for most repos should remain `<projectRoot>/.lev/workshop`.
- For Lev itself, repo-local overlays can point `workshop.root` at `workshop/` while preserving the global default.
- For project repos, default to `<projectRoot>/.lev/workshop`.
- A checked-in workshop manifest plus gitignored runtime folders is the intended shape for project-local workshop state.
