> **SYNTHETIC TEST DATA.** All data pasted into this simulated chat is
> fictional and generated for Netskope One DLP testing of "shadow AI" /
> AI-data-leakage scenarios — i.e., a user or application sending sensitive
> data to an AI provider's API (Anthropic, OpenAI, etc.) as part of a prompt.

# Simulated Chat Transcript — Employee Pastes Sensitive Data Into an AI Assistant

This simulates the DLP scenario where a well-meaning employee pastes
sensitive internal data into an AI chat UI (or an internal app silently
forwards it to an LLM API) to "get help," inadvertently sending it outside
the corporate boundary to a third-party AI provider.

---

**User:**

> Hey can you help me write a follow-up email to this patient? Here's their
> chart info:
>
> Patient: Marisol A. Reyes, DOB 1984-11-19, SSN 000-14-9273, MRN
> RFC-2026-004471. Diagnosis: G43.909 (migraine), E11.9 (T2 diabetes,
> screening). Insurance: Buckeye Mutual Health Plan, Member ID
> BMH-778213456. She's worried about her A1C results (6.9%, high) and wants
> to know if she needs to see an endocrinologist. Can you draft something
> reassuring but clear?

**Assistant (simulated):**

> I can help draft that email. Note: I'd recommend not including the
> patient's full SSN, MRN, or insurance member ID in a message drafted by an
> external AI tool — that data should stay within your EHR/patient portal
> system. Here's a draft that omits those identifiers...

---

**User (second example, different data class):**

> I'm getting a weird error connecting to our prod database, here's my
> config, can you spot the bug?
>
> ```
> DB_HOST=prod-db-01.internal.lakesideoutfitters.corp
> DB_USER=svc_app_prod
> DB_PASSWORD=Tr0ub4dor&3-Prod-2026!
> STRIPE_SECRET_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dcEXAMPLE00
> ```

**Assistant (simulated):**

> Before I look at the config — that password and the Stripe secret key
> should be rotated immediately, since they were just sent to an external
> AI service. For debugging, share the connection error and a redacted
> config with secrets replaced by placeholders instead.

---

## Why this file exists

This is exactly the pattern a DLP policy inspecting outbound traffic to
`api.anthropic.com`, `api.openai.com`, `chat.openai.com`, or similar
AI-service endpoints/domains should be able to catch: PHI, SSNs, and
plaintext credentials riding inside an otherwise innocuous-looking prompt
body (often JSON POST payloads to a chat completions / messages API).

See also [`mcp-server-config-with-credentials.json`](./mcp-server-config-with-credentials.json)
for the analogous MCP (Model Context Protocol) scenario, where secrets leak
via *tool configuration* rather than chat prompt text, and
[`ai-chat-export-with-customer-pii.md`](./ai-chat-export-with-customer-pii.md)
for a bulk customer-data leakage scenario.

---
*Synthetic fixture — DLP testing only.*
