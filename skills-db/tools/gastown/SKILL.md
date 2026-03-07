---
name: gastown
description: Execute multi-agent workflows from YAML definitions. Claude Code IS the runtime - reads workflow, creates artifacts, dispatches agents via Task tool.
when_to_use: When running agency workflows, CDO orchestration, or any multi-agent task defined in YAML
category: orchestration
version: 1.0.0
---

# Gastown - Multi-Agent Workflow Executor

**You ARE the runtime.** Read the YAML, create artifacts, dispatch agents.

## Core Pattern

```
1. Load workflow YAML (context:// or file path)
2. mkdir -p tmp/<workflow>-<timestamp>/
3. echo "user input" > tmp/.../00-input.md
4. For each turn:
   - Dispatch agents via Task tool (parallel or sequential)
   - Each agent reads assigned input, writes output
   - Sync: verify outputs exist
5. Final synthesis reads all artifacts
```

## Loading Workflows

### From Agency (context://)
```bash
# List available workflows
node core/index/src/protocols/context-resolver.js list agency

# Resolve to path
node core/index/src/protocols/context-resolver.js path context://agency/workflows/brand-identity-lifecycle

# Load content
node core/index/src/protocols/context-resolver.js resolve context://agency/workflows/brand-identity-lifecycle
```

### From File
Just read the YAML directly: `~/k/hub/agency/contexts/workflows/*.yaml`

## Execution Protocol

### Step 1: Create Artifact Directory
```bash
WORKFLOW="brand-identity"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DIR="tmp/${WORKFLOW}-${TIMESTAMP}"
mkdir -p "$DIR"
```

### Step 2: Write Input
Write `00-input.md` with:
- User's request
- Client context (if applicable)
- Relevant background

### Step 3: Parse Workflow YAML

Key sections to extract:
- `iteration_cycles` or `turns` - execution phases
- `consciousness_streams` or `agents` - who does what
- `quality_gates` - confidence thresholds
- `ceo_orchestration` - synthesis rules

### Step 4: Dispatch Agents

**For each turn/cycle:**

```
Use Task tool with subagent_type based on role:
- brand_strategist → general-purpose
- voice_specialist → general-purpose
- visual_designer → general-purpose
- ceo (synthesis) → general-purpose with opus model

Each agent prompt includes:
1. Their role from workflow
2. Input file(s) to read
3. Output file to write
4. Thinking patterns to apply
5. Quality criteria to meet
```

**Parallel execution:** Launch multiple Task calls in single message
**Sequential execution:** Wait for each to complete

### Step 5: Agent I/O Pattern

Each agent:
1. **Reads** assigned input file(s) from tmp/
2. **Writes** their output to assigned file
3. **Never** sees other agents' concurrent work
4. **Expresses** confidence/uncertainty in output

File naming:
- `00-input.md` - original input
- `01-discovery-brand-strategist.md` - first turn, first agent
- `01-discovery-voice-specialist.md` - first turn, second agent (parallel)
- `02-synthesis-ceo.md` - CEO synthesis of turn 1
- `FINAL-deliverable.md` - final output

### Step 6: Quality Gates

After each turn, check:
- Do all expected output files exist?
- Do agents express sufficient confidence?
- Are collaboration needs addressed?

If gates fail:
- Request additional iteration
- CEO intervention for conflicts
- Escalate to human if deadlocked

### Step 7: CEO Synthesis

The CEO agent (you, running as orchestrator, OR a dispatched opus agent):
- Reads ALL artifacts from previous turn
- Synthesizes into coherent direction
- Makes proceed/revise/pivot decision
- Writes synthesis to next input

## Client Integration

### Client Folder Format

Agency clients follow this structure:

```bash
~/k/hub/agency/clients/<client-name>/
├── client.yaml              # Client config (name, status, features, etc.)
├── client-brief.md          # Project brief (problem, solution, audience)
├── context/                 # Background information
├── consciousness-streams/   # Specialist thinking artifacts
├── deliverables/            # Organized outputs
│   ├── brand/
│   ├── marketing/
│   ├── operations/
│   └── ux/
└── tmp/                     # CDO working artifacts (auto-created)
```

### Loading a Client

```bash
CLIENT="agenticseo"
CLIENT_PATH="$HOME/k/hub/agency/clients/$CLIENT"

# Load client config
cat "$CLIENT_PATH/client.yaml"

# Load brief
cat "$CLIENT_PATH/client-brief.md"

# Create working directory
WORKFLOW="brand-identity"
TIMESTAMP=$(date +%Y-%m-%dT%H-%M-%S)
mkdir -p "$CLIENT_PATH/tmp/$WORKFLOW-$TIMESTAMP"
```

### Client Input Template

Include client context in `00-input.md`:

```markdown
# Workflow Input

## Client: {client.name}
{client-brief.md content}

## User Request
{user's specific request}

## Workflow: {workflow_name}
{workflow description}
```

### Deliverables Routing

Final artifacts go to the appropriate client deliverable folder:
- Brand → `deliverables/brand/`
- Marketing → `deliverables/marketing/`
- UX → `deliverables/ux/`
- Operations → `deliverables/operations/`

---

## CDO Analysis Pattern

For multi-agent analysis workflows, use the **numbered role pattern**:

```
tmp/<workflow>-<timestamp>/
├── 00-input.md
├── cdo-analysis-1-{role-a}.md      # First analyst
├── cdo-analysis-2-{role-b}.md      # Second analyst
├── cdo-analysis-3-{role-c}.md      # Third analyst
├── cdo-analysis-4-{role-d}.md      # Fourth analyst
├── cdo-final-recommendations.md    # Individual recommendations merged
├── cdo-synthesis-consolidated.md   # CEO synthesis of all analyses
├── README.md                       # Workflow documentation
└── work-<timestamp>                # Metadata/logs (optional)
```

