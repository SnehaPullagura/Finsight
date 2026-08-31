import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/analytics/advanced_models.py
    write_file("backend/app/analytics/advanced_models.py", """import math
import statistics
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class StatisticalForecastModel:
    @staticmethod
    def moving_average_forecast(series: List[float], window_size: int = 3, forecast_periods: int = 3) -> List[float]:
        if len(series) < window_size:
            return [series[-1] if series else 0.0] * forecast_periods

        current_series = list(series)
        forecasts = []

        for _ in range(forecast_periods):
            avg = sum(current_series[-window_size:]) / float(window_size)
            forecasts.append(round(avg, 2))
            current_series.append(avg)

        return forecasts

    @staticmethod
    def linear_trend_regression(series: List[float], forecast_periods: int = 3) -> Dict[str, Any]:
        n = len(series)
        if n < 2:
            return {"slope": 0.0, "intercept": series[0] if series else 0.0, "r_squared": 0.0, "forecast": [0.0] * forecast_periods}

        x = list(range(n))
        y = series

        x_mean = sum(x) / float(n)
        y_mean = sum(y) / float(n)

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = y_mean - (slope * x_mean)

        # R-squared calculation
        y_pred = [intercept + slope * xi for xi in x]
        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

        future_x = range(n, n + forecast_periods)
        forecasts = [round(max(0.0, intercept + slope * fx), 2) for fx in future_x]

        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 2),
            "r_squared": round(max(0.0, min(1.0, r_squared)), 4),
            "forecast": forecasts
        }

    @staticmethod
    def exponential_smoothing(series: List[float], alpha: float = 0.3, forecast_periods: int = 3) -> List[float]:
        if not series:
            return [0.0] * forecast_periods

        smoothed = [series[0]]
        for t in range(1, len(series)):
            st = alpha * series[t] + (1 - alpha) * smoothed[t - 1]
            smoothed.append(st)

        last_smoothed = smoothed[-1]
        return [round(last_smoothed, 2)] * forecast_periods
""")

    # 2. backend/app/domain_services/pipeline_automation_service.py
    write_file("backend/app/domain_services/pipeline_automation_service.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class PipelineAutomationService:
    STAGE_PROBABILITIES = {
        "discovery": 20,
        "scoping": 40,
        "proposal": 60,
        "negotiation": 80,
        "closed_won": 100,
        "closed_lost": 0
    }

    @staticmethod
    def evaluate_deal_advancement(
        deal: Dict[str, Any],
        completed_activities: List[Dict[str, Any]],
        has_accepted_proposal: bool = False
    ) -> Dict[str, Any]:
        current_stage = (deal.get("stage") or "discovery").lower()
        deal_id = deal.get("id")

        if current_stage == "discovery":
            # Advance to scoping if at least 1 discovery call was logged
            has_call = any(a.get("activity_type") in ["CALL", "MEETING"] for a in completed_activities)
            if has_call:
                return {"should_advance": True, "target_stage": "scoping", "reason": "Discovery meeting completed"}

        elif current_stage == "scoping":
            # Advance to proposal if scoping document or email sent
            has_scope = any(a.get("activity_type") in ["EMAIL", "NOTE"] for a in completed_activities)
            if has_scope:
                return {"should_advance": True, "target_stage": "proposal", "reason": "Scoping requirements verified"}

        elif current_stage == "proposal":
            if has_accepted_proposal:
                return {"should_advance": True, "target_stage": "negotiation", "reason": "Customer accepted formal proposal"}

        elif current_stage == "negotiation":
            if has_accepted_proposal and deal.get("is_contract_signed"):
                return {"should_advance": True, "target_stage": "closed_won", "reason": "Contract executed by both parties"}

        return {"should_advance": False, "target_stage": current_stage, "reason": "Stage entry criteria not yet satisfied"}
""")

    # 3. backend/app/domain_services/marketing_attribution_matrix.py
    write_file("backend/app/domain_services/marketing_attribution_matrix.py", """from typing import Any, Dict, List, Optional

class MarketingAttributionMatrix:
    @staticmethod
    def calculate_w_shaped_attribution(touchpoints: List[Dict[str, Any]], total_revenue: float) -> Dict[str, float]:
        if not touchpoints:
            return {}

        n = len(touchpoints)
        if n == 1:
            return {touchpoints[0]["channel"]: round(total_revenue, 2)}
        elif n == 2:
            return {
                touchpoints[0]["channel"]: round(total_revenue * 0.50, 2),
                touchpoints[1]["channel"]: round(total_revenue * 0.50, 2)
            }

        # W-Shaped: 30% First Touch, 30% Lead Creation Touch, 30% Opportunity Creation Touch, 10% split across remaining
        first_touch = touchpoints[0]["channel"]
        last_touch = touchpoints[-1]["channel"]
        mid_touch = touchpoints[int(n / 2)]["channel"]

        attribution = {}
        attribution[first_touch] = attribution.get(first_touch, 0.0) + round(total_revenue * 0.30, 2)
        attribution[mid_touch] = attribution.get(mid_touch, 0.0) + round(total_revenue * 0.30, 2)
        attribution[last_touch] = attribution.get(last_touch, 0.0) + round(total_revenue * 0.30, 2)

        remaining_count = max(1, n - 3)
        remaining_pool = round(total_revenue * 0.10, 2)
        per_item = remaining_pool / float(remaining_count)

        for i in range(1, n - 1):
            if i != int(n / 2):
                ch = touchpoints[i]["channel"]
                attribution[ch] = attribution.get(ch, 0.0) + round(per_item, 2)

        return attribution
""")

    # 4. backend/app/domain_services/quote_lifecycle_manager.py
    write_file("backend/app/domain_services/quote_lifecycle_manager.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class QuoteLifecycleManager:
    @staticmethod
    def validate_quote_discount_thresholds(
        line_items: List[Dict[str, Any]],
        approver_role: str = "Sales Rep"
    ) -> Dict[str, Any]:
        max_discount_found = 0.0
        requires_manager_approval = False
        requires_vp_approval = False

        for item in line_items:
            disc_pct = float(item.get("discount_percentage", 0.0))
            max_discount_found = max(max_discount_found, disc_pct)

            if disc_pct > 30.0:
                requires_vp_approval = True
            elif disc_pct > 15.0:
                requires_manager_approval = True

        status = "approved"
        if requires_vp_approval:
            status = "requires_vp_approval" if approver_role not in ["VP of Sales", "Admin"] else "approved"
        elif requires_manager_approval:
            status = "requires_manager_approval" if approver_role not in ["Sales Manager", "VP of Sales", "Admin"] else "approved"

        return {
            "max_discount_percentage": max_discount_found,
            "requires_manager_approval": requires_manager_approval,
            "requires_vp_approval": requires_vp_approval,
            "approval_status": status
        }
""")

    print("Created advanced models and domain services.")

if __name__ == '__main__':
    run()
