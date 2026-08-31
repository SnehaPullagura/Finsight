from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RevenueScheduleItem(BaseModel):
    period_month: str
    recognized_amount: float
    deferred_balance: float
    is_recognized: bool = False
    performance_obligation_id: str

class ASC606RevenueRecognitionEngine:
    """
    ASC 606 / IFRS 15 Compliant Five-Step Revenue Recognition Engine:
    1. Identify the contract with a customer
    2. Identify the performance obligations in the contract
    3. Determine the transaction price
    4. Allocate the transaction price to performance obligations
    5. Recognize revenue when/as the entity satisfies a performance obligation
    """
    @staticmethod
    def generate_straight_line_schedule(
        contract_id: str,
        total_price: float,
        term_months: int,
        start_date: str,
        obligation_name: str = "SaaS Platform Access"
    ) -> Dict[str, Any]:
        monthly_rec = round(total_price / max(1, term_months), 2)
        schedules: List[Dict[str, Any]] = []
        remaining_deferred = total_price

        # Parse start year and month
        parts = start_date.split("-")
        year = int(parts[0])
        month = int(parts[1])

        for m in range(term_months):
            curr_month = ((month - 1 + m) % 12) + 1
            curr_year = year + ((month - 1 + m) // 12)
            period_key = f"{curr_year:04d}-{curr_month:02d}"

            # Last month adjustment for rounding pennies
            if m == term_months - 1:
                recognized = round(remaining_deferred, 2)
                remaining_deferred = 0.0
            else:
                recognized = monthly_rec
                remaining_deferred = round(remaining_deferred - recognized, 2)

            schedules.append({
                "period_month": period_key,
                "contract_id": contract_id,
                "obligation_name": obligation_name,
                "recognized_amount": recognized,
                "deferred_ending_balance": remaining_deferred,
                "accounting_standard": "ASC_606_IFRS_15",
                "status": "SCHEDULED"
            })

        return {
            "contract_id": contract_id,
            "total_contract_value": total_price,
            "term_months": term_months,
            "monthly_amortization_rate": monthly_rec,
            "schedule_count": len(schedules),
            "revenue_schedules": schedules
        }

    @staticmethod
    def allocate_multi_element_arr(
        elements: List[Dict[str, Any]],
        total_discounted_price: float
    ) -> List[Dict[str, Any]]:
        """
        Allocates transaction price based on Standalone Selling Price (SSP).
        """
        total_ssp = sum(float(e.get("standalone_selling_price", 0.0)) for e in elements)
        allocated_elements = []

        for e in elements:
            ssp = float(e.get("standalone_selling_price", 0.0))
            ratio = ssp / max(1.0, total_ssp)
            allocated_price = round(total_discounted_price * ratio, 2)

            allocated_elements.append({
                "obligation_id": e.get("id"),
                "obligation_name": e.get("name"),
                "standalone_selling_price": ssp,
                "ssp_allocation_ratio": round(ratio, 4),
                "allocated_transaction_price": allocated_price,
                "timing": e.get("recognition_timing", "OVER_TIME")
            })

        return allocated_elements
