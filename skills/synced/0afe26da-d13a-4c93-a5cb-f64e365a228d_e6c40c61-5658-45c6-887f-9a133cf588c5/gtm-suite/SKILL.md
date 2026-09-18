---
name: gtm-suite
description: "Complete Go-To-Market strategy suite combining 5 frameworks from Maja Voje's GTM Strategist. Covers: Power Hour (GTM 1-pager hypothesis), ICP Validation (empirical customer profiling, beachhead market selection), Positioning (competitive analysis, messaging architecture, strategic narrative), Pricing (willingness-to-pay testing, pricing models, offer design), and Motion (PLG/SLG/CLG/content/partnership selection, 90-day sprint planning). Use when starting a product launch, validating GTM assumptions, defining target audience, creating positioning/messaging, setting pricing strategy, or planning growth motions. Triggers on: go-to-market, GTM, launch plan, ICP, target audience, customer persona, segmentation, beachhead, positioning, messaging, differentiation, value proposition, competitive analysis, pricing, willingness to pay, monetization, tiers, freemium, offer design, traction, growth strategy, GTM motion, distribution, channel strategy, PLG, sales-led, community-led, content-led, partnership."
metadata:
  author: kingly-agency
  version: '1.0'
---

# GTM Strategy Suite

This skill combines five sequential GTM frameworks drawn from Maja Voje's GTM Strategist methodology into a single end-to-end system. Each module builds on the last: Power Hour produces the hypothesis document that ICP Validation challenges with real signals; ICP Validation feeds the validated customer profile that Positioning needs to build differentiated messaging; Positioning informs the value framing that Pricing requires to set defensible prices; and Pricing feeds the offer design that Motion deploys through the right growth channel. Run them in sequence for a complete go-to-market strategy, or jump to the relevant module when a specific question arises.

**Recommended sequence:**

**Power Hour → ICP Validation → Positioning → Pricing → Motion**

---

## § Power Hour

# GTM Power Hour

The GTM Power Hour is a structured 60-minute exercise drawn from Maja Voje's GTM Strategist framework. Its purpose is to produce a one-page GTM plan — a "GTM compass" — that captures your **initial assumptions** (not validated truths) about your market, customer, value proposition, pricing, channels, and success metrics. This document becomes the foundation that every subsequent GTM module challenges and refines.

**Key principle:** Speed over perfection. The 1-pager is a hypothesis document. Every field is an assumption until proven otherwise.

---

### When to Use This Skill

- Starting a new product launch or go-to-market process
- Entering a new market or customer segment
- Reframing an existing GTM strategy
- Creating alignment across a founding team or stakeholders before deeper research
- As a prerequisite to the `gtm-icp-validation` and `gtm-positioning` skills

---

### Step 1: Interview the User

Use structured questions to gather the raw material for the 1-pager. Ask each question in sequence. If the user is uncertain, encourage a hypothesis — "what's your best guess right now?" is always valid at this stage.

**Questions to ask:**

1. What is the product name? What does it do in one sentence?
2. What problem does your product solve? For whom specifically?
3. Who is your initial target customer? Be specific — their job title, company size, industry, and the pain they feel most acutely.
4. What is your core value proposition in one sentence? ("We help [customer] do [outcome] by [mechanism].")
5. Who are your top 3 competitors or closest alternatives — including the "do nothing" option? How are you different from each?
6. What is your pricing model hypothesis? (Freemium, usage-based, per-seat, flat subscription, one-time, services-led?)
7. What entry price point are you considering? Is your optimization target adoption (low friction) or profit (high margin)?
8. What are your top 3 distribution channel hypotheses — how will customers find you and buy?
9. What does success look like in 90 days? Name at least one specific metric.
10. What is your single biggest GTM risk right now — the assumption that, if wrong, breaks everything?

---

### Step 2: Synthesize into the GTM 1-Pager

After gathering answers, produce the following structured document. Fill every section, even if it means writing "Unknown — to be validated." Leave nothing blank.

```markdown
# GTM Power Hour — [Product Name]
## Date: [date]
## Status: ASSUMPTIONS (unvalidated)

---

### Problem Statement
[1–2 sentences. Who experiences this problem, when, and what is the cost of the problem to them?]

---

### Target Customer (ICP Hypothesis)
- **Role/Title:** 
- **Company type/size:** 
- **Industry:** 
- **Core pain point:** 
- **Current workaround:** 
- **Trigger moment:** [What event causes them to look for a solution?]

---

### Value Proposition
> [One sentence. Format: "We help [target] achieve [outcome] by [differentiating mechanism]."]

---

### Competitive Landscape
| Competitor | Their Strength | Our Differentiation |
|---|---|---|
| [Competitor 1] | | |
| [Competitor 2] | | |
| [Do nothing / status quo] | | |

---

### Pricing Hypothesis
- **Model:** [freemium / usage-based / per-seat / flat / one-time / hybrid]
- **Entry price:** 
- **Optimization target:** [adoption — keep friction low] OR [profit — maximize margin]
- **Expansion revenue mechanism:** [How do customers pay more over time?]

---

### Distribution Channels (ranked by priority)
1. [Channel 1] — Rationale: 
2. [Channel 2] — Rationale: 
3. [Channel 3] — Rationale: 

---

### 90-Day Success Metrics
- **Primary metric:** [The one number that defines success]
- **Secondary metric:** [Supporting indicator]
- **Guardrail metric:** [What must NOT get worse — e.g., churn, NPS, support volume]

---

### Top GTM Risks
1. [Risk] — Impact if wrong: [high/medium/low]
2. [Risk] — Impact if wrong: 
3. [Risk] — Impact if wrong: 

---

### Open Questions to Validate
1. [Question] — How to validate: 
2. [Question] — How to validate: 
3. [Question] — How to validate: 
```

