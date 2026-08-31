from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseContractRenewalEngine:
    @staticmethod
    def calculate_auto_renewal_terms(
        contract: Dict[str, Any],
        standard_uplift_pct: float = 5.0,
        extend_years: int = 1
    ) -> Dict[str, Any]:
        curr_end_str = contract.get("termination_date") or date.today().isoformat()
        curr_end = date.fromisoformat(curr_end_str)
        curr_val = float(contract.get("contract_value", {}).get("total_amount", 0.0))

        new_val = round(curr_val * (1.0 + (standard_uplift_pct / 100.0)), 2)
        new_end = curr_end + timedelta(days=365 * extend_years)

        return {
            "original_contract_id": contract.get("id"),
            "renewal_effective_date": curr_end.isoformat(),
            "new_termination_date": new_end.isoformat(),
            "previous_annual_value": curr_val,
            "uplift_percentage": standard_uplift_pct,
            "new_annual_value": new_val,
            "auto_renew_status": "drafted"
        }
