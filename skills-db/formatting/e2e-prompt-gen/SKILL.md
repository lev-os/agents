---
name: e2e-prompt-gen
description: Generate prompts targeting multiple action surfaces (Telegram, OpenAI Canvas, MCP Apps, CLI, etc.)
version: 1.0.0
dependencies:
  - lev-ui-universal
  - lev-poly
storage:
  templates: ./templates/
  outputs: ./outputs/
---

# E2E Target Prompt Generator

Generate prompts that render across multiple action surfaces using abstract widget definitions.

## Overview

This skill bridges `lev-ui-universal` widget definitions to concrete action surface implementations:

```
UniversalWidget → ActionSurfaceAdapter → Platform-Specific Output
     │                    │
     │                    ├── TelegramAdapter → InlineKeyboard / Mini App
     │                    ├── OpenAIAdapter → Canvas iframe / GPT App
     │                    ├── McpAppsAdapter → SEP-1865 HTML
     │                    ├── CliAdapter → inquirer prompts
     │                    └── HttpAdapter → JSON API response
```

## Usage

```bash
# Generate prompt for specific surface
e2e-prompt-gen --surface telegram --widget status-dashboard

# Generate for all surfaces
e2e-prompt-gen --surface all --widget event-log

# From UniversalWidget JSON
cat widget.json | e2e-prompt-gen --surface openai
```

## Supported Action Surfaces

| Surface | Output Format | Constraints |
|---------|--------------|-------------|
| `telegram` | InlineKeyboardMarkup + WebApp URL | 100 buttons max, 64 bytes callback_data |
| `openai` | Canvas iframe HTML + `window.openai` API | Sandboxed, frame_domains allowlist |
| `mcp-apps` | SEP-1865 compliant HTML | JSON-RPC over postMessage |
| `discord` | Embed + Components | 5 action rows, 25 components max |
| `cli` | inquirer.js prompts | stdin/stdout |
| `http` | JSON response | RESTful |
| `grpc` | Protocol Buffer | lev.ui.v1 schema |

## Widget Mapping

### Card → Surfaces

```typescript
// UniversalWidget::Card
{
  type: "card",
  title: "System Status",
  variant: "elevated",
  glow: "emerald",
  children: [...]
}

// → Telegram: WebApp with embedded card HTML
// → OpenAI: iframe with cyberpunk CSS
// → CLI: boxen-style bordered output
// → HTTP: { card: {...}, rendered_html: "..." }
```

### StatusBadge → Surfaces

```typescript
// UniversalWidget::StatusBadge
{
  type: "status_badge",
  status: "active",
  label: "Online",
  pulse: true
}

// → Telegram: emoji prefix (🟢 Online)
// → OpenAI: <span class="status-badge active pulse">Online</span>
// → CLI: chalk.green("● Online")
// → HTTP: { status: "active", label: "Online", badge_html: "..." }
```

### ActionButton → Surfaces

```typescript
// UniversalWidget::ActionButton
{
  type: "action_button",
  label: "Approve",
  action: "task:approve:123",
  variant: "primary"
}

// → Telegram: InlineKeyboardButton { text: "Approve", callback_data: "task:approve:123" }
// → OpenAI: <button onclick="window.openai.toolCall('approve', {id:'123'})">Approve</button>
// → CLI: { type: 'select', choices: [{ name: 'Approve', value: 'task:approve:123' }] }
// → HTTP: { actions: [{ method: 'POST', href: '/task/123/approve', label: 'Approve' }] }
```

## Template System

Templates live in `./templates/` and use handlebars syntax:

```handlebars
{{! templates/telegram-mini-app.hbs }}
<!DOCTYPE html>
<html>
<head>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <style>{{{cyberpunk_css}}}</style>
</head>
<body>
  <div class="lev-container">
    {{#each widgets}}
      {{{render this}}}
    {{/each}}
  </div>
  <script>
    Telegram.WebApp.ready();
    Telegram.WebApp.MainButton.setText('{{main_button_text}}');
    Telegram.WebApp.MainButton.onClick(() => {
      Telegram.WebApp.sendData(JSON.stringify({{data}}));
    });
  </script>
</body>
</html>
```

