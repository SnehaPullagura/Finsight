from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

class SLAMonitoringEngine:
    PRIORITY_TARGETS_HOURS = {
        "critical": {"first_response_hours": 1, "resolution_hours": 4},
        "high": {"first_response_hours": 2, "resolution_hours": 8},
        "medium": {"first_response_hours": 8, "resolution_hours": 24},
        "low": {"first_response_hours": 24, "resolution_hours": 72}
    }

    @staticmethod
    def evaluate_ticket_sla(
        created_at: datetime,
        priority: str,
        first_response_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        now = current_time or datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if first_response_at and first_response_at.tzinfo is None:
            first_response_at = first_response_at.replace(tzinfo=timezone.utc)
        if resolved_at and resolved_at.tzinfo is None:
            resolved_at = resolved_at.replace(tzinfo=timezone.utc)

        target = SLAMonitoringEngine.PRIORITY_TARGETS_HOURS.get(priority.lower(), SLAMonitoringEngine.PRIORITY_TARGETS_HOURS["medium"])
        resp_deadline = created_at + timedelta(hours=target["first_response_hours"])
        res_deadline = created_at + timedelta(hours=target["resolution_hours"])

        # Check response SLA
        if first_response_at:
            resp_breached = first_response_at > resp_deadline
            resp_status = "breached" if resp_breached else "met"
        else:
            resp_breached = now > resp_deadline
            resp_status = "breached" if resp_breached else "pending"

        # Check resolution SLA
        if resolved_at:
            res_breached = resolved_at > res_deadline
            res_status = "breached" if res_breached else "met"
        else:
            res_breached = now > res_deadline
            res_status = "breached" if res_breached else "in_progress"

        return {
            "priority": priority,
            "response_sla": {
                "target_hours": target["first_response_hours"],
                "deadline": resp_deadline.isoformat(),
                "status": resp_status,
                "is_breached": resp_breached
            },
            "resolution_sla": {
                "target_hours": target["resolution_hours"],
                "deadline": res_deadline.isoformat(),
                "status": res_status,
                "is_breached": res_breached
            },
            "overall_breached": resp_breached or res_breached
        }
