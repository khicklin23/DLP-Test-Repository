"""Generates the financial/PCI-category .docx fixtures. Run: python3 scripts/build_financial_docx.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_docx import make_docx

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documents", "02-financial-pci")

payment_profiles = [
    ("h1", "SYNTHETIC TEST DATA"),
    ("p", "All card numbers are industry-standard published test PANs (never issued "
          "to a real cardholder). Names/addresses are fictional. Generated for "
          "Netskope One DLP (PCI-DSS) testing."),
    ("h1", "Lakeside Outfitters Co. — Stored Customer Payment Profiles (Export)"),
    ("p", "Export Source: payments_db.customer_cards   Export Date: 2026-02-05"),
    ("p", "CONFIDENTIAL — Cardholder Data Environment (CDE). Distribution restricted "
          "to PCI-scoped personnel only."),
    ("table", [
        ["Customer ID", "Name", "PAN", "Exp", "Billing ZIP", "Card Type"],
        ["CUST-10021", "Nadia Ferreira", "4111 1111 1111 1111", "09/28", "44011", "Visa"],
        ["CUST-10022", "Colton Marsh", "5555 5555 5555 4444", "11/27", "44102", "Mastercard"],
        ["CUST-10023", "Renata Okafor", "3782 822463 10005", "03/29", "44236", "Amex"],
        ["CUST-10024", "Jasper Lindqvist", "6011 1111 1111 1117", "07/26", "44070", "Discover"],
        ["CUST-10025", "Bianca Delacroix", "4012 8888 8888 1881", "05/28", "44115", "Visa"],
        ["CUST-10026", "Théo Whitfield", "5105 1051 0510 5100", "01/27", "44094", "Mastercard"],
        ["CUST-10027", "Priya Nakamura", "4111 1111 1111 1111", "12/26", "44060", "Visa"],
        ["CUST-10028", "Owen Kaczmarek", "3714 496353 98431", "02/28", "44107", "Amex"],
    ]),
    ("p", "Note: PANs stored here in plaintext for this export — production "
          "environment tokenizes PAN at rest per PCI-DSS Req. 3.4. This export "
          "exists specifically to test DLP detection of a PCI-DSS control failure "
          "scenario (plaintext PAN at rest / in transit)."),
    ("p", "Synthetic fixture — DLP testing only."),
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_docx(os.path.join(OUT_DIR, "customer-payment-profiles.docx"), payment_profiles,
              title="Customer Payment Profiles (Synthetic)")
    print("wrote customer-payment-profiles.docx")
