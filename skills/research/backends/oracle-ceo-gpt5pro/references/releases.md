# Releases

Version history for this repository (30 releases).

## v0.8.5: 0.8.5
**Published:** 2026-01-19

### Added
- Bridge: add the bridge workflow + MCP browser controls for remote ChatGPT sessions. Original PR #42 by Kyle McCleary (@kmccleary3301) — thank you!
- CLI: add `--background`/`--no-background`, `--http-timeout`, `--zombie-timeout`, and `--zombie-last-activity` to support long-running API sessions.

### Fixed
- CLI: restore legacy `--[no-]notify`, `--[no-]notify-sound`, and `--[no-]background` flags as hidden aliases (Commander no longer accepts `[no-]` in `new Option()`).
- Sessions: zombie detection now respects explicit timeouts and can optionally use last log activity to avoid false “zombie” status on long runs.
- Browser: fall back to the default DevTools target if an isolated tab fails, and keep the run tab open when `--keep-browser` is set.
- Browser: refresh long assistant responses without clobbering captured Markdown.

### Changed
- Config: remove legacy `remote.host`/`remote.token` and top-level `remoteHost`/`remoteToken`; use `browser.remoteHost`/`browser.remoteToken` or env vars.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.8.5)

---

## v0.8.4: 0.8.4
**Published:** 2026-01-05


### Changed
- Deps: update zod to `4.3.5`.
- Deps: add `qs` as a direct dependency (avoids Dependabot pnpm transitive-update failures).

### Fixed
- Browser: fix attachment uploads in the current ChatGPT composer (avoid duplicate uploads; avoid image-only inputs for non-image files). Original PR #60 by Alex Naidis (@TheCrazyLex) — thank you!


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.8.4)

---

## v0.8.3: 0.8.3
**Published:** 2025-12-31

### Added
- Config: allow `browser.forceEnglishLocale` to opt into `--lang/--accept-lang` for browser runs.
- Browser: add `--browser-cookie-wait` / `browser.cookieSyncWaitMs` to wait once and retry cookie sync. Original PR #55 by bheemreddy-samsara — thank you!

### Fixed
- Browser: avoid stray attachment removal clicks while still detecting stale chips, and allow completed uploads even if send stays disabled. Original PR #56 by Alex Naidis (@TheCrazyLex) — thank you!
- Browser: dismiss blocking modals when a custom ChatGPT project URL is missing, and harden attachment uploads (force input/change events; retry via DataTransfer; treat “file selected” as insufficient unless the composer shows attachment UI).
- Browser: prefer a trusted (CDP) click on the composer “+” button so attachment uploads work even when ChatGPT ignores synthetic clicks.



[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.8.3)

---

## v0.8.1: 0.8.1
**Published:** 2025-12-30

### Added
- Config: allow `browser.thinkingTime`, `browser.manualLogin`, and `browser.manualLoginProfileDir` defaults in `~/.oracle/config.json`.

### Fixed
- Browser: thinking-time chip selection now recognizes "Pro" labeled composer pills. Original PR #54 by Alex Naidis (@TheCrazyLex) — thank you!
- CLI: disable OSC progress output when running under Codex (`CODEX_MANAGED_BY_NPM=1`) to avoid spinner noise.

### Tests
- Stabilize OSC progress detection tests when `CODEX_MANAGED_BY_NPM=1` is set.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.8.1)

---

## v0.8.0: 0.8.0
**Published:** 2025-12-28

### Highlights
- Browser reliability push: stronger reattach, response capture, and attachment uploads (fewer prompt-echoes, truncations, and duplicate uploads).
- Cookie stack revamp via Sweet Cookie (no native addons) with better inline-cookie handling; Gemini web now works on Windows and honors `--browser-cookie-path`.
- New `--browser-model-strategy` flag to control ChatGPT model selection (`select`/`current`/`ignore`) in browser mode. Original PR #49 by @djangonavarro220 — thank you!

### Improvements
- Browser reattach now preserves `/c/` conversation URLs and project URL prefixes, validates conversation ids, and recovers from mid-run disconnects or capture failures.
- Response capture is more stable: wider selectors, assistant-only copy-turn capture, prompt-echo avoidance, and stop-button/clipboard stability checks.
- Attachment uploads are idempotent and count-aware (composer + chips + file inputs), with explicit completion waits and stale-input cleanup.
- Login flow adds richer diagnostics, auto-accepts the “Welcome back” picker, and always logs the active ChatGPT URL.
- Cookie handling prefers live Chrome over legacy `~/.oracle/cookies.json`; Gemini web can use inline cookies when sync is disabled.

### Fixes
- CLI: stream Markdown via Markdansi’s block renderer and guard the live renderer for non‑TTY edge cases.
- Tests: stabilize browser live tests (serialization + project URL fallback) and add response-observer assertions; browser smoke runs are faster.



[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.8.0)

---

## v0.7.6: 0.7.6
**Published:** 2025-12-25

### Changed
- CLI: compact finish line summary across API, browser, and session views.
- CLI: token counts now render as `↑in ↓out ↻reasoning Δtotal`.

### Fixed
- CLI/Browser: ignore duplicate `--file` inputs (log once) and improve attachment presence detection so re-runs don’t spam “already attached” upload errors.
- Browser: harden session reattach (better conversation targeting, longer prompt-commit wait, avoid closing shared DevTools targets).
- Live tests: add coverage + retries for browser reattach/model selection; tolerate transient OpenRouter free-tier failures.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.6)

