---
name: user-research-methodologies
description: Systematic approaches for discovering user needs, behaviors, and pain points through interviews, testing, observation, and surveys
---

# User Research Methodologies

## Overview

User research methodologies are systematic approaches to understanding user behaviors, needs, motivations, and contexts through various qualitative and quantitative techniques. As defined by Nielsen Norman Group, UX research can be positioned along three dimensions: Attitudinal vs. Behavioral (what people say vs. what they do), Qualitative vs. Quantitative (depth vs. scale), and Generative vs. Evaluative (discovery vs. validation). The goal is to inform design decisions with evidence rather than assumptions, using the right method at the right stage of product development.

## When to Use

- Beginning new product development to discover unmet user needs (generative)
- Validating design concepts before investing in full development (evaluative)
- Understanding why users behave in certain ways (qualitative)
- Measuring task success rates or satisfaction scores at scale (quantitative)
- Identifying usability problems in existing products
- Creating user personas, journey maps, or mental models
- Prioritizing features based on actual user needs rather than stakeholder opinions

## The Process

### Step 1: Define Research Questions and Choose Method Type

Articulate what you need to learn and select appropriate attitudinal/behavioral and qualitative/quantitative methods. **Example:** Question: "Why do users abandon checkout?" Choose Behavioral + Qualitative = Usability Testing and Session Recording Analysis.

### Step 2: Conduct User Interviews (Generative, Qualitative, Attitudinal)

Perform 1-on-1 conversations to explore user needs, pain points, and mental models. **Example:** 10 interviews with target users, 45-60 minutes each, semi-structured questions about current workflow pain points, recorded and transcribed for analysis.

### Step 3: Execute Usability Testing (Evaluative, Qualitative, Behavioral)

Observe users attempting realistic tasks with your product to identify usability issues. **Example:** 5 participants perform "find and purchase product" task while thinking aloud, facilitator notes friction points, measures task completion rate and time-on-task.

### Step 4: Deploy Surveys (Attitudinal, Quantitative)

Collect structured feedback from large sample sizes for statistical significance. **Example:** Post-purchase survey (n=500) using System Usability Scale (SUS) and Net Promoter Score (NPS), 5-point Likert scales, multiple-choice questions for demographics.

### Step 5: Perform Field Studies / Contextual Inquiry (Generative, Qualitative, Behavioral)

Observe users in their natural environment to understand context and workarounds. **Example:** Shadow 6 nurses during hospital shifts, observe EMR system usage in actual clinical context, identify interruptions and workarounds not visible in lab setting.

### Step 6: Conduct Card Sorting (Generative/Evaluative, Qualitative, Behavioral)

Understand user mental models for information organization and navigation. **Example:** Give 15 participants 50 content cards, ask them to group and name categories (open sort), validate proposed IA structure (closed sort), analyze with clustering software.

### Step 7: Analyze and Synthesize Findings

Identify patterns across research data, prioritize insights by frequency and severity, translate to actionable recommendations. **Example:** Affinity diagramming of interview notes reveals 3 major themes, usability test videos coded for error types, survey data analyzed for statistical significance, findings compiled into research report with prioritized recommendations.

## Example Application

**Situation:** Healthcare scheduling app has 2.1 star rating and declining usage, but team doesn't understand root causes.

**Application:**
- User Interviews (n=12): Discovered patients confused by medical terminology, feared scheduling wrong appointment type
- Usability Testing (n=8): 87% struggled to reschedule appointments, 62% couldn't find cancellation policy
- Field Study (n=4): Observed patients at clinic trying to use app while stressed, multi-tasking, interrupted by staff
- Survey (n=350): Quantified that 68% preferred phone scheduling despite app availability, SUS score of 48/100 (below average)
- Card Sort (n=15): Revealed users organized appointments by body system (cardiology, orthopedics) not by clinic location (current design)

**Synthesis:** Primary issues were (1) unclear appointment type selection, (2) hidden rescheduling function, (3) stressful usage contexts requiring simpler UI.

**Outcome Post-Redesign:** App rating increased to 4.3 stars, active users grew 140%, phone call volume decreased 35%, SUS score improved to 76/100.

## Anti-Patterns

- Testing with 1-2 users and treating findings as representative of all users
- Leading questions in interviews that bias responses ("Don't you think this design is intuitive?")
- Usability testing without realistic tasks in realistic contexts
- Confusing attitudinal data (what users say) with behavioral data (what users do)
- Running research without clear questions, resulting in unfocused findings
- Skipping synthesis and jumping directly from data collection to design solutions
- Using only quantitative methods without understanding the "why" behind numbers
- Recruiting participants who don't match target user profile (employees, friends)

## Related

- Nielsen Norman Group Research Framework - Dimensional classification of methods
- Jobs To Be Done - Understanding user motivations and goals
- User Personas - Research-derived user archetypes
- Journey Mapping - Visualizing user experience over time
- Affinity Diagramming - Synthesis technique for qualitative data
- System Usability Scale (SUS) - Standardized usability questionnaire
- Ethnographic Research - Deep observational studies in context
- A/B Testing - Quantitative method for comparing design variants
