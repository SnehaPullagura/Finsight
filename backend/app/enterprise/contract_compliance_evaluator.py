from datetime import date
from typing import Any, Dict, List, Optional

class ContractComplianceEvaluator:
    @staticmethod
    def evaluate_contract_risk(contract_payload: Dict[str, Any]) -> Dict[str, Any]:
        clauses = contract_payload.get("terms_and_conditions", {})
        risk_flags = []

        # Check required mandatory compliance clauses
        if "data_protection_gdpr" not in clauses:
            risk_flags.append("Missing GDPR Data Protection Agreement clause")
        if "service_level_agreement" not in clauses:
            risk_flags.append("Missing explicit Uptime Service Level Agreement (SLA)")
        if "confidentiality" not in clauses:
            risk_flags.append("Missing Mutual Non-Disclosure / Confidentiality clause")

        val = float(contract_payload.get("contract_value", {}).get("total_amount", 0.0))
        if val >= 500000 and "executive_approval" not in contract_payload:
            risk_flags.append("Contracts >= $500,000 require VP / Executive signoff")

        risk_score = len(risk_flags) * 25
        risk_tier = "low" if risk_score == 0 else "medium" if risk_score <= 50 else "high"

        return {
            "risk_score": min(100, risk_score),
            "risk_tier": risk_tier,
            "compliance_flags": risk_flags,
            "is_ready_for_execution": len(risk_flags) == 0
        }
