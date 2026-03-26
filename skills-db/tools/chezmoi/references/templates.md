# Chezmoi Advanced Templating

Complete reference for chezmoi's Go text/template system with sprig extensions.

## Template Basics

### When Templates Are Executed

A file is treated as a template when:
- Filename has `.tmpl` suffix (e.g., `dot_bashrc.tmpl`)
- File is in `.chezmoitemplates/` directory

### Template Syntax

```
{{ .chezmoi.hostname }}           # Variable access
{{ if condition }}...{{ end }}    # Conditionals
{{- ... -}}                       # Trim whitespace
{{ /* comment */ }}               # Comments
```

---

## Variables

### Built-in chezmoi Variables

```go
// System info
{{ .chezmoi.os }}              // darwin, linux, windows, freebsd
{{ .chezmoi.arch }}            // amd64, arm64, arm
{{ .chezmoi.hostname }}        // machine hostname
{{ .chezmoi.fqdnHostname }}    // fully qualified domain name
{{ .chezmoi.username }}        // current user
{{ .chezmoi.uid }}             // user ID
{{ .chezmoi.gid }}             // group ID
{{ .chezmoi.homeDir }}         // home directory path
{{ .chezmoi.cacheDir }}        // XDG cache directory
{{ .chezmoi.configFile }}      // chezmoi config file path
{{ .chezmoi.sourceDir }}       // chezmoi source directory
{{ .chezmoi.workingTree }}     // git working tree (if applicable)

// Kernel info (Linux)
{{ .chezmoi.kernel.osrelease }}
{{ .chezmoi.kernel.ostype }}
{{ .chezmoi.kernel.version }}

// OS Release info (Linux)
{{ .chezmoi.osRelease.id }}           // ubuntu, fedora, arch
{{ .chezmoi.osRelease.idLike }}       // debian, rhel
{{ .chezmoi.osRelease.name }}         // Ubuntu, Fedora
{{ .chezmoi.osRelease.version }}      // 22.04
{{ .chezmoi.osRelease.versionID }}    // 22.04
{{ .chezmoi.osRelease.versionCodename }}  // jammy
```

### View All Available Data

```bash
chezmoi data
chezmoi data --format=yaml
```

### Custom Data Sources

#### In Config File (`~/.config/chezmoi/chezmoi.toml`)

```toml
[data]
    email = "me@example.com"
    name = "My Name"
    
[data.work]
    enabled = true
    vpn = "work-vpn"
```

#### In Data Files (`.chezmoidata.toml`, `.chezmoidata.yaml`, `.chezmoidata.json`)

```toml
# ~/.local/share/chezmoi/.chezmoidata.toml
[packages]
    editors = ["nvim", "helix"]
    
[colors]
    primary = "#ff5500"
```

Access: `{{ .packages.editors }}`, `{{ .colors.primary }}`

---

## Conditionals

### Basic If/Else

```go
{{ if eq .chezmoi.os "darwin" }}
# macOS config
{{ else if eq .chezmoi.os "linux" }}
# Linux config
{{ else }}
# Other OS
{{ end }}
```

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `{{ if eq .chezmoi.os "darwin" }}` |
| `ne` | Not equal | `{{ if ne .chezmoi.arch "arm64" }}` |
| `lt` | Less than | `{{ if lt .version 10 }}` |
| `le` | Less or equal | `{{ if le .count 5 }}` |
| `gt` | Greater than | `{{ if gt .priority 3 }}` |
| `ge` | Greater or equal | `{{ if ge .level 2 }}` |

### Boolean Operators

```go
// AND - all conditions must be true
{{ if and (eq .chezmoi.os "linux") (eq .chezmoi.arch "amd64") }}
# 64-bit Linux only
{{ end }}

// OR - any condition can be true
{{ if or (eq .chezmoi.os "darwin") (eq .chezmoi.os "linux") }}
# Unix-like systems
{{ end }}

// NOT - negate condition
{{ if not .work.enabled }}
# Personal machine
{{ end }}

// Chained conditions
{{ if and (eq .chezmoi.os "linux") (ne .email "work@example.com") }}
# Linux personal machine
{{ end }}
```

### Checking for Existence

```go
// Check if variable exists
{{ if .email }}
email = "{{ .email }}"
{{ end }}

// Check if key exists in map
{{ if hasKey . "work" }}
# Work config available
{{ end }}
```

---

## Whitespace Control

### Problem: Unwanted Newlines

```go
{{ if eq .chezmoi.os "darwin" }}
export PATH="/opt/homebrew/bin:$PATH"
{{ end }}
```
Produces blank lines before/after the export.

