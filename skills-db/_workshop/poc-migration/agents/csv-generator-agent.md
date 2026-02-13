Create `agents/csv-generator-agent.md`:

```markdown
# CSV Generator Agent - Domain Framework Extraction

## Your Role
Read a domain.md file and extract all mentioned frameworks into task.csv with accurate classification.

## Input
- Domain directory (e.g., `docs/domains/04-decision-making/`)
- Contains: `domain.md` (extracted content from seed docs)

## Your Task
Read domain.md, identify every framework mentioned, classify each one, generate task.csv.

### Step 1: Read Domain File (5 min)
```bash
cat docs/domains/04-decision-making/domain.md
```

Understand:
- What frameworks are explicitly named
- What frameworks are mentioned in lists (e.g., "9 Scenario planning techniques")
- What descriptions exist for each

### Step 2: Extract Frameworks (15 min per domain)

For each framework you find:

**Identify**:
- Framework name (exact)
- Is it described in detail or just mentioned?
- Who is the author/source (if mentioned)?

**Classify Status**:
- **KNOWN**: Has multi-paragraph description + examples + steps/process described
  - Example: "TRIZ 40 Inventive Principles - Soviet engineering framework based on 200,000 patents. 40 principles including: Segmentation, taking out, asymmetry, nested doll..."
- **VAGUE**: Has concept explanation but missing actionable steps
  - Example: "OODA Loop - Boyd Cycle for competitive dynamics (Observe, Orient, Decide, Act)"
- **UNKNOWN**: Just name or one-liner
  - Example: "9 Scenario planning techniques" or "Morphological Analysis"

**Classify Detail Level**:
- **detailed**: Multiple paragraphs, examples, steps
- **partial**: Paragraph with concept but no steps
- **one-liner**: Just name or single sentence mention

**Extract Source Hint**:
- Look for author names: "Charlie Munger", "Donella Meadows", "Philip Tetlock"
- Look for book mentions: "Thinking in Systems", "Superforecasting"
- Format: "Author - Book/Context" or just "Author"

**Assign Priority**:
- **high**: Mentioned prominently, has source, appears in multiple places
- **medium**: Standard framework mention
- **low**: Obscure or tangential mention

### Step 3: Build CSV (10 min)

Track each framework as you read:

```csv
id,framework_name,track,status,detail_level,source_hint,priority,score,yaml_path,notes
1,"First Principles Thinking",mental-models,KNOWN,detailed,"Aristotle/Elon Musk",high,0,,"Break down to fundamental truths"
2,"Five Whys",mental-models,VAGUE,partial,"Sakichi Toyoda - Toyota",medium,0,,"Root cause technique"
3,"Scenario Planning Techniques",mental-models,UNKNOWN,one-liner,"Shell method mentioned",high,0,,"9 techniques but not detailed"
```

### Step 4: Determine Track
- Domains 01-08: `track = "mental-models"`
- Domains 09-15: `track = "practitioner-frameworks"`

### Step 5: Write CSV File
```bash
# Create CSV with header
echo "id,framework_name,track,status,detail_level,source_hint,priority,score,yaml_path,notes" > docs/domains/04-decision-making/task.csv

# Add each framework row
# Use proper CSV escaping for commas in notes
```

### Quality Guidelines

**Do**:
- Read the entire domain.md carefully
- Extract every framework mentioned, even brief ones
- Be conservative with KNOWN status (requires real detail)
- Note when framework is part of a list (e.g., "9 techniques")
- Use exact framework names as written

**Don't**:
- Invent framework names not in the text
- Mark as KNOWN if no actionable steps present
- Skip frameworks that seem minor (include everything)
- Guess at sources not mentioned in text

### Example Scenarios

**Scenario 1**: "Porter's Five Forces - Competitive analysis framework (threats, bargaining power, rivalry, substitutes, barriers)"
- Status: VAGUE (concept listed but no process)
- Detail: partial
- Source: "Michael Porter"

**Scenario 2**: Just text saying "strategic frameworks include SWOT, PESTLE, BCG Matrix"
- Create 3 separate rows, all UNKNOWN, one-liner

**Scenario 3**: Full paragraph explaining OODA Loop with 4 steps detailed
- Status: KNOWN
- Detail: detailed
- Extract steps into notes

### Output Format

CSV file with:
- Header row
- One row per framework
- All fields filled (use empty string "" if unknown)
- Proper CSV escaping (quotes around fields with commas)

Report back with:
- Domain processed
- Number of frameworks extracted
