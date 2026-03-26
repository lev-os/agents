# CLI-Side Implementation Guide

> This guide covers the Rust CLI implementation patterns for the auth flow.
> Adaptable to any language with HTTP client, crypto, and keyring libraries.

## Command Structure

```
my-cli login          # Browser PKCE (auto-detected)
my-cli login --remote # Force device code flow
my-cli login --manual # Force manual PKCE (print URL, paste callback)
my-cli logout         # Revoke + clear credentials
my-cli auth set-key   # Store pre-generated API key
my-cli whoami         # Show current user
```

## Login Command Flow

```rust
pub async fn login(opts: LoginOpts) -> Result<()> {
    // 1. Determine auth tier
    let tier = if opts.remote {
        AuthTier::DeviceCode
    } else if opts.manual {
        AuthTier::ManualPkce
    } else {
        detect_environment()
    };

    // 2. Execute tier-specific flow
    let tokens = match tier {
        AuthTier::BrowserPkce => browser_pkce_flow(&opts).await?,
        AuthTier::ManualPkce => manual_pkce_flow(&opts).await?,
        AuthTier::DeviceCode => device_code_flow(&opts).await?,
    };

    // 3. Store credentials
    store_credentials(&tokens)?;

    // 4. Post-login actions (e.g., sync, install defaults)
    if opts.onboard {
        post_login_onboarding(&tokens).await?;
    }

    eprintln!("Logged in as {}", tokens.email.unwrap_or_default());
    Ok(())
}
```

## Environment Detection

```rust
fn detect_environment() -> AuthTier {
    // Check for explicit flags first
    if !atty::is(atty::Stream::Stdin) {
        // Non-interactive terminal (piped, cron, etc.)
        return AuthTier::DeviceCode; // or error
    }

    // SSH detection
    if std::env::var("SSH_CLIENT").is_ok() || std::env::var("SSH_TTY").is_ok() {
        return AuthTier::DeviceCode;
    }

    // Linux: check for display server
    #[cfg(target_os = "linux")]
    {
        if std::env::var("DISPLAY").is_err() && std::env::var("WAYLAND_DISPLAY").is_err() {
            return AuthTier::ManualPkce;
        }
    }

    // macOS and Windows always have GUI
    AuthTier::BrowserPkce
}
```

## Browser PKCE Flow

```rust
async fn browser_pkce_flow(opts: &LoginOpts) -> Result<TokenResponse> {
    // 1. Generate PKCE pair
    let verifier = generate_pkce_verifier(); // 32 random bytes → base64url
    let challenge = sha256_base64url(&verifier);

    // 2. Generate CSRF state
    let state = generate_state(); // 32 random bytes → base64url

    // 3. Bind TCP listener on random port
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let port = listener.local_addr()?.port();

    // 4. Build auth URL
    let url = format!(
        "{}/api/v1/auth/cli-login?port={}&code_challenge={}&state={}",
        api_url, port, challenge, state
    );

    // 5. Open browser (graceful failure)
    let _ = open::that(&url);
    eprintln!("Opening browser... If it doesn't open, visit:\n  {}", url);

    // 6. Wait for callback
    let callback = wait_for_callback(listener, &state, Duration::from_secs(300))?;

    // 7. Exchange code for tokens
    exchange_code(&callback.code, &verifier).await
}

fn wait_for_callback(
    listener: TcpListener,
    expected_state: &str,
    timeout: Duration,
) -> Result<CallbackParams> {
    // Non-blocking so we can implement a timeout loop
    listener.set_nonblocking(true)?;
    let deadline = Instant::now() + timeout;

    loop {
        if Instant::now() > deadline {
            return Err(anyhow!("Timeout waiting for callback"));
        }

        match listener.accept() {
            Ok((stream, _)) => {
                // Parse HTTP request
                let request = read_http_request(&stream)?;
                let params = parse_callback_params(&request)?;

                // Verify CSRF state
                if params.state != expected_state {
                    send_http_response(&stream, 400, "State mismatch");
                    continue;
                }

                send_http_response(&stream, 200, "Login successful! You can close this tab.");
                return Ok(params);
            }
            Err(e) if e.kind() == io::ErrorKind::WouldBlock => {
                // No connection yet — sleep briefly and retry
                std::thread::sleep(Duration::from_millis(100));
            }
            Err(e) => return Err(e.into()),
        }
    }
}
```

