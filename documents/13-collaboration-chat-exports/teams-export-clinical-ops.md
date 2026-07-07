> **SYNTHETIC TEST DATA.** All users, patients, and messages are fictional.
> Rendered to mimic a Microsoft Teams chat export. Generated for Netskope
> One DLP testing of PHI shared informally in collaboration tools.

# Microsoft Teams Export — "Clinical Ops Coordination" Group Chat

**Exported:** 2026-02-04 | **Members:** Aiyana Whitehorse, Helena Voss, Tobias Chen

---

**Aiyana Whitehorse** — 2026-02-03 9:14 AM
> Can someone double check the A1C result for Marisol Reyes (MRN
> RFC-2026-004471) before I call her back? System's showing 6.9% but she
> swears her last one was normal.

**Helena Voss** — 2026-02-03 9:16 AM
> Confirmed 6.9%, high. Also her SSN on file shows 000-14-9273 — that
> doesn't match what's in the insurance portal (ends differently), might be
> a data entry issue worth flagging to records.

**Aiyana Whitehorse** — 2026-02-03 9:18 AM
> Good catch, I'll submit a correction ticket. Calling her back now re: the
> A1C and possible endo referral.

**Tobias Chen** — 2026-02-03 11:40 AM
> Unrelated - reminder that Priya Nakamura's session notes from last week
> (F41.1, GAD-7 score 14) need co-signature by end of day, insurance is
> asking for documentation before they'll approve the psych referral.

**Helena Voss** — 2026-02-03 11:42 AM
> Signed off. Also - can we stop putting full patient names + MRNs in this
> chat? Compliance flagged our channel last quarter for exactly this. Use
> the ticket number only going forward, anyone can look up the rest in the
> EHR.

**Aiyana Whitehorse** — 2026-02-03 11:43 AM
> Fair, will do. Sorry, wanted to be fast turning around her callback.

---

## Why this file exists

This models the extremely common "fast informal coordination" PHI leak
pattern: clinicians aren't trying to violate HIPAA, they're trying to move
quickly, and informal chat tools end up holding identifiable patient data
outside the EHR's access controls and audit logging. A persistent,
searchable chat export like this is itself a HIPAA-scoped record once it
contains PHI, and needs the same DLP coverage as an actual EHR export.

---
*Synthetic fixture — DLP testing only.*
