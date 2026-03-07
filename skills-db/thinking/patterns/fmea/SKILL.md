---
name: fmea
description: Systematically identify potential failure modes, assess their severity and likelihood, and prioritize preventive actions using risk priority numbers
---

# FMEA (Failure Mode Effects Analysis)

## Overview
FMEA is a systematic, proactive method for evaluating processes to identify where and how they might fail and assessing the relative impact of different failures. Developed in aerospace/automotive industries, FMEA calculates Risk Priority Numbers (RPN = Severity × Occurrence × Detection) to prioritize which failures to prevent first.

## When to Use
- Designing new products, processes, or systems
- Launching critical features with high failure cost
- Incident post-mortems to prevent recurrence
- Evaluating vendor/supplier reliability
- Improving manufacturing quality
- Pre-launch risk assessment

## The Process

### Step 1: Identify Potential Failure Modes
List all ways the system could fail. For each component/process step, ask: "What could go wrong?"

**Example:** E-commerce checkout process failure modes: payment gateway timeout, inventory out of sync, address validation fails, credit card decline, email confirmation fails.

### Step 2: Assess Severity (1-10 Scale)
Rate impact if failure occurs. 1 = no impact, 10 = catastrophic. Focus on customer/business impact, not technical complexity.

**Example:** Payment gateway timeout: Severity = 9 (lost revenue, customer frustration). Email confirmation fails: Severity = 3 (inconvenient but order proceeds).

### Step 3: Assess Occurrence (1-10 Scale)
Rate likelihood of failure happening. 1 = rare, 10 = inevitable. Base on data if available, educated guess if not.

**Example:** Payment timeout: Occurrence = 2 (gateway 99.5% uptime). Email fails: Occurrence = 4 (email service less reliable).

### Step 4: Assess Detection (1-10 Scale)
Rate likelihood of catching failure before customer impact. 1 = always detected, 10 = never detected until customer complains.

**Example:** Payment timeout: Detection = 3 (monitoring alerts immediately). Email fails: Detection = 8 (no monitoring, customer must report).

### Step 5: Calculate RPN and Prioritize
RPN = Severity × Occurrence × Detection. Higher RPN = higher priority. Focus mitigations on highest RPNs first.

**Example:**
- Payment timeout: 9 × 2 × 3 = 54 RPN
- Email fails: 3 × 4 × 8 = 96 RPN → Prioritize email monitoring despite lower severity

### Step 6: Implement Actions and Reassess
Design mitigations to reduce Severity (safer failure mode), Occurrence (prevent failure), or Detection (catch earlier). Recalculate RPN after mitigation.

**Example:** Add email delivery monitoring (Detection 8 → 2). New RPN: 3 × 4 × 2 = 24 (acceptable).

## Example Application

**Situation:** SaaS company launching new API with high-value enterprise customers.

**Failure Modes Analysis**:
1. API returns 500 errors: S=10, O=3, D=2 → RPN=60
2. Response time >5sec: S=7, O=5, D=4 → RPN=140
3. Authentication fails: S=9, O=2, D=3 → RPN=54
4. Rate limiting blocks requests: S=8, O=6, D=7 → RPN=336

**Prioritization**: Address rate limiting first (RPN=336), then response time (RPN=140).

**Mitigations**:
- Rate limiting: Per-customer limits (O: 6→2), monitoring alerts (D: 7→2) → New RPN=32
- Response time: Database indexing (O: 5→2), performance monitoring (D: 4→1) → New RPN=14

**Outcome:** Launch succeeds, no customer-facing failures. Prevented potential churn.

## Anti-Patterns
- ❌ Skipping low-severity, high-occurrence issues (death by a thousand cuts)
- ❌ Rating based on technical complexity vs. customer impact
- ❌ Ignoring detection rating (undetected failures multiply impact)
- ❌ Treating FMEA as one-time exercise vs. living document
- ❌ Analysis paralysis (don't FMEA every trivial process)
- ❌ Confusing RPN with absolute risk (RPN is relative prioritization tool)

## Related
- five-whys
- fishbone-diagram
- root-cause-analysis
- risk-management
- pre-mortem
