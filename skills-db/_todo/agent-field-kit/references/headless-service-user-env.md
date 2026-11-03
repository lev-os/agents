# Headless service-user PATH and auth handoff

Use this reference when a VPS/container agent is reachable through a gateway or scheduler and the human asks to install CLI tools, wire shell profiles, or authenticate a headless CLI that later cron/gateway jobs must use.

## Durable pattern

1. **Identify the runtime user first**
   ```bash
   whoami
   id
   printf 'HOME=%s\nSHELL=%s\n' "$HOME" "$SHELL"
   ```
   Authenticate and install tools under the same Unix user/HOME that the gateway, cron, or long-running service uses. If the human SSHs as a different user, credentials and caches may land in the wrong HOME and the agent will not see them later.

2. **Create one managed environment file**
   Prefer a single sourced file over scattered profile edits, e.g.:
   ```bash
   mkdir -p "$HOME/.config/<workspace>"
   cat > "$HOME/.config/<workspace>/env.sh" <<'EOF'
   for dir in \
     /opt/data/bin \
     /opt/data/.npm-global/bin \
     /opt/hermes/.venv/bin \
     "$HOME/.local/bin" \
     "$HOME/bin"
   do
     if [ -d "$dir" ]; then
       case ":$PATH:" in
         *":$dir:"*) ;;
         *) PATH="$dir:$PATH" ;;
       esac
     fi
   done
   export PATH
   export NPM_CONFIG_PREFIX="/opt/data/.npm-global"
   EOF
   ```

3. **Source it from all shells the user might invoke**
   Add an idempotent block to `.profile`, `.bashrc`, `.zprofile`, and `.zshrc` as appropriate:
   ```bash
   # >>> workspace tools >>>
   [ -f "$HOME/.config/<workspace>/env.sh" ] && . "$HOME/.config/<workspace>/env.sh"
   # <<< workspace tools <<<
   ```

4. **Verify with login shells**
   ```bash
   sh -lc 'command -v hermes; command -v slackdump; command -v gh'
   bash -lc 'command -v hermes; command -v slackdump; command -v gh'
   zsh -lc 'command -v hermes; command -v slackdump; command -v gh'
   ```
   Skip `zsh` if it is not installed.

## Headless CLI auth handoff

For browser-based CLIs on dumb terminals, do not assume the CLI can open a browser or provide a device-code URL. Check the tool's auth modes. If browser auth is unavailable, prefer a secure file-based handoff over pasting secrets into chat:

- cookie file path (for tools that accept `-cookie /path/to/cookie.txt`)
- token file or env var loaded from the service user's secure env
- a human-run command that explicitly sets `HOME=<service-user-home>` so caches land where cron/gateway jobs will read them

Example shape:
```bash
HOME=/opt/data/home tool auth ...
```

## Cron/script placement pitfall

Some schedulers resolve relative script names under a scheduler-owned scripts directory, not the job workdir. If a job says `script: name.sh`, verify the actual resolved path in the scheduler status, then either:

- place a thin wrapper in the scheduler scripts directory, or
- update the job to an absolute/expected script path if the scheduler supports it.

Keep wrappers tiny: source the managed env file, then `exec` the repo script.
