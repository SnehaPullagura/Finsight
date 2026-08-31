import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/deal_risk_analyzer.py
    write_file("backend/app/domain_services/deal_risk_analyzer.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class DealRiskAnalyzer:
    @staticmethod
    def evaluate_deal_health(
        deal: Dict[str, Any],
        recent_activities: List[Dict[str, Any]],
        days_in_stage: int,
        stage_sla_days: int = 14
    ) -> Dict[str, Any]:
        risk_signals = []
        health_score = 100

        # 1. Stage SLA Stagnation
        if days_in_stage > stage_sla_days:
            stagnation_days = days_in_stage - stage_sla_days
            penalty = min(35, stagnation_days * 3)
            health_score -= penalty
            risk_signals.append(f"Deal stalled in current stage for {days_in_stage} days (SLA: {stage_sla_days} days)")

        # 2. Activity Recency
        if not recent_activities:
            health_score -= 30
            risk_signals.append("Zero logged customer touchpoints or meetings in the last 14 days")
        else:
            last_activity = recent_activities[0]
            # Check for negative sentiment keywords
            desc = (last_activity.get("description") or "").lower()
            if any(k in desc for k in ["budget cut", "delayed", "evaluating competitor", "freeze", "push to next quarter"]):
                health_score -= 25
                risk_signals.append("Risk signals identified in customer communication notes")

        final_score = max(0, min(100, health_score))
        risk_level = "low" if final_score >= 75 else "medium" if final_score >= 45 else "high"

        return {
            "health_score": final_score,
            "risk_level": risk_level,
            "risk_signals": risk_signals,
            "recommended_next_action": "Schedule executive alignment call" if risk_level == "high" else "Send follow-up proposal review"
        }
""")

    # 2. backend/app/domain_services/marketing_cohort_builder.py
    write_file("backend/app/domain_services/marketing_cohort_builder.py", """from datetime import date
from typing import Any, Dict, List, Optional

class MarketingCohortBuilder:
    @staticmethod
    def segment_audience(contacts: List[Dict[str, Any]], criteria: Dict[str, Any]) -> Dict[str, Any]:
        matched_contacts = []
        excluded_contacts = []

        target_industry = criteria.get("industry")
        min_revenue = float(criteria.get("min_annual_revenue", 0.0))
        target_lifecycle = criteria.get("lifecycle_stage")

        for c in contacts:
            ind = c.get("industry")
            rev = float(c.get("annual_revenue", 0.0))
            stage = c.get("lifecycle_stage")

            match = True
            if target_industry and ind != target_industry:
                match = False
            if rev < min_revenue:
                match = False
            if target_lifecycle and stage != target_lifecycle:
                match = False

            if match:
                matched_contacts.append(c)
            else:
                excluded_contacts.append(c)

        return {
            "segment_name": criteria.get("name", "Custom Segment"),
            "matched_count": len(matched_contacts),
            "excluded_count": len(excluded_contacts),
            "matched_audience": matched_contacts[:50]
        }
""")

    # 3. backend/app/domain_services/invoice_reconciliation_service.py
    write_file("backend/app/domain_services/invoice_reconciliation_service.py", """from datetime import date
from typing import Any, Dict, List, Optional

class InvoiceReconciliationService:
    @staticmethod
    def reconcile_payment_against_invoice(
        invoice: Dict[str, Any],
        payment_amount: float,
        payment_reference: str
    ) -> Dict[str, Any]:
        total_due = float(invoice.get("total_amount", 0.0))
        prev_paid = float(invoice.get("amount_paid", 0.0))
        outstanding = max(0.0, round(total_due - prev_paid, 2))

        new_total_paid = round(prev_paid + payment_amount, 2)
        remaining_balance = max(0.0, round(total_due - new_total_paid, 2))

        if new_total_paid >= total_due:
            status = "paid"
        elif new_total_paid > 0:
            status = "partially_paid"
        else:
            status = "unpaid"

        return {
            "invoice_id": invoice.get("id"),
            "invoice_number": invoice.get("invoice_number"),
            "payment_applied": payment_amount,
            "payment_reference": payment_reference,
            "previous_paid": prev_paid,
            "new_total_paid": new_total_paid,
            "remaining_balance": remaining_balance,
            "new_payment_status": status
        }
""")

    # 4. backend/app/domain_services/sales_quota_manager.py
    write_file("backend/app/domain_services/sales_quota_manager.py", """from typing import Any, Dict, List, Optional

class SalesQuotaManager:
    @staticmethod
    def calculate_team_rollups(reps_quotas: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_team_quota = sum(float(r.get("quota", 0.0)) for r in reps_quotas)
        total_team_attainment = sum(float(r.get("attained", 0.0)) for r in reps_quotas)
        team_pct = round((total_team_attainment / max(1.0, total_team_quota)) * 100.0, 2)

        return {
            "total_team_quota": round(total_team_quota, 2),
            "total_team_attainment": round(total_team_attainment, 2),
            "team_attainment_percentage": team_pct,
            "reps_count": len(reps_quotas)
        }
""")

    print("Created deal risk analyzer, marketing cohort, invoice reconciliation, and quota manager.")

if __name__ == '__main__':
    run()
