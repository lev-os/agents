# Environment Detection for Auth Tier Selection

> The CLI must automatically determine whether the user has access to a local
> browser, is running over SSH, or is in a fully headless environment. Getting
> this wrong means the auth flow fails silently or presents an unusable path.

## Detection Algorithm

```
┌─────────────────────────────────────┐
│ Is stdin a terminal (TTY)?          │
│ (atty::is(Stream::Stdin))           │
└─────────────┬───────────────────────┘
              │
         ┌────┴────┐
         │ NO      │ YES
         ▼         ▼
    Error:     ┌──────────────────────┐
    "Non-      │ Is --remote flag set?│
    interactive│ Is --manual flag set?│
    mode.      └─────────┬────────────┘
    Use API            │
    key."         ┌────┴────────┐
                  │ --remote    │ --manual → Tier 2
                  ▼             │ neither ↓
             Tier 3        ┌───────────────────────┐
             (Device)      │ SSH_CLIENT or SSH_TTY  │
                           │ environment var set?   │
                           └──────────┬────────────┘
                                 ┌────┴────┐
                                 │ YES     │ NO
                                 ▼         ▼
                            Tier 3    ┌────────────────┐
                            (Device)  │ Platform check │
                                      └───────┬────────┘
                                          ┌───┴───────┐
                                          │           │
                                     Linux       macOS/Windows
                                       │              │
                               ┌───────┴──────┐   Always Tier 1
                               │ DISPLAY or    │   (has GUI)
                               │ WAYLAND_      │
                               │ DISPLAY set?  │
                               └──────┬────────┘
                                 ┌────┴────┐
                                 │ YES     │ NO
                                 ▼         ▼
                            Tier 1    Tier 2
                            (Browser) (Manual)
```

## Environment Variables

| Variable | Meaning | Platform |
|----------|---------|----------|
| `SSH_CLIENT` | Set by OpenSSH when connected via SSH | All |
| `SSH_TTY` | TTY allocated for SSH session | All |
| `SSH_CONNECTION` | Full connection info (also indicates SSH) | All |
| `DISPLAY` | X11 display server address | Linux |
| `WAYLAND_DISPLAY` | Wayland compositor socket | Linux |
| `TERM_PROGRAM` | Terminal emulator name | macOS (often) |
| `CONTAINER` | Container runtime indicator | Docker, Podman |
| `WSL_DISTRO_NAME` | Windows Subsystem for Linux | WSL |

## Platform-Specific Notes

### Linux

Linux is the most complex because it has multiple display server protocols
and can run without any GUI at all (headless servers).

```rust
#[cfg(target_os = "linux")]
fn has_display() -> bool {
    std::env::var("DISPLAY").is_ok() || std::env::var("WAYLAND_DISPLAY").is_ok()
}
```

**WSL edge case:** WSL2 may have `DISPLAY` set (for WSLg) but `open::that()` may
still fail to open a browser. Test empirically and fall back gracefully.

### macOS

macOS always has a GUI (even when accessed via SSH, the GUI persists).
However, SSH sessions can't open the user's browser on the remote display.

```rust
#[cfg(target_os = "macos")]
fn detect_tier() -> AuthTier {
    if is_ssh() {
        AuthTier::DeviceCode // SSH into Mac → device code
    } else {
        AuthTier::BrowserPkce // Local Mac → browser
    }
}
```

### Windows

Windows always has a GUI. The main edge case is WSL:

```rust
#[cfg(target_os = "windows")]
fn detect_tier() -> AuthTier {
    AuthTier::BrowserPkce // Windows always has browser access
}

// But for WSL (detected as Linux):
#[cfg(target_os = "linux")]
fn is_wsl() -> bool {
    std::env::var("WSL_DISTRO_NAME").is_ok()
}
```

### Containers

Docker, Podman, and other containers are always headless:

```rust
fn is_container() -> bool {
    // Check for container indicators
    std::env::var("CONTAINER").is_ok()
        || std::path::Path::new("/.dockerenv").exists()
        || std::fs::read_to_string("/proc/1/cgroup")
            .map(|s| s.contains("docker") || s.contains("containerd"))
            .unwrap_or(false)
}
```

## Browser Opening

```rust
fn try_open_browser(url: &str) -> bool {
    match open::that(url) {
        Ok(()) => {
            // Wait briefly for browser to start
            std::thread::sleep(std::time::Duration::from_millis(500));
            true
        }
        Err(e) => {
            eprintln!("Could not open browser: {}", e);
            false
        }
    }
}
```

**Important:** `open::that()` returning `Ok(())` doesn't guarantee the browser
actually opened. It means the OS command succeeded. On Linux, this calls
`xdg-open` which may succeed but the browser may not launch.

## Graceful Degradation

The golden rule: **never let the user get stuck**. If auto-detection is wrong,
the user should still be able to complete auth.

```rust
async fn login_with_fallback(opts: &LoginOpts) -> Result<TokenResponse> {
    let tier = detect_environment();

    match tier {
        AuthTier::BrowserPkce => {
            match browser_pkce_flow(opts).await {
                Ok(tokens) => Ok(tokens),
                Err(e) => {
                    eprintln!("Browser auth failed: {}. Falling back to device code.", e);
                    device_code_flow(opts).await
                }
            }
        }
        AuthTier::ManualPkce => manual_pkce_flow(opts).await,
        AuthTier::DeviceCode => device_code_flow(opts).await,
    }
}
```

## Testing Environment Detection

```rust
#[cfg(test)]
mod tests {
    use temp_env::with_vars;

    #[test]
    fn ssh_detected_from_env() {
        with_vars([("SSH_CLIENT", Some("1.2.3.4 5678 22"))], || {
            assert!(is_ssh());
            assert_eq!(detect_environment(), AuthTier::DeviceCode);
        });
    }

    #[test]
    fn linux_with_display_gets_browser() {
        with_vars([
            ("SSH_CLIENT", None::<&str>),
            ("DISPLAY", Some(":0")),
        ], || {
            assert_eq!(detect_environment(), AuthTier::BrowserPkce);
        });
    }

    #[test]
    fn linux_no_display_gets_manual() {
        with_vars([
            ("SSH_CLIENT", None::<&str>),
            ("DISPLAY", None::<&str>),
            ("WAYLAND_DISPLAY", None::<&str>),
        ], || {
            assert_eq!(detect_environment(), AuthTier::ManualPkce);
        });
    }
}
```