## Integration with Lev Poly

This skill leverages existing lev poly infrastructure:

```
lev/core/polyglot-runners/
├── bridge/        # MCP Bridge (WebSocket + JSON-RPC)
├── cli/           # CLI transport
├── src/server/    # HTTP/SSE
├── proto/         # gRPC definitions
└── sdk/typescript # SDK client
```

### MCP Tool Registration

```typescript
// Register as MCP tool
server.registerTool({
  name: "render_ui",
  description: "Render UniversalWidget to action surface",
  inputSchema: {
    type: "object",
    properties: {
      widget: { $ref: "#/definitions/UniversalWidget" },
      surface: { enum: ["telegram", "openai", "mcp-apps", "cli", "http"] }
    }
  },
  handler: async ({ widget, surface }) => {
    const adapter = getAdapter(surface);
    return adapter.render(widget);
  }
});
```

## Platform Capabilities Detection

```typescript
interface PlatformCaps {
  has_mouse: boolean;
  has_touch: boolean;
  has_system_tray: boolean;
  has_notifications: boolean;
  has_color: boolean;
  max_colors: number;  // 2, 16, 256, 0=truecolor
  max_buttons?: number;
  max_callback_data?: number;
  supports_iframe?: boolean;
}

// Telegram
const telegramCaps: PlatformCaps = {
  has_mouse: false,
  has_touch: true,
  has_system_tray: false,
  has_notifications: true,
  has_color: true,
  max_colors: 0,
  max_buttons: 100,
  max_callback_data: 64,
  supports_iframe: true  // Mini Apps
};

// CLI
const cliCaps: PlatformCaps = {
  has_mouse: false,
  has_touch: false,
  has_system_tray: false,
  has_notifications: false,
  has_color: true,
  max_colors: 256
};
```

## Prompt Generation Examples

### Generate Status Dashboard Prompt

```bash
e2e-prompt-gen --surface telegram --widget status-dashboard
```

Output:
```json
{
  "method": "sendMessage",
  "chat_id": "{{chat_id}}",
  "text": "System Status",
  "reply_markup": {
    "inline_keyboard": [
      [{ "text": "View Dashboard", "web_app": { "url": "https://lev.app/mini/status" } }],
      [{ "text": "Refresh", "callback_data": "status:refresh" }]
    ]
  }
}
```

### Generate OpenAI Canvas Prompt

```bash
e2e-prompt-gen --surface openai --widget event-log
```

Output:
```html
<!DOCTYPE html>
<html>
<head>
  <style>/* cyberpunk.css */</style>
  <script>
    window.addEventListener('message', (e) => {
      if (e.data.type === 'events') {
        renderEventLog(e.data.events);
      }
    });
    window.openai?.onToolOutput((data) => {
      renderEventLog(data.events);
    });
  </script>
</head>
<body>
  <div class="event-log" id="log"></div>
</body>
</html>
```

## Files

```
e2e-prompt-gen/
├── SKILL.md              # This file
├── templates/
│   ├── telegram-mini-app.hbs
│   ├── telegram-inline.hbs
│   ├── openai-canvas.hbs
│   ├── mcp-apps.hbs
│   ├── cli-inquirer.hbs
│   └── http-response.hbs
├── adapters/
│   ├── telegram.ts
│   ├── openai.ts
│   ├── mcp-apps.ts
│   ├── cli.ts
│   └── http.ts
└── outputs/              # Generated prompts cached here
```

## References

- [OpenAI Apps SDK](https://developers.openai.com/apps-sdk/build/chatgpt-ui/)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- [MCP Apps Extension (SEP-1865)](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1865)
- [Google A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
- [lev-ui-universal](/Users/jean-patricksmith/lev/crates/lev-ui-universal/)
