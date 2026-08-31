import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/domain_handlers/round_robin_lead_balancer.py
    write_file("backend/app/enterprise/domain_handlers/round_robin_lead_balancer.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class RoundRobinLeadBalancer:
    def __init__(self, sales_reps: List[Dict[str, Any]]):
        self.reps = sales_reps # List of reps with id, name, max_capacity, is_active
        self.cursor = 0
        self.assignment_counts = defaultdict(int)

    def assign_lead(self, lead_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        active_reps = [r for r in self.reps if r.get("is_active", True)]
        if not active_reps:
            return None

        # Filter by capacity
        available_reps = []
        for r in active_reps:
            rid = r.get("id")
            cap = r.get("max_capacity", 50)
            if self.assignment_counts[rid] < cap:
                available_reps.append(r)

        if not available_reps:
            available_reps = active_reps # Fallback if all at capacity

        # Select next rep round-robin
        self.cursor = self.cursor % len(available_reps)
        chosen_rep = available_reps[self.cursor]
        self.cursor = (self.cursor + 1) % len(available_reps)

        rid = chosen_rep.get("id")
        self.assignment_counts[rid] += 1

        return {
            "assigned_rep_id": rid,
            "assigned_rep_name": chosen_rep.get("name"),
            "assigned_rep_email": chosen_rep.get("email"),
            "lead_id": lead_data.get("id"),
            "current_load": self.assignment_counts[rid]
        }
""")

    # 2. backend/app/enterprise/domain_handlers/contract_lifecycle_state_machine.py
    write_file("backend/app/enterprise/domain_handlers/contract_lifecycle_state_machine.py", """from datetime import date
from typing import Any, Dict, List, Optional, Tuple

class ContractLifecycleStateMachine:
    VALID_TRANSITIONS = {
        "draft": ["internal_review", "discarded"],
        "internal_review": ["approved", "changes_requested", "draft"],
        "approved": ["out_for_signature", "internal_review"],
        "out_for_signature": ["signed", "rejected", "expired"],
        "signed": ["active", "terminated"],
        "active": ["renewal_pending", "amended", "terminated", "expired"],
        "renewal_pending": ["renewed", "expired", "terminated"],
        "amended": ["active"],
        "renewed": ["active"],
        "expired": [],
        "terminated": [],
        "discarded": []
    }

    @staticmethod
    def transition_state(
        current_state: str,
        target_state: str,
        actor_id: str,
        actor_role: str
    ) -> Tuple[bool, Optional[str]]:
        cur = current_state.lower()
        tgt = target_state.lower()

        allowed = ContractLifecycleStateMachine.VALID_TRANSITIONS.get(cur, [])
        if tgt not in allowed:
            return False, f"Invalid transition from state '{cur}' to '{tgt}'."

        # Role-based state transition gates
        if tgt == "approved" and actor_role not in ["Legal", "VP of Sales", "Admin"]:
            return False, "Only Legal Counsel or VP of Sales can approve contracts."

        if tgt == "active" and cur != "signed" and actor_role != "Admin":
            return False, "Contract must be signed by all parties before activation."

        return True, None
""")

    # 3. backend/app/enterprise/domain_handlers/dynamic_pricing_calculator.py
    write_file("backend/app/enterprise/domain_handlers/dynamic_pricing_calculator.py", """from typing import Any, Dict, List, Optional

class DynamicPricingCalculator:
    @staticmethod
    def calculate_enterprise_quote(
        base_product_price: float,
        user_licenses: int,
        support_tier: str, # standard, gold, platinum
        contract_duration_years: int,
        custom_discount_pct: float = 0.0
    ) -> Dict[str, Any]:
        license_subtotal = base_product_price * user_licenses
        
        # Support tier multiplier
        support_pct = 0.10 if support_tier.lower() == "gold" else 0.20 if support_tier.lower() == "platinum" else 0.0
        support_cost_annual = license_subtotal * support_pct

        annual_gross = license_subtotal + support_cost_annual

        # Multi-year commitment discount
        term_discount_pct = 0.15 if contract_duration_years >= 3 else 0.08 if contract_duration_years >= 2 else 0.0
        
        total_discount_pct = min(0.40, term_discount_pct + (custom_discount_pct / 100.0))
        discount_amount_annual = annual_gross * total_discount_pct

        annual_net = max(0.0, annual_gross - discount_amount_annual)
        total_contract_value = round(annual_net * contract_duration_years, 2)
        monthly_mrr = round(annual_net / 12.0, 2)

        return {
            "user_licenses": user_licenses,
            "contract_duration_years": contract_duration_years,
            "support_tier": support_tier,
            "annual_gross_price": round(annual_gross, 2),
            "term_discount_percentage": round(term_discount_pct * 100, 1),
            "custom_discount_percentage": custom_discount_pct,
            "effective_annual_net": round(annual_net, 2),
            "total_contract_value": total_contract_value,
            "monthly_recurring_revenue": monthly_mrr
        }
""")

    print("Created lead balancer, contract state machine, and pricing calculator.")

if __name__ == '__main__':
    run()
