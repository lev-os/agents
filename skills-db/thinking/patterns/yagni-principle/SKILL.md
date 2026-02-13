---
name: yagni-principle
description: Build only what you need now, not what you think you'll need later - avoid speculative features
---

# YAGNI (You Aren't Gonna Need It)

## Overview

YAGNI is a principle from Extreme Programming (XP) stating "don't add functionality until it's actually needed." Coined by Kent Beck during the C3 project, the mantra arose when developers proposed building capabilities for anticipated future requirements. Beck's response: "You aren't gonna need it." The principle combats speculative generality - building features, abstractions, or infrastructure based on imagined future needs that often never materialize.

YAGNI addresses the cost of premature optimization and over-engineering. Every line of code written carries maintenance burden: it must be understood, tested, debugged, and updated when requirements change. Building features "just in case" wastes time on code that may never be used, and worse, creates complexity that slows down implementing features you actually need. Studies show 64% of features are rarely or never used.

The principle operates in tension with architectural planning - you can't build a skyscraper by adding floors later. YAGNI applies to features and abstractions, not foundational architecture. It works best with continuous refactoring, automated testing, and incremental design. The discipline is saying "no" to your engineering instincts when they whisper "but what if we need to support 17 payment providers someday?" Build for today's requirements with clean, refactorable code that can evolve tomorrow.

## When to Use

- Planning feature development roadmaps - resist building "nice to have" features
- Designing abstractions and frameworks - avoid generality beyond current needs
- Code reviews when teammate proposes "future-proofing" without concrete requirement
- Choosing between simple implementation and complex flexible system
- Evaluating third-party dependencies - do you need all 47 features?
- Refactoring decisions - wait for proven need before adding indirection layers
- Prioritizing technical work - defer infrastructure until feature demands it

## The Process

### Step 1: Identify Current vs. Speculative Requirements

Separate features you need now from features you think you might need later. Challenge assumptions about future needs.

**Ask:** "Is this required for current sprint? Is there a committed customer or business case?"

**Current requirement:** User authentication for beta customers launching next month.

**Speculative:** OAuth integration for Google/Facebook (no customer requested, "might want later").

**Decision:** Build email/password auth now. Add OAuth when customer requests it.

### Step 2: Implement Simplest Solution for Current Need

Choose the straightforward implementation that solves today's problem without premature generalization.

**Ask:** "What's the simplest code that satisfies current requirements while remaining clean and refactorable?"

**Example:** Need to send email notifications.
- **YAGNI approach:** Use SMTP library, hardcode email provider credentials in config
- **Over-engineered:** Build email provider abstraction layer supporting SMTP, SendGrid, Mailgun, SES with plugin architecture (when you only use one provider)

**Outcome:** Working email in 1 hour vs. 2 days building unused abstraction.

### Step 3: Maintain Clean, Refactorable Code

While avoiding speculative features, write clean code that's easy to change when requirements evolve.

**Ask:** "If requirements change, can I refactor this in reasonable time?"

**YAGNI doesn't mean bad code:** Write tests, use descriptive names, keep functions small, follow SOLID principles. Just don't add unused features.

**Trade-off:** Simple implementation with good structure beats complex flexible system that's never used.

### Step 4: Defer Until Proven Necessary

When tempted to build for future, defer and revisit when concrete need arises. Track deferred ideas for later evaluation.

**Ask:** "What's the cost of adding this later if needed?"

**Example:** Database schema supports single currency. "But we might expand internationally!"
- **YAGNI:** Implement single currency now. Track "multi-currency support" in backlog. Add when first international customer signs.
- **Cost of deferral:** 2-3 days migration work when needed
- **Benefit:** 1 week saved now, possible that international expansion never happens

**Pattern:** Many anticipated needs never materialize. Build when you have evidence.

### Step 5: Refactor When Requirements Actually Change

When deferred need becomes actual requirement, refactor existing code to support it.

**Ask:** "Now that we need this feature, what's the incremental path from current state?"

**Example:** Third customer requests Google OAuth - now justified.
- Refactor authentication to interface
- Implement OAuth provider
- Migration time: 1 day (vs. 2 days building speculatively before)

**XP practice:** Continuous refactoring makes this affordable. Automated tests give confidence.

### Step 6: Balance with Architecture Decisions

Distinguish features (YAGNI applies) from foundational architecture (requires foresight).

**Features (apply YAGNI):** Payment providers, export formats, notification channels - add when needed

**Architecture (requires planning):** Database choice, monolith vs. microservices, programming language - high cost to change later

**Ask:** "Is this a feature I can add incrementally, or foundational choice that's expensive to reverse?"

### Step 7: Cultivate Team Discipline

Build team culture that resists gold-plating and feature creep. Make YAGNI part of code review culture.

**Code review questions:**
- "Is this used in current sprint?"
- "Can we defer this until concrete requirement?"
- "What's simplest implementation that works?"

**Celebrate:** Praise developers who ship simple solutions over those who build complex unused systems.

## Example Application

**Situation:** Building API for mobile app. Engineer proposes GraphQL with full schema, subscriptions, batching, caching layer. Current need: 4 simple REST endpoints for authentication and profile management.

**YAGNI Application:**
- **Analysis:** GraphQL adds 2 weeks development time. Current app needs 4 endpoints, no complex querying, no real-time updates.
- **Decision:** Build REST endpoints. Takes 2 days. Defer GraphQL.
- **Implementation:** Clean REST design with versioning. Well-tested, documented.
- **Refactoring capability:** If future need demands GraphQL, existing endpoints provide reference implementation. Migration feasible.
- **Outcome (6 months later):** App launched successfully. GraphQL never needed - REST endpoints sufficient. Saved 2 weeks that were spent on actual user-requested features. App now has 50k users.

**Outcome:** Shipping simple solution enabled faster iteration on actual user feedback. Time saved on unused complexity invested in features users wanted.

## Anti-Patterns

- Building plugin architecture when you have one plugin and no roadmap for more
- Creating abstraction layers for "flexibility" without concrete variation points
- Implementing features because they're "cool" or good for portfolio, not business need
- Adding configuration options for every hardcoded value "just in case"
- Building entire CRUD API for tables that only need one endpoint
- Selecting enterprise-grade infrastructure for MVP with 10 users
- Dismissing YAGNI as "not thinking ahead" - it's thinking economically about present vs. future

## Related

- dry-principle (balance - don't abstract until third use, don't build until first use)
- continuous-refactoring (enables YAGNI by making future changes affordable)
- mvp-methodology (apply YAGNI at product level)
- incremental-design (build architecture as needs emerge)
- technical-debt (YAGNI prevents speculative debt, but refactoring prevents reckless debt)
- kiss-principle (Keep It Simple, Stupid - complementary to YAGNI)
- lean-development (eliminate waste, including unused features)
