---
name: fishbone-diagram
description: Visually map all potential causes of a problem across structured categories to systematically identify root causes through team collaboration
---

# Fishbone Diagram (Ishikawa)

## Overview

The Fishbone Diagram (also called Ishikawa Diagram or Cause-and-Effect Diagram) is a visual root cause analysis tool created by Kaoru Ishikawa for quality defect prevention. The diagram resembles a fish skeleton: the problem (effect) is the "head" on the right, and potential causes branch off the "spine" like bones, organized into major categories.

Unlike linear techniques like 5 Whys, the Fishbone structures brainstorming across multiple dimensions simultaneously. This prevents tunnel vision and reveals interactions between cause categories. It's particularly powerful for complex problems with multiple contributing factors across systems, processes, and human elements.

## When to Use

- Complex problems with multiple potential causes across different domains
- Team needs to brainstorm comprehensively without fixating on one causal path
- Quality defects in manufacturing, service delivery, or product development
- You need visual documentation of root cause analysis for stakeholders
- Cross-functional teams are investigating process breakdowns
- Combining with Six Sigma, Lean, or continuous improvement initiatives
- Preventing recurrence by identifying all contributing factors, not just the primary cause

## The Process

### Step 1: Define the Problem Statement (Fish Head)

Write the specific problem in a box on the right side. Be precise and measurable.

**Example:** "Server downtime exceeded 2 hours on Dec 1, 2025"

### Step 2: Draw the Spine and Select Categories (Major Bones)

Draw a horizontal line (spine) from the problem. Branch major categories off the spine.

**Manufacturing (6 M's):** Man/Manpower, Machine, Method, Material, Measurement, Mother Nature (Environment)
**Service/IT (4 P's):** People, Process, Platform, Policy
**General (4 S's):** Surroundings, Suppliers, Systems, Skills

### Step 3: Brainstorm Causes for Each Category

For each major category, ask "What factors in this category could cause the problem?" List sub-causes as smaller branches.

**Example (Server downtime - Platform category):**
- Outdated server OS
- Insufficient capacity planning
- No redundancy
- Database not optimized

### Step 4: Drill Deeper - Ask "Why?" for Each Cause

For significant sub-causes, add smaller branches asking why that cause exists.

**Example:** "Outdated OS" → Why? → "No patch schedule" → Why? → "No assigned owner"

### Step 5: Identify Root Causes Through Pattern Recognition

Look for causes appearing in multiple categories or chains that terminate in systemic issues.

**Root pattern:** Multiple branches point to "No documented procedures" and "No ownership assigned"

### Step 6: Validate and Prioritize Root Causes

Use data to confirm which identified causes actually contributed. Prioritize based on impact.

**Validation:** Check logs - outdated OS contributed; environmental causes did not.

### Step 7: Develop Action Plan for Root Causes

Create interventions targeting validated root causes across all relevant categories.

**Actions:** Assign platform owner, create patch schedule, document change procedures, add monitoring

## Example Application

**Situation:** Automotive manufacturer experiencing paint defects on vehicle doors.

**Application:**
- **Machine:** Spray nozzle worn, temperature inconsistent, timer calibration off
- **Method:** New procedure not documented, training incomplete, inconsistent application
- **Material:** Paint batch variability, thinner ratio incorrect, storage temperature fluctuates
- **Man:** High turnover, rushed work, lack of experience
- **Measurement:** Quality checks skipped, no statistical process control
- **Environment:** Humidity fluctuates, dust in paint booth, seasonal temperature swings

**Outcome:** Diagram revealed root cause cluster: lack of environmental controls + undocumented procedures + insufficient training. Addressed all three systemically - defect rate dropped 85%.

## Anti-Patterns

- ❌ Using generic categories without tailoring to your problem domain
- ❌ Stopping at surface-level causes without asking "why?" deeper
- ❌ One person creating the diagram instead of collaborative team brainstorming
- ❌ Listing causes without validating with data which actually contributed
- ❌ Creating a beautiful diagram but never implementing solutions
- ❌ Ignoring causes that appear across multiple categories (often the systemic root)
- ❌ Treating all causes as equal instead of prioritizing by impact

## Related

- 5-whys (iterative root cause questioning technique)
- pareto-analysis (80/20 prioritization of causes)
- fault-tree-analysis (deductive failure analysis)
- process-mapping (visualizing workflows to identify breakdowns)
- six-sigma-dmaic (data-driven improvement framework)
