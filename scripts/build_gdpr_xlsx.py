"""Generates the GDPR-category .xlsx fixture. Run: python3 scripts/build_gdpr_xlsx.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_xlsx import make_xlsx

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "documents", "10-gdpr-eu-personal-data")

HEADER = [
    "customer_id", "full_name", "eu_national_id", "date_of_birth", "email",
    "phone", "address", "city", "country", "special_category_flag",
    "marketing_consent", "payment_token_last4",
]

ROWS = [
    ["EU-CUST-2001", "Ines Marchetti", "IT-CF-MRCNSI89E63H501X", "1989-05-23", "ines.marchetti@example.com", "+39 02 0000 5581", "Via Roma 44", "Milano", "Italy", "religion:islam", "Y", "1111"],
    ["EU-CUST-2002", "Anders Solheim", "NO-FNR-23058900123", "1990-08-23", "anders.solheim@example.com", "+47 000 05582", "Karl Johans gate 12", "Oslo", "Norway", "trade_union:FNV", "Y", "4444"],
    ["EU-CUST-2003", "Selin Ostrowski", "PL-PESEL-89112505583", "1989-11-25", "selin.ostrowski@example.com", "+48 000 05583", "ul. Nowy Świat 8", "Warsaw", "Poland", "health:disability", "N", "0005"],
    ["EU-CUST-2004", "Tamsin Sokolov", "DE-STEUID-00000005584", "1992-02-14", "tamsin.sokolov@example.com", "+49 000 05584", "Unter den Linden 5", "Berlin", "Germany", "", "Y", "1117"],
    ["EU-CUST-2005", "Emiliano Vantongeren", "NL-BSN-000005585", "1988-07-30", "emiliano.vantongeren@example.com", "+31 000 05585", "Keizersgracht 241", "Amsterdam", "Netherlands", "health:pregnancy", "Y", "1881"],
    ["EU-CUST-2006", "Odalys Achebe", "FR-NIR-289055860012", "1995-03-09", "odalys.achebe@example.com", "+33 000 05586", "Rue de Rivoli 20", "Paris", "France", "", "N", "5100"],
    ["EU-CUST-2007", "Rhett Beaumont", "ES-DNI-00000587X", "1983-12-01", "rhett.beaumont@example.com", "+34 000 05587", "Gran Vía 30", "Madrid", "Spain", "religion:catholic", "Y", "1111"],
    ["EU-CUST-2008", "Zora Njoroge", "IE-PPSN-0000588AA", "1997-06-18", "zora.njoroge@example.com", "+353 000 05588", "O'Connell Street 10", "Dublin", "Ireland", "", "Y", "4444"],
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "eu-customer-database-export.xlsx")
    make_xlsx(out_path, HEADER, ROWS, sheet_name="EU Customers",
              title="EU Customer Database Export (Synthetic)")
    print(f"wrote {out_path}")
