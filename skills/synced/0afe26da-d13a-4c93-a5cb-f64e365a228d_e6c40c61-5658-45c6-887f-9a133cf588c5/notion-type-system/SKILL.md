---
name: notion-type-system
description: "CMS meta-layer for Kingly AI OS — manages the Notion-native type system. Provides four foundational databases (ContentTypes, FieldDefinitions, IntentRegistry, FlowMindTemplates) that make all schemas, intents, and workflow templates discoverable at runtime. Load this skill when: creating or modifying content type definitions, registering new intents, importing skill schemas into Notion, exporting type definitions to YAML, compiling FlowMind templates into executable RunPlans, or bootstrapping the CMS type system from scratch. Triggers on: content type, field definition, intent registry, flowmind template, cms boot, type system, schema import, yaml export, compile flow, run plan, skill importer, cms, ddi."
metadata:
  author: kingly-agency
  version: '1.0'
---

# Notion Type System

CMS meta-layer for the Kingly AI OS. All schemas, intents, and workflow templates live in Notion — the agent boots by reading its own definitions from these four databases instead of relying on hardcoded values in SKILL.md files.

## System Overview

```text
SKILL.md files (source of truth for authoring)
        │
        ▼  § SkillImporter
┌─── CMS Type System (Notion) ────────────────────────────┐
│  ContentTypes DB   — master registry of all types        │
│  FieldDefinitions DB — field-level schema definitions    │
│  IntentRegistry DB — registered operations               │
│  FlowMindTemplates DB — reusable workflow templates      │
└──────────────────────────────────────────────────────────┘
        │
        ▼  § CMSBootLoader
  TypeSystem object (hydrated at session start)
        │
        ▼
  All skills use CMS-loaded schemas (hardcoded = fallback)
```

## Database DDL — Four New Databases

Parent page for all four: `3189b3e2-80ff-81a8-92f4-c036f544bcaf` (Leviathan OS)

Placeholder IDs (populate after creation via § CMSBootLoader discovery):
- `<CMS_CONTENT_TYPES_DB_ID>`
- `<CMS_FIELD_DEFINITIONS_DB_ID>`
- `<CMS_INTENT_REGISTRY_DB_ID>`
- `<CMS_FLOWMIND_TEMPLATES_DB_ID>`

### ContentTypes Database

```sql
CREATE TABLE "ContentTypes" (
  "Name"            TITLE,
  "Slug"            RICH_TEXT,
  "Category"        SELECT('Core':blue, 'Lev':purple, 'Social':green, 'GTM':orange, 'Meta':red),
  "Description"     RICH_TEXT,
  "SchemaVersion"   NUMBER,
  "Fields"          RELATION → FieldDefinitions,
  "NotionDBId"      RICH_TEXT,
  "ParentPage"      RICH_TEXT,
  "LifecycleStates" RICH_TEXT,
  "Intents"         RELATION → IntentRegistry,
  "FlowTemplates"   RELATION → FlowMindTemplates,
  "Status"          SELECT('Active':green, 'Draft':yellow, 'Deprecated':orange, 'Archived':red)
)
```

**Field notes:**
- `Name` — human-readable type name, e.g., "Project", "Task", "LevEntity"
- `Slug` — URL-safe identifier used in code, e.g., "project", "lev-entity"
- `Category` — Core (Kingly operational DBs), Lev (graph layer), Social (content/CRM), GTM (sales), Meta (CMS itself)
- `LifecycleStates` — JSON array: `["Idea","Active","Paused","Shipped","Archived"]`
- `NotionDBId` — the `data_source_id` of the live Notion DB backing this type (if any)

### FieldDefinitions Database