---

## v0.7.5: 0.7.5
**Published:** 2025-12-23

### Fixed
- Packaging: switch tokentally to npm release so Homebrew installs don't trigger git prepare builds.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.5)

---

## v0.7.4: 0.7.4
**Published:** 2025-12-23


### Changed
- Browser: add `--browser-thinking-time <light|standard|extended|heavy>` to select thinking-time intensity in ChatGPT.

### Fixed
- Browser: throttle attachment upload pokes and pace multi-file uploads to avoid duplicate “already attached” warnings.
- Browser: correct GPT-5.2 variant selection (Auto/Thinking/Instant/Pro) with stricter matching and improved testid scoring; thinking-time selection now supports multiple levels. Original PR #45 by Manish Malhotra (@manmal) — thank you!
- Browser: only reload stalled conversations after an assistant-response failure (and only once), instead of always refreshing after submit.



[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.4)

---

## v0.7.3: 0.7.3
**Published:** 2025-12-23

- Changed: API: streaming answers in a rich TTY now use Markdansi’s live renderer (`createLiveRenderer`) so we can stream *and* render Markdown in-place.
- Changed: Dependencies: update `markdansi` to 0.1.5.
- Changed: Dependencies: update `devtools-protocol` to 0.0.1561482.
- Fixed: Browser: prevent `chrome-launcher` from auto-killing Chrome on SIGINT so reattach sessions survive Ctrl+C.
- Fixed: Sessions: running browser sessions now mark as errored when the Chrome PID/port are no longer reachable.
- Fixed: Browser: reattach now recovers even if Chrome was closed by reopening, locating the conversation in the sidebar, and resuming the response.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.3)

---

## v0.7.2: 0.7.2
**Published:** 2025-12-17

### Fixed
- Browser: stop auto-clicking the “Answer now” gate; wait for the full Pro-thinking response instead of skipping it.
- Browser: reject `?temporary-chat=true` URLs when targeting Pro models (Pro picker entries are not available in Temporary Chat); error message now calls this out explicitly.
- Browser: attachment uploads re-trigger the file-input change event until ChatGPT renders the attachment card (avoids hydration races); verify attachments are present on the sent user message before waiting for the assistant.
- Live tests: make the `gpt-5.2-instant` OpenAI smoke test resilient to transient API stalls/errors.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.2)

---

## v0.7.1: 0.7.1
**Published:** 2025-12-17

### Changed
- API: default model is now `gpt-5.2-pro` (and “Pro” label inference prefers GPT‑5.2 Pro).
- Tests: updated fixtures/defaults to use `gpt-5.2-pro` instead of `gpt-5.1-pro`.
- API: clarify `gpt-5.1-pro` as a stable alias that targets `gpt-5.2-pro`.
- Dependencies: refresh (notably `zod` 4.2.1 and `devtools-protocol` 0.0.1559729).
- Browser: browser engine GPT selection now supports ChatGPT 5.2 (`gpt-5.2`) and ChatGPT 5.2 Pro (`gpt-5.2-pro`); legacy labels like `gpt-5.1` normalize to 5.2, and “Pro” always resolves to 5.2 Pro (ignores Legacy GPT‑5.1 Pro submenu) with a top-bar label confirmation.

### Fixed
- Browser: prompt commit verification handles markdown code fences better; prompt-echo recovery is more robust (including remote browser mode); multi-file uploads are less flaky (dynamic timeouts + better filename matching). Original PR #41 by Muly Oved (@mulyoved) — thank you!
- Browser: adapt to ChatGPT DOM changes (`data-turn=assistant|user`) and “Answer now” gating in Pro thinking so we don’t capture placeholders/truncate answers.
- Gemini web: add abortable timeouts + retries for cookie-based runs so live tests are less likely to hang on transient Gemini web responses.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.1)

---

## v0.7.0: 0.7.0
**Published:** 2025-12-14


### Added
- Browser: Gemini browser mode via direct Gemini web client (uses Chrome cookies; no API key required; runs fully in Node/TypeScript — no Python/venv). Includes `--youtube`, `--generate-image`, `--edit-image`, `--output`, `--aspect`, and `--gemini-show-thoughts`. Original PR #39 by Nico Bailon (@nicobailon) — thank you!
- Browser: media files passed via `--file` (images/video/audio/PDF) are treated as upload attachments instead of being inlined into the prompt (enables Gemini file analysis).
- Browser: Gemini image ops follow `gg-dl` redirects while preserving cookies, so `--generate-image`/`--edit-image` actually create output files.
- Browser: Gemini web runs support “Pro” auto-fallback when unavailable and include compatibility init for Gemini web token changes.
- Live tests: add opt-in Gemini web smoke coverage for image generation/editing (cookie-based browser mode).

### Changed
- Browser guard now allows Gemini models (browser engine supports GPT + Gemini; other models require `--engine api`).



[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.7.0)

---

## v0.6.1: 0.6.1
**Published:** 2025-12-13

### Changed
- Browser: default model target now prefers ChatGPT 5.2. Original PR #40 by Muly Oved (@mulyoved) — thank you!
- Browser: remove the “browser fallback” API retry suggestion to avoid accidental billable reruns. Idea from PR #38 by Nico Bailon (@nicobailon) — thank you!

