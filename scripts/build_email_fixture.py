"""
Generates a raw .eml fixture (RFC 822 message, multipart/mixed with a CSV
attachment) using only the stdlib `email` package, to test email-based DLP
(outbound mail scanning, attachment inspection). Run:
    python3 scripts/build_email_fixture.py
"""
import os
from email.message import EmailMessage

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "documents", "02-financial-pci",
    "customer-refund-request-with-attachment.eml"
)

BODY = """\
Hi Colton,

Following up on the refund request for the batch we closed out last week -
customer is disputing TXN-88214 (Mastercard ending 4444, $212.50). I've
pulled the relevant rows from the settlement export into the attached CSV so
Finance can process the reversal without needing system access.

Let me know once it's processed and I'll close the ticket.

Thanks,
Nadia

--
SYNTHETIC TEST DATA. This email and its attachment are fabricated for
Netskope One DLP testing (email + attachment exfiltration of cardholder
data). No real customer, transaction, or account is represented.
"""

ATTACHMENT_CSV = """txn_id,cardholder_name,pan,exp,card_type,amount,dispute_reason
TXN-88214,Colton Marsh,5555 5555 5555 4444,11/27,Mastercard,212.50,customer states charge not recognized
TXN-88213,Nadia Ferreira,4111 1111 1111 1111,09/28,Visa,84.20,related purchase same order
"""


def main():
    msg = EmailMessage()
    msg["Subject"] = "RE: Refund request - TXN-88214 dispute (customer callback)"
    msg["From"] = "Nadia Ferreira <nadia.ferreira@example.com>"
    msg["To"] = "Colton Marsh <colton.marsh@example.com>"
    msg["Cc"] = "finance-disputes@example.com"
    msg["Date"] = "Wed, 04 Feb 2026 15:22:10 -0500"
    msg["Message-ID"] = "<CAExample00000000000000000000000@mail.example.com>"
    msg.set_content(BODY)
    msg.add_attachment(
        ATTACHMENT_CSV.encode("utf-8"),
        maintype="text",
        subtype="csv",
        filename="dispute_txn_88214_cardholder_detail.csv",
    )

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        f.write(bytes(msg))
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
