---
name: dual-track-agile
description: Parallel discovery and delivery tracks that validate product ideas before building, preventing waste from shipping the wrong things
---

# Dual-Track Agile (Product Discovery vs Delivery)

## Overview
A product development approach where discovery (validating ideas) and delivery (building features) happen concurrently. Coined by Jeff Patton and popularized by Marty Cagan around 2012, this framework prevents teams from building validated features efficiently while building the wrong things.

## Core Principle
Separate "Are we building the right thing?" (discovery) from "Are we building the thing right?" (delivery). Discovery reduces risk before delivery invests significant resources.

## The Two Tracks

### Discovery Track
**Purpose**: Validate ideas quickly and cheaply before committing to production builds

**Key Activities**:
- Customer interviews to understand problems
- Opportunity assessment and prioritization
- Rapid prototyping and concept testing
- Assumption testing through experiments
- Technical feasibility spikes

**Outputs**:
- Validated opportunities worth pursuing
- De-risked feature concepts
- Evidence-based backlog items
- Technical feasibility assessments

**Participants**: Entire product trio (PM, Design, Engineering)

### Delivery Track
**Purpose**: Build, test, and ship validated features with quality and efficiency

**Key Activities**:
- Sprint planning and backlog refinement
- Production code development
- Quality assurance and testing
- Deployment and monitoring
- Performance optimization

**Outputs**:
- Working software in production
- Technical documentation
- Quality metrics and monitoring
- Customer-facing features

**Participants**: Full engineering team + design for implementation

## The Critical Distinction

**Discovery validates WHAT to build**:
- Customer problems worth solving
- Solutions customers will adopt
- Business model viability
- Technical approach feasibility

**Delivery validates HOW to build**:
- Code quality and architecture
- System performance and reliability
- User experience polish
- Operational stability

## Implementation Steps

### Step 1: Establish Discovery Rhythm
- Allocate specific capacity for discovery work (typically 20-30% of team time)
- Create recurring calendar blocks for discovery activities
- Set up customer research recruitment pipeline
- Define "definition of ready" for ideas to enter delivery

### Step 2: Form Cross-Functional Discovery Team
- Product manager leads opportunity assessment
- Designer creates prototypes and tests usability
- Engineer assesses technical feasibility and effort
- All three participate in customer research

**Why All Three?**:
- PM alone misses design and engineering constraints
- Designer alone optimizes for wrong problems
- Engineer alone builds technically impressive but unusable features

### Step 3: Create Discovery Pipeline
Structure discovery as a funnel:
1. **Ideation**: Generate multiple potential opportunities
2. **Investigation**: Deep dive on promising opportunities
3. **Validation**: Test solutions with customers
4. **Specification**: Document for delivery team

### Step 4: Define Handoff Criteria
Ideas graduate from discovery to delivery when:
- Customer problem validated through interviews
- Solution desirability confirmed through prototype testing
- Technical feasibility assessed and documented
- Business viability (effort vs. impact) justified
- Success metrics defined

### Step 5: Run Both Tracks Concurrently
- Discovery works 1-2 sprints ahead of delivery
- Regular discovery reviews share learnings with full team
- Delivery team feeds implementation insights back to discovery
- Adjust discovery based on delivery findings

### Step 6: Maintain Discovery Backlog
Separate discovery backlog from delivery backlog:
- **Discovery backlog**: Opportunities to investigate
- **Delivery backlog**: Validated features to build
- Only validated items flow from discovery ’ delivery

### Step 7: Measure and Iterate
Track both tracks separately:
- **Discovery metrics**: Ideas tested, assumptions validated, time to validation
- **Delivery metrics**: Velocity, quality, deployment frequency
- **Overall**: Feature success rate, customer adoption, outcome progress

## Practical Applications

### Discovery Activities by Week

**Week 1: Problem Exploration**
- 3-5 customer interviews exploring pain points
- Synthesize themes and opportunity areas
- Map opportunities to business outcomes

**Week 2: Solution Ideation**
- Generate multiple solution concepts
- Create low-fidelity prototypes
- Internal critique and refinement

**Week 3: Solution Testing**
- Test prototypes with 5-8 customers
- Observe behavior, gather feedback
- Iterate on promising directions

**Week 4: Specification**
- Document validated solution
- Technical spike for implementation approach
- Create delivery-ready specs and acceptance criteria

