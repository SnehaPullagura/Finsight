from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ASC606RevenueRecognitionEngine:
    @staticmethod
    def generate_amortization_schedule(
        contract_id: str,
        total_contract_value: float,
        start_date: date,
        term_months: int
    ) -> List[Dict[str, Any]]:
        monthly_recognized = round(total_contract_value / float(term_months), 2)
        schedule = []
        cumulative_recognized = 0.0

        for month_idx in range(1, term_months + 1):
            # Last month adjusts rounding difference
            if month_idx == term_months:
                amount = round(total_contract_value - cumulative_recognized, 2)
            else:
                amount = monthly_recognized

            cumulative_recognized += amount
            deferred_remaining = max(0.0, round(total_contract_value - cumulative_recognized, 2))
            
            period_date = start_date + timedelta(days=30 * (month_idx - 1))

            schedule.append({
                "period_number": month_idx,
                "recognition_date": period_date.isoformat(),
                "recognized_amount": amount,
                "cumulative_recognized": round(cumulative_recognized, 2),
                "deferred_revenue_balance": deferred_remaining,
                "compliance_standard": "ASC 606 / IFRS 15"
            })

        return schedule
