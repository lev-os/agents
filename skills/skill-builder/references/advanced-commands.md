# Advanced Commands & Configuration

## Large Docs (10K+ Pages)

```bash
# Estimate page count
skill-seekers estimate configs/godot.json

# Auto-split into router + sub-skills
python3 -m skill_seekers.cli.split_config configs/godot.json --strategy router

# Scrape all in parallel
for config in configs/godot-*.json; do
  skill-seekers scrape --config $config --async --workers 8 &
done
wait

# Generate router + package
python3 -m skill_seekers.cli.generate_router configs/godot-*.json
python3 -m skill_seekers.cli.package_multi output/godot*/
```

## Async Mode with Checkpoint/Resume

```bash
# Async scraping (2-3x faster for 500+ pages)
skill-seekers scrape --config config.json --async --workers 8

# Resume interrupted scrape
skill-seekers scrape --config config.json --resume

# Fresh start (clear checkpoint)
skill-seekers scrape --config config.json --fresh
```

## Three-Stream GitHub Analysis (v2.6.0+)

```python
from skill_seekers.cli.unified_codebase_analyzer import UnifiedCodebaseAnalyzer

analyzer = UnifiedCodebaseAnalyzer()
result = analyzer.analyze(
    source="https://github.com/facebook/react",
    depth="c3x",  # "basic" (1-2 min) or "c3x" (20-60 min)
    fetch_github_metadata=True
)

# Code stream: design patterns, test examples
# Docs stream: README, repository docs
# Insights stream: stars, common issues, metadata
```

## Skill_Seekers Feature Matrix

| Feature | Version | Notes |
|---------|---------|-------|
| Website scraping | v1.0+ | llms.txt auto-detection, 8 presets |
| PDF extraction | v1.2+ | OCR, tables, parallel, caching |
| GitHub analysis | v2.0+ | AST parsing, conflict detection |
| Multi-source unified | v2.0+ | Combine all sources with merging |
| Multi-LLM export | v2.5+ | Claude, Gemini, ChatGPT, Markdown |
| Three-stream GitHub | v2.6+ | Code + Docs + Insights streams |

## Large Docs Splitting Strategy

| Pages | Strategy |
|-------|----------|
| < 5K | Single skill, no splitting |
| 5K-10K | Consider category-based split |
| 10K-30K | Router + categories recommended |
| 30K+ | Router + categories strongly recommended |

## Async Mode Tuning

| Doc Size | Workers | Flag |
|----------|---------|------|
| 100-500 pages | 4 | `--async --workers 4` |
| 500-2000 pages | 8 | `--async --workers 8` |
| 2000+ pages | 8 | `--async --workers 8 --no-rate-limit` |

## Troubleshooting (Quick)

| Problem | Cause | Fix |
|---------|-------|-----|
| `skill-seekers: command not found` | Not installed or venv not active | `source venv/bin/activate` or see `references/setup.md` |
| No content extracted | Wrong CSS selector | Test selectors: `article`, `main`, `div[role="main"]` |
| 429 / rate limited | Too aggressive scraping | Add rate limit config or use `--async --workers 4` |
| Python version error | < 3.10 | `brew install python@3.11` (macOS) |
| Poor categorization | Config keywords mismatch | Edit `categories` in config JSON |
| Scrape interrupted | Network/crash | `skill-seekers scrape --config config.json --resume` |

For detailed troubleshooting, see `references/troubleshooting.md`.
