# SELF-TEST: wrangler

Run from the skill directory.

## 1) Reference files exist
```bash
test -f references/COMMANDS.md
test -f references/CONFIG.md
test -f references/PAGES.md
```

## 2) Tool availability + version
```bash
command -v wrangler
wrangler --version
```

## 3) Core help output
```bash
wrangler --help | head -n 40
```

## 4) Subcommand sanity
```bash
wrangler d1 --help | head -n 20
wrangler r2 --help | head -n 20
```

Expected:
- `wrangler` is installed and responds to `--version`.
- Help output matches the commands listed in references/COMMANDS.md.