---

### Step 3: Save the Document

Save the completed 1-pager to the workspace as:

```
gtm-power-hour-[product-name].md
```

Use lowercase, hyphen-separated product name. Example: `gtm-power-hour-acme-analytics.md`

---

### Step 4: Identify Critical Assumptions

After completing the 1-pager, review every field and identify the **top 3 assumptions** that are:
- Most central to the GTM strategy succeeding, AND
- Least validated by existing evidence

Present them in this format:

```markdown
## Critical Assumptions to Validate First

### Assumption 1: [State the assumption]
- **Why it matters:** [If wrong, this happens...]
- **How to validate:** [Fastest, cheapest test — interview, search, landing page, etc.]
- **Timeline:** [Days to get signal]

### Assumption 2: [State the assumption]
...

### Assumption 3: [State the assumption]
...
```

---

### Step 5: Recommend Next Module

Based on the weakest assumptions identified, recommend which GTM skill to run next:

| Weakest Area | Recommended Next Skill |
|---|---|
| ICP / target customer unclear | `gtm-icp-validation` — validate who you're selling to |
| Differentiation or messaging unclear | `gtm-positioning` — define competitive positioning |
| Channel strategy unclear | Run distribution channel research |
| Pricing unclear | Run pricing validation interviews |

Always note: "This 1-pager is a living document. Revisit and update it after completing each validation module."

---

### Output Checklist

Before finishing, confirm:
- [ ] All 1-pager sections are filled (no blanks — use "Unknown — TBV" if genuinely unknown)
- [ ] Document saved to workspace as `gtm-power-hour-[product-name].md`
- [ ] Top 3 critical assumptions identified with validation methods
- [ ] Next recommended module specified
- [ ] Status header clearly reads "ASSUMPTIONS (unvalidated)"

---

## § ICP Validation

# GTM ICP Validation

Drawn from Maja Voje's GTM Strategist framework (Module 2), this skill replaces assumption-based personas with empirically validated customer profiles. The goal is to identify **who you can win with first** — the beachhead segment — rather than trying to serve everyone at once.

**Key principle:** ICPs built on stereotypes lead to messaging that resonates with no one. Validate with real signals — interviews, behavioral data, reviews, forum language — before locking in your strategy.

---

### When to Use This Skill

- After completing a GTM Power Hour (loads the ICP hypothesis)
- When a product is not converting as expected despite traffic
- When entering a new market segment
- When repositioning to a different customer type
- Before writing positioning, messaging, or outbound copy
- Triggered by: "who is our customer?", "define our ICP", "segment the market", "find our beachhead"

---

### Step 1: Load or Establish the ICP Hypothesis

**If a GTM Power Hour file exists in the workspace:**
- Search for `gtm-power-hour-*.md` files
- Extract the "Target Customer (ICP Hypothesis)" and "Value Proposition" sections
- Present the hypothesis to the user for confirmation before proceeding

**If no GTM Power Hour exists:**
Ask the user:
1. What does your product do and who is it for?
2. Who has expressed the most interest or gotten the most value so far?
3. Are there any early customers or users? What do they have in common?
4. What pain are you solving and who feels it most intensely?

Document the hypothesis before moving to validation.

---

### Step 2: Segmentation Frameworks

Apply the most relevant framework(s) based on the product and market stage.

#### Framework A: TAM / SAM / SOM Analysis

Estimate market size at three levels:

| Level | Definition | How to Estimate |
|---|---|---|
| **TAM** (Total Addressable Market) | Everyone who could theoretically benefit | Industry reports, census data, LinkedIn counts |
| **SAM** (Serviceable Addressable Market) | The portion you could realistically reach with your model | Filter by geography, segment, buying capacity |
| **SOM** (Serviceable Obtainable Market) | Realistic capture in 12–24 months | Assume 1–5% of SAM for early-stage; benchmark competitors |

Use `search_web` to find market sizing data. Always cite sources. Express in number of potential customers AND annual revenue potential.

#### Framework B: Beachhead Market Selection

The beachhead is the **smallest viable segment you can dominate first** — then use as a reference base to expand. Criteria for a good beachhead:

- **Accessible:** You can reach them without massive budget
- **Urgent pain:** The problem is a top-3 priority, not a nice-to-have
- **Willing to pay:** They have budget and authority to buy
- **Referenceable:** A win here creates credibility in adjacent segments
- **Winnable:** Competition is weak or absent in this specific niche

Score candidate segments across these five criteria (1–3 each) and select the highest-scoring segment.

#### Framework C: Jobs-to-Be-Done Segmentation

Segment customers by **what they are trying to accomplish**, not who they are demographically.

Ask: "What job is the customer hiring this product to do?"

Examples:
- "Help me report to my board without spending a weekend on it" (executive outcome)
- "Help me hit my quota without cold calling strangers" (sales rep outcome)
- "Help me stop losing sleep over compliance audits" (risk/compliance outcome)

