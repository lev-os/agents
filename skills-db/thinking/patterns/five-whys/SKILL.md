---
name: five-whys
description: Uncover root causes by iteratively asking why a problem occurred, moving from symptoms to underlying system failures
---

# Five Whys

## Overview
Developed by Sakichi Toyoda and Taiichi Ohno at Toyota, the Five Whys is a root cause analysis technique that asks "why?" five times (or until reaching root cause) to move from problem symptoms to underlying system failures. Each answer forms the basis of the next "why?" The method reveals that surface problems (machine stopped) often trace to systemic issues (no maintenance strainer).

## When to Use
- Recurring problems that keep coming back despite fixes
- Symptoms being treated instead of root causes
- Need to move from blame to systemic understanding
- Team jumping to solutions before understanding problem
- Expensive failures requiring investigation
- Simple problems where heavy analysis frameworks are overkill

## The Process

### Step 1: Define the Problem Clearly
Write a specific, observable problem statement. Avoid vague language. Bad: "Quality is poor." Good: "Product X failed QA inspection 3 times this week due to misaligned components."

**Example:** "The website went down for 2 hours on Tuesday afternoon, affecting 10,000 users."

### Step 2: Assemble People Close to the Work
Gather those directly involved in the process—they have the detailed knowledge. Don't rely solely on management perspectives removed from day-to-day reality.

**Example:** Include the on-call engineer who responded, the developer who deployed, and the QA tester who reviewed the change.

### Step 3: Ask "Why?" and Document Answers
Ask why the problem occurred. Each answer becomes the input for the next "why?" Don't accept vague answers—push for specific, verifiable causes.

**Example:**
- **Problem**: Website went down
- **Why?** Database connection pool exhausted
- **Why?** Connection leak in new user authentication code
- **Why?** Code review didn't catch resource management bug
- **Why?** Code reviewers lack training on connection pooling patterns
- **Why?** No onboarding process for distributed systems concepts

### Step 4: Stop at the Root Cause
Continue asking until reaching a root cause you can act on. Signs you've hit root: answer is a process gap, missing system, or design flaw—not a person or one-time event.

**Example:** Root cause is "No onboarding process for distributed systems concepts," not "Developer made a mistake" (blame) or "Connection leaked" (symptom).

### Step 5: Implement System-Level Countermeasures
Fix the root cause, not the symptom. Verify the fix prevents recurrence, not just the specific instance.

**Example:** Countermeasure: Create distributed systems onboarding with connection pooling best practices, add automated tests for resource leaks, update code review checklist. Result: No further connection pool failures.

## Classic Taiichi Ohno Example

**Problem**: Machine stopped working

1. **Why?** Overload, fuse blew
2. **Why?** Bearing not sufficiently lubricated
3. **Why?** Lubrication pump not pumping sufficiently
4. **Why?** Pump shaft worn and rattling
5. **Why?** No strainer attached, metal scraps got in

**Root Cause**: Missing strainer (design/process flaw)
**Countermeasure**: Install strainer on all lubrication pumps

## Example Application

**Situation:** E-commerce company experiences spike in customer service complaints about late deliveries.

**Application:**
1. **Why are deliveries late?** Warehouse picking delays
2. **Why are picks delayed?** Inventory locations incorrect in system
3. **Why are locations incorrect?** Returns not scanned to proper shelf
4. **Why aren't returns scanned?** Scanners frequently dead or missing
5. **Why are scanners dead?** No charging station in returns area

**Root Cause**: Missing infrastructure (charging station), not "lazy workers"

**Countermeasure**: Install 5 charging stations in returns area, add scanner battery checks to opening checklist, train returns team on scan importance

**Outcome**: Late deliveries drop 60%, complaints fall 75%, warehouse productivity increases 20%.

## Anti-Patterns
- ❌ Stopping at blame ("Because Bob made a mistake")—root causes are systemic
- ❌ Accepting vague answers ("Bad communication")—push for specifics
- ❌ Treating 5 as magic number—stop when you hit root, might be 3 or 7
- ❌ Using technique for complex problems with multiple causes (use fishbone instead)
- ❌ Implementing fixes for symptoms (earlier whys) instead of root cause
- ❌ Conducting Five Whys alone—need diverse perspectives

## Related
- root-cause-analysis
- fishbone-diagram
- systems-thinking
- feedback-loops
