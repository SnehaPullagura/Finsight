from typing import Any, Dict, List, Optional

class PipelineDriftMonitor:
    """
    Monitors week-over-week changes in quarterly pipeline:
    Identifies newly created pipeline, stage progressions, slipped deals, and reduced values.
    """
    @staticmethod
    def compute_pipeline_drift(
        start_of_week_deals: List[Dict[str, Any]],
        end_of_week_deals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        start_dict = {d["id"]: d for d in start_of_week_deals}
        end_dict = {d["id"]: d for d in end_of_week_deals}

        new_deals = [d for d in end_of_week_deals if d["id"] not in start_dict]
        won_deals = [d for d in end_of_week_deals if d.get("stage") == "Closed Won" and start_dict.get(d["id"], {}).get("stage") != "Closed Won"]
        slipped_deals = [d for d in end_of_week_deals if d.get("is_slipped_to_next_quarter", False) and not start_dict.get(d["id"], {}).get("is_slipped_to_next_quarter", False)]

        new_arr = sum(float(d.get("value", 0.0)) for d in new_deals)
        won_arr = sum(float(d.get("value", 0.0)) for d in won_deals)
        slipped_arr = sum(float(d.get("value", 0.0)) for d in slipped_deals)

        return {
            "new_pipeline_created_arr": round(new_arr, 2),
            "closed_won_arr": round(won_arr, 2),
            "slipped_pipeline_arr": round(slipped_arr, 2),
            "net_pipeline_velocity": round(new_arr + won_arr - slipped_arr, 2),
            "drift_health": "POSITIVE_ACCELERATION" if new_arr >= slipped_arr else "PIPELINE_DECAY_WARNING"
        }
