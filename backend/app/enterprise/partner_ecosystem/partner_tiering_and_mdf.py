from typing import Any, Dict, List, Optional

class PartnerTieringAndMDFManager:
    """
    Partner Leveling (Authorized, Silver, Gold, Platinum) & Market Development Funds (MDF):
    Calculates partner tier status and allocates quarterly marketing funds.
    """
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
