"""Generates the PII-category .docx fixtures. Run: python3 scripts/build_pii_docx.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_docx import make_docx

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documents", "03-pii-personal-data")

employee_list = [
    ("h1", "SYNTHETIC TEST DATA"),
    ("p", "All names, SSNs, salaries, and addresses are fictional. Generated for "
          "Netskope One DLP (bulk PII / HR data) testing."),
    ("h1", "Lakeside Outfitters Co. — HR Employee Master List"),
    ("p", "HRIS Export Date: 2026-01-31   Classification: HR Confidential"),
    ("table", [
        ["Emp ID", "Full Name", "SSN", "DOB", "Home Address", "Title", "Annual Salary", "Bank Acct (Direct Deposit)"],
        ["EMP-0041", "Corinne Baptiste", "000-61-2201", "1987-08-27", "47 Redstone Ave, Oberlin, OH", "CFO", "$212,000", "000445566778"],
        ["EMP-0042", "Marcus Ilundu", "000-61-2202", "1970-05-19", "233 Tanglewood Ct, Sheffield, OH", "Treasurer", "$168,500", "000445566779"],
        ["EMP-0043", "Aiyana Whitehorse", "000-61-2203", "1982-10-08", "18 Copperfield Way, Lorain, OH", "VP Clinical Ops", "$174,300", "000445566780"],
        ["EMP-0044", "Tobias Chen", "000-61-2204", "1985-02-14", "9 Willowbrook Ln, Elyria, OH", "Sr. Clinician", "$98,750", "000445566781"],
        ["EMP-0045", "Helena Voss", "000-61-2205", "1979-11-30", "301 Cliffside Dr, Avon Lake, OH", "Medical Director", "$246,000", "000445566782"],
        ["EMP-0046", "Nadia Ferreira", "000-61-2206", "1990-04-12", "22 Larkspur Ct, Springvale, OH", "Store Manager", "$62,400", "000445566783"],
        ["EMP-0047", "Colton Marsh", "000-61-2207", "1985-09-30", "87 Birchwood Dr, Elyria, OH", "Warehouse Lead", "$54,100", "000445566784"],
        ["EMP-0048", "Renata Okafor", "000-61-2208", "1978-01-17", "145 Cedar Hollow Rd, Medina, OH", "Regional Sales Dir.", "$121,000", "000445566785"],
    ]),
    ("p", "This document contains Social Security Numbers, dates of birth, "
          "compensation data, and direct-deposit bank account numbers. Access "
          "restricted to HR and Payroll roles."),
    ("p", "Synthetic fixture — DLP testing only."),
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_docx(os.path.join(OUT_DIR, "employee-master-list.docx"), employee_list,
              title="HR Employee Master List (Synthetic)")
    print("wrote employee-master-list.docx")