### Fixed
- Browser: manual-login runs now reuse an already-running Chrome more reliably (persist DevTools port in the profile; probe with retries; clean up stale port state). Original PR #40 by Muly Oved (@mulyoved) — thank you!
- Browser: response capture is less likely to truncate by mistaking earlier turns as complete; completion detection is scoped to the last assistant turn and requires brief stability before capture. Original PR #40 by Muly Oved (@mulyoved) — thank you!
- Browser: stale profile cleanup avoids deleting lock files when an active Chrome process is using the profile.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.6.1)

---

## v0.6.0: 0.6.0
**Published:** 2025-12-12

### Added
- GPT-5.2 model support (`gpt-5.2` Thinking, `gpt-5.2-instant`, `gpt-5.2-pro`) plus browser `--browser-extended-thinking` automation. Original PR #37 by Nico Bailon (@nicobailon) — thank you!

### Changed
- API: `gpt-5.1-pro` now targets `gpt-5.2-pro` instead of older Pro fallbacks.
- Browser: “Thinking time → Extended” selection now reuses centralized menu selectors, normalizes text matching, and ships a best-effort helper for future “auto” mode. Original PR #36 by Victor Vannara (@voctory) — thank you!
- Browser: new `--browser-attachments <auto|never|always>` (default `auto`) pastes file contents inline up to ~60k characters, then switches to uploads; if ChatGPT rejects an inline paste as too large, Oracle retries automatically with uploads.
  - Note: the ~60k threshold is based on pasted **characters** in the ChatGPT composer (not token estimates); on rejection we log the retry and switch to uploads automatically.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.6.0)

---

## v0.5.6: 0.5.6
**Published:** 2025-12-09

## Changed
- Browser uploads: after `setFileInputFiles` we now log the chips + file-input contents and only mark success when the real file input contains the uploaded filename; the generic “Files” pill is no longer treated as proof of attachment.
- Inline prompt commit: verification now matches on a normalized prefix and logs the last user turn + counts when commit fails, reducing false negatives for inline/file-paste runs.

## Fixed
- Inline fallback (pasting file contents) now reliably submits and captures the user turn; headful smoke confirms the marker text is echoed back.

(Re-release of 0.5.5)


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.6)

---

## v0.5.4: 0.5.4
**Published:** 2025-12-08

## Changed
- Docs: README now explicitly warns against `pnpx @steipete/oracle` (pnpx cache breaks sqlite bindings); use `npx -y @steipete/oracle` instead. Thanks Xuanwo for flagging this.
- Browser uploads: stick to the single reliable file-input path (no drag/drop fallbacks), wait for the composer to render the new “N files” pill/remove-card UI before sending, and prefer non-image inputs. Thanks Peter for the repros and screenshots that caught the regressions.

## Fixed
- API fallback: gpt-5.1-pro API runs now automatically downgrade to gpt-5.0-pro with a one-line notice (5.1 Pro is not yet available via API).
- Browser uploads: detect ChatGPT’s composer attachment chip (not echoed in the last user turn) to avoid false “Attachment did not appear” failures. Thanks Mariano Belinky (@mbelinky) for the fix.
- Browser interruption: if the user/agent sends SIGINT/SIGTERM/SIGQUIT while the assistant response is still pending, Oracle leaves Chrome running, writes runtime hints, and logs how to reattach with `oracle session <slug>` instead of killing the browser mid-run.
- Browser uploads (ChatGPT UI 2025-12): wait for DOM ready, avoid duplicate uploads, and block Send until the attachment chip/file name (or “N files” pill) is visible so files aren’t sent empty or multiple times.
- Browser i18n: stop-button detection now uses data-testid instead of English `aria-label`; send/input/+ selectors favor data-testid/structural cues to work across localized UIs.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.4)

---

## v0.5.3: 0.5.3
**Published:** 2025-12-06

- `oracle` with no arguments now prints the help/usage banner; launch the interactive UI explicitly via `oracle tui` (keeps `ORACLE_FORCE_TUI` for automation/tests). README updated to match.
- TUI exits gracefully when the terminal drops raw mode (e.g., `setRawMode EIO` after pager issues) and shows a hint to run `stty sane`.
- Ctrl+C in the TUI menu now exits cleanly without printing the paging error loop.
- Exit banner is printed once when leaving the TUI, preventing duplicate "Closing the book" messages after SIGINT or exit actions.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.3)

---

## v0.5.2: 0.5.2
**Published:** 2025-12-06

## Highlights
- Browser click automation now uses a shared pointer/mouse dispatch for send/model/answer-now/copy/stop, fixing blank/ignored clicks in React/ProseMirror UIs. Community contribution: Mike Demarais (PR #30).
- Attachments are verified as visible before sending (covers WKWebView/browser runs where files were selected but not attached), plus refreshed browser smokes for inline + upload paths.
- Updated Inquirer to 13.x and aligned TUI `select` prompts with the latest API.
- Browser config defaults from `~/.oracle/config.json` now apply when CLI flags are untouched, fixing missing Chrome path/profile issues.

## Checks
- lint, typecheck, test, browser smokes, live suites (API/Grok/Gemini/Claude/OpenRouter), and release smoke (`npx @steipete/oracle@0.5.2 --dry-run`).


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.2)

---

