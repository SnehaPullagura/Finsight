from typing import Any, Dict, List, Optional

class RepPipelineCoverageModeler:
    @staticmethod
    def calculate_rep_coverage_ratios(reps_data: List[Dict[str, Any]], target_coverage_multiple: float = 3.0) -> List[Dict[str, Any]]:
        results = []
        for r in reps_data:
            quota = float(r.get("quota_remaining", 100000.0))
            pipeline = float(r.get("open_pipeline", 0.0))
            coverage = round(pipeline / max(1.0, quota), 2)
            gap = max(0.0, round((quota * target_coverage_multiple) - pipeline, 2))

            results.append({
                "rep_id": r.get("id"),
                "rep_name": r.get("name"),
                "quota_remaining": quota,
                "open_pipeline": pipeline,
                "coverage_multiple": coverage,
                "target_coverage": target_coverage_multiple,
                "pipeline_gap_to_target": gap,
                "is_well_covered": coverage >= target_coverage_multiple
            })

        return sorted(results, key=lambda x: x["coverage_multiple"])