```sql
CREATE TABLE "FieldDefinitions" (
  "Name"           TITLE,
  "ContentType"    RELATION → ContentTypes,
  "FieldType"      SELECT(
                     'title':blue, 'rich_text':default, 'select':green,
                     'multi_select':purple, 'number':orange, 'date':yellow,
                     'checkbox':red, 'url':default, 'relation':blue,
                     'files':default, 'created_time':default,
                     'status':green, 'formula':orange, 'rollup':purple
                   ),
  "Required"       CHECKBOX,
  "ValidValues"    RICH_TEXT,
  "DefaultValue"   RICH_TEXT,
  "Description"    RICH_TEXT,
  "RelationTarget" RICH_TEXT
)
```

**Field notes:**
- `ValidValues` — JSON: `["Idea","Active"]` for select/multi_select, or `{"min":0,"max":100}` for numbers
- `RelationTarget` — slug or `data_source_id` of the target DB for relation fields

### IntentRegistry Database

```sql
CREATE TABLE "IntentRegistry" (
  "Name"         TITLE,
  "Slug"         RICH_TEXT,
  "ContentType"  RELATION → ContentTypes,
  "InputSchema"  RICH_TEXT,
  "OutputSchema" RICH_TEXT,
  "GateRequired" CHECKBOX,
  "Surface"      SELECT('integration':blue, 'agent':purple, 'research':green, 'browser':orange, 'file':default, 'cli':red),
  "Description"  RICH_TEXT,
  "Status"       SELECT('Active':green, 'Draft':yellow, 'Deprecated':red)
)
```

**Field notes:**
- `Name` — intent identifier, e.g., "create_project", "advance_lifecycle", "draft_post"
- `Slug` — snake_case, e.g., "create_project"
- `InputSchema` / `OutputSchema` — JSON Schema strings
- `GateRequired` — if true, a LeaseGate artifact must be created and pass before execution
- `Surface` — which tool type executes this intent (maps to FlowMind step surfaces)

### FlowMindTemplates Database

```sql
CREATE TABLE "FlowMindTemplates" (
  "Name"               TITLE,
  "Slug"               RICH_TEXT,
  "ContentType"        RELATION → ContentTypes,
  "Version"            NUMBER,
  "FlowYAML"           RICH_TEXT,
  "CompletionCriteria" RICH_TEXT,
  "RequiredIntents"    RELATION → IntentRegistry,
  "Status"             SELECT('Active':green, 'Draft':yellow, 'Deprecated':red)
)
```

**Field notes:**
- `FlowYAML` — the full FlowMind YAML template stored as a rich_text string
- `CompletionCriteria` — prose description of what constitutes flow completion
- `RequiredIntents` — relation to all IntentRegistry entries used in this flow

---

## § CMSBootLoader

Reads the four CMS databases at session start and hydrates a TypeSystem object that all other skills use instead of hardcoded schemas.

### When to Run

- At the start of any session where entity schemas, intents, or workflows may be needed
- When kingly-ai-os v3.0 boots and the `CMS_BOOT` flag is set
- After any SkillImporter run (to refresh the in-memory TypeSystem)

### Procedure

**Step 1 — Discover DB IDs**

If the four CMS DB IDs are not yet known (first boot), search Notion for them:

```json
call_external_tool(
  source_id="notion_mcp",
  tool_name="notion-search",
  arguments={"query": "ContentTypes", "data_source_url": "collection://3189b3e2-80ff-81a8-92f4-c036f544bcaf"}
)
```

Repeat for FieldDefinitions, IntentRegistry, FlowMindTemplates. Cache the `data_source_id` values as:
- `CMS_CONTENT_TYPES_DB_ID`
- `CMS_FIELD_DEFINITIONS_DB_ID`
- `CMS_INTENT_REGISTRY_DB_ID`
- `CMS_FLOWMIND_TEMPLATES_DB_ID`

**Step 2 — Load ContentTypes**

```json
call_external_tool(
  source_id="notion_mcp",
  tool_name="notion-fetch",
  arguments={"id": "collection://<CMS_CONTENT_TYPES_DB_ID>"}
)
```