### Example: CDO Analysis Workflow

```yaml
workflow: cdo-analysis
turns:
  - turn: 1
    parallel: true
    agents:
      - step: 1
        role: protocol-architect
        output: cdo-analysis-1-protocol-architect.md
        lens: "Protocol design, API boundaries, communication patterns"
      - step: 2
        role: type-systematist
        output: cdo-analysis-2-type-systematist.md
        lens: "Type safety, schema design, data contracts"
      - step: 3
        role: hook-integrator
        output: cdo-analysis-3-hook-integrator.md
        lens: "Event hooks, side effects, lifecycle integration"
      - step: 4
        role: simplicity-advocate
        output: cdo-analysis-4-simplicity-advocate.md
        lens: "Complexity reduction, YAGNI, minimal viable approach"

  - turn: 2
    agents:
      - step: final
        role: ceo
        inputs: ["cdo-analysis-*.md"]
        output: cdo-final-recommendations.md

  - turn: 3
    agents:
      - step: synthesis
        role: ceo
        inputs: ["cdo-final-recommendations.md"]
        output: cdo-synthesis-consolidated.md
```

### Agent Roles (CDO Analysis)

| Role | Lens | Focus |
|------|------|-------|
| protocol-architect | System boundaries | APIs, protocols, communication |
| type-systematist | Type safety | Schemas, contracts, validation |
| hook-integrator | Side effects | Events, hooks, lifecycle |
| simplicity-advocate | Complexity | YAGNI, minimal, pragmatic |
| ceo | Synthesis | Final decision, trade-offs |

## Example: Brand Identity Lifecycle

```yaml
# Load workflow
workflow = context://agency/workflows/brand-identity-lifecycle

# Execution:
Turn 1 (Discovery - Parallel):
  - Agent: brand_strategist → 01-discovery-strategist.md
  - Agent: voice_specialist → 01-discovery-voice.md

Turn 2 (CEO Synthesis):
  - Agent: ceo → 02-ceo-synthesis.md (reads 01-*)

Turn 3 (Concept Development - Sequential):
  - Agent: visual_designer → 03-concept-visual.md
  - Agent: brand_strategist → 03-concept-validation.md
  - Agent: voice_specialist → 03-concept-voice.md

Turn 4 (CEO Decision):
  - If quality_gates pass → proceed to refinement
  - If fail → additional iteration

Turn 5 (Refinement):
  - Agent: creative_director → 04-refinement.md
  - Agent: guidelines_manager → 04-implementation.md

Turn 6 (Final):
  - Agent: ceo → FINAL-brand-identity.md
```

## Agent Prompt Template

```markdown
You are the {role} agent in the "{workflow}" workflow.

## Your Role
{role_description from workflow YAML}

## Input
Read and analyze: {input_files}

## Thinking Patterns
Apply: {thinking_patterns from workflow}

## Output
Write your analysis to: {output_file}

Include:
- Your reasoning process
- Confidence levels (0-1)
- Uncertainties/unknowns
- Collaboration needs (what you need from other agents)
- Quality self-assessment

## Quality Criteria
{quality_gates from workflow}

---
Input content follows:
{actual file contents}
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Create JavaScript per workflow | Read YAML, dispatch via Task tool |
| Orchestrator synthesizes | Dispatch CEO agent to synthesize |
| Agents share context | Each reads/writes disk only |
| Custom runtime framework | Claude Code IS the runtime |
| Over-engineer infrastructure | mkdir + Task tool + md files |

## Agency Paths

```bash
AGENCY_ROOT="$HOME/k/hub/agency"

# Workflows (29 YAML definitions)
$AGENCY_ROOT/contexts/workflows/

# Clients
$AGENCY_ROOT/clients/
├── agenticseo/     # First production client
├── mpos/           # Mobile POS project
└── mpos2/          # MPOS v2

# Patterns & Templates
$AGENCY_ROOT/contexts/patterns/
$AGENCY_ROOT/contexts/templates/

# Claude-Flow Agents (54 agent definitions)
$AGENCY_ROOT/claude-flow/

# Config Templates
$AGENCY_ROOT/config/
├── master_template.yaml
├── stealth_startup.yaml
└── verification_needed.yaml
```

## Quick Start: AgenticSEO

```bash
# 1. Load client
cat ~/k/hub/agency/clients/agenticseo/client.yaml
cat ~/k/hub/agency/clients/agenticseo/client-brief.md

# 2. Create work directory
mkdir -p ~/k/hub/agency/clients/agenticseo/tmp/brand-$(date +%Y%m%d-%H%M%S)

# 3. Write input
cat > ~/k/hub/agency/clients/agenticseo/tmp/brand-.../00-input.md << 'EOF'
# Brand Identity Workflow

## Client: AgenticSEO
(paste client-brief.md)

## Request
Create brand identity foundation...
EOF

# 4. Load workflow
cat ~/k/hub/agency/contexts/workflows/brand-identity-lifecycle.yaml

# 5. Execute (Claude Code IS the runtime)
# Dispatch agents via Task tool, write artifacts to tmp/
```

## Related

- **Workflows:** ~/k/hub/agency/contexts/workflows/ (29 workflows)
- **Clients:** ~/k/hub/agency/clients/ (agenticseo, mpos, mpos2)
- **Claude-Flow Agents:** ~/k/hub/agency/claude-flow/ (54 agents)
- **Config Templates:** ~/k/hub/agency/config/
- **Context Resolver:** core/index/src/protocols/context-resolver.js
- **BD-CDO Skill:** skills/bd-cdo/SKILL.md
- **BD Epic:** lev-8wkh