Different jobs = different ICPs, even if the demographics look similar. Identify the 1–2 most common jobs and build validation around those.

#### Framework D: Behavioral Segmentation

Group potential customers by observable behaviors:

| Behavior | What It Signals |
|---|---|
| Already using a manual workaround | High pain, high motivation to switch |
| Currently paying for a competitor | Validated willingness to pay |
| Actively searching for solutions (SEO demand) | In-market right now |
| Complaining in forums/communities | High frustration, vocal, findable |
| Early adopter profile | Will tolerate rough product for the benefit |

---

### Step 3: Research the ICP with Real Signals

Use available tools to gather evidence. Do not rely on assumptions.

#### 3a. Search for ICP Language Online

Use `search_web` and `search_social` to find where the target persona congregates and what language they use:

- Search Reddit: `[pain point] reddit` — look for posts, upvotes, comment language
- Search X/Twitter: complaints, feature requests, workaround threads
- Search LinkedIn: job postings for roles related to this pain (signals company investment)
- Search product review sites (G2, Capterra, Trustpilot) for competitor reviews

**Capture exact quotes.** The language customers use to describe their pain is gold for messaging.

#### 3b. Research Competitor Customers

Find evidence of who is actually buying from competitors:
- Case studies and testimonials on competitor websites
- Review profiles on G2/Capterra (reviewers often list job title, company size, industry)
- "Customers" or "Used by" pages
- LinkedIn — search who follows or works at competing companies

This reveals the actual ICP, not the stated one.

#### 3c. Estimate Market Size

Use `search_web` to find:
- Industry analyst reports
- LinkedIn audience size (search by title + geography)
- Professional association membership counts
- Bureau of Labor Statistics occupational data (US)
- SBA or census data for business counts by size/industry

---

### Step 4: Produce the Validated ICP Document

For each validated persona, complete this template:

```markdown
# ICP Persona: [Name — give a memorable label, not a generic "marketing manager"]
## Last Updated: [date]
## Based on: [n] interviews / [n] survey responses / [data sources used]
## Validation Status: [Hypothesis / Partially Validated / Validated]

---

### Who They Are
- **Role/Title:** 
- **Seniority:** [individual contributor / manager / director / VP / C-suite]
- **Company stage/size:** 
- **Industry vertical:** 
- **Geography (if relevant):** 

### Behavioral Signals
- **How they currently solve this problem:** 
- **Tools they already use:** 
- **Time spent on workaround per week:** 
- **Budget authority:** [yes / no / influences decision]
- **Typical budget range:** 

### Pain Hierarchy
Ranked by frequency × intensity (source each pain with evidence):

1. **[Pain]**
   - Frequency: [daily / weekly / monthly]
   - Intensity: [1–10]
   - Evidence: [quote, review, or observation]

2. **[Pain]**
   - Frequency: 
   - Intensity: 
   - Evidence: 

3. **[Pain]**
   - Frequency: 
   - Intensity: 
   - Evidence: 

### Jobs-to-Be-Done
> "When [situation], I want to [motivation], so I can [outcome]."

Primary job: 
Secondary job: 

### Decision Triggers
- **What makes them look for a solution:** [Event, trigger, or threshold]
- **What would make them switch from current approach:** 
- **What would make them NOT switch:** [Objections, switching costs]
- **Who else influences the decision:** [Roles involved in buying]
- **Typical sales cycle length:** 

### Where They Exist
- **Online communities:** 
- **Social platforms:** 
- **Newsletters/publications they read:** 
- **Events/conferences they attend:** 
- **Search terms they use:** 

### Validation Checklist
- [ ] Confirmed via customer/prospect interviews (n=?)
- [ ] Confirmed via survey data (n=?)
- [ ] Confirmed via behavioral/product data
- [ ] Confirmed via sales or support conversation analysis
- [ ] Cross-validated against competitor customer evidence
```

---

### Step 5: Identify the Beachhead Market

After completing the persona(s), make a definitive beachhead recommendation:

```markdown
## Beachhead Market Recommendation

**Recommended Beachhead:** [Specific segment — role + company size + industry + geography if applicable]

**Rationale:**
- Accessibility: [How you reach them]
- Pain urgency: [Evidence of urgency]
- Willingness to pay: [Evidence of budget]
- Referenceability: [Why a win here unlocks the next segment]
- Competitive gap: [Why you can win here]

**Expansion Path:**
1. Win beachhead → [Segment 2 that becomes accessible]
2. Win Segment 2 → [Segment 3]

**Segments Explicitly Deprioritized (and why):**
- [Segment] — Reason: [too broad / no urgency / can't reach / competition too strong]
```

---

### Step 6: Flag Unvalidated Assumptions

List any ICP assumptions that could not be validated with available data:

```markdown
## Unvalidated Assumptions

| Assumption | Why It Matters | How to Validate |
|---|---|---|
| [Assumption] | [Impact if wrong] | [Interview / survey / test] |
```

---

### Step 7: Save and Hand Off

Save the completed ICP document as:
```
gtm-icp-[product-name].md
```

After saving:
- If positioning hasn't been done: recommend running `gtm-positioning`
- If messaging copy is needed: recommend the positioning skill before writing copy
- Update the original `gtm-power-hour-[product-name].md` ICP section with validated findings

