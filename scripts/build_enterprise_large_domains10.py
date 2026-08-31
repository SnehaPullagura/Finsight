import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_compensation_calculator.py
    write_file("backend/app/enterprise/sales_compensation_calculator.py", """import math
from typing import Any, Dict, List, Optional

class EnterpriseCompensationCalculator:
    @staticmethod
    def calculate_rep_payout(
        rep_name: str,
        quota_target: float,
        closed_deals: List[Dict[str, Any]],
        base_commission_rate: float = 0.10,
        accelerator_tier_1: float = 1.0, # 0-100%
        accelerator_tier_2: float = 1.5, # 100-120%
        accelerator_tier_3: float = 2.0  # 120%+
    ) -> Dict[str, Any]:
        total_closed = sum(float(d.get("value", 0.0)) for d in closed_deals if d.get("status") == "won")
        attainment_pct = (total_closed / max(1.0, quota_target)) * 100.0

        commission_earned = 0.0

        # Tier 1: 0 - 100%
        tier_1_max = quota_target
        tier_1_attained = min(total_closed, tier_1_max)
        commission_earned += tier_1_attained * base_commission_rate * accelerator_tier_1

        # Tier 2: 100% - 120%
        if total_closed > quota_target:
            tier_2_max = quota_target * 1.20
            tier_2_attained = min(total_closed, tier_2_max) - quota_target
            commission_earned += tier_2_attained * base_commission_rate * accelerator_tier_2

        # Tier 3: 120%+
        if total_closed > quota_target * 1.20:
            tier_3_attained = total_closed - (quota_target * 1.20)
            commission_earned += tier_3_attained * base_commission_rate * accelerator_tier_3

        effective_rate = (commission_earned / max(1.0, total_closed)) * 100.0

        return {
            "rep_name": rep_name,
            "quota_target": quota_target,
            "total_closed_revenue": round(total_closed, 2),
            "attainment_percentage": round(attainment_pct, 2),
            "total_commission_payout": round(commission_earned, 2),
            "effective_commission_rate_pct": round(effective_rate, 2),
            "is_quota_achieved": attainment_pct >= 100.0
        }
""")

    # 2. backend/app/enterprise/customer_lifecycle_matrix.py
    write_file("backend/app/enterprise/customer_lifecycle_matrix.py", """from datetime import date, timedelta
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
""")

    # 3. backend/app/enterprise/data_quality_sanitizer.py
    write_file("backend/app/enterprise/data_quality_sanitizer.py", """import re
from typing import Any, Dict, List, Optional

class DataQualitySanitizer:
    @staticmethod
    def sanitize_phone_number(raw_phone: Optional[str], default_country_code: str = "+1") -> Optional[str]:
        if not raw_phone:
            return None
        digits_only = re.sub(r"\D", "", raw_phone)
        if len(digits_only) == 10:
            return f"{default_country_code}-{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 11 and digits_only.startswith("1"):
            return f"+1-{digits_only[1:4]}-{digits_only[4:7]}-{digits_only[7:]}"
        return f"+{digits_only}" if digits_only else None

    @staticmethod
    def clean_company_name(raw_name: Optional[str]) -> str:
        if not raw_name:
            return ""
        cleaned = re.sub(r"(?i)\b(inc|incorporated|corp|corporation|llc|ltd|limited|gmbh|co)\b\.?", "", raw_name)
        return re.sub(r"\s+", " ", cleaned).strip().title()
""")

    print("Created compensation calculator, lifecycle matrix, and data quality sanitizer.")

if __name__ == '__main__':
    run()
