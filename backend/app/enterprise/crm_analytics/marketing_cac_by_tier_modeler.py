from typing import Any, Dict, List, Optional

class TieredCACModeler:
    @staticmethod
    def calculate_tier_payback_metrics(
        enterprise_cac: float,
        midmarket_cac: float,
        smb_cac: float,
        enterprise_arpu: float,
        midmarket_arpu: float,
        smb_arpu: float,
        gross_margin_pct: float = 80.0
    ) -> Dict[str, Any]:
        margin = gross_margin_pct / 100.0

        ent_payback = round(enterprise_cac / max(1.0, enterprise_arpu * margin), 1)
        mid_payback = round(midmarket_cac / max(1.0, midmarket_arpu * margin), 1)
        smb_payback = round(smb_cac / max(1.0, smb_arpu * margin), 1)

        return {
            "enterprise": {"cac": enterprise_cac, "arpu": enterprise_arpu, "payback_months": ent_payback},
            "mid_market": {"cac": midmarket_cac, "arpu": midmarket_arpu, "payback_months": mid_payback},
            "smb": {"cac": smb_cac, "arpu": smb_arpu, "payback_months": smb_payback},
            "blended_average_payback_months": round((ent_payback + mid_payback + smb_payback) / 3.0, 1)
        }