Filter to `Status = Active`. For each ContentType, extract: Name, Slug, Category, NotionDBId, LifecycleStates (parse JSON), SchemaVersion.

**Step 3 — Load FieldDefinitions (per ContentType)**

For each active ContentType, fetch its fields:

```json
call_external_tool(
  source_id="notion_mcp",
  tool_name="notion-search",
  arguments={
    "query": "<ContentType.Name>",
    "data_source_url": "collection://<CMS_FIELD_DEFINITIONS_DB_ID>"
  }
)
```

Build a field map: `{ [contentTypeSlug]: FieldDefinition[] }`

**Step 4 — Load IntentRegistry**

Fetch all `Status = Active` intents. Build intent map: `{ [slug]: IntentDefinition }`.

**Step 5 — Load FlowMindTemplates**

Fetch all `Status = Active` templates. Build template map: `{ [slug]: FlowMindTemplate }` with `FlowYAML` stored as raw string.

**Step 6 — Return TypeSystem Object**

```json
{
  "ok": {
    "data": {
      "type_system": {
        "version": "<timestamp of load>",
        "content_types": {
          "project": {
            "name": "Project",
            "slug": "project",
            "category": "Core",
            "notion_db_id": "1b09c85c-4418-4b69-9c44-6eefc7ae2c48",
            "lifecycle_states": ["Idea", "Active", "Paused", "Shipped", "Archived"],
            "schema_version": 1,
            "fields": [
              {"name": "Name", "type": "title", "required": true},
              {"name": "Status", "type": "select", "required": true, "valid_values": ["Idea","Active","Paused","Shipped","Archived"]}
            ]
          }
        },
        "intents": {
          "create_project": {
            "slug": "create_project",
            "content_type": "project",
            "gate_required": true,
            "surface": "integration"
          }
        },
        "flow_templates": {
          "propose": {
            "slug": "propose",
            "version": 1,
            "flow_yaml": "flow: propose\n..."
          }
        }
      }
    },
    "meta": {"skill": "CMSBootLoader", "operation": "boot", "correlation_id": "<uuid>"}
  }
}
```

**Step 7 — Fallback on Empty CMS**

If ContentTypes DB returns 0 records, emit `{warn: "CMS_EMPTY"}` and fall back to hardcoded schemas in kingly-ai-os. Log a LevEvent: `cms.boot.fallback`.

---

## § SkillImporter

Takes a SKILL.md file and writes its schemas into the four CMS databases, making them queryable from Notion.

### When to Run

- When onboarding a new SKILL.md into the CMS
- After editing a skill's schemas, to sync changes to Notion
- During initial CMS population (run against all existing SKILL.md files)

### Procedure

**Step 1 — Parse SKILL.md**

Read the SKILL.md file. Extract:
- **ContentTypes**: any `Database Schema` tables or explicitly named types with fields
- **Intents**: any `§`-prefixed sections (each section = one or more intents). Map section name → intent slugs using snake_case conversion.
- **FlowMind blocks**: any `flow:` YAML blocks in the file

**Step 2 — Build ContentType records**

For each identified type:

```yaml
content_type:
  name: "Project"
  slug: "project"
  category: "Core"           # infer from context
  description: "..."          # from surrounding prose
  schema_version: 1
  notion_db_id: "..."         # from Database Registry if present
  lifecycle_states: [...]     # from LifecycleStates in schema
  status: "Active"
```

**Step 3 — Write ContentType to Notion**

Check for existing entry first (RealityScan by Slug). If found, update. If not, create:

```json
call_external_tool(
  source_id="notion_mcp",
  tool_name="notion-create-pages",
  arguments={
    "parent": {"data_source_id": "<CMS_CONTENT_TYPES_DB_ID>"},
    "pages": [{"properties": {
      "Name": "Project",
      "Slug": "project",
      "Category": "Core",
      "Description": "Master project tracker",
      "SchemaVersion": 1,
      "NotionDBId": "1b09c85c-4418-4b69-9c44-6eefc7ae2c48",
      "LifecycleStates": "[\"Idea\",\"Active\",\"Paused\",\"Shipped\",\"Archived\"]",
      "Status": "Active"
    }}]
  }
)
```

