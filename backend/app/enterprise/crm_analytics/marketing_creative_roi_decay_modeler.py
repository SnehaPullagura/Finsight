from typing import Any, Dict, List, Optional

class CreativeROIDecayModeler:
    @staticmethod
    def calculate_decay_schedule(initial_roas: float, weekly_decay_pct: float = 4.5, weeks: int = 8) -> List[Dict[str, Any]]:
        schedule = []
        current_roas = initial_roas

        for w in range(1, weeks + 1):
            schedule.append({
                "week_number": w,
                "projected_roas": round(current_roas, 2),
                "is_profitable": current_roas >= 3.0
            })
            current_roas *= (1.0 - (weekly_decay_pct / 100.0))

        return schedule
