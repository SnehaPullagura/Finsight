from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepPipelineGenerationVelocityAnalyzer:
    @staticmethod
    def calculate_pipeline_created(reps_sourcing: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_sourcing:
            name = r.get("rep_name")
            pipe_created = float(r.get("pipeline_dollars_created", 0.0))
            quota = float(r.get("quarterly_quota", 250000.0))
            self_sourced_pct = float(r.get("self_sourced_pct", 50.0))

            pipeline_multiple = round(pipe_created / max(1.0, quota), 2)
            tier = "High Pipeline Engine (> 4x)" if pipeline_multiple >= 4.0 else "Self-Sustaining (3x - 4x)" if pipeline_multiple >= 3.0 else "Dependent on Inbound (< 3x)"

            results.append({
                "rep_name": name,
                "pipeline_created": pipe_created,
                "quarterly_quota": quota,
                "pipeline_created_multiple": pipeline_multiple,
                "self_sourced_percentage": self_sourced_pct,
                "sourcing_efficiency_tier": tier
            })

        return sorted(results, key=lambda x: x["pipeline_created_multiple"], reverse=True)
