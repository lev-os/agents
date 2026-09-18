# SuntiQ authentication identities

Use AgentMail as the owned email/OTP surface, Clerk as the identity and session authority, and Convex as the tenant and role authority. Do not derive access from the email address itself.

## Credential custody

- Store the AgentMail key in machine-local `~/.env.suntiq`, mode `0600`, outside Git and chezmoi.
- Source that file after `~/.env.local`; product wrappers also load it directly for non-login agent processes.
- Use lane-specific Clerk variable names; never put a live staging key in the generic local `CLERK_SECRET_KEY` environment.
- Prefer a read-only, inbox-scoped AgentMail key for testing and a separate narrowly scoped key only if setup must create inboxes.

## Persona setup

Create explicit local and staging Clerk identities, then provision their exact tenant, location, vessel, and role memberships in Convex. Keep production App Review credentials separate.

Proposed addresses such as `suntiq+owner@agentmail.to`, `suntiq+manager@agentmail.to`, and `suntiq+operator@agentmail.to` must pass an inbound-routing probe before use. Send a unique message to each address and verify the delivered recipient and inbox. If AgentMail does not support plus aliases, use separate inboxes or a verified custom-domain routing rule.

## Automated sign-in

Use the product's real email-code path:

1. Start a fresh Clerk sign-in for the persona address.
2. Poll only that persona's verified inbox boundary.
3. Read the newest matching Clerk message and extract the one-time code in memory.
4. Submit it to the active device/browser session.
5. Assert the Clerk subject and Convex role/location scope, run the journey, then sign out and clean up disposable state.

Never log the OTP, persist it in a receipt, bypass verified email, or reuse a personal Google/passkey session.
