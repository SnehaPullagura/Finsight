"""
Double-Entry General Ledger Engine with Debit/Credit Balancing and Chart of Accounts.
"""
import enum
import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class AccountClassification(str, enum.Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

class LedgerEntryLine(BaseModel):
    account_code: str
    account_name: str
    classification: AccountClassification
    debit_amount: float = 0.0
    credit_amount: float = 0.0
    description: Optional[str] = None

class JournalEntry(BaseModel):
    entry_id: str
    date: datetime.date
    reference_number: str
    narration: str
    lines: List[LedgerEntryLine]
    is_posted: bool = True

class TrialBalanceAccount(BaseModel):
    account_code: str
    account_name: str
    classification: AccountClassification
    total_debits: float
    total_credits: float
    net_balance: float

class DoubleEntryLedgerEngine:
    @staticmethod
    def validate_journal_entry(entry: JournalEntry) -> bool:
        total_debits = sum(line.debit_amount for line in entry.lines)
        total_credits = sum(line.credit_amount for line in entry.lines)
        return abs(total_debits - total_credits) < 0.01

    @classmethod
    def generate_trial_balance(cls, entries: List[JournalEntry]) -> List[TrialBalanceAccount]:
        acc_map: Dict[str, Dict[str, Any]] = {}
        
        for e in entries:
            if not e.is_posted:
                continue
            for line in e.lines:
                if line.account_code not in acc_map:
                    acc_map[line.account_code] = {
                        "name": line.account_name,
                        "class": line.classification,
                        "debit": 0.0,
                        "credit": 0.0
                    }
                acc_map[line.account_code]["debit"] += line.debit_amount
                acc_map[line.account_code]["credit"] += line.credit_amount

        result = []
        for code, data in sorted(acc_map.items()):
            net = data["debit"] - data["credit"] if data["class"] in [AccountClassification.ASSET, AccountClassification.EXPENSE] else data["credit"] - data["debit"]
            result.append(TrialBalanceAccount(
                account_code=code,
                account_name=data["name"],
                classification=data["class"],
                total_debits=round(data["debit"], 2),
                total_credits=round(data["credit"], 2),
                net_balance=round(net, 2)
            ))
        return result