**Step 4 — Write FieldDefinitions**

For each field in the ContentType:

```json
call_external_tool(
  source_id="notion_mcp",
  tool_name="notion-create-pages",
  arguments={
    "parent": {"data_source_id": "<CMS_FIELD_DEFINITIONS_DB_ID>"},
    "pages": [{"properties": {
      "Name": "Status",
      "ContentType": "[\"https://www.notion.so/<content_type_page_id>\"]",
      "FieldType": "select",
      "Required": "__YES__",
      "ValidValues": "[\"Idea\",\"Active\",\"Paused\",\"Shipped\",\"Archived\"]",
      "Description": "Current project lifecycle status"
    }}]
  }
)
```

**Step 5 — Write Intents**

For each `§` section identified as an intent:

```json
{
  "Name": "create_project",
  "Slug": "create_project",
  "ContentType": "[\"<content_type_page_url>\"]",
  "GateRequired": "__YES__",
  "Surface": "integration",
  "Description": "Create a new project entry in the Projects DB",
  "Status": "Active"
}
```

**Step 6 — Write FlowMind Templates**

For each `flow:` YAML block found:

```json
{
  "Name": "propose",
  "Slug": "propose",
  "Version": 1,
  "FlowYAML": "<full yaml string>",
  "CompletionCriteria": "entity transitions to committed",
  "Status": "Active"
}
```

**Step 7 — Return Import Summary**

```json
{
  "ok": {
    "data": {
      "skill_file": "kingly-ai-os/SKILL.md",
      "content_types_written": 12,
      "field_definitions_written": 87,
      "intents_written": 24,
      "flow_templates_written": 5
    },
    "meta": {"skill": "SkillImporter", "operation": "import", "correlation_id": "<uuid>"}
  }
}
```

---

## § FlowMindCompiler

Compiles a FlowMind YAML template from the FlowMindTemplates DB into an executable RunPlan.

### FlowMind YAML Specification

```yaml
flow: <flow_name>           # name of the workflow
entity: <entity_slug>       # the entity this flow operates on
version: <integer>          # version of this flow template
steps:
  - id: <step_id>           # unique step identifier (snake_case)
    surface: <surface>      # cli | browser | research | integration | file | agent
    action: <action_desc>   # what this step does (resolved by compiler to tool binding)
    input: <var_name>       # input variable(s) from prior steps or initial context
    output: <var_name>      # output variable(s) available to downstream steps
    gate: <gate_check>      # optional: schema_check(SchemaName) | notion_write_confirmed | human_approval
    depends_on: [step_ids]  # explicit dependencies (compiler also infers from input/output)
completion: <criteria>      # prose or structured criteria for flow completion
```

**Surface → Tool Binding:**

| Surface | Tool / Method |
|---------|--------------|
| `integration` | `call_external_tool` (Notion MCP, Gmail, Calendar) |
| `agent` | LLM reasoning step — no external tool call |
| `research` | `search_web`, `search_vertical`, `fetch_url` |
| `browser` | `screenshot_page`, browser navigation tools |
| `file` | `write`, `read`, `bash` (local file operations) |
| `cli` | `bash` command execution |

### Compiler Procedure

**Input:** FlowMind YAML string (from FlowMindTemplates.FlowYAML) + entity_slug + TypeSystem object

**Step 1 — Parse and Validate Structure**

Parse YAML. Validate:
- `flow` name is non-empty
- `entity` resolves to an entry in TypeSystem.content_types
- All `steps[].id` are unique
- All `steps[].surface` are in the valid surface set
- All `steps[].gate` references resolve to known gate types

