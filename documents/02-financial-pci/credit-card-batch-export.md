> **SYNTHETIC TEST DATA.** All card numbers below are industry-standard,
> publicly published **test PANs** used by payment processors for
> integration testing (Visa/Mastercard/Amex/Discover). They are Luhn-valid
> but have never been issued to a real cardholder. Names/addresses are
> fictional. Generated for Netskope One DLP (PCI-DSS/cardholder data) testing.

# Merchant Batch Settlement Export — batch_20260204_close.csv (rendered)

**Merchant:** Lakeside Outfitters Co.
**Merchant ID:** 9004471123
**Acquiring Bank:** First Continental Merchant Services
**Batch Date:** 2026-02-04
**Terminal ID:** TERM-0042

| Txn ID | Cardholder Name | PAN | Exp | CVV | Card Type | Amount | Auth Code |
|---|---|---|---|---|---|---|---|
| TXN-88213 | Nadia Ferreira | 4111 1111 1111 1111 | 09/28 | 123 | Visa | $84.20 | A0K3F9 |
| TXN-88214 | Colton Marsh | 5555 5555 5555 4444 | 11/27 | 456 | Mastercard | $212.50 | B1L4G0 |
| TXN-88215 | Renata Okafor | 3782 822463 10005 | 03/29 | 4321 | Amex | $1,045.00 | C2M5H1 |
| TXN-88216 | Jasper Lindqvist | 6011 1111 1111 1117 | 07/26 | 789 | Discover | $58.99 | D3N6I2 |
| TXN-88217 | Bianca Delacroix | 4012 8888 8888 1881 | 05/28 | 234 | Visa | $340.10 | E4O7J3 |
| TXN-88218 | Théo Whitfield | 5105 1051 0510 5100 | 01/27 | 567 | Mastercard | $19.99 | F5P8K4 |

**Batch Totals:** 6 transactions, $1,760.78 gross, $1,724.36 net after
interchange fees.

## Bank Deposit Detail

| Field | Value |
|---|---|
| Depository Account Name | Lakeside Outfitters Co. Operating Account |
| Bank Routing Number (ABA) | 000123456 |
| Bank Account Number | 000456789012 |
| Deposit Reference | DEP-2026-020400471 |

---
*Contains cardholder data (PAN, CVV, expiration) subject to PCI-DSS. Synthetic
fixture — DLP testing only. Do not use these test PANs for anything other
than DLP pattern-matching validation.*
