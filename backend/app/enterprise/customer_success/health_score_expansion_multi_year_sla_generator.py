from typing import Any, Dict, List, Optional

class MultiYearSLAPackageGenerator:
    @staticmethod
    def generate_sla_package(sla_tier: str = "MISSION_CRITICAL") -> Dict[str, Any]:
        return {
            "sla_tier": sla_tier,
            "uptime_commitment_pct": 99.99,
            "sev1_response_time_minutes": 15,
            "sev2_response_time_hours": 2,
            "dedicated_named_tam_assigned": True,
            "financial_service_credits": {
                "below_99_9pct": "10% Monthly Credit",
                "below_99_5pct": "25% Monthly Credit",
                "below_99_0pct": "50% Monthly Credit"
            },
            "sla_status": "BINDING_CONTRACT_ATTACHED"
        }
