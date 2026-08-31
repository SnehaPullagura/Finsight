from typing import Any, Dict, List, Optional

class SalesQuotaManager:
    @staticmethod
    def calculate_team_rollups(reps_quotas: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_team_quota = sum(float(r.get("quota", 0.0)) for r in reps_quotas)
        total_team_attainment = sum(float(r.get("attained", 0.0)) for r in reps_quotas)
        team_pct = round((total_team_attainment / max(1.0, total_team_quota)) * 100.0, 2)

        return {
            "total_team_quota": round(total_team_quota, 2),
            "total_team_attainment": round(total_team_attainment, 2),
            "team_attainment_percentage": team_pct,
            "reps_count": len(reps_quotas)
        }
