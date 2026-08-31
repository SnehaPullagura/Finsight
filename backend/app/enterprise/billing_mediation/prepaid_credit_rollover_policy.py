from typing import Any, Dict, List, Optional

class PrepaidCreditRolloverPolicy:
    """
    Annual prepaid credit expiration & rollover calculator:
    Allows up to 20% unused credit rollover upon contract renewal execution.
    """
    @staticmethod
    def calculate_renewal_rollover(
        unused_credits_balance: float,
        is_contract_renewed: bool,
        max_rollover_percentage: float = 20.0
    ) -> Dict[str, Any]:
        if not is_contract_renewed:
            return {
                "unused_credits_balance": unused_credits_balance,
                "credits_rolled_over": 0.0,
                "credits_forfeited": unused_credits_balance,
                "policy_outcome": "ALL_CREDITS_EXPIRED_NO_RENEWAL"
            }

        max_allowed = round(unused_credits_balance * (max_rollover_percentage / 100.0), 2)
        forfeited = round(unused_credits_balance - max_allowed, 2)

        return {
            "unused_credits_balance": unused_credits_balance,
            "max_rollover_pct_allowed": max_rollover_percentage,
            "credits_rolled_over_to_new_term": max_allowed,
            "credits_forfeited": forfeited,
            "policy_outcome": "RENEWAL_ROLLOVER_APPLIED"
        }