---

### Output Checklist

Before finishing, confirm:
- [ ] ICP hypothesis was loaded or established
- [ ] At least one segmentation framework applied
- [ ] Real signals researched (search results, reviews, forums, competitor customers)
- [ ] Full persona template completed with evidence citations
- [ ] Beachhead market identified with rationale
- [ ] Unvalidated assumptions flagged
- [ ] Document saved as `gtm-icp-[product-name].md`
- [ ] Next step recommended

---

## § Positioning

# GTM Positioning

Drawn from Maja Voje's GTM Strategist framework (Module 3), this skill builds the complete positioning, messaging, and strategic narrative for your product. Positioning is not what you say about your product — it is the mental real estate you own in your customer's mind relative to alternatives. Done correctly, it makes every subsequent marketing and sales asset more effective.

**Key principle:** Great positioning is not invented — it is discovered by studying your best customers, your competitors' weaknesses, and the gaps in the market no one is claiming.

---

### When to Use This Skill

- After completing GTM Power Hour and ICP Validation
- When product messaging is unclear, inconsistent, or not resonating
- When entering a competitive market and needing differentiation
- When preparing website copy, ad copy, or outbound messaging
- Before writing any customer-facing content
- Triggered by: "how should we position this?", "write our messaging", "what's our differentiation?", "craft our value prop", "competitive positioning"

---

### Step 1: Load Existing GTM Context

Search the workspace for:
- `gtm-power-hour-*.md` — extract: value proposition hypothesis, competitive landscape, target customer
- `gtm-icp-*.md` — extract: validated persona(s), pain hierarchy, jobs-to-be-done, customer language/quotes

If neither file exists, interview the user:
1. What is your product and what does it do?
2. Who is your target customer (role, company size, pain)?
3. Who are your 3 closest competitors?
4. What do you currently say about your product — what's your value prop?
5. What's the single biggest reason customers choose you over alternatives?

Document answers before proceeding.

---

### Step 2: Research the Competitive Landscape

Use `search_web` to research each competitor's actual positioning. Look at:
- Their homepage headline and subheadline
- Their "About" page messaging
- How they describe themselves in press releases and case studies
- G2/Capterra category and how they describe their product there
- Their ads (use search to find examples)

For each competitor, document:

```markdown
## Competitor: [Name]

**Their headline:** 
**Their category claim:** [What they say they are]
**Their primary benefit claim:** 
**Their target audience (stated):** 
**Their proof points:** 
**Their tone/voice:** [Technical / emotional / enterprise / startup / etc.]
**What they don't say:** [Gaps, weaknesses, avoided topics]
```

#### Identify Positioning Gaps

After mapping competitors, look for:
- **Overclaimed territory:** What every competitor is saying (avoid or reframe)
- **Underclaimed territory:** Real customer value no competitor is messaging on
- **Uncontested territory:** A positioning angle nobody owns

This gap analysis is where differentiated positioning lives.

---

### Step 3: Apply the Positioning Framework

Work through each element in order. Each answer informs the next.

#### Element 1: Category Definition

What category does this product compete in?

Options:
- **Existing category:** Compete directly (easier to explain, harder to differentiate)
- **Subcategory:** Carve a niche within an existing category ("AI-native CRM for sales engineers")
- **New category:** Name a new problem space (hardest, but winner-take-all if it works)

Ask: Does the product fit an existing category customers already search for? Or does it solve a problem the market doesn't yet have a word for?

#### Element 2: Competitive Alternatives

What would customers use if this product didn't exist?
- Named competitors
- Manual processes / spreadsheets
- Internal builds
- Doing nothing (status quo)

**This is the real baseline for differentiation** — not just named competitors.

#### Element 3: Unique Attributes

What does this product have that alternatives genuinely don't?
- Features or capabilities
- Data advantages
- Integration ecosystem
- Speed or simplicity
- Business model (e.g., no lock-in, usage-based)
- Expertise or support

**Rule:** Only list attributes that are real and defensible. "Better UX" and "great customer service" are not differentiators unless you can prove them.

#### Element 4: Value Mapping

For each unique attribute, translate it to a customer outcome:

| Attribute (Feature/Capability) | Customer Outcome | Which ICP Cares Most |
|---|---|---|
| [Attribute 1] | [Outcome: saves time / reduces risk / increases revenue / etc.] | [Persona] |
| [Attribute 2] | | |
| [Attribute 3] | | |

#### Element 5: Target Segment Fit

Which customer segment values these outcomes most intensely?
- Cross-reference the ICP pain hierarchy
- The segment with the highest overlap between "what they need most" and "what you uniquely deliver" is your primary positioning target

---

### Step 4: Write the Positioning Statement

Use this template to produce a formal positioning statement. This is an **internal alignment tool** — not copy for external use:

```
For [target customer — specific role/situation],
who [the problem or need they have],
[Product Name] is the [category] that [primary benefit or outcome].
Unlike [primary competitive alternative],
we [key differentiator that matters to this customer].
```

Write 2–3 variants if the product serves distinct segments with different value drivers. Present all variants and recommend the strongest.

---

### Step 5: Build the Strategic Narrative

The strategic narrative gives context for why your product exists and why now. It works at the sales, marketing, and fundraising level.

Five-part structure:

#### 1. The Old World (Status Quo Pain)
Describe how the target customer's problem is handled today. Be vivid and specific. Use customer language from the ICP research.

