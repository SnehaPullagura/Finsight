from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class SPIFFIncentiveEngine:
    """
    Special Performance Incentive Funds (SPIFFs):
    Calculates instant cash kickers for strategic product add-ons, multi-year prepayments, and competitive takeovers.
    """
    @staticmethod
    def calculate_deal_spiffs(deal: Dict[str, Any]) -> Dict[str, Any]:
        deal_name = deal.get("name")
        val = float(deal.get("value", 0.0))
        is_multi_year = bool(deal.get("is_multi_year", False))
        is_competitive_rip = bool(deal.get("is_competitive_takeover", False))
        has_ai_copilot = bool(deal.get("has_ai_copilot_addon", False))

        earned_spiffs = []
        total_spiff_payout = 0.0

        if is_multi_year and val >= 50000.0:
            bonus = 2500.0
            earned_spiffs.append({"spiff_name": "Multi-Year Enterprise Commitment Bonus", "amount": bonus})
            total_spiff_payout += bonus

        if is_competitive_rip:
            bonus = 3000.0
            earned_spiffs.append({"spiff_name": "Legacy Competitor Takeover Bounty", "amount": bonus})
            total_spiff_payout += bonus

        if has_ai_copilot:
            bonus = 1000.0
            earned_spiffs.append({"spiff_name": "AI Copilot Strategic Adoption Kicker", "amount": bonus})
            total_spiff_payout += bonus

        return {
            "deal_name": deal_name,
            "deal_value": val,
            "earned_spiffs_count": len(earned_spiffs),
            "earned_spiffs_detail": earned_spiffs,
            "total_spiff_payout": total_spiff_payout,
            "disbursed_in_payroll_cycle": "NEXT_SCHEDULED_CYCLE"
        }
