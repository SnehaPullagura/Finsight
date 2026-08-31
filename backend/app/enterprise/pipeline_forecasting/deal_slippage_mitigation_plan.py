from typing import Any, Dict, List, Optional

class DealSlippageMitigationPlan:
    """
    Prescribes targeted concession packages to prevent quarter-end deal slippage.
    """
    @staticmethod
    def generate_mitigation_offer(deal: Dict[str, Any]) -> Dict[str, Any]:
        dname = deal.get("name")
        val = float(deal.get("value", 0.0))

        concessions = [
            "Waive first 3 months implementation fee ($15,000 value)",
            "Lock in 10% multi-year discount upon signature by quarter close",
            "Include 1 complimentary named TAM seat for first 90 days"
        ]

        return {
            "deal_name": dname,
            "contract_value": val,
            "slippage_mitigation_package": concessions,
            "required_cro_approval": val >= 100000.0,
            "expected_pull_forward_success_rate_pct": 72.5
        }
