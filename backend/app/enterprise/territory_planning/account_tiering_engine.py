from typing import Any, Dict, List, Optional

class EnterpriseAccountTieringEngine:
    """
    Algorithmic Enterprise Account Tiering:
    Assigns Tier 1 (Strategic / Named), Tier 2 (Enterprise), and Tier 3 (Commercial)
    based on employee size, tech stack signals, funding, and revenue scale.
    """
    @staticmethod
    def classify_account_tier(account: Dict[str, Any]) -> Dict[str, Any]:
        employees = int(account.get("employee_count", 50))
        annual_rev = float(account.get("annual_revenue", 1000000.0))
        has_enterprise_crm = bool(account.get("uses_enterprise_tech_stack", False))
        funding_m = float(account.get("total_funding_millions", 0.0))

        # Scoring index: 0 to 100
        score = 0
        if employees >= 5000:
            score += 40
        elif employees >= 1000:
            score += 30
        elif employees >= 250:
            score += 20
        else:
            score += 10

        if annual_rev >= 100000000.0: # $100M+
            score += 35
        elif annual_rev >= 25000000.0: # $25M+
            score += 25
        elif annual_rev >= 5000000.0:
            score += 15
        else:
            score += 5

        if has_enterprise_crm:
            score += 15
        if funding_m >= 50.0:
            score += 10

        if score >= 75:
            tier = "TIER_1_STRATEGIC_NAMED"
            touch_model = "Dedicated Enterprise Account Executive & Named Solutions Architect"
            cadence = "Weekly Custom Outreach & Executive Alignment"
        elif score >= 50:
            tier = "TIER_2_ENTERPRISE"
            touch_model = "Territory Account Executive & Pooled Sales Engineering"
            cadence = "Bi-Weekly Multichannel Cadence"
        else:
            tier = "TIER_3_COMMERCIAL"
            touch_model = "Inside Sales & Automated Product-Led Nurture"
            cadence = "Automated Marketing & Inbound SDR Follow-Up"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "tier_score": score,
            "assigned_tier": tier,
            "recommended_touch_model": touch_model,
            "sales_cadence": cadence
        }
