from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseDunningManager:
    @staticmethod
    def evaluate_invoice_dunning_stage(
        due_date: date,
        amount_due: float,
        current_date: Optional[date] = None
    ) -> Dict[str, Any]:
        today = current_date or date.today()
        days_overdue = (today - due_date).days

        if days_overdue <= 0:
            stage = "current"
            action = "none"
            grace_active = False
        elif days_overdue <= 7:
            stage = "soft_reminder"
            action = "send_gentle_reminder_email"
            grace_active = True
        elif days_overdue <= 14:
            stage = "urgent_reminder"
            action = "send_urgent_past_due_email"
            grace_active = True
        elif days_overdue <= 30:
            stage = "account_warning"
            action = "create_account_manager_task"
            grace_active = False
        else:
            stage = "service_suspension_warning"
            action = "suspend_non_essential_features"
            grace_active = False

        return {
            "due_date": due_date.isoformat(),
            "days_overdue": max(0, days_overdue),
            "amount_due": amount_due,
            "dunning_stage": stage,
            "recommended_action": action,
            "is_grace_period_active": grace_active
        }
