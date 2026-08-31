from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class CMKKeyRotationScheduler:
    @staticmethod
    def evaluate_key_age(keys: List[Dict[str, Any]], max_age_days: int = 90) -> List[Dict[str, Any]]:
        results = []
        today = date.today()

        for k in keys:
            created_str = k.get("created_date", today.isoformat())
            created_date = date.fromisoformat(created_str)
            age = (today - created_date).days
            needs_rotation = age >= max_age_days

            results.append({
                "key_id": k.get("id"),
                "key_alias": k.get("alias"),
                "age_days": age,
                "max_allowed_age": max_age_days,
                "is_rotation_due": needs_rotation,
                "status": "ROTATION_REQUIRED" if needs_rotation else "ACTIVE_COMPLIANT"
            })

        return results
