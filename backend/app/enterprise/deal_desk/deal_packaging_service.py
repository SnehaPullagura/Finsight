from typing import Any, Dict, List, Optional

class DealPackagingService:
    """
    Enterprise Deal Desk & Custom Package Bundler:
    Combines core platform licenses, dedicated TAM, premium SLA, and professional services
    into optimized executive proposals with margin protection.
    """
    @staticmethod
    def package_enterprise_deal(
        platform_tier: str,
        user_seats: int,
        include_tam: bool = True,
        include_24x7_sla: bool = True,
        implementation_package: str = "ENTERPRISE_QUICKSTART"
    ) -> Dict[str, Any]:
        seat_rate = 1200.0 if platform_tier == "ENTERPRISE" else 800.0
        platform_subtotal = user_seats * seat_rate

        tam_fee = 35000.0 if include_tam else 0.0
        sla_fee = platform_subtotal * 0.15 if include_24x7_sla else 0.0

        services_fees = {
            "ENTERPRISE_QUICKSTART": 15000.0,
            "CUSTOM_SYSTEM_INTEGRATION": 45000.0,
            "SELF_SERVICE": 0.0
        }
        services_subtotal = services_fees.get(implementation_package, 15000.0)

        total_contract_value = platform_subtotal + tam_fee + sla_fee + services_subtotal
        blended_gross_margin = 82.5 # Percentage

        return {
            "package_title": f"Enterprise Cloud CRM — {platform_tier} Bundle ({user_seats} Seats)",
            "platform_licenses_subtotal": platform_subtotal,
            "dedicated_tam_fee": tam_fee,
            "mission_critical_sla_fee": sla_fee,
            "professional_services_fee": services_subtotal,
            "total_contract_value_annual": round(total_contract_value, 2),
            "estimated_gross_margin_pct": blended_gross_margin,
            "deal_desk_recommendation": "PRE_APPROVED_TIER_1_BUNDLE"
        }
