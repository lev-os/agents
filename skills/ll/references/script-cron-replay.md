# Script-only cron replay pattern

Use this when a user asks to rerun an existing scheduled/no-agent job by name and expects the result now.

## Pattern

1. List cron jobs and match the exact job name; never guess the job id.
2. Trigger the job with the scheduler (`cronjob run <job_id>`) first so the scheduler state remains the source of truth.
3. Verify the trigger by listing jobs again and checking `last_run_at`, `last_status`, and `next_run_at`.
4. If the job is `no_agent: true` with a `script` and the scheduler trigger does not visibly execute in time for the user's immediate request, run the same script directly in the job's `workdir` to get grounded output now.
5. Preserve script-only semantics in the report: empty stdout means healthy/silent; non-empty stdout is the alert/body; non-zero exit is a failure.
6. Report the concrete result, not just that the job was queued.

## Notes

- This is especially useful for daily hygiene/autosync/watchdog jobs whose scheduled run may be asynchronous or silent.
- Direct script replay should use the script path shown in the job metadata or its wrapper, with the same working directory. Do not invent a different command.
- Do not save missing credentials or transient setup failures as durable rules. If the replay reports missing env vars, report them as the current blocker only.