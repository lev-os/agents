# Template Patterns

Leviathan uses Mustache-style templates for code generation. The template engine lives in `core/agent-adapter/src/sdk/template-engine.ts`.

## Quick Reference

| Pattern | Syntax | Description |
|---------|--------|-------------|
| Variable | `{{name}}` | Simple substitution |
| Nested | `{{user.name}}` | Dot notation access |
| Conditional | `{{#if cond}}...{{/if}}` | Truthy check |
| Equality | `{{#if status == "active"}}...{{/if}}` | Equality check |
| Inverse | `{{#unless cond}}...{{/unless}}` | Falsy check |
| Loop | `{{#each items}}{{this}}{{/each}}` | Array iteration |
| Index | `{{@index}}` | Current loop index |
| First/Last | `{{@first}}`/`{{@last}}` | Boolean flags |

## Variable Substitution

### Simple Variables

```handlebars
Hello, {{name}}!
```

Context: `{ name: "World" }` → `Hello, World!`

### Nested Properties

```handlebars
{{user.profile.displayName}}
```

Context: `{ user: { profile: { displayName: "Alice" } } }` → `Alice`

### Missing Variables

If a variable is not found, it's left as-is (useful for runtime variables):

```handlebars
{{undefined_var}}
```

→ `{{undefined_var}}` (preserved)

## Conditionals

### Boolean/Truthy Check

```handlebars
{{#if isActive}}
  Active user
{{/if}}
```

Truthy values:
- `true`
- Non-empty strings
- Non-zero numbers

Falsy values:
- `false`
- `''` (empty string)
- `0`
- `null`
- `undefined`

### Equality Check

```handlebars
{{#if status == "active"}}
  Status is active
{{/if}}
```

Supports both regular quotes and JSON-escaped quotes:
```handlebars
{{#if status == \"active\"}}
```

### Inverse Conditionals

```handlebars
{{#unless hasError}}
  Everything is fine
{{/unless}}
```

## Loops

### Basic Array Iteration

```handlebars
{{#each items}}
  - {{this}}
{{/each}}
```

Context: `{ items: ["a", "b", "c"] }`

Output:
```
  - a
  - b
  - c
```

### Loop Metadata

```handlebars
{{#each users}}
  {{@index}}. {{this.name}}{{#if @last}} (last){{/if}}
{{/each}}
```

Available metadata:
- `{{@index}}` - Zero-based index
- `{{@first}}` - Boolean, true for first item
- `{{@last}}` - Boolean, true for last item
- `{{this}}` - Current item

### Nested Object Access in Loops

```handlebars
{{#each users}}
  Name: {{this.name}}
  Email: {{this.email}}
{{/each}}
```

### Conditional Inside Loop

```handlebars
{{#each users}}
  {{this.name}}{{#if @first}} (admin){{/if}}
{{/each}}
```

## Processing Objects

The template engine can process entire objects (YAML/JSON configs):

```typescript
import { processTemplateObject } from '@lev-os/agent-adapter';

const config = {
  name: "{{project.name}}",
  version: "{{project.version}}",
  enabled: "{{#if production}}true{{/if}}"
};

const context = {
  project: { name: "my-app", version: "1.0.0" },
  production: true
};

const result = processTemplateObject(config, context);
// → { name: "my-app", version: "1.0.0", enabled: "true" }
```

## Template Usage in Lev

### Skill Templates

```yaml
# SKILL.md template
---
name: {{name}}
description: {{description}}
version: 1.0.0
---

# {{name | titleCase}}

{{#if overview}}
## Overview

{{overview}}
{{/if}}

## Capabilities

{{#each capabilities}}
- {{this}}
{{/each}}
```

### Command Handler Templates

```typescript
// Handler template
import type { CommandContext } from '@lev-os/poly-sdk';

export interface {{name | pascalCase}}Args {
{{#each args}}
  {{name}}{{#unless required}}?{{/unless}}: {{type}};
{{/each}}
}

export async function {{name}}(
  args: {{name | pascalCase}}Args,
  ctx: CommandContext
): Promise<void> {
  // TODO: Implement {{name}}
}
```

### Config.yaml Templates

```yaml
package:
  name: {{name}}
  version: 0.1.0
  type: core_package
  namespace: {{namespace}}
  description: '{{description}}'

poly:
  sdk:
{{#each commands}}
    {{name}}:
      handler: src/commands/{{name}}.ts
      description: '{{description}}'
{{/each}}
```

## TypeScript API

```typescript
import {
  TemplateEngine,
  createTemplateEngine,
  processTemplate,
  processTemplateObject
} from '@lev-os/agent-adapter';

// Create engine instance
const engine = createTemplateEngine();

// Process string template
const result = engine.process(template, context);

// Process object (for configs)
const config = engine.processObject(yamlConfig, context);

// Convenience functions
const output = processTemplate(template, context);
const configOutput = processTemplateObject(config, context);
```

## Empty Line Cleanup

The engine automatically cleans up excessive empty lines (3+ consecutive newlines → 2).

## Best Practices

1. **Keep templates readable** - Use whitespace for clarity
2. **Preserve structure** - Templates should look like the output
3. **Handle missing values** - Use conditionals for optional fields
4. **Test with edge cases** - Empty arrays, null values, etc.

## Limitations

- No helper functions (capitalize, etc.) built-in
- No partial templates
- No block helpers beyond if/unless/each
- No comments syntax

For complex transformations, pre-process context data before templating.

## Source Reference

Full implementation: `core/agent-adapter/src/sdk/template-engine.ts`
