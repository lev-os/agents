# Chrome DevTools MCP — 26 Browser Automation Tools

## Table of Contents
- [Installation](#installation)
- [Input Automation](#input-automation)
- [Navigation](#navigation)
- [Debugging](#debugging)
- [Network](#network)
- [Performance](#performance)
- [Configuration](#configuration)

---

## Installation

```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

Or add to MCP config:
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

---

## Input Automation (8 tools)

| Tool | Description | Example |
|------|-------------|---------|
| `click` | Click elements | Click button by selector |
| `drag` | Drag and drop | Reorder items |
| `fill` | Fill input fields | Single input |
| `fill_form` | Fill entire forms | Multiple fields at once |
| `handle_dialog` | Handle alerts/confirms | Accept or dismiss |
| `hover` | Hover over elements | Trigger dropdowns |
| `press_key` | Keyboard input | Enter, Tab, shortcuts |
| `upload_file` | Upload files | File inputs |

---

## Navigation (6 tools)

| Tool | Description |
|------|-------------|
| `navigate_page` | Go to URL |
| `new_page` | Create new tab |
| `close_page` | Close tab |
| `list_pages` | List open pages |
| `select_page` | Switch to page |
| `wait_for` | Wait for element/condition |

---

## Debugging (5 tools)

| Tool | Description |
|------|-------------|
| `take_screenshot` | Capture page |
| `take_snapshot` | Capture DOM |
| `evaluate_script` | Run JavaScript |
| `get_console_message` | Get console log |
| `list_console_messages` | Get all logs |

---

## Network (2 tools)

| Tool | Description |
|------|-------------|
| `list_network_requests` | List all requests |
| `get_network_request` | Get request details |

---

## Performance (3 tools)

| Tool | Description |
|------|-------------|
| `performance_start_trace` | Start performance tracing |
| `performance_stop_trace` | Stop tracing |
| `performance_analyze_insight` | Analyze results |

---

## Emulation (2 tools)

| Tool | Description |
|------|-------------|
| `emulate` | Emulate device (mobile, tablet) |
| `resize_page` | Resize viewport |

---

## Configuration

### Connect to Running Chrome

```bash
npx chrome-devtools-mcp@latest --browser-url http://localhost:9222
```

First launch Chrome with debugging:
```bash
google-chrome --remote-debugging-port=9222
```

### Headless Mode

```bash
npx chrome-devtools-mcp@latest --headless
```

### Custom Viewport

```bash
npx chrome-devtools-mcp@latest --viewport 1920x1080
```

### Chrome Canary

```bash
npx chrome-devtools-mcp@latest --channel canary
```

---

## Common Patterns

### Test Form Validation

```
1. navigate_page to localhost:3000
2. fill_form with invalid data
3. click submit
4. take_screenshot
5. list_console_messages for errors
```

### Extract Data

```
1. navigate_page to data page
2. wait_for table to load
3. evaluate_script to extract data
4. Return as JSON
```

### Performance Audit

```
1. performance_start_trace
2. navigate_page to target
3. Perform actions
4. performance_stop_trace
5. performance_analyze_insight
```