## v0.5.1: 0.5.1
**Published:** 2025-12-03

- Browser runs auto-click the ChatGPT ‘Answer now’ gate and wait 500ms before/after submit to avoid subscription/widget races.
- Browser mode fails fast when cookie sync copies zero cookies, pointing at the profile and keytar rebuild command.
- Status CLI matches the TUI session table layout (status/model/mode/timestamp/chars/cost/slug).
- OpenRouter routes via chat/completions; live smokes use z-ai/glm-4.6 and the mixed run covers Grok fast path without skips.
- Docs/guardrails updated with sqlite/keytar rebuild notes for Node 25 and the browser cookie-sync guard.

[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.1)

---

## v0.5.0: 0.5.0
**Published:** 2025-11-25

## Added
- Browser sessions now persist Chrome reattach hints (port/host/target/url) and log them inline; `oracle session <id>` can reconnect to a live tab, harvest the assistant turn, and mark the run completed even if the original controller died. Includes a reconnection helper and regression tests for runtime hint capture and reattach.
- OpenRouter support: `OPENROUTER_API_KEY` auto-routes API runs (when provider keys are missing or the base URL points at OpenRouter), accepts arbitrary model ids (`minimax/minimax-m2`, `z-ai/glm-4.6`, etc.), mixes with built-in models in `--models`, passes attribution headers (`OPENROUTER_REFERER`/`OPENROUTER_TITLE`), and stores per-model logs with safe slugs.
- `pnpm test:browser` runs a Chrome DevTools connectivity check plus headless browser smokes across GPT-5.1 / GPT-5.1-Pro / 5.1 Instant.
- `--browser-manual-login` skips cookie copy, reuses a persistent automation profile (`~/.oracle/browser-profile` by default), and waits for manual ChatGPT login—handy on Windows where app-bound cookies can’t be decrypted; works as an opt-in on macOS/Linux too.
- Manual-login browser sessions can reuse an already-running automation Chrome when remote debugging is enabled; point Oracle at it via `--remote-chrome <host:port>` to avoid relaunching/locks.
- `--browser-port` (alias `--browser-debug-port`, env `ORACLE_BROWSER_PORT`) pins the DevTools port so WSL/Windows users can open a single firewall rule; includes a lightweight `pnpm test:browser` DevTools reachability check.

## Changed
- All API errors now surface as transport reason `api-error` with the raw message and are shown in status/render/TUI; verbose mode still prints transport details. Multi-model callback order test stabilized.
- Default system prompt no longer asks models to announce when the search tool was used.
- API now surfaces a clear error when `gpt-5.1-pro` isn’t available yet (suggests using `gpt-5-pro`).
- Dependency refresh: openai 6.9.1, clipboardy 5, Vitest 4.0.13 (+ coverage), Biome 2.3.7, puppeteer-core 24.31.0, devtools-protocol 0.0.1548823; pinned zod-to-json-schema to 3.24.1 to stay compatible with zod 3.x.
- Windows cookie reader now accepts any `v**` AES-GCM prefix (v10/v11/v20) to stay forward compatible.
- On Windows, cookie sync is disabled by default and manual-login is forced; use inline cookies or `--browser-manual-login` (default) instead of profile-based cookie copy.

## Fixed
- CLI/TUI now print the intro banner only once; forced TUI launches (`ORACLE_FORCE_TUI` or no args in a TTY) no longer show duplicate 🧿 header lines.
- TUI session list cleans up separators, removing the `__disabled__ (Disabled)` placeholder and `(Disabled)` tag on the header row.
- `oracle session --render` no longer drops answers when the model filter is empty or per-model logs are missing (common for browser runs); stored session output is rendered again.
- Browser uploads no longer time out in ChatGPT project workspaces: file input/send-button selectors are broader, upload completion falls back to attached files when buttons are missing, and we added tests to guard the new selectors.
- Live tests now call out that `gpt-5.1` must be reached via api.openai.com; OpenRouter’s Responses API endpoint doesn’t expose `openai/gpt-5.1`, so runs will fail there with `model_not_found` until they add it.
- Browser reattach flow survives controller loss: the controller PID is persisted with the Chrome port/URL so `oracle session <id>` can reconnect, harvest the assistant turn, and mark the run completed even if the original process died.
- Live multi-model smokes force first-party API bases and soft-skip HTML/transport errors (e.g., proxy 404 pages) so missing provider access doesn’t fail the suite.
- Gemini live coverage confirmed with `gemini-2.5-flash-lite` after refreshing `GEMINI_API_KEY`; multi-model live now passes end-to-end when first-party keys are present.
- Token usage formatter again emits two-decimal abbreviations for thousands (e.g., 4.25k) to match CLI output and tests.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.5.0)

---

## v0.4.5: 0.4.5
**Published:** 2025-11-22

- MCP/API responses now report 404/405 from /v1/responses as unsupported-endpoint with guidance to fix base URLs/gateways or use browser engine.

[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.4.5)

---

## v0.4.3: 0.4.3
**Published:** 2025-11-22

