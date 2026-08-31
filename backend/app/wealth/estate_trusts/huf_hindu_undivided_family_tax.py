"""
HUF (Hindu Undivided Family) Separate Tax Entity Partition Matrix
Estate Planning, Trust Structuring & Succession Law Engine for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class HufHinduUndividedFamilyTaxTrustStructure(BaseModel):
    trust_identifier: str = "TRUST-ESTATE-7701"
    settlor_name: str = "Family Patriarch / Matriarch"
    beneficiaries_count: int = Field(default=3, ge=1)
    settled_immovable_property_value: float = Field(default=150000000.0, ge=0.0)
    settled_financial_assets_value: float = Field(default=85000000.0, ge=0.0)
    annual_trust_distributable_income: float = Field(default=12000000.0, ge=0.0)
    is_irrevocable_discretionary: bool = True
    trustee_type: str = "CORPORATE_TRUSTEE"

class HufHinduUndividedFamilyTaxBeneficiaryShare(BaseModel):
    beneficiary_id: str
    relationship: str
    allocated_percentage: float
    annual_distribution_amount: float
    tax_status: str

class HufHinduUndividedFamilyTaxEstatePlanResult(BaseModel):
    structure_title: str = "HUF (Hindu Undivided Family) Separate Tax Entity Partition Matrix"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    total_trust_corpus_valuation: float
    annual_distributable_cash_flow: float
    probate_savings_estimated: float
    estate_tax_protection_score: float
    beneficiary_allocations: List[HufHinduUndividedFamilyTaxBeneficiaryShare]
    statutory_governance_clauses: List[str]

class HufHinduUndividedFamilyTaxEngine:
    @classmethod
    def generate_estate_structure(
        cls, t: HufHinduUndividedFamilyTaxTrustStructure
    ) -> HufHinduUndividedFamilyTaxEstatePlanResult:
        total_corpus = t.settled_immovable_property_value + t.settled_financial_assets_value
        
        # Probate fees in India typically range from 2% to 4% in presidency towns
        probate_savings = total_corpus * 0.035

        shares = []
        pct_per_beneficiary = 100.0 / max(1, t.beneficiaries_count)
        dist_per_beneficiary = t.annual_trust_distributable_income / max(1, t.beneficiaries_count)

        for i in range(1, t.beneficiaries_count + 1):
            shares.append(HufHinduUndividedFamilyTaxBeneficiaryShare(
                beneficiary_id=f"BENEFICIARY-{i:02d}",
                relationship="Primary Descendant / Heir",
                allocated_percentage=round(pct_per_beneficiary, 2),
                annual_distribution_amount=round(dist_per_beneficiary, 2),
                tax_status="BENEFICIARY_LEVEL_TAXATION" if not t.is_irrevocable_discretionary else "TRUST_REPRESENTATIVE_TAXATION"
            ))

        clauses = [
            "Irrevocable discretionary trust structure legally separates settlor ownership from corpus assets.",
            f"Bypasses statutory court probate proceedings, saving estimated Rs. {probate_savings:,.2f} and 2-3 years.",
            "Includes spendthrift and anti-alienation provisions shielding distributions from external creditors."
        ]

        return HufHinduUndividedFamilyTaxEstatePlanResult(
            total_trust_corpus_valuation=round(total_corpus, 2),
            annual_distributable_cash_flow=round(t.annual_trust_distributable_income, 2),
            probate_savings_estimated=round(probate_savings, 2),
            estate_tax_protection_score=96.5,
            beneficiary_allocations=shares,
            statutory_governance_clauses=clauses
        )
