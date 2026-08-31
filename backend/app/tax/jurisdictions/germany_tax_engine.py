"""
Germany (Finanzamt Einkommensteuer, Solidaritätszuschlag, Kirchensteuer)
Multi-Jurisdiction Tax & Cross-Border Compliance Module.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel

class GermanyTaxBracket(BaseModel):
    bracket_index: int
    income_from: float
    income_to: Optional[float]
    rate_pct: float

class GermanyTaxCalculationResult(BaseModel):
    country: str = "Germany"
    gross_income: float
    total_deductions: float
    taxable_income: float
    total_tax_liability: float
    effective_tax_rate_pct: float
    marginal_tax_rate_pct: float

class GermanyTaxEngine:
    SLABS = [
        GermanyTaxBracket(bracket_index=1, income_from=0.0, income_to=250000.0, rate_pct=0.0),
        GermanyTaxBracket(bracket_index=2, income_from=250000.0, income_to=500000.0, rate_pct=5.0),
        GermanyTaxBracket(bracket_index=3, income_from=500000.0, income_to=1000000.0, rate_pct=15.0),
        GermanyTaxBracket(bracket_index=4, income_from=1000000.0, income_to=2000000.0, rate_pct=25.0),
        GermanyTaxBracket(bracket_index=5, income_from=2000000.0, income_to=None, rate_pct=30.0),
    ]

    @classmethod
    def compute_tax(cls, gross_income: float, deductions: float = 0.0) -> GermanyTaxCalculationResult:
        taxable = max(0.0, gross_income - deductions)
        tax = 0.0
        marginal = 0.0

        for slab in cls.SLABS:
            if taxable > slab.income_from:
                taxable_in_slab = taxable - slab.income_from
                if slab.income_to is not None:
                    taxable_in_slab = min(taxable_in_slab, slab.income_to - slab.income_from)
                tax += taxable_in_slab * (slab.rate_pct / 100.0)
                marginal = slab.rate_pct

        eff_rate = (tax / gross_income * 100.0) if gross_income > 0 else 0.0

        return GermanyTaxCalculationResult(
            gross_income=round(gross_income, 2),
            total_deductions=round(deductions, 2),
            taxable_income=round(taxable, 2),
            total_tax_liability=round(tax, 2),
            effective_tax_rate_pct=round(eff_rate, 2),
            marginal_tax_rate_pct=round(marginal, 2)
        )
