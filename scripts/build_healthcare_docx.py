"""Generates the healthcare-category .docx fixtures. Run: python3 scripts/build_healthcare_docx.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_docx import make_docx

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documents", "01-healthcare-hipaa")

lab_results = [
    ("h1", "SYNTHETIC TEST DATA — NOT A REAL PATIENT"),
    ("p", "Generated for Netskope One DLP policy testing (HIPAA/PHI detection). "
          "No relation to any real individual or lab."),
    ("h1", "Meridian Diagnostics Laboratory — Confidential Lab Results"),
    ("p", "Patient Name: Owen Kaczmarek"),
    ("p", "Date of Birth: 1976-03-22"),
    ("p", "Social Security Number: 000-31-5567"),
    ("p", "Medical Record Number: MDL-2026-778102"),
    ("p", "Ordering Physician: Dr. Helena Voss, MD (NPI 0000287341)"),
    ("p", "Collection Date: 2026-01-15   Report Date: 2026-01-17"),
    ("h2", "Comprehensive Metabolic Panel"),
    ("table", [
        ["Test", "Result", "Reference Range", "Flag"],
        ["Glucose", "142 mg/dL", "70-99 mg/dL", "HIGH"],
        ["BUN", "18 mg/dL", "7-20 mg/dL", ""],
        ["Creatinine", "1.0 mg/dL", "0.6-1.3 mg/dL", ""],
        ["Sodium", "139 mmol/L", "136-145 mmol/L", ""],
        ["Potassium", "4.3 mmol/L", "3.5-5.1 mmol/L", ""],
    ]),
    ("h2", "Hemoglobin A1C"),
    ("table", [
        ["Test", "Result", "Reference Range", "Flag"],
        ["Hemoglobin A1C", "6.9 %", "<5.7 %", "HIGH"],
    ]),
    ("h2", "HIV / Hepatitis Panel (Sensitive)"),
    ("table", [
        ["Test", "Result"],
        ["HIV 1/2 Ag/Ab Combo", "Non-Reactive"],
        ["Hepatitis C Antibody", "Non-Reactive"],
        ["Hepatitis B Surface Antigen", "Non-Reactive"],
    ]),
    ("p", "Clinical Impression: Results consistent with new-onset Type 2 Diabetes "
          "Mellitus. Recommend endocrinology referral and lifestyle counseling."),
    ("p", "Reviewed and released by: Dr. Helena Voss, MD — 2026-01-17"),
    ("p", "This report contains Protected Health Information (PHI), including "
          "communicable disease test results subject to additional state-law "
          "confidentiality protections. Synthetic fixture — DLP testing only."),
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_docx(os.path.join(OUT_DIR, "lab-results-confidential.docx"), lab_results,
              title="Confidential Lab Results (Synthetic)")
    print("wrote lab-results-confidential.docx")
