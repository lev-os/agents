# Bun Development

> Fast, modern JavaScript/TypeScript development with the Bun runtime.

## When to Use This Skill

* Starting new JS/TS projects with Bun
* Migrating from Node.js to Bun
* Optimizing development speed
* Using Bun's built-in tools (bundler, test runner)
* Troubleshooting Bun-specific issues

---

## 1. Getting Started

### Installation

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"

# Homebrew
brew tap oven-sh/bun && brew install bun

# Upgrade
bun upgrade
```

### Why Bun?

| Feature | Bun | Node.js |
|---------|-----|---------|
| Startup time | ~25ms | ~100ms+ |
| Package install | 10-100x faster | Baseline |
| TypeScript | Native | Requires transpiler |
| JSX | Native | Requires transpiler |
| Test runner | Built-in | External (Jest, Vitest) |
| Bundler | Built-in | External (Webpack, esbuild) |

---

## 2. Project Setup

### Create New Project

```bash
bun init

# With specific template
bun create react my-app
bun create next my-app
bun create vite my-app
bun create elysia my-api
```

### tsconfig.json (Bun-optimized)

```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "module": "esnext",
    "target": "esnext",
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "composite": true,
    "strict": true,
    "skipLibCheck": true,
    "jsx": "react-jsx",
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "allowJs": true,
    "types": ["bun-types"]
  }
}
```

---

## 3. Package Management

```bash
bun install              # Install from package.json
bun add express          # Regular dependency
bun add -d typescript    # Dev dependency
bun remove lodash        # Remove package
bun update               # Update all
bun outdated             # Check outdated
bunx prettier --write .  # Execute package binaries (npx equivalent)
bun install --frozen-lockfile  # Trust lockfile
```

---

## 4. Running Code

```bash
bun run index.ts         # Run TypeScript directly
bun run dev              # Run package.json script
bun --watch run index.ts # Watch mode
bun --hot run server.ts  # Hot reloading
```

### Environment Variables

```typescript
// .env file is loaded automatically
const apiKey = Bun.env.API_KEY;
const port = Bun.env.PORT ?? "3000";
```

---

## 5. Built-in APIs

### File System (Bun.file)

```typescript
const file = Bun.file("./data.json");
const text = await file.text();
const json = await file.json();
await Bun.write("./output.txt", "Hello, Bun!");
```

### HTTP Server (Bun.serve)

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/") return new Response("Hello World!");
    if (url.pathname === "/api/users") return Response.json([{ id: 1, name: "Alice" }]);
    return new Response("Not Found", { status: 404 });
  },
});
```

### WebSocket Server

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (server.upgrade(req)) return;
    return new Response("Upgrade failed", { status: 500 });
  },
  websocket: {
    open(ws) { ws.send("Welcome!"); },
    message(ws, message) { ws.send(`Echo: ${message}`); },
    close(ws) { console.log("Disconnected"); },
  },
});
```

### SQLite

```typescript
import { Database } from "bun:sqlite";
const db = new Database("mydb.sqlite");
db.run(`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE)`);
const insert = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
insert.run("Alice", "alice@example.com");
const user = db.prepare("SELECT * FROM users WHERE name = ?").get("Alice");
```

### Password Hashing

```typescript
const hash = await Bun.password.hash("super-secret");
const isValid = await Bun.password.verify("super-secret", hash);
```

---

## 6. Testing

```typescript
import { describe, it, expect } from "bun:test";

describe("Math operations", () => {
  it("adds two numbers", () => { expect(1 + 1).toBe(2); });
});
```

```bash
bun test                 # Run all tests
bun test math.test.ts    # Run specific file
bun test --watch         # Watch mode
bun test --coverage      # With coverage
```

---

## 7. Bundling

```bash
bun build ./src/index.ts --outdir ./dist --minify --sourcemap
```

### Compile to Executable

```bash
bun build ./src/cli.ts --compile --outfile myapp
bun build ./src/cli.ts --compile --target=bun-linux-x64 --outfile myapp-linux
```

---

## 8. Migration from Node.js

```bash
rm -rf node_modules package-lock.json
bun install
bun add -d @types/bun
```

### Differences from Node.js

```typescript
// Use import instead of require()
// Use import.meta.resolve() instead of require.resolve()
// Use Bun.nanoseconds() instead of process.hrtime()
// Use queueMicrotask() instead of setImmediate()
```

---

## 9. Performance Tips

- Use `Bun.file()` instead of `fs.readFile()` for faster I/O
- Use `Bun.serve()` instead of Express/Fastify for 4-10x faster HTTP
- Or use Elysia (Bun-optimized framework)
- Always bundle and minify for production

## Quick Reference

| Task | Command |
|------|---------|
| Init project | `bun init` |
| Install deps | `bun install` |
| Add package | `bun add <pkg>` |
| Run script | `bun run <script>` |
| Run file | `bun run file.ts` |
| Watch mode | `bun --watch run file.ts` |
| Run tests | `bun test` |
| Build | `bun build ./src/index.ts --outdir ./dist` |
| Execute pkg | `bunx <pkg>` |
