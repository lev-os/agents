# Monid installation

## Prerequisites

- Node and npm. The package is `@monid-ai/cli` (MIT). Latest on npm: 0.1.9
  (checked 2026-11-12 with `npm view`). The binary is `monid`.
- Install state on 2026-11-12: version 0.1.6 on the MacBook (`ssh kingly-macbook`);
  not installed on the Mac Studio. Read help there with
  `ssh kingly-macbook 'zsh -lc "monid <cmd> --help"'`.

## Install (only when the user asks)

```bash
npm install -g @monid-ai/cli
```

This skill update did not install anything.

## Credentials and verification

The key variable is `MONID_API_KEY`. It lives in the user's local env file.
Never print it. Free checks:

```bash
command -v monid
monid --version
monid whoami
monid balance
```

## Remove

`npm uninstall -g @monid-ai/cli`. This does not revoke the key.

Source: npm registry and `monid --help` on the MacBook, checked 2026-11-12.
