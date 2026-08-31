from typing import Any, Dict, List, Optional
from collections import defaultdict

class SalesQuotaAttainmentCube:
    @staticmethod
    def calculate_hierarchy_attainment(rep_quotas: List[Dict[str, Any]]) -> Dict[str, Any]:
        team_rollups = defaultdict(lambda: {"quota": 0.0, "closed": 0.0, "pipeline": 0.0, "reps": []})

        for r in rep_quotas:
            team = r.get("team_name", "Global Sales")
            quota = float(r.get("quota_target", 0.0))
            closed = float(r.get("closed_revenue", 0.0))
            pipe = float(r.get("open_pipeline", 0.0))

            team_rollups[team]["quota"] += quota
            team_rollups[team]["closed"] += closed
            team_rollups[team]["pipeline"] += pipe
            team_rollups[team]["reps"].append({
                "rep_id": r.get("rep_id"),
                "rep_name": r.get("rep_name"),
                "quota": quota,
                "closed": closed,
                "attainment_pct": round((closed / max(1.0, quota)) * 100.0, 1)
            })

        teams_summary = []
        company_quota = 0.0
        company_closed = 0.0
        company_pipeline = 0.0

        for tname, stats in team_rollups.items():
            t_quota = stats["quota"]
            t_closed = stats["closed"]
            t_pipe = stats["pipeline"]
            pct = round((t_closed / max(1.0, t_quota)) * 100.0, 1)
            coverage = round((t_pipe / max(1.0, t_quota - t_closed)), 2) if t_quota > t_closed else 99.0

            company_quota += t_quota
            company_closed += t_closed
            company_pipeline += t_pipe

            teams_summary.append({
                "team_name": tname,
                "total_quota": round(t_quota, 2),
                "total_closed": round(t_closed, 2),
                "open_pipeline": round(t_pipe, 2),
                "attainment_percentage": pct,
                "pipeline_coverage_ratio": coverage,
                "reps": stats["reps"]
            })

        company_attainment = round((company_closed / max(1.0, company_quota)) * 100.0, 1)

        return {
            "company_total_quota": round(company_quota, 2),
            "company_total_closed": round(company_closed, 2),
            "company_total_pipeline": round(company_pipeline, 2),
            "company_attainment_percentage": company_attainment,
            "teams": sorted(teams_summary, key=lambda x: x["total_closed"], reverse=True)
        }
