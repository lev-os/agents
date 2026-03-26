# Wrangler Commands Reference

Complete command reference (v4.59.2, Jan 2026).

---

## Worker Management

| Command | Description |
|---------|-------------|
| `wrangler dev` | Start local dev server |
| `wrangler deploy` | Deploy to Cloudflare |
| `wrangler delete` | Delete deployed Worker |
| `wrangler build` | Build without deploying |
| `wrangler tail` | Tail live logs |
| `wrangler types` | Generate TypeScript types |
| `wrangler types --check` | Verify types up-to-date (CI) |

## Secrets

| Command | Description |
|---------|-------------|
| `wrangler secret put NAME` | Add/update secret |
| `wrangler secret delete NAME` | Delete secret |
| `wrangler secret list` | List all secrets |
| `wrangler secret bulk FILE` | Bulk upload from JSON file |

## Versions & Deployments

| Command | Description |
|---------|-------------|
| `wrangler deployments list` | List deployment history |
| `wrangler deployments status` | Current deployment status |
| `wrangler versions list` | List Worker versions |
| `wrangler versions deploy` | Deploy specific version |
| `wrangler rollback` | Rollback to previous |

---

## KV (Key-Value)

### Namespaces
| Command | Description |
|---------|-------------|
| `wrangler kv namespace create NAME` | Create namespace |
| `wrangler kv namespace list` | List namespaces |
| `wrangler kv namespace delete --namespace-id ID` | Delete namespace |

### Keys
| Command | Description |
|---------|-------------|
| `wrangler kv key put KEY VALUE --namespace-id ID` | Put key |
| `wrangler kv key get KEY --namespace-id ID` | Get key |
| `wrangler kv key delete KEY --namespace-id ID` | Delete key |
| `wrangler kv key list --namespace-id ID` | List keys |

### Bulk
| Command | Description |
|---------|-------------|
| `wrangler kv bulk put FILE --namespace-id ID` | Bulk put from JSON |
| `wrangler kv bulk delete FILE --namespace-id ID` | Bulk delete from JSON |

---

## R2 (Object Storage)

### Buckets
| Command | Description |
|---------|-------------|
| `wrangler r2 bucket create NAME` | Create bucket |
| `wrangler r2 bucket list` | List buckets |
| `wrangler r2 bucket delete NAME` | Delete bucket |
| `wrangler r2 bucket info NAME` | Bucket details |

### Objects
| Command | Description |
|---------|-------------|
| `wrangler r2 object put BUCKET/KEY --file FILE` | Upload object |
| `wrangler r2 object get BUCKET/KEY` | Download object |
| `wrangler r2 object delete BUCKET/KEY` | Delete object |

### Advanced
| Command | Description |
|---------|-------------|
| `wrangler r2 bucket cors set BUCKET --rules FILE` | Set CORS |
| `wrangler r2 bucket lifecycle set BUCKET --rules FILE` | Set lifecycle |
| `wrangler r2 bucket domain add BUCKET DOMAIN` | Add custom domain |
| `wrangler r2 sql query BUCKET -q "SQL"` | Query with SQL |

---

## D1 (Database)

| Command | Description |
|---------|-------------|
| `wrangler d1 create NAME` | Create database |
| `wrangler d1 list` | List databases |
| `wrangler d1 delete NAME` | Delete database |
| `wrangler d1 info NAME` | Database details |
| `wrangler d1 execute NAME --file FILE` | Execute SQL file |
| `wrangler d1 execute NAME --command "SQL"` | Execute SQL command |
| `wrangler d1 export NAME --output FILE` | Export database |

### Migrations
| Command | Description |
|---------|-------------|
| `wrangler d1 migrations create NAME MSG` | Create migration |
| `wrangler d1 migrations list NAME` | List migrations |
| `wrangler d1 migrations apply NAME` | Apply migrations |

### Time Travel
| Command | Description |
|---------|-------------|
| `wrangler d1 time-travel info NAME` | Available restore points |
| `wrangler d1 time-travel restore NAME --timestamp TS` | Restore to point |