- Add xAI Grok 4.1 API support (`--model grok-4.1` / alias `grok`), defaults to `https://api.x.ai/v1`, uses `XAI_API_KEY`, and maps search to `web_search` with docs + live smoke.
- Per-model search tool selection so Grok uses `web_search` while OpenAI models stay on `web_search_preview`; multi-model orchestrator now includes Grok coverage.
- PTY-driven CLI/TUI harness landed for end-to-end coverage; enable via `ORACLE_ENABLE_PTY_TESTS=1` with stub tokenizers to keep runs lightweight.
- MCP (global installs): keep the stdio transport alive until the client closes it so `oracle-mcp` no longer exits immediately after `connect()`.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.4.3)

---

## v0.4.2: Oracle 0.4.2
**Published:** 2025-11-21

### Fixed
- MCP: `npx @steipete/oracle oracle-mcp` now routes directly to the MCP server (even when npx defaults to the CLI binary) and keeps stdout JSON-only for Cursor/other MCP hosts.
- Added the missing `@anthropic-ai/tokenizer` runtime dependency so `npx @steipete/oracle oracle-mcp` starts cleanly.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.4.2)

---

## v0.4.1: Oracle 0.4.1
**Published:** 2025-11-21

### Fixed
- MCP: stdout is now muted during MCP runs, preventing non-JSON logs from breaking hosts like Cursor.
- Added the missing `@anthropic-ai/tokenizer` runtime dependency so `npx @steipete/oracle oracle-mcp` starts cleanly.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.4.1)

---

## v0.4.0: Oracle 0.4.0
**Published:** 2025-11-21

### Added
- Remote Chrome + remote browser service: `oracle serve` launches Chrome with host/token defaults for cross-machine runs, requires the host profile to be signed in, and supports reusing an existing Chrome via `--remote-chrome <host:port>` (IPv6 with `[host]:port`), including remote attachment uploads and clearer validation errors.
- Linux browser support: Chrome/Chromium/Edge runs now work on Linux (including snap-installed Chromium) with cookie sync picking up the snap profile paths. See docs/linux.md for paths and display guidance.
- Browser engine can target Chromium/Edge by pairing `--browser-chrome-path` with the new `--browser-cookie-path` (also configurable via `browser.chromePath` / `browser.chromeCookiePath`). See docs/chromium-forks.md for OS-specific paths and setup steps.
- Markdown bundles render better in the CLI and ChatGPT: each attached file now appears as `### File: <path>` followed by a fenced code block (language inferred), across API bundles, browser bundles (including inline mode), and render/dry-run output; ANSI highlighting still applies on rich TTYs.
- `--render-plain` forces plain markdown output (no ANSI/highlighting) even in a rich TTY; takes precedence when combined with `--render` / `--render-markdown`.
- `--write-output <path>` saves just the final assistant message to disk (adds `.<model>` per file for multi-model runs), with safe path guards and non-fatal write failures.
- Browser engine: `--chatgpt-url` (alias `--browser-url`) and `browser.chatgptUrl` config let you target specific ChatGPT workspace/folder URLs while keeping API `--base-url` separate.
- Multi-model API runner orchestrates multiple API models in one command and aggregates usage/cost; browser engine stays single-model.
- GPT-5.1 Pro API support (new default) and `gpt-5-pro` alias for earlier Pro rollout; GPT-5.1 Codex (API-only) now works end-to-end with high reasoning and auto-forces the API engine. GPT-5.1 Codex Max isn’t available via API yet; the CLI rejects that model until OpenAI ships it.
- Duplicate prompt guard remains active: Oracle blocks a second run when the exact prompt is already running.

### Changed
- Cookie sync covers Chrome, Chromium, Edge, Brave, and Vivaldi profiles; targets chatgpt.com, chat.openai.com, and atlas.openai.com. Windows browser automation is still partial—prefer API or clipboard fallback there.
- Reject prompts shorter than 20 characters with a friendly hint for pro-tier models (`gpt-5.1-pro`) only (prevents accidental costly runs while leaving cheaper models unblocked). Override via ORACLE_MIN_PROMPT_CHARS for automated environments.
- Browser engine default timeout bumped from 15m (900s) to 20m (1200s) so long GPT-5.x Pro responses don’t get cut off; CLI docs/help text now reflect the new ceiling.
- Duration flags such as `--browser-timeout`/`--browser-input-timeout` now accept chained units (`1h2m10s`, `3m10s`, etc.) plus `h`, `m`, `s`, or `ms` suffixes, matching the formats we already log.
- GPT-5.1 Pro and GPT-5 Pro API runs now default to a 60-minute timeout (was 20m) and the “zombie” detector waits the same hour before marking sessions as `error`; CLI messaging/docs updated accordingly so a single “auto” limit covers both behaviors.
- Browser-to-API coercion now happens automatically for GPT-5.1 Codex and Gemini (with a console hint) instead of failing when `--engine browser` is set.
- Multi-model output is easier to scan: aggregate header/summary, deduped per-model headings, and on-demand OSC progress when replaying combined logs.
- `--write-output` adds stricter path safety, rejecting unsafe destinations while keeping writes non-fatal to avoid breaking runs.
- Session slugs now trim individual words to 10 characters to keep auto-generated IDs readable when prompts include very long tokens.
- CLI: `--mode` is now a silent alias for `--engine` for backward compatibility with older docs/scripts; prefer `--engine`.
- CLI guardrail: if a session with the same prompt is already running, new runs abort with guidance to reattach unless `--force` is provided (prevents unintended duplicate API/browser runs).

