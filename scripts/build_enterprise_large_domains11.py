import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/deal_stage_gate_validator.py
    write_file("backend/app/enterprise/deal_stage_gate_validator.py", """from typing import Any, Dict, List, Tuple

class DealStageGateValidator:
    GATE_REQUIREMENTS = {
        "discovery": ["contact_id", "company_id", "lead_source"],
        "scoping": ["estimated_budget", "decision_maker_identified"],
        "proposal": ["proposal_document_id", "line_items_count"],
        "negotiation": ["legal_review_approved", "contract_terms_agreed"],
        "closed_won": ["signed_contract_id", "payment_method_verified"]
    }

    @staticmethod
    def validate_stage_transition(
        target_stage: str,
        deal_attributes: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        stage_key = target_stage.lower()
        required_fields = DealStageGateValidator.GATE_REQUIREMENTS.get(stage_key, [])

        missing_fields = []
        for req in required_fields:
            val = deal_attributes.get(req)
            if val is None or val == "" or val is False:
                missing_fields.append(req)

        is_valid = len(missing_fields) == 0
        return is_valid, missing_fields
""")

    # 2. backend/app/enterprise/contract_compliance_evaluator.py
    write_file("backend/app/enterprise/contract_compliance_evaluator.py", """from datetime import date
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
""")

    # 3. backend/app/enterprise/multi_currency_exchange_matrix.py
    write_file("backend/app/enterprise/multi_currency_exchange_matrix.py", """from typing import Dict, List, Optional

class MultiCurrencyExchangeMatrix:
    RATES_TO_USD = {
        "USD": 1.0,
        "EUR": 1.087,
        "GBP": 1.265,
        "CAD": 0.735,
        "AUD": 0.658,
        "JPY": 0.00644,
        "INR": 0.0120,
        "SGD": 0.741,
        "CHF": 1.10
    }

    @staticmethod
    def convert_amount(amount: float, source_currency: str, target_currency: str) -> float:
        src = source_currency.upper()
        dst = target_currency.upper()
        if src == dst:
            return round(amount, 2)

        usd_val = amount * MultiCurrencyExchangeMatrix.RATES_TO_USD.get(src, 1.0)
        target_rate = MultiCurrencyExchangeMatrix.RATES_TO_USD.get(dst, 1.0)
        final_val = usd_val / target_rate
        return round(final_val, 2)
""")

    print("Created stage gate validator, compliance evaluator, and currency matrix.")

if __name__ == '__main__':
    run()