### Solution: Trim Markers

```go
{{- if eq .chezmoi.os "darwin" }}
export PATH="/opt/homebrew/bin:$PATH"
{{- end }}
```

| Marker | Effect |
|--------|--------|
| `{{-` | Trim whitespace BEFORE |
| `-}}` | Trim whitespace AFTER |
| `{{- ... -}}` | Trim both sides |

### Script Shebang Fix

**Wrong** (causes "exec format error"):
```go
{{ if eq .chezmoi.os "linux" }}
#!/bin/bash
```

**Correct**:
```go
{{- if eq .chezmoi.os "linux" }}
#!/bin/bash
```

---

## Loops

### Range Over List

```go
{{ range .packages.editors }}
- {{ . }}
{{ end }}
```

### Range with Index

```go
{{ range $index, $editor := .packages.editors }}
{{ $index }}: {{ $editor }}
{{ end }}
```

### Range Over Map

```go
{{ range $key, $value := .colors }}
{{ $key }} = {{ $value }}
{{ end }}
```

---

## Functions

### String Functions (Sprig)

```go
{{ upper "hello" }}              // HELLO
{{ lower "HELLO" }}              // hello
{{ title "hello world" }}        // Hello World
{{ trim "  hello  " }}           // hello
{{ trimPrefix "hello" "hel" }}   // lo
{{ trimSuffix "hello" "lo" }}    // hel
{{ replace "foo" "bar" "foofoo" }} // barbar
{{ contains "ell" "hello" }}     // true
{{ hasPrefix "hel" "hello" }}    // true
{{ hasSuffix "lo" "hello" }}     // true
{{ quote "hello" }}              // "hello"
{{ squote "hello" }}             // 'hello'
```

### Path Functions

```go
{{ joinPath .chezmoi.homeDir ".config" "nvim" }}
// $HOME/.config/nvim

{{ base "/path/to/file.txt" }}   // file.txt
{{ dir "/path/to/file.txt" }}    // /path/to
{{ ext "file.txt" }}             // .txt
{{ clean "/path//to/../file" }}  // /path/file
```

### Execution Functions

```go
// Run command, get output
{{ output "hostname" "-f" }}

// Run command, get output as list (split by newlines)
{{ outputList "ls" "-1" }}

// Check if command exists
{{ if lookPath "brew" }}
# Homebrew available
{{ end }}

// Find executable in multiple paths
{{ findExecutable "python3" (list "/usr/bin" "/usr/local/bin") }}

// Find first available executable
{{ findOneExecutable (list "nvim" "vim" "vi") }}
```

### Data Format Functions

```go
// Parse formats
{{ $data := fromJson `{"key": "value"}` }}
{{ $data := fromToml `key = "value"` }}
{{ $data := fromYaml `key: value` }}

// Generate formats
{{ toJson .data }}
{{ toPrettyJson .data }}
{{ toToml .data }}
{{ toYaml .data }}

// INI files
{{ toIni .iniData }}
{{ $parsed := fromIni (include "config.ini") }}
```

### File Functions

```go
// Include another file's contents
{{ include "path/to/file" }}

// Include and execute as template
{{ template "partial" . }}
{{ includeTemplate "partial" . }}

// Glob files
{{ range glob "*.txt" }}
Found: {{ . }}
{{ end }}

// File info
{{ $info := stat "/path/to/file" }}
{{ $info.isDir }}
{{ $info.size }}
{{ $info.mode }}
```

### Environment Variables

```go
{{ env "HOME" }}
{{ env "EDITOR" | default "vim" }}

// All environment as map
{{ range $key, $value := .chezmoi.env }}
{{ $key }}={{ $value }}
{{ end }}
```

---

## Init Functions (Only During `chezmoi init`)

### Prompting for Input

```go
// In .chezmoi.toml.tmpl
[data]
    email = {{ promptString "Email address" | quote }}
    name = {{ promptString "Full name" "Default Name" | quote }}
    isWork = {{ promptBool "Is this a work machine" false }}
    priority = {{ promptInt "Priority level" 5 }}
```

### Choice Prompts

```go
    editor = {{ promptChoice "Preferred editor" (list "nvim" "vim" "emacs" "code") | quote }}
    
    // Multiple selections
    features = {{ promptMultichoice "Enable features" (list "git" "docker" "k8s") | toJson }}
```

### "Once" Variants (Only Prompt If Not Set)

```go
    email = {{ promptStringOnce . "email" "Email address" | quote }}
    // Won't re-prompt if .email already exists
```

### TTY Check

```go
{{ if stdinIsATTY }}
    email = {{ promptString "Email" | quote }}
{{ else }}
    email = "default@example.com"
{{ end }}
```