### Fixed
- Browser assistant capture is more resilient: markdown cleanup no longer drops real answers and prompt-echo recovery keeps the assistant text intact.
- Browser cookie sync on Windows now copies the profile DB into a named temp directory with the expected `Cookies` filename so `chrome-cookies-secure` can read it reliably during browser fallbacks.
- Streaming runs in `--render-plain` mode now send chunks directly to stdout and keep the log sink newline-aligned, preventing missing or double-printed output in TTY and background runs.
- CLI output is consistent again: final answers always print to stdout (even when a log sink is active) and inline runs once more echo the assistant text to stdout.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v0.4.0)

---

## v1.3.0: 1.3.0
**Published:** 2025-11-19

# Changelog

All notable changes to this project will be documented in this file.

## 1.3.0 — 2025-11-19

### Added
- Native Azure OpenAI support! Set `AZURE_OPENAI_ENDPOINT` (plus `AZURE_OPENAI_API_KEY` and optionally `AZURE_OPENAI_DEPLOYMENT`/`AZURE_OPENAI_API_VERSION`) or use the new CLI flags (`--azure-endpoint`, `--azure-deployment`, etc.) to switch automatically to the Azure client.
- **Gemini 3 Pro Support**: Use Google's latest model via `oracle --model gemini`. Requires `GEMINI_API_KEY`.
- Configurable API timeout: `--timeout <seconds|auto>` (default auto = 20m for gpt-5-pro, 30s for other models). Enforced for streaming and background runs.
- OpenAI-compatible base URL override: `--base-url` (or `apiBaseUrl` in config / `OPENAI_BASE_URL`) lets you target LiteLLM proxies, Azure gateways, and other compatible hosts.
- Help text tip: best results come from 6–30 sentences plus key source files; very short prompts tend to be generic.
- Browser inline cookies: `--browser-inline-cookies[(-file)]` (or env) accepts JSON/base64 payloads, auto-loads `~/.oracle/cookies.{json,base64}`, adds a cookie allowlist (`--browser-cookie-names`), and dry-run now reports whether cookies come from Chrome or inline sources.
- Inline runs now print a single completion line (removed duplicate “Finished” summary), keeping output concise.
- Gemini runs stay on API (no browser detours), and the CLI logs the resolved model id alongside masked keys when it differs.
- `--dry-run [summary|json|full]` is now the single preview flag; `--preview` remains as a hidden alias for compatibility.

### Changed
 - Browser engine is now macOS-only; Windows and Linux runs fail fast with guidance to re-run via `--engine api`. Cross-platform browser support is in progress.
 - Browser fallback tips focus on `--browser-bundle-files`, making it clear users can drag the single bundled file into ChatGPT when automation fails.
 - Sessions TUI separates recent vs older runs, adds an Older/Newer action, keeps headers aligned with rows, and avoids separator crashes while preserving an always-selectable “ask oracle” entry.
- CLI output is tidier and more resilient: graceful Ctrl+C, shorter headers/footers, clearer verbose token labels, and reduced trailing spacing.
- File discovery is more reliable on Windows thanks to normalized paths, native-fs glob handling, and `.gitignore` respect across platforms.

## 1.2.0 — 2025-11-18

### Added
- `oracle-mcp` stdio server (bin) with `consult` and `sessions` tools plus read-only session resources at `oracle-session://{id}/{metadata|log|request}`.
- MCP logging notifications for consult streaming (info/debug with byte sizes); browser engine guardrails now check Chrome availability before a browser run starts.
- Hidden root-level aliases `--message` (prompt) and `--include` (files) to mirror common agent calling conventions.
- `--preview` now works with `--engine browser`, emitting the composed browser payload (token estimate, attachment list, optional JSON/full dumps) without launching Chrome or requiring an API key.
- New `--browser-bundle-files` flag to opt into bundling all attachments into a single upload; bundling is still auto-applied when more than 10 files are provided.
- Desktop session notifications (default on unless CI/SSH) with `--[no-]notify` and optional `--notify-sound`; completed runs announce session name, API cost, and character count via OS-native toasts.
- Per-user JSON5 config at `~/.oracle/config.json` to set default engine/model, notification prefs (including sound/mute rules), browser defaults, heartbeat, file-reporting, background mode, and prompt suffixes. CLI/env still override config.
- Session lists now show headers plus a cost column for quick scanning.

### Changed
- Browser model picker is now more robust: longer menu-open window, richer tokens/testids for GPT-5.1 and GPT-5 Pro, fallback snapshot logging, and best-effort selection to reduce “model not found” errors.
- MCP consult honors notification settings so the macOS Swift notifier fires for MCP-triggered runs.
- `sessions` tool now returns a summary row for `id` lookups by default; pass `detail: true` to fetch full metadata/log/request to avoid large accidental payloads.
- Directory/glob expansions now honor `.gitignore` files and skip dotfiles by default; explicitly matching patterns (e.g., `--file "src/**/.keep"`) still opt in.
- Default ignores when crawling project roots now drop common build/cache folders (`node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`) unless the path is passed explicitly. Oracle logs each skipped path for transparency.
- Browser engine now logs a one-line warning before cookie sync, noting macOS may prompt for a Keychain password and how to bypass via `--browser-no-cookie-sync` or `--browser-allow-cookie-errors`.
- gpt-5-pro API runs default to non-blocking; add `--wait` to block. `gpt-5.1` and browser runs still block by default. CLI now polls once for `in_progress` responses before failing.
- macOS notifier helper now ships signed/notarized with the Oracle icon and auto-repairs execute bits for the fallback terminal-notifier.
- Session summaries and cost displays are clearer, with zombie-session detection to avoid stale runs.
- Token estimation now uses the full request body (instructions + input text + tools/reasoning/background/store) and compares estimated vs actual tokens in the finished stats to reduce 400/413 surprises.
- Help tips now explicitly warn that Oracle cannot see your project unless you pass `--file …` to attach the necessary source.

