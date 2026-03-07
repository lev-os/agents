# Event Analysis

Detailed guide for analyzing ~/lev/.lev/events.jsonl

## Event Schema

```jsonl
{"ts":"2026-01-17T00:00:00Z","event":"skill.loaded","data":{"skill":"lev","duration":120}}
{"ts":"2026-01-17T00:00:01Z","event":"task.completed","data":{"id":"abc","success":true}}
{"ts":"2026-01-17T00:00:02Z","event":"error","data":{"type":"timeout","context":"..."}}
```

## Pattern Detection

### Frequency Patterns
- Events occurring >3x in 24h → potential workflow candidate
- Errors recurring → fix needed

### Sequence Patterns
- A always followed by B → dependency
- A never followed by B → potential bug

### Performance Patterns
- Duration >2s → optimization target
- Memory >100MB → leak investigation

## CLI Usage

```bash
lev learn analyze                    # All patterns
lev learn analyze --since 24h        # Time filter
lev learn analyze --type error       # Event type filter
lev learn analyze --output patterns  # Save to patterns.jsonl
```

## Integration with jq

```bash
# Count events by type
jq -s 'group_by(.event) | map({event: .[0].event, count: length})' events.jsonl

# Find slowest operations
jq -s 'sort_by(.data.duration) | reverse | .[0:10]' events.jsonl
```
