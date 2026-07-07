# AGENTS.md — Working Notes for Agents on This Project

This file tracks where this project actually stands so any agent (or human)
picking it up mid-stream can continue without re-deriving context. **Update
this file as the project progresses** — treat it as a running log, not a
one-time doc. Add new entries under "Session Log" rather than rewriting
history.

## What this project is

`DLP-Test-Repository` (github.com/khicklin23/DLP-Test-Repository) is a
synthetic-data test fixture repo for evaluating **Netskope One** DLP
policies. Full explanation of purpose/categories is in [README.md](README.md)
— read that first. Short version: every file that looks sensitive (SSNs,
credit cards, patient records, credentials, source code, etc.) is fake,
generated specifically to give DLP policies realistic content to match
against, across scenarios like git push/pull exfiltration, AI/LLM data
leakage (pasting sensitive data into Claude/ChatGPT-style tools or an app
silently forwarding it to an AI API), MCP server/tool-call leakage, and the
standard PCI/HIPAA/PII/legal/export-control categories.

## Repo layout

```
README.md                     Full explanation of purpose + synthetic-data conventions
AGENTS.md                     This file
.gitignore                    Ignores __pycache__/*.pyc
documents/
  01-healthcare-hipaa/         PHI: patient intake record (md), lab results (docx),
                                mental health notes (md, 42 CFR Part 2 flavor),
                                insurance claim/EOB (md)
  02-financial-pci/            PCI: credit card batch export (md), ACH/wire log (md),
                                customer payment profiles (docx)
  03-pii-personal-data/        PII: customer contact database (md), employee master
                                list (docx, salary/SSN/bank acct)
  04-credentials-secrets/      API keys/tokens dump (md), leaked app config w/ DB
                                passwords (md), throwaway_test_key.pem (real
                                RSA keypair generated via openssl, never used for
                                anything, purely a PEM-shaped fixture)
  05-source-code-ip/           proprietary_pricing_engine.py — 515-line synthetic
                                but *runnable* Python codebase (fictional dynamic
                                pricing/inventory engine) with proprietary/trade-secret
                                headers and embedded fake credentials, for source-code
                                DLP + secret-in-code detection testing
  06-legal-confidential/       NDA (md), M&A term sheet (docx)
  07-export-control-itar/      Fictional ITAR/EAR-style marked technical data doc (md)
  08-ai-llm-mcp-security/      Prompt-leaking-secrets-to-AI chat transcript (md),
                                MCP server config with embedded credentials (json),
                                bulk-customer-PII-pasted-into-AI-chat export (md)
  09-bulk-data-exports/        master_sensitive_records.csv — 250-row synthetic
                                "master database" mixing every data class above
                                into one bulk export (good EDM/fingerprinting fixture)
  10-gdpr-eu-personal-data/    DSAR response (md), Art.9 special-category HR
                                register (md), EU customer export (xlsx, via
                                gen_xlsx.py)
  11-insider-threat-offboarding/ Resignation letter (md) + offboarding security
                                review (md) + bulk-download-audit-log.csv tying
                                together a departing employee's CRM export,
                                git clone/personal-remote push, and Drive/USB
                                exfil in one correlated timeline
  12-cicd-cloud-secrets/       GitHub Actions workflow (yml), Terraform .tfvars,
                                kubeconfig (yaml) — all with hardcoded fake
                                cloud credentials
  13-collaboration-chat-exports/ Slack channel export (json, conversations.history
                                shape) + Teams chat export (md) — PCI/PHI shared
                                informally in chat
scripts/
  gen_docx.py                  Stdlib-only (zipfile + hand-built OOXML) .docx
                                generator — no pip/pandoc available in this sandbox,
                                so this is how all .docx fixtures are made.
  gen_xlsx.py                  Same approach for .xlsx (single worksheet, inline
                                strings, no sharedStrings.xml needed)
  build_healthcare_docx.py     Each build_*.py script generates one category's
  build_financial_docx.py      binary fixture(s) by importing gen_docx.make_docx()
  build_pii_docx.py            or gen_xlsx.make_xlsx(). Re-run any of these to
  build_legal_docx.py          regenerate that category's fixture if you edit
  build_master_database.py     the content list/rows inside.
  build_gdpr_xlsx.py
  build_email_fixture.py       Builds the .eml fixture via stdlib `email` package
                                (multipart/mixed with a CSV attachment)
```

## Synthetic data conventions (already established — keep following these)

- **Names**: invented combinations, not modeled on real people.
- **SSNs**: format `000-XX-XXXX` (000 prefix is never issued by SSA) so
  values are guaranteed non-real while still matching standard SSN regexes.
