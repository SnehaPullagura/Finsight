from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ContractClauseBuilder:
    STANDARD_CLAUSES = {
        "confidentiality": "Each party agrees to hold the other party's Confidential Information in strict confidence and not to disclose such Confidential Information to any third party.",
        "intellectual_property": "ClientFlow CRM retains all right, title, and interest in and to the platform, including all modifications, enhancements, and intellectual property rights.",
        "service_level_agreement": "Provider warrants that the Production Cloud Service shall maintain an uptime SLA of 99.9% in each calendar month.",
        "data_protection_gdpr": "Both parties shall comply with all applicable requirements of the General Data Protection Regulation (EU) 2016/679 (GDPR).",
        "governing_law": "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without giving effect to any choice of law rules."
    }

    @staticmethod
    def generate_contract_document(
        customer_name: str,
        total_contract_value: float,
        term_months: int,
        currency: str = "USD",
        custom_clauses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        start_date = date.today()
        end_date = start_date + timedelta(days=term_months * 30)

        clauses = dict(ContractClauseBuilder.STANDARD_CLAUSES)
        if custom_clauses:
            for i, c in enumerate(custom_clauses, 1):
                clauses[f"special_condition_{i}"] = c

        contract_payload = {
            "title": f"Enterprise Cloud Platform Master Services Agreement — {customer_name}",
            "customer_legal_name": customer_name,
            "effective_date": start_date.isoformat(),
            "termination_date": end_date.isoformat(),
            "contract_value": {
                "total_amount": total_contract_value,
                "currency": currency,
                "billing_schedule": "Annual Upfront" if term_months >= 12 else "Monthly Recurring"
            },
            "terms_and_conditions": clauses,
            "signature_required": True,
            "status": "ready_for_signature"
        }
        return contract_payload
