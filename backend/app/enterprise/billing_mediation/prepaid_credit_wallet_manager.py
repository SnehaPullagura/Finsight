from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class PrepaidCreditWalletManager:
    """
    Enterprise Prepaid Credit & Drawdown Wallet Manager:
    Draws down usage charges against upfront commit credits with automated low-balance replenishment alerts.
    """
    @staticmethod
    def process_usage_drawdown(
        current_wallet_balance: float,
        drawdown_amount: float,
        low_balance_threshold: float = 1000.0
    ) -> Dict[str, Any]:
        remaining_balance = round(current_wallet_balance - drawdown_amount, 2)
        is_low = remaining_balance <= low_balance_threshold
        is_exhausted = remaining_balance <= 0.0

        return {
            "starting_balance": current_wallet_balance,
            "drawdown_deducted": drawdown_amount,
            "ending_wallet_balance": remaining_balance,
            "is_low_balance_alert": is_low and not is_exhausted,
            "is_wallet_exhausted": is_exhausted,
            "recommended_action": "TRIGGER_PREPAID_TOP_UP" if is_low else "NORMAL_DRAWDOWN",
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
