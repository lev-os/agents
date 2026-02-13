# Skills Agent: Framework Discovery Methodology

## Project Overview

**Mission**: Codify every high-value thinking framework, methodology, and mental model across software development, business management, and systems thinking into executable instruction sets.

**Philosophy**: Prioritize practitioner wisdom over academic abstraction. Field-tested frameworks from operators who've shipped products beat theoretical models from researchers who haven't.

---

## Three-Phase Execution Model

### Phase 1: Discovery & Source Mapping (Current Phase)
**Objective**: Identify canonical frameworks and map authoritative sources

**Outputs**:
- skills-agent.md (this document)
- skills-brief.md (executive summary)
- Weighted source catalog
- Research plan for Phase 2

**Activities**:
1. Domain decomposition into 8 core areas
2. Source identification (books, blogs, practitioners)
3. Framework enumeration (broad capture)
4. Quality scoring system development
5. Research plan finalization

### Phase 2: Index Generation
**Objective**: Create comprehensive catalog with sparse execution steps

**Output**:
- skills-index.md (master catalog)

**Format per Framework**:
```
## [Framework Name]
**Source**: [Book/Blog/Author] (Score: X/50)
**Domain**: [Primary] | Cross-applies to: [Secondary domains]
**Core Concept**: [1-2 sentence essence]

**Sparse Steps**:
1. [Actionable step]
2. [Actionable step]
3. [Actionable step]
...

**When to Use**: [Trigger conditions]
**Hidden Gem Factor**: [Why this is non-obvious]
```

### Phase 3: Deep Expansion (Future Work)
**Objective**: Generate individual artifacts per framework with full implementation details

**Output**: Separate markdown files per framework
**Format**: Extended playbooks with examples, edge cases, templates

---

## Domain Architecture

### 1. Software Engineering Patterns
**Focus Areas**:
- Design patterns (structural, behavioral, creational)
- Architectural patterns (microservices, event-driven, CQRS)
- Code quality frameworks (SOLID, DRY, YAGNI)
- Refactoring methodologies
- Testing strategies (TDD, BDD, property-based)

**Key Sources to Mine**:
- Gang of Four (Design Patterns)
- Martin Fowler (Refactoring, Enterprise Patterns)
- Robert C. Martin (Clean Code, Clean Architecture)
- Eric Evans (Domain-Driven Design)
- Sam Newman (Building Microservices)

### 2. App Development & Architecture
**Focus Areas**:
- Mobile architecture patterns (MVC, MVVM, Clean Architecture)
- State management approaches
- Performance optimization frameworks
- Cross-platform development methodologies
- Backend-for-frontend patterns

**Key Sources to Mine**:
- iOS/Android official guidelines
- Practitioner blogs (Gergely Orosz, Dave DeLong)
- Architecture decision records from major apps
- Conference talks from app developers

### 3. UI/UX Principles & Methods
**Focus Areas**:
- Design systems and component libraries
- User research methodologies
- Information architecture frameworks
- Interaction design patterns
- Accessibility frameworks (WCAG, ARIA)
- Visual hierarchy principles

