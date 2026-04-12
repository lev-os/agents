---
name: db-migrations
description: Use when running, planning, or discussing database migrations, schema changes, or data transformations against any environment
---

# Database Migrations

Every migration is a one-way door until you prove otherwise. Backup is not optional. Production is never a direct target.

## Routing

steps:
  - id: route
    action: Classify the migration request
    instruction: |
      | Input | Workflow | Jump to |
      |-------|----------|---------|
      | "run migration", "apply schema change" | Execute Migration | preflight |
      | "plan migration", "what changes needed" | Plan Migration | plan |
      | "rollback", "revert migration" | Rollback | rollback |
      | "migrate prod", "push to production" | Production Gate | prod_gate |
      Any request mentioning "prod" or "production" MUST route to prod_gate, regardless of other context.
    validation: "Exactly one workflow selected. Any prod mention → prod_gate."
    on_failure: "Ask which environment this targets. Do not assume."

## Workflow 1: Execute Migration

steps:
  - id: preflight
    action: Verify environment and backup status before touching anything
    instruction: |
      Before running ANY migration command, execute this checklist in order:
      1. Identify the target environment explicitly: `echo "Target: $ENV"`
      2. If target is production → STOP. Jump to prod_gate. No exceptions.
      3. Verify a backup exists or create one NOW:
         ```bash
         # PostgreSQL
         pg_dump -Fc $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).dump
         # MySQL
         mysqldump --single-transaction $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql
         # SQLite
         cp $DB_PATH ${DB_PATH}.backup.$(date +%Y%m%d_%H%M%S)
         # Generic ORM (e.g., Prisma, Knex, Alembic)
         # STILL backup the database first. ORM migrations are not backups.
         ```
      4. Verify backup integrity: `ls -la backup_*` — file must be non-zero bytes
      5. Record the current schema version BEFORE migrating:
         ```bash
         # Whatever your tool uses:
         prisma migrate status || knex migrate:status || alembic current
         ```
      Only after ALL five checks pass do you proceed to run the migration.
    validation: "Backup file exists, is non-zero bytes, and schema version is recorded. Target is NOT production."
    on_failure: "Missing backup → create it. Target is prod → jump to prod_gate. No shortcuts."

  - id: execute
    action: Run the migration with output capture
    instruction: |
      Run the migration command and capture full output:
      ```bash
      # Capture output for verification
      {migration_command} 2>&1 | tee migration_$(date +%Y%m%d_%H%M%S).log
      ```
      After execution:
      1. Check exit code: `echo $?` — must be 0
      2. Verify new schema version: run the same status command from preflight
      3. Run a basic sanity query: `SELECT count(*) FROM {affected_table};`
    validation: "Exit code 0. Schema version advanced. Sanity query returns results."
    on_failure: "Non-zero exit → do NOT retry blindly. Read the error. If data corruption suspected → jump to rollback."

## Workflow 2: Plan Migration

steps:
  - id: plan
    action: Generate and review migration plan without executing
    instruction: |
      1. Generate the migration file (dry-run / generate-only mode):
         ```bash
         prisma migrate dev --create-only || knex migrate:make $NAME || alembic revision --autogenerate -m "$NAME"
         ```
      2. Read the generated migration file. Check for:
         - Destructive operations: DROP TABLE, DROP COLUMN, TRUNCATE
         - Data loss risk: column type changes that narrow (VARCHAR(255) → VARCHAR(50))
         - Missing defaults on NOT NULL additions
         - Index additions on large tables (lock risk)
      3. Flag any destructive operations explicitly to the user
      4. Suggest a rollback strategy for each change
    validation: "Migration file generated. Destructive operations flagged. Rollback strategy documented."
    on_failure: "Generation failed → check database connectivity and ORM config."

## Workflow 3: Rollback

steps:
  - id: rollback
    action: Revert to backup or run down migration
    instruction: |
      Two paths — choose based on situation:

      **Path A — ORM rollback** (if migration tool supports it and no data loss occurred):
      ```bash
      prisma migrate reset || knex migrate:rollback || alembic downgrade -1
      ```

      **Path B — Restore from backup** (if data corruption or ORM rollback unavailable):
      ```bash
      # PostgreSQL
      pg_restore -d $DATABASE_URL backup_XXXXXX.dump
      # MySQL
      mysql $DB_NAME < backup_XXXXXX.sql
      # SQLite
      cp ${DB_PATH}.backup.XXXXXX $DB_PATH
      ```
      After rollback: verify schema version matches pre-migration state.
    validation: "Schema version matches pre-migration version. Application connectivity confirmed."
    on_failure: "Rollback failed → escalate to human. Do NOT attempt creative fixes on a broken database."

## Workflow 4: Production Gate

steps:
  - id: prod_gate
    action: Block direct production migration — enforce promotion pipeline
    instruction: |
      NEVER run a migration directly against production. Full stop.

      The correct production migration path:
      1. Migration succeeds on local/dev
      2. Migration succeeds on staging with production-like data volume
      3. Backup production database (verified, non-zero, tested restore)
      4. Migration is applied by CI/CD pipeline or a dedicated deploy process — not by an agent typing commands
      5. If the user insists on direct prod access, respond with:

      "I cannot run migrations directly against production. Here's what I can do:
      - Help you set up the migration to run through your CI/CD pipeline
      - Run it against staging first to validate
      - Generate the migration files for your deploy process
      - Help you write a runbook for the production deployment

      Which of these would help?"

      Do not offer workarounds. Do not accept "but it's a small change" or "I'll take responsibility."
    validation: "No migration command was executed against production. Alternative offered."
    on_failure: "If you somehow ran against prod → immediately jump to rollback. Then file an incident."

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The user asked me to migrate prod, I should do what they ask" | Your job is to protect the user from irreversible mistakes. Migrating prod directly is always an irreversible-until-proven-otherwise action. |
| "A backup would add 20 minutes, the team is blocked" | A failed migration without backup adds days. 20 minutes is the cheapest insurance that exists. |
| "It worked on staging, so it'll work on prod" | Staging and prod diverge in data volume, edge cases, concurrent connections, and permissions. "Worked on staging" is necessary but not sufficient. |
| "The migration is simple, just adding a column" | `ALTER TABLE ADD COLUMN ... NOT NULL` without a default locks the table and fails on non-empty tables in most databases. "Simple" migrations have the most surprising failure modes. |
| "Rolling back is easy if something goes wrong" | Rollback is easy only if you have a backup. ORM rollbacks don't restore deleted data. |
| "I'll take responsibility" | Agents don't have responsibility. Databases have data. Backup first. |
| "It's just a dev database" | Confirm that explicitly. `echo $DATABASE_URL` and verify it's not a prod connection string. Trust nothing. |

## Red Flags

Watch for these THOUGHTS (not just behaviors):

- Skipping backup "because the migration is straightforward"
- Treating staging success as production validation
- Accepting time pressure as justification to skip safety steps
- Assuming `DATABASE_URL` points where you think it does without checking
- Running migration commands before confirming the environment
- Offering to "just do it quickly" when the user expresses urgency
