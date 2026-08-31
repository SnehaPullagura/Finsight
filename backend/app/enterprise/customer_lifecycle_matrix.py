from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class CustomerLifecycleMatrix:
    @staticmethod
    def transition_lifecycle_stage(current_stage: str, trigger_event: str) -> Dict[str, Any]:
        transitions = {
            ("subscriber", "lead_form_submitted"): "lead",
            ("lead", "marketing_qualified"): "mql",
            ("mql", "sales_accepted"): "sql",
            ("sql", "opportunity_created"): "opportunity",
            ("opportunity", "deal_closed_won"): "customer",
            ("customer", "expansion_deal_won"): "evangelist",
            ("customer", "subscription_canceled"): "churned",
            ("churned", "winback_campaign_accepted"): "customer"
        }

        next_stage = transitions.get((current_stage.lower(), trigger_event.lower()), current_stage)
        is_valid_transition = next_stage != current_stage

        return {
            "from_stage": current_stage,
            "trigger_event": trigger_event,
            "to_stage": next_stage,
            "is_transition_applied": is_valid_transition,
            "timestamp": date.today().isoformat()
        }
