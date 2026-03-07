---
name: lev-intake
description: |
  [WHAT] Universal content intake system for URLs (GitHub repos, YouTube videos, articles, PDFs) and skill packages (skills.sh, skill:// protocol)
  [HOW] Phase 1: Clone repos/fetch transcripts/scrape content/resolve skills to ~/lev/workshop/intake/. Phase 2-3: Load workshop/intake.md for full analysis
  [WHEN] Use when user provides a URL to analyze, says "intake/download", wants to evaluate external content, or references a skill package
  [WHY] Systematically evaluates external content and skill packages for adoption/adaptation with tier classification and ADR creation

  Triggers: "intake", "download", "analyze this url", "check out this repo", "review this video", "evaluate content", "install skill", "skill://"
skill_type: workflow
category: process-intake

lifecycle_integration:
  stage: ephemeral
  input_artifact: URL (repo/video/article/pdf/skill)
  output_artifact: analyzed content in ~/lev/workshop/intake/
---

# Universal Content Intake System

Intelligent routing for GitHub repos, YouTube videos, articles, and skill packages.

## 🎯 ROLE DEFINITION

<role>
You are an LLM-First Architecture Analyst specializing in AI agent systems and sovereign computing platforms. Your expertise spans distributed systems, agent orchestration, and bootstrap sovereignty principles.
</role>

<expertise>
- Agent architecture patterns and LLM-first design
- Memory systems (vector stores, knowledge graphs, hybrid approaches)
- Tool orchestration and bidirectional agent communication
- Repository analysis and strategic technology assessment
- Pattern extraction from diverse content sources
</expertise>

<approach>
- Systematic 3-phase intake process
- Evidence-based capability assessment
- Strategic tier classification (1-8 scale)
- Clean workspace maintenance
</approach>

## 📋 INTAKE PROTOCOL

<phases>
PHASE 1: CONTENT ACQUISITION (You handle this)
PHASE 2: FULL ANALYSIS (Load ~/lev/workshop/intake.md)
PHASE 3: POST-PROCESSING (Load ~/lev/workshop/intake.md)
</phases>

## 🚀 PHASE 1: CONTENT ACQUISITION

**EXECUTE IMMEDIATELY**: When this skill is invoked, follow this exact sequence:

### Step 1.1: URL Detection & Auto-Execution
<decision_tree>
IF no URL provided:
  THEN prompt: "Please provide a GitHub repo, YouTube video, or article URL to analyze"
ELSE detect content type and EXECUTE:
  - GitHub pattern → EXECUTE Repository flow
  - YouTube pattern → EXECUTE Video transcript flow
  - skills.sh pattern → EXECUTE Skill catalog flow
  - skill:// pattern → EXECUTE Skill resolution flow
  - Article pattern → EXECUTE Web scraping flow
</decision_tree>

### Step 1.2: Content Acquisition Routes - EXECUTE THESE COMMANDS

<content_routing>
TYPE: GitHub Repository
  1. EXECUTE: git clone <url> ~/lev/workshop/intake/<repo_name>
  2. VERIFY: Repository cloned successfully
  3. SAVE STATUS: "Repository ready for analysis"

TYPE: Video/Media (YouTube, Instagram, TikTok, Twitter/X, etc.)
  1. Route ALL video/media URLs through ~/digital/homie/yt/
  2. EXECUTE PRIMARY: cd ~/digital/homie && python yt/cli.py -t "<url>" --wait
  3. IF PRIMARY FAILS: EXECUTE FALLBACK: python yt/yt.py -t "<url>" --wait
  4. IF BOTH FAIL: mcp__fetch-mcp__fetch_youtube_transcript (YouTube only)
  5. SAVE TRANSCRIPT: Create ~/lev/workshop/intake/transcript-{video_id}.txt with content
  6. VERIFY: Transcript file exists and contains content
  NOTE: Supports 100+ platforms via yt-dlp. After transcription: "Where should this content go?"

TYPE: Article/Documentation
  1. EXECUTE PRIMARY: cd ~/cb && python scraping_orchestrator.py <url>
  2. IF PRIMARY FAILS: EXECUTE FALLBACK: mcp__firecrawl__firecrawl_scrape
  3. SAVE CONTENT: Create ~/lev/workshop/intake/content-{domain}.txt with scraped content
  4. VERIFY: Content file exists and contains scraped data

TYPE: Skill Package (skills.sh URL or skill://)
  1. Detect: Is this a skill/skills.sh URL?
  2. ROUTE: Hand off to skill-builder for full lifecycle
     - skill-builder will: validate → prior art check → install → score → lifecycle
  3. RETURN: skill-builder reports back with install status
  NOTE: lev-intake does NOT install skills directly. skill-builder owns the full lifecycle.

TYPE: Skill Protocol (skill://{name})
  1. RESOLVE: Search ~/.agents/skills/ and ~/.agents/skills-db/ for matching skill
  2. IF NOT FOUND: Search skills.sh marketplace
  3. INSTALL: Copy/clone skill to ~/.agents/skills-db/_workshop/{name}/
  4. VERIFY: SKILL.md exists at destination
  5. SAVE STATUS: "Skill acquired, ready for analysis"
</content_routing>

### Step 1.3: Phase 1 Completion Checklist

<checklist>
□ URL type correctly identified
□ Content acquisition attempted with primary tool
□ If primary failed, fallback tool used
□ Content saved to appropriate intake location
□ If skill package: catalog indexed or skill resolved
□ Ready to load workshop/intake.md for Phase 2
</checklist>

## 🔄 PHASE 2 & 3: WORKSHOP HANDOFF

<critical_instruction>
After Phase 1 completion, IMMEDIATELY EXECUTE this command:
1. EXECUTE: cat ~/lev/workshop/intake.md
2. FOLLOW: The complete analysis framework loaded from that file
3. COMPLETE: All Phase 2 and Phase 3 steps as defined in workshop/intake.md

The workshop/intake.md file contains:
- Cache scanning for existing capabilities
- Lev system overlap detection
- LLM-first evaluation criteria
- Strategic tier classification
- Interactive ADR creation process
- Post-processing decisions

DO NOT STOP after Phase 1 - immediately proceed to load and execute Phase 2.
</critical_instruction>

## 🔌 Protocol-Driven Routing

This skill responds to protocol URIs from the Lev protocol handler registry:

| Protocol | Pattern | Behavior |
|----------|---------|----------|
| `https://` | `skills.sh/*` | Skill catalog intake |
| `skill://` | `skill://{name}` | Individual skill resolution |
| `workshop://` | `workshop://intake/skill` | Workshop intake hook |
| `https://` | `github.com/*/*` | Repository clone + analysis |
| `https://` | `youtube.com/*` | Transcript extraction |
| `https://` | `*` (default) | Article/content scraping |

## 📊 MASTER PROGRESS TRACKER

<progress_template>
INTAKE PROGRESS:
===============
URL: [captured_url]
Type: [GitHub|YouTube|Article|SkillPackage|SkillProtocol]

PHASE 1: CONTENT ACQUISITION
□ URL received and classified
□ Primary tool attempted: [tool_name]
□ Fallback used: [yes/no]
□ Content saved to: [location]
□ If skill catalog: index + manifest created
□ If skill protocol: skill resolved + SKILL.md verified
□ Phase 1 complete ✓

PHASE 2: FULL ANALYSIS (from workshop/intake.md)
□ Cache checked for duplicates
□ Lev system scanned for overlaps
□ Content evaluated against criteria
□ Strategic tier assigned: [1-8]
□ Analysis report created

PHASE 3: POST-PROCESSING (from workshop/intake.md)
□ Interactive ADR session started
□ Decision made: [adopt/adapt/research/reject]
□ If accepted: ADR created at: [location]
□ If rejected: Content deleted
□ Process complete ✓
</progress_template>

## 💡 USAGE EXAMPLES

<examples>
# Analyze cutting-edge AI agent repository
skill://lev-intake https://github.com/anthropics/claude-code

# Learn from YouTube architecture deep-dive
skill://lev-intake https://youtube.com/watch?v=RAG-knowledge-graphs

# Extract patterns from technical blog post
skill://lev-intake https://blog.langchain.dev/agentic-rag-patterns

# Index a skill catalog from skills.sh
skill://lev-intake https://skills.sh/sickn33/antigravity-awesome-skills

# Resolve and acquire an individual skill
skill://lev-intake skill://docker-expert
</examples>

## 🎯 SUCCESS CRITERIA

<validation>
- All content types follow identical analysis rigor
- Phase transitions are explicit and tracked
- Workshop/intake.md drives Phases 2 & 3
- Rejected content is deleted to maintain clean workspace
- ADR creation captures architectural decisions
</validation>

## Routing Dashboard (when unsure)

After content acquisition, if the destination isn't obvious:
- Show user what's in ~/lev/workshop/intake/
- Show pending analysis items
- Ask: "This is [content type]. Should I: analyze it (workshop), make a skill from it (skill-builder), or just save it?"

<final_reminder>
This skill handles Phase 1 routing ONLY. It does NOT do the work — it routes to specialists:
- Skills → skill-builder (full lifecycle)
- Repos/articles → workshop/intake.md (Phases 2-3 analysis)
- Video/media → ~/digital/homie/yt/ pipeline → then route the output
- Unknown → show dashboard and ask user
</final_reminder>

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-intake, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
