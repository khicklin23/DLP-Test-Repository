> **SYNTHETIC TEST DATA.** Every record in this folder, including
> `eu-customer-database-export.xlsx`, is fictional. Generated for Netskope
> One DLP testing of GDPR-scoped EU personal data (including Article 9
> "special category" data: health, religion/belief, trade union membership,
> biometric data).

# GDPR / EU Personal Data

- [`data-subject-access-request-response.md`](./data-subject-access-request-response.md) —
  a DSAR response package (Art. 15), the kind of document that names every
  category of personal data held on one individual in one place.
- [`special-category-employee-data.md`](./special-category-employee-data.md) —
  an internal HR register of Article 9 special category data.
- `eu-customer-database-export.xlsx` — bulk EU customer PII in spreadsheet
  form (national ID numbers formatted per-country, special-category flags),
  built via [`scripts/build_gdpr_xlsx.py`](../../scripts/build_gdpr_xlsx.py)
  using the stdlib [`gen_xlsx.py`](../../scripts/gen_xlsx.py) writer.

Good test scenarios: cross-border transfer (uploading to a non-EU cloud
service/AI tool), bulk-export-leaving-restricted-workspace, and Article 9
special-category-data policies that should be stricter than generic PII
policies.

---
*Synthetic fixture — DLP testing only.*
