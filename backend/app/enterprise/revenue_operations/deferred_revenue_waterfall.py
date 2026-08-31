from typing import Any, Dict, List, Optional

class DeferredRevenueWaterfallCalculator:
    """
    Computes monthly roll-forward waterfall for deferred revenue accounting:
    Beginning Deferred + New Bookings/Billings - Recognized Revenue = Ending Deferred.
    """
    @staticmethod
    def calculate_roll_forward(
        starting_deferred: float,
        monthly_billings: List[Dict[str, Any]],
        monthly_recognitions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        billings_by_period = {b["period"]: float(b.get("amount", 0.0)) for b in monthly_billings}
        rec_by_period = {r["period"]: float(r.get("amount", 0.0)) for r in monthly_recognitions}

        all_periods = sorted(list(set(list(billings_by_period.keys()) + list(rec_by_period.keys()))))
        waterfall = []
        current_deferred = starting_deferred

        for p in all_periods:
            beg = round(current_deferred, 2)
            bill = round(billings_by_period.get(p, 0.0), 2)
            rec = round(rec_by_period.get(p, 0.0), 2)
            ending = round(beg + bill - rec, 2)
            current_deferred = ending

            waterfall.append({
                "period": p,
                "beginning_deferred": beg,
                "new_billings": bill,
                "revenue_recognized": rec,
                "ending_deferred": ending,
                "is_balanced": round(beg + bill - rec - ending, 2) == 0.0
            })

        return waterfall
