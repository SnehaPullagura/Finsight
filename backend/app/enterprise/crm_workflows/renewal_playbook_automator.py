from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseRenewalPlaybookAutomator:
    @staticmethod
    def generate_renewal_tasks(contract: Dict[str, Any], health_score: int) -> List[Dict[str, Any]]:
        cid = contract.get("id")
        end_date_str = contract.get("termination_date") or date.today().isoformat()
        end_date = date.fromisoformat(end_date_str)
        arr = float(contract.get("contract_value", {}).get("total_amount", 0.0))

        tasks = []
        # T-90 Days: Executive Business Review
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 90,
            "due_date": (end_date - timedelta(days=90)).isoformat(),
            "title": f"Schedule Executive Business Review (EBR) — ARR: ${arr:,.2f}",
            "priority": "high" if arr >= 100000 else "medium",
            "assigned_role": "Customer Success Manager"
        })

        # T-60 Days: Proposal & Uplift Proposal
        uplift_pct = 5.0 if health_score >= 80 else 0.0
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 60,
            "due_date": (end_date - timedelta(days=60)).isoformat(),
            "title": f"Draft Renewal Proposal with {uplift_pct}% Standard Uplift",
            "priority": "high",
            "assigned_role": "Account Executive"
        })

        # T-30 Days: Contract Execution & Legal Review
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 30,
            "due_date": (end_date - timedelta(days=30)).isoformat(),
            "title": "Secure Signed Renewal Agreement",
            "priority": "urgent",
            "assigned_role": "Account Executive"
        })

        return tasks