> "Today, [customer type] deal with [specific problem]. They spend [time/money/energy] on [workaround]. This leads to [consequence]."

#### 2. The Shift (Why Now)
What changed — technologically, economically, behaviorally, or regulatorily — that makes the old approach insufficient or a new approach possible?

> "But [X has changed]. [Trend, technology, or event] means [old approach no longer works / new opportunity exists]."

#### 3. The New World (The Vision)
Describe the future state where the problem is solved. What does success look like for the customer?

> "In the new world, [customer type] can [outcome]. They spend their time on [high-value activity] instead of [low-value workaround]."

#### 4. The Product (How You Enable It)
Position the product as the vehicle to get from old world to new world.

> "[Product] makes this possible by [mechanism]. It [key capability], which means [outcome]."

#### 5. The Proof (Evidence It Works)
Back up the narrative with specific evidence: metrics, customer quotes, case study results, or third-party validation.

> "Companies using [Product] have [specific result]. [Customer name] achieved [outcome] in [timeframe]."

---

### Step 6: Build the Messaging Architecture

Produce the full messaging architecture document:

```markdown
# Messaging Architecture — [Product Name]
## Date: [date]
## Version: [1.0]

---

## Core Positioning Statement
For [target customer] who [need/situation],
[Product] is the [category] that [primary benefit].
Unlike [alternative], we [key differentiator].

---

## Headline (6 words or fewer)
[Primary value in fewest possible words]

**Alternatives considered:**
- 
- 

---

## Subheadline (1 sentence)
[Expand on the headline with specificity — what it does, for whom, and the key outcome]

---

## Elevator Pitch (30 seconds / ~75 words)
[Problem → Solution → Differentiation → Proof point]

---

## Boilerplate (1 paragraph)
[Standard product/company description for press releases, bios, directory listings]

---

## Strategic Narrative Summary
**The Old World:** 
**The Shift:** 
**The New World:** 
**The Product:** 
**The Proof:** 

---

## Key Messages by Audience

### For [Primary Persona — e.g., "VP of Sales"]:
- **Lead with:** [The outcome or pain that resonates most]
- **Emphasize:** [The feature/capability that delivers it]
- **Proof point:** [Metric, customer story, or data]
- **Call to action:** 

### For [Secondary Persona — e.g., "SDR / End User"]:
- **Lead with:** 
- **Emphasize:** 
- **Proof point:** 
- **Call to action:** 

### For [Economic Buyer / Finance / Procurement]:
- **Lead with:** [ROI, risk reduction, or cost savings]
- **Emphasize:** 
- **Proof point:** 

---

## Objection Handling

| Objection | Root Cause | Response |
|---|---|---|
| "We already have [competitor]" | Switching cost fear | |
| "It's too expensive" | Value not clear | |
| "We'll build it internally" | Trust gap | |
| "Not a priority right now" | Urgency gap | |
| [Product-specific objection] | | |

---

## Messaging Don'ts
[Words, phrases, or claims to avoid — either because competitors already own them or because they erode trust]
- Avoid: 
- Avoid: 
- Avoid: 

---

## SEO / Search Demand Alignment
[Primary search terms this messaging should rank for or capture]
- Primary keyword: 
- Secondary keywords: 
- Long-tail intents: 
```

---

### Step 7: Produce Channel-Specific Copy Angles

Based on the messaging architecture, recommend specific copy angles for:

#### Website Homepage
- Hero headline option(s)
- Hero subheadline
- CTA button text
- Social proof placement strategy (what to show and where)

#### Paid Ads
- 3 headline variants (different angles: pain, outcome, differentiation)
- Description copy
- Which audience to target for each angle

#### Cold Outbound (Email / LinkedIn)
- Opening hook (reference a pain signal, not a product pitch)
- Value proposition in one sentence
- Soft CTA that doesn't ask for a meeting

#### Content Marketing
- 3 content angles that support the strategic narrative
- Suggested formats (case study, how-to, comparison, data report)

---

### Step 8: Save the Positioning Kit

Save the complete output as:
```
gtm-positioning-[product-name].md
```

The file should contain:
1. Competitive landscape analysis with gap findings
2. Positioning framework completion (5 elements)
3. Positioning statement (primary + alternatives)
4. Strategic narrative (5-part)
5. Messaging architecture document
6. Channel-specific copy angles

After saving, update the original `gtm-power-hour-[product-name].md` value proposition and competitive landscape sections with the validated, refined versions.

---

### Output Checklist

Before finishing, confirm:
- [ ] Existing GTM Power Hour and ICP files loaded (or user interviewed)
- [ ] Competitor positioning researched with real evidence (not guesses)
- [ ] Positioning gaps identified
- [ ] All 5 positioning framework elements completed
- [ ] Positioning statement written (primary + 1–2 alternatives)
- [ ] Strategic narrative completed (5 parts)
- [ ] Messaging architecture fully populated
- [ ] Objection handling table completed
- [ ] Channel-specific copy angles provided
- [ ] Document saved as `gtm-positioning-[product-name].md`

---

## § Pricing

# GTM Pricing

Test willingness to pay, design pricing models, and create compelling offers. Based on Maja Voje's Module 4.

---

### When to Use This Skill

