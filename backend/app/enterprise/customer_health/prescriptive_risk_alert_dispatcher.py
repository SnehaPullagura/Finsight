from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class PrescriptiveRiskAlertDispatcher:
    """
    Monitors leading indicators of churn (drop in daily active users, champion departure, support ticket spikes)
    and dispatches immediate prescriptive playbooks to CSMs.
    """
    @staticmethod
    def dispatch_health_triage(
        account: Dict[str, Any],
        dau_drop_pct: float,
        champion_departed: bool,
        sev2_ticket_count: int
    ) -> Dict[str, Any]:
        cname = account.get("name")
        arr = float(account.get("current_arr", 50000.0))

        risk_score = 0
        prescribed_steps = []

        if dau_drop_pct >= 30.0:
            risk_score += 40
            prescribed_steps.append(f"Usage down {dau_drop_pct}%: Schedule team workflow audit & re-enablement workshop.")

        if champion_departed:
            risk_score += 45
            prescribed_steps.append("Executive Champion Left: Identify secondary sponsor and initiate VIP onboarding.")

        if sev2_ticket_count >= 3:
            risk_score += 25
            prescribed_steps.append(f"{sev2_ticket_count} Active Support Tickets: Escalate to dedicated Solutions Architect.")

        if risk_score >= 65:
            priority = "URGENT_RED_ALERT"
        elif risk_score >= 35:
            priority = "WARNING_YELLOW_ALERT"
        else:
            priority = "HEALTHY_GREEN"

        return {
            "account_name": cname,
            "annual_recurring_revenue": arr,
            "composite_risk_score": min(100, risk_score),
            "alert_priority": priority,
            "prescribed_remediation_actions": prescribed_steps,
            "auto_assigned_csm": account.get("csm_name", "Lead CSM"),
            "dispatched_at": datetime.now(timezone.utc).isoformat()
        }
