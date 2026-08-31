from typing import Any, Dict, List, Optional

class SLAAutoRemediationService:
    @staticmethod
    def remediate_breached_ticket(ticket: Dict[str, Any], team_members: List[Dict[str, Any]]) -> Dict[str, Any]:
        tid = ticket.get("id")
        priority = (ticket.get("priority") or "medium").lower()

        # Elevate priority if not already critical
        new_priority = "critical" if priority in ["high", "medium"] else priority
        
        # Pick senior support engineer
        senior_engineers = [m for m in team_members if m.get("level") in ["Senior", "Lead", "Principal"]]
        assigned_to = senior_engineers[0] if senior_engineers else (team_members[0] if team_members else {})

        return {
            "ticket_id": tid,
            "previous_priority": priority,
            "escalated_priority": new_priority,
            "reassigned_to_id": assigned_to.get("id"),
            "reassigned_to_name": assigned_to.get("name"),
            "notification_action": "DISPATCH_URGENT_SLACK_ESCALATION",
            "remediation_status": "remediated"
        }