## Manual PKCE Flow (Tier 2)

```rust
async fn manual_pkce_flow(opts: &LoginOpts) -> Result<TokenResponse> {
    let verifier = generate_pkce_verifier();
    let challenge = sha256_base64url(&verifier);
    let state = generate_state();

    // Bind listener (may or may not be reachable)
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let port = listener.local_addr()?.port();

    let url = format!(
        "{}/api/v1/auth/cli-login?port={}&code_challenge={}&state={}",
        api_url, port, challenge, state
    );

    eprintln!("Open this URL in your browser:\n  {}\n", url);
    eprintln!("Then paste the callback URL here:");

    // Race: wait for TCP callback OR stdin paste
    // Note: stdin read must be spawned on a blocking thread
    tokio::select! {
        result = wait_for_tcp_callback(&listener, &state) => {
            let callback = result?;
            exchange_code(&callback.code, &verifier).await
        }
        result = tokio::task::spawn_blocking({
            let state = state.clone();
            move || wait_for_stdin_paste_sync(&state)
        }) => {
            let callback = result??;
            exchange_code(&callback.code, &verifier).await
        }
    }
}

fn wait_for_stdin_paste_sync(expected_state: &str) -> Result<CallbackParams> {
    // Called via spawn_blocking — blocking stdin read is safe here
    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;
    let input = input.trim();

    // Accept multiple formats:
    // 1. Full URL: http://127.0.0.1:12345/callback?code=abc&state=xyz
    // 2. Relative: /callback?code=abc&state=xyz
    // 3. Query only: ?code=abc&state=xyz
    // 4. Params only: code=abc&state=xyz

    let query = if input.starts_with("http") {
        Url::parse(input)?.query().unwrap_or("").to_string()
    } else if input.starts_with("/callback") {
        input.splitn(2, '?').nth(1).unwrap_or("").to_string()
    } else if input.starts_with('?') {
        input[1..].to_string()
    } else {
        input.to_string()
    };

    let params = parse_query_string(&query)?;

    if params.state != expected_state {
        return Err(anyhow!("State mismatch — possible CSRF attack"));
    }

    Ok(params)
}
```

## Device Code Flow (Tier 3)

```rust
async fn device_code_flow(opts: &LoginOpts) -> Result<TokenResponse> {
    // 1. Request device code
    let response: DeviceCodeResponse = client
        .post(&format!("{}/api/v1/auth/device-code", api_url))
        .json(&json!({ "client_id": CLIENT_ID }))
        .send()
        .await?
        .json()
        .await?;

    // 2. Display code to user
    eprintln!("\n  Code: {}\n", response.user_code);
    eprintln!("  Visit: {}", response.verification_url_complete);
    eprintln!("  Or open {} and enter the code.\n", response.verification_url);

    // 3. Poll for verification
    let mut interval = response.interval;
    let deadline = Instant::now() + Duration::from_secs(response.expires_in);

    loop {
        if Instant::now() > deadline {
            return Err(anyhow!("Device code expired"));
        }

        tokio::time::sleep(Duration::from_secs(interval)).await;

        let poll = client
            .post(&format!("{}/api/v1/auth/device-token", api_url))
            .json(&json!({
                "device_code": response.device_code,
                "client_id": CLIENT_ID,
            }))
            .send()
            .await?;

        match poll.status().as_u16() {
            200 => return poll.json().await.map_err(Into::into),
            400 => {
                let err: ErrorBody = poll.json().await?;
                match err.error.code.as_str() {
                    "authorization_pending" => continue,
                    "slow_down" => { interval += 5; continue; }
                    "expired_token" => return Err(anyhow!("Code expired")),
                    _ => return Err(anyhow!("{}", err.error.message)),
                }
            }
            429 => { interval += 5; continue; }
            _ => return Err(anyhow!("Unexpected status: {}", poll.status())),
        }
    }
}
```

