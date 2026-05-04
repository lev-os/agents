# Agent Adapter

Platform-specific adapters enable Leviathan to work across different AI coding assistants.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     Agent Adapter Layer                       │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │ Claude  │ │ Cursor  │ │  Aider  │ │ Windsurf│ │ Codex  │ │
│  │  Code   │ │         │ │         │ │         │ │        │ │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘ │
│       │           │           │           │          │       │
│       └───────────┴─────┬─────┴───────────┴──────────┘       │
│                         │                                     │
│                   ┌─────▼─────┐                               │
│                   │   Base    │                               │
│                   │  Adapter  │                               │
│                   └─────┬─────┘                               │
│                         │                                     │
│                   ┌─────▼─────┐                               │
│                   │  Template │                               │
│                   │  Engine   │                               │
│                   └───────────┘                               │
└──────────────────────────────────────────────────────────────┘
```

## Supported Platforms

| Platform | Status | Location |
|----------|--------|----------|
| claude-code | Stable | `src/adapters/claude-code.ts` |
| cursor | Stable | `src/adapters/cursor.ts` |
| aider | Stable | `src/adapters/aider.ts` |
| windsurf | Stable | `src/adapters/windsurf.ts` |
| codex | Stable | `src/adapters/codex.ts` |
| cline | Stable | `src/adapters/cline.ts` |
| continue | Beta | `src/adapters/continue.ts` |
| roo | Beta | `src/adapters/roo.ts` |
| opencode | Beta | `src/adapters/opencode.ts` |

## Base Adapter Interface

All adapters extend `BaseAdapter`:

```typescript
// core/agent-adapter/src/sdk/base-adapter.ts

export interface AdapterConfig {
  name: string;
  version: string;
  conversationDir: string;
  configPath?: string;
  templateOverrides?: Record<string, string>;
}

export abstract class BaseAdapter {
  protected config: AdapterConfig;
  protected templateEngine: TemplateEngine;

  constructor(config: AdapterConfig) {
    this.config = config;
    this.templateEngine = createTemplateEngine();
  }

  // Required: Parse conversations from platform storage
  abstract parseConversations(): Promise<Conversation[]>;

  // Required: Detect if platform is installed
  abstract detect(): Promise<boolean>;

  // Optional: Platform-specific skill emission
  emitSkill?(skill: SkillDefinition): Promise<string>;

  // Optional: Platform-specific config
  getConfig?(): Promise<PlatformConfig>;
}
```

## Creating a New Adapter

### 1. Create Adapter File

```typescript
// core/agent-adapter/src/adapters/my-platform.ts
import { BaseAdapter, AdapterConfig, Conversation } from '../sdk/base-adapter.js';
import { existsSync, readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

export class MyPlatformAdapter extends BaseAdapter {
  private readonly conversationPath: string;

  constructor() {
    super({
      name: 'my-platform',
      version: '1.0.0',
      conversationDir: join(homedir(), '.my-platform', 'conversations'),
    });
    this.conversationPath = this.config.conversationDir;
  }

  async detect(): Promise<boolean> {
    return existsSync(this.conversationPath);
  }

  async parseConversations(): Promise<Conversation[]> {
    if (!await this.detect()) {
      return [];
    }

    // Platform-specific parsing logic
    const conversations: Conversation[] = [];

    // Read conversation files
    // Parse into standard Conversation format
    // Return normalized data

    return conversations;
  }

  // Optional: Custom skill emission for this platform
  async emitSkill(skill: SkillDefinition): Promise<string> {
    const template = this.getSkillTemplate();
    return this.templateEngine.process(template, skill);
  }

  private getSkillTemplate(): string {
    // Platform-specific skill format
    return `
# {{name}}

{{description}}

## Instructions

{{instructions}}
`;
  }
}
```

### 2. Register in Index

```typescript
// core/agent-adapter/src/adapters/index.ts
export * from './claude-code.js';
export * from './cursor.js';
export * from './my-platform.js';  // Add new adapter
```

### 3. Add to Platform Registry

```typescript
// core/agent-adapter/src/registry.ts
import { MyPlatformAdapter } from './adapters/my-platform.js';

export const platformRegistry: Record<string, () => BaseAdapter> = {
  'claude-code': () => new ClaudeCodeAdapter(),
  'cursor': () => new CursorAdapter(),
  'my-platform': () => new MyPlatformAdapter(),  // Register
};
```

### 4. Update config.yaml

```yaml
# core/agent-adapter/config.yaml
poly:
  sdk:
    sync:
      args:
        - name: platform
          type: string
          enum:
            - claude-code
            - cursor
            - my-platform    # Add new platform
```

## Conversation Format

Standard conversation structure:

```typescript
interface Conversation {
  id: string;
  platform: string;
  startedAt: Date;
  lastMessageAt: Date;
  messages: Message[];
  metadata: Record<string, unknown>;
}

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];
}

