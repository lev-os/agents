---
name: blog-writer
description: Technical blog post enhancement workflow with parallel research agents, perplexity-powered source discovery, and image integration. This skill should be used when writing, enhancing, or publishing blog posts that need authoritative sources, hero images, inline diagrams, and interlinking.
---

# Blog Writer

Enhance technical blog posts with authoritative sources, relevant images, and internal links using parallel research agents.

## When to Use

- Writing new blog posts that need research backing
- Enhancing existing posts with sources and images
- Publishing workflow that requires quality gates (sources, images, links)

## Enrichment Loop

The core workflow iterates until quality gates pass:

```
┌─────────────────────────────────────────────────────────────┐
│  BLOG ENHANCEMENT LOOP                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. LOAD    → Read blog content, extract key topics         │
│      ↓                                                      │
│  2. RESEARCH → Dispatch 1-n haiku agents + bird bookmarks   │
│      ↓                                                      │
│  3. ENHANCE  → Add sources, images, interlinks              │
│      ↓                                                      │
│  4. VALIDATE → Check quality gates                          │
│      ↓                                                      │
│  [LOOP back to step 2 until gates pass]                     │
│                                                             │
│  EXIT CONDITIONS:                                           │
│  ✓ 5-10 authoritative sources                               │
│  ✓ 2-3 inline images + 1 hero                               │
│  ✓ Internal links to related posts                          │
│  ✓ Further Reading section                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quality Gates

| Gate | Requirement | Validation Command |
|------|-------------|-------------------|
| Sources | 5-10 external links | `grep -c 'https://' post.mdx` |
| Hero Image | 1 after intro | `head -20 post.mdx \| grep -c '!\['` |
| Inline Images | 2-3 throughout | `grep -c '!\[' post.mdx` |
| Interlinks | Related internal posts | `grep -c '/blog/' post.mdx` |
| Further Reading | Section at end | `grep -c '## Further Reading' post.mdx` |

## Step 1: Load Blog Content

Read the post and extract key elements:

```bash
cat ~/k/presence/www/content/logs/<post>.mdx
```

Identify:
1. **Title and topic** - Main subject
2. **Key terms** - Concepts needing authoritative backing
3. **Sections** - Where images add value
4. **Related posts** - Internal linking opportunities

## Step 2: Research with Multiple Sources

### 2A: Parallel Haiku Agents via Perplexity

Dispatch multiple haiku agents for cost-efficient parallel research:

```python
# Parallel dispatch pattern
Task(subagent_type=general-purpose, model=haiku,
     prompt="Use mcp__perplexity-mcp__search for '[topic] 2025 authoritative'")
Task(subagent_type=general-purpose, model=haiku,
     prompt="Use mcp__perplexity-mcp__reason for '[complex topic] explanation'")
```

### 2B: Bird CLI for Fresh AI Resources

Fetch recent bookmarks from X/Twitter for bleeding-edge sources:

```bash
# Get AI-related bookmarks
bird bookmarks -n 30 --json | jq -r '
  .[] | select(.text | test("AI|LLM|agent|RAG|Claude|GPT"; "i"))
  | "\(.user.name): \(.text[0:100])... \(.url)"
'