**Key Sources to Mine**:
- Don Norman (Design of Everyday Things)
- Steve Krug (Don't Make Me Think)
- Julie Zhuo (Making of a Manager - design perspective)
- Nielsen Norman Group research
- Material Design, Human Interface Guidelines
- Practitioner blogs (Refactoring UI, Laws of UX)

### 4. Growth & Distribution
**Focus Areas**:
- Growth loop frameworks
- Distribution channel strategies
- Viral mechanics and referral systems
- Conversion optimization methodologies
- Retention and engagement frameworks
- Pricing strategy models

**Key Sources to Mine**:
- Reforge growth series
- Andrew Chen (Cold Start Problem)
- Sean Ellis (Hacking Growth)
- Gabriel Weinberg (Traction)
- Nir Eyal (Hooked)
- Brian Balfour blog
- Lenny's Newsletter insights

### 5. Systems Thinking & First Principles
**Focus Areas**:
- First principles reasoning frameworks
- Mental models catalogs
- Systems dynamics and feedback loops
- Constraint theory (Theory of Constraints)
- Complexity navigation frameworks
- Decision-making frameworks

**Key Sources to Mine**:
- Donella Meadows (Thinking in Systems)
- Charlie Munger mental models
- Farnam Street blog (Shane Parrish)
- James Clear (decision-making frameworks)
- Eliyahu Goldratt (Theory of Constraints)
- Peter Senge (Fifth Discipline)

### 6. Executive Management & Strategy
**Focus Areas**:
- Strategic planning frameworks (OGSM, Hoshin Kanri)
- OKR and goal-setting methodologies
- Decision frameworks (RACI, DACI, RAPID)
- Team organization patterns (Spotify model, Team Topologies)
- Delegation and leverage frameworks
- Meeting and communication protocols

**Key Sources to Mine**:
- Andy Grove (High Output Management)
- Ben Horowitz (Hard Thing About Hard Things)
- Patrick Lencioni (Five Dysfunctions)
- Kim Scott (Radical Candor)
- Stripe, Airbnb, Netflix culture docs
- First Round Review articles
- Camille Fournier (Manager's Path)

### 7. Product Development & Management
**Focus Areas**:
- Product discovery frameworks (Jobs to Be Done)
- Prioritization methodologies (RICE, Kano Model)
- Roadmapping frameworks
- Feature validation approaches
- Product-market fit measurement
- Customer development methodologies

**Key Sources to Mine**:
- Teresa Torres (Continuous Discovery)
- Marty Cagan (Inspired, Empowered)
- Clayton Christensen (Jobs to Be Done)
- Melissa Perri (Escaping the Build Trap)
- Gibson Biddle (product strategy frameworks)
- Shreyas Doshi (Twitter threads on PM)

### 8. Computer Science, AI/ML
**Focus Areas**:
- Algorithm design paradigms (divide-conquer, dynamic programming)
- Data structure selection frameworks
- ML model selection frameworks
- Training and evaluation methodologies
- Feature engineering approaches
- ML system design patterns
- Prompt engineering frameworks

**Key Sources to Mine**:
- Designing Data-Intensive Applications (Martin Kleppmann)
- ML engineering best practices (Chip Huyen)
- Andrew Ng course materials
- FastAI philosophy (Jeremy Howard)
- Papers with Code implementations
- Eugene Yan blog (ML in production)
- Anthropic/OpenAI prompt engineering guides

---

## Source Quality Scoring Rubric

### Weighted Scoring System (0-50 points)

**1. Practitioner Weight (0-10 points)**
- 10: Author built/shipped products using this framework
- 8: Author consulted on implementations
- 5: Author teaches based on case studies
- 3: Academic with industry collaboration
- 0: Pure theory, no implementation evidence

**2. Clarity & Executability (0-10 points)**
- 10: Step-by-step instructions, immediately actionable
- 8: Clear process with minor ambiguity
- 5: Conceptual framework, requires interpretation
- 3: Abstract principles, heavy adaptation needed
- 0: Philosophical, not executable

**3. Proven ROI (0-10 points)**
- 10: Multiple documented success stories with metrics
- 8: Clear before/after examples
- 5: Anecdotal evidence from practitioners
- 3: Logical framework, limited proof
- 0: Unproven or untested

**4. Novelty & Non-Obviousness (0-10 points)**
- 10: Completely counter-intuitive, hidden gem
- 8: Fresh perspective on known problem
- 5: Useful synthesis of existing ideas
- 3: Common knowledge, well-articulated
- 0: Obvious or trivial

**5. Cross-Domain Applicability (0-10 points)**
- 10: Applicable across all domains (universal pattern)
- 8: Works in 3+ domains
- 5: Works in 2 domains
- 3: Domain-specific but foundational
- 0: Highly specialized, narrow use case

### Score Interpretation
- **45-50**: Canonical framework, must-include
- **35-44**: High-value, strong inclusion candidate
- **25-34**: Valuable, include if space permits
- **15-24**: Niche use case, consider for completeness
- **0-14**: Low priority, exclude unless novel insight

---

## Source Discovery Strategy

### Book Selection Criteria
**Top 25 Books Per Domain** (targeting ~200 total books)

Selection filters:
1. **Practitioner-authored** (founders, CTOs, senior ICs who shipped)
2. **Field-tested frameworks** (not just theory)
3. **Clarity over comprehensiveness** (executable > exhaustive)
4. **Recent relevance** (published post-2010 preferred, classics exempted)
5. **Community validation** (HN recommendations, practitioner citations)

### Blog & Online Source Strategy

**Tier 1: Individual Practitioners** (operators currently shipping)
- Personal blogs from senior engineers, designers, founders
- Twitter threads from domain experts
- Conference talks with novel frameworks
- Company engineering blogs (Stripe, Airbnb, Netflix, etc.)

**Tier 2: Curated Collections**
- First Round Review
- Lenny's Newsletter
- Reforge content
- a16z blog (operational content)
- Y Combinator library

**Tier 3: Research & Academic**
- Papers with practical implementation
- Stanford/MIT course materials with applied focus
- Research-backed but practitioner-friendly sources

### Hidden Gem Hunting Strategy

**Where to Find Non-Obvious Frameworks**:
1. **Niche community forums**: Indie Hackers, specific subreddits
2. **Old blog archives**: Pre-2015 practitioner blogs often have unpolished gems
3. **Conference talk recordings**: Practitioners share internal frameworks
4. **Company handbooks**: Public docs from Gitlab, Basecamp, etc.
5. **Tool documentation**: Best practices embedded in tool docs (Figma, Linear)
6. **Adjacent fields**: Psychology â†’ UX, Biology â†’ Systems, Physics â†’ Architecture

**Red Flags for Exclusion**:
- Consultantware (frameworks designed to sell consulting)
- Buzzword-heavy with no substance
- Repackaged common sense
- No clear implementation path
- Author has no shipping experience

---

## Research Execution Plan (Phase 1 â†’ Phase 2)

### Step 1: Canonical Framework Enumeration
**Method**: Start with known high-value frameworks per domain
**Output**: Initial list of ~150-200 frameworks

**Examples**:
- Software: SOLID, DRY, Design Patterns (23 patterns)
- UX: Hick's Law, Fitts's Law, Jakob's Law
- Growth: Sean Ellis Growth Framework, Reforge Growth Loops
- Systems: Feedback Loops, Leverage Points, Stock-Flow Diagrams
- Management: OKRs, RACI, Eisenhower Matrix

### Step 2: Source Deep Dive
**Method**: For each canonical framework, trace to authoritative source
**Output**: Framework â†’ Source mapping with scores

### Step 3: Adjacent Framework Discovery
**Method**: From each source, identify related frameworks mentioned
**Output**: Expanded framework list (~300-400 total)

### Step 4: Hidden Gem Mining
**Method**: Targeted searches in niche communities and old archives
**Output**: Non-obvious frameworks with high practitioner value

### Step 5: Scoring & Ranking
**Method**: Apply rubric to all frameworks
**Output**: Prioritized list for inclusion in skills-index.md

### Step 6: Index Generation
**Method**: Format each framework with sparse steps
**Output**: skills-index.md (Phase 2 deliverable)

---

## Quality Control Gates

### Before Including a Framework:
1. **Clarity test**: Can you explain it in 2 sentences?
2. **Execution test**: Can you write 3-7 actionable steps?
3. **Differentiation test**: Is this distinct from other frameworks?
4. **Value test**: Would an experienced practitioner find this useful?
5. **Source test**: Is the source credible (practitioner or proven)?

### Red Flags:
- Steps are vague ("think about X")
- Framework is just a checklist of obvious items
- No clear trigger for when to use
- Source is purely academic with no implementation examples
- Framework is a rebranding of existing concept

---

## Research Plan Requirements

The research plan (to be generated after preliminary web searches) should include:

1. **Specific search queries** per domain
2. **Target sources** (URLs for top blogs, book lists)
3. **Framework enumeration strategy** (where to find comprehensive lists)
4. **Hidden gem locations** (specific forums, archives, communities)
5. **Validation approach** (how to verify practitioner credentials)
6. **Timeline estimate** (hours per domain)
7. **Quality checkpoints** (when to review progress)

---

## Success Criteria

**Phase 1 Complete When**:
- Research plan approved
- Source catalog mapped (books, blogs, practitioners)
- Scoring rubric validated
- Framework discovery strategy locked

**Phase 2 Complete When**:
- skills-index.md contains 200+ high-value frameworks
- Each framework has 3-7 sparse steps
- Weighted scores included with reasoning
- Hidden gems highlighted
- Cross-domain tags applied

**Phase 3 Success** (future):
- Individual artifacts per framework
- Deep implementation details
- Templates and examples
- Edge case handling

---

## Notes for Future Expansion

### Potential Phase 3 Enhancements:
- Interactive decision trees (which framework for this situation?)
- Case studies per framework
- Anti-patterns (when NOT to use)
- Framework combination strategies
- Domain-specific variations
- Tool recommendations per framework

### Maintenance Strategy:
- Quarterly updates for new frameworks
- Community contributions pipeline
- Practitioner validation process
- Deprecated framework identification

---

---

## COMPREHENSIVE RESEARCH PLAN (Phase 2 Execution)

### Overview
Based on preliminary web searches, this plan outlines the specific sources, search strategies, and framework enumeration approach for Phase 2. The research will be conducted systematically across all 8 domains with a focus on practitioner-validated frameworks.

---

### Domain 1: Software Engineering Patterns

**Top 25 Books (Preliminary)**
1. Design Patterns: Elements of Reusable Object-Oriented Software - Gang of Four â­ (Score: 48/50 - Canonical)
2. Clean Code - Robert C. Martin â­ (Score: 46/50 - Field-tested)
3. Clean Architecture - Robert C. Martin (Score: 45/50)
4. Refactoring - Martin Fowler (Score: 46/50)
5. Patterns of Enterprise Application Architecture - Martin Fowler (Score: 44/50)
6. Domain-Driven Design - Eric Evans (Score: 43/50)
7. Head First Design Patterns - Freeman & Freeman (Score: 40/50 - High clarity)
8. The Pragmatic Programmer - Hunt & Thomas (Score: 45/50)
9. Code Complete - Steve McConnell (Score: 44/50)
10. Building Microservices - Sam Newman (Score: 40/50)
11. Game Programming Patterns - Robert Nystrom (Score: 42/50 - Hidden gem)
12. Working Effectively with Legacy Code - Michael Feathers (Score: 41/50)
13. Refactoring to Patterns - Joshua Kerievsky (Score: 39/50)
14. Test-Driven Development - Kent Beck (Score: 40/50)
15. Growing Object-Oriented Software - Freeman & Pryce (Score: 38/50)
16. Software Architecture Patterns - Mark Richards (Score: 37/50)
17. Fundamentals of Software Architecture - Richards & Ford (Score: 38/50)
18. Building Evolutionary Architectures - Ford et al. (Score: 36/50)
19. Release It! - Michael Nygard (Score: 39/50)
20. Designing Data-Intensive Applications - Martin Kleppmann â­ (Score: 47/50)
21. The Art of Unix Programming - Eric S. Raymond (Score: 38/50)
22. Structure and Interpretation of Computer Programs - Abelson & Sussman (Score: 40/50)
23. Enterprise Integration Patterns - Hohpe & Woolf (Score: 39/50)
24. Continuous Delivery - Humble & Farley (Score: 40/50)
25. Accelerate - Forsgren, Humble, Kim (Score: 41/50)

**Key Practitioner Blogs**
- Martin Fowler (martinfowler.com) - Refactoring, architecture patterns
- Joel Spolsky (Joel on Software) - Practical engineering wisdom
- Paul Graham (paulgraham.com) - Startup engineering principles
- Gergely Orosz (The Pragmatic Engineer) - Engineering practices at scale
- Netflix Tech Blog - Production patterns
- Stripe Engineering Blog - API design, infrastructure
- Airbnb Engineering Blog - React patterns, data infrastructure

**Framework Enumeration Sources**
- Gang of Four: 23 design patterns (Creational, Structural, Behavioral)
- SOLID principles (5 principles)
- DRY, YAGNI, KISS
- 12-Factor App methodology
- Microservices patterns catalog (Sam Newman)
- Event-driven architecture patterns
- CQRS and Event Sourcing patterns
- API design patterns (REST, GraphQL, gRPC)

**Hidden Gem Locations**
- Hacker News "Who is hiring" thread discussions
- /r/programming, /r/softwarearchitecture
- Conference talks: QCon, StrangeLoop, GOTO
- Company engineering handbooks (Gitlab, Basecamp)

---

### Domain 2: App Development & Architecture

**Top 25 Books (Preliminary)**
1. iOS Programming: The Big Nerd Ranch Guide
2. Android Programming: The Big Nerd Ranch Guide
3. React Native in Action - Nader Dabit
4. Clean Architecture - Robert C. Martin (crossover)
5. App Architecture - Eidhof, Gallagher, Kugler
6. Design Patterns by Tutorials (raywenderlich.com)
7. Advanced iOS App Architecture (raywenderlich.com)
8. Kotlin for Android Developers - Antonio Leiva
9. SwiftUI by Tutorials
10. Jetpack Compose by Tutorials
11. Flutter in Action - Eric Windmill
12. Mobile Design Pattern Gallery - Theresa Neil
13. Programming iOS - Matt Neuburg
14. Android Architecture Components - Florina Muntenescu
15-25. (To be expanded with search)

**Key Practitioner Blogs**
- raywenderlich.com - iOS/Android patterns
- iOS Dev Weekly
- Android Weekly
- Dave DeLong (davedelong.com) - iOS architecture
- Sundell's Swift by Sundell
- Gergely Orosz (mobile focus)

**Framework Enumeration Sources**
- MVC, MVP, MVVM, VIPER patterns
- Redux/Flux patterns
- Clean Architecture for mobile
- Dependency injection patterns
- State management patterns (Bloc, Provider, MobX)
- Navigation patterns
- Offline-first architecture
- Performance optimization patterns

**Hidden Gem Locations**
- iOS Conf SG talks
- Android Dev Summit recordings
- /r/iOSProgramming, /r/androiddev
- Company tech blogs (Uber, Lyft mobile teams)

---

### Domain 3: UI/UX Principles & Methods

**Top 25 Books (Preliminary)**
1. The Design of Everyday Things - Don Norman â­ (Score: 50/50 - Foundational)
2. Don't Make Me Think - Steve Krug â­ (Score: 48/50 - Clarity)
3. Rocket Surgery Made Easy - Steve Krug (Score: 43/50)
4. Laws of UX - Jon Yablonski (Score: 42/50)
5. About Face - Cooper, Reimann, Cronin (Score: 44/50)
6. Sprint - Jake Knapp (Score: 45/50 - Field-tested at Google)
7. The User's Journey - Donna Lichaw (Score: 40/50)
8. UX for Beginners - Joel Marsh (Score: 38/50 - High clarity)
9. Observing the User Experience - Kuniavsky (Score: 41/50)
10. Just Enough Research - Erika Hall (Score: 42/50)
11. Interviewing Users - Steve Portigal (Score: 40/50)
12. The Mom Test - Rob Fitzpatrick (Score: 44/50 - Hidden gem)
13. Refactoring UI - Wathan & Schoger (Score: 43/50 - Practitioner-focused)
14. Universal Principles of Design - Lidwell, Holden, Butler (Score: 41/50)
15. Measuring the User Experience - Tullis & Albert (Score: 39/50)
16. Lean UX - Gothelf & Seiden (Score: 40/50)
17. The Best Interface Is No Interface - Krishna (Score: 37/50 - Contrarian)
18. Orchestrating Experiences - Chris Risdon (Score: 36/50)
19. Design Systems Handbook - Suarez et al. (Score: 38/50)
20. Designing Web Interfaces - Scott & Neil (Score: 37/50)
21. Microinteractions - Dan Saffer (Score: 39/50)
22. 100 Things Every Designer Needs to Know - Weinschenk (Score: 36/50)
23. Information Architecture - Rosenfeld, Morville, Arango (Score: 40/50)
24. Emotional Design - Don Norman (Score: 38/50)
25. Seductive Interaction Design - Anderson (Score: 35/50)

**Key Practitioner Blogs**
- Nielsen Norman Group (nngroup.com) â­ - Research-backed UX
- Laws of UX (lawsofux.com) - Pattern library
- Refactoring UI blog - Practical design advice
- UX Booth - Beginner to intermediate
- UX Matters - Best practices
- A List Apart - Web design and UX
- Smashing Magazine UX section
- UX Collective on Medium
- Julie Zhuo (medium.com/@joulee)

**Framework Enumeration Sources**
- Nielsen's 10 Usability Heuristics
- Gestalt Principles (7 principles)
- Laws of UX (20+ laws - Hick's, Fitts's, Jakob's, etc.)
- WCAG accessibility guidelines
- Material Design principles
- Human Interface Guidelines (Apple)
- Design thinking process (IDEO)
- Double Diamond process
- Kano Model
- User story mapping

**Hidden Gem Locations**
- Designer Hangout Slack
- /r/userexperience, /r/UI_Design
- Figma community resources
- Company design system docs (Shopify Polaris, IBM Carbon)
- Interaction Design Foundation articles

---

### Domain 4: Growth & Distribution

**Top 25 Books (Preliminary)**
1. Hacking Growth - Sean Ellis & Morgan Brown â­ (Score: 47/50 - Definitive)
2. Traction - Gabriel Weinberg & Justin Mares â­ (Score: 46/50 - 19 channels)
3. The Cold Start Problem - Andrew Chen (Score: 45/50 - Network effects)
4. Hooked - Nir Eyal (Score: 44/50 - Habit formation)
5. Growth Hacker Marketing - Ryan Holiday (Score: 40/50)
6. The Lean Startup - Eric Ries (Score: 46/50 - Foundational)
7. Zero to One - Peter Thiel (Score: 43/50)
8. Crossing the Chasm - Geoffrey Moore (Score: 45/50 - Classic)
9. The Mom Test - Rob Fitzpatrick (Score: 44/50 - Customer development)
10. Obviously Awesome - April Dunford (Score: 41/50 - Positioning)
11. Product-Led Growth - Wes Bush (Score: 40/50)
12. The Growth Handbook - Andrew Chen & Intercom (Score: 42/50)
13. Blitzscaling - Reid Hoffman (Score: 39/50)
14. The SaaS Playbook - Rob Walling (Score: 38/50)
15. $100M Offers - Alex Hormozi (Score: 37/50)
16. $100M Leads - Alex Hormozi (Score: 36/50)
17. Contagious - Jonah Berger (Score: 40/50)
18. Made to Stick - Chip & Dan Heath (Score: 41/50)
19. Influence - Robert Cialdini (Score: 42/50)
20. Subscription Marketing - Anne Janzer (Score: 35/50)
21. Lean Analytics - Croll & Yoskovitz (Score: 40/50)
22. High Growth Handbook - Elad Gil (Score: 39/50)
23. Play Bigger - Lochhead et al. (Score: 37/50)
24. Demand-Side Sales - Bob Moesta (Score: 38/50)
25. This Is Marketing - Seth Godin (Score: 36/50)

**Key Practitioner Blogs**
- Lenny's Newsletter (Lenny Rachitsky) â­ - Product & growth
- Reforge Blog (Brian Balfour et al.) â­ - Growth frameworks
- Andrew Chen's blog (andrewchen.com) - Growth, metrics
- Brian Balfour's blog - Growth loops, PMF
- Sean Ellis's blog (GrowthHackers)
- First Round Review â­ - Startup tactics
- a16z blog (operational content)
- Y Combinator Blog
- GrowthMentor resources
- Lenny's Podcast transcripts

**Framework Enumeration Sources**
- Sean Ellis Growth Framework
- Bullseye Framework (19 traction channels)
- AARRR (Pirate Metrics)
- Growth Loops framework (Reforge)
- Hook Model (Nir Eyal)
- Network effects types (Andrew Chen)
- North Star Metric framework
- ICE/RICE prioritization
- Viral coefficient calculation
- Retention cohort analysis

**Hidden Gem Locations**
- GrowthHackers community
- Indie Hackers forums â­
- /r/startups, /r/entrepreneur
- Product Hunt maker stories
- YC Startup School resources
- Reforge alumni Slack

---

### Domain 5: Systems Thinking & First Principles

**Top 25 Books (Preliminary)**
1. Thinking in Systems - Donella Meadows â­ (Score: 50/50 - Definitive)
2. Poor Charlie's Almanack - Charlie Munger â­ (Score: 49/50 - Mental models)
3. The Great Mental Models Vol. 1 - Shane Parrish (Score: 46/50)
4. The Great Mental Models Vol. 2 - Shane Parrish (Score: 44/50)
5. The Great Mental Models Vol. 3 - Shane Parrish (Score: 43/50)
6. Super Thinking - Weinberg & McCann (Score: 45/50)
7. Seeking Wisdom - Peter Bevelin (Score: 44/50)
8. The Fifth Discipline - Peter Senge (Score: 43/50)
9. Theory of Constraints - Eliyahu Goldratt (Score: 42/50)
10. The Goal - Goldratt (Score: 40/50 - Business novel)
11. Antifragile - Nassim Taleb (Score: 44/50)
12. The Black Swan - Nassim Taleb (Score: 41/50)
13. Thinking, Fast and Slow - Daniel Kahneman (Score: 46/50)
14. Range - David Epstein (Score: 40/50)
15. How to Solve It - George PÃ³lya (Score: 42/50)
16. The Art of Problem Solving - Russell Ackoff (Score: 38/50)
17. Systems Thinking for Business - Rich Jolly (Score: 37/50)
18. The Systems Thinking Playbook - Sweeney & Meadows (Score: 36/50)
19. Limits to Growth - Meadows et al. (Score: 39/50)
20. An Introduction to General Systems Thinking - Gerald Weinberg (Score: 40/50)
21. The Art of Thinking Clearly - Rolf Dobelli (Score: 39/50)
22. Pre-Suasion - Robert Cialdini (Score: 38/50)
23. Principles - Ray Dalio (Score: 41/50)
24. Algorithms to Live By - Christian & Griffiths (Score: 42/50)
25. The Map Is Not the Territory - Alfred Korzybski (Score: 35/50)

**Key Practitioner Blogs**
- Farnam Street (Shane Parrish) â­ - Mental models, decision-making
- Donella Meadows Project - Systems resources
- Paul Saffo (IFTF) - Long-term thinking
- James Clear (jamesclear.com) - Decision frameworks
- LessWrong community - Rationality
- Ribbonfarm (Venkatesh Rao) - Systems thinking

**Framework Enumeration Sources**
- Feedback loops (balancing, reinforcing)
- Stock and flow diagrams
- Causal loop diagrams
- Leverage points (12 places to intervene)
- Mental models catalog (100+ models)
- First principles reasoning process
- Inversion thinking
- Second-order thinking
- Probabilistic thinking
- Circle of competence

**Hidden Gem Locations**
- System Dynamics Society resources
- MIT System Dynamics group papers
- /r/systemsthinking
- Santa Fe Institute complexity papers
- Long Now Foundation resources

---

### Domain 6: Executive Management & Strategy

**Top 25 Books (Preliminary)**
1. High Output Management - Andy Grove â­ (Score: 50/50 - Legendary)
2. The Hard Thing About Hard Things - Ben Horowitz â­ (Score: 47/50)
3. Only the Paranoid Survive - Andy Grove (Score: 44/50)
4. Good Strategy/Bad Strategy - Richard Rumelt (Score: 46/50)
5. Playing to Win - Lafley & Martin (Score: 43/50)
6. 7 Powers - Hamilton Helmer (Score: 44/50)
7. Radical Candor - Kim Scott (Score: 45/50)
8. The Manager's Path - Camille Fournier (Score: 44/50 - Engineering focus)
9. The Making of a Manager - Julie Zhuo (Score: 43/50)
10. Team Topologies - Skelton & Pais (Score: 42/50)
11. The Five Dysfunctions of a Team - Patrick Lencioni (Score: 41/50)
12. Measure What Matters - John Doerr (Score: 42/50 - OKRs)
13. Trillion Dollar Coach - Schmidt, Rosenberg, Eagle (Score: 40/50 - Bill Campbell)
14. An Elegant Puzzle - Will Larson (Score: 43/50 - Engineering management)
15. The Effective Executive - Peter Drucker (Score: 44/50 - Classic)
16. Turn the Ship Around - David Marquet (Score: 40/50)
17. Extreme Ownership - Willink & Babin (Score: 39/50)
18. Creativity, Inc. - Ed Catmull (Score: 42/50 - Pixar)
19. Powerful - Patty McCord (Score: 38/50 - Netflix culture)
20. Work Rules! - Laszlo Bock (Score: 39/50 - Google HR)
21. The Advantage - Patrick Lencioni (Score: 37/50)
22. Leadership Is Language - David Marquet (Score: 36/50)
23. Multipliers - Liz Wiseman (Score: 38/50)
24. Scaling Up - Verne Harnish (Score: 37/50)
25. The Lean Manager - BallÃ© & BallÃ© (Score: 35/50)

**Key Practitioner Blogs**
- First Round Review â­ - Operational advice
- Rework (Basecamp blog) - Management philosophy
- a16z podcast transcripts
- Stripe Press blog
- Will Larson (lethain.com) - Engineering leadership
- Camille Fournier blog
- Charity Majors blog (engineering management)
- Ken Norton essays â­

**Framework Enumeration Sources**
- OKRs (Objectives & Key Results)
- RACI matrix
- DACI/RAPID decision frameworks
- Eisenhower Matrix
- Delegation levels (7 levels)
- 1-on-1 frameworks
- Performance review frameworks
- Hiring scorecards
- Organizational design patterns
- Strategic planning frameworks (Hoshin Kanri, OGSM)

**Hidden Gem Locations**
- Manager Tools podcast archives
- Gitlab handbook (public)
- Basecamp handbook (public)
- /r/management
- LeadDev conference talks
- Engineering manager Slack communities

---

### Domain 7: Product Development & Management

**Top 25 Books (Preliminary)**
1. Inspired - Marty Cagan â­ (Score: 50/50 - PM bible)
2. Empowered - Marty Cagan & Chris Jones (Score: 48/50)
3. Transformed - Marty Cagan (Score: 46/50 - Latest in trilogy)
4. Continuous Discovery Habits - Teresa Torres â­ (Score: 49/50)
5. Escaping the Build Trap - Melissa Perri (Score: 46/50)
6. The Lean Product Playbook - Dan Olsen (Score: 44/50)
7. Sprint - Jake Knapp (Score: 45/50)
8. Competing Against Luck - Clayton Christensen (Score: 45/50 - JTBD)
9. User Story Mapping - Jeff Patton (Score: 42/50)
10. Deploy Empathy - Michele Hansen (Score: 43/50 - Hidden gem)
11. The Mom Test - Rob Fitzpatrick (Score: 44/50)
12. Product Leadership - Banfield, Eriksson, Walkingshaw (Score: 40/50)
13. Product Roadmaps Relaunched - Lombardo et al. (Score: 39/50)
14. Radical Product Thinking - R. Dutt (Score: 38/50)
15. Loved - Martina Lauchengco (Score: 37/50)
16. Outcomes Over Output - Josh Seiden (Score: 40/50)
17. Intercom on Product Management (Score: 41/50)
18. Cracking the PM Interview - McDowell & Bavaro (Score: 38/50)
19. Decode and Conquer - Lewis Lin (Score: 36/50)
20. The Product Book - Product School (Score: 35/50)
21. Hooked - Nir Eyal (Score: 44/50 - Crossover)
22. Designing Products People Love - Scott Hurff (Score: 37/50)
23. UX Strategy - Jaime Levy (Score: 38/50)
24. Lean Customer Development - Alvarez (Score: 36/50)
25. The Innovator's Solution - Christensen (Score: 41/50)

**Key Practitioner Blogs**
- SVPG (Marty Cagan) â­ - Product leadership
- ProductTalk.org (Teresa Torres) â­ - Discovery
- Lenny's Newsletter â­ - PM insights
- Melissa Perri blog - Product operations
- Gibson Biddle (gibsonbiddle.com) - Strategy
- Shreyas Doshi (Twitter/X) â­ - PM wisdom
- Ken Norton essays - PM craft
- Mind the Product blog
- Product Coalition on Medium
- Intercom blog

**Framework Enumeration Sources**
- Jobs to Be Done framework
- Continuous Discovery framework (Teresa Torres)
- Product discovery vs delivery
- Opportunity solution trees
- RICE prioritization
- Kano Model
- North Star framework
- Product-market fit measurement
- Product strategy frameworks (Gibson Biddle)
- Product trio model

**Hidden Gem Locations**
- ProductTank meetup recordings
- Mind the Product conference talks
- /r/ProductManagement
- Product School resources
- Product Manager HQ community

---

### Domain 8: Computer Science, AI/ML

**Top 25 Books (Preliminary)**
1. Designing Machine Learning Systems - Chip Huyen â­ (Score: 49/50 - Production ML)
2. AI Engineering - Chip Huyen â­ (Score: 48/50 - Foundation models)
3. Designing Data-Intensive Applications - Kleppmann (Score: 47/50)
4. Machine Learning Design Patterns - Google engineers (Score: 44/50)
5. Hands-On Machine Learning - AurÃ©lien GÃ©ron (Score: 45/50)
6. Deep Learning - Goodfellow, Bengio, Courville (Score: 46/50 - Theoretical)
7. The Algorithm Design Manual - Steven Skiena (Score: 43/50)
8. Introduction to Algorithms (CLRS) (Score: 44/50)
9. Grokking Algorithms - Aditya Bhargava (Score: 40/50 - Beginner-friendly)
10. Programming Pearls - Jon Bentley (Score: 41/50)
11. Elements of Programming Interviews - Aziz et al. (Score: 38/50)
12. Cracking the Coding Interview - Gayle McDowell (Score: 39/50)
13. System Design Interview - Alex Xu (Score: 42/50)
14. The Art of Computer Programming - Knuth (Score: 40/50 - Reference)
15. Introduction to Machine Learning Interviews - Chip Huyen (Score: 37/50)
16. Machine Learning Engineering - Andriy Burkov (Score: 38/50)
17. The Hundred-Page Machine Learning Book - Burkov (Score: 36/50)
18. Feature Engineering for Machine Learning - Zheng & Casari (Score: 37/50)
19. Natural Language Processing with Transformers - Tunstall et al. (Score: 40/50)
20. Deep Learning for Coders - Jeremy Howard (Score: 41/50 - Fast.ai)
21. Probabilistic Machine Learning - Kevin Murphy (Score: 43/50)
22. Reinforcement Learning - Sutton & Barto (Score: 42/50)
23. Pattern Recognition and ML - Christopher Bishop (Score: 40/50)
24. Speech and Language Processing - Jurafsky & Martin (Score: 39/50)
25. Dive into Deep Learning (D2L.ai) - Open source (Score: 42/50)

**Key Practitioner Blogs**
- Chip Huyen's blog (huyenchip.com) â­ - ML systems
- Eugene Yan (eugeneyan.com) â­ - Applied ML
- Jay Alammar (jalammar.github.io) - Visual ML explanations
- Lil'Log (lilianweng.github.io) - Deep learning
- Sebastian Raschka blog - Practical ML
- Machine Learning Mastery - Jason Brownlee
- Distill.pub - Research communication
- Papers with Code
- The Batch (Andrew Ng newsletter)
- Fast.ai blog (Jeremy Howard)

**Framework Enumeration Sources**
- Algorithm paradigms (divide-conquer, DP, greedy, backtracking)
- Data structure selection framework
- ML model selection framework
- Training loop patterns
- Feature engineering patterns
- ML system design patterns (batch, streaming, online learning)
- Prompt engineering frameworks
- RAG (Retrieval-Augmented Generation) patterns
- Fine-tuning strategies
- Model evaluation frameworks

**Hidden Gem Locations**
- ML Engineering Discord (Chip Huyen)
- Papers with Code discussions
- /r/MachineLearning
- Hugging Face forums
- fast.ai forums
- AI Alignment Forum (for safety patterns)
- MLOps community resources

---

## Search Query Templates (to be executed in Phase 2)

### Pattern Discovery Queries
```
"[DOMAIN] frameworks list"
"[DOMAIN] best practices checklist"
"[DOMAIN] patterns catalog"
"[FRAMEWORK_NAME] step by step"
"how to [TASK] framework"
```

### Practitioner Validation Queries
```
"[AUTHOR_NAME] practitioner experience"
"[AUTHOR_NAME] companies worked"
"[BOOK_NAME] case studies examples"
"[FRAMEWORK_NAME] used at [COMPANY]"
```

### Hidden Gem Queries
```
site:news.ycombinator.com "[DOMAIN] framework"
site:reddit.com/r/[SUBREDDIT] "framework we use"
"[DOMAIN] internal playbook" filetype:pdf
"[DOMAIN] decision framework we use at"
```

---

## Validation & Quality Control Process

### For Each Framework:
1. **Source Verification**: Confirm author has shipped products/worked in field
2. **Implementation Evidence**: Find 2+ case studies or examples
3. **Step Extraction**: Identify 3-7 clear, actionable steps
4. **Differentiation Check**: Ensure framework is distinct from others
5. **Scoring**: Apply full rubric (Practitioner, Clarity, ROI, Novelty, Cross-domain)

### Red Flag Triggers (skip/deprioritize):
- No clear author credentials
- Only academic citations, no practitioner usage
- Steps are vague/philosophical
- Exact duplicate of another framework
- Consultantware (designed to sell services)

---

## Timeline Estimate

**Week 1-2: Canonical Framework Enumeration**
- 8 domains Ã— 20-30 frameworks each = ~200 frameworks
- ~10 hours per domain = 80 hours total
- Extract from known books, verify sources

**Week 3-4: Source Deep Dive & Scoring**
- Trace each framework to source
- Apply scoring rubric
- Document reasoning
- ~100 hours

**Week 5-6: Adjacent Discovery & Hidden Gems**
- Mine practitioner blogs for related frameworks
- Search niche communities
- Identify non-obvious connections
- ~80 hours

**Week 7: Expansion & Documentation**
- Expand to ~300-400 total frameworks
- Final scoring pass
- Create skills-index.md
- ~40 hours

**Total Estimated Time: 300 hours (7-8 weeks at 40hr/week or 12-15 weeks part-time)**

---

## Output Format (skills-index.md)

Each framework will follow this template:

```markdown
## [Framework Name]

**Source**: [Book/Author/Blog] (Publication Year)  
**Score**: X/50 (Practitioner: X, Clarity: X, ROI: X, Novelty: X, Cross-domain: X)  
**Domain**: [Primary Domain] | Cross-applies to: [Secondary Domains]

**Core Concept**: [1-2 sentence essence]

**When to Use**: [Trigger conditions/problem type]

**Sparse Steps**:
1. [Actionable step with concrete output]
2. [Actionable step with concrete output]
3. [Actionable step with concrete output]
4. [Continue as needed, max 7 steps]

**Why High-Value**: [Practitioner impact, proven outcomes]

**Hidden Gem Factor**: [If score >7 on Novelty: why this is non-obvious]

**Related Frameworks**: [Links to complementary or alternative frameworks]

---
```

**Next Action**: Await approval of this research plan before executing Phase 2.