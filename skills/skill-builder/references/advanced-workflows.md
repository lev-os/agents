# Advanced Workflows

Advanced documentation codification workflows for complex scenarios.

## Large Documentation (10K+ Pages)

### When to Split

| Pages | Recommendation | Strategy |
|-------|---------------|----------|
| < 5K | One skill | No splitting |
| 5K - 10K | Consider splitting | Category-based |
| 10K - 30K | Recommended | Router + Categories |
| 30K+ | Strongly recommended | Router + Categories |

### Split Strategies

#### 1. Router + Categories (Recommended for 10K+)

Creates intelligent hub skill that routes to specialized sub-skills:

```bash
# Auto-split by categories with router
python3 -m skill_seekers.cli.split_config configs/godot.json --strategy router

# Creates:
# - godot.json (router/hub)
# - godot-scripting.json
# - godot-2d.json
# - godot-3d.json
# - godot-physics.json
```

**Benefits:**
- Natural user experience (ask any question)
- Router automatically directs to correct sub-skill
- Faster scraping (parallel execution)
- Better Claude performance (focused context)

#### 2. Category Split

Multiple independent skills by topic:

```bash
python3 -m skill_seekers.cli.split_config configs/godot.json --strategy category
```

User must know which skill to use.

#### 3. Size-Based Split

Split every N pages (for docs without clear categories):

```bash
python3 -m skill_seekers.cli.split_config configs/large.json \
  --strategy size \
  --target-pages 5000
```

### Complete Large Docs Workflow

```bash
# 1. Estimate page count (1-2 minutes)
skill-seekers estimate configs/godot.json
# Output: ~40,000 pages estimated

# 2. Split into focused sub-skills
python3 -m skill_seekers.cli.split_config configs/godot.json \
  --strategy router \
  --target-pages 5000

# 3. Scrape all in parallel (4-8 hours instead of 20-40!)
for config in configs/godot-*.json; do
  skill-seekers scrape --config $config --async --workers 8 &
done
wait

# 4. Generate router skill
python3 -m skill_seekers.cli.generate_router configs/godot-*.json

# 5. Package all skills
python3 -m skill_seekers.cli.package_multi output/godot*/

# 6. Upload all .zip files to Claude
```

**Time savings:** Parallel execution: 4-8 hours vs 20-40 hours sequential

## Async Mode (2-3x Faster)

### When to Use Async

- ✅ Large documentation (500+ pages)
- ✅ High network latency
- ✅ Memory constrained environments
- ❌ Small docs (< 100 pages) - overhead not worth it

### Async Mode Settings

```bash
# Small docs (~100-500 pages)
skill-seekers scrape --config config.json --async --workers 4

# Medium docs (~500-2000 pages)
skill-seekers scrape --config config.json --async --workers 8

# Large docs (2000+ pages) with no rate limiting
skill-seekers scrape --config config.json --async --workers 8 --no-rate-limit
```

### Performance Comparison

| Mode | Speed | Memory | Use Case |
|------|-------|--------|----------|
| Sync (threads) | ~18 pages/sec | 120 MB | Small docs |
| Async | ~55 pages/sec | 40 MB | Large docs |

**Result:** 3x faster, 66% less memory

## Checkpoint & Resume

### Enabling Checkpoints

Add to config:
```json
{
  "checkpoint": {
    "enabled": true,
    "interval": 1000  // Save every 1000 pages
  }
}
```

### Resume Interrupted Scrape

```bash
# Resume from last checkpoint
skill-seekers scrape --config config.json --resume

# Start fresh (clear checkpoint)
skill-seekers scrape --config config.json --fresh
```

**Benefits:**
- Never lose hours of scraping progress
- Auto-saves on Ctrl+C
- Configurable save intervals

## Enhancement Options

### LOCAL Enhancement (No API Key)

Uses your Claude Code Max plan:

```bash
# During scraping
skill-seekers scrape --config config.json --enhance-local

# After scraping
skill-seekers enhance output/myframework/
```

**Time:** ~60 seconds
**Quality:** 9/10 (comparable to API)
**Cost:** Free (uses Claude Code Max)

### API Enhancement (Requires Key)

Uses Anthropic API:

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# During scraping
skill-seekers scrape --config config.json --enhance

# After scraping
skill-seekers-enhance output/myframework/
```

**Time:** ~30 seconds
**Quality:** 9/10
**Cost:** ~$0.15-$0.30 per skill

### Enhancement Benefits

- Transforms 75-line templates into 500+ line guides
- Extracts 5-10 best code examples
- Creates comprehensive quick reference
- Adds domain-specific key concepts
- Provides navigation guidance

## Custom Configurations

### Creating Custom Configs

#### Method 1: Interactive Mode

```bash
skill-seekers scrape --interactive
# Follow prompts to configure URL, selectors, patterns
```

#### Method 2: Copy and Modify

```bash
# Copy similar preset
cp configs/react.json configs/myframework.json

# Edit configuration
nano configs/myframework.json

# Test with limited pages first
# Set "max_pages": 20 in config

# Run test
skill-seekers scrape --config configs/myframework.json
```

### Configuration Structure

```json
{
  "name": "myframework",
  "description": "When to use this skill",
  "base_url": "https://docs.myframework.com/",
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/docs", "/guide"],
    "exclude": ["/blog", "/about", "/_static/"]
  },
  "categories": {
    "getting_started": ["intro", "quickstart", "getting started"],
    "api": ["api", "reference", "class", "method"],
    "guides": ["guide", "how-to", "tutorial"]
  },
  "rate_limit": 0.5,
  "max_pages": 500,
  "checkpoint": {
    "enabled": true,
    "interval": 1000
  }
}
```

### Finding CSS Selectors

Test selectors before creating config:

```python
from bs4 import BeautifulSoup
import requests

