from typing import Any, Dict, List, Optional

class ExpansionGovernanceGuard:
    @staticmethod
    def validate_expansion_prerequisites(account: Dict[str, Any]) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        open_sev1_tickets = int(account.get("open_sev1_tickets_count", 0))
        past_due_invoices = int(account.get("unpaid_invoices_count", 0))

        is_eligible = health >= 70 and open_sev1_tickets == 0 and past_due_invoices == 0

        return {
            "account_name": account.get("name"),
            "health_score": health,
            "open_sev1_tickets": open_sev1_tickets,
            "past_due_invoices": past_due_invoices,
            "is_expansion_eligible": is_eligible,
            "blocker_reason": "Sev 1 Support Ticket Pending" if open_sev1_tickets > 0 else "Unpaid Invoices Present" if past_due_invoices > 0 else "Sub-Optimal Health" if health < 70 else "None (Clear to Propose)"
        }
