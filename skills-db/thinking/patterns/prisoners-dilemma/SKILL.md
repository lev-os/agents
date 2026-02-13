---
name: prisoners-dilemma
description: Recognize situations where individual rational choices lead to collectively worse outcomes - core model for cooperation vs. defection dynamics
---

# Prisoner's Dilemma

## Overview

The Prisoner's Dilemma is the foundational game theory model explaining why rational self-interest can produce collectively irrational outcomes. Two prisoners, interrogated separately, each face a choice: cooperate (stay silent) or defect (confess). If both cooperate, light sentences for both. If one defects while the other cooperates, the defector walks free while the cooperator gets maximum sentence. If both defect, moderate sentences for both. The tragic equilibrium: both defect, despite mutual cooperation being better for everyone.

This structure appears everywhere in business: price wars where both competitors lose, arms races in features, tragedy of commons in shared resources, and trust breakdowns in partnerships. Understanding the dilemma reveals when competition is self-defeating and what mechanisms enable cooperation.

## When to Use

- Pricing strategy: deciding whether to cut prices when competitors might retaliate
- Market competition: recognizing when price/feature wars destroy industry profitability
- Partnerships and joint ventures: structuring agreements that prevent defection
- Resource sharing: commons problems where individual exploitation depletes shared assets
- Team dynamics: situations where individual credit-seeking undermines collective outcomes
- Contract negotiations: anticipating where parties might renege on commitments

## The Process

### Step 1: Identify the Dilemma Structure

Confirm the situation has Prisoner's Dilemma characteristics: two or more actors, cooperation and defection options, and the specific payoff ranking.

**Core payoff structure (ranked best to worst):**
1. Defect while others cooperate (temptation payoff - best individual outcome)
2. Mutual cooperation (reward payoff - best collective outcome)
3. Mutual defection (punishment payoff - stable but suboptimal)
4. Cooperate while others defect (sucker payoff - worst individual outcome)

**Confirming the dilemma:**
- Temptation > Reward > Punishment > Sucker's payoff
- Defection is dominant strategy for each player in isolation
- Mutual defection is Nash Equilibrium but Pareto inferior to mutual cooperation

### Step 2: Assess Whether Game is One-Shot or Repeated

The fundamental dynamics change between single interaction and ongoing relationship.

**One-shot games:**
- Defection is rational (no future punishment possible)
- Cooperation requires external enforcement (contracts, reputation)
- Common in: one-time transactions, anonymous interactions

**Repeated games (Iterated Prisoner's Dilemma):**
- Future retaliation changes calculus
- Cooperation can emerge without external enforcement
- Shadow of the future enables trust

### Step 3: Evaluate Cooperation-Enabling Mechanisms

For repeated games, determine what strategies and structures enable cooperative outcomes.

**Successful strategies (from Axelrod's tournaments):**
- **Tit-for-Tat:** Start cooperating, then mirror opponent's last move. Simple, forgiving, retaliatory.
- **Grim Trigger:** Cooperate until first defection, then defect forever. Harsh but stable.
- **Generous Tit-for-Tat:** Occasional forgiveness prevents death spirals from mistakes.

**Structural enablers:**
- Transparency (observe defection quickly)
- Frequent interaction (more chances to punish/reward)
- Long time horizons (future matters enough to discipline present)
- Communication (coordinate on mutual cooperation)

### Step 4: Design for Cooperation or Protect Against Defection

Either change the game structure to enable cooperation or protect yourself from exploitation.

**Changing the game:**
- Create binding commitments (contracts with penalties)
- Build reputation stakes (defection damages brand)
- Establish communication channels (explicit coordination)
- Increase transparency (actions visible to all parties)

**Protection strategies:**
- Limit downside from partner defection (diversification)
- Build in verification mechanisms (audits, escrow)
- Structure phased commitments (small steps, trust-building)

## Example Application

**Situation:** Two dominant airlines on a route, both considering fare cuts.

**Application:**
- **Cooperate:** Maintain $400 fares, both profit $100M/year
- **Defect:** Cut to $300 fares
- **If both defect:** Both profit only $40M/year (price war)
- **If one defects:** Defector gains $130M, cooperator drops to $30M

**Dilemma confirmed:** Defection dominates for each airline individually, but mutual defection destroys $120M of industry profit.

**Solution applied:** Airlines recognize iterated game. Establish price leadership patterns where one signals changes, other follows. Implicit coordination without illegal collusion.

## Example Application 2

**Situation:** Two co-founders splitting equity and responsibilities, tempted to free-ride.

**Application:**
- **Cooperate:** Both work 80-hour weeks building the company
- **Defect:** Reduce effort while partner overworks
- **Mutual defection:** Company fails, both lose

**Dilemma structure:** Individual temptation to coast while partner carries load. But repeated game with high stakes.

**Solution applied:**
- Weekly check-ins create transparency (defection visible quickly)
- Vesting schedules align long-term incentives
- Clear role definition enables accountability
- Equity tied to milestones prevents free-riding

## Anti-Patterns

- Treating one-shot situations as repeated games (hoping for cooperation that won't come)
- Over-punishing (Grim Trigger when Tit-for-Tat would preserve relationship)
- Under-punishing (persistent cooperation despite repeated exploitation)
- Misidentifying the game (not all conflicts are Prisoner's Dilemmas)
- Ignoring asymmetric stakes (payoff structures differ between players)
- Expecting cooperation without transparency (hidden defection unpunished)

## Related

- nash-equilibrium (prisoner's dilemma equilibrium is mutual defection)
- tit-for-tat (optimal strategy for iterated dilemmas)
- game-theory (broader strategic interaction framework)
- incentives (understanding what drives defection vs. cooperation)
- tragedy-of-commons (multi-player version of the dilemma)
