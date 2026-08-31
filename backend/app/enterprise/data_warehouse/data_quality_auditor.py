import re
from typing import Any, Dict, List, Tuple

class DataQualityAuditor:
    @staticmethod
    def audit_contacts_cleanliness(contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(contacts)
        if total == 0:
            return {"total_records": 0, "cleanliness_score": 100.0, "issues": []}

        invalid_emails = 0
        missing_phones = 0
        missing_companies = 0
        duplicates = set()
        seen_emails = set()

        for c in contacts:
            email = (c.get("email") or "").lower().strip()
            if not email or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                invalid_emails += 1
            if email in seen_emails:
                duplicates.add(email)
            seen_emails.add(email)

            if not c.get("phone"):
                missing_phones += 1
            if not c.get("company_name") and not c.get("company_id"):
                missing_companies += 1

        defect_count = invalid_emails + missing_phones + missing_companies + len(duplicates)
        max_possible_defects = total * 4
        clean_pct = round(max(0.0, (1.0 - (defect_count / float(max_possible_defects)))) * 100.0, 1)

        return {
            "total_contacts_audited": total,
            "cleanliness_score_pct": clean_pct,
            "invalid_emails_count": invalid_emails,
            "missing_phones_count": missing_phones,
            "missing_companies_count": missing_companies,
            "duplicate_emails_count": len(duplicates),
            "data_grade": "A" if clean_pct >= 90 else "B" if clean_pct >= 75 else "C" if clean_pct >= 60 else "Poor"
        }