### Example Discovery-to-Delivery Flow

**Discovery Phase** (2 weeks):
- Problem: Users abandon checkout at shipping page
- Hypothesis: Unexpected shipping costs cause abandonment
- Test: Show 5 users prototype with upfront shipping estimates
- Result: 4 of 5 complete purchase with upfront costs, 1 still abandons due to price
- Validation: Shipping transparency improves completion

**Delivery Phase** (2-3 sprints):
- Sprint 1: Implement shipping calculation API integration
- Sprint 2: Add shipping preview to cart page
- Sprint 3: Polish and deploy with monitoring

## Common Pitfalls

### Separate Discovery and Delivery Teams
**Wrong**: Discovery team throws specs "over the wall" to delivery team
**Right**: Same people (especially engineers) participate in both tracks

The most common misconception is that there are two separate teams. This defeats the purpose of integrated learning.

### Discovery as "Waterfall-lite"
**Wrong**: Complete all discovery before any delivery (sequential)
**Right**: Both tracks run in parallel, with discovery leading by 1-2 sprints

### Over-Specification in Discovery
**Wrong**: Creating pixel-perfect designs and detailed specs in discovery
**Right**: Just enough validation to reduce risk, details refined during delivery

### Skipping Discovery When "Busy"
**Wrong**: Abandoning discovery when delivery deadlines loom
**Right**: Protecting discovery time as investment in building the right things

## Evolution: Modern Terminology

Marty Cagan stopped using "Dual-Track Agile" after INSPIRED V2 because teams focused too much on process. He now uses:
- **Continuous Discovery** (instead of Discovery Track)
- **Continuous Delivery** (instead of Delivery Track)

The principles remain the same: validate before building, and do both continuously.

## Success Metrics

### Discovery Health
- **Validation velocity**: Ideas tested per sprint
- **Idea quality**: % of validated ideas that succeed post-launch
- **Time to validation**: Days from hypothesis to evidence
- **Customer contact rate**: Interactions per week

### Delivery Health
- **Build velocity**: Story points or features per sprint
- **Quality**: Bug rates, deployment success rate
- **Cycle time**: Days from commit to production
- **Technical debt**: Accumulation vs. paydown

### Combined Health
- **Feature success rate**: % of launched features hitting success metrics
- **Waste reduction**: Features built but not adopted (should trend toward zero)
- **Outcome progress**: Movement on key business and customer outcomes

## Integration with Other Frameworks

**Enables**:
- Continuous Discovery Habits: Discovery track structure for weekly research
- Lean Startup: Build-Measure-Learn cycles in discovery track
- Jobs to Be Done: Discover customer jobs during discovery track

**Compatible with**:
- Scrum: Discovery and delivery both use sprint cadences
- Kanban: Flow-based approach to both discovery and delivery
- Shape Up: Discovery = shaping, Delivery = building

**Replaces**:
- Big Upfront Design: Discovery is iterative, not comprehensive
- Waterfall: Both tracks run concurrently, not sequentially

## When to Use

**Best for**:
- Established product teams with active users to research
- Organizations struggling with low feature adoption rates
- Teams building too much before validation
- Products in competitive or uncertain markets

**Not ideal for**:
- Solo founders (just do discovery, then delivery - naturally dual-track)
- Teams without customer access (adapt to proxy users or stakeholders)
- Maintenance-heavy products (less discovery needed for bug fixes)

## Anti-Patterns

### "Discovery Theater"
Doing discovery activities without changing what gets built. If every idea still ships regardless of discovery findings, you're wasting time.

### Analysis Paralysis
Endless discovery without committing to delivery. Discovery should quickly validate or invalidate, not study forever.

### Engineering Absent from Discovery
Engineers only see ideas after discovery completes. They bring critical feasibility and effort insights during discovery.

### No Definition of Ready
Unclear when ideas graduate from discovery to delivery. Results in half-baked ideas entering sprints.

## References
- "Dual Track Development" - Jeff Patton (2005 origin)
- "INSPIRED" - Marty Cagan (popularized concept)
- "Continuous Discovery Habits" - Teresa Torres (modern evolution)
- Silicon Valley Product Group (SVPG) articles on dual-track

## Related
- continuous-discovery-habits
- lean-startup
- build-measure-learn
- jobs-to-be-done
- opportunity-solution-trees
- product-trio
- outcome-over-output
- agile-development
- shape-up
