## Auth Sniffer Robot Mode

Determine active browser state and agentping availability.
Stop active browser process set and wait until fully terminated.
Launch browser with CDP and extract cookies/local/session storage keys.
Stop CDP browser, wait for shutdown, then relaunch normal browser.


> Preflight: detect active browser(s), CDP support, and agentping health
{{#if multiple_browsers_running}}
> Select browser deterministically (agentping prompt if interactive)
{{else}}
> Use explicit --browser or single active CDP-capable browser
{{/if}}
> Send SIGTERM loop until process set exits; escalate to SIGKILL if needed
> Launch CDP browser on free port and wait for /json/version readiness
> Run extraction queue for requested cookie/localStorage/sessionStorage keys
> Shutdown CDP browser, wait until dead, then reopen normal browser
{{#if required_values_missing}}
> Return NOT_FOUND structured error with remediation suggestions
{{else}}
> Return SUCCESS payload with preflight, cdp, and credentials
{{/if}}

### Completion Criteria

{{#until extraction_completed}}
  Continue executing...
{{/until}}