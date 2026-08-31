from typing import Any, Dict, List, Optional

class AIQBRDeckGenerator:
    @staticmethod
    def generate_qbr_briefing(company: Dict[str, Any], usage_metrics: Dict[str, Any]) -> Dict[str, Any]:
        cname = company.get("name")
        total_sessions = usage_metrics.get("total_sessions_qtr", 12000)
        time_saved_hours = round(total_sessions * 0.25, 1)

        return {
            "account_name": cname,
            "qbr_period": "Q3 2026",
            "business_impact_metrics": {
                "total_platform_sessions": total_sessions,
                "estimated_sales_hours_saved": time_saved_hours,
                "workflow_automations_executed": usage_metrics.get("automations_executed", 850),
                "proposals_generated": usage_metrics.get("proposals_count", 140)
            },
            "recommendations_for_next_quarter": [
                "Deploy CPQ Rule Configurator for custom bundles",
                "Integrate SSO SCIM automated user provisioning",
                "Activate AI Copilot automated meeting summaries"
            ],
            "readiness_status": "READY_FOR_EXECUTIVE_PRESENTATION"
        }
