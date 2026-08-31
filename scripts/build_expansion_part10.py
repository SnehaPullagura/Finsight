import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_workflows/lead_scoring_rule_processor.py
    write_file("backend/app/enterprise/crm_workflows/lead_scoring_rule_processor.py", """from typing import Any, Dict, List, Optional

class EnterpriseLeadScoringRuleProcessor:
    @staticmethod
    def evaluate_firmographic_fit(lead_record: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        reasons = []

        employees = int(lead_record.get("employee_count", 0))
        if employees >= 1000:
            score += 35
            reasons.append("Enterprise Tier 1: 1,000+ employees (+35 pts)")
        elif employees >= 250:
            score += 20
            reasons.append("Mid-Market Tier 2: 250-999 employees (+20 pts)")

        revenue = float(lead_record.get("annual_revenue", 0.0))
        if revenue >= 50000000.0:
            score += 35
            reasons.append("High ARR Company: $50M+ annual revenue (+35 pts)")
        elif revenue >= 10000000.0:
            score += 20
            reasons.append("Mid ARR Company: $10M-$50M annual revenue (+20 pts)")

        country = (lead_record.get("country") or "").upper()
        if country in ["US", "CA", "GB", "DE", "FR", "AU", "SG"]:
            score += 30
            reasons.append(f"Strategic Tier 1 Territory: {country} (+30 pts)")

        final_score = max(0, min(100, score))
        grade = "A" if final_score >= 80 else "B" if final_score >= 60 else "C" if final_score >= 40 else "D"

        return {
            "firmographic_score": final_score,
            "grade": grade,
            "is_sales_qualified": final_score >= 70,
            "scoring_reasons": reasons
        }
""")

    # 2. backend/app/enterprise/crm_workflows/quote_approval_matrix.py
    write_file("backend/app/enterprise/crm_workflows/quote_approval_matrix.py", """from typing import Any, Dict, List, Optional

class EnterpriseQuoteApprovalMatrix:
    @staticmethod
    def determine_approval_chain(quote_total: float, discount_pct: float, payment_terms: str) -> Dict[str, Any]:
        required_approvers = []
        sla_hours = 24

        # Discount threshold rules
        if discount_pct > 30.0:
            required_approvers.append({"role": "Chief Revenue Officer (CRO)", "priority": 1})
            sla_hours = 48
        elif discount_pct > 20.0:
            required_approvers.append({"role": "VP of Sales", "priority": 2})
        elif discount_pct > 10.0:
            required_approvers.append({"role": "Sales Director", "priority": 3})

        # Total value rules
        if quote_total >= 250000.0:
            if not any(a["role"] == "Chief Revenue Officer (CRO)" for a in required_approvers):
                required_approvers.append({"role": "VP of Sales", "priority": 2})

        # Non-standard payment terms
        if payment_terms.upper() in ["NET60", "NET90", "CUSTOM"]:
            required_approvers.append({"role": "Head of Finance / Controller", "priority": 2})

        requires_approval = len(required_approvers) > 0

        return {
            "quote_total": quote_total,
            "discount_percentage": discount_pct,
            "payment_terms": payment_terms,
            "requires_executive_approval": requires_approval,
            "approval_chain": sorted(required_approvers, key=lambda x: x["priority"]),
            "approval_sla_hours": sla_hours
        }
""")

    # 3. backend/app/enterprise/data_warehouse/data_quality_auditor.py
    write_file("backend/app/enterprise/data_warehouse/data_quality_auditor.py", """import re
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
""")

    print("Created lead scoring rule processor, quote approval matrix, and data quality auditor.")

if __name__ == '__main__':
    run()
