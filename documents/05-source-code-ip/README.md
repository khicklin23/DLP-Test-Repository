# Source Code / IP Fixture

`proprietary_pricing_engine.py` (515 lines) is a fully synthetic but
functional Python codebase — a fictional "dynamic pricing & inventory
allocation engine" for the fictional Lakeside Outfitters Co. It's meant to
exercise **source-code DLP policies**: fingerprinting/exact-match detection
on internal repos, "Proprietary and Confidential" header/marking detection,
and secret-in-source-code scanning (it embeds a few fake API keys/DSNs, same
pattern as [`04-credentials-secrets`](../04-credentials-secrets)).

Good test scenarios with this file:

- Upload/attach to an external site (Google Drive, personal email, ChatGPT
  file upload) → should trigger source-code exfiltration policy.
- `git push` to a personal/external GitHub remote → should trigger git-based
  source-code policy.
- Paste a function or the whole file into an AI chat asking "can you refactor
  this" → should trigger AI/LLM data-leakage policy (see also
  [`08-ai-llm-mcp-security`](../08-ai-llm-mcp-security)).
- Copy into a personal note-taking app / pastebin-style tool.

It's runnable standalone (`python3 proprietary_pricing_engine.py`) so it also
works as a fixture for tools that only scan executed/interpreted content
rather than static text.