#### MCP configuration (quick reference)
- Local stdio (mcporter): add to `config/mcporter.json`
  ```json
  {
    "name": "oracle",
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@steipete/oracle", "oracle-mcp"]
  }
  ```
- Claude Code (global/user scope):  
  `claude mcp add --scope user --transport stdio oracle -- oracle-mcp`
- Project-scoped Claude: drop `.mcp.json` next to the repo root with
  ```json
  {
    "mcpServers": {
      "oracle": { "type": "stdio", "command": "npx", "args": ["-y", "@steipete/oracle", "oracle-mcp"] }
    }
  }
  ```
- The MCP `consult` tool honors `~/.oracle/config.json` defaults (engine/model/search/prompt suffix/heartbeat/background/filesReport) unless the caller overrides them.

## 1.1.0 — 2025-11-17

Highlights
- Markdown rendering for completed sessions (`oracle session|status <id> --render` / `--render-markdown`) with ANSI formatting in rich TTYs; falls back to raw when logs are huge or stdout isn’t a TTY.
- New `--path` flag on `oracle session <id>` prints the stored session directory plus metadata/request/log files, erroring if anything is missing. Uses soft color in rich terminals for quick scanning.

Details
### Added
- `oracle session <id> --path` now prints the on-disk session directory plus metadata/request/log files, exiting with an error when any expected file is missing instead of attaching.
- When run in a rich TTY, `--path` labels and paths are colorized for easier scanning.

### Improved
- `oracle session|status <id> --render` (alias `--render-markdown`) pretty-prints completed session markdown to ANSI in rich TTYs, falls back to raw when non-TTY or oversized logs.
## 1.0.10 — 2025-11-17

### Added
- Rich terminals that support OSC 9;4 (Ghostty 1.2+, WezTerm, Windows Terminal) now show an inline progress bar while Oracle waits for the OpenAI response; disable with `ORACLE_NO_OSC_PROGRESS=1`, force with `ORACLE_FORCE_OSC_PROGRESS=1`.

## 1.0.9 — 2025-11-16

### Added
- `oracle session|status <id> --render` (alias `--render-markdown`) pretty-prints completed session markdown to ANSI in rich TTYs, falls back to raw when non-TTY or oversized logs.
- Hidden root-level `--session <id>` alias attaches directly to a stored session (for agents/automation).
- README now recommends preferring API engine for reliability and longer uninterrupted runs when an API key is available.
- Session rendering now uses Markdansi (micromark/mdast-based), removing markdown-it-terminal and eliminating HTML leakage/crashes during replays.
- Added a local Markdansi type shim for now; switch to official types once the npm package ships them.
- Markdansi renderer now enables color/hyperlinks when TTY by default and auto-renders sessions unless the user explicitly disables it.

## 1.0.8 — 2025-11-16

### Changed
- Help tips call out that Oracle is one-shot and does not remember prior runs, so every query should include full context.
- `oracle session <id>` now logs a brief notice when extra root-only flags are present (e.g., `--render-markdown`) to make it clear those options are ignored during reattach.

## 1.0.7 — 2025-11-16

### Changed
- Browser-mode thinking monitor now emits a text-only progress bar instead of the "Pro thinking" string.
- `oracle session <id>` trims preamble/log noise and prints from the first `Answer:` line once a session is finished.
- Help tips now stress sending whole directories and richer project briefings for better answers.

## 1.0.6 — 2025-11-15

### Changed
- Colorized live run header (model/tokens/files) when a rich TTY is available.
- Added a blank line before the `Answer:` prefix for readability.
- Masked API key logging now shows first/last 4 characters (e.g., `OPENAI_API_KEY=sk-p****qfAA`).
- Suppressed duplicate session header on reattach and removed repeated background response IDs in heartbeats.

### Browser mode
- When more than 10 files are provided, automatically bundles all files into a single `attachments-bundle.txt` to stay under ChatGPT’s upload cap and logs a verbose warning when bundling occurs.

## 1.0.5 — 2025-11-15

### Added
- Logs the masked OpenAI key in use (`Using OPENAI_API_KEY=xxxx****yyyy`) so runs are traceable without leaking secrets.
- Logs a helpful tip when you run without attachments, reminding you to pass context via `--file`.

## 1.0.3 — 2025-11-15

## 1.0.2 — 2025-11-15

## 1.0.2 — 2025-11-15

### Added
- Positional prompt shorthand: `oracle "prompt here"` (and `npx -y @steipete/oracle "..."`) now maps the positional argument to `--prompt` automatically.

### Fixed
- `oracle status/session` missing-prompt guard now coexists with the positional prompt path and still shows the cleanup tip when no sessions exist.

## 1.0.1 — 2025-11-15

### Fixed
- Corrected npm binary mapping so `oracle` is installed as an executable. Published with `--tag beta`.

