import re
import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class MT940Statement(BaseModel):
    transaction_reference: str
    account_identification: str
    statement_number: str
    opening_balance: float
    closing_balance: float
    currency: str
    transactions: List[Dict[str, Any]]

class SwiftMT940Parser:
    """
    SWIFT MT940 Bank Statement Parser (Field :20:, :25:, :28C:, :60F:, :61:, :86:, :62F:)
    """
    @staticmethod
    def parse_mt940_text(content: str) -> MT940Statement:
        lines = content.splitlines()
        ref = "MT940-REF"
        account = "ACCOUNT-UNKNOWN"
        stmt_num = "1"
        currency = "INR"
        opening_bal = 0.0
        closing_bal = 0.0
        transactions: List[Dict[str, Any]] = []

        current_tx: Dict[str, Any] = {}

        for line in lines:
            line = line.strip()
            if line.startswith(":20:"):
                ref = line[4:].strip()
            elif line.startswith(":25:"):
                account = line[4:].strip()
            elif line.startswith(":28C:"):
                stmt_num = line[5:].strip()
            elif line.startswith(":60F:"):
                # :60F:C260801INR100000,00
                direction = line[5]
                date_str = line[6:12] # YYMMDD
                currency = line[12:15]
                amt_str = line[15:].replace(",", ".")
                try:
                    opening_bal = float(amt_str) * (1 if direction == "C" else -1)
                except ValueError:
                    opening_bal = 0.0
            elif line.startswith(":61:"):
                # :61:2608050805CD5000,00NTRFNONREF//12345
                if current_tx:
                    transactions.append(current_tx)
                    current_tx = {}
                date_str = line[4:10]
                cdt_dbt = line[10]
                match = re.search(r":61:\d{6}\d{0,4}([CD])([A-Z]?)(\d+[\,\.]\d{2})", line)
                if match:
                    d_c = match.group(1)
                    amt = float(match.group(3).replace(",", "."))
                    current_tx = {
                        "date": f"20{date_str[:2]}-{date_str[2:4]}-{date_str[4:6]}",
                        "amount": amt,
                        "type": "CREDIT" if d_c == "C" else "DEBIT",
                        "narration": "Bank Transfer"
                    }
            elif line.startswith(":86:") and current_tx:
                current_tx["narration"] = line[4:].strip()
            elif line.startswith(":62F:"):
                direction = line[5]
                amt_str = line[15:].replace(",", ".")
                try:
                    closing_bal = float(amt_str) * (1 if direction == "C" else -1)
                except ValueError:
                    closing_bal = opening_bal

        if current_tx:
            transactions.append(current_tx)

        return MT940Statement(
            transaction_reference=ref,
            account_identification=account,
            statement_number=stmt_num,
            opening_balance=opening_bal,
            closing_balance=closing_bal,
            currency=currency,
            transactions=transactions
        )
