# Troubleshooting Guide

Common issues when using the Documentation Codifier skill.

## Installation Issues

### skill-seekers Command Not Found

**Symptoms:**
```bash
skill-seekers: command not found
```

**Solutions:**

1. **Check if venv is activated:**
   ```bash
   which python3  # Should show venv path
   source venv/bin/activate
   ```

2. **Use Python module syntax:**
   ```bash
   python3 -m skill_seekers scrape --help
   ```

3. **Reinstall in current environment:**
   ```bash
   cd path/to/Skill_Seekers
   pip install -e .
   ```

### Permission Denied During Installation

**Solution:** Use virtual environment instead of global install:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Python Version Too Old

**Error:** `Python 3.10+ required`

**Solution:**
```bash
# macOS
brew install python@3.11
python3.11 -m venv venv

# Ubuntu/Debian
sudo apt install python3.11
python3.11 -m venv venv
```

## Runtime Issues

### No Content Extracted from Website

**Symptoms:** Pages scraped but content is empty

**Cause:** Incorrect CSS selector in config

**Solutions:**

1. **Test selectors manually:**
   ```python
   from bs4 import BeautifulSoup
   import requests

   url = "https://docs.example.com/page"
   soup = BeautifulSoup(requests.get(url).content, 'html.parser')

   # Try different selectors
   print(soup.select_one('article'))
   print(soup.select_one('main'))
   print(soup.select_one('div[role="main"]'))
   print(soup.select_one('div.content'))
   ```

2. **Common working selectors:**
   - `article`
   - `main`
   - `div[role="main"]`
   - `div.content`
   - `div.documentation`

3. **Update config with correct selector:**
   ```json
   {
     "selectors": {
       "main_content": "article"
     }
   }
   ```

### Poor Categorization

**Symptoms:** Pages not organized well in references/

**Solution:** Edit `categories` section with better keywords:

```json
{
  "categories": {
    "getting_started": ["introduction", "quickstart", "tutorial", "getting started"],
    "api": ["api", "reference", "class", "method", "function"],
    "guides": ["guide", "how-to", "example", "tutorial"],
    "concepts": ["concept", "architecture", "overview"]
  }
}
```

### Rate Limiting / Getting Blocked

**Symptoms:** 429 errors, connection refused, or scraping stops

**Solutions:**

1. **Increase rate limit in config:**
   ```json
   {
     "rate_limit": 1.0  // Increase from 0.5 to 1.0 seconds
   }
   ```

2. **Use async mode with conservative settings:**
   ```bash
   skill-seekers scrape --config config.json --async --workers 4
   ```

3. **Check if site has llms.txt:**
   ```bash
   curl https://docs.example.com/llms.txt
   # If exists, it will be used automatically (10x faster, no rate limiting)
   ```

### Tool Won't Use Existing Data

**Symptoms:** Re-scraping even when data exists

**Solution:** Force use of existing data:
```bash
skill-seekers scrape --config config.json --skip-scrape
```

**Or force fresh scrape:**
```bash
rm -rf output/myframework_data/
skill-seekers scrape --config config.json
```

### Scrape Interrupted / Crashed

**Solution:** Resume from checkpoint:
```bash
skill-seekers scrape --config config.json --resume
```

**Start fresh:**
```bash
skill-seekers scrape --config config.json --fresh
```

## Configuration Issues

### Config File Not Found

**Error:** `FileNotFoundError: configs/myframework.json`

**Solution:**
```bash
# Check current directory
pwd
# Should be in Skill_Seekers directory

# Or use absolute path
skill-seekers scrape --config /full/path/to/config.json
```

### Invalid JSON in Config

**Error:** `JSONDecodeError: Expecting property name`

**Solution:**
1. Validate JSON syntax at jsonlint.com
2. Common mistakes:
   - Trailing commas in objects/arrays
   - Missing quotes around keys
   - Single quotes instead of double quotes

### URL Patterns Not Working

**Symptoms:** Wrong pages being scraped or skipped

**Debug approach:**
```json
{
  "url_patterns": {
    "include": ["/docs/", "/api/"],  // Must contain one of these
    "exclude": ["/blog/", "/_static/"]  // Must not contain these
  }
}
```

**Tips:**
- Patterns are substrings, not regex
- Both include and exclude can be empty lists: `[]`
- If include is empty, all URLs pass (unless excluded)
- Exclude is checked after include

## Output Issues

### Enhancement Failed

**Symptoms:** SKILL.md is generic template

**Solutions:**

1. **Verify enhancement ran:**
   ```bash
   ls output/myframework/SKILL.md.backup
   # Should exist if enhancement completed
   ```

2. **Try LOCAL enhancement:**
   ```bash
   skill-seekers enhance output/myframework/
   ```

3. **Check reference files exist:**
   ```bash
   ls output/myframework/references/
   # Should have .md files
   ```

### Package Creation Failed

**Error:** `No such file or directory: output/myframework/`

**Solution:** Ensure skill was built first:
```bash
# Build first
skill-seekers scrape --config config.json

# Then package
skill-seekers package output/myframework/
```

### Upload Failed (API)

**Error:** `ANTHROPIC_API_KEY not set`

**Solution:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
skill-seekers package output/myframework/ --upload
```

**Alternative:** Manual upload:
1. Locate the `.zip` file in `output/`
2. Go to https://claude.ai/skills
3. Click "Upload Skill"
4. Select the `.zip` file

## GitHub-Specific Issues

### GitHub Rate Limiting

**Error:** `403: API rate limit exceeded`

**Solution:** Use authentication:
```bash
export GITHUB_TOKEN=ghp_your_token_here
skill-seekers github --repo owner/repo
```

Get token at: https://github.com/settings/tokens

### Repository Too Large

**Symptoms:** Analysis takes too long or fails

**Solution:** Limit analysis depth:
```json
{
  "sources": [{
    "type": "github",
    "repo": "owner/repo",
    "code_analysis_depth": "surface",  // Not "deep"
    "max_files": 1000
  }]
}
```

## Large Documentation Issues

### Out of Memory

**Symptoms:** Process killed during large scrape

**Solutions:**

1. **Split into smaller skills:**
   ```bash
   python3 -m skill_seekers.cli.split_config configs/large.json --strategy router
   ```

2. **Use async mode (less memory):**
   ```bash
   skill-seekers scrape --config config.json --async --workers 4
   ```

3. **Reduce max_pages:**
   ```json
   {
     "max_pages": 5000  // Instead of 40000
   }
   ```

### Estimate Shows Way More Pages Than Expected

**This is normal** - Documentation sites often have:
- Version archives (v1.0, v2.0, etc.)
- Translations (en, es, fr, etc.)
- Generated API docs
- Search results

**Solution:** Use exclude patterns:
```json
{
  "url_patterns": {
    "exclude": [
      "/v1/", "/v2/", "/archive/",
      "/es/", "/fr/", "/de/",
      "/search", "/api/search"
    ]
  }
}
```

## Getting Further Help

If issues persist:

1. **Check Skill_Seekers documentation:**
   ```bash
   cat ~/.local/share/skill-seekers/README.md
   # Or check: references/skill-seekers-reference.md
   ```

2. **Verify installation:**
   ```bash
   skill-seekers --version
   python3 --version  # Should be 3.10+
   git --version  # Should be 2.30+
   ```

3. **Test with simple config:**
   ```bash
   skill-seekers scrape --name test --url https://react.dev/ --max-pages 20
   ```

4. **Check output logs:**
   Most commands show detailed progress. Read the output carefully for clues.