- After completing GTM Power Hour, ICP Validation, and Positioning
- When setting an initial price for a new product or feature
- When validating whether your current price is optimal
- When designing tier structures, freemium layers, or offer bundles
- Triggered by: "how should we price this?", "what's our pricing model?", "design our offer", "willingness to pay", "freemium vs paid"

---

### Pricing Frameworks

#### 1. Van Westendorp Price Sensitivity Meter
Find the acceptable price range using 4 questions:
- At what price would this be so cheap you'd question quality?
- At what price is this a great deal?
- At what price is this getting expensive but you'd still consider?
- At what price is this too expensive?

Plot the four curves to find:
- **Acceptable Price Range**: between "too cheap" and "too expensive" intersections
- **Optimal Price Point (OPP)**: intersection of "too cheap" and "too expensive"
- **Indifference Price Point (IDP)**: intersection of "cheap/good value" and "getting expensive"

#### 2. Gabor-Granger Method
Direct price testing: would you buy at $X? Iterate up and down from an anchor.
- Start with a mid-range anchor
- Ask: "Would you buy at this price?" → Yes/No/Maybe
- If yes, increase price; if no, decrease
- Produces a demand curve showing purchase likelihood at each price point
- Best used in surveys or sales calls with 20+ respondents

#### 3. Conjoint Analysis (Simplified)
Test bundles of features at different price points.
- Create 3-5 feature packages at varying price points
- Ask prospects to rank or choose between packages
- Reveals which features drive willingness to pay
- Use for designing tiered plans

#### 4. Value-Based Pricing
Price based on value delivered, not cost or competitor benchmarks.
- Quantify the outcome the customer gets (time saved, revenue generated, risk reduced)
- Price at 10-20% of the value delivered (rule of thumb)
- Anchor to economic impact, not feature count

---

### Pricing Model Options

| Model | Best For | Pros | Cons |
|---|---|---|---|
| Flat rate | Simple products, predictable use | Easy to sell, predictable revenue | Leaves money on table at high usage |
| Per seat/user | Team tools, collaboration | Scales with customer growth | Penalizes power users, discourages adoption |
| Usage-based | APIs, infrastructure, consumption | Aligns cost to value, low entry | Unpredictable revenue, hard to forecast |
| Freemium | Self-serve, high volume | Low friction adoption, viral | High support cost, conversion challenge |
| Reverse trial | SaaS with power features | Shows full value before paywall | Requires polished product at launch |
| Hybrid (base + usage) | Platform + consumption | Predictable floor + upside | Complex to communicate |

---

### Offer Design Framework

```markdown
# Offer Design — [Product]

## Core Offer
- What's included: 
- Price: 
- Target: [adoption or profit optimization]

## Tier Structure (if applicable):
| Tier | Features | Price | Target Persona |
|---|---|---|---|

## Pricing Anchors
- Competitor A: $X for [scope]
- Competitor B: $X for [scope]
- Your positioning: [cheaper/premium/different axis]

## Value Metrics
- Primary metric: [what the customer pays for]
- Why this metric: [aligns incentives how?]

## Risk Reducers
- Free trial: [yes/no, duration]
- Money-back guarantee: [yes/no, terms]
- Pilot program: [yes/no, scope]

## Revenue Projections (90-day)
- Conservative: 
- Expected: 
- Optimistic: 
```

---

### Adoption vs. Profit Optimization

**Optimize for Adoption when:**
- Pre-product-market fit (need feedback and usage data)
- Network-effects product (value increases with users)
- Market share play (land and expand)
- Low marginal cost of serving additional users

**Optimize for Profit when:**
- Strong product-market fit confirmed
- High-touch delivery limits scale
- Enterprise or high-ACV segment
- Profitable unit economics required by investors

---

### Revenue Projection Formula

```
Conservative: [lowest viable conversion rate] × [addressable leads] × [lowest tier price]
Expected: [realistic conversion rate] × [addressable leads] × [blended ACV]
Optimistic: [best-case conversion] × [addressable leads] × [average expansion ACV]
```

---

### A/B Testing Pricing

- **Test 1**: Two landing pages with different price points, measure conversion
- **Test 2**: Sales call split — quote price A to first half, price B to second half
- **Test 3**: Reverse trial vs. freemium for activation rate
- Track: conversion rate, time-to-close, churn rate at 30/60/90 days, expansion revenue
- Minimum sample: 50 prospects per variant for statistical significance

---

### Instructions

1. Load existing GTM artifacts if available (Power Hour, ICP, Positioning)
2. Research competitor pricing in detail (fetch pricing pages, check reviews for pricing complaints)
3. Determine whether the user should optimize for **ADOPTION** (lower price, higher volume) or **PROFIT** (higher price, lower volume)
4. Walk through the Van Westendorp or Gabor-Granger framework based on available data
5. Design the offer structure with tiers, anchors, and risk reducers
6. Calculate simple revenue projections at different price points
7. Produce an "Offer Design Kit" saved to workspace as `offer-design-[product].md`
8. Recommend an A/B testing approach for validating the price

---

### Output Format

Save to workspace: `offer-design-[product-name].md`

Include:
- Completed Offer Design Framework (filled in)
- Pricing model recommendation with rationale
- Competitor pricing comparison table
- Revenue projections (conservative / expected / optimistic)
- A/B test design for price validation
- Next actions with owner and deadline

---

## § Motion