If any validation fails: `{error: {code: "FLOW_INVALID", message: "...", context: {step_id, reason}}}`

**Step 2 — Resolve Entity**

Look up `entity` in TypeSystem.content_types. Hydrate:
- `entity_def.lifecycle_states`
- `entity_def.notion_db_id`
- `entity_def.fields`

**Step 3 — Build Dependency Graph**

For each step:
1. Collect explicit `depends_on` references
2. Infer implicit dependencies: if step B's `input` matches step A's `output`, add edge A → B
3. Build adjacency list: `{ [step_id]: [prerequisite_step_ids] }`

**Step 4 — Detect Cycles**

Run topological sort (Kahn's algorithm) on the dependency graph. If a cycle is detected:
`{error: {code: "CYCLE_DETECTED", message: "Circular dependency: stepA → stepB → stepA", context: {cycle: [...]}}}`

**Step 5 — Assign Tool Bindings**

For each step, based on `surface`:

```json
{
  "step_id": "gather_context",
  "surface": "integration",
  "tool_binding": {
    "source_id": "notion_mcp",
    "tool_name": "notion-fetch",
    "args_template": {"id": "collection://<entity.notion_db_id>"}
  },
  "gate": null
}
```

Agent steps get `"tool_binding": {"type": "llm_reasoning", "context_inputs": [...]}`.

**Step 6 — Produce RunPlan**

```json
{
  "ok": {
    "data": {
      "run_plan": {
        "flow": "propose",
        "entity": "kingly-ai-os-v3",
        "entity_def": {"slug": "lev-entity", "notion_db_id": "2d69d21d-..."},
        "version": 1,
        "execution_order": ["gather_context", "analyze_problem", "assess_risks", "define_success", "compile_proposal", "write_to_notion"],
        "steps": [
          {
            "id": "gather_context",
            "surface": "integration",
            "action": "load_context(entity_slug)",
            "input": null,
            "output": "entity_context",
            "gate": null,
            "depends_on": [],
            "tool_binding": {
              "source_id": "notion_mcp",
              "tool_name": "notion-fetch",
              "args_template": {"id": "collection://2d69d21d-df48-4dd5-a7b9-3bf6094d4764"}
            }
          },
          {
            "id": "compile_proposal",
            "surface": "file",
            "action": "assemble ProposalArtifactSchema JSON",
            "input": "problem_statement, proposed_approach, risks, success_criteria",
            "output": "proposal_artifact",
            "gate": "schema_check(ProposalArtifactSchema)",
            "depends_on": ["analyze_problem", "assess_risks", "define_success"],
            "tool_binding": {"type": "schema_assembly", "schema": "ProposalArtifactSchema"}
          }
        ],
        "completion": "entity transitions to committed",
        "compiled_at": "<ISO 8601 timestamp>"
      }
    },
    "meta": {"skill": "FlowMindCompiler", "operation": "compile", "correlation_id": "<uuid>"}
  }
}
```

**Step 7 — Gate Resolution**

For steps with `gate` specified:
- `schema_check(SchemaName)` → compiler inserts a validation micro-step before the gated step writes output
- `notion_write_confirmed` → after the integration step, compiler inserts a confirmation check on the returned page_id
- `human_approval` → compiler marks the step as `requires_pause: true`; execution halts until `confirm_action` resolves

---

## § YAMLExporter

Reads ContentTypes and FieldDefinitions from Notion CMS databases, exports to YAML files compatible with the Lev CLI/SDK.

### When to Run

- When syncing Notion CMS → local filesystem (e.g., before a Lev CLI deploy)
- When JP runs `lev types export`
- To create a backup of the current type system

### Output Format

Each ContentType exports to one YAML file at `types/<slug>.yaml`:

```yaml
name: Project
slug: project
category: Core
description: Master project tracker
schema_version: 1
notion_db_id: "1b09c85c-4418-4b69-9c44-6eefc7ae2c48"
parent_page: "1fb9b3e2-80ff-8052-858f-e606586116e3"
lifecycle_states: [Idea, Active, Paused, Shipped, Archived]
fields:
  - name: Name
    type: title
    required: true
  - name: Status
    type: select
    required: true
    valid_values: [Idea, Active, Paused, Shipped, Archived]
  - name: Priority
    type: select
    valid_values: [P0-Critical, P1-High, P2-Medium, P3-Low]
  - name: Notes
    type: rich_text
  - name: Tasks
    type: relation
    relation_target: tasks
intents:
  - create_project
  - update_project_status
  - archive_project
flow_templates:
  - propose
  - plan
  - execute
```

### Procedure

1. Run § CMSBootLoader to get the hydrated TypeSystem
2. For each ContentType in TypeSystem, build the YAML structure above
3. Write each to `/home/user/workspace/types/<slug>.yaml` using the `write` tool
4. Also write a combined `types/_index.yaml` with all slugs listed
5. Return:

```json
{
  "ok": {
    "data": {
      "exported_count": 12,
      "files": ["types/project.yaml", "types/task.yaml", "..."],
      "index": "types/_index.yaml"
    },
    "meta": {"skill": "YAMLExporter", "operation": "export", "correlation_id": "<uuid>"}
  }
}
```

---

## § YAMLImporter

Reads YAML type definition files and writes them into the Notion CMS databases.

### When to Run

- When onboarding type definitions that were authored locally (e.g., from Lev CLI scaffolding)
- After a `lev types scaffold` command produces YAML files
- To restore the CMS from a YAML backup

### Procedure

1. Read YAML files from the specified directory (default: `/home/user/workspace/types/`)
2. For each `.yaml` file (excluding `_index.yaml`), parse the YAML structure
3. Run § SkillImporter logic (Steps 3–6) to write ContentType + FieldDefinitions + Intents + FlowTemplates to Notion
4. Validate against the YAML format spec (name, slug, fields array required)
5. If parse error: `{error: {code: "YAML_PARSE_ERROR", message: "...", context: {file, line}}}`
6. Return import summary (same shape as § SkillImporter Step 7)

### Supported YAML Field Keys

| YAML Key | Maps To |
|----------|---------|
| `name` | ContentTypes.Name |
| `slug` | ContentTypes.Slug |
| `category` | ContentTypes.Category |
| `description` | ContentTypes.Description |
| `schema_version` | ContentTypes.SchemaVersion |
| `notion_db_id` | ContentTypes.NotionDBId |
| `parent_page` | ContentTypes.ParentPage |
| `lifecycle_states` | ContentTypes.LifecycleStates (JSON-encoded) |
| `fields[].name` | FieldDefinitions.Name |
| `fields[].type` | FieldDefinitions.FieldType |
| `fields[].required` | FieldDefinitions.Required |
| `fields[].valid_values` | FieldDefinitions.ValidValues (JSON-encoded) |
| `fields[].default_value` | FieldDefinitions.DefaultValue |
| `fields[].description` | FieldDefinitions.Description |
| `fields[].relation_target` | FieldDefinitions.RelationTarget |
| `intents[]` | IntentRegistry.Slug (must already exist or be created) |
| `flow_templates[]` | FlowMindTemplates.Slug (must already exist or be created) |

---

## Governance

- CMS databases are Meta-category — never delete records, only Deprecate/Archive
- All writes to CMS databases pass through RealityScan → LeaseGate → NotionWriter
- Schema changes increment SchemaVersion on the ContentType record
- FlowMind templates are versioned — create new records, never overwrite FlowYAML on existing Active records
- SkillImporter is idempotent — re-running against the same SKILL.md updates existing records (by Slug match) rather than duplicating
- All CMS operations emit LevEvents to the Event Log with source = "notion-type-system"
