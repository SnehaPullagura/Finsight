import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/pipeline_forecasting_service.py
    write_file("backend/app/domain_services/pipeline_forecasting_service.py", """import math
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class AdvancedPipelineForecastingService:
    @staticmethod
    def calculate_category_rollups(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        categories = {
            "closed": {"count": 0, "amount": 0.0, "deals": []},
            "commit": {"count": 0, "amount": 0.0, "deals": []},
            "best_case": {"count": 0, "amount": 0.0, "deals": []},
            "pipeline": {"count": 0, "amount": 0.0, "deals": []},
            "omitted": {"count": 0, "amount": 0.0, "deals": []}
        }

        for d in deals:
            status = (d.get("status") or "open").lower()
            stage = (d.get("stage") or "").lower()
            val = float(d.get("value", 0.0))
            prob = float(d.get("probability", 0.0))

            if status == "won":
                cat = "closed"
            elif status == "lost":
                cat = "omitted"
            elif prob >= 85 or stage in ["negotiation", "contract"]:
                cat = "commit"
            elif prob >= 50 or stage in ["proposal", "demo"]:
                cat = "best_case"
            else:
                cat = "pipeline"

            categories[cat]["count"] += 1
            categories[cat]["amount"] = round(categories[cat]["amount"] + val, 2)
            categories[cat]["deals"].append(d)

        total_open = categories["commit"]["amount"] + categories["best_case"]["amount"] + categories["pipeline"]["amount"]

        return {
            "categories": {k: {"count": v["count"], "amount": v["amount"]} for k, v in categories.items()},
            "summary": {
                "total_closed_won": categories["closed"]["amount"],
                "total_commit": categories["commit"]["amount"],
                "total_best_case": categories["best_case"]["amount"],
                "total_open_pipeline": round(total_open, 2),
                "expected_quarter_finish": round(categories["closed"]["amount"] + categories["commit"]["amount"] + (categories["best_case"]["amount"] * 0.5), 2)
            }
        }
""")

    # 2. backend/app/domain_services/abac_policy_evaluator.py
    write_file("backend/app/domain_services/abac_policy_evaluator.py", """from typing import Any, Dict, List, Optional

class ABACPolicyRule:
    def __init__(self, rule_id: str, action: str, resource_type: str, condition_fn: Any):
        self.rule_id = rule_id
        self.action = action # read, write, delete, export, approve
        self.resource_type = resource_type # deal, contact, organization, invoice, audit
        self.condition_fn = condition_fn

class ABACPolicyEvaluator:
    def __init__(self, rules: Optional[List[ABACPolicyRule]] = None):
        self.rules = rules or []

    def evaluate(self, user_context: Dict[str, Any], resource: Dict[str, Any], action: str, resource_type: str) -> Dict[str, Any]:
        # 1. Superuser override
        if user_context.get("is_superuser") or "Admin" in user_context.get("roles", []):
            return {"allowed": True, "reason": "Superuser / Admin override permitted"}

        # 2. Tenant isolation check
        user_tenant = user_context.get("tenant_id")
        resource_tenant = resource.get("tenant_id")
        if user_tenant and resource_tenant and user_tenant != resource_tenant:
            return {"allowed": False, "reason": "Cross-tenant access violation"}

        # 3. Ownership check
        if resource.get("owner_id") == user_context.get("id") or resource.get("user_id") == user_context.get("id"):
            return {"allowed": True, "reason": "Resource owner access permitted"}

        return {"allowed": True, "reason": "Default RBAC role permitted"}
""")

    # 3. backend/app/domain_services/contract_amendment_engine.py
    write_file("backend/app/domain_services/contract_amendment_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ContractAmendmentEngine:
    @staticmethod
    def create_co_termed_amendment(
        original_contract: Dict[str, Any],
        added_products: List[Dict[str, Any]],
        amendment_effective_date: date
    ) -> Dict[str, Any]:
        contract_end = date.fromisoformat(original_contract.get("termination_date", date.today().isoformat()))
        contract_start = date.fromisoformat(original_contract.get("effective_date", date.today().isoformat()))

        total_days = max(1, (contract_end - contract_start).days)
        remaining_days = max(0, (contract_end - amendment_effective_date).days)
        proration_factor = remaining_days / float(total_days)

        amendment_items = []
        total_amendment_cost = 0.0

        for p in added_products:
            annual_price = float(p.get("unit_price", 0.0)) * int(p.get("quantity", 1))
            prorated_price = round(annual_price * proration_factor, 2)
            total_amendment_cost += prorated_price

            amendment_items.append({
                "product_id": p.get("product_id"),
                "name": p.get("name"),
                "quantity": p.get("quantity", 1),
                "full_period_price": annual_price,
                "prorated_cost": prorated_price,
                "days_remaining": remaining_days
            })

        return {
            "original_contract_id": original_contract.get("id"),
            "effective_date": amendment_effective_date.isoformat(),
            "co_termed_termination_date": contract_end.isoformat(),
            "amendment_items": amendment_items,
            "total_amendment_cost": round(total_amendment_cost, 2),
            "new_annualized_contract_value": round(float(original_contract.get("contract_value", {}).get("total_amount", 0.0)) + sum(p.get("unit_price", 0.0) * p.get("quantity", 1) for p in added_products), 2)
        }
""")

    print("Created pipeline forecasting, ABAC evaluator, and amendment engine.")

if __name__ == '__main__':
    run()
