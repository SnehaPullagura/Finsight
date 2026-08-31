from typing import Any, Dict, List, Optional

class BoardLevelGuidanceCompiler:
    """
    Compiles executive board-ready quarterly revenue guidance briefings.
    """
    @staticmethod
    def compile_quarterly_guidance(
        target_quota: float,
        committed_arr: float,
        best_case_arr: float,
        pipeline_coverage_multiple: float
    ) -> Dict[str, Any]:
        gap_to_target = max(0.0, target_quota - committed_arr)
        attainment_trajectory_pct = round((committed_arr / max(1.0, target_quota)) * 100.0, 1)

        return {
            "quarterly_board_target": target_quota,
            "current_committed_arr": committed_arr,
            "best_case_upside_arr": best_case_arr,
            "gap_to_target": round(gap_to_target, 2),
            "projected_attainment_pct": attainment_trajectory_pct,
            "pipeline_coverage_multiple": pipeline_coverage_multiple,
            "board_verdict": "ON_PLAN_TO_BEAT" if committed_arr >= target_quota else "ON_PACE_NEEDS_ACCELERATION" if attainment_trajectory_pct >= 85.0 else "AT_RISK_REQUIRES_INTERVENTION"
        }