## Token Refresh (Transparent to User)

```rust
/// Middleware: ensure credentials are fresh before any API call
async fn ensure_fresh_credentials(creds: &mut Credentials) -> Result<()> {
    // Check if token needs refresh (30-second safety window)
    let needs_refresh = match creds.expires_at {
        Some(exp) => exp - Duration::from_secs(30) < Utc::now(),
        None => false, // API keys don't expire
    };

    if !needs_refresh {
        return Ok(());
    }

    let refresh_token = creds.refresh_token.as_ref()
        .ok_or_else(|| anyhow!("No refresh token — re-login required"))?;

    let response = client
        .post(&format!("{}/api/v1/auth/refresh", api_url))
        .json(&json!({ "refresh_token": refresh_token }))
        .send()
        .await?;

    if response.status().is_success() {
        let new_tokens: TokenResponse = response.json().await?;
        creds.access_token = new_tokens.access_token;
        if let Some(rt) = new_tokens.refresh_token {
            creds.refresh_token = Some(rt);
        }
        creds.expires_at = Some(Utc::now() + chrono::Duration::seconds(new_tokens.expires_in));
        store_credentials(creds)?;
        Ok(())
    } else {
        Err(anyhow!("Token refresh failed — re-login required"))
    }
}
```

## HTTP Client Configuration

```rust
// Retry client for connectivity-sensitive operations
fn build_retry_client() -> RetryClient {
    RetryClient::new(
        Client::builder()
            .user_agent(format!("jsm/{} ({}/{})", VERSION, OS, ARCH))
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap(),
        ExponentialBackoff::builder()
            .retry_initial_wait(Duration::from_millis(500))
            .retry_max_elapsed_time(Duration::from_secs(30))
            .build(),
        3, // max retries
    )
}

// For health/connectivity checks specifically:
// Use a dedicated lightweight endpoint (/api/health/live)
// that has near-zero cold start time
async fn check_connectivity() -> bool {
    retry_client
        .get(&format!("{}/api/health/live", api_url))
        .send()
        .await
        .map(|r| r.status().is_success())
        .unwrap_or(false)
}
```

## Error Handling Patterns

```rust
// Map server errors to user-friendly messages
fn map_auth_error(status: u16, code: &str) -> String {
    match (status, code) {
        (401, "UNAUTHORIZED") => "Authentication required. Run `jsm login`".into(),
        (401, "TOKEN_EXPIRED") => "Session expired. Run `jsm login`".into(),
        (403, "SUBSCRIPTION_REQUIRED") => "Active subscription required. Visit https://...".into(),
        (403, "ACCOUNT_SUSPENDED") => "Account suspended. Contact support.".into(),
        (409, _) => "Authorization code already used. Try logging in again.".into(),
        (429, _) => "Rate limited. Wait a moment and try again.".into(),
        _ => format!("Authentication failed: {} ({})", code, status),
    }
}
```

## Testing Auth in CI

```rust
#[cfg(test)]
mod tests {
    // Use environment variables for test credentials
    // NEVER use real OAuth in CI
    fn test_credentials() -> Option<Credentials> {
        let token = std::env::var("JSM_TEST_OAUTH_TOKEN").ok()?;
        Some(Credentials {
            access_token: token,
            refresh_token: None,
            expires_at: None,
            user_id: Some("test-user".into()),
            email: Some("test@example.com".into()),
        })
    }
}
```
