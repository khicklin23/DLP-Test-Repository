# DLP Test Repository

This repository is a **controlled test fixture set** for evaluating and tuning
the **various dlp engines**. Every
file in here containing "sensitive" data — SSNs, credit card numbers, patient
records, API keys, source code, etc. — is **entirely synthetic**. Nothing in
this repo identifies a real person, a real account, or a real system. See
[Synthetic Data Conventions](#synthetic-data-conventions) below for exactly how
fake data is generated so it's unmistakably fake to a human, while still
matching the formats/patterns real DLP engines look for.

## Purpose

Netskope One (and DLP platforms like it) inspect traffic and content across a
lot of different vectors: web uploads/downloads, email, endpoint file activity,
cloud app sync (OneDrive/Google Drive/Slack/etc.), git operations, and —
increasingly — traffic to AI/LLM services and MCP (Model Context Protocol)
tool calls. This repo exists to give those policies real content to react to,
so we can validate detection, tune false-positive/false-negative rates, and
build a regression suite before rolling policies out broadly.

Concretely, we're using this repo to experiment with scenarios like:

- **Git push/pull exfiltration** — sensitive files leaving the org via `git push`
  to a personal/external remote, or being pulled down from an untrusted repo.
- **Source code exfiltration** — proprietary/internal source code leaving via
  upload, email, clipboard, or copy into an external tool.
- **Shadow AI / AI data leakage** — pasting sensitive data into ChatGPT/Claude/
  Copilot-style web UIs, or an application sending sensitive data to an AI
  provider's API on a user's behalf.
- **MCP security** — MCP server configs and tool-call payloads that carry
  credentials or sensitive context to a local or remote MCP server/tool.
- **Standard DLP categories** — HIPAA/PHI, PCI/cardholder data, PII, credentials
  and secrets, legal/M&A confidential material, and export-controlled
  technical data.

The goal is a policy test suite: known-bad files that *should* trigger a
given policy, organized so it's obvious which policy/category each file is
meant to exercise.

## Repository Structure

```
documents/
  01-healthcare-hipaa/        Synthetic PHI: patient records, lab results, claims
  02-financial-pci/           Synthetic cardholder data, wire transfers, payment profiles, emailed dispute w/ attachment
  03-pii-personal-data/       Synthetic employee/customer PII (SSNs, DOB, addresses)
  04-credentials-secrets/     Fake API keys, DB connection strings, private keys
  05-source-code-ip/          Fake ~500-line proprietary codebase for source-code DLP
  06-legal-confidential/      Fake NDA, fake M&A term sheet
  07-export-control-itar/     Fake export-controlled technical data document
  08-ai-llm-mcp-security/     Fake AI-chat leakage, MCP server config w/ secrets
  09-bulk-data-exports/       "Master database" CSV mixing every data type at volume
  10-gdpr-eu-personal-data/   EU DSAR response, Article 9 special-category data, EU customer xlsx export
  11-insider-threat-offboarding/ Departing-employee exfiltration scenario (resignation → bulk export → audit log)
  12-cicd-cloud-secrets/      CI/CD & IaC configs with embedded cloud credentials (GitHub Actions, Terraform, kubeconfig)
  13-collaboration-chat-exports/ Slack/Teams-style exports with sensitive data shared informally
scripts/
  gen_docx.py                 Stdlib-only .docx generator used to build Word fixtures
  gen_xlsx.py                  Stdlib-only .xlsx generator used to build spreadsheet fixtures
  build_*.py                   One script per category that generates its binary fixtures
```

Each category folder generally contains the **same content in multiple
formats** (Markdown, `.docx`/`.xlsx`, `.json`/`.csv`/`.yaml`/`.eml`/`.py`)
since real exfiltration doesn't only happen in one file type, and different
DLP content inspectors (regex, exact-data-match, fingerprinting) behave
differently depending on format/encoding.

## Categories

| # | Category | What it tests |
|---|----------|----------------|
| 01 | Healthcare / HIPAA | PHI detectors: patient name+diagnosis+MRN combos, insurance claims |
| 02 | Financial / PCI-DSS | Cardholder data detectors: PAN + CVV + expiry, bank/ACH details, emailed attachments |
| 03 | PII / Personal Data | SSN, DOB, address, phone/email bulk PII |
| 04 | Credentials & Secrets | API keys, DB connection strings, private keys in plaintext files |
| 05 | Source Code / IP | Large proprietary-looking codebase for source-code fingerprinting |
| 06 | Legal / Confidential | NDA and M&A term sheet language, "Attorney-Client Privileged" markers |
| 07 | Export Control / ITAR | Controlled technical data markings (ITAR/EAR-style) |
| 08 | AI/LLM & MCP Security | Prompts/chat logs leaking secrets to an AI API, MCP config w/ credentials |
| 09 | Bulk Data Exports | A single large "master database" file mixing all the above at scale |
| 10 | GDPR / EU Personal Data | Article 9 special-category data, DSAR responses, cross-border EU PII |
| 11 | Insider Threat / Offboarding | Correlated exfiltration signals around a departing employee |
| 12 | CI/CD & Cloud Secrets | Hardcoded cloud credentials in pipeline/IaC/kubeconfig files |
| 13 | Collaboration Chat Exports | PHI/PCI/financial data shared informally in Slack/Teams |

## Synthetic Data Conventions

So results are meaningful (patterns should match real-world formats) while
staying unambiguously fake:

- **Names** are invented and not modeled on real people.
- **SSNs** use the `000-XX-XXXX` / clearly-invalid-block conventions or are
  otherwise randomly generated and not tied to any real person; every document
  is marked as synthetic.
- **Credit card numbers** use the industry-standard, publicly published
  **test PANs** (Visa `4111 1111 1111 1111`, Mastercard `5555 5555 5555 4444`,
  Amex `3782 822463 10005`, Discover `6011 1111 1111 1117`). These are
  Luhn-valid (so checksum-aware DLP engines fire) but are universally
  recognized test numbers, never issued to a real cardholder.
- **Phone numbers** use the `555-01XX` block, reserved by NANP for fictional
  use.
- **Emails/domains** use `example.com`/`example.org`, reserved by IANA for
  documentation and testing.
- **API keys/secrets** are randomly generated strings with realistic prefixes
  (e.g. `sk-`, `AKIA`) — inert and non-functional.
- Every document includes a visible **"SYNTHETIC TEST DATA"** banner.

## Status

See [AGENTS.md](AGENTS.md) for the current state of this project and what's
planned next — that file is kept up to date as work progresses so any agent
(or person) picking this up mid-stream can continue without re-deriving
context.
