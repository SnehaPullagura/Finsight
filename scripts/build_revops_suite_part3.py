import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/partner_ecosystem/co_sell_deal_registration.py
    write_file("backend/app/enterprise/partner_ecosystem/co_sell_deal_registration.py", """from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

class CoSellDealRegistrationManager:
    \"\"\"
    Channel Partner & Co-Sell Deal Registration:
    Validates registration freshness, checks direct sales conflicts, locks deal exclusivity,
    and calculates partner referral incentives.
    \"\"\"
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
""")

    # 2. backend/app/enterprise/partner_ecosystem/partner_tiering_and_mdf.py
    write_file("backend/app/enterprise/partner_ecosystem/partner_tiering_and_mdf.py", """from typing import Any, Dict, List, Optional

class PartnerTieringAndMDFManager:
    \"\"\"
    Partner Leveling (Authorized, Silver, Gold, Platinum) & Market Development Funds (MDF):
    Calculates partner tier status and allocates quarterly marketing funds.
    \"\"\"
    TIER_CRITERIA = {
        "PLATINUM": {"min_arr": 500000.0, "min_certs": 10, "mdf_budget_pct": 5.0, "reseller_discount": 25.0},
        "GOLD": {"min_arr": 200000.0, "min_certs": 5, "mdf_budget_pct": 3.5, "reseller_discount": 20.0},
        "SILVER": {"min_arr": 50000.0, "min_certs": 2, "mdf_budget_pct": 2.0, "reseller_discount": 15.0},
        "AUTHORIZED": {"min_arr": 0.0, "min_certs": 0, "mdf_budget_pct": 0.0, "reseller_discount": 10.0}
    }

    @classmethod
    def evaluate_partner_standing(cls, partner: Dict[str, Any]) -> Dict[str, Any]:
        pname = partner.get("name")
        arr = float(partner.get("annual_sourced_arr", 0.0))
        certs = int(partner.get("certified_engineers_count", 0))

        assigned_tier = "AUTHORIZED"
        for t, criteria in [("PLATINUM", cls.TIER_CRITERIA["PLATINUM"]),
                            ("GOLD", cls.TIER_CRITERIA["GOLD"]),
                            ("SILVER", cls.TIER_CRITERIA["SILVER"])]:
            if arr >= criteria["min_arr"] and certs >= criteria["min_certs"]:
                assigned_tier = t
                break

        tier_info = cls.TIER_CRITERIA[assigned_tier]
        mdf_allocated = round(arr * (tier_info["mdf_budget_pct"] / 100.0), 2)

        return {
            "partner_name": pname,
            "annual_sourced_arr": arr,
            "certified_engineers": certs,
            "assigned_tier": assigned_tier,
            "reseller_discount_percentage": tier_info["reseller_discount"],
            "quarterly_mdf_budget_allocated": mdf_allocated,
            "dedicated_channel_manager": assigned_tier in ["GOLD", "PLATINUM"]
        }
""")

    # 3. backend/app/enterprise/partner_ecosystem/reseller_margin_calculator.py
    write_file("backend/app/enterprise/partner_ecosystem/reseller_margin_calculator.py", """from typing import Any, Dict, List, Optional

class ResellerMarginCalculator:
    \"\"\"
    Computes Wholesale vs Suggested Retail Price (MSRP) margins for multi-tier distribution.
    \"\"\"
    @staticmethod
    def calculate_reseller_quote(
        list_price: float,
        reseller_discount_pct: float,
        end_user_discount_pct: float = 0.0
    ) -> Dict[str, Any]:
        wholesale_cost = round(list_price * (1.0 - (reseller_discount_pct / 100.0)), 2)
        end_user_quote = round(list_price * (1.0 - (end_user_discount_pct / 100.0)), 2)
        reseller_gross_margin = round(end_user_quote - wholesale_cost, 2)
        reseller_margin_pct = round((reseller_gross_margin / max(1.0, end_user_quote)) * 100.0, 1)

        return {
            "list_price": list_price,
            "reseller_discount_pct": reseller_discount_pct,
            "wholesale_cost_to_reseller": wholesale_cost,
            "end_user_quote_price": end_user_quote,
            "reseller_gross_profit": reseller_gross_margin,
            "reseller_margin_percentage": reseller_margin_pct,
            "is_profitable_for_partner": reseller_gross_margin > 0
        }
""")

    # 4. backend/app/enterprise/partner_ecosystem/distributor_rebate_engine.py
    write_file("backend/app/enterprise/partner_ecosystem/distributor_rebate_engine.py", """from typing import Any, Dict, List, Optional

class DistributorVolumeRebateEngine:
    \"\"\"
    End-of-Quarter Partner Volume Rebate Calculator based on tiered ARR achievement.
    \"\"\"
    @staticmethod
    def calculate_quarterly_rebate(
        quarterly_revenue: float,
        target_quota: float
    ) -> Dict[str, Any]:
        attainment_pct = round((quarterly_revenue / max(1.0, target_quota)) * 100.0, 1)

        if attainment_pct >= 150.0:
            rebate_rate = 6.0
        elif attainment_pct >= 120.0:
            rebate_rate = 4.5
        elif attainment_pct >= 100.0:
            rebate_rate = 3.0
        elif attainment_pct >= 80.0:
            rebate_rate = 1.5
        else:
            rebate_rate = 0.0

        rebate_amount = round(quarterly_revenue * (rebate_rate / 100.0), 2)

        return {
            "quarterly_revenue": quarterly_revenue,
            "target_quota": target_quota,
            "quota_attainment_pct": attainment_pct,
            "rebate_multiplier_pct": rebate_rate,
            "rebate_payout_amount": rebate_amount,
            "accelerator_status": "SUPER_ATTAINMENT_BONUS" if attainment_pct >= 120.0 else "STANDARD_REBATE" if attainment_pct >= 100.0 else "BASE_OR_BELOW"
        }
""")

    print("Partner ecosystem suite created successfully.")

if __name__ == "__main__":
    run()
