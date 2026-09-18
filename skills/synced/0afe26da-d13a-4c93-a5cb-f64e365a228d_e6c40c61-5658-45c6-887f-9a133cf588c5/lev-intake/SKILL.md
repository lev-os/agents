---
name: lev-intake
description: "Config-driven content intake system for GitHub repos, videos, articles, PDFs, and skill packages. Acquires content, analyzes against project playbooks, and recommends disposition (integrate/extract/monitor/pass/vendor). Triggers on: intake, download, analyze this url, check out this repo, review this video, evaluate content, install skill, skill://"
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
- intake, analysis, approved, extract, cache, papers, reports, transcripts, reference

If no manifest exists, default folder names are:
- `intake`, `analysis`, `approved`, `extract`, `cache`, `papers`, `reports`, `transcripts`, `_ref`

### 0.5 Load project docs

Required:
- `<projectRoot>/AGENTS.md`

Preferred:
- `<projectRoot>/docs/NORTH_STAR.md`
- `<projectRoot>/docs/01-architecture.md`
- `<projectRoot>/docs/00-process.md`

If the project-specific context paths are configured under `workshop.context`, use those first.

### 0.6 Load relevant local skills

If project-local skills are relevant, load them before analysis.

## Phase 1: Acquire Content

### URL Detection

If no URL is provided, ask for one.

If provided, classify as:
- GitHub repo → clone into `<workshopRoot>/<folders.intake>/<repo_name>`
- Video/media → route through `~/digital/homie/yt/cli.py`, save transcript
- Article/documentation → scrape, save to intake
- Skill package / `skill://` → route to skill-builder for installation

## Phase 2: Analyze

### If a playbook is configured, follow it after acquisition.

### If no playbook is configured

Analyze against the active project's own docs and structure. Answer with evidence:
1. What problem does this solve?
2. Which part of the active project does it map to?
3. Is it product, infrastructure, integration, or tooling?
4. Does it conflict with current architecture or constraints?
5. Is the value in adoption, extraction, monitoring, or simple awareness?

## Phase 3: Disposition

- `integrate` — strong fit for roadmap or architecture
- `extract` — valuable patterns, not a direct dependency
- `monitor` — interesting, not aligned enough right now
- `pass` — low fit or redundant
- `vendor` — near-term reason to vendor code into `vendor/`

## Output

Write final report to `<workshopRoot>/<folders.analysis>/<slug>/analysis.md` with: URL, type, project root, workshop root, staged source, project context, decision, rationale, next action.
