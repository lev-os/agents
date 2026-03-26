# Credential Storage

> CLI tokens must be stored securely at rest. The storage hierarchy tries the
> most secure option first and falls back gracefully.

## Storage Hierarchy

```
1. OS Keyring (preferred)
   ├── macOS: Keychain (via Security.framework)
   ├── Linux: Secret Service (GNOME Keyring, KDE Wallet)
   └── Windows: Credential Manager (DPAPI)

2. Encrypted File (fallback)
   └── ~/.config/<cli>/credentials.json
       AES-256-GCM + PBKDF2 key derivation (file contents are encrypted)

3. Error (no suitable storage)
   → Suggest API key stored in environment variable
```

## Keyring Implementation

```rust
use keyring::Entry;

const SERVICE_NAME: &str = "my-saas-cli";
const KEYRING_USER: &str = "default";

fn store_to_keyring(creds: &Credentials) -> Result<()> {
    let json = serde_json::to_string(creds)?;
    let entry = Entry::new(SERVICE_NAME, KEYRING_USER)?;
    entry.set_password(&json)?;
    Ok(())
}

fn load_from_keyring() -> Result<Credentials> {
    let entry = Entry::new(SERVICE_NAME, KEYRING_USER)?;
    let json = entry.get_password()?;
    Ok(serde_json::from_str(&json)?)
}

fn delete_from_keyring() -> Result<()> {
    let entry = Entry::new(SERVICE_NAME, KEYRING_USER)?;
    entry.delete_credential()?;
    Ok(())
}
```

### Keyring Pitfall: Interactive Prompts

On Linux, accessing the keyring may trigger a GUI password dialog.
This is **catastrophic** for background operations like `is_authenticated()`.

```rust
// BAD: triggers keyring prompt during background check
fn is_authenticated() -> bool {
    load_from_keyring().is_ok() // May pop up dialog!
}

// GOOD: suppress keyring in non-login contexts
fn is_authenticated_noninteractive() -> bool {
    // Try keyring with timeout/suppression
    match load_from_keyring_quiet() {
        Ok(creds) => !creds.access_token.is_empty(),
        Err(_) => {
            // Fallback to encrypted file (never prompts)
            load_from_encrypted_file().is_ok()
        }
    }
}
```

## Encrypted File Storage

When keyring is unavailable (SSH, containers, WSL):

```rust
use aes_gcm::{Aes256Gcm, Key, Nonce, aead::Aead};
use pbkdf2::pbkdf2_hmac;
use rand::RngCore;

const CREDENTIALS_FILE: &str = "credentials.json";
const PBKDF2_ITERATIONS: u32 = 600_000;

fn derive_key(passphrase: &[u8], salt: &[u8]) -> Key<Aes256Gcm> {
    let mut key = [0u8; 32];
    pbkdf2_hmac::<sha2::Sha256>(passphrase, salt, PBKDF2_ITERATIONS, &mut key);
    Key::<Aes256Gcm>::from(key)
}

fn encrypt_credentials(creds: &Credentials) -> Result<Vec<u8>> {
    let plaintext = serde_json::to_vec(creds)?;

    // Generate random salt and nonce
    let mut salt = [0u8; 32];
    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut salt);
    rand::thread_rng().fill_bytes(&mut nonce_bytes);

    // Derive key from machine-specific material
    let machine_id = get_machine_identifier()?;
    let key = derive_key(machine_id.as_bytes(), &salt);

    // Encrypt
    let cipher = Aes256Gcm::new(&key);
    let nonce = Nonce::from_slice(&nonce_bytes);
    let ciphertext = cipher.encrypt(nonce, plaintext.as_ref())?;

    // Pack: salt + nonce + ciphertext
    let mut packed = Vec::new();
    packed.extend_from_slice(&salt);
    packed.extend_from_slice(&nonce_bytes);
    packed.extend_from_slice(&ciphertext);

    Ok(packed)
}

fn get_machine_identifier() -> Result<String> {
    // Not a password — an anti-portability measure. hostname + username are
    // low-entropy and discoverable, so this protects against casual file
    // theft (e.g., backup exposure) but NOT a targeted local attacker.
    // For stronger protection, prompt for a passphrase or use OS keyring.
    let hostname = hostname::get()?.to_string_lossy().to_string();
    let username = whoami::username();
    Ok(format!("{}:{}", hostname, username))
}
```

### File Layout

```
~/.config/my-cli/
├── config.toml              # Non-secret configuration
├── credentials.json         # Encrypted credentials (base64url encoded)
└── state.db                 # Local state (FrankenSQLite, etc.)
```

## Credential Data Structure

```rust
#[derive(Serialize, Deserialize)]
pub struct Credentials {
    pub access_token: String,
    pub refresh_token: Option<String>,
    pub expires_at: Option<DateTime<Utc>>,
    pub user_id: Option<String>,
    pub email: Option<String>,
}
```

## API Key as Alternative

For CI/CD and automation, users can bypass OAuth entirely:

```rust
// Set via command
fn set_api_key(key: &str) -> Result<()> {
    // Validate format
    // prefix_ (4 chars) + 64 hex chars = 68 total
    if !key.starts_with("jsm_") || key.len() < 68 {
        return Err(anyhow!("Invalid API key format"));
    }

    // Store as credentials (same storage, no refresh token)
    store_credentials(&Credentials {
        access_token: key.to_string(),
        refresh_token: None,
        expires_at: None,
        user_id: None,
        email: None,
    })
}
```

```bash
# Usage
export MY_CLI_API_KEY=jsm_abc123...
my-cli install some-package  # Uses API key from env

# Or persist
my-cli auth set-key jsm_abc123...
```

## Auth Resolution Order

When making API requests, resolve credentials in this order:

```rust
fn resolve_auth() -> Result<String> {
    // 1. Environment variable (highest priority — CI/CD use case)
    if let Ok(key) = std::env::var("MY_CLI_API_KEY") {
        return Ok(key);
    }

    // 2. Command-line flag (per-invocation override)
    if let Some(key) = cli_args.api_key.as_ref() {
        return Ok(key.clone());
    }

    // 3. Stored credentials (keyring or encrypted file)
    let creds = load_credentials()?;

    // 4. Auto-refresh if needed
    if needs_refresh(&creds) {
        let refreshed = refresh_token(&creds).await?;
        store_credentials(&refreshed)?;
        return Ok(refreshed.access_token);
    }

    Ok(creds.access_token)
}
```

## Security Checklist for Storage

- [ ] Tokens never written to stdout (only stderr for user messages)
- [ ] Credentials file has `0600` permissions (owner-only)
- [ ] Config directory has `0700` permissions
- [ ] Tokens masked in debug/trace logs: `jsm_abc...xyz`
- [ ] No credentials in shell history (use stdin or keyring, not args)
- [ ] Encrypted file not portable (machine-specific key derivation)
- [ ] Keyring access suppressed in non-interactive contexts
- [ ] API keys validated before storage (format check)
