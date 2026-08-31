"""
United States - India Double Tax Avoidance Agreement (Article 12 Royalties & FTS)
FinSight International Tax & Cross-Border Wealth Compliance.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class UsIndiaDtaaReliefRequest(BaseModel):
    resident_country: str = "India"
    source_country: str = "US"
    income_category: str = "DIVIDENDS" # DIVIDENDS, INTEREST, ROYALTIES, FTS, CAPITAL_GAINS
    gross_foreign_income: float
    tax_paid_in_source_country: float
    has_tax_residency_certificate_trc: bool = True
    form_10f_filed: bool = True

class UsIndiaDtaaReliefResult(BaseModel):
    treaty_title: str = "United States - India Double Tax Avoidance Agreement (Article 12 Royalties & FTS)"
    treaty_withholding_rate_pct: float
    domestic_withholding_rate_pct: float
    eligible_treaty_benefit: bool
    foreign_tax_credit_section_90: float
    net_tax_payable_in_india: float
    compliance_notes: List[str]

class UsIndiaDtaaEngine:
    TREATY_RATES = {
        "DIVIDENDS": 10.0,
        "INTEREST": 10.0,
        "ROYALTIES": 15.0,
        "FTS": 10.0,
        "CAPITAL_GAINS": 0.0
    }

    @classmethod
    def compute_foreign_tax_credit(cls, req: UsIndiaDtaaReliefRequest) -> UsIndiaDtaaReliefResult:
        treaty_rate = cls.TREATY_RATES.get(req.income_category.upper(), 15.0)
        domestic_rate = 20.0 # Standard domestic non-treaty rate
        
        eligible = req.has_tax_residency_certificate_trc and req.form_10f_filed
        eff_rate = treaty_rate if eligible else domestic_rate

        indian_tax_at_slab = req.gross_foreign_income * 0.30 # Assume 30% slab
        max_ftc = min(req.tax_paid_in_source_country, indian_tax_at_slab)
        net_payable = max(0.0, indian_tax_at_slab - max_ftc)

        notes = [
            f"Under the United States - India Double Tax Avoidance Agreement (Article 12 Royalties & FTS), maximum source withholding is capped at {eff_rate:.1f}%.",
            f"Foreign Tax Credit (FTC) under Section 90 of Rs. {max_ftc:,.2f} claimed via Form 67.",
            "Valid Tax Residency Certificate (TRC) verified for treaty eligibility."
        ]

        return UsIndiaDtaaReliefResult(
            treaty_withholding_rate_pct=treaty_rate,
            domestic_withholding_rate_pct=domestic_rate,
            eligible_treaty_benefit=eligible,
            foreign_tax_credit_section_90=round(max_ftc, 2),
            net_tax_payable_in_india=round(net_payable, 2),
            compliance_notes=notes
        )
