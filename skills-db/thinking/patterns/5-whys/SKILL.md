---
name: 5-whys
description: Ask "why?" five times to drill past symptoms and surface-level causes to reveal the true root cause of a problem
---

# 5 Whys

## Overview

The 5 Whys is an iterative interrogative technique developed by Sakichi Toyoda in the 1930s and formalized by Taiichi Ohno at Toyota Motor Corporation as a cornerstone of the Toyota Production System. The method explores cause-and-effect relationships by repeatedly asking "why?" (typically five times) until the root cause emerges. The number five is not rigid - continue until you reach a systemic root cause rather than a symptom.

Ohno called it "the basis of Toyota's scientific approach" to problem-solving. The technique is deceptively simple but powerful: each answer becomes the basis for the next question, creating a chain of causation that reveals where intervention will have lasting impact rather than temporary fixes.

## When to Use

- A problem keeps recurring despite multiple "fixes" (symptom treatment, not root cause)
- You need quick root cause analysis without complex statistical tools
- Simple to moderately complex problems with human/process factors
- Team needs shared understanding of why a failure occurred
- Manufacturing defects, process breakdowns, or organizational issues
- You suspect the obvious answer masks a deeper systemic issue

## The Process

### Step 1: Define the Problem Precisely

State the problem as a specific, observable fact. Avoid vague descriptions.

**Example:** "The machine stopped working at 2:15 PM on Line 3" (not "machines are unreliable")

### Step 2: Ask "Why Did This Happen?" - First Why

Answer based on facts, not speculation. Gather data from people who witnessed the problem.

**Example:** Why did the machine stop? → The motor overheated and the thermal fuse blew.

### Step 3: Ask "Why?" of the Previous Answer - Second Why

Take the first answer and ask why that condition existed.

**Example:** Why did the motor overheat? → The bearing was not sufficiently lubricated.

### Step 4: Continue the Chain - Third, Fourth, Fifth Whys

Keep drilling down. Each answer should point to a more fundamental cause.

**Example (Ohno's classic):**
- Why wasn't it lubricated? → The lubrication pump wasn't pumping sufficiently.
- Why wasn't it pumping? → The pump shaft was worn and rattling.
- Why was the shaft worn? → No strainer was attached; metal scraps got in.

### Step 5: Identify the Root Cause and Implement Systemic Fix

The final "why" reveals the root cause. Fix this, not the symptoms.

**Root cause:** No strainer on pump intake
**Fix:** Install strainer + add inspection checklist for all pumps

### Step 6: Verify the Fix Prevents Recurrence

Test that addressing the root cause eliminates the problem completely.

**Verification:** Run machine for 100 hours with new strainer - no lubrication failures.

## Example Application

**Situation (Taiichi Ohno, Toyota):** Machine stopped on production line.

**Application:**
1. Why stopped? → Overload blew the fuse
2. Why overload? → Bearing not lubricated
3. Why not lubricated? → Pump not pumping sufficiently
4. Why not pumping? → Pump shaft worn and rattling
5. Why shaft worn? → No strainer; metal scraps got in

**Outcome:** Root cause identified as missing strainer. Installing strainers across all pumps prevented recurrence. Without 5 Whys, they would have replaced the fuse (symptom) and the problem would repeat.

## Anti-Patterns

- ❌ Stopping at symptom-level answers ("the fuse blew" - replace fuse without asking why)
- ❌ Accepting opinions instead of facts ("someone was careless" vs. "no checklist exists")
- ❌ Using 5 Whys for highly complex problems requiring statistical analysis
- ❌ Rigidly asking exactly five questions when root cause appears at question 3 or requires 7
- ❌ Working alone instead of gathering the team closest to the problem
- ❌ Jumping to solutions before completing the causal chain
- ❌ Blaming people rather than identifying systemic/process failures

## Related

- fishbone-diagram (visual root cause analysis with categorized causes)
- fault-tree-analysis (deductive failure analysis for complex systems)
- pre-mortem (imagining failure before it happens)
- inversion (identifying what would cause failure)
- second-order-thinking (tracing consequences beyond first level)
