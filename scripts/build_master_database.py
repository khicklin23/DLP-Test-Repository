"""
Generates documents/09-bulk-data-exports/master_sensitive_records.csv —
a large synthetic "master database" export mixing every sensitive data
class in this repo (PII, PHI, PCI, HR/financial) into one bulk file, since
that's a common real-world DLP scenario (a full customer/employee export
leaving via email, cloud sync, or upload).

All data is deterministic (seeded) and entirely fake. Credit card numbers
are drawn only from the small set of industry-standard published test PANs
(never issued to a real cardholder) rather than freshly generated numbers,
so there is no chance of coincidentally generating a real issued PAN.

Run: python3 scripts/build_master_database.py
"""
import csv
import os
import random

random.seed(20260706)

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "documents", "09-bulk-data-exports",
    "master_sensitive_records.csv"
)

FIRST_NAMES = [
    "Nadia", "Colton", "Renata", "Jasper", "Bianca", "Theo", "Priya", "Owen",
    "Aiyana", "Marcus", "Corinne", "Daniel", "Helena", "Tobias", "Kenji",
    "Marisol", "Ines", "Soren", "Amara", "Declan", "Yuki", "Freya", "Malik",
    "Simone", "Rosalind", "Elias", "Naomi", "Gideon", "Petra", "Lucian",
    "Odalys", "Rhett", "Selin", "Tamsin", "Anders", "Ophelia", "Cyrus",
    "Ingrid", "Emiliano", "Zora",
]
LAST_NAMES = [
    "Ferreira", "Marsh", "Okafor", "Lindqvist", "Delacroix", "Whitfield",
    "Nakamura", "Kaczmarek", "Whitehorse", "Ilundu", "Baptiste", "Reyes",
    "Voss", "Chen", "Fujimoto", "Solheim", "Adebayo", "Marchetti",
    "Kowalczyk", "Broussard", "Yamane", "Ostrowski", "Njoroge", "Beaumont",
    "Castellano", "Whitlock", "Anand", "Sokolov", "Vantongeren", "Achebe",
]
STREETS = [
    "Larkspur Ct", "Birchwood Dr", "Cedar Hollow Rd", "Prairie View Ln",
    "Harborview Ave", "Meadowlark St", "Sable Ridge Dr", "Windmill Pkwy",
    "Copperfield Way", "Tanglewood Ct", "Redstone Ave", "Foxglove Ln",
    "Willowbrook Ln", "Cliffside Dr", "Aspen Grove Way", "Bramblewood Ct",
]
CITIES_STATE_ZIP = [
    ("Springvale", "OH", "44011"), ("Elyria", "OH", "44102"),
    ("Medina", "OH", "44236"), ("Avon", "OH", "44070"),
    ("Cleveland", "OH", "44115"), ("North Ridgeville", "OH", "44094"),
    ("Amherst", "OH", "44060"), ("Vermilion", "OH", "44107"),
    ("Lorain", "OH", "44052"), ("Sheffield", "OH", "44054"),
    ("Oberlin", "OH", "44074"), ("Avon Lake", "OH", "44012"),
]
DEPARTMENTS = ["Retail Ops", "Warehouse", "Finance", "HR", "Clinical Affairs",
               "Engineering", "Marketing", "Legal", "IT", "Customer Success"]
ICD10_CODES = ["G43.909", "E11.9", "F41.1", "G47.00", "I10", "J45.909",
               "M54.5", "K21.9", "E78.5", "N/A"]
TEST_CARDS = [
    ("4111111111111111", "Visa"),
    ("5555555555554444", "Mastercard"),
    ("378282246310005", "Amex"),
    ("6011111111111117", "Discover"),
    ("4012888888881881", "Visa"),
    ("5105105105105100", "Mastercard"),
]

N_RECORDS = 250


def fmt_pan(pan: str) -> str:
    if len(pan) == 15:
        return f"{pan[:4]} {pan[4:10]} {pan[10:]}"
    return " ".join(pan[i:i + 4] for i in range(0, len(pan), 4))


def gen_row(i: int) -> dict:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    city, state, zip_code = random.choice(CITIES_STATE_ZIP)
    pan, card_type = random.choice(TEST_CARDS)
    dob_year = random.randint(1955, 2003)
    dob_month = random.randint(1, 12)
    dob_day = random.randint(1, 28)

    return {
        "record_id": f"REC-{100000 + i}",
        "full_name": f"{first} {last}",
        "date_of_birth": f"{dob_year:04d}-{dob_month:02d}-{dob_day:02d}",
        "ssn": f"000-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
        "phone": f"(555) 016-{random.randint(1000, 9999)}",
        "email": f"{first.lower()}.{last.lower()}{i}@example.com",
        "address": f"{random.randint(1, 999)} {random.choice(STREETS)}",
        "city": city,
        "state": state,
        "zip": zip_code,
        "credit_card_pan": fmt_pan(pan),
        "credit_card_type": card_type,
        "credit_card_exp": f"{random.randint(1,12):02d}/{random.randint(26,30)}",
        "bank_account_number": f"000{random.randint(100000000, 999999999)}",
        "bank_routing_number": "000123456",
        "medical_record_number": f"MRN-{200000 + i}",
        "primary_diagnosis_icd10": random.choice(ICD10_CODES),
        "insurance_member_id": f"BMH-{random.randint(100000000, 999999999)}",
        "employee_id": f"EMP-{1000 + i}",
        "department": random.choice(DEPARTMENTS),
        "annual_salary": random.choice([42000, 54100, 62400, 71500, 89750,
                                         98750, 121000, 145200, 168500, 212000]),
    }


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = list(gen_row(0).keys())
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(N_RECORDS):
            writer.writerow(gen_row(i))
    print(f"wrote {N_RECORDS} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
