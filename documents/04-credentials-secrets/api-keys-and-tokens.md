> **SYNTHETIC TEST DATA.** Every credential below is randomly generated,
> inert, and was never valid against any real service. Formats mimic real
> vendor key prefixes so pattern/entropy-based secret scanners have something
> realistic to match. Generated for Netskope One DLP (credential/secret
> exfiltration) testing.

# leaked_credentials_dump.txt — Example Secret Sprawl File

This simulates the kind of file that shows up pasted into a support ticket,
a Slack DM, a `.env` accidentally committed, or copy/pasted into an AI
chatbot for "help debugging."

```
# --- Cloud Provider ---
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# --- Payments ---
STRIPE_SECRET_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dcEXAMPLE00
STRIPE_WEBHOOK_SECRET=whsec_8f3e2b1c9d7a4f6e0b2c1d8a9f3e2b1cEXAMPLE

# --- Source Control ---
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2aEXMP
GITLAB_TOKEN=glpat-9f8e7d6c5b4a3f2e1d0c9EXMP

# --- Chat / Collab ---
SLACK_BOT_TOKEN=xoxb-000000000000-000000000000-EXAMPLEexampleexamplE0
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/EXAMPLEexampleexample00

# --- AI / LLM Providers (see also 08-ai-llm-mcp-security/) ---
ANTHROPIC_API_KEY=sk-ant-api03-EXAMPLE0000000000000000000000000000000000000000000000000000-EXMP
OPENAI_API_KEY=sk-proj-EXAMPLE00000000000000000000000000000000000000000000000000000000EXMP
GOOGLE_API_KEY=AIzaSyEXAMPLE00000000000000000000000

# --- Internal Services ---
INTERNAL_ADMIN_PASSWORD=CorrectHorseBattery!Staple2026
JWT_SIGNING_SECRET=8f0e3c1a9b7d6f4e2c0a8b6d4f2e0c8a6b4d2f0e8c6a4b2d0f8e6c4a2b0d8f6e
DB_ROOT_PASSWORD=Sup3rS3cretRootPW!2026
```

## Where this kind of file shows up in real incidents

- Accidentally committed `.env` file pushed to a public or personal GitHub repo
- Pasted into a ChatGPT/Claude/Copilot chat window asking "why isn't my AWS
  config working"
- Sent over Slack/Teams DM to a coworker for "quick debugging help"
- Attached to a support ticket or included in a bug report screenshot/log dump
- Sent to a third-party MCP tool/server as part of an agent's tool-call context

---
*Synthetic fixture — every value above is fake and inert. DLP testing only.*
