> **SYNTHETIC TEST DATA.** Every field in `master_sensitive_records.csv` is
> fabricated by [`scripts/build_master_database.py`](../../scripts/build_master_database.py).
> No real individuals, accounts, or medical records are represented.

# Master Sensitive Records Export

`master_sensitive_records.csv` (250 rows) is a single bulk file that mixes
**every** sensitive data class covered elsewhere in this repo into one
export — SSN, DOB, address/phone/email (PII), credit card PAN/expiry (PCI),
bank account/routing (financial), MRN + ICD-10 diagnosis code (PHI), and
employee ID/salary/department (HR) — because that's a very common real-world
DLP scenario: a full database/warehouse export leaving via email attachment,
cloud storage sync, or upload to a third-party analytics/AI tool, rather than
one narrow document type.

Credit card numbers are drawn only from the small set of industry-standard
published test PANs (Visa/Mastercard/Amex/Discover) — never freshly
generated — so there is zero chance of coincidentally producing a real
issued card number.

## Regenerating / extending

```
python3 scripts/build_master_database.py
```

Edit the name/address pools or `N_RECORDS` in that script to produce a
larger or differently-shaped export. The generation is seeded
(`random.seed(20260706)`) so re-running produces identical output unless the
script itself changes.

This is a good fixture for testing **Exact Data Match (EDM)** / structured
fingerprinting DLP features in addition to plain pattern matching, since it's
a well-formed CSV with consistent column semantics across many rows.

---
*Synthetic fixture — DLP testing only.*
