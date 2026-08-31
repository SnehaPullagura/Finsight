from typing import Any, Dict, List, Optional

class EnterpriseLeadRoutingRuleEvaluator:
    @staticmethod
    def route_lead_to_team(lead: Dict[str, Any]) -> Dict[str, Any]:
        emp = int(lead.get("employee_count", 0))
        country = (lead.get("country") or "US").upper()
        industry = (lead.get("industry") or "technology").lower()

        if emp >= 1000:
            team = "Strategic Enterprise Team"
            sla_min = 15
        elif emp >= 250:
            team = "Mid-Market Growth Team"
            sla_min = 60
        else:
            team = "Inbound SMB Team"
            sla_min = 120

        return {
            "lead_id": lead.get("id"),
            "assigned_team": team,
            "sla_response_minutes": sla_min,
            "territory_country": country,
            "industry_segment": industry
        }