interface ToolCall {
  name: string;
  input: Record<string, unknown>;
  output?: string;
}
```

## Skill Emission

Adapters can emit skills in platform-specific formats:

### Claude Code Format

```markdown
---
name: skill-name
description: When to use
---

# Skill Name

Instructions...
```

### Cursor Rules Format

```markdown
# Cursor Rules

## skill-name

Instructions...
```

### Aider Format

```yaml
# .aider.conf.yml
model-instructions:
  skill-name: |
    Instructions...
```

## Template Engine Usage

Adapters use the shared template engine:

```typescript
const template = `
{{#if isSkill}}
# {{name}}

{{description}}
{{/if}}

{{#each commands}}
## {{this.name}}

{{this.description}}
{{/each}}
`;

const output = this.templateEngine.process(template, {
  isSkill: true,
  name: 'my-skill',
  description: 'Does X',
  commands: [
    { name: 'cmd1', description: 'First command' },
    { name: 'cmd2', description: 'Second command' }
  ]
});
```

## Testing Adapters

```typescript
// core/agent-adapter/src/adapters/my-platform.test.ts
import { describe, it, expect, vi } from 'vitest';
import { MyPlatformAdapter } from './my-platform.js';

describe('MyPlatformAdapter', () => {
  it('should detect when platform is installed', async () => {
    const adapter = new MyPlatformAdapter();
    // Mock filesystem
    const detected = await adapter.detect();
    expect(detected).toBe(true);
  });

  it('should parse conversations', async () => {
    const adapter = new MyPlatformAdapter();
    const conversations = await adapter.parseConversations();
    expect(conversations).toHaveLength(expectedCount);
  });
});
```

## Platform Detection

Auto-detect installed platforms:

```typescript
import { detectPlatforms } from '@lev-os/agent-adapter';

const installed = await detectPlatforms();
// → ['claude-code', 'cursor']
```

## Sync Command

The `lev sync` command uses adapters:

```bash
# Sync all platforms
lev sync

# Sync specific platform
lev sync --platform cursor

# Full resync
lev sync --full

# Watch mode
lev sync --watch
```

## Adding Platform-Specific Features

### Custom Config Loading

```typescript
async getConfig(): Promise<PlatformConfig> {
  const configPath = join(homedir(), '.my-platform', 'config.json');
  if (existsSync(configPath)) {
    return JSON.parse(readFileSync(configPath, 'utf-8'));
  }
  return {};
}
```

### Custom Export Formats

```typescript
async exportTo(format: 'markdown' | 'json' | 'yaml'): Promise<string> {
  const conversations = await this.parseConversations();
  switch (format) {
    case 'markdown': return this.toMarkdown(conversations);
    case 'json': return JSON.stringify(conversations, null, 2);
    case 'yaml': return yaml.stringify(conversations);
  }
}
```

## Source Reference

- Base adapter: `core/agent-adapter/src/sdk/base-adapter.ts`
- Template engine: `core/agent-adapter/src/sdk/template-engine.ts`
- Example adapters: `core/agent-adapter/src/adapters/`
- Tests: `core/agent-adapter/src/adapters/*.test.ts`
