# OpenCode worker

Prefer the Lev OpenCode provider card. For direct unattended fallback, run
`opencode run` from the exact project root with the frozen prompt and the safest
permission mode that can finish the bounded task. Capture stdout, stderr, exit
status, and any explicit session identifier separately.

Let the project/provider configuration select the model unless the user gives
a current-run override. Preserve normal project configuration and resume the
same session when the installed CLI exposes a stable identifier.

CAAM identity management applies only when the installed CAAM reports OpenCode
as a supported, profile-addressable provider. Check live capability; do not
infer support from the presence of OpenCode auth files in `caam doctor`.