url = "https://docs.example.com/page"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Try different selectors
print("article:", soup.select_one('article'))
print("main:", soup.select_one('main'))
print("div[role='main']:", soup.select_one('div[role="main"]'))
print("div.content:", soup.select_one('div.content'))
print("div.documentation:", soup.select_one('div.documentation'))

# Test code blocks
print("Code blocks:", len(soup.select('pre code')))
```

## Unified Multi-Source Skills

### Creating Unified Configs

Combine documentation + GitHub + PDF with conflict detection:

```json
{
  "name": "myframework",
  "description": "Complete framework knowledge from docs + code",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.myframework.com/",
      "extract_api": true,
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "owner/myframework",
      "include_code": true,
      "code_analysis_depth": "surface"
    },
    {
      "type": "pdf",
      "path": "docs/manual.pdf"
    }
  ]
}
```

### Running Unified Scraper

```bash
skill-seekers unified --config configs/myframework_unified.json
```

### Conflict Detection

Automatically detects 4 types of discrepancies:

- 🔴 **Missing in code** (high): Documented but not implemented
- 🟡 **Missing in docs** (medium): Implemented but not documented
- ⚠️ **Signature mismatch**: Different parameters/types
- ℹ️ **Description mismatch**: Different explanations

### Merge Modes

1. **rule-based** (default): Deterministic merging rules
2. **claude-enhanced**: AI-powered intelligent merging

```bash
# Override merge mode
skill-seekers unified --config config.json --merge-mode claude-enhanced
```

## PDF Advanced Features

### Basic PDF Extraction

```bash
skill-seekers pdf --pdf docs/manual.pdf --name myskill
```

### Advanced Features

```bash
# Extract tables + parallel processing
skill-seekers pdf --pdf docs/manual.pdf --name myskill \
  --extract-tables \
  --parallel \
  --workers 8

# Scanned PDFs with OCR (requires: pip install pytesseract Pillow)
skill-seekers pdf --pdf docs/scanned.pdf --name myskill --ocr

# Password-protected PDFs
skill-seekers pdf --pdf docs/encrypted.pdf --name myskill --password mypassword
```

**Performance:**
- Standard: 5-15 minutes
- Parallel (8 workers): 2-5 minutes

## GitHub Analysis

### Basic Repository Scraping

```bash
skill-seekers github --repo facebook/react
```

### With Authentication (Higher Rate Limits)

```bash
export GITHUB_TOKEN=ghp_your_token_here
skill-seekers github --repo owner/repo
```

Get token at: https://github.com/settings/tokens

### Advanced Options

```bash
skill-seekers github --repo fastapi/fastapi \
  --include-issues \
  --max-issues 100 \
  --include-changelog \
  --include-releases \
  --code-analysis-depth deep
```

### What Gets Extracted

- Deep code analysis (AST parsing for Python, JS, TS, Java, C++, Go)
- API functions, classes, methods with parameters and types
- Repository metadata (README, file tree, language breakdown)
- GitHub Issues & PRs with labels and milestones
- CHANGELOG & Releases version history
- Conflict detection vs documentation

**Time:** 5-10 minutes depending on repository size

## Iteration and Caching

### Skip Scraping (Use Cached Data)

Fast rebuilds using previously scraped data:

```bash
# Scrape once
skill-seekers scrape --config configs/react.json

# Rebuild multiple times instantly
skill-seekers scrape --config configs/react.json --skip-scrape
# Time: < 1 minute
```

### Force Re-scrape

Delete cached data:

```bash
rm -rf output/myframework_data/
skill-seekers scrape --config configs/myframework.json
```

## Performance Optimization

### Tips for Faster Scraping

1. **Use async mode** for docs > 500 pages
2. **Enable checkpointing** for docs > 5K pages
3. **Split large docs** into parallel sub-skills
4. **Check for llms.txt** (10x faster if available)
5. **Adjust rate limiting** based on server tolerance

### Memory Optimization

1. **Use async mode** (66% less memory)
2. **Split into smaller skills** (< 5K pages each)
3. **Reduce max_pages** if hitting memory limits

### Time Estimation

| Documentation Size | Sync Mode | Async Mode | Parallel (Split) |
|-------------------|-----------|------------|------------------|
| 100-500 pages | 5-15 min | 2-5 min | N/A |
| 500-2000 pages | 15-45 min | 5-15 min | N/A |
| 5K-10K pages | 2-4 hours | 45-90 min | 30-60 min |
| 10K-40K pages | 8-20 hours | 3-8 hours | 1-4 hours |

## llms.txt Detection

Skill_Seekers automatically checks for llms.txt files before HTML scraping:

### Detection Order

1. `{base_url}/llms-full.txt` (complete documentation)
2. `{base_url}/llms.txt` (standard version)
3. `{base_url}/llms-small.txt` (quick reference)

### Benefits

- ⚡ 10x faster (< 5 seconds vs 20-60 seconds)
- ✅ More reliable (maintained by docs authors)
- 🎯 Better quality (pre-formatted for LLMs)
- 🚫 No rate limiting needed

If no llms.txt found, automatically falls back to HTML scraping.

### Force HTML Scraping

To skip llms.txt detection:

```json
{
  "skip_llms_txt": true
}
```

## Best Practices

1. **Always estimate first** for unknown documentation
2. **Test with max_pages: 20** before full scrape
3. **Use async mode** for large docs
4. **Enable checkpointing** for docs > 5K pages
5. **Split docs > 10K pages** for best performance
6. **Always enhance** SKILL.md (local or API)
7. **Reuse cached data** for iteration
8. **Check for llms.txt** support
9. **Use authentication** for GitHub scraping
10. **Monitor memory** on large scrapes
