# Wrangler Configuration Reference

All configuration options for `wrangler.jsonc` (recommended) or `wrangler.toml`.

---

## Minimal Config

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01"
}
```

---

## Core Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `name` | string | Yes | Worker name |
| `main` | string | Yes* | Entry point file (*optional for assets-only) |
| `compatibility_date` | string | Yes | Runtime version date |
| `compatibility_flags` | string[] | No | Feature flags |
| `account_id` | string | No | Cloudflare account ID |

---

## Routes & Deployment

```jsonc
{
  // Deploy to workers.dev subdomain
  "workers_dev": true,

  // Custom routes
  "routes": [
    { "pattern": "example.com/*", "zone_name": "example.com" },
    { "pattern": "api.example.com/v1/*", "zone_id": "abc123" }
  ],

  // Or simple patterns
  "routes": ["example.com/*", "*.example.com/*"]
}
```

---

## Bindings

### KV Namespaces

```jsonc
{
  "kv_namespaces": [
    {
      "binding": "CACHE",          // Variable name in code
      "id": "abc123...",           // Optional - auto-provisioned if missing
      "preview_id": "def456..."    // Optional - for wrangler dev
    }
  ]
}
```

### R2 Buckets

```jsonc
{
  "r2_buckets": [
    {
      "binding": "ASSETS",
      "bucket_name": "my-bucket",   // Optional - auto-provisioned
      "preview_bucket_name": "my-bucket-preview"
    }
  ]
}
```

### D1 Databases

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "abc123..."   // Optional - auto-provisioned
    }
  ]
}
```

### Durable Objects

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "COUNTER",
        "class_name": "Counter"
      }
    ]
  }
}
```

### Service Bindings

```jsonc
{
  "services": [
    {
      "binding": "AUTH",
      "service": "auth-worker"
    }
  ]
}
```

### Queues

```jsonc
{
  "queues": {
    "producers": [
      { "binding": "QUEUE", "queue": "my-queue" }
    ],
    "consumers": [
      { "queue": "my-queue", "max_batch_size": 10 }
    ]
  }
}
```

### AI

```jsonc
{
  "ai": {
    "binding": "AI"
  }
}
```

### Vectorize

```jsonc
{
  "vectorize": [
    {
      "binding": "VECTOR_INDEX",
      "index_name": "my-index"
    }
  ]
}
```

### Hyperdrive

```jsonc
{
  "hyperdrive": [
    {
      "binding": "POSTGRES",
      "id": "abc123..."
    }
  ]
}
```

---

## Environment Variables

```jsonc
{
  // Non-secret variables (committed to repo)
  "vars": {
    "ENVIRONMENT": "production",
    "API_URL": "https://api.example.com"
  }
}
```

**Secrets:** Use `wrangler secret put NAME` — never in config file.

---

## Build Configuration

```jsonc
{
  "build": {
    "command": "npm run build",    // Custom build command
    "cwd": "./app",                // Working directory
    "watch_paths": ["./src"]       // Paths to watch for changes
  },

  "no_bundle": false,              // Skip bundling
  "minify": true,                  // Minify output
  "node_compat": true,             // Enable Node.js compatibility

  // Module rules
  "rules": [
    { "type": "Text", "globs": ["**/*.sql"] }
  ]
}
```

---

## Static Assets

```jsonc
{
  "assets": {
    "directory": "./public",
    "binding": "ASSETS",           // Optional binding
    "include": ["**/*"],
    "exclude": ["**/*.map"]
  }
}
```

---

## Triggers (Cron)

```jsonc
{
  "triggers": {
    "crons": ["0 * * * *", "0 0 * * *"]  // Every hour, every day at midnight
  }
}
```

---

## Environments

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",

  "env": {
    "staging": {
      "vars": { "ENVIRONMENT": "staging" },
      "routes": [{ "pattern": "staging.example.com/*" }],
      "kv_namespaces": [{ "binding": "CACHE", "id": "staging-id" }]
    },
    "production": {
      "vars": { "ENVIRONMENT": "production" },
      "routes": [{ "pattern": "example.com/*" }],
      "kv_namespaces": [{ "binding": "CACHE", "id": "prod-id" }]
    }
  }
}
```

Deploy: `wrangler deploy --env staging`

---

## Development Options

```jsonc
{
  "dev": {
    "ip": "localhost",
    "port": 8787,
    "local_protocol": "http",
    "generate_types": true         // Auto-gen types on wrangler dev
  }
}
```

---

## Observability

```jsonc
{
  "tail_consumers": [
    { "service": "log-worker" }    // Forward logs to another Worker
  ]
}
```

---

## Advanced Options

```jsonc
{
  "keep_vars": true,               // Don't overwrite dashboard vars on deploy
  "send_metrics": false,           // Disable anonymous metrics

  // Limits
  "limits": {
    "cpu_ms": 50                   // CPU time limit
  },

  // Migrations (for Durable Objects)
  "migrations": [
    { "tag": "v1", "new_classes": ["Counter"] }
  ]
}
```

---

## Pages-Specific

```jsonc
{
  "pages_build_output_dir": "./dist",
  "pages_config_version": 1
}
```

---

## Full Example

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/cloudflare/workers-sdk/main/packages/wrangler/config-schema.json",

  "name": "my-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],

  "routes": [
    { "pattern": "api.example.com/*", "zone_name": "example.com" }
  ],

  "vars": {
    "ENVIRONMENT": "production"
  },

  "kv_namespaces": [{ "binding": "CACHE" }],
  "r2_buckets": [{ "binding": "ASSETS", "bucket_name": "assets" }],
  "d1_databases": [{ "binding": "DB" }],

  "ai": { "binding": "AI" },

  "triggers": {
    "crons": ["0 0 * * *"]
  },

  "dev": {
    "generate_types": true
  }
}
```
