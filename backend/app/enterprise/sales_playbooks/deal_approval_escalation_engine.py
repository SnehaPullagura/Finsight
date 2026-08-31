from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class DealApprovalEscalationEngine:
    @staticmethod
    def check_pending_approvals(pending_quotes: List[Dict[str, Any]], max_wait_hours: int = 24) -> List[Dict[str, Any]]:
        escalations = []
        now = datetime.now(timezone.utc)

        for q in pending_quotes:
            submitted_str = q.get("submitted_at")
            if not submitted_str:
                continue
            submitted_time = datetime.fromisoformat(submitted_str.replace("Z", "+00:00"))
            hours_elapsed = (now - submitted_time).total_seconds() / 3600.0

            if hours_elapsed >= max_wait_hours:
                escalations.append({
                    "quote_id": q.get("id"),
                    "deal_name": q.get("deal_name"),
                    "amount": q.get("total_amount"),
                    "hours_elapsed": round(hours_elapsed, 1),
                    "current_approver_role": q.get("current_approver_role", "Sales Director"),
                    "escalate_to_role": "VP of Sales / CRO",
                    "action": "TRIGGER_EXECUTIVE_SLACK_ESCALATION"
                })

        return escalations
