from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class ExecutiveTelemetrySync:
    """
    Continuous telemetry sync aggregating feature adoption, active seat saturation,
    and API throughput across enterprise customer cohorts.
    """
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
