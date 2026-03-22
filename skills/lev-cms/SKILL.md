---
name: lev-cms
description: Boot and operate JP's self-referential CMS. 1-liner boot for any agent with Notion access. Connection-agnostic — works with notionctl, Notion MCP, raw API, or curl.
triggers: ["cms", "notion cms", "boot cms", "lev cms", "triage", "inbox", "content queue", "heartbeat", "bootup"]
---

# Lev CMS — Self-Referential Agent Operating System

You operate a self-referential CMS. The CMS describes its own schema, intents, workflows, and governance. Everything you need is IN the CMS — this skill just teaches you how to connect.

## 1-Liner Boot

```
RuntimeState DB: fdbf6902-5597-438d-8e6d-1452b51a5d57
Bootup key:     system.bootup_prompt (page title: "System Bootup Prompt")
```

Read the `Value` property of that page. It contains your full operating instructions: identity, governance, 23 database IDs, routing table, write pipeline, entity lifecycle, content strategy, and FlowMind DSL.

## Connection Surface (pick one)

The CMS doesn't care how you connect. Use whatever Notion tool you have:

### notionctl (recommended — on PATH)

```bash
# Verify connectivity
notionctl doctor --json

# Read bootup prompt
notionctl page get 31f9b3e2-80ff-819a-b427-fd874996c93a --json
# → .ok.data.page.properties.Value contains the full prompt

# Query a database (use DB alias or ID)
notionctl db query inbox --json
notionctl db query runtime_state --json
notionctl db query inbox --limit 50 --filter '{"property":"Processed","checkbox":{"equals":false}}' --json

# Get a specific page
notionctl page get <page_id> --json

# Create a page
notionctl page create --db <db_id> --props '{"Name":"value","Status":"Active"}' --json

# Update a page
notionctl page update <page_id> --props '{"Status":"Active","Processed":"YES"}' --json

# Search across workspace
notionctl search "query" --json
```

### Notion MCP (if available as tool)

```
notion-fetch {id: "collection://<db_id>"}           → read database schema + records
notion-fetch {id: "<page_id>"}                       → read page properties + content
notion-search {query: "...", data_source_url: "collection://<db_id>"}  → search
notion-create-pages {parent: {data_source_id: "<db_id>", type: "data_source_id"}, pages: [{properties: {...}}]}
notion-update-page {command: "update_properties", page_id: "<id>", properties: {...}}
```

### Raw Notion API (with NOTION_ACCESS_TOKEN)

```bash
# Read page
curl -s https://api.notion.com/v1/pages/<page_id> \
  -H "Authorization: Bearer $NOTION_ACCESS_TOKEN" \
  -H "Notion-Version: 2022-06-28"

# Query database
curl -s -X POST https://api.notion.com/v1/databases/<db_id>/query \
  -H "Authorization: Bearer $NOTION_ACCESS_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Processed", "checkbox": {"equals": false}}}'
```

## Property Format Reference

Notion properties have specific write formats:

| Type | Format | Example |
|------|--------|---------|
| Title | `"Name": "value"` | `"Name": "My Project"` |
| Select | `"Status": "Active"` | exact match required |
| Multi-select | `"Platform": "LinkedIn"` | ONE value only, never comma-separated |
| Date | `"date:Start Date:start": "2026-03-17"` + `"date:Start Date:is_datetime": 0` | |
| Number | `"Energy": 7` | JS number, not string |
| Checkbox | `"Processed": "YES"` or `"Processed": "NO"` | |
| Rich text | `"Notes": "content"` | |
| URL | `"Source URL": "https://..."` | |
| Relation | `"Project": "[\"https://www.notion.so/<page-id>\"]"` | |

## Database Quick Reference

The bootup prompt has all 23 IDs. Here are the ones you'll use most:

| Alias | DB ID | Title Prop |
|-------|-------|------------|
| inbox | d76d98e4-fd89-4e9e-820a-772608235806 | Title |
| tasks | 51027961-71bf-4b61-8ddd-056cbde7c662 | Task |
| content_queue | f96e4e69-0750-4bd2-8b93-9f45631cc5b4 | Hook |
| crm | f3507de2-7fed-4967-9b04-ef441bf61a11 | Name |
| kb | 81521f8d-b99d-4382-baef-21c5fd7d2414 | Title |
| projects | 1b09c85c-4418-4b69-9c44-6eefc7ae2c48 | Name |
| runtime_state | fdbf6902-5597-438d-8e6d-1452b51a5d57 | Name |
| entities | 2d69d21d-df48-4dd5-a7b9-3bf6094d4764 | Name |
| event_log | 1cb3877c-2820-451b-98e9-f1b652ded0b9 | EventType |

## Progressive Disclosure

Don't load everything at once. Boot with the prompt, then fetch on demand:

```bash
# 1. Boot (read the prompt — this is your operating manual)
notionctl page get 31f9b3e2-80ff-819a-b427-fd874996c93a --json

# 2. When you need to triage → query inbox
notionctl db query inbox --filter '{"property":"Processed","checkbox":{"equals":false}}' --json

# 3. When you need intent details → query IntentRegistry
notionctl db query intent_registry --json

# 4. When you need content types → query ContentTypes
notionctl db query content_types --json

# 5. When you need heartbeat/cron → read heartbeat protocol page
notionctl page get 31f9b3e2-80ff-81f1-9b37-c8b7be473a02 --json
```

## Governance (non-negotiable)

These rules are in the bootup prompt but worth repeating:

1. **CMS-authoritative** — schemas come from Notion. Never hardcode.
2. **Intent-first** — resolve intent from IntentRegistry before executing.
3. **No raw writes** — validate schema → confirm → write → log event.
4. **Fail-closed** — if validation fails, stop.
5. **No auto-posting** — LinkedIn/X/Substack require explicit human approval.
6. **Never delete** — only Archive or Deprecate.
7. **Multi-select: ONE value** — pass exactly one value as plain string.
8. **Engagement logging** — every social interaction → CRM.

## Write Pipeline

Every write follows: **Validate → Confirm → Write → Log Event**

After any write, log to Event Log (1cb3877c):
```json
{
  "EventType": "notion.write.completed",
  "Source": "<module>",
  "date:Time:start": "<ISO-8601>",
  "date:Time:is_datetime": 1,
  "CorrelationId": "<uuid>",
  "DataJSON": "<json>"
}
```

## notionctl DB Aliases

notionctl knows these aliases (use instead of raw UUIDs):

```bash
notionctl db query inbox --json
notionctl db query tasks --json
notionctl db query content_queue --json
notionctl db query crm --json
notionctl db query kb --json
notionctl db query projects --json
notionctl db query runtime_state --json
notionctl db query entities --json
notionctl db query artifacts --json
notionctl db query event_log --json
notionctl db query reflections --json
notionctl db query briefs --json
notionctl db query goals --json
notionctl db query fundraising --json
notionctl db query documents --json
notionctl db query content_types --json
notionctl db query field_definitions --json
notionctl db query intent_registry --json
notionctl db query flowmind_templates --json
notionctl db query skills --json
notionctl db query agent_config --json
notionctl db query memory --json
notionctl db query automation_rules --json
```
