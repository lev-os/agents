---
name: cook-vs-chef
description: Distinguish between reasoning by analogy (following recipes) and reasoning from first principles (creating recipes) to identify innovation opportunities
---

# Cook vs. Chef Mental Model

## Overview
Tim Urban's "Cook vs. Chef" mental model, from his Wait But Why analysis of Elon Musk's thinking, distinguishes between two modes of reasoning. Cooks follow recipes—working from existing templates, best practices, and what others have done. Chefs reason from raw ingredients—understanding fundamentals deeply enough to create new recipes. Most people are cooks most of the time, using "recipes" handed to them. Innovators shift into chef mode when creating something genuinely new.

## When to Use
- Evaluating whether you're copying or innovating
- Team defaulting to "industry best practices" without questioning
- Distinguishing incremental improvement from breakthrough thinking
- Assessing whether conventional approaches are limiting you
- Deciding when to follow proven patterns vs. forge new paths
- Identifying areas requiring chef thinking vs. where cook thinking suffices

## The Process

### Step 1: Identify Your Current Mode
Recognize whether you're in cook mode (following templates, copying competitors, applying best practices) or chef mode (reasoning from fundamentals, creating novel approaches). Most decisions don't require chef mode.

**Example:** Building a SAAS checkout flow? Cook mode is fine—use Stripe, follow e-commerce patterns. Creating a new marketplace model? Chef mode needed.

### Step 2: Determine If the Problem Needs a Chef
Ask: Does this require genuine innovation, or is proven approach sufficient? Chef thinking is mentally exhausting—reserve it for problems where conventional solutions fail or where breakthroughs create massive value.

**Example:** Tesla couldn't buy batteries good enough for 300-mile range at acceptable cost. No recipe existed. Chef mode required: design battery packs from cell-level physics upward.

### Step 3: If Cook Mode, Find the Best Recipe
Research thoroughly, understand proven approaches, and adapt intelligently. Don't reinvent wheels. Excellence in execution matters more than novelty for most problems.

**Example:** Building authentication? Follow OAuth 2.0 standards, use Auth0 or similar. Don't create custom security—the recipe exists and works.

### Step 4: If Chef Mode, Return to Ingredients
Strip away all recipes and conventions. Understand the fundamental components (the "ingredients"), the constraints (physics, economics, human behavior), and reason upward from there.

**Example:** SpaceX chef-mode thinking: Ingredients = aluminum, titanium, fuel, physics of thrust. Constraints = escape velocity, atmospheric drag. Question everything: Why are rockets disposable? Because we accept the recipe "too hard to land them." But physics allows controlled descent...

### Step 5: Know When to Switch Modes
Throughout execution, toggle between modes. Use chef thinking to design architecture, cook thinking to implement components. Use recipes for solved problems, invent for unsolved ones.

**Example:** Amazon: Chef mode on AWS (no cloud computing recipe existed). Cook mode on retail logistics (apply Walmart/FedEx learnings). Chef mode on recommendation engines (no recipe for scale). Cook mode on UI patterns (established e-commerce conventions).

## Classic Tim Urban Example

**Situation:** Conventional wisdom says rockets are expensive and disposable because landing them is prohibitively difficult.

**Cook Thinking:** "Every aerospace company disposes of rockets. That must be the right approach. We should optimize disposable rocket design like everyone else."

**Chef Thinking:** "Raw ingredients: rockets are metal tubes filled with fuel. Physics: controlled thrust can decelerate and land. Why do we accept disposal? That's convention, not physical law. Can we design for reusability from first principles?"

**Result:** Elon Musk's chef-mode reasoning led to reusable Falcon 9 boosters—impossible according to conventional recipes, routine in physics-based thinking.

## Example Application

**Situation:** Startup building project management software sees incumbents using per-seat pricing.

**Cook Approach:**
"Everyone does per-seat pricing. Let's copy that model with 20% lower prices to compete."

**Result:** Commodity positioning, price-based competition, low differentiation.

**Chef Approach:**
"Ingredients: people collaborate in teams with varying activity levels. Convention: charge equally for all seats. But core constraint: some users need full access, others just need visibility. What if pricing matched actual usage patterns instead of following SaaS convention?"

**Result:** Usage-based pricing innovation (like Slack's MAU model), better aligns cost with value, competitive differentiation.

## When to Be a Cook

Use cook mode (follow recipes) when:
- Proven solutions exist and work well
- Problem is not your core differentiation
- Time/resources don't justify reinvention
- Industry standards provide network effects (OAuth, APIs, etc.)
- Risk of failure is high (security, compliance, safety)

**Example:** Most startups should use AWS (recipe) not build datacenters (chef mode). Use React (recipe) not create new UI framework. Use SQL databases (recipe) not invent new database engines.

## When to Be a Chef

Use chef mode (invent recipes) when:
- No good solution exists for your specific constraint
- Conventional approaches systematically fail
- Breakthrough creates massive competitive advantage
- You have unique insight others lack
- Core differentiation requires novel approach

**Example:** Google needed to index billions of pages—no database recipe existed at that scale, so they invented BigTable and MapReduce from first principles.

## Anti-Patterns
- ❌ Being a chef everywhere (exhausting, wasteful, "not invented here" syndrome)
- ❌ Being a cook everywhere (never innovating, permanent commodity status)
- ❌ Confusing contrarianism with chef thinking (different ≠ first principles)
- ❌ Dismissing all recipes as inferior (many are battle-tested and superior)
- ❌ Using "chef mode" to justify poor execution ("we're innovating" as excuse for broken product)
- ❌ Failing to recognize when your "new recipe" is worse than the existing one

## Related
- first-principles-reasoning
- inversion
- second-order-thinking
- reasoning-by-analogy
- innovation-vs-imitation
- build-vs-buy