# Filter by specific topic
bird bookmarks -n 50 --plain | grep -i "agent\|orchestration\|swarm"
```

**Bird CLI Reference:**
```bash
bird bookmarks -n <count>     # Fetch N bookmarks
bird bookmarks --all          # Fetch all (paged)
bird bookmarks --json         # JSON output for parsing
bird bookmarks --plain        # Stable text output
```

**Note:** Requires X/Twitter auth configured in `~/.config/bird/config.json5`

### 2C: Perplexity Direct Queries

For deep research, call perplexity tools directly:

```
mcp__perplexity-mcp__search   → Quick authoritative sources
mcp__perplexity-mcp__reason   → Deep explanations, comparisons
mcp__perplexity-mcp__deep_research → Comprehensive analysis
```

### Query Patterns

| Topic | Query Template |
|-------|---------------|
| Technical | "[term] tutorial 2025 2026 authoritative" |
| Benchmarks | "[domain] benchmarks statistics 2025" |
| Best Practices | "[topic] best practices patterns 2025" |
| Comparisons | "[A] vs [B] comparison 2025" |

### Source Quality Criteria

Prefer sources that are:
- **Recent** (2024-2026)
- **Authoritative** (official docs, papers, major tech companies)
- **Actionable** (tutorials, guides, implementation patterns)
- **Diverse** (mix of blogs, docs, papers, videos, tweets)

## Step 3: Enhance Post

### Adding Sources

Weave sources naturally into the text:

```markdown
# Good - inline with context
Research shows [layered mitigation strategies reduce hallucinations by 25-45%](https://arxiv.org).

# Avoid - citation dump at end only
```

### Adding Images

Strategic placement:

1. **Hero image** - After intro paragraph, before first H2
2. **Section images** - At start of major sections
3. **Diagrams** - For complex concepts (pipelines, architectures)

```markdown
![Descriptive alt text](/static/image-name.png)
```

### Image Generation

Use free AI tools for technical diagrams:
- **Perchance AI** - No signup, quick generations
- **Canva Magic Media** - Free tier with export
- **Stable Diffusion** - Best for technical illustrations

Prompt pattern:
```
"clean flowchart of [concept], minimalist line art, dark background,
high contrast, vector style, labeled nodes"
```

### Adding Interlinks

Link to related internal posts:

```markdown
See our [AI Dictionary](/blog/logs/003-ai-dictionary) for term definitions.
This connects to [YAML to Agentic Runners](/blog/logs/002-yaml-to-agentic-runners).
```

## Step 4: Validate and Loop

Run validation:

```bash
echo "=== Quality Gate Validation ==="
echo "Sources:"; grep -c 'https://' post.mdx
echo "Images:"; grep -c '!\[' post.mdx
echo "Further Reading:"; grep -c '## Further Reading' post.mdx
echo "Interlinks:"; grep -c '/blog/' post.mdx
```

**Decision:**
- All gates pass → COMPLETE
- Gates not met → Return to Step 2 with refined queries

## MDX Format Reference

```yaml
---
title: "Post Title"
date: 2026-01-14
description: "Short description under 200 chars"
tags: ["tag1", "tag2", "tag3"]
published: true
---
```

**Important:** Do NOT use ESM imports in MDX. Standard markdown only.

## Best Practices

### SEO and Readability
- Use H2 for major sections, H3 sparingly
- Bold key terms at first use
- Keep paragraphs short (2-4 sentences)
- Include code examples where relevant

### Source Integration
- Weave sources into explanations naturally
- Use descriptive link text, not "click here"
- Prefer deep links to specific sections
- Mix inline sources + Further Reading section

### Image Optimization
- Use descriptive alt text for accessibility
- Keep file sizes under 500KB
- Use PNG for diagrams, WebP for photos
- Name files descriptively (not image1.png)

## Example Enhancement Session

```
1. LOAD: ~/k/presence/www/content/logs/004-growth-architect.mdx
   → Topics: K-factor, viral loops, B2B SaaS benchmarks, MBTI personas

2. RESEARCH (parallel):
   → Haiku Agent 1: "B2B SaaS conversion benchmarks 2025"
   → Haiku Agent 2: "viral coefficient K-factor optimization"
   → Haiku Agent 3: "MBTI buyer personas B2B marketing"
   → Bird CLI: bird bookmarks -n 30 --json | filter AI/growth

3. ENHANCE:
   → Add 9 inline sources (First Page Sage, Kurve, WDG Agency...)
   → Add hero image placeholder
   → Add 1 section image
   → Add Further Reading with 9 sources
   → Interlink to AI Dictionary and YAML post

4. VALIDATE:
   → Sources: 12 ✓
   → Hero: 1 ✓
   → Images: 1 (need 2 more)
   → Interlinks: 2 ✓

5. LOOP (need more images):
   → Generate 2 more section images
   → Re-validate

6. COMPLETE:
   → All gates pass
```

## Troubleshooting

### Bird CLI Auth Issues
```bash
# Check auth status
bird whoami

# Configure auth (add to ~/.config/bird/config.json5)
{
  "chromeProfile": "Default"  // or firefoxProfile
}
```

### MDX Rendering Errors
- Remove all `import` statements
- Use standard markdown image syntax `![]()`
- Avoid JSX components