# GTM Motion

Select and execute your first GTM motion to generate initial traction and growth. Based on Maja Voje's Module 5.

---

### When to Use This Skill

- After completing Power Hour, ICP Validation, Positioning, and Pricing
- When choosing how to acquire your first customers
- When deciding between PLG, sales-led, community, content, or partnership approaches
- When planning a 90-day execution sprint
- Triggered by: "what's our go-to-market motion?", "how do we get customers?", "build our growth plan", "PLG vs sales-led", "channel strategy"

---

### GTM Motions Overview

Pick one motion to start. Spreading across multiple motions at launch dilutes focus and burns resources.

#### 1. Product-Led Growth (PLG)
- **Best for**: Self-serve products, dev tools, low-friction onboarding
- **Key metrics**: Time to value, activation rate, organic expansion
- **Playbook**: Free tier → activation event → expansion trigger → viral loop
- **Winning pattern**: Remove all friction before the "aha moment"; let the product sell itself
- **Examples**: Slack, Notion, Figma, Vercel, Calendly

#### 2. Sales-Led Growth (SLG)
- **Best for**: High ACV, complex products, enterprise buyers
- **Key metrics**: Pipeline created, close rate, ACV, sales cycle length
- **Playbook**: ICP targeting → outbound sequence → demo → pilot → close
- **Winning pattern**: Nail the demo, build a repeatable sales motion before hiring reps
- **Examples**: Salesforce, Palantir, Databricks, Gong

#### 3. Community-Led Growth (CLG)
- **Best for**: Developer tools, open-source, passion products, niche professionals
- **Key metrics**: Community size, engagement rate, contributor count, community-sourced pipeline
- **Playbook**: Open-source or free tool → community → adoption → commercial layer
- **Winning pattern**: Give away something genuinely useful; community drives word-of-mouth
- **Examples**: HashiCorp, Hugging Face, Supabase, dbt

#### 4. Content-Led Growth
- **Best for**: Thought leadership, SEO-driven acquisition, educational products
- **Key metrics**: Organic traffic, email list size, content-to-trial conversion rate
- **Playbook**: Educational content → SEO → lead magnet → nurture sequence → convert
- **Winning pattern**: Own a specific keyword cluster or content format your ICP searches for
- **Examples**: HubSpot, Ahrefs, Buffer, Intercom

#### 5. Partnership / Ecosystem-Led Growth
- **Best for**: Platform plays, integrations, marketplace products
- **Key metrics**: Partner count, integration installs, co-sell revenue, partner-sourced pipeline
- **Playbook**: Build integrations → co-market with platform → ride ecosystem network effects
- **Winning pattern**: Become the best-in-class app in a marketplace your ICP already uses
- **Examples**: Stripe, Zapier, Shopify apps, Salesforce AppExchange

---

### Motion Selection Matrix

| Factor | PLG | SLG | CLG | Content | Partnership |
|---|---|---|---|---|---|
| ACV < $100/mo | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| ACV $100–1K/mo | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| ACV > $1K/mo | ⚠️ | ✅ | ⚠️ | ⚠️ | ✅ |
| Technical buyer | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| Non-technical buyer | ⚠️ | ✅ | ❌ | ✅ | ⚠️ |
| Solo founder capacity | ✅ | ❌ | ⚠️ | ✅ | ⚠️ |
| Fast validation (< 30 days) | ✅ | ❌ | ⚠️ | ❌ | ❌ |
| Network effects product | ✅ | ⚠️ | ✅ | ❌ | ✅ |
| Requires education | ⚠️ | ✅ | ⚠️ | ✅ | ❌ |

**Key**: ✅ Strong fit | ⚠️ Possible with caveats | ❌ Poor fit

---

### 90-Day GTM Sprint Template

```markdown
# 90-Day GTM Sprint — [Product]
## Motion: [selected motion]

### Week 1–2: Foundation
- [ ] Finalize positioning and messaging
- [ ] Set up analytics/tracking (events, funnel, activation)
- [ ] Create or update landing page
- [ ] Define activation event (the action that predicts retention)
- [ ] Set up feedback collection (Typeform, Intercom, Notion)

### Week 3–4: First Traction
- [ ] Launch in [specific channel]
- [ ] Reach [n] users/conversations
- [ ] Measure activation rate (% who hit activation event)
- [ ] Collect first 3–5 testimonials or case quotes

### Week 5–8: Iterate
- [ ] Analyze funnel: where are users dropping off?
- [ ] Double down on top-performing channel or message
- [ ] Kill underperforming channels (ruthlessly)
- [ ] Iterate on onboarding based on activation data

### Week 9–12: Scale Signal
- [ ] Hit [target metric]
- [ ] Document the repeatable playbook
- [ ] Decide: double down on this motion or pivot
- [ ] Plan next 90-day sprint

### Success Criteria:
- Primary metric: 
- Secondary metric: 
- Kill criteria: [what would make us abandon this motion]
```

---

### Activation Event Framework

The activation event is the single action that most predicts long-term retention. Define it before launch.

**Format**: "[User role] [completed action] within [time window]"

**Examples**:
- Slack: Team sends 2,000 messages (team-level, not user-level)
- Dropbox: User uploads first file within 24 hours
- HubSpot: User creates and sends first email campaign
- Figma: User shares a design file with a collaborator