## 1.0.0 — 2025-11-15

### Added
- Dual-engine support (API and browser) with automatic selection: defaults to API when `OPENAI_API_KEY` is set, otherwise falls back to browser mode.
- Session-friendly prompt guard that allows `status`/`session` commands to run without a prompt while still enforcing prompts for normal runs, previews, and dry runs.
- Browser mode uploads each `--file` individually and logs Chrome PID/port for detachable runs.
- Background GPT-5 Pro runs with heartbeat logging and reconnect support for long responses.
- File token accounting (`--files-report`) and dry-run summaries for both engines.
- Comprehensive CLI and browser automation test suites, including engine selection and prompt requirement coverage.

### Changed
- Help text, README, and browser-mode docs now describe the auto engine fallback and the deprecated `--browser` alias.
- CLI engine resolution is centralized to keep legacy flags, model inference, and environment defaults consistent.

### Fixed
- `oracle status` and `oracle session` no longer demand `--prompt` when used directly.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v1.3.0)

---

## v1.2.0: Oracle 1.2.0
**Published:** 2025-11-18

### Added
- `oracle-mcp` stdio server (bin) with `consult` and `sessions` tools plus read-only session resources at `oracle-session://{id}/{metadata|log|request}`.
- MCP logging notifications for consult streaming (info/debug with byte sizes); browser engine guardrails now check Chrome availability before a browser run starts.
- Hidden root-level aliases `--message` (prompt) and `--include` (files) to mirror common agent calling conventions.
- `--preview` now works with `--engine browser`, emitting the composed browser payload (token estimate, attachment list, optional JSON/full dumps) without launching Chrome or requiring an API key.
- New `--browser-bundle-files` flag to opt into bundling all attachments into a single upload; bundling is still auto-applied when more than 10 files are provided.
- Desktop session notifications (default on unless CI/SSH) with `--[no-]notify` and optional `--notify-sound`; completed runs announce session name, API cost, and character count via OS-native toasts.
- Per-user JSON5 config at `~/.oracle/config.json` to set default engine/model, notification prefs (including sound/mute rules), browser defaults, heartbeat, file-reporting, background mode, and prompt suffixes. CLI/env still override config.
- Session lists now show headers plus a cost column for quick scanning.

### Changed
- Browser model picker is now more robust: longer menu-open window, richer tokens/testids for GPT-5.1 and GPT-5 Pro, fallback snapshot logging, and best-effort selection to reduce “model not found” errors.
- MCP consult honors notification settings so the macOS Swift notifier fires for MCP-triggered runs.
- `sessions` tool now returns a summary row for `id` lookups by default; pass `detail: true` to fetch full metadata/log/request to avoid large accidental payloads.
- Directory/glob expansions now honor `.gitignore` files and skip dotfiles by default; explicitly matching patterns (e.g., `--file "src/**/.keep"`) still opt in.
- Default ignores when crawling project roots now drop common build/cache folders (`node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`) unless the path is passed explicitly. Oracle logs each skipped path for transparency.
- Browser engine now logs a one-line warning before cookie sync, noting macOS may prompt for a Keychain password and how to bypass via `--browser-no-cookie-sync` or `--browser-allow-cookie-errors`.
- gpt-5-pro API runs default to non-blocking; add `--wait` to block. `gpt-5.1` and browser runs still block by default. CLI now polls once for `in_progress` responses before failing.
- macOS notifier helper now ships signed/notarized with the Oracle icon and auto-repairs execute bits for the fallback terminal-notifier.
- Session summaries and cost displays are clearer, with zombie-session detection to avoid stale runs.
- Token estimation now uses the full request body (instructions + input text + tools/reasoning/background/store) and compares estimated vs actual tokens in the finished stats to reduce 400/413 surprises.

#### MCP configuration (quick reference)
- Local stdio (mcporter): add to `config/mcporter.json`
  ```json
  {
    "name": "oracle",
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@steipete/oracle", "oracle-mcp"]
  }
  ```
- Claude Code (global/user scope):  
  `claude mcp add --scope user --transport stdio oracle -- oracle-mcp`
- Project-scoped Claude: drop `.mcp.json` next to the repo root with
  ```json
  {
    "mcpServers": {
      "oracle": { "type": "stdio", "command": "npx", "args": ["-y", "@steipete/oracle", "oracle-mcp"] }
    }
  }
  ```
- The MCP `consult` tool honors `~/.oracle/config.json` defaults (engine/model/search/prompt suffix/heartbeat/background/filesReport) unless the caller overrides them.



[View on GitHub](https://github.com/steipete/oracle/releases/tag/v1.2.0)

---

## v1.1.0: Oracle 1.1.0
**Published:** 2025-11-18

- New `--path` flag prints stored session directory + metadata/request/log files, erroring if anything is missing.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v1.1.0)

---

## v1.0.8: Oracle 1.0.8
**Published:** 2025-11-18

- `oracle session <id>` logs a notice when extra root-only flags are present.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v1.0.8)

---

## v1.0.7: Oracle 1.0.7
**Published:** 2025-11-18

- `oracle session <id>` trims preamble/logs and prints from the first `Answer:` line once finished.
- Help tips emphasize richer context and directory uploads; improved key masking shows first/last 4 characters.


[View on GitHub](https://github.com/steipete/oracle/releases/tag/v1.0.7)

---

