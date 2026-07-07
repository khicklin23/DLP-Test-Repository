"""Generates the legal-category .docx fixtures. Run: python3 scripts/build_legal_docx.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_docx import make_docx

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documents", "06-legal-confidential")

term_sheet = [
    ("h1", "SYNTHETIC TEST DATA — FICTIONAL TRANSACTION"),
    ("p", "Generated for Netskope One DLP (M&A / legal confidential) testing. "
          "No relation to any real company or transaction."),
    ("h1", "STRICTLY CONFIDENTIAL — DRAFT TERM SHEET"),
    ("p", "Project Codename: \"Project Northstar\""),
    ("p", "Prepared for the Board of Directors of Lakeside Outfitters Co. — "
          "Do Not Distribute Beyond Authorized Recipients"),
    ("p", "Date: 2026-01-30"),
    ("h2", "Summary of Proposed Terms (Non-Binding, Subject to Definitive Agreement)"),
    ("table", [
        ["Term", "Detail"],
        ["Acquirer", "Meridian Outdoor Holdings, Inc."],
        ["Target", "Lakeside Outfitters Co."],
        ["Structure", "All-cash merger; Acquirer to form merger sub"],
        ["Purchase Price", "$412,000,000 enterprise value"],
        ["Per-Share Consideration", "$28.40 per share (est. 14.5M shares o/s)"],
        ["Financing", "$275M committed debt facility (Continental Trust Bank) + $137M cash on hand"],
        ["Exclusivity Period", "45 days from execution of this term sheet"],
        ["Break-Up Fee", "3.0% of enterprise value ($12.36M)"],
        ["Key Employee Retention", "Corinne Baptiste (CFO), Marcus Ilundu (Treasurer) — 2yr retention agreements"],
        ["Target Close Date", "2026-06-30, subject to HSR clearance"],
    ]),
    ("h2", "Key Conditions Precedent"),
    ("p", "1. Satisfactory completion of confirmatory due diligence, including review "
          "of Project Wayfinder pricing-engine IP and associated trade secrets."),
    ("p", "2. No material adverse change in Target's financial condition."),
    ("p", "3. Expiration or termination of the HSR Act waiting period."),
    ("p", "4. Retention agreements executed with identified key employees."),
    ("p", "5. Consent of Target's senior lender under existing credit facility."),
    ("h2", "Confidentiality"),
    ("p", "This term sheet is non-binding except for the Confidentiality, "
          "Exclusivity, and Governing Law sections, which are binding upon "
          "execution. Recipients agree not to disclose the existence or "
          "contents of this term sheet without prior written consent of both "
          "parties."),
    ("p", "Legal Counsel (Acquirer): Whitfield & Marsh LLP"),
    ("p", "Legal Counsel (Target): Reyes & Whitehorse Law Group"),
    ("p", "Synthetic fixture — DLP testing only."),
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_docx(os.path.join(OUT_DIR, "merger-acquisition-term-sheet.docx"), term_sheet,
              title="M&A Term Sheet (Synthetic)")
    print("wrote merger-acquisition-term-sheet.docx")
