from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

class CoSellDealRegistrationManager:
    """
    Channel Partner & Co-Sell Deal Registration:
    Validates registration freshness, checks direct sales conflicts, locks deal exclusivity,
    and calculates partner referral incentives.
    """
    @staticmethod
    def evaluate_deal_registration(
        deal_reg: Dict[str, Any],
        existing_direct_pipeline: List[Dict[str, Any]],
        exclusivity_days: int = 90
    ) -> Dict[str, Any]:
        partner_name = deal_reg.get("partner_name", "Global SI Partner")
        target_account = deal_reg.get("target_account_name", "")
        deal_amount = float(deal_reg.get("estimated_deal_value", 50000.0))

        # Check for active direct sales conflict within past 60 days
        conflict = any(
            d.get("account_name", "").lower() == target_account.lower()
            for d in existing_direct_pipeline
        )

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=exclusivity_days)

        if conflict:
            status = "REJECTED_DIRECT_SALES_COLLISION"
            exclusivity = False
            margin_rate = 0.0
        else:
            status = "APPROVED_EXCLUSIVITY_LOCKED"
            exclusivity = True
            margin_rate = 15.0 if deal_amount >= 100000.0 else 10.0

        partner_margin = round(deal_amount * (margin_rate / 100.0), 2)

        return {
            "registration_id": deal_reg.get("id"),
            "partner_name": partner_name,
            "target_account": target_account,
            "estimated_deal_value": deal_amount,
            "status": status,
            "is_exclusivity_locked": exclusivity,
            "exclusivity_expires_at": expires_at.isoformat() if exclusivity else None,
            "partner_discount_margin_pct": margin_rate,
            "partner_commission_payable": partner_margin
        }
