# Hidden Gems Discovery Query - Finding NEW Unknown Frameworks

## Purpose
Discover obscure but powerful thinking frameworks NOT yet identified in our seed documents.

## Context
We've cataloged ~495 known frameworks across 15 domains. But we're looking for:
- **Hidden gems**: Obscure frameworks from unexpected sources
- **High novelty**: Counter-intuitive, non-obvious (8+/10 on novelty scale)
- **Practitioner-validated**: Used successfully, not just academic theory
- **Cross-domain applicable**: Work across multiple fields

## Discovery Strategy

### 1. Mine Unusual Sources

**Question for Research Agent:**
```
Find obscure but powerful thinking frameworks and mental models from these non-obvious sources:

1. **Soviet/Russian Innovation**: Beyond TRIZ, what other systematic frameworks came from Soviet engineering, military, or scientific programs?

2. **Ancient Non-Western Philosophy**: Beyond mainstream Buddhism/Taoism/Stoicism, what frameworks exist in:
   - Confucian strategic thinking
   - Hindu decision-making systems (Arthashastra, Yoga Sutras)
   - Islamic scholarship (Al-Ghazali, Ibn Khaldun)
   - African philosophical traditions
   - Indigenous knowledge systems

3. **Niche Academic Fields**:
   - Cybernetics (beyond Ashby)
   - Operations Research (beyond Theory of Constraints)
   - Complexity Science (Santa Fe Institute lesser-known frameworks)
   - Cognitive Science (beyond Kahneman/Tversky)
   - Information Theory (beyond Shannon)

4. **Military/Intelligence**:
   - Beyond OODA Loop - what other mil frameworks exist?
   - Intelligence analysis methodologies
   - Strategic war gaming frameworks
   - Counterintelligence thinking

5. **Obscure Rationality Community**:
   - Beyond Schelling Fence - what other LessWrong/CFAR frameworks?
   - Effective Altruism methodologies
   - Forecasting techniques beyond Tetlock

6. **Hidden Corporate Practices**:
   - Internal frameworks from successful companies not widely published
   - Consulting firm proprietary methods (leaked/published)
   - Startup operator frameworks (from blogs, not books)

Search for frameworks that are:
- Rarely mentioned in mainstream mental models literature
- From specialized communities (engineering, military, philosophy, etc.)
- Counter-intuitive or non-obvious
- Actually used by practitioners (not just academic theory)
- Transferable across domains

For each discovered framework, provide:
- Name and origin (who, when, where)
- Why it's obscure (specialized field, math complexity, non-Western, etc.)
- Why it's powerful (what problems it solves)
- Evidence of practitioner use
- Potential cross-domain applications
```

### 2. Cross-Domain Pattern Mining

**Question for Research Agent:**
```
Identify powerful frameworks by finding patterns that appear in multiple unrelated fields:

Search for:
- What problem-solving patterns appear in BOTH military strategy AND product design?
- What frameworks appear in BOTH physics AND organizational management?
- What methods appear in BOTH ancient philosophy AND modern AI?
- What techniques appear in BOTH biology AND software engineering?

These cross-domain patterns are likely fundamental frameworks worth documenting.

Example: "Feedback loops" appear in systems thinking, cybernetics, biology, software, psychology - suggesting it's a universal pattern.

Find 10 such cross-domain patterns not yet in our catalog.
```

### 3. Obscurity-First Search

**Question for Research Agent:**
```
Find frameworks specifically marked as "obscure", "lesser-known", "hidden gem", "rarely used" in:

1. Academic papers discussing innovation methodologies
2. "Best kept secrets" blog posts from practitioners
3. Conference talks mentioning "techniques we use internally"
4. Reddit/HN discussions: "What framework changed your thinking that nobody talks about?"
5. Book appendices and footnotes (often hide gems)
6. Failed/abandoned methods that actually worked (but weren't marketed well)

Target: Frameworks with novelty score 8+/10 that practitioners swear by but aren't mainstream.
```

### 4. Inverse Search

**Question for Research Agent:**
```
Find frameworks by searching for what they SOLVE rather than what they ARE:

Problems without mainstream solutions:
- "How to prevent value drift over time" → Led us to Schelling Fence
- "How to handle controller complexity mismatch" → Led us to Ashby's Law
- "How to systematically innovate" → Led us to TRIZ

Now search for frameworks solving:
- "How to maintain principle clarity under social pressure"
- "How to coordinate distributed agents without communication"
- "How to make decisions when time/ensemble averages diverge"
- "How to systematically generate breakthrough insights"
- "How to prevent organizational mission drift"
- "How to handle irreversible decisions differently than reversible ones"
- "How to maintain long-term thinking in short-term environments"

What frameworks exist for these meta-problems?
```

### 5. Historical Deep Cuts

**Question for Research Agent:**
```
Find powerful frameworks from:

1. **World War II operations research**: Beyond OODA, what systematic methods emerged?
2. **Cold War strategic thinking**: RAND Corporation, game theory origins
3. **Industrial Revolution innovations**: Beyond Taylorism, what systematic approaches existed?
4. **Victorian engineering**: What frameworks did great engineers use?
5. **Ancient mathematics**: What thinking frameworks from Euclid, Archimedes, etc.?

Target: Methods that were revolutionary in their time but forgotten or underutilized now.
```

## Output Format

For each discovered framework:

```markdown
# [Framework Name] (DISCOVERED)

**Source**: [Origin - person/organization/culture]
**Year/Era**: [When created]
**Original Domain**: [Where it came from]
**Obscurity Factors**:
- [Why hard to find: specialized field, foreign language, out of print, etc.]

**Brief Description**: [2-3 sentences]

**Evidence of Value**:
- [Where it's been successfully used]
- [Outcomes or results]

**Cross-Domain Potential**:
- [What other domains could use this]

**Initial Score Estimate**: [X]/50
- Practitioner: [X]/10
- Clarity: [X]/10
- ROI: [X]/10
- Novelty: [X]/10
- Cross-Domain: [X]/10

**Recommended for**:
- [ ] Full research (high-value gem)
- [ ] Monitor (interesting but needs validation)
- [ ] Skip (too obscure or low-value)

**Search Trail**: [How you found it - for reproducibility]
```

Save to: `docs/hidden-gems/discoveries/[framework-slug].md`

## Quality Filters

**Include if**:
- ✅ Novelty ≥ 7/10 (genuinely non-obvious)
- ✅ Evidence of practitioner use (not just academic)
- ✅ Potential score ≥ 30/50
- ✅ Cross-domain applicable (works in 2+ domains)

**Exclude if**:
- ❌ Consultantware (designed to sell services)
- ❌ Rebranded existing framework
- ❌ Pure academic theory (no implementation evidence)
- ❌ Obvious/trivial

## Target

Discover **20-30 new hidden gems** not in our current seed documents.

Focus on Tier 1 (⭐⭐⭐) level obscurity with high power.

## Next Steps After Discovery

1. Add to relevant domain task.csv as UNKNOWN
2. Run full research protocol (research → analyze → YAML)
3. Validate with quality-validator
4. Tag as "hidden-gem" in YAML metadata
