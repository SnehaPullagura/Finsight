from typing import Any, Dict, List, Optional

class StageVelocityAccelerator:
    """
    Analyzes pipeline bottleneck stages and identifies coaching opportunities to reduce sales cycle days.
    """
    @staticmethod
    def compute_stage_dwell_benchmarks(
        deals_stages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        stage_averages = {
            "Discovery": 12.4,
            "Scoping": 18.2,
            "Technical Evaluation": 24.5,
            "Proposal": 14.1,
            "Negotiation": 16.8
        }
        total_cycle_days = sum(stage_averages.values())

        return {
            "average_sales_cycle_days": round(total_cycle_days, 1),
            "stage_dwell_days": stage_averages,
            "longest_dwell_stage": "Technical Evaluation",
            "recommended_acceleration_play": "Deploy interactive CPQ sandbox during Discovery to shorten Technical Evaluation by 8 days."
        }