---

## Shared Templates (`.chezmoitemplates/`)

### Creating Reusable Partials

```
~/.local/share/chezmoi/.chezmoitemplates/
├── shell-aliases        # Shared shell aliases
├── git-config           # Git config partial  
└── ssh-hosts            # SSH host configs
```

### Using Shared Templates

```go
// In dot_bashrc.tmpl
{{ template "shell-aliases" . }}

// Pass custom data
{{ template "ssh-hosts" dict "hosts" .ssh.hosts "user" .username }}
```

### Template with Arguments

```go
// .chezmoitemplates/fontconfig
font_family: {{ .font }}
font_size: {{ .size }}

// Usage
{{ template "fontconfig" dict "font" "JetBrains Mono" "size" 14 }}
```

---

## Password Manager Functions

### 1Password

```go
{{ onepasswordRead "op://vault/item/field" }}
{{ (onepassword "item-name").password }}
{{ onepasswordDocument "document-name" }}
```

### Bitwarden

```go
{{ (bitwarden "item-name").login.password }}
{{ bitwardenAttachment "filename" "item-id" }}
{{ bitwardenSecrets "secret-id" }}
```

### pass

```go
{{ pass "path/to/secret" }}
{{ passRaw "path/to/secret" }}
{{ (passFields "path/to/secret").username }}
```

### Generic Secret Command

```go
// Configure in chezmoi.toml
[secret]
    command = "my-secret-tool"
    args = ["get"]

// Use in templates
{{ secret "secret-name" }}
{{ secretJSON "secret-name" | fromJson }}
```

---

## GitHub Functions

```go
// Get user's SSH keys
{{ range gitHubKeys "username" }}
{{ . }}
{{ end }}

// Get latest release
{{ (gitHubLatestRelease "owner/repo").TagName }}

// Get release asset URL
{{ gitHubLatestReleaseAssetURL "owner/repo" "asset-pattern" }}

// Get all tags
{{ range gitHubTags "owner/repo" }}
{{ .Name }}
{{ end }}
```

---

## Common Patterns

### OS-Specific PATH

```bash
# dot_bashrc.tmpl
{{- if eq .chezmoi.os "darwin" }}
export PATH="/opt/homebrew/bin:$PATH"
{{- else if eq .chezmoi.os "linux" }}
export PATH="$HOME/.local/bin:$PATH"
{{- end }}
```

### Conditional Package Installation Script

```bash
#!/bin/bash
# run_once_install-packages.sh.tmpl

{{- if eq .chezmoi.os "darwin" }}
brew bundle --file=/dev/stdin <<EOF
brew "ripgrep"
brew "fd"
{{- if .work.enabled }}
brew "awscli"
{{- end }}
EOF
{{- else if eq .chezmoi.os "linux" }}
sudo apt-get install -y ripgrep fd-find
{{- end }}
```

### Machine-Specific Git Config

```toml
# dot_gitconfig.tmpl
[user]
    name = {{ .name | quote }}
    email = {{ .email | quote }}
{{- if .git.signingKey }}
    signingkey = {{ .git.signingKey | quote }}

[commit]
    gpgsign = true
{{- end }}

{{- if eq .chezmoi.os "darwin" }}
[credential]
    helper = osxkeychain
{{- end }}
```

### Dynamic SSH Config

```
# private_dot_ssh/config.tmpl
{{- range .ssh.hosts }}
Host {{ .name }}
    HostName {{ .hostname }}
    User {{ .user | default $.chezmoi.username }}
    {{- if .port }}
    Port {{ .port }}
    {{- end }}
    {{- if .identityFile }}
    IdentityFile {{ .identityFile }}
    {{- end }}

{{ end -}}
```

---

## Debugging Templates

```bash
# Test template expression
chezmoi execute-template '{{ .chezmoi.os }}'

# Test entire template file
chezmoi execute-template < dot_bashrc.tmpl

# Show what a file would look like
chezmoi cat ~/.bashrc

# Verbose output shows template execution
chezmoi apply -v

# View all available data
chezmoi data
```

---

## Template Options

Configure in `~/.config/chezmoi/chezmoi.toml`:

```toml
[template]
    # Don't error on missing keys (default: error)
    options = ["missingkey=zero"]
    
    # Custom left/right delimiters
    leftDelimiter = "[["
    rightDelimiter = "]]"
```

---

## References

- [Go text/template docs](https://pkg.go.dev/text/template)
- [Sprig function reference](http://masterminds.github.io/sprig/)
- [chezmoi template reference](https://www.chezmoi.io/reference/templates/)
