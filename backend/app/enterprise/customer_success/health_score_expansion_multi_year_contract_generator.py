from typing import Any, Dict, List, Optional

class MultiYearContractPayloadGenerator:
    @staticmethod
    def generate_contract_agreement(account: Dict[str, Any], term_years: int, annual_rate: float) -> Dict[str, Any]:
        cname = account.get("name")
        total_tcv = annual_rate * term_years

        return {
            "agreement_title": f"Master Services Agreement Multi-Year Extension — {cname}",
            "account_name": cname,
            "term_commitment_years": term_years,
            "committed_annual_run_rate": round(annual_rate, 2),
            "total_contract_value_tcv": round(total_tcv, 2),
            "payment_terms": "Net 30 Annual Invoicing",
            "sla_tier": "Mission Critical 99.99% Availability",
            "legal_status": "DRAFT_READY_FOR_ESIGNATURE"
        }