**How to find yours**:
1. Look at your best retained users — what did they do in session 1 that churned users didn't?
2. Run a cohort analysis: users who did [X] in 72 hours vs. those who didn't
3. If you lack data, hypothesize and instrument for it now

---

### Channel Prioritization Framework

Rank candidate channels by:
1. **Reach** — How many of your ICP can you access?
2. **Conversion** — What % typically convert in this channel?
3. **Cost** — CAC in time and money
4. **Speed** — How fast will you get signal?
5. **Control** — Can you turn it on/off? Or is it algorithmic?

Start with the channel where you have an **unfair advantage** (existing audience, relationships, domain expertise).

---

### Tracking Setup Recommendations

| Motion | Must-Track Events | Recommended Tools |
|---|---|---|
| PLG | Signup, activation event, feature adoption, invite sent | Mixpanel, PostHog, Amplitude |
| SLG | Lead created, demo booked, demo completed, proposal sent, closed | HubSpot, Salesforce, Attio |
| CLG | Member joined, post created, member referred user, commercial conversion | Discord analytics, Common Room |
| Content | Organic sessions, email signup, content-to-trial, keyword rankings | GA4, Search Console, ConvertKit |
| Partnership | Integration installs, partner-referred signups, co-sell opportunities | Crossbeam, PartnerStack |

---

### Instructions

1. Load all prior GTM artifacts (Power Hour, ICP, Positioning, Pricing)
2. Assess the user's situation: solo founder or team? Budget? Technical or non-technical buyer? ACV range?
3. Use the Motion Selection Matrix to recommend a primary motion with rationale
4. Research 2–3 case studies of similar products using that motion
5. Generate a customized 90-Day GTM Sprint plan with specific actions and metrics
6. Define the activation event and day-3 retention trigger
7. Set up tracking recommendations for the chosen motion
8. Produce a "GTM Sprint Plan" document saved to workspace

---

### Output Format

Save to workspace: `gtm-sprint-[product-name].md`

Include:
- Motion recommendation with rationale (reference the matrix)
- Completed 90-Day Sprint Plan (filled in with specifics)
- Activation event definition
- Channel prioritization ranking
- Tracking setup checklist
- 2–3 comparable case studies with lessons
- Kill criteria and decision date

---

## Workflow Sequence

Each module in this suite produces artifacts that feed the next. Run them in order for a complete GTM strategy, or enter at the appropriate stage if prior work already exists.

### Module Dependencies

```
Power Hour
  └─► Produces: gtm-power-hour-[product].md
        └─► ICP Validation
              └─► Consumes: ICP hypothesis, value prop
              └─► Produces: gtm-icp-[product].md
                    └─► Positioning
                          └─► Consumes: validated persona, pain hierarchy, customer language
                          └─► Produces: gtm-positioning-[product].md
                                └─► Pricing
                                      └─► Consumes: ICP, positioning, value framing
                                      └─► Produces: offer-design-[product].md
                                            └─► Motion
                                                  └─► Consumes: all prior artifacts
                                                  └─► Produces: gtm-sprint-[product].md
```

### What Each Module Feeds Forward

| Completed Module | Key Output Used By Next Module |
|---|---|
| **Power Hour** | ICP hypothesis → ICP Validation; pricing model hypothesis → Pricing; channel hypotheses → Motion |
| **ICP Validation** | Validated persona + pain hierarchy → Positioning (messaging); beachhead segment → Motion (who to target first); customer language (exact quotes) → Positioning (copy) |
| **Positioning** | Positioning statement → Pricing (value framing justifies price); messaging architecture → Motion (channel copy); strategic narrative → all external content |
| **Pricing** | Offer design + price point → Motion (what to offer in outreach); adoption vs. profit optimization → Motion (PLG vs. SLG selection); revenue projections → 90-day sprint success criteria |
| **Motion** | 90-day sprint → execution; activation event definition → product instrumentation; channel prioritization → budget and time allocation |

### Decision Points Between Modules

After **Power Hour**: If the ICP hypothesis is weak or untested, go to ICP Validation next. If the ICP is already clear from prior customer work, you may skip ahead to Positioning — but revisit ICP Validation if messaging doesn't resonate.

After **ICP Validation**: If multiple segments score similarly on the beachhead matrix, use Positioning to find where your differentiation is strongest, then return to confirm the beachhead choice.

After **Positioning**: If the value you're messaging doesn't have a clear price anchor, run Pricing before building channel assets. If price is already established, proceed directly to Motion.

After **Pricing**: If the pricing model points to freemium or self-serve, PLG is likely the right motion. If it points to high ACV with a complex sale, SLG. Use the Motion Selection Matrix to confirm.

After **Motion**: Revisit earlier modules after 30–60 days with real traction data. The ICP often sharpens significantly once you see who actually converts and stays.

### Artifact Cross-Reference

All five modules save artifacts to the workspace. When running any module other than Power Hour, always search for prior artifacts first:

```
gtm-power-hour-[product].md      ← foundation hypothesis
gtm-icp-[product].md             ← validated customer profile
gtm-positioning-[product].md     ← messaging architecture + positioning kit
offer-design-[product].md        ← pricing and offer structure
gtm-sprint-[product].md          ← 90-day execution plan
```

If artifacts exist, load and reference them. If they contradict new findings, flag the discrepancy and recommend updating the earlier document before proceeding.
