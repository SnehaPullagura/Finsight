from typing import Any, Dict, List, Optional

class StakeholderCollaborationMatrix:
    """
    Multi-Threaded Stakeholder Buying Committee Matrix:
    Maps engagement depth across Economic Buyer, Technical Champion, Procurement, and InfoSec.
    """
    @staticmethod
    def assess_buying_committee_coverage(stakeholders: List[Dict[str, Any]]) -> Dict[str, Any]:
        roles_covered = set(s.get("committee_role") for s in stakeholders)
        required_roles = {"ECONOMIC_BUYER", "CHAMPION", "INFOSEC_SECURITY", "LEGAL_PROCUREMENT"}

        missing_roles = required_roles - roles_covered
        coverage_score = round(((len(required_roles) - len(missing_roles)) / len(required_roles)) * 100.0, 1)

        return {
            "total_stakeholders_engaged": len(stakeholders),
            "roles_represented": list(roles_covered),
            "missing_critical_roles": list(missing_roles),
            "committee_coverage_percentage": coverage_score,
            "is_single_threaded_risk": len(stakeholders) <= 1 or "ECONOMIC_BUYER" not in roles_covered,
            "deal_readiness": "MULTI_THREADED_DE_RISKED" if not missing_roles else "SINGLE_THREADED_VULNERABLE"
        }
