---
name: lev-cms
description: Boot and operate JP's self-referential CMS. Connection-agnostic — works with notionctl, Notion MCP, raw API, or curl. The CMS describes its own schema, intents, workflows, and governance.
triggers: ["cms", "notion cms", "boot cms", "lev cms", "triage", "inbox", "content queue", "heartbeat", "bootup"]
---

# Lev CMS — Self-Referential Agent Operating System

The CMS describes its own schema, intents, workflows, and governance. This skill teaches you how to connect. Everything else is IN the CMS.

## 1-Liner Boot

```
RuntimeState DB: fdbf6902-5597-438d-8e6d-1452b51a5d57
Bootup page: 31f9b3e2-80ff-819a-b427-fd874996c93a
```

Read the `Value` property of the bootup page. It contains your operating instructions: identity, governance, boot sequence, database aliases, routing, and write pipeline.

## How to Connect

Use whatever Notion tool you have. The CMS doesn't care.

| Tool | Verify | Read DB | Read Page |
|------|--------|---------|-----------|
| notionctl | `notionctl doctor --json` | `notionctl db query <alias> --json` | `notionctl page get <id> --json` |
| MCP | `notion-fetch` any page | `notion-fetch {id: "collection://<uuid>"}` | `notion-fetch {id: "<id>"}` |
| API | `GET /v1/users/me` | `POST /v1/databases/<uuid>/query` | `GET /v1/pages/<id>` |

## After Boot

The bootup prompt tells you what to do. Key operations:

- **Triage inbox**: query `inbox` DB, filter `Processed=NO`
- **Route intents**: check IntentRegistry before executing
- **Write pipeline**: validate → confirm → write → log event to `event_log`
- **Entity lifecycle**: query `entities` DB for states and transitions
- **Content strategy**: query `content_queue` for hooks and themes

## Architecture (for developers, not operators)

The CMS has 3 layers — do not confuse them:

1. **Storage Adapter** (`CanonicalStorageAdapter`) — owns CRUD, emits LevEvents. Today: Notion via notionctl.
2. **CMS Control Plane** (`CmsControlPort`) — orchestrates workflows, approvals, scheduling OVER storage. Future: `plugins/cms-control-plane/`
3. **Publish Targets** (`PublishTargetPort`) — projection-only consumers. Today: `plugins/publisher/` (filesystem materializer).

Contracts in `core/domain/src/event-source.ts`. Specs in `docs/specs/spec-cms-control-plane.md` and `docs/specs/spec-storage-adapters.md`.

notionctl is a thin API envelope. It has zero CMS domain logic. CMS semantics live above the adapter.
