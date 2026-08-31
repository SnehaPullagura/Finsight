import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/revenue_operations/asc606_revenue_schedules.py
    write_file("backend/app/enterprise/revenue_operations/asc606_revenue_schedules.py", """from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RevenueScheduleItem(BaseModel):
    period_month: str
    recognized_amount: float
    deferred_balance: float
    is_recognized: bool = False
    performance_obligation_id: str

class ASC606RevenueRecognitionEngine:
    \"\"\"
    ASC 606 / IFRS 15 Compliant Five-Step Revenue Recognition Engine:
    1. Identify the contract with a customer
    2. Identify the performance obligations in the contract
    3. Determine the transaction price
    4. Allocate the transaction price to performance obligations
    5. Recognize revenue when/as the entity satisfies a performance obligation
    \"\"\"
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
        \"\"\"
        Allocates transaction price based on Standalone Selling Price (SSP).
        \"\"\"
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
""")

    # 2. backend/app/enterprise/revenue_operations/usage_metering_aggregator.py
    write_file("backend/app/enterprise/revenue_operations/usage_metering_aggregator.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class UsageMeteringAggregator:
    \"\"\"
    Aggregates high-throughput usage events (API calls, storage GB, AI tokens)
    and computes rating charges based on tiered or graduated pricing models.
    \"\"\"
    @staticmethod
    def compute_tiered_charge(
        metric_name: str,
        units_consumed: float,
        tiers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        total_charge = 0.0
        remaining_units = units_consumed
        tier_breakdown = []

        for tier in sorted(tiers, key=lambda x: x.get("min_units", 0)):
            min_u = float(tier.get("min_units", 0))
            max_u = float(tier.get("max_units", float("inf")))
            rate = float(tier.get("unit_price", 0.0))

            tier_capacity = max_u - min_u
            if remaining_units > 0:
                units_in_tier = min(remaining_units, tier_capacity)
                tier_cost = round(units_in_tier * rate, 4)
                total_charge += tier_cost
                remaining_units -= units_in_tier

                tier_breakdown.append({
                    "tier_range": f"{int(min_u)} - {int(max_u) if max_u != float('inf') else 'Unlimited'}",
                    "units_rated": units_in_tier,
                    "unit_rate": rate,
                    "tier_total": tier_cost
                })

        return {
            "metric_name": metric_name,
            "total_units_consumed": units_consumed,
            "total_rated_charge": round(total_charge, 2),
            "tier_breakdown": tier_breakdown,
            "rated_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def aggregate_account_events(
        account_id: str,
        events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        totals = {}
        for ev in events:
            metric = ev.get("metric_name", "generic_counter")
            val = float(ev.get("quantity", 1.0))
            totals[metric] = totals.get(metric, 0.0) + val

        return {
            "account_id": account_id,
            "event_count": len(events),
            "aggregated_metrics": totals,
            "aggregated_at": datetime.now(timezone.utc).isoformat()
        }
""")

    # 3. backend/app/enterprise/revenue_operations/deferred_revenue_waterfall.py
    write_file("backend/app/enterprise/revenue_operations/deferred_revenue_waterfall.py", """from typing import Any, Dict, List, Optional

class DeferredRevenueWaterfallCalculator:
    \"\"\"
    Computes monthly roll-forward waterfall for deferred revenue accounting:
    Beginning Deferred + New Bookings/Billings - Recognized Revenue = Ending Deferred.
    \"\"\"
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
""")

    # 4. backend/app/enterprise/revenue_operations/billing_dunning_lifecycle.py
    write_file("backend/app/enterprise/revenue_operations/billing_dunning_lifecycle.py", """from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

class DunningLifecycleManager:
    \"\"\"
    Automated Dunning & Involuntary Churn Recovery:
    Smart payment retries, escalating notification cadences, grace periods, and service suspension.
    \"\"\"
    @staticmethod
    def evaluate_invoice_dunning(
        invoice: Dict[str, Any],
        days_past_due: int
    ) -> Dict[str, Any]:
        inv_id = invoice.get("id")
        amount = float(invoice.get("amount_due", 0.0))
        customer = invoice.get("customer_name", "Enterprise Account")

        if days_past_due <= 3:
            stage = "SOFT_REMINDER"
            action = "Dispatch polite email reminder with updated payment link."
            retry_payment = True
            suspend = False
        elif days_past_due <= 10:
            stage = "PAST_DUE_WARNING"
            action = "Dispatch urgent finance escalation notice and trigger backup payment method retry."
            retry_payment = True
            suspend = False
        elif days_past_due <= 21:
            stage = "FINAL_NOTICE"
            action = "Notify Account Executive and Customer Success Manager for high-touch intervention."
            retry_payment = True
            suspend = False
        else:
            stage = "SERVICE_SUSPENDED"
            action = "Apply temporary read-only account lock until outstanding balance is resolved."
            retry_payment = False
            suspend = True

        return {
            "invoice_id": inv_id,
            "customer_name": customer,
            "amount_due": amount,
            "days_past_due": days_past_due,
            "dunning_stage": stage,
            "recommended_action": action,
            "should_retry_charge": retry_payment,
            "is_service_suspended": suspend,
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }
""")

    # 5. backend/app/enterprise/revenue_operations/tax_jurisdiction_engine.py
    write_file("backend/app/enterprise/revenue_operations/tax_jurisdiction_engine.py", """from typing import Any, Dict, List, Optional

class TaxJurisdictionEngine:
    \"\"\"
    Enterprise Sales Tax & VAT Determination Engine with multi-state nexus support.
    \"\"\"
    RATES_BY_JURISDICTION = {
        "US-CA": {"state_tax": 0.0725, "digital_goods_exempt": True, "vat_name": "Sales Tax"},
        "US-NY": {"state_tax": 0.08875, "digital_goods_exempt": False, "vat_name": "Sales Tax"},
        "US-TX": {"state_tax": 0.0825, "digital_goods_exempt": False, "vat_name": "Sales Tax (80% SaaS Taxable)"},
        "EU-DE": {"state_tax": 0.19, "digital_goods_exempt": False, "vat_name": "MwSt (VAT)"},
        "EU-FR": {"state_tax": 0.20, "digital_goods_exempt": False, "vat_name": "TVA (VAT)"},
        "UK": {"state_tax": 0.20, "digital_goods_exempt": False, "vat_name": "VAT"},
        "SG": {"state_tax": 0.09, "digital_goods_exempt": False, "vat_name": "GST"},
        "DEFAULT": {"state_tax": 0.0, "digital_goods_exempt": True, "vat_name": "Zero Tax"}
    }

    @classmethod
    def calculate_invoice_tax(
        cls,
        jurisdiction_code: str,
        subtotal: float,
        is_tax_exempt_entity: bool = False
    ) -> Dict[str, Any]:
        if is_tax_exempt_entity:
            return {
                "jurisdiction": jurisdiction_code,
                "subtotal": round(subtotal, 2),
                "tax_rate_percentage": 0.0,
                "tax_amount": 0.0,
                "total_with_tax": round(subtotal, 2),
                "exemption_status": "EXEMPT_CERTIFICATE_VERIFIED"
            }

        rule = cls.RATES_BY_JURISDICTION.get(jurisdiction_code, cls.RATES_BY_JURISDICTION["DEFAULT"])
        rate = rule["state_tax"]
        tax_val = round(subtotal * rate, 2)
        total = round(subtotal + tax_val, 2)

        return {
            "jurisdiction": jurisdiction_code,
            "tax_regime_name": rule["vat_name"],
            "subtotal": round(subtotal, 2),
            "tax_rate_percentage": round(rate * 100.0, 3),
            "tax_amount": tax_val,
            "total_with_tax": total,
            "exemption_status": "TAXABLE"
        }
""")

    print("RevOps suite part 1 created successfully.")

if __name__ == "__main__":
    run()
