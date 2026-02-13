---
name: kano-model
description: Customer satisfaction framework that categorizes product features into five types based on their relationship to user delight and investment
---

# Kano Model

## Overview

The Kano Model, developed by Dr. Noriaki Kano in 1984, challenges the assumption that customer satisfaction has a linear relationship with feature investment. This framework reveals that different feature types create fundamentally different satisfaction curves: some features are expected (absence creates dissatisfaction), others scale linearly with quality, and some create outsized delight. The model categorizes features into five types: Must-Be (basic requirements), One-Dimensional (performance features), Attractive (delighters), Indifferent (irrelevant), and Reverse (unwanted by some segments). By surveying customers with functional/dysfunctional question pairs, teams can classify features and make strategic trade-offs about where to invest limited resources.

## When to Use

- Prioritizing feature roadmap when resources are constrained
- Deciding whether to invest in table stakes, performance improvements, or innovation
- Understanding why customers aren't satisfied despite adding features they requested
- Segmenting customers by their different satisfaction drivers
- Preventing feature bloat by identifying indifferent attributes
- Planning MVP scope (include only Must-Be features, one Attractive delighter)
- Competitive analysis to identify where competitors are vulnerable

## The Process

### Step 1: Identify Features to Evaluate

List 10-20 product attributes or potential features to assess. Focus on meaningful capabilities, not implementation details. Include existing features (to validate assumptions) and proposed features (to guide roadmap). Include features competitors have that you don't. **Example:** For email client: "Search messages", "Dark mode", "AI-powered sorting", "Read receipts", "Custom swipe actions".

### Step 2: Design Functional and Dysfunctional Question Pairs

For each feature, create two questions. Functional: "How would you feel if this feature was present?" Dysfunctional: "How would you feel if this feature was absent?" Use standard five-option scale: I like it, I expect it, I'm neutral, I can tolerate it, I dislike it. **Example:** Functional: "How would you feel if the app had AI-powered email sorting?" Dysfunctional: "How would you feel if the app did NOT have AI-powered email sorting?"

### Step 3: Survey Active Users (Minimum 30, Target 100+)

Send survey to users who have used product at least twice in past 14 days. Random sampling across customer segments. Anonymous responses reduce social desirability bias. Takes 5-7 minutes per respondent. **Example:** SaaS company surveys 150 active users across free, pro, and enterprise tiers.

### Step 4: Classify Each Response Using Kano Evaluation Table

Cross-reference functional vs. dysfunctional answers using standard classification matrix. Must-Be: customer expects it (functional: neutral/like, dysfunctional: dislike). One-Dimensional: satisfaction scales with quality (functional: like, dysfunctional: dislike). Attractive: unexpected delight (functional: like, dysfunctional: neutral/tolerate). Indifferent: doesn't matter (functional: neutral, dysfunctional: neutral). Reverse: causes dissatisfaction (functional: dislike). **Example:** User answers "I expect it" (functional) and "I dislike it" (dysfunctional) = Must-Be classification.

### Step 5: Calculate Category Distribution Per Feature

For each feature, count percentage of responses in each category. Assign feature to dominant category (mode). If split between categories, segment customers differently value the feature. Threshold: 50%+ in one category = clear classification. **Example:** "AI sorting" results: 45% Attractive, 35% One-Dimensional, 15% Indifferent, 5% Must-Be. Classification: Attractive (plurality), but segment analysis needed.

### Step 6: Plot Features on Kano Diagram

Create 2D plot with Implementation Investment (X-axis) and Customer Satisfaction (Y-axis). Must-Be features: high dissatisfaction when absent, neutral when present (horizontal line at 0). One-Dimensional: diagonal line from dissatisfied to satisfied. Attractive: neutral when absent, high satisfaction when present (exponential curve). Indifferent: flat line at neutral. **Example:** Email search plots as Must-Be (expected), AI sorting as Attractive (delighter), custom fonts as Indifferent.

### Step 7: Make Strategic Investment Decisions

Prioritize Must-Be features first (prevent dissatisfaction). Invest in One-Dimensional features where competitors are weak (differentiation). Add one Attractive feature per release (create delight). Eliminate or deprioritize Indifferent features (waste of resources). Investigate Reverse features for market segmentation opportunity. **Example:** Roadmap: Fix slow search (Must-Be), improve attachment handling (One-Dimensional), add AI sorting (Attractive), remove clutter features (Indifferent).

## Example Application

**Situation:** B2B project management tool evaluating 12 features for next quarter's roadmap. Engineering capacity for 3 major features. Need to balance customer retention (satisfaction with basics) and growth (delighters for new customers).

**Application**: Survey 120 active users across small business and enterprise segments. Key findings:

| Feature | Category | Small Business | Enterprise | Decision |
|---------|----------|----------------|------------|----------|
| Real-time collaboration | Must-Be | 85% | 92% | Fix latency issues (P0) |
| Mobile app parity | Must-Be | 78% | 65% | Bring iOS to web feature parity (P0) |
| Advanced permissions | One-Dimensional | 35% | 88% | Enterprise differentiator (P1) |
| AI task suggestions | Attractive | 62% | 58% | Build for delight (P1) |
| Gantt charts | One-Dimensional | 45% | 72% | Enterprise ask (P2) |
| Custom themes | Indifferent | 55% | 48% | Deprioritize (P3) |

**Outcome:** Q1 roadmap: (1) Fix real-time collaboration latency (Must-Be retention issue), (2) Advanced permissions (One-Dimensional enterprise driver + competitive gap), (3) AI task suggestions (Attractive cross-segment delighter). Custom themes moved to backlog despite 12 customer requests. Segment analysis revealed enterprise customers value permissions 3x more than small business.

## Anti-Patterns

- Surveying prospects instead of active users (they don't understand current state)
- Using vague feature descriptions (respondents interpret differently)
- Skipping dysfunctional questions to save time (can't classify without both)
- Sample size under 30 (statistically unreliable distribution)
- Treating all Must-Be features equally (some are more critical than others)
- Building every Attractive feature found (resources finite, prioritize impact)
- Ignoring segment differences (B2B vs. B2C often classify same features differently)
- One-time analysis without re-running (features decay: Attractive → One-Dimensional → Must-Be over time)

## Related

- RICE Prioritization - quantifies priority after Kano identifies feature type
- Jobs to Be Done - helps identify features to evaluate with Kano
- North Star Metric - Kano insights should connect to moving North Star
- Value Proposition Canvas - Kano identifies which pains/gains matter most
- Product-Market Fit Survey - Kano explains why PMF is achieved or missing
- Feature Voting - Kano reveals why voting alone misleads (confuses Must-Be with Attractive)
- Competitive Analysis - Kano categories reveal competitor vulnerabilities
