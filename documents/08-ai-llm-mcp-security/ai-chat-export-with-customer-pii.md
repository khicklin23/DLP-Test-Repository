> **SYNTHETIC TEST DATA.** All customer data is fictional. Generated for
> Netskope One DLP testing of bulk-PII-via-AI-chat leakage scenarios.

# Exported AI Chat History — "Help Me Analyze Churn Risk" (bulk PII pasted)

Simulates an exported conversation log (the kind of file that gets saved
locally, emailed to a manager for review, or synced to cloud storage) where
an employee pasted a bulk customer export into an AI chat to ask for
analysis — a very common shadow-AI pattern that moves data class boundaries
without going through any sanctioned data pipeline or DPA-covered vendor.

---

**Conversation Title:** Help me find our highest churn-risk customers
**Exported:** 2026-02-06 14:32 UTC
**Platform:** (generic AI chat web UI — simulated)

**User:**

> I have our customer list with contact info and purchase history, can you
> help me figure out who's most likely to churn? Here's the data:
>
> ```
> CUST-10021, Nadia Ferreira, nadia.ferreira@example.com, (555) 016-3341, 000-55-1029, Gold, last_purchase=2025-08-02
> CUST-10022, Colton Marsh, colton.marsh@example.com, (555) 016-3342, 000-55-1030, Silver, last_purchase=2025-11-19
> CUST-10023, Renata Okafor, renata.okafor@example.com, (555) 016-3343, 000-55-1031, Platinum, last_purchase=2026-01-28
> CUST-10024, Jasper Lindqvist, jasper.lindqvist@example.com, (555) 016-3344, 000-55-1032, Bronze, last_purchase=2025-06-14
> CUST-10025, Bianca Delacroix, bianca.delacroix@example.com, (555) 016-3345, 000-55-1033, Gold, last_purchase=2025-09-30
> ```
>
> Also can you draft a win-back email for the ones who haven't purchased in
> 6+ months?

**Assistant (simulated):**

> I can help with the churn analysis approach, but a couple of flags first:
> this data includes full SSNs, which have no bearing on churn prediction
> and shouldn't have been included — and pasting a customer list with SSNs
> into an external AI chat sends regulated PII outside your company's
> environment. For the analysis itself, purchase recency and tier alone are
> enough: Ferreira, Lindqvist, and Delacroix all show 6+ months since last
> purchase and are good win-back candidates...

---

## Why this file exists

This models the "well-intentioned analyst" shadow-AI leak: no malicious
intent, but a bulk PII export (SSNs included, unnecessarily) crossed into an
AI chat tool that may not be covered by the company's data processing
agreements. This is one of the highest-value DLP catches for AI-focused
policies because it's *common* — not an edge case.

---
*Synthetic fixture — DLP testing only.*
