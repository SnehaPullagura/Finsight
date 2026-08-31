from typing import Any, Dict, List, Optional

class CustomLegalClauseApprover:
    """
    Audits redlines and non-standard contract clauses (e.g. uncapped liability, non-compete, SLA indemnification).
    """
    RISK_LEVELS = {
        "UNCAPPED_INDEMNITY": {"risk": "CRITICAL", "approver": "GENERAL_COUNSEL_AND_CFO"},
        "NON_STANDARD_SLA_PENALTIES": {"risk": "HIGH", "approver": "VP_ENGINEERING_AND_LEGAL"},
        "NET_60_PAYMENT_TERMS": {"risk": "MEDIUM", "approver": "VP_FINANCE"},
        "CUSTOM_GOVERNING_LAW": {"risk": "LOW", "approver": "STAFF_LEGAL_COUNSEL"}
    }

    @classmethod
    def evaluate_clause_modifications(cls, requested_clauses: List[str]) -> Dict[str, Any]:
        highest_risk = "LOW"
        required_approvers = set()

        for c in requested_clauses:
            rule = cls.RISK_LEVELS.get(c, {"risk": "MEDIUM", "approver": "DEAL_DESK_DIRECTOR"})
            required_approvers.add(rule["approver"])
            if rule["risk"] == "CRITICAL":
                highest_risk = "CRITICAL"
            elif rule["risk"] == "HIGH" and highest_risk != "CRITICAL":
                highest_risk = "HIGH"

        return {
            "requested_clauses": requested_clauses,
            "overall_contract_risk": highest_risk,
            "required_approval_workflow": list(required_approvers),
            "is_auto_sign_eligible": highest_risk == "LOW",
            "contract_turnaround_sla_hours": 4 if highest_risk == "LOW" else 24 if highest_risk == "MEDIUM" else 72
        }
