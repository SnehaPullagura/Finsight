from typing import Any, Dict, List, Optional

class ExecutivePipelineHealthIndex:
    @staticmethod
    def calculate_health_index(
        total_open_pipeline: float,
        quarter_target: float,
        average_deal_age_days: float,
        slippage_rate_pct: float,
        pushed_deals_pct: float
    ) -> Dict[str, Any]:
        coverage = total_open_pipeline / max(1.0, quarter_target)
        
        # Base score on 3.0x coverage = 50 pts
        coverage_score = min(50.0, (coverage / 3.0) * 50.0)

        # Freshness score (max 25 pts)
        freshness_score = max(0.0, 25.0 - (max(0.0, average_deal_age_days - 30.0) * 0.5))

        # Slippage penalty (max 25 pts)
        slippage_penalty = min(25.0, (slippage_rate_pct * 0.5) + (pushed_deals_pct * 0.5))
        stability_score = max(0.0, 25.0 - slippage_penalty)

        total_health_score = round(coverage_score + freshness_score + stability_score, 1)

        rating = "Elite Pipeline Health" if total_health_score >= 85.0 else "Healthy Pipeline" if total_health_score >= 70.0 else "Vulnerable to Target Miss"

        return {
            "pipeline_coverage_ratio": round(coverage, 2),
            "coverage_score": round(coverage_score, 1),
            "freshness_score": round(freshness_score, 1),
            "stability_score": round(stability_score, 1),
            "total_health_score": total_health_score,
            "pipeline_grade": rating,
            "is_target_at_risk": total_health_score < 70.0
        }