- **Credit cards**: only the well-known, publicly published test PANs
  (Visa `4111111111111111`, Mastercard `5555555555554444`, Amex
  `378282246310005`, Discover `6011111111111117`, plus Visa
  `4012888888881881` and Mastercard `5105105105105100`) — Luhn-valid, never
  issued to a real cardholder. **Don't invent new card numbers** — reuse
  this set so there's no chance of coincidentally generating a real PAN.
- **Phones**: `(555) 016-XXXX` — NANP-reserved fictional block.
- **Emails/domains**: `example.com` — IANA-reserved for documentation/testing.
- **API keys/secrets**: realistic vendor-style prefixes (`sk_live_`, `AKIA`,
  `ghp_`, `sk-ant-`, etc.) with the word `EXAMPLE` or all-zeros worked into
  the body, always inert/non-functional.
- **Private key fixture**: `04-credentials-secrets/throwaway_test_key.pem` is
  a real key pair, generated locally with `openssl genpkey`, never
  registered/used anywhere — it exists purely so "does this look like a real
  PEM block" detectors have genuine structure to match.
- Every document carries a visible **"SYNTHETIC TEST DATA"** banner.
- A recurring fictional company (**Lakeside Outfitters Co.**) and cast of
  fictional people/vendors/law firms ties records together across
  categories (e.g. Corinne Baptiste appears as CFO in the PII, financial,
  and legal docs) so cross-document correlation testing is possible.

## Session Log

### 2026-07-06 — Initial build (this session)

- Cloned the (previously empty) GitHub repo into the local working directory.
- Wrote `README.md` explaining purpose/scope/categories/synthetic-data rules.
- Built the 9 category folders under `documents/` listed above, with a mix
  of Markdown, `.docx` (via the custom stdlib `gen_docx.py`), `.json`, `.csv`,
  and one `.pem`.
- Wrote `documents/05-source-code-ip/proprietary_pricing_engine.py` (515
  lines, syntactically valid, actually runs) as the source-code DLP fixture.
- Wrote `documents/09-bulk-data-exports/master_sensitive_records.csv` (250
  rows) as the "master database" bulk-export fixture.
- Wrote this `AGENTS.md`.
- **Not yet done**: nothing has been committed or pushed to GitHub — all
  work so far is uncommitted in the local working tree. The user hasn't
  asked for a commit/push yet; check with them before doing so per this
  project's normal workflow (commits/pushes require explicit ask).
- **Environment note**: this sandbox has no `pip`/`pandoc`/network package
  install available. `scripts/gen_docx.py` was built specifically to work
  around that (pure-stdlib OOXML writer). If a future session *does* have
  pip/pandoc, it's fine to keep using `gen_docx.py` anyway for consistency,
  or switch to `python-docx`/pandoc if richer formatting is needed.

### 2026-07-06 — Second pass: 4 more categories, xlsx generator, email fixture

- Added categories 10-13: GDPR/EU personal data, insider-threat/offboarding,
  CI/CD & cloud secrets, collaboration chat exports (see layout above).
- Built `scripts/gen_xlsx.py` (stdlib-only, same rationale as `gen_docx.py`)
  and used it for `10-gdpr-eu-personal-data/eu-customer-database-export.xlsx`.
- Built `scripts/build_email_fixture.py` using stdlib `email` package —
  produces `02-financial-pci/customer-refund-request-with-attachment.eml`,
  a multipart email with a CSV cardholder-data attachment.
- Updated `README.md` category table/structure to include 10-13.
- Committed and pushed to `origin/main` (first push required walking through
  GitHub secret-scanning push-protection "allow secret" flow for the fake
  Stripe key / Slack token in `04-credentials-secrets` and
  `08-ai-llm-mcp-security` — expected, since those files exist specifically
  to look like real leaked secrets. If adding more fake-secret-bearing files
  in future sessions, expect the same GitHub push-protection prompt and that
  the repo owner will need to click "allow" via the URL GitHub returns.)
- **Still not done**: none of the "policy test matrix" / results-tracking
  ideas below have been started.

## Ideas for what's next (not started — pick from these or propose new ones)

- More categories: source-code diffs (before/after a secret was added).
- More file formats: `.pdf`, `.pptx`.
- A scripted "policy test matrix" doc mapping each fixture file to the
  specific Netskope One policy/rule it's meant to trigger, plus expected
  verdict (block/alert/allow), so this becomes a real regression suite
  rather than just a pile of fixtures.
- Once real Netskope policies are being tested against this repo, record
  actual results/false-positive findings back into this file or a new
  `TESTING_LOG.md`.
