from typing import Any, Dict, List, Optional

class RepWorkloadCapacityBalancer:
    """
    Monitors rep active opportunities and pipeline workload capacity.
    """
    @staticmethod
    def audit_rep_bandwidth(
        reps_load: List[Dict[str, Any]],
        max_active_deals_threshold: int = 25
    ) -> List[Dict[str, Any]]:
        results = []
        for r in reps_load:
            name = r.get("rep_name")
            active_deals = int(r.get("active_deals_count", 0))
            active_pipe = float(r.get("active_pipeline_amount", 0.0))
            quota = float(r.get("quarterly_quota", 250000.0))

            utilization_pct = round((active_deals / max(1, max_active_deals_threshold)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "active_deals_count": active_deals,
                "active_pipeline_amount": active_pipe,
                "capacity_utilization_pct": utilization_pct,
                "bandwidth_status": "OVERLOADED (> 100%)" if utilization_pct > 100.0 else "OPTIMAL_BANDWIDTH (70%-100%)" if utilization_pct >= 70.0 else "UNDERUTILIZED (< 70%)",
                "can_accept_new_inbound": utilization_pct <= 90.0
            })

        return sorted(results, key=lambda x: x["capacity_utilization_pct"], reverse=True)