---

## Queues

| Command | Description |
|---------|-------------|
| `wrangler queues create NAME` | Create queue |
| `wrangler queues list` | List queues |
| `wrangler queues delete NAME` | Delete queue |
| `wrangler queues info NAME` | Queue details |
| `wrangler queues pause-delivery NAME` | Pause delivery |
| `wrangler queues resume-delivery NAME` | Resume delivery |
| `wrangler queues purge NAME` | Purge all messages |

### Consumers
| Command | Description |
|---------|-------------|
| `wrangler queues consumer add QUEUE --script-name WORKER` | Add Worker consumer |
| `wrangler queues consumer remove QUEUE --script-name WORKER` | Remove consumer |

---

## Pages

| Command | Description |
|---------|-------------|
| `wrangler pages dev DIR` | Local Pages dev server |
| `wrangler pages deploy DIR` | Deploy Pages site |
| `wrangler pages project list` | List projects |
| `wrangler pages project create NAME` | Create project |
| `wrangler pages deployment list --project-name NAME` | List deployments |

### Functions
| Command | Description |
|---------|-------------|
| `wrangler pages functions build` | Build functions |
| `wrangler pages functions optimize-routes` | Optimize routing |

### Secrets
| Command | Description |
|---------|-------------|
| `wrangler pages secret put NAME --project-name PROJ` | Add secret |
| `wrangler pages secret list --project-name PROJ` | List secrets |

---

## Workflows

| Command | Description |
|---------|-------------|
| `wrangler workflows list` | List workflows |
| `wrangler workflows describe NAME` | Workflow details |
| `wrangler workflows trigger NAME` | Trigger workflow |
| `wrangler workflows delete NAME` | Delete workflow |

### Instances
| Command | Description |
|---------|-------------|
| `wrangler workflows instances list NAME` | List instances |
| `wrangler workflows instances describe NAME ID` | Instance details |
| `wrangler workflows instances pause NAME ID` | Pause instance |
| `wrangler workflows instances resume NAME ID` | Resume instance |
| `wrangler workflows instances terminate NAME ID` | Terminate instance |

---

## Vectorize

| Command | Description |
|---------|-------------|
| `wrangler vectorize create NAME --dimensions N --metric TYPE` | Create index |
| `wrangler vectorize list` | List indexes |
| `wrangler vectorize delete NAME` | Delete index |
| `wrangler vectorize insert NAME --file FILE` | Insert vectors |
| `wrangler vectorize query NAME --vector "[...]"` | Query vectors |

---

## Hyperdrive

| Command | Description |
|---------|-------------|
| `wrangler hyperdrive create NAME --connection-string "..."` | Create config |
| `wrangler hyperdrive list` | List configs |
| `wrangler hyperdrive get NAME` | Get config |
| `wrangler hyperdrive delete NAME` | Delete config |
| `wrangler hyperdrive update NAME --origin-host HOST` | Update config |

---

## AI

| Command | Description |
|---------|-------------|
| `wrangler ai models` | List available models |
| `wrangler ai finetune create --model MODEL --data FILE` | Create fine-tune |
| `wrangler ai finetune list` | List fine-tunes |

---

## Account & Auth

| Command | Description |
|---------|-------------|
| `wrangler login` | OAuth login |
| `wrangler logout` | Logout |
| `wrangler whoami` | Show current user |
| `wrangler auth token` | Get auth token (for scripts) |

---

## Utilities

| Command | Description |
|---------|-------------|
| `wrangler check startup` | Validate config |
| `wrangler docs` | Open docs in browser |
| `wrangler telemetry disable` | Disable telemetry |
| `wrangler telemetry status` | Check telemetry status |

---

## Common Flags

| Flag | Description |
|------|-------------|
| `--config FILE` | Use specific config file |
| `--env NAME` | Use specific environment |
| `--compatibility-date DATE` | Override compatibility date |
| `--var KEY:VALUE` | Set variable |
| `--json` | Output as JSON |
