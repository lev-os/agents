# BrowserSkill (bsk) installation

## Runtime and checks

`bsk` is a host binary with a local daemon and a browser extension. It supports
macOS, Linux and Windows, and Chromium browsers (Chrome, Brave, Edge). The
official installers put the binary in `~/.local/bin` (`BSK_INSTALL_DIR` changes
that).

```bash
command -v bsk
bsk --version
bsk update --check --json     # status "up_to_date", or the newer version
bsk doctor                    # daemon, protocol, extension, auto-update
bsk browsers --json           # each connected profile: instance_id, label, extension_version
```

These checks change nothing. `version_skew: true` on a browser means the
extension and the CLI differ: update both.

## Install

Follow the official guide on the agent's machine:
<https://github.com/Tencent/BrowserSkill/blob/main/AGENT_INSTALL.md>. It covers
the CLI installer and the extension. Do not install a package with a similar
name from another source. Record the version and the executable path.

The user connects the extension in each browser profile they want to use, then
copies that profile's instance ID from the extension popup. An agent does not
install the extension or change its Automation settings.

## Credentials

None. `bsk` uses the sign-ins that already exist in the user's browser profile.
A sign-in, a one-time code or a CAPTCHA is the user's step
(`bsk request-help`).

## Update

```bash
bsk update --check --json
bsk update            # installs the newer CLI and restarts the daemon
```

`bsk update` restarts the shared daemon, which ends other agents' sessions. Run
`bsk session list --json` first, and update only inside a requested maintenance
scope. The daemon also updates itself (`bsk doctor` shows the last auto-update).

## Agent skill

`bsk install-skill` writes the bundled `browser-skill` skill into agent hosts.
On this machine the skill in `~/.agents/skills/browser-skill` is a custom copy
with automatic updates off; do not overwrite it without the user's request.

## Verification

A session that starts on the named instance and stops cleanly:

```bash
bsk session start --browser <instance-id> --json
bsk session stop <session_id>
bsk session list --json       # []
```

A version check does not prove that a profile is connected or signed in.

## Remove

Remove the recorded binary and the extension from each browser profile. Stop
sessions first. Leave other agents' sessions and the user's browser data alone.

Source: `bsk --help`, `bsk update --help`, `bsk doctor` (CLI 0.4.2) and the
browser-skill `references/environment.md`, checked 2026-11-10.
