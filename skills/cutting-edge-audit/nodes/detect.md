# Detect: Stack Discovery

Scan the entire repository to build a complete stack manifest.

## Steps

### 1. File Extension Survey
Glob for all file types in the repo. Count occurrences. Identify primary and secondary languages.

### 2. Package Manifests
Read all dependency/config files to identify frameworks and versions:
- `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` (Node/JS/TS)
- `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile` (Python)
- `Cargo.toml`, `Cargo.lock` (Rust)
- `go.mod`, `go.sum` (Go)
- `Gemfile`, `Gemfile.lock` (Ruby)
- `pom.xml`, `build.gradle`, `build.gradle.kts` (Java/Kotlin)
- `composer.json` (PHP)
- `*.csproj`, `*.sln` (C#/.NET)
- `pubspec.yaml` (Dart/Flutter)
- `mix.exs` (Elixir)
- `Package.swift` (Swift)

### 3. Framework Detection
From dependencies, identify specific frameworks and their versions:
- Frontend: React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit, Astro, etc.
- Backend: Express, FastAPI, Django, Rails, Actix, Gin, Phoenix, etc.
- Mobile: React Native, Flutter, SwiftUI, etc.
- Infrastructure: Docker, Terraform, Kubernetes, etc.

### 4. Architecture Scan
Identify patterns from directory structure:
- Monorepo vs single package
- API patterns (REST, GraphQL, gRPC, tRPC)
- Test framework(s) in use
- CI/CD configuration (GitHub Actions, etc.)
- Database/ORM setup

### 5. Version Detection
Pin exact versions for every major dependency. This is critical for the research step — "React best practices" is useless, "React 19.1 best practices 2026" is actionable.

## Output

Write a stack manifest to memory (do not create a file yet). Format:

```
PRIMARY LANGUAGES: [list with versions]
FRAMEWORKS: [list with exact versions]
BUILD TOOLS: [list]
TEST FRAMEWORKS: [list]
CI/CD: [what's configured]
ARCHITECTURE: [patterns detected]
DATABASE/ORM: [if applicable]
INFRA: [Docker, K8s, etc.]
```

Proceed to research with this manifest.
