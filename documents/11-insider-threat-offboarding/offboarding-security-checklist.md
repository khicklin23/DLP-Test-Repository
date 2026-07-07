> **SYNTHETIC TEST DATA.** Fictional employee/company. Generated for
> Netskope One DLP testing of insider-threat/departing-employee scenarios.

# IT Security — Employee Offboarding & Risk Review

**Employee:** Renata Okafor (EMP-0048, Regional Sales Director)
**Resignation Date Received:** 2026-01-20
**Last Day:** 2026-02-06
**Reviewed by:** IT Security — Marcus Ilundu

## Standard Offboarding Steps

- [x] Manager notified, transition plan requested
- [ ] Revoke SSO/Okta access — **scheduled for last day, 2026-02-06 17:00**
- [ ] Revoke VPN/remote access
- [ ] Disable badge access
- [ ] Collect company laptop
- [ ] Remove from Slack/Teams workspaces
- [ ] Remove from customer CRM and payment-profile systems (PCI scope)

## Pre-Departure Activity Review (flagged by DLP for security review)

Per standard practice, the two weeks between notice and last day are
reviewed for anomalous data activity. The following items were flagged and
routed to IT Security for manual review — **not yet confirmed as malicious**,
under investigation per standard offboarding procedure:

| Date | Activity | System | Volume | Flag Reason |
|---|---|---|---|---|
| 2026-01-22 | Bulk export | CRM (customer-contact-database) | 2,140 customer records | Volume 40x employee's typical weekly export |
| 2026-01-24 | Git clone | Internal source repo (`wayfinder-pricing-engine`) | Full repo, 1 commit before resignation letter submitted | Employee has no prior commit history in this repo |
| 2026-01-27 | Upload | Personal Google Drive (via browser, sanctioned-app-to-unsanctioned-instance) | 1 file, 340MB | Destination outside corporate Google Workspace tenant |
| 2026-01-29 | USB write | Local endpoint | 1 file, `customer_export_final.csv` | USB mass storage policy normally blocks this; exception was on file for a prior legitimate project (now revoked) |

## Recommended Actions

1. Accelerate access revocation to end of business today rather than last day.
2. Legal/HR to review employment agreement's confidentiality and non-solicit
   clauses given destination employer is a direct competitor.
3. Preserve audit logs and endpoint forensic image per retention policy
   pending Legal's decision on further action.

---
*Synthetic fixture — DLP testing only. See
[`bulk-download-audit-log.csv`](./bulk-download-audit-log.csv) for the full
log this table summarizes.*
