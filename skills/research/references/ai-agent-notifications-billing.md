# AI agent notifications, SMS providers, and token billing research

Use this reference when a user asks for provider selection around agent/product notifications, SMS alternatives to Twilio, or usage/token billing for AI features.

## Decision frame

Start with the product architecture, not a provider beauty contest:

1. **Notification orchestration vs raw SMS**
   - If agents need to notify humans across email/SMS/push/chat/Slack/Teams/Discord/WhatsApp/in-app, evaluate a notification infrastructure layer first.
   - If only one or two transactional SMS paths are needed, a raw SMS provider may be enough.
2. **Payments vs usage ledger**
   - Keep an internal product usage ledger regardless of billing vendor.
   - Billing vendors are downstream sinks; do not make Stripe/Polar/Orb the only source of truth for model usage.
3. **Compliance**
   - For US A2P SMS over long codes, 10DLC registration is mandatory regardless of vendor.
   - Ask for brand, campaign/use-case, consent/opt-in, sample messages, opt-out wording, and number mapping before launch.

## Notification infrastructure options

### Courier

Best fit: managed omnichannel notification infrastructure for product and agent messaging.

Strengths:
- Email, SMS, push, chat, Slack, Teams, Discord, WhatsApp, in-app.
- Provider abstraction, routing/failover, templates, preferences, delivery logs, retries/throttling.
- Good fit when agents need to escalate/notify people across channels.

Tradeoffs:
- SaaS dependency and pricing.
- May be overkill for a single simple SMS path.

### Novu

Best fit: open-source/self-hostable notification infrastructure.

Strengths:
- In-app inbox plus email/SMS/push/chat workflows.
- Many provider integrations.
- Lower lock-in and easier to align with infra-control preferences.

Tradeoffs:
- Self-hosting/operations burden if not using cloud.
- Less polished as an enterprise managed notification layer than Courier/Knock.

### Knock

Best fit: B2B SaaS notification feeds, preferences, and workflow UX.

Strengths:
- Strong developer/product notification workflow experience.
- Good for in-app notification feed plus external channels.

Tradeoffs:
- SaaS-only and pricing floor can be higher.

## Raw SMS alternatives to Twilio

### Telnyx

Best default when the user asks for “better than Twilio” and the team can handle a slightly more technical provider.

Observed official pricing pattern from Telnyx messaging pricing page:
- US local/10DLC SMS around `$0.004` per message part plus carrier fees.
- MMS and toll-free have separate base rates plus carrier fees.
- Volume discounts at high monthly volume.

Strengths:
- Cost-effective, network/control story, voice/SIP/RCS/AI voice adjacencies.

Tradeoffs:
- Less universally familiar than Twilio; API/ecosystem may require more direct engineering attention.

### Plivo

Best fit when the team wants a Twilio-like SMS/voice API with lower cost/simpler migration.

Observed official pricing pattern from Plivo US SMS page:
- US long-code SMS around `$0.0077` per SMS plus carrier surcharges.
- Long-code number rental around `$0.50/month`.
- 10DLC pages emphasize mandatory brand/campaign registration and approval delays.

Strengths:
- Straightforward SMS/voice product surface; good migration candidate.

Tradeoffs:
- Often not as low-cost/control-oriented as Telnyx.

### Bandwidth / Sinch / Vonage / Bird

- **Bandwidth:** strong US carrier/enterprise path; usually a later-stage choice.
- **Sinch/Vonage/Bird:** useful for global omnichannel/WhatsApp/RCS/enterprise requirements; can be vendor-complex.

## AI token / usage billing options

### Internal usage ledger first

Create a product-owned event ledger before wiring billing deeply:

- `orgId` / `customerId`
- `model`
- `inputTokens`
- `outputTokens`
- `reasoningTokens` if available
- `feature` / `taskType`
- `taskId` / `runId` / checkpoint number
- idempotency key
- raw provider cost fields if useful
- billing export status / downstream vendor event IDs

This preserves auditability and allows changing Stripe/Polar/Orb later.

### Stripe

Best fit: fastest mainstream subscription launch and simple metered usage.

Useful facts:
- Stripe Meter Events support async usage reporting and require idempotency discipline.
- Stripe’s dedicated LLM token billing is documented as private preview; do not assume it is available.
- Good for subscriptions and simple overages; credit/wallet flows are possible but can get complex.

Recommendation pattern:
- Use Stripe for initial paid SaaS if already assumed by the repo.
- Avoid building a complex token-credit product directly against preview-only Stripe surfaces unless access is confirmed.

### Polar

Best fit: AI/software products selling credits, token packs, and top-ups with less billing/tax plumbing.

Useful facts:
- Polar usage meters can filter events and aggregate token-like fields.
- Polar credits can prepay usage; customer state / customer meters APIs can expose balances.
- Polar does not automatically block product usage at zero balance; the application must enforce balance checks.

Recommendation pattern:
- Prefer Polar when token packs/credits are central to v1 and merchant-of-record simplicity matters.

### Orb

Best fit: enterprise-grade usage billing and complex AI-agent pricing.

Useful facts:
- Orb’s AI agent pricing docs model monthly token allocations, top-ups, prepaid credits, checkpoint events, and idempotency keys.
- Strong when pricing varies by model, hardware, region, customer contract, or enterprise usage commitments.

Recommendation pattern:
- Use later when usage billing is itself a core business capability or enterprise contracts require it.
- Usually overkill for first deploy.

## Common recommendation for early SaaS/agent products

1. Launch payments with Stripe if already integrated.
2. Maintain internal usage events in the app database.
3. If prepaid AI credits/token packs are needed immediately, evaluate Polar before writing deep Stripe-specific credit logic.
4. Use Orb when usage billing becomes enterprise-grade or contract-heavy.
5. For notifications, choose Courier/Novu/Knock only when multi-channel routing/preferences/observability matter; otherwise keep direct email + one SMS provider.

## Source URLs to re-check before final recommendations

- Telnyx messaging pricing: https://telnyx.com/pricing/messaging
- Plivo US SMS pricing: https://www.plivo.com/sms/pricing/us/
- Plivo 10DLC overview: https://www.plivo.com/sms/10dlc/
- Courier notification infrastructure: https://www.courier.com/platform/notification-infrastructure
- Novu platform docs: https://docs.novu.co/platform
- Stripe LLM token billing: https://docs.stripe.com/billing/token-billing
- Stripe usage meter event API: https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage-api
- Polar meters: https://polar.sh/docs/features/usage-based-billing/meters
- Polar credits: https://polar.sh/docs/features/usage-based-billing/credits
- Orb AI agent pricing: https://docs.withorb.com/self-serve/agent-pricing
