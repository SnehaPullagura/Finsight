import math
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class AdvancedPipelineForecastingService:
    @staticmethod
    def calculate_category_rollups(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        categories = {
            "closed": {"count": 0, "amount": 0.0, "deals": []},
            "commit": {"count": 0, "amount": 0.0, "deals": []},
            "best_case": {"count": 0, "amount": 0.0, "deals": []},
            "pipeline": {"count": 0, "amount": 0.0, "deals": []},
            "omitted": {"count": 0, "amount": 0.0, "deals": []}
        }

        for d in deals:
            status = (d.get("status") or "open").lower()
            stage = (d.get("stage") or "").lower()
            val = float(d.get("value", 0.0))
            prob = float(d.get("probability", 0.0))

            if status == "won":
                cat = "closed"
            elif status == "lost":
                cat = "omitted"
            elif prob >= 85 or stage in ["negotiation", "contract"]:
                cat = "commit"
            elif prob >= 50 or stage in ["proposal", "demo"]:
                cat = "best_case"
            else:
                cat = "pipeline"

            categories[cat]["count"] += 1
            categories[cat]["amount"] = round(categories[cat]["amount"] + val, 2)
            categories[cat]["deals"].append(d)

        total_open = categories["commit"]["amount"] + categories["best_case"]["amount"] + categories["pipeline"]["amount"]

        return {
            "categories": {k: {"count": v["count"], "amount": v["amount"]} for k, v in categories.items()},
            "summary": {
                "total_closed_won": categories["closed"]["amount"],
                "total_commit": categories["commit"]["amount"],
                "total_best_case": categories["best_case"]["amount"],
                "total_open_pipeline": round(total_open, 2),
                "expected_quarter_finish": round(categories["closed"]["amount"] + categories["commit"]["amount"] + (categories["best_case"]["amount"] * 0.5), 2)
            }
        }
