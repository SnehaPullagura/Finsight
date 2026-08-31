import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/customer_health/prescriptive_risk_alert_dispatcher.py
    write_file("backend/app/enterprise/customer_health/prescriptive_risk_alert_dispatcher.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class PrescriptiveRiskAlertDispatcher:
    \"\"\"
    Monitors leading indicators of churn (drop in daily active users, champion departure, support ticket spikes)
    and dispatches immediate prescriptive playbooks to CSMs.
    \"\"\"
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
""")

    # 2. backend/app/enterprise/customer_health/executive_telemetry_sync.py
    write_file("backend/app/enterprise/customer_health/executive_telemetry_sync.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class ExecutiveTelemetrySync:
    \"\"\"
    Continuous telemetry sync aggregating feature adoption, active seat saturation,
    and API throughput across enterprise customer cohorts.
    \"\"\"
    @staticmethod
    def aggregate_cohort_telemetry(accounts_telemetry: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_accounts = len(accounts_telemetry)
        total_licensed_seats = sum(int(a.get("licensed_seats", 0)) for a in accounts_telemetry)
        total_active_users = sum(int(a.get("active_users_30d", 0)) for a in accounts_telemetry)

        seat_utilization = round((total_active_users / max(1, total_licensed_seats)) * 100.0, 1)

        return {
            "total_accounts_monitored": total_accounts,
            "total_enterprise_seats": total_licensed_seats,
            "active_30d_users": total_active_users,
            "portfolio_seat_saturation_pct": seat_utilization,
            "telemetry_health_rating": "EXCELLENT (> 85%)" if seat_utilization >= 85.0 else "HEALTHY (70%-85%)" if seat_utilization >= 70.0 else "UNDER_ADOPTED (< 70%)",
            "last_synced_at": datetime.now(timezone.utc).isoformat()
        }
""")

    print("Customer health suite created successfully.")

if __name__ == "__main__":
    run()
