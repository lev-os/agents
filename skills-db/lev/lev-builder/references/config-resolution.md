# Config Resolution

Leviathan uses a two-level KISS configuration cascade (ADR-060).

## The Pattern

```
Level 1: ~/.config/lev/config.yaml   (global defaults)
         ↓ deep merge
Level 2: .lev/config.yaml            (project overrides)
         ↓
         Final merged config
```

**Rule**: Project wins over global. Simple.

## XDG Compliance

Lev follows the XDG Base Directory specification:

| Purpose | Variable | Default | Lev Path |
|---------|----------|---------|----------|
| Config | XDG_CONFIG_HOME | ~/.config | ~/.config/lev/ |
| Data | XDG_DATA_HOME | ~/.local/share | ~/.local/share/lev/ |
| State | XDG_STATE_HOME | ~/.local/state | ~/.local/state/lev/ |
| Cache | XDG_CACHE_HOME | ~/.cache | ~/.cache/lev/ |
| Project | - | .lev/ | .lev/ |

## Directory Structure

### Global (~/.config/lev/)

```
~/.config/lev/
├── config.yaml        # Global settings
├── policy.yaml        # Promotion rules
├── projects.yaml      # Registered projects
└── events.jsonl       # CloudEvents stream
```

### User Data (~/.local/share/lev/)

```
~/.local/share/lev/
├── skills/            # Promoted skills
├── plans/             # Crystallized plans
├── handoffs/          # Session handoffs
├── synths/            # Approved synths
├── auth/              # Cached credentials
└── sessions/          # Session data
```

### Runtime State (~/.local/state/lev/)

```
~/.local/state/lev/
├── logs/              # Daemon logs
├── cdo/               # CDO execution traces
├── ralph/             # Ralph loop traces
├── history.txt        # Command history
└── telemetry/         # Usage data
```

### Cache (~/.cache/lev/)

```
~/.cache/lev/
├── embeddings/        # Cached vectors
├── indexes/           # Search indexes
└── downloads/         # Temp downloads
```

### Project (.lev/)

```
.lev/
├── config.yaml        # Project overrides
├── policy.yaml        # Project promotion rules
├── events.jsonl       # Project events
├── pm/
│   ├── handoffs/      # Project handoffs
│   └── plans/         # Project plans
├── cdo/               # Project CDO runs
├── indexes/           # Project indexes
└── workshop.yaml      # Optional standalone
```

## Config Loading

### Section-Based Loading

Consumers request specific sections:

```typescript
import { loadConfigSection } from '@lev-os/config';

// Load memory config section
const memoryConfig = await loadConfigSection('memory');

// Load with defaults
const workshopConfig = await loadConfigSection('workshop', {
  defaults: { autoIndex: true }
});
```

### Deep Merge Strategy

```yaml
# ~/.config/lev/config.yaml (global)
memory:
  backend: sqlite
  ttl: 3600
  features:
    - semantic
    - episodic

# .lev/config.yaml (project)
memory:
  ttl: 7200
  features:
    - semantic
    - procedural
```

Result (deep merge):

```yaml
memory:
  backend: sqlite      # From global
  ttl: 7200           # Project override
  features:           # Project override (array replaced, not merged)
    - semantic
    - procedural
```

**Note**: Arrays are replaced, not merged. Objects are deep merged.

## Implementation

### Loading Config

```typescript
// core/config/src/loader.ts
export async function loadConfigSection(
  sectionName: string,
  options: { defaults?: Record<string, unknown> } = {}
): Promise<Record<string, unknown>> {
  const global = await loadGlobalConfig();    // ~/.config/lev/config.yaml
  const project = await loadProjectConfig();  // .lev/config.yaml

  const merged = deepMerge(
    options.defaults ?? {},
    global[sectionName] ?? {},
    project[sectionName] ?? {}
  );

  return merged;
}
```

### Deep Merge Utility

```typescript
// core/config/src/merger.ts
export function deepMerge(...objects: Record<string, unknown>[]): Record<string, unknown> {
  return objects.reduce((acc, obj) => {
    for (const key of Object.keys(obj)) {
      if (isPlainObject(acc[key]) && isPlainObject(obj[key])) {
        acc[key] = deepMerge(acc[key], obj[key]);
      } else {
        acc[key] = obj[key];
      }
    }
    return acc;
  }, {});
}
```

### Path Helpers

```typescript
import { getLevConfigHome, getLevDataHome, getLevStateHome } from '@lev-os/config';

const configDir = getLevConfigHome();  // ~/.config/lev or $XDG_CONFIG_HOME/lev
const dataDir = getLevDataHome();      // ~/.local/share/lev
const stateDir = getLevStateHome();    // ~/.local/state/lev
```

## Config for New Entities

### Skills

Skills don't use config.yaml directly. They use frontmatter in SKILL.md.

### Commands

Commands inherit config from their package:

```yaml
# core/memory/config.yaml
package:
  name: memory
  # ...

config:              # Package-level defaults
  backend: sqlite
  ttl: 3600

poly:
  sdk:
    remember:
      handler: src/commands/remember.ts
```

### Packages

Packages declare their config schema in config.yaml:

```yaml
# core/memory/config.yaml
package:
  name: memory
  # ...

config:
  backend:
    type: string
    default: sqlite
    enum: [sqlite, postgres, memory]
  ttl:
    type: number
    default: 3600
```

## Standalone Config Files

For large configs, use standalone files:

```
.lev/
├── config.yaml        # Main config
├── workshop.yaml      # Standalone workshop config
└── memory.yaml        # Standalone memory config
```

Load explicitly:

```typescript
const workshop = await loadStandaloneConfig('.lev/workshop.yaml');
```

## Variable Interpolation

For manifest-level variables (not config loading), use:

```typescript
import { resolveVariables } from '@lev-os/polyglot-runners';

const manifest = {
  name: '${lev.project.name}',
  version: '${env.VERSION}'
};

const resolved = resolveVariables(manifest);
```

**Note**: Variable interpolation is a separate concern from config loading. Config loading is pure YAML merge.

## Anti-Patterns

### DON'T: Environment Variable Overrides

```yaml
# Bad: Magic env var handling
memory:
  backend: ${MEMORY_BACKEND:-sqlite}  # Don't do this
```

### DON'T: Auto-Detection

```yaml
# Bad: Implicit behavior
memory:
  autodetect: true  # Don't do this
```

### DON'T: Multiple Override Levels

```yaml
# Bad: Too many levels
# env → local → project → user → global → default
```

### DO: Explicit Two Levels

```
~/.config/lev/config.yaml → .lev/config.yaml → Final
```

## Source Reference

- ADR: `docs/adr/060-config-cascade-pattern.md`
- Implementation: `core/config/src/loader.ts`
- Path helpers: `core/polyglot-runners/src/commands/install.ts`
