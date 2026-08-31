from typing import Any, Dict, List, Optional

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
