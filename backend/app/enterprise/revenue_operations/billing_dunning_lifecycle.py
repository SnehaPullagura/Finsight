from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

class DunningLifecycleManager:
    """
    Automated Dunning & Involuntary Churn Recovery:
    Smart payment retries, escalating notification cadences, grace periods, and service suspension.
    """
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
