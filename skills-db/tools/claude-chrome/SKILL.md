---
name: claude-chrome
description: >-
  Control Chrome browser via Claude extension. Use when automating browser
  workflows, filling forms, extracting data from authenticated sites, testing
  web apps, or creating scheduled browser tasks.
---

<!-- TOC: Quick Start | THE EXACT PROMPT | MCP Option | Workflows | References -->

# Claude in Chrome

> **Core Capability:** Control your real Chrome browser with Claude. Works with sites you're already logged into — Gmail, Google Docs, Notion, CRMs — no re-authentication needed.

## Quick Start

```bash
# Update Claude Code
claude update

# Start with Chrome enabled
claude --chrome

# Disable Chrome integration
claude --no-chrome

# Check connection
/chrome

# Enable by default
/chrome → "Enabled by default"
```

---

## THE EXACT PROMPT — Common Tasks

### Navigation

```
Go to github.com/anthropics and click on the "Code" tab
```

### Form Testing

```
Open localhost:3000, try submitting the login form with invalid data,
and check if error messages appear correctly
```

### Data Extraction

```
Go to the product listings page and extract the name, price, and
availability for each item. Save as CSV.
```

### Authenticated Workflow

```
Draft a project update based on our recent commits and add it to
my Google Doc at docs.google.com/document/d/abc123
```

### Form Automation

```
I have contacts in contacts.csv. For each row, go to crm.example.com,
click "Add Contact", and fill in the name, email, and phone fields.
```

### Record Demo GIF

```
Record a GIF showing the checkout flow from adding an item to cart
through to the confirmation page
```

---

## Browser Capabilities

**Navigation & Interaction:**
- Navigate to URLs
- Click elements (buttons, links, form fields)
- Type text into inputs
- Scroll pages, create/manage tabs

**Information Retrieval:**
- Read page content and DOM state
- Access console logs and errors
- Monitor network requests
- Extract structured data

**Advanced:**
- Fill forms automatically
- Record browser actions as GIFs
- Chain browser + terminal commands
- Work across multiple tabs

---

## MCP Alternative: Chrome DevTools

For programmatic control with 26 browser automation tools:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

Or in config:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### Key Tools

| Category | Tools |
|----------|-------|
| Input | click, drag, fill, fill_form, hover, press_key |
| Navigation | navigate_page, new_page, close_page, list_pages |
| Debugging | take_screenshot, evaluate_script, get_console_message |
| Network | list_network_requests, get_network_request |
| Performance | performance_start_trace, performance_analyze_insight |

---

## Extension Features

### Workflow Shortcuts

Create reusable shortcuts (type "/" in extension):

1. Click cursor icon or "/" → "Record workflow"
2. Perform actions while Claude watches
3. Claude generates shortcut with name, description, URL

### Scheduled Tasks

```
1. When creating shortcut, toggle "Schedule"
2. Set frequency: daily, weekly, monthly
3. Choose date/time and model
4. Claude runs automatically
```

**Examples:**
- Daily inbox cleanup at 9am
- Weekly competitor scan every Monday
- Monthly expense report filing

---

## When to Use

**Good for:**
- Form filling and data entry
- Button clicking and navigation
- Extracting data from authenticated pages
- Testing web applications
- Tasks behind logins

**Better manually:**
- One-click tasks (faster by hand)
- Subjective decisions
- Exploratory research

---

## Tips

1. **Be specific** — Ambiguous instructions produce inconsistent results
2. **Add verification** — "Verify you completed all items"
3. **Handle modals** — Dismiss alerts manually, then continue
4. **Use fresh tabs** — If unresponsive, ask for a new tab
5. **Filter console** — Specify patterns vs. requesting all logs

---

## Troubleshooting

**Extension not detected:**
```bash
claude --version  # Should be 2.0.73+
```
Then `/chrome` → "Reconnect extension"

**Browser not responding:**
- Check for blocking modal dialogs
- Ask Claude to create a new tab
- Restart extension in chrome://extensions

---

## Requirements

| Component | Version |
|-----------|---------|
| Chrome | Latest stable |
| Claude Extension | 1.0.36+ |
| Claude Code CLI | 2.0.73+ |
| Claude Plan | Pro/Team/Enterprise/Max |

**Not supported:** Brave, Arc, Edge, WSL, Mobile

---

## References

| Topic | Reference |
|-------|-----------|
| MCP tools | [MCP-TOOLS.md](references/MCP-TOOLS.md) |
| Workflow examples | [WORKFLOWS.md](references/WORKFLOWS.md) |
